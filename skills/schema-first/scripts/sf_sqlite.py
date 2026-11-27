"""Snapshot of a SQLite database, read from the database itself. Standard library only, read-only.

Beyond names and declared types it records what queries go wrong on: how values are stored (flags, date text,
epoch integers, numbers as text), which column joins to which key (declared, or inferred from the values),
and for two columns that point at the same table whether a pair is stored once, twice or directed.
"""
from __future__ import annotations

import re
import sqlite3
from pathlib import Path

from sf_format import SEP, digest, fmt_value, today
from sf_profile import describe, tokens

SELF_REFERENCE = re.compile(r"(parent|manager|mgr|supervisor|reports|referr|predecessor|successor|prev|next|ancestor|repl(y|ies))", re.I)
LABEL_NAMES = re.compile(r"(name|title|label|nick|handle|code|slug|login|email)", re.I)
EXTRA_DDL = re.compile(r"--|/\*|\bCHECK\b|\bGENERATED\b|\bCOLLATE\b|\bDEFAULT\b|\bWITHOUT\s+ROWID\b", re.I)


def q(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def connect(path: str) -> sqlite3.Connection:
    file = Path(path)
    if not file.is_file():
        raise FileNotFoundError(path)
    return sqlite3.connect(file.resolve().as_uri() + "?mode=ro", uri=True)


def schema_rows(con: sqlite3.Connection) -> list[tuple]:
    return con.execute("SELECT type, name, tbl_name, coalesce(sql, '') FROM sqlite_master "
                       "WHERE name NOT LIKE 'sqlite_%' ORDER BY type, name").fetchall()


def fingerprint(path: str) -> str:
    con = connect(path)
    try:
        return digest(*[" ".join(row) for row in schema_rows(con)])
    finally:
        con.close()


class Column:
    def __init__(self, name, decl, notnull, pk):
        self.name, self.decl, self.notnull, self.pk = name, (decl or "").upper() or "(no type)", bool(notnull), pk
        self.non_null = self.distinct = 0
        self.low = self.high = None
        self.storage: dict[str, int] = {}
        self.top: list[tuple] = []
        self.sample: list = []
        self.unique = False
        self.ref: tuple[str, str, str] | None = None   # (table, column, "foreign key" | "inferred ...")
        self.alternatives: list[str] = []


class Table:
    def __init__(self, name, sql):
        self.name, self.sql = name, sql
        self.columns: list[Column] = []
        self.rows = 0
        self.profiled = 0
        self.indexes: list[str] = []
        self.unique_sets: list[list[str]] = []
        self.pair_lines: list[str] = []
        self.error = ""

    def col(self, name: str) -> Column | None:
        return next((c for c in self.columns if c.name == name), None)

    def pk(self) -> list[str]:
        return [c.name for c in sorted((c for c in self.columns if c.pk), key=lambda c: c.pk)]

    def label_column(self) -> str | None:
        texts = [c for c in self.columns if "text" in c.storage and not c.ref]
        for pool in ([c for c in texts if c.unique], [c for c in texts if LABEL_NAMES.search(c.name)]):
            if pool:
                return pool[0].name
        return None


def read_tables(con: sqlite3.Connection, max_rows: int) -> list[Table]:
    tables = []
    for kind, name, _tbl, sql in schema_rows(con):
        if kind != "table":
            continue
        table = Table(name, sql)
        tables.append(table)
        try:
            try:
                info = con.execute(f"PRAGMA table_xinfo({q(name)})").fetchall()
            except sqlite3.Error:
                info = [row + (0,) for row in con.execute(f"PRAGMA table_info({q(name)})").fetchall()]
            table.columns = [Column(r[1], r[2], r[3], r[5]) for r in info if r[6] in (0, 2, 3)]
            table.rows = con.execute(f"SELECT count(*) FROM {q(name)}").fetchone()[0]
            table.profiled = min(table.rows, max_rows)
            src = q(name) if table.rows <= max_rows else f"(SELECT * FROM {q(name)} LIMIT {max_rows})"
            for col in table.columns:
                c = q(col.name)
                col.non_null, col.distinct, col.low, col.high = con.execute(
                    f"SELECT count({c}), count(DISTINCT {c}), min({c}), max({c}) FROM {src}").fetchone()
                col.storage = dict(con.execute(
                    f"SELECT typeof({c}), count(*) FROM {src} WHERE {c} IS NOT NULL GROUP BY 1").fetchall())
                col.top = con.execute(f"SELECT {c}, count(*) AS n FROM {src} WHERE {c} IS NOT NULL "
                                      f"GROUP BY {c} ORDER BY n DESC, {c} LIMIT 9").fetchall()
                col.sample = [r[0] for r in con.execute(
                    f"SELECT DISTINCT {c} FROM {src} WHERE {c} IS NOT NULL LIMIT 400").fetchall()]
            for _seq, index, unique, origin, *_rest in con.execute(f"PRAGMA index_list({q(name)})").fetchall():
                cols = [r[2] for r in con.execute(f"PRAGMA index_info({q(index)})").fetchall()]
                if unique:
                    table.unique_sets.append(cols)
                    if len(cols) == 1 and table.col(cols[0]):
                        table.col(cols[0]).unique = True
                if origin == "c":
                    table.indexes.append(f"{index}({', '.join(str(c) for c in cols)})" + (" unique" if unique else ""))
            pk = table.pk()
            if len(pk) == 1:
                table.col(pk[0]).unique = True
        except sqlite3.Error as exc:
            table.error = str(exc)
    return tables


def resolve_references(con: sqlite3.Connection, tables: list[Table], max_rows: int) -> None:
    by_name = {t.name.lower(): t for t in tables}
    # Declared foreign keys first: they are the store's own statement.
    for table in tables:
        try:
            fks = con.execute(f"PRAGMA foreign_key_list({q(table.name)})").fetchall()
        except sqlite3.Error:
            fks = []
        for _id, _seq, target, source, to, *_rest in fks:
            col, other = table.col(source), by_name.get(str(target).lower())
            if col is None:
                continue
            if to is None and other is not None and len(other.pk()) == 1:
                to = other.pk()[0]
            col.ref = (other.name if other else str(target), to or "?", "foreign key")
    # Then inference: a column whose every value is a key of another table, backed by its name.
    keys: dict[tuple[str, str], set] = {}
    for table in tables:
        if table.error or table.rows == 0 or table.rows > max_rows:
            continue
        for col in table.columns:
            if col.unique and col.non_null:
                keys[(table.name, col.name)] = {r[0] for r in con.execute(
                    f"SELECT {q(col.name)} FROM {q(table.name)} WHERE {q(col.name)} IS NOT NULL").fetchall()}
    for table in tables:
        if table.error:
            continue
        for col in table.columns:
            if col.ref or col.unique or col.distinct == 0 or set(col.storage) - {"integer", "text"}:
                continue
            values = set(col.sample)
            found = []
            for (other, key), keyset in keys.items():
                if not values <= keyset:
                    continue
                shared = tokens(col.name) & (tokens(other) | tokens(key))
                same = col.name.lower() == key.lower() and bool(tokens(key))
                if other == table.name and not SELF_REFERENCE.search(col.name):
                    continue   # a column named after its own table proves nothing; only a hierarchy-style name does
                found.append((len(shared) + (1 if same else 0) + (1 if other == table.name else 0), -len(keyset), other, key))
            found.sort(reverse=True)
            named = [f for f in found if f[0] > 0]
            is_text = set(col.storage) == {"text"}
            if named:
                best = named[0]
                col.ref = (best[2], best[3], "inferred: every value is a key there and the names agree")
                col.alternatives = [f"{f[2]}.{f[3]}" for f in named[1:3]]
            elif is_text and len(found) == 1 and col.distinct >= 3:
                col.ref = (found[0][2], found[0][3], "inferred: every value is a key there")


def pair_line(con, table: Table, a: Column, b: Column, target: Table | None, max_rows: int, samples: bool) -> str:
    rows = con.execute(f"SELECT {q(a.name)}, {q(b.name)} FROM {q(table.name)} "
                       f"WHERE {q(a.name)} IS NOT NULL AND {q(b.name)} IS NOT NULL LIMIT {max_rows}").fetchall()
    if not rows:
        return ""
    pairs = set(rows)
    loops = sum(1 for x, y in rows if x == y)
    proper = [(x, y) for x, y in pairs if x != y]
    both = sum(1 for x, y in proper if (y, x) in pairs)
    try:
        a_first = sum(1 for x, y in proper if x < y)
    except TypeError:
        a_first = -1
    in_both = len({x for x, _y in pairs} & {y for _x, y in pairs})
    ordered = re.search(rf"CHECK\s*\(\s*\"?(?:{re.escape(a.name)}\"?\s*<=?\s*\"?{re.escape(b.name)}|{re.escape(b.name)}\"?\s*>=?\s*\"?{re.escape(a.name)})\b", table.sql, re.I) or \
        re.search(rf"CHECK\s*\(\s*\"?(?:{re.escape(b.name)}\"?\s*<=?\s*\"?{re.escape(a.name)}|{re.escape(a.name)}\"?\s*>=?\s*\"?{re.escape(b.name)})\b", table.sql, re.I)
    if not proper:
        storage = "only self-pairs"
    elif len(pairs) < 0.9 * len(rows):
        storage = ("the same pair occurs in many rows: a row is an event or record between the two, not one row per link, so "
                   "read each column for what it is named")
    elif ordered:
        storage = (f"a CHECK constraint fixes the order of the two columns and no pair is stored reversed: an unordered pair "
                   f"is stored once, so one member's links are the rows where it is in either column")
    elif both == len(proper):
        storage = "every pair is also stored reversed: a symmetric link is two rows, so count or sum it once if it is undirected"
    elif both == 0 and in_both == 0:
        storage = (f"no value appears in both columns and no pair is stored reversed: the two columns are different roles, "
                   f"read each for what it is named")
    elif both == 0 and a_first in (0, len(proper)):
        storage = (f"no pair is stored reversed and {a.name} {'<' if a_first else '>'} {b.name} in every row ({in_both} values appear in both "
                   f"columns): either a directed link or an unordered pair stored once; the values cannot tell which, the "
                   f"writer or a constraint can")
    elif both == 0:
        storage = f"no pair is stored reversed, order mixed ({in_both} values appear in both columns): direction is data"
    else:
        storage = f"{both} of {len(proper)} pairs are also stored reversed: direction is data, some links go both ways"
    fan_a = max(n for _v, n in con.execute(
        f"SELECT {q(a.name)}, count(*) FROM {q(table.name)} GROUP BY 1 ORDER BY 2 DESC LIMIT 1").fetchall())
    fan_b = max(n for _v, n in con.execute(
        f"SELECT {q(b.name)}, count(*) FROM {q(table.name)} GROUP BY 1 ORDER BY 2 DESC LIMIT 1").fetchall())
    parts = [f"- pair ({a.name}, {b.name}): {len(rows)} rows, {len(pairs)} distinct pairs" + (f", {loops} self-pairs" if loops else ""),
             storage,
             f"one {a.name} value in up to {fan_a} rows, one {b.name} value in up to {fan_b} rows"]
    label = target.label_column() if target else None
    if samples and target is not None and a.ref:
        key = a.ref[1]
        shown = []
        for x, y in rows[:3]:
            if label:
                names = dict(con.execute(f"SELECT {q(key)}, {q(label)} FROM {q(target.name)} WHERE {q(key)} IN (?, ?)", (x, y)).fetchall())
                shown.append(f"{fmt_value(names.get(x, x), 24)}→{fmt_value(names.get(y, y), 24)}")
            else:
                shown.append(f"{fmt_value(x, 24)}→{fmt_value(y, 24)}")
        parts.append(f"stored rows as {a.name}→{b.name}" + (f" (shown by {target.name}.{label})" if label else "") + ": " + ", ".join(shown))
    return SEP.join(parts)


def hierarchy_line(con, table: Table, col: Column, max_rows: int) -> str:
    key = col.ref[1]
    rows = con.execute(f"SELECT {q(key)}, {q(col.name)} FROM {q(table.name)} LIMIT {max_rows}").fetchall()
    parent = dict(rows)
    deepest = 0
    for start in parent:
        depth, node, seen = 1, start, set()
        while parent.get(node) is not None and node not in seen and depth < 1000:
            seen.add(node)
            node = parent[node]
            depth += 1
        deepest = max(deepest, depth)
    roots = sum(1 for _k, p in rows if p is None)
    return (f"- self-reference {col.name} -> {table.name}.{key}: each row names one other row of the same table; "
            f"{roots} rows have null (the top), longest chain {deepest} rows")


def column_line(table: Table, col: Column, samples: bool) -> str:
    parts = [f"- `{col.name}` {col.decl.replace(' ', '_')}"]
    flags = []
    if col.pk and len(table.pk()) == 1:
        flags.append("primary key")
    elif col.unique:
        flags.append("unique")
    if col.notnull and not col.pk:
        flags.append("not null")
    if flags:
        parts.append(", ".join(flags))
    if col.ref:
        parts.append(f"-> {col.ref[0]}.{col.ref[1]} ({col.ref[2]}" +
                     (f"; also fits {', '.join(col.alternatives)}" if col.alternatives else "") + ")")
    nulls = table.profiled - col.non_null
    if nulls and table.profiled:
        parts.append(f"null in {nulls} of {table.profiled} rows")
    if not col.non_null:
        if table.profiled:
            parts.append("always null")
        return SEP.join(parts)
    declared = col.decl.split("(")[0]
    stored = sorted(col.storage)
    numeric_decl = any(word in declared for word in ("INT", "REAL", "FLOA", "DOUB", "NUM", "DEC"))
    if len(stored) > 1 or (stored == ["text"] and numeric_decl) or (stored != ["text"] and any(w in declared for w in ("CHAR", "TEXT", "CLOB"))):
        parts.append("stored as " + ", ".join(f"{k} ({n})" for k, n in sorted(col.storage.items())))
    notes = describe(col.sample)
    if not samples:   # keep the format, drop the range of real values
        notes = [re.sub(r" \(\d{4}-\d{2}-\d{2} to [^)]*\)", "", note) for note in notes]
    code_ref = bool(col.ref) and stored == ["text"]
    enumerable = col.distinct <= 8 and not col.unique and (not col.ref or code_ref) and (table.profiled >= 2 * col.distinct or col.distinct <= 3)
    if enumerable and samples:
        parts.append("values: " + ", ".join(f"{fmt_value(v)} ({n})" for v, n in col.top))
    else:
        if not col.unique:
            parts.append(f"{col.distinct} distinct")
        if samples and not col.ref:
            if stored in (["integer"], ["real"], ["integer", "real"]):
                parts.append(f"{fmt_value(col.low)} to {fmt_value(col.high)}")
            else:
                parts.append("e.g. " + ", ".join(fmt_value(v) for v in col.sample[:3]))
    parts += notes
    return SEP.join(parts)


DDL_START = re.compile(r"\s*(CREATE\s+(TEMP\w*\s+)?(TABLE|UNIQUE\s+INDEX|INDEX|VIEW|TRIGGER)|ALTER\s+TABLE|DROP\s+(TABLE|VIEW|INDEX))\b", re.I)


def ddl_files(inputs: list[str]) -> list[Path]:
    files: list[Path] = []
    for item in inputs:
        path = Path(item)
        if path.is_dir():
            files += [p for p in sorted(path.rglob("*.sql")) if p.is_file()]
        elif path.is_file():
            files.append(path)
        else:
            raise FileNotFoundError(item)
    return files


def ddl_fingerprint(inputs: list[str]) -> str:
    return digest(*[part for f in ddl_files(inputs) for part in (str(f), f.read_bytes())])


def from_ddl(inputs: list[str]) -> tuple[sqlite3.Connection, int, list[str]]:
    """Run the schema statements of .sql files, in order, in an empty in-memory SQLite database.

    Only CREATE / ALTER / DROP of tables, indexes, views and triggers are run. A statement SQLite cannot parse
    (another dialect) is skipped and reported, so the caller can say what is missing."""
    con = sqlite3.connect(":memory:")
    ran, skipped = 0, []
    for file in ddl_files(inputs):
        buffer, start = "", 1
        for number, line in enumerate(file.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if not buffer.strip():
                start = number
            buffer += line + "\n"
            if not sqlite3.complete_statement(buffer):
                continue
            statement, buffer = buffer, ""
            bare = re.sub(r"--[^\n]*|/\*.*?\*/", "", statement, flags=re.S)
            if not DDL_START.match(bare):
                continue
            try:
                con.execute(statement)
                ran += 1
            except sqlite3.Error as exc:
                skipped.append(f"{file}:{start}: {' '.join(bare.split())[:70]} ({exc})")
    return con, ran, skipped


def take(path: str, max_rows: int = 100000, samples: bool = True, con: sqlite3.Connection | None = None) -> tuple[dict, list[str], list[str]]:
    con = con or connect(path)
    try:
        tables = read_tables(con, max_rows)
        resolve_references(con, tables, max_rows)
        by_name = {t.name: t for t in tables}
        review: list[str] = []
        for table in tables:
            if table.error:
                continue
            groups: dict[tuple[str, str], list[Column]] = {}
            for col in table.columns:
                if col.ref:
                    groups.setdefault((col.ref[0], col.ref[1]), []).append(col)
            for (target, _key), cols in groups.items():
                if target == table.name:
                    for col in cols:
                        table.pair_lines.append(hierarchy_line(con, table, col, max_rows))
                for i in range(len(cols)):
                    for j in range(i + 1, len(cols)):
                        if len(table.pair_lines) < 4:
                            line = pair_line(con, table, cols[i], cols[j], by_name.get(target), max_rows, samples)
                            if line:
                                table.pair_lines.append(line)
                                edge_like = {cols[i].name, cols[j].name} <= set(table.pk()) or len(table.columns) <= 3
                            if line and edge_like and ("direction is data" in line or "cannot tell which" in line):
                                review.append(f"{table.name} ({cols[i].name}, {cols[j].name}): what does a row mean, and which "
                                              f"end is which? The snapshot shows how pairs are stored, not what they mean.")
            for col in table.columns:
                if any("not decidable" in note for note in describe(col.sample)):
                    review.append(f"{table.name}.{col.name}: date text whose day/month order the values do not settle.")
        views = [(name, sql) for kind, name, _t, sql in schema_rows(con) if kind == "view"]
        triggers = [(name, tbl, sql) for kind, name, tbl, sql in schema_rows(con) if kind == "trigger"]

        body = ["## Index", "", "One line per table: rows, then columns (`column→table.key` where it joins). Look the table up below before using it.", ""]
        for table in tables:
            cols = ", ".join(c.name + (f"→{c.ref[0]}.{c.ref[1]}" if c.ref else "") for c in table.columns)
            body.append(f"- {table.name} ({table.rows} rows): {cols}")
        for name, _sql in views:
            body.append(f"- {name} (view)")
        body += ["", "## Tables", ""]
        referenced = {c.ref[0] for t in tables for c in t.columns if c.ref}
        for table in tables:
            body.append(f"### {table.name}")
            if table.error:
                body += [f"could not be read: {table.error}", ""]
                continue
            head = [f"rows: {table.rows}" + (f" (first {table.profiled} profiled)" if table.profiled < table.rows else "")]
            if table.pk():
                head.append(f"primary key: ({', '.join(table.pk())})")
            extra_unique = [u for u in table.unique_sets if len(u) > 1 and u != table.pk()]
            if extra_unique:
                head.append("unique together: " + "; ".join("(" + ", ".join(map(str, u)) + ")" for u in extra_unique))
            if table.indexes:
                head.append("indexes: " + ", ".join(table.indexes))
            body.append(SEP.join(head))
            body += [column_line(table, col, samples) for col in table.columns]
            body += table.pair_lines
            small = table.rows <= 12 or (table.rows <= 40 and len(table.columns) <= 3 and table.name in referenced)
            if samples and 0 < table.rows and small and len(table.columns) <= 8:
                names = ", ".join(c.name for c in table.columns)
                rows = con.execute(f"SELECT * FROM {q(table.name)} LIMIT 40").fetchall()
                body.append(f"- all {table.rows} rows as ({names}): " + "; ".join("(" + ", ".join(fmt_value(v, 32) if v is not None else "NULL" for v in row) + ")" for row in rows))
            if EXTRA_DDL.search(table.sql):
                body += ["```sql", table.sql.strip(), "```"]
            body.append("")
        if views:
            body += ["## Views", ""]
            for name, sql in views:
                body.append(f"### {name}")
                try:
                    body += [f"- `{r[1]}` {(r[2] or '(no type)').upper().replace(' ', '_')}" for r in con.execute(f"PRAGMA table_info({q(name)})").fetchall()]
                except sqlite3.Error as exc:
                    body.append(f"columns could not be read: {exc}")
                body += ["```sql", sql.strip(), "```", ""]
        if triggers:
            body += ["## Triggers", "", "Triggers change or reject writes: read them before trusting a column name.", ""]
            for name, tbl, sql in triggers:
                body += [f"- {name} on {tbl}", "```sql", sql.strip()[:1200], "```"]
            body.append("")
        capped = [t.name for t in tables if t.profiled < t.rows]
        facts = {
            "taken": today(),
            "store": f"sqlite {path}",
            "source": "live store",
            "refresh": f"schema.py sqlite {path}",
            "method": "schema.py sqlite (reads sqlite_master, PRAGMA table_xinfo / foreign_key_list / index_list, and the rows)",
            "read_with": f"SQLite library {sqlite3.sqlite_version}",
            "coverage": f"complete: {len(tables)} tables, {len(views)} views, {len(triggers)} triggers",
            "values": ("profiled from all rows" if not capped else f"profiled from the first {max_rows} rows of {', '.join(capped[:5])}") if samples
                      else "not sampled (--no-samples): stored formats are described, values are not shown",
            "fingerprint": digest(*[" ".join(row) for row in schema_rows(con)]),
        }
        return facts, body, review
    finally:
        con.close()
