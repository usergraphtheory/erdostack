"""A tolerant static reader for Cypher text. Standard library only.

It does not validate Cypher. It finds node patterns, relationship patterns with their arrow, the labels a
variable is bound to, property reads and writes, removals and deletions, plus the DDL forms that define a
schema (constraints, indexes, CREATE NODE TABLE / CREATE REL TABLE). Whatever it cannot attribute it leaves out.

Two users: `inventory` builds a schema from the files that define and load a graph when no live database can
be asked; the checker lists what a query file uses so each name can be compared with the snapshot.
"""
from __future__ import annotations

import re
from pathlib import Path

TOKEN = re.compile(r"""
  (?P<ws>\s+)
 |(?P<lc>//[^\n]*)
 |(?P<bc>/\*.*?\*/)
 |(?P<str>'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*")
 |(?P<bt>`(?:``|[^`])*`)
 |(?P<num>\d+\.\d+(?:[eE][+-]?\d+)?|\d+)
 |(?P<param>\$[A-Za-z_]\w*|\$`[^`]*`|\$\d+)
 |(?P<id>[A-Za-z_][A-Za-z0-9_]*)
 |(?P<op><>|<=|>=|\+=|=~|\.\.|::|[-<>()\[\]{}:,.;|*=+/%^!&?])
 |(?P<other>.)
""", re.X | re.S)

CLAUSES = {"MATCH", "OPTIONAL", "MERGE", "CREATE", "SET", "REMOVE", "DELETE", "DETACH", "WHERE", "RETURN", "WITH",
           "UNWIND", "ORDER", "CALL", "FOREACH", "LOAD", "YIELD", "LIMIT", "SKIP", "UNION", "FINISH", "INSERT",
           "FILTER", "LET", "USE", "USING"}
PATTERN_CLAUSES = {"MATCH", "MERGE", "CREATE", "INSERT"}
WRITE_CLAUSES = {"MERGE", "CREATE", "INSERT"}
KEYWORDS = CLAUSES | {"AND", "OR", "XOR", "NOT", "IN", "IS", "NULL", "AS", "ON", "BY", "ASC", "DESC", "DISTINCT",
                      "CASE", "WHEN", "THEN", "ELSE", "END", "TRUE", "FALSE", "STARTS", "ENDS", "CONTAINS",
                      "FROM", "HEADERS", "CSV", "FIELDTERMINATOR",
                      "TRANSACTIONS", "OF", "ROWS", "FOR", "REQUIRE", "ASSERT", "UNIQUE", "KEY", "NODE", "IF", "CYPHER"}
FUNCTION_TYPES = {
    "date": "DATE", "datetime": "DATETIME", "localdatetime": "LOCAL_DATETIME", "time": "TIME", "localtime": "LOCAL_TIME",
    "duration": "DURATION", "tointeger": "INTEGER", "tointegerornull": "INTEGER", "toint": "INTEGER", "size": "INTEGER",
    "count": "INTEGER", "length": "INTEGER", "tofloat": "FLOAT", "tofloatornull": "FLOAT", "toboolean": "BOOLEAN",
    "tobooleanornull": "BOOLEAN", "tostring": "STRING", "tostringornull": "STRING", "trim": "STRING", "tolower": "STRING",
    "toupper": "STRING", "replace": "STRING", "substring": "STRING", "left": "STRING", "right": "STRING",
    "randomuuid": "STRING", "timestamp": "INTEGER(epoch_ms)", "point": "POINT", "split": "LIST<STRING>",
}
CYPHER_WORD = re.compile(r"\b(MATCH|MERGE|CREATE)\b[^\n]*\(", re.I)
STRING_LITERAL = re.compile(r'"""(.*?)"""|\'\'\'(.*?)\'\'\'|`((?:[^`\\]|\\.)*)`|"((?:[^"\\\n]|\\.)*)"|\'((?:[^\'\\\n]|\\.)*)\'', re.S)
CYPHER_SUFFIXES = {".cypher", ".cql", ".cyp", ".cy", ".gql"}


class Tok:
    __slots__ = ("kind", "text", "line")

    def __init__(self, kind, text, line):
        self.kind, self.text, self.line = kind, text, line

    @property
    def up(self) -> str:
        return self.text.upper() if self.kind == "id" else self.text

    def name(self) -> str:
        return self.text[1:-1].replace("``", "`") if self.kind == "bt" else self.text


def tokenize(text: str, first_line: int = 1) -> list[Tok]:
    out, line = [], first_line
    for match in TOKEN.finditer(text):
        kind, value = match.lastgroup, match.group()
        if kind not in ("ws", "lc", "bc"):
            out.append(Tok(kind, value, line))
        line += value.count("\n")
    return out


def cypher_chunks(path: Path) -> list[tuple[str, int]]:
    """(text, first line) pieces of Cypher in a file: the whole file, or the string literals of a source file."""
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() in CYPHER_SUFFIXES:
        return [(text, 1)]
    chunks = []
    for match in STRING_LITERAL.finditer(text):
        body = next((g for g in match.groups() if g is not None), "")
        if CYPHER_WORD.search(body) or re.search(r"\bCREATE\s+(NODE|REL)\s+TABLE\b", body, re.I):
            chunks.append((body, text.count("\n", 0, match.start()) + 1))
    return chunks


def statements(tokens: list[Tok]) -> list[list[Tok]]:
    out, current = [], []
    for tok in tokens:
        if tok.text == ";" and tok.kind == "op":
            if current:
                out.append(current)
            current = []
        else:
            current.append(tok)
    if current:
        out.append(current)
    return out


class Node:
    def __init__(self, var, labels, props, clause, line, any_of=False):
        self.var, self.labels, self.props, self.clause, self.line, self.any_of = var, labels, props, clause, line, any_of


class Rel:
    def __init__(self, var, types, props, direction, varlen, clause, line):
        self.var, self.types, self.props, self.direction, self.varlen = var, types, props, direction, varlen
        self.clause, self.line = clause, line
        self.left: Node | None = None
        self.right: Node | None = None

    def ends(self) -> tuple["Node", "Node"]:
        """(start, end) following the arrow; for an undirected pattern the order written."""
        return (self.right, self.left) if self.direction == "in" else (self.left, self.right)


class Ref:
    """One use of a property: on a variable (`n.name`) or in the inline map of a pattern (`{name: ...}`)."""

    def __init__(self, var, prop, mode, value, line, index=-1, owner=None):
        self.var, self.prop, self.mode, self.value, self.line, self.index, self.owner = var, prop, mode, value, line, index, owner


class Statement:
    def __init__(self):
        self.nodes: list[Node] = []
        self.rels: list[Rel] = []
        self.refs: list[Ref] = []
        self.removed: list[tuple] = []     # (var, prop or None, label or None, token index)
        self.deleted: list[tuple] = []     # (var, token index)
        self.compares: list[tuple] = []    # (var, prop, literal Tok)
        self.where_refs: set[tuple] = set()
        self.bind: dict[str, dict] = {}    # var -> {"kind": "node"|"rel", "labels": [..]}
        self.has_params = False
        self.has_where = False
        self.csv_vars: set[str] = set()
        self.ddl: dict | None = None
        self.line = 0
        self.kind = "read"

    def labels_of(self, var: str | None) -> list[str]:
        return list(self.bind.get(var, {}).get("labels", [])) if var else []


def _match_close(toks: list[Tok], i: int) -> int:
    """Index of the bracket that closes toks[i], or -1."""
    pairs = {"(": ")", "[": "]", "{": "}"}
    close, depth = pairs[toks[i].text], 0
    for j in range(i, len(toks)):
        t = toks[j]
        if t.kind != "op":
            continue
        if t.text in pairs:
            depth += 1 if t.text == toks[i].text else 0
        if t.text == close:
            depth -= 1
            if depth == 0:
                return j
    return -1


def _parse_map(toks: list[Tok], i: int) -> tuple[dict, int]:
    """toks[i] is '{'. Returns ({key: value tokens}, index after the closing brace)."""
    end = _match_close(toks, i)
    if end < 0:
        return {}, len(toks)
    props, j = {}, i + 1
    while j < end:
        key = toks[j]
        if key.kind in ("id", "bt", "str") and j + 1 < end and toks[j + 1].text == ":":
            k, depth, value = j + 2, 0, []
            while k < end:
                t = toks[k]
                if t.kind == "op" and t.text in "([{":
                    depth += 1
                elif t.kind == "op" and t.text in ")]}":
                    depth -= 1
                elif t.kind == "op" and t.text == "," and depth == 0:
                    break
                value.append(t)
                k += 1
            props[key.name() if key.kind != "str" else key.text[1:-1]] = value
            j = k + 1
        else:
            j += 1
    return props, end + 1


def _parse_node(toks: list[Tok], i: int, clause: str):
    """toks[i] is '('. Returns (Node, index after ')') or None when this is not a node pattern."""
    j, var, labels, props, any_of = i + 1, None, [], {}, False
    if j < len(toks) and toks[j].kind in ("id", "bt") and (toks[j].kind == "bt" or toks[j].up not in ("WHERE",)):
        nxt = toks[j + 1].text if j + 1 < len(toks) else ""
        if nxt in (")", ":", "{") or (j + 1 < len(toks) and toks[j + 1].up == "WHERE") or (j + 1 < len(toks) and toks[j + 1].up == "IS"):
            var = toks[j].name()
            j += 1
        else:
            return None
    if j < len(toks) and (toks[j].text == ":" or toks[j].up == "IS"):
        if toks[j].up == "IS" and (j + 1 >= len(toks) or toks[j + 1].up in ("NOT", "NULL", "TYPED", "NORMALIZED") or toks[j + 1].text == "::"):
            return None
        j += 1
        while j < len(toks):
            if toks[j].kind not in ("id", "bt"):   # a label expression with ! or ( ): keep what was read, skip the rest
                any_of = True
                end = _match_close(toks, i)
                if end < 0:
                    return None
                return Node(var, labels, {}, clause, toks[i].line, True), end + 1
            labels.append(toks[j].name())
            j += 1
            if j < len(toks) and toks[j].text in (":", "&", "|"):
                any_of = any_of or toks[j].text == "|"
                j += 1
                if j < len(toks) and toks[j].text == ":":
                    j += 1
                continue
            break
    if j < len(toks) and toks[j].text == "{":
        props, j = _parse_map(toks, j)
    if j < len(toks) and toks[j].up == "WHERE":
        end = _match_close(toks, i)
        if end < 0:
            return None
        j = end
    if j < len(toks) and toks[j].text == ")":
        return Node(var, labels, props, clause, toks[i].line, any_of), j + 1
    return None


def _parse_rel(toks: list[Tok], i: int, clause: str):
    """toks[i] starts a relationship after a node: '-' or '<'. Returns (Rel, index of the next '(') or None."""
    j, left_arrow = i, False
    if toks[j].text == "<" and j + 1 < len(toks) and toks[j + 1].text == "-":
        left_arrow, j = True, j + 2
    elif toks[j].text == "-":
        j += 1
    else:
        return None
    var, types, props, varlen = None, [], {}, False
    if j < len(toks) and toks[j].text == "[":
        end = _match_close(toks, j)
        if end < 0:
            return None
        k = j + 1
        if k < end and toks[k].kind in ("id", "bt") and toks[k].up != "WHERE":
            var = toks[k].name()
            k += 1
        if k < end and toks[k].text == ":":
            k += 1
            while k < end and toks[k].kind in ("id", "bt"):
                types.append(toks[k].name())
                k += 1
                if k < end and toks[k].text in ("|", "&"):
                    k += 1
                    if k < end and toks[k].text == ":":
                        k += 1
                else:
                    break
        while k < end:
            if toks[k].text == "*" or toks[k].text == "+":
                varlen = True
            if toks[k].text == "{":
                inner = _match_close(toks, k)
                nxt = toks[k + 1] if k + 1 < end else None
                if nxt is not None and nxt.kind in ("id", "bt", "str"):
                    props, _ = _parse_map(toks, k)
                else:
                    varlen = True  # a quantifier such as {1,3}
                k = inner if inner > 0 else end
            k += 1
        j = end + 1
    if j >= len(toks) or toks[j].text != "-":
        return None
    j += 1
    right_arrow = j < len(toks) and toks[j].text == ">"
    if right_arrow:
        j += 1
    if j < len(toks) and toks[j].text in ("+", "*"):       # quantified relationship
        varlen, j = True, j + 1
    elif j < len(toks) and toks[j].text == "{":
        close = _match_close(toks, j)
        varlen, j = True, (close + 1 if close > 0 else j)
    if j >= len(toks) or toks[j].text != "(":
        return None
    direction = "in" if left_arrow and not right_arrow else "out" if right_arrow and not left_arrow else "none"
    return Rel(var, types, props, direction, varlen, clause, toks[i].line), j


def value_type(value: list[Tok], csv_vars: set[str]) -> tuple[str, str | None]:
    """(type guess or '', literal sample or None) for the expression a property is set to."""
    if not value:
        return "", None
    head = value[0]
    if head.kind == "id" and head.text in csv_vars and len(value) == 3 and value[1].text == ".":
        return "STRING", None   # a LOAD CSV field is text until something converts it
    tail = [t.text for t in value[-2:]]
    if len(value) > 3 and tail[0] == ".":
        if tail[1] in ("epochSeconds", "epochMillis"):
            return f"INTEGER({'epoch_s' if tail[1] == 'epochSeconds' else 'epoch_ms'})", None
        if tail[1] in ("year", "month", "day", "hour", "minute", "second", "week", "quarter"):
            return "INTEGER", None
    if len(value) == 1:
        if head.kind == "str":
            return "STRING", head.text
        if head.kind == "num":
            return ("FLOAT" if "." in head.text else "INTEGER"), head.text
        if head.up in ("TRUE", "FALSE"):
            return "BOOLEAN", head.text.lower()
        if head.kind == "param":
            return "", None
    if head.text == "-" and len(value) == 2 and value[1].kind == "num":
        return ("FLOAT" if "." in value[1].text else "INTEGER"), "-" + value[1].text
    if head.kind == "id" and len(value) > 1 and value[1].text == "(":
        name = head.text.lower()
        if name == "coalesce":
            close = _match_close(value, 1)
            for arg in _split_top(value[2:close if close > 0 else len(value)]):
                guess = value_type(arg, csv_vars)[0]
                if guess:
                    return guess, None
            return "", None
        close = _match_close(value, 1)
        if close == len(value) - 1 or close < 0:
            return FUNCTION_TYPES.get(name, ""), None
        return "", None
    if head.text == "[":
        return "LIST", None
    if head.text == "(" and _match_close(value, 0) == len(value) - 1:
        if any(t.text in ("=", "<>", "<", ">", "<=", ">=") or t.up in ("IN", "IS", "CONTAINS") for t in value[1:-1]):
            return "BOOLEAN", None
        return value_type(value[1:-1], csv_vars)
    if any(t.text in ("=", "<>", "<=", ">=") or t.up in ("IS", "CONTAINS", "STARTS") for t in value) and head.text != "CASE":
        return "BOOLEAN", None
    return "", None


def _split_top(toks: list[Tok]) -> list[list[Tok]]:
    parts, current, depth = [], [], 0
    for t in toks:
        if t.kind == "op" and t.text in "([{":
            depth += 1
        elif t.kind == "op" and t.text in ")]}":
            depth -= 1
        if t.kind == "op" and t.text == "," and depth == 0:
            parts.append(current)
            current = []
        else:
            current.append(t)
    if current:
        parts.append(current)
    return parts


def _ddl(toks: list[Tok]) -> dict | None:
    """Schema-defining statements. Returns a dict describing it, or None for an ordinary query."""
    ups = [t.up for t in toks[:8]]
    text = " ".join(ups)
    if re.match(r"CREATE (NODE|REL) TABLE", text):
        rel = ups[1] == "REL"
        i = 3
        if i < len(toks) and toks[i].up == "GROUP":
            i += 1
        if i + 2 < len(toks) and toks[i].up == "IF":
            i += 3
        if i >= len(toks) or toks[i].kind not in ("id", "bt"):
            return None
        name, open_at = toks[i].name(), i + 1
        if open_at >= len(toks) or toks[open_at].text != "(":
            return None
        close = _match_close(toks, open_at)
        cols, pairs, key = {}, [], []
        for part in _split_top(toks[open_at + 1: close if close > 0 else len(toks)]):
            if not part:
                continue
            if part[0].up == "FROM" and len(part) >= 4 and part[2].up == "TO":
                pairs.append((part[1].name(), part[3].name()))
            elif part[0].up == "PRIMARY":
                key += [t.name() for t in part if t.kind in ("id", "bt") and t.up not in ("PRIMARY", "KEY")]
            elif len(part) >= 2 and part[0].kind in ("id", "bt"):
                type_toks = part[1:]
                is_key = any(t.up == "PRIMARY" for t in type_toks)
                cut = next((n for n, t in enumerate(type_toks) if t.up in ("PRIMARY", "DEFAULT")), len(type_toks))
                cols[part[0].name()] = "".join(t.text for t in type_toks[:cut]).upper()
                if is_key:
                    key.append(part[0].name())
        return {"op": "rel_table" if rel else "node_table", "name": name, "cols": cols, "pairs": pairs, "key": key}
    if text.startswith("DROP TABLE"):
        i = 2 + (2 if len(toks) > 3 and toks[2].up == "IF" else 0)
        return {"op": "drop_table", "name": toks[i].name()} if i < len(toks) else None
    if text.startswith("ALTER TABLE") and len(toks) >= 5:
        name, verb = toks[2].name(), toks[3].up
        if verb == "ADD":
            i = 4 + (1 if toks[4].up == "COLUMN" else 0) + (3 if toks[4].up == "IF" else 0)
            if i + 1 < len(toks):
                cut = next((n for n, t in enumerate(toks[i + 1:]) if t.up == "DEFAULT"), len(toks) - i - 1)
                return {"op": "add_column", "name": name, "col": toks[i].name(), "type": "".join(t.text for t in toks[i + 1:i + 1 + cut]).upper()}
        if verb == "DROP":
            i = 4 + (1 if toks[4].up == "COLUMN" else 0) + (2 if toks[4].up == "IF" else 0)
            return {"op": "drop_column", "name": name, "col": toks[i].name()} if i < len(toks) else None
        if verb == "RENAME":
            if toks[4].up == "TO" and len(toks) > 5:
                return {"op": "rename_table", "name": name, "to": toks[5].name()}
            i = 4 + (1 if toks[4].up == "COLUMN" else 0)
            if i + 2 < len(toks) and toks[i + 1].up == "TO":
                return {"op": "rename_column", "name": name, "col": toks[i].name(), "to": toks[i + 2].name()}
    full = " ".join(t.up for t in toks)
    if re.match(r"CREATE( OR REPLACE)?( \w+)? (CONSTRAINT|INDEX)\b", full) or re.match(r"CREATE (CONSTRAINT|INDEX)\b", full):
        is_constraint = "CONSTRAINT" in ups[:4]
        kind = "index"
        if is_constraint:
            kind = ("node key" if re.search(r"IS (NODE |RELATIONSHIP |REL )?KEY", full) else
                    "unique" if "UNIQUE" in full else
                    "not null" if "IS NOT NULL" in full else
                    "typed" if re.search(r"IS (::|TYPED)", full) else "constraint")
        else:
            kind = next((f"{w.lower()} index" for w in ("FULLTEXT", "VECTOR", "TEXT", "POINT", "LOOKUP") if w in ups[:3]), "index")
        at = next(n for n, t in enumerate(toks) if t.up in ("CONSTRAINT", "INDEX"))
        after = toks[at + 1] if at + 1 < len(toks) else None
        named = after.name() if after is not None and after.kind in ("id", "bt") and after.up not in ("IF", "FOR", "ON") else None
        legacy = re.search(r"ON : (\w+) \( ([^)]*) \)", " ".join(t.text for t in toks))
        return {"op": "constraint" if is_constraint else "index", "kind": kind, "cname": named,
                "legacy": (legacy.group(1), [p.strip() for p in legacy.group(2).split(",")]) if legacy else None}
    if re.match(r"DROP (CONSTRAINT|INDEX)\b", full) and len(toks) >= 3:
        return {"op": "drop_named", "cname": toks[2].name()}
    return None


def scan(toks: list[Tok]) -> Statement:
    st = Statement()
    st.line = toks[0].line if toks else 0
    st.ddl = _ddl(toks)
    if st.ddl and st.ddl["op"] not in ("constraint", "index"):
        st.kind = "ddl"
        return st
    st.has_params = any(t.kind == "param" for t in toks)
    clause, csv_vars, i, n = "", set(), 0, len(toks)
    last_node: Node | None = None
    pending: Rel | None = None
    in_where = False

    def bind(var, kind, labels):
        if not var:
            return
        entry = st.bind.setdefault(var, {"kind": kind, "labels": []})
        for label in labels:
            if label not in entry["labels"]:
                entry["labels"].append(label)

    while i < n:
        t = toks[i]
        prev = toks[i - 1] if i else None
        if t.kind == "id" and t.up in CLAUSES and not (prev is not None and prev.text in (".", ":")) \
                and not (i + 1 < n and toks[i + 1].text == ":"):
            if prev is not None and prev.up == "ON" and t.up in ("CREATE", "MATCH"):   # ON CREATE SET / ON MATCH SET
                i += 1
                continue
            if t.up == "CREATE" and st.ddl:
                clause = "MATCH"
            else:
                clause = "MATCH" if t.up == "OPTIONAL" else "DELETE" if t.up == "DETACH" else t.up
            in_where = clause == "WHERE"
            st.has_where = st.has_where or in_where
            if clause == "LOAD":
                for k in range(i, min(n, i + 12)):
                    if toks[k].up == "AS" and k + 1 < n:
                        csv_vars.add(toks[k + 1].text)
                        break
            last_node = None
            i += 1
            continue
        if t.text == "(" and t.kind == "op":
            is_call = prev is not None and prev.kind == "id" and prev.up not in KEYWORDS
            parsed = None if is_call else _parse_node(toks, i, clause)
            if parsed:
                node, after = parsed
                bare = not node.labels and not node.props
                adjacent = pending is not None or (after < n and toks[after].text in ("-", "<") and _parse_rel(toks, after, clause))
                in_pattern = clause in PATTERN_CLAUSES and (prev is None or prev.up in CLAUSES or prev.text in (",", "=", "(") or prev.up in ("MATCH", "FOR"))
                if not bare or adjacent or (in_pattern and node.var):
                    st.nodes.append(node)
                    bind(node.var, "node", node.labels)
                    if pending is not None:
                        pending.right = node
                        st.rels.append(pending)
                        pending = None
                    last_node = node
                    i = after
                    if i < n and toks[i].text in ("-", "<"):
                        rel = _parse_rel(toks, i, clause)
                        if rel:
                            pending, i = rel
                            pending.left = last_node
                            bind(pending.var, "rel", pending.types)
                    continue
            pending = None
        if t.kind in ("id", "bt") and i + 2 < n and toks[i + 1].text == "." and toks[i + 2].kind in ("id", "bt") \
                and not (prev is not None and prev.text == "."):
            var, prop = t.name(), toks[i + 2].name()
            after = toks[i + 3] if i + 3 < n else None
            if clause == "SET" and after is not None and after.text in ("=", "+=") and prev is not None and (prev.up == "SET" or prev.text == ","):
                k, depth, value = i + 4, 0, []
                while k < n:
                    x = toks[k]
                    if x.kind == "op" and x.text in "([{":
                        depth += 1
                    elif x.kind == "op" and x.text in ")]}":
                        depth -= 1
                    elif depth == 0 and ((x.kind == "op" and x.text == ",") or (x.kind == "id" and (x.up in CLAUSES or x.up == "ON") and toks[k - 1].text != ".")):
                        break
                    value.append(x)
                    k += 1
                st.refs.append(Ref(var, prop, "write", value, t.line, i))
            elif clause == "REMOVE":
                st.removed.append((var, prop, None, i))
            else:
                st.refs.append(Ref(var, prop, "read", None, t.line, i))
                if in_where:
                    st.where_refs.add((var, prop))
                literal = None
                if after is not None and after.text in ("=", "<>", "<", ">", "<=", ">=") and i + 4 < n and toks[i + 4].kind in ("str", "num"):
                    literal = toks[i + 4]
                elif prev is not None and prev.text in ("=", "<>", "<", ">", "<=", ">=") and i >= 2 and toks[i - 2].kind in ("str", "num"):
                    literal = toks[i - 2]
                elif after is not None and after.text in ("=", "<>", "<", ">", "<=", ">=") and i + 5 < n \
                        and toks[i + 4].kind == "id" and toks[i + 5].text == "(":
                    close = _match_close(toks, i + 5)
                    if close > 0 and not (close + 1 < n and toks[close + 1].text == "."):
                        literal = Tok("func", toks[i + 4].text, toks[i + 4].line)
                if literal is not None:
                    st.compares.append((var, prop, literal))
            i += 3
            continue
        if t.kind in ("id", "bt") and prev is not None:
            nxt = toks[i + 1] if i + 1 < n else Tok("op", "", t.line)
            if clause == "SET" and (prev.up == "SET" or prev.text == ","):
                if nxt.text in ("+=", "=") and i + 2 < n and toks[i + 2].text == "{":
                    props, after_map = _parse_map(toks, i + 2)
                    for key, value in props.items():
                        st.refs.append(Ref(t.name(), key, "write", value, t.line, i))
                    i = after_map   # the map's own keys are not SET items
                    continue
                elif nxt.text == ":" and i + 2 < n and toks[i + 2].kind in ("id", "bt") and t.name() in st.bind:
                    bind(t.name(), "node", [toks[i + 2].name()])
                    st.nodes.append(Node(t.name(), [toks[i + 2].name()], {}, "SET", t.line))
            elif clause == "REMOVE" and nxt.text == ":" and i + 2 < n and toks[i + 2].kind in ("id", "bt"):
                st.removed.append((t.name(), None, toks[i + 2].name(), i))
            elif clause == "DELETE" and (prev.up in ("DELETE",) or prev.text == ","):
                st.deleted.append((t.name(), i))
            elif clause == "WHERE" and nxt.text == ":" and i + 2 < n and toks[i + 2].kind in ("id", "bt") and t.name() in st.bind:
                bind(t.name(), st.bind[t.name()]["kind"], [toks[i + 2].name()])
                st.nodes.append(Node(t.name(), [toks[i + 2].name()], {}, "WHERE", t.line))
            elif clause in ("WITH", "RETURN") and nxt.up == "AS" and i + 2 < n and t.name() in st.bind \
                    and (prev.up in ("WITH", "RETURN", "DISTINCT") or prev.text == ","):
                entry = st.bind[t.name()]
                bind(toks[i + 2].name(), entry["kind"], entry["labels"])
            elif nxt.text == "{" and t.name() in st.bind and clause in ("RETURN", "WITH"):
                end = _match_close(toks, i + 1)
                for k in range(i + 2, end if end > 0 else i + 2):
                    if toks[k].text == "." and toks[k - 1].text in ("{", ",") and toks[k + 1].kind in ("id", "bt"):
                        st.refs.append(Ref(t.name(), toks[k + 1].name(), "read", None, t.line, k))
        i += 1
    for node in st.nodes:
        for key, value in node.props.items():
            mode = "write" if node.clause in WRITE_CLAUSES else "read"
            st.refs.append(Ref(node.var, key, mode, value, node.line, -1, node))
    for rel in st.rels:
        for key, value in rel.props.items():
            mode = "write" if rel.clause in WRITE_CLAUSES else "read"
            st.refs.append(Ref(rel.var, key, mode, value, rel.line, -1, rel))
    st.kind = "ddl" if st.ddl else "write" if any(c.up in ("MERGE", "CREATE", "SET", "INSERT") for c in toks if c.kind == "id") else "read"
    st.csv_vars = csv_vars
    return st


def scan_file(path: Path) -> list[Statement]:
    out = []
    for text, first_line in cypher_chunks(path):
        for toks in statements(tokenize(text, first_line)):
            try:
                out.append(scan(toks))
            except (IndexError, KeyError, ValueError, StopIteration, AttributeError, TypeError):
                st = Statement()   # text this reader cannot follow is left out, never guessed at
                st.line, st.kind = toks[0].line, "unread"
                out.append(st)
    return out
