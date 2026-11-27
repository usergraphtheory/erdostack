"""Compare what a query or code file uses with the schema snapshot. Standard library only.

    .cypher / .cql   labels, relationship types, arrow direction, endpoint kinds, properties, literal types
    .sql             compiled by SQLite against empty tables rebuilt from the snapshot (names only, no data)
    .py              text literals that are close to, but not, a name in the snapshot; where each attribute lives

A finding means "not in the snapshot": fix the file, or show that the snapshot is out of date.
"""
from __future__ import annotations

import ast
import difflib
import re
import sqlite3
from pathlib import Path

from sf_cypher import Node, Rel, scan_file
from sf_format import SEP, Snapshot

NUMERIC = ("INT", "FLOAT", "DOUBLE", "DECIMAL", "NUM", "REAL", "SERIAL", "LONG", "SHORT")
TEMPORAL = ("DATE", "TIME", "ZONED", "LOCAL")
TEXTUAL = ("STR", "TEXT", "CHAR", "UUID")


def closest(name: str, pool, n: int = 3) -> list[str]:
    pool = list(pool)
    lowered = {p.lower(): p for p in pool}
    hits = difflib.get_close_matches(name.lower(), list(lowered), n=n, cutoff=0.6)
    flat = re.sub(r"[_\-\s]", "", name.lower())
    extra = [p for p in pool if re.sub(r"[_\-\s]", "", p.lower()) == flat]
    out = []
    for p in extra + [lowered[h] for h in hits]:
        if p not in out and p != name:
            out.append(p)
    return out[:n]


def hint(name: str, pool) -> str:
    near = closest(name, pool)
    return f" Closest in the snapshot: {', '.join(near)}." if near else ""


class CypherChecker:
    def __init__(self, snap: Snapshot):
        self.nodes = {name: el.props() for name, el in snap.nodes().items()}
        self.rels = {name: el.props() for name, el in snap.rels().items()}
        self.patterns = {name: el.patterns() for name, el in snap.rels().items()}
        self.retired = snap.retired()
        self.snap = snap
        self.strict = snap.is_generated()

    def loose(self, name: str) -> bool:
        """A hand-written snapshot may describe a name in a layout this tool does not parse: then do not call it missing."""
        return not self.strict and self.snap.mentions(name)

    def retired_note(self, name: str) -> str:
        for line in self.retired:
            if re.search(rf"(?<![\w.]){re.escape(name)}(?![\w])", line):
                return " It is listed as retired: " + line[2:]
        return ""

    def infer(self, st) -> dict[int, list[str]]:
        """Labels for unlabelled pattern nodes, where the relationship they sit on allows only one kind."""
        found: dict[str, set] = {}
        for rel in st.rels:
            if rel.direction == "none" or not rel.types or any(t not in self.patterns for t in rel.types):
                continue
            start, end = rel.ends()
            for node, side in ((start, 0), (end, 1)):
                if node is None or not node.var or node.labels or st.labels_of(node.var):
                    continue
                kinds = {p[side] for t in rel.types for p in self.patterns[t] if p[2]} | \
                        {k for t in rel.types for p in self.patterns[t] if not p[2] for k in p[:2]}
                kinds.discard("?")
                if kinds:
                    found[node.var] = found[node.var] & kinds if node.var in found else kinds
        return {var: sorted(kinds) for var, kinds in found.items() if len(kinds) == 1}

    def check(self, path: Path) -> tuple[list[str], list[str]]:
        findings, unchecked = [], []
        for st in scan_file(path):
            if st.ddl and st.ddl["op"] not in ("constraint", "index"):
                continue
            if st.kind == "unread":
                unchecked.append(f"{path}:{st.line}: this statement could not be read by the checker")
                continue
            inferred = self.infer(st)

            def labels(node: Node | None) -> list[str]:
                if node is None:
                    return []
                return node.labels or st.labels_of(node.var) or inferred.get(node.var or "", [])

            seen = set()
            for node in st.nodes:
                for label in node.labels:
                    if label not in self.nodes and label not in seen and self.loose(label):
                        seen.add(label)
                        unchecked.append(f"{path}:{node.line}: `{label}` is mentioned in the snapshot but not as an entry this tool can read: compare by eye")
                    elif label not in self.nodes and label not in seen:
                        seen.add(label)
                        findings.append(f"{path}:{node.line}: label or node kind `{label}` is not in the snapshot."
                                        + hint(label, self.nodes) + self.retired_note(label))
            for rel in st.rels:
                start, end = rel.ends()
                for type_ in rel.types:
                    if type_ not in self.rels:
                        if ("rel", type_) not in seen and self.loose(type_):
                            seen.add(("rel", type_))
                            unchecked.append(f"{path}:{rel.line}: `{type_}` is mentioned in the snapshot but not as an entry this tool can read: compare by eye")
                        elif ("rel", type_) not in seen:
                            seen.add(("rel", type_))
                            findings.append(f"{path}:{rel.line}: relationship type `{type_}` is not in the snapshot."
                                            + hint(type_, self.rels) + self.retired_note(type_))
                        continue
                    pats = self.patterns[type_]
                    if not pats:
                        continue
                    s = [l for l in labels(start) if l in self.nodes or not self.strict]
                    e = [l for l in labels(end) if l in self.nodes or not self.strict]
                    if not s and not e:
                        continue

                    def fits(a_ok, b_ok):
                        return any((not a_ok or a in a_ok or a == "?") and (not b_ok or b in b_ok or b == "?") for a, b, _d in pats)

                    forward, backward = fits(s, e), fits(e, s)
                    loose = rel.direction == "none" or any(not d for _a, _b, d in pats)
                    if forward or (loose and backward):
                        continue
                    stored = "; ".join(f"(:{a})-[:{type_}]{'->' if d else '-'}(:{b})" for a, b, d in pats[:6])
                    used = f"(:{'|'.join(s) or '?'})-[:{type_}]->(:{'|'.join(e) or '?'})"
                    if backward:
                        findings.append(f"{path}:{rel.line}: direction reversed: the file uses {used}, the snapshot stores {stored}.")
                    else:
                        findings.append(f"{path}:{rel.line}: `{type_}` does not connect these kinds: the file uses {used}, the snapshot stores {stored}.")
            reported = set()
            for ref in st.refs:
                if isinstance(ref.owner, Rel) or (ref.owner is None and st.bind.get(ref.var, {}).get("kind") == "rel"):
                    names = ref.owner.types if isinstance(ref.owner, Rel) and ref.owner.types else st.labels_of(ref.var)
                    home, what = self.rels, "relationship"
                elif isinstance(ref.owner, Node):
                    names, home, what = labels(ref.owner), self.nodes, "node kind"
                else:
                    names = st.labels_of(ref.var) or inferred.get(ref.var, [])
                    home, what = self.nodes, "node kind"
                known = [n for n in names if n in home]
                if not known:
                    if ref.var in st.bind and not names and (ref.var, ref.prop) not in reported:
                        reported.add((ref.var, ref.prop))
                        unchecked.append(f"{path}:{ref.line}: {ref.var}.{ref.prop} (no label on `{ref.var}`, so the property could not be placed)")
                    continue
                if any(ref.prop in home[n] for n in known) or (tuple(known), ref.prop) in reported:
                    continue
                reported.add((tuple(known), ref.prop))
                if any(not home[n] for n in known):   # entry without readable property lines
                    unchecked.append(f"{path}:{ref.line}: {'|'.join(known)}.{ref.prop} (the snapshot entry lists no properties in a form this tool can read: compare by eye)")
                    continue
                owner = "|".join(known)
                has = ", ".join(list(home[known[0]])[:14]) or "no properties"
                elsewhere = [f"{n} (node)" for n, props in self.nodes.items() if ref.prop in props] + \
                            [f"{n} (relationship)" for n, props in self.rels.items() if ref.prop in props]
                findings.append(f"{path}:{ref.line}: `{owner}` has no property `{ref.prop}` in the snapshot. {what.capitalize()} {owner} has: {has}."
                                + (f" `{ref.prop}` lives on: {', '.join(elsewhere[:6])}." if elsewhere else "")
                                + hint(ref.prop, home[known[0]]) + self.retired_note(f"{known[0]}.{ref.prop}"))
            for var, prop, literal in st.compares:
                entry = st.bind.get(var)
                names = entry["labels"] if entry else inferred.get(var, [])
                home = self.rels if entry and entry["kind"] == "rel" else self.nodes
                for name in names:
                    type_ = (home.get(name, {}).get(prop, ("", ""))[0] or "").upper()
                    if not type_:
                        continue
                    if literal.kind == "func":
                        call = literal.text.lower()
                        if call in ("date", "datetime", "localdatetime", "time", "localtime") and type_.startswith(NUMERIC):
                            findings.append(f"{path}:{literal.line}: {name}.{prop} is {type_} in the snapshot but is compared with the "
                                            f"temporal value {literal.text}(...): convert one side first (a number is not a date).")
                        elif call == "timestamp" and type_.startswith(TEMPORAL):
                            findings.append(f"{path}:{literal.line}: {name}.{prop} is {type_} in the snapshot but is compared with "
                                            f"timestamp(), which is an integer: convert one side first.")
                        continue
                    text = literal.kind == "str"
                    if text and (type_.startswith(NUMERIC) or type_ in ("BOOLEAN", "BOOL")):
                        findings.append(f"{path}:{literal.line}: {name}.{prop} is {type_} in the snapshot but is compared with the text {literal.text}.")
                    elif text and type_.startswith(TEMPORAL):
                        findings.append(f"{path}:{literal.line}: {name}.{prop} is {type_} in the snapshot but is compared with the text {literal.text}: compare with a temporal value, not a string.")
                    elif not text and (type_.startswith(TEXTUAL) or type_.startswith(TEMPORAL)):
                        findings.append(f"{path}:{literal.line}: {name}.{prop} is {type_} in the snapshot but is compared with the number {literal.text}.")
        return findings, unchecked


# --- SQL -----------------------------------------------------------------------------

def rebuild(snap: Snapshot) -> tuple[sqlite3.Connection, list[str]]:
    """Empty in-memory tables with the snapshot's table and column names, so SQLite can resolve names."""
    con = sqlite3.connect(":memory:")
    problems = []
    for name, element in snap.elements.get("Tables", {}).items():
        cols = []
        for col, (type_, _rest) in element.props().items():
            decl = type_.replace("_", " ") if re.fullmatch(r"[A-Za-z][A-Za-z0-9_(),]*", type_ or "") else ""
            cols.append('"' + col.replace('"', '""') + '" ' + decl)
        if not cols:
            continue
        try:
            con.execute(f'CREATE TABLE "{name}" ({", ".join(cols)})')
        except sqlite3.Error as exc:
            problems.append(f"table {name} could not be rebuilt from the snapshot: {exc}")
    for name, element in snap.elements.get("Views", {}).items():
        text = "\n".join(element.lines)
        match = re.search(r"```sql\n(.*?)\n```", text, re.S)
        if match:
            try:
                con.execute(match.group(1))
            except sqlite3.Error as exc:
                problems.append(f"view {name} could not be rebuilt: {exc}")
    return con, problems


def split_sql(text: str) -> list[tuple[str, int]]:
    out, buffer, start = [], "", 1
    for number, line in enumerate(text.splitlines(), 1):
        if not buffer.strip():
            start = number
        buffer += line + "\n"
        if sqlite3.complete_statement(buffer):
            out.append((buffer.strip(), start))
            buffer = ""
    if re.sub(r"--[^\n]*|/\*.*?\*/", "", buffer, flags=re.S).strip():
        out.append((buffer.strip(), start))
    return out


def check_sql(path: Path, snap: Snapshot, con: sqlite3.Connection) -> tuple[list[str], list[str], list[str]]:
    findings, unchecked, notes = [], [], []
    tables = snap.elements.get("Tables", {})
    is_sqlite = snap.facts.get("store", "").lower().startswith("sqlite")
    text = path.read_text(encoding="utf-8", errors="replace")
    for statement, line in split_sql(text):
        bare = re.sub(r"--[^\n]*|/\*.*?\*/", "", statement, flags=re.S).strip()
        if not bare or bare.startswith(".") or re.match(r"(PRAGMA|ATTACH|DETACH|BEGIN|COMMIT|ROLLBACK|VACUUM)\b", bare, re.I):
            continue
        try:
            con.execute("EXPLAIN " + statement)
        except sqlite3.Error as exc:
            message = str(exc)
            if message.startswith(("no such table", "no such column")) and not snap.is_generated() \
                    and snap.mentions(message.split(":", 1)[1].strip().split(".")[-1]):
                unchecked.append(f"{path}:{line}: `{message.split(':', 1)[1].strip()}` is mentioned in the snapshot but not in a form this tool can read: compare by eye")
            elif message.startswith("no such table"):
                name = message.split(":", 1)[1].strip()
                findings.append(f"{path}:{line}: table `{name}` is not in the snapshot." + hint(name.split(".")[-1], tables))
            elif message.startswith("no such column"):
                name = message.split(":", 1)[1].strip()
                column = name.split(".")[-1]
                words = {w.lower() for w in re.findall(r"\w+", statement)}
                used = [t for t in tables if t.lower() in words]
                pool = [c for t in used for c in tables[t].props()]
                homes = [t for t in tables if column in tables[t].props()]
                findings.append(f"{path}:{line}: column `{name}` is not on the tables this statement reads ({', '.join(used) or 'none recognised'})."
                                + hint(column, pool) + (f" A column of that name is on: {', '.join(homes[:6])}." if homes else ""))
            elif message.startswith("ambiguous column name"):
                findings.append(f"{path}:{line}: {message}: qualify it with its table.")
            elif is_sqlite:
                findings.append(f"{path}:{line}: SQLite cannot compile this statement: {message}.")
            else:
                unchecked.append(f"{path}:{line}: not SQLite syntax ({message}), so names were not checked here")
    code = re.sub(r"--[^\n]*|/\*.*?\*/", " ", text, flags=re.S)
    words = {w.lower() for w in re.findall(r"\w+", re.sub(r"'(?:''|[^'])*'", " ", code))}
    allowed: dict[str, set[str]] = {}
    for name, element in tables.items():
        if name.lower() not in words:
            continue
        for col, (_type, rest) in element.props().items():
            if col.lower() not in words:
                continue
            listed = re.search(r"values: (.*?)(?: · |$)", rest)
            if listed:
                allowed.setdefault(col.lower(), set()).update(
                    v.strip() for v in re.sub(r" \(\d+\)", "", listed.group(1)).split(", "))
            flags = [part for part in rest.split(SEP) if part.startswith(("values:", "stored as", "null in", "always null"))
                     or "text" in part or "epoch" in part or "integers YYYYMMDD" in part or "inferred" in part]
            if flags:
                notes.append(f"{name}.{col}: " + "; ".join(flags))
        for line_ in element.lines:
            match = re.match(r"^- (pair \(([^,]+), ([^)]+)\)|self-reference (\S+))", line_)
            if match and all(c.strip().lower() in words for c in (match.group(2, 3) if match.group(2) else (match.group(4),))):
                notes.append(f"{name}: " + SEP.join(line_[2:].split(SEP)[:2]))
    for col, values in allowed.items():   # a literal the column never holds usually means an assumed encoding
        for match in re.finditer(rf"(?<!\w){re.escape(col)}\"?\s*(=|==|<>|!=)\s*('(?:''|[^'])*'|-?\d+(?:\.\d+)?)(?!\s*[-+*/|])", code, re.I):
            if match.group(2) not in values:
                line = code.count("\n", 0, match.start()) + 1
                findings.append(f"{path}:{line}: `{match.group(0).strip()}`: the snapshot lists every value this column holds "
                                f"({', '.join(sorted(values))}) and {match.group(2)} is not one of them.")
    return findings, unchecked, notes


# --- Python ---------------------------------------------------------------------------

def vocabulary(snap: Snapshot) -> tuple[set[str], dict[str, list[str]], set[str]]:
    names, lives, values = set(), {}, set()
    for shape, home in (("node", snap.nodes()), ("edge", snap.rels())):
        for kind, element in home.items():
            names.add(kind)
            for prop, (_type, rest) in element.props().items():
                names.add(prop)
                where = f"{shape} {kind}"
                only = re.search(r"only on (.*?) edges", rest)
                if only:
                    where += f" ({only.group(1)})"
                lives.setdefault(prop, []).append(where)
                listed = re.search(r"values: (.*?)(?: · |$)", rest)
                if listed:
                    values.update(re.findall(r"'([^']*)' \(\d+\)", listed.group(1)))
    for key in ("node_kind_attribute", "edge_kind_attribute"):
        value = snap.facts.get(key, "")
        if re.fullmatch(r"\w+", value):
            names.add(value)
    return names, lives, values


def near_miss(text: str, names: set[str]) -> list[str]:
    """Snapshot names that `text` is probably a misspelling of: same letters in another style, one inside the other, or a close edit."""
    flat = re.sub(r"[_\-\s]", "", text.lower())
    out = []
    for name in names:
        other = re.sub(r"[_\-\s]", "", name.lower())
        if other == flat or (min(len(flat), len(other)) >= 5 and (flat in other or other in flat)):
            out.append(name)
    if len(text) >= 5:
        out += [n for n in difflib.get_close_matches(text, [n for n in names if len(n) >= 5], n=2, cutoff=0.8) if n not in out]
    return [n for n in out if n != text][:3]


def check_python(path: Path, snap: Snapshot) -> tuple[list[str], list[str], list[str]]:
    names, lives, values = vocabulary(snap)
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError as exc:
        return [f"{path}:{exc.lineno}: not parseable as Python: {exc.msg}"], [], []
    literals: dict[str, int] = {}
    keys: dict[str, int] = {}   # literals used to look something up: x["k"], x.get("k"), data="k", weight="k"

    def remember(node, into):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and re.fullmatch(r"[A-Za-z_][\w\-]*", node.value):
            into.setdefault(node.value, node.lineno)

    for node in ast.walk(tree):
        if isinstance(node, ast.Subscript):
            remember(node.slice, keys)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute) and node.func.attr in ("get", "pop", "get_edge_attributes", "get_node_attributes") and node.args:
                remember(node.args[-1] if node.func.attr.startswith("get_") else node.args[0], keys)
            for keyword in node.keywords:
                if keyword.arg in ("data", "weight", "label", "attr", "name"):
                    remember(keyword.value, keys)
        elif isinstance(node, ast.Compare):
            for side in [node.left] + node.comparators:
                remember(side, literals)
    literals.update({k: v for k, v in keys.items()})
    findings, unchecked, notes = [], [], []
    known = names | values
    for text, line in sorted(literals.items(), key=lambda item: item[1]):
        if text in known:
            continue
        near = near_miss(text, names)
        if near:
            findings.append(f"{path}:{line}: '{text}' is not a name in the snapshot but is close to one: {', '.join(near)}.")
        elif text in keys:
            unchecked.append(f"{path}:{line}: '{text}' is used as a key or attribute name and is not in the snapshot (fine only if it is a key of your own data)")
    placed = []
    for name in literals:
        homes = lives.get(name, [])
        on_edges = [h for h in homes if h.startswith("edge ")]
        if homes and (on_edges or len(homes) <= 3):   # skip attributes nearly every node kind has
            placed.append(f"{name} → {', '.join((on_edges + [h for h in homes if h not in on_edges])[:5])}" + (" …" if len(homes) > 5 else ""))
    if placed:
        notes.append("where the attributes this file names live (an edge attribute is read from the edge, not the node): " + "; ".join(placed[:14]))
    return findings, unchecked, notes


def run(paths: list[str], snap: Snapshot, quiet: bool = False) -> int:
    files: list[Path] = []
    for item in paths:
        path = Path(item)
        if path.is_dir():
            files += [p for p in sorted(path.rglob("*")) if p.suffix.lower() in (".cypher", ".cql", ".cyp", ".sql", ".py")]
        elif path.is_file():
            files.append(path)
        else:
            print(f"{item}: no such file")
    if not snap.parseable():
        print("The snapshot is not in the layout this tool reads (no `### Name` entries under `## Nodes`, `## Tables` or "
              "`## Relationships`), so nothing was checked. Read it and compare each name, direction and property by eye.")
        return 0
    cypher, con, problems = CypherChecker(snap), None, []
    total = 0
    for path in files:
        suffix = path.suffix.lower()
        if suffix == ".sql" and not snap.elements.get("Tables"):
            print(f"?    {path}: the snapshot has no `## Tables` section, so SQL names were not checked")
            continue
        if suffix == ".sql":
            if con is None:
                con, problems = rebuild(snap)
            findings, unchecked, notes = check_sql(path, snap, con)
        elif suffix == ".py" and not snap.elements.get("Tables"):
            findings, unchecked, notes = check_python(path, snap)
        elif suffix == ".py":
            continue
        else:
            findings, unchecked = cypher.check(path)
            notes = []
        total += len(findings)
        if not findings and not unchecked and (quiet or not notes):
            print(f"ok   {path}")
            continue
        print(f"{'FAIL' if findings else 'ok  '} {path}")
        for line in findings:
            print("  - " + line)
        said = set()
        for line in unchecked:
            what = line.split(": ", 1)[-1]
            if what not in said:
                said.add(what)
                print("  ? not checked: " + line)
        if not quiet:
            for line in notes:
                print("  · " + line)
    for line in problems:
        print("note: " + line)
    taken = snap.facts.get("taken", "unknown date")
    print(f"{len(files)} file(s) checked against the snapshot taken {taken} ({snap.facts.get('source', 'source not recorded')}): "
          f"{total} finding(s).")
    return 1 if total else 0
