"""Schema of a graph database rebuilt from the files that define and load it. Standard library only.

Used when no live database can be asked. Files are read in the order given (directories in path order, which
is how numbered migrations are applied), so a later file can retire what an earlier one created. The result
is evidence from files, and the snapshot says so: it is weaker than asking the database.
"""
from __future__ import annotations

from pathlib import Path

from sf_cypher import CYPHER_SUFFIXES, WRITE_CLAUSES, Node, Rel, scan_file, value_type
from sf_format import SEP, digest, today

SOURCE_SUFFIXES = {".py", ".js", ".mjs", ".ts", ".java", ".kt", ".go", ".rb", ".cs", ".php", ".scala", ".rs", ".groovy"}
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".agents", ".claude", "dist", "build", "target"}
STRONG = ("primary key", "unique", "node key", "not null", "typed", "indexed", "defined", "written")


def collect_files(inputs: list[str]) -> list[Path]:
    files: list[Path] = []
    for item in inputs:
        path = Path(item)
        if path.is_dir():
            found = [p for p in sorted(path.rglob("*")) if p.is_file() and not (set(p.parts) & SKIP_DIRS)
                     and p.suffix.lower() in CYPHER_SUFFIXES | SOURCE_SUFFIXES]
            files += found
        elif path.is_file():
            files.append(path)
        else:
            raise SystemExit(f"{item}: no such file or directory")
    seen, out = set(), []
    for f in files:
        if f not in seen:
            seen.add(f)
            out.append(f)
    return out


def fingerprint(inputs: list[str]) -> str:
    return digest(*[part for f in collect_files(inputs) for part in (str(f), f.read_bytes())])


class Prop:
    def __init__(self):
        self.types: list[str] = []
        self.evidence: list[str] = []
        self.samples: list[str] = []
        self.written = None
        self.removed = None
        self.removed_at = ""

    def add(self, evidence: str, type_: str = "", sample: str | None = None):
        if evidence not in self.evidence:
            self.evidence.append(evidence)
        if type_ and type_ not in self.types:
            self.types.append(type_)
        if sample is not None and sample not in self.samples and len(self.samples) < 5:
            self.samples.append(sample)

    def strong(self) -> bool:
        return any(e in STRONG for e in self.evidence)


class Kind:
    """A label / node table, or a relationship type / rel table."""

    def __init__(self):
        self.props: dict[str, Prop] = {}
        self.files: list[str] = []
        self.evidence: list[str] = []
        self.written = None
        self.deleted = None
        self.deleted_at = ""
        self.patterns: dict[tuple[str, str], dict] = {}
        self.undirected: list[str] = []

    def prop(self, name: str) -> Prop:
        return self.props.setdefault(name, Prop())

    def seen(self, file: str, evidence: str):
        if file not in self.files:
            self.files.append(file)
        if evidence not in self.evidence:
            self.evidence.append(evidence)


class Inventory:
    def __init__(self):
        self.nodes: dict[str, Kind] = {}
        self.rels: dict[str, Kind] = {}
        self.constraints: dict[str, str] = {}
        self.retired: list[str] = []
        self.review: list[str] = []
        self._anon = 0

    def node(self, name: str) -> Kind:
        return self.nodes.setdefault(name, Kind())

    def rel(self, name: str) -> Kind:
        return self.rels.setdefault(name, Kind())

    # -- reading ---------------------------------------------------------------
    def read(self, files: list[Path]) -> None:
        for file_no, path in enumerate(files):
            try:
                found = scan_file(path)
            except (OSError, UnicodeError):
                continue
            for stmt_no, st in enumerate(found):
                self.statement(st, (file_no, stmt_no), f"{path}:{st.line}")

    def statement(self, st, seq, where: str) -> None:
        file = where.rsplit(":", 1)[0]
        ddl = st.ddl
        if ddl and ddl["op"] in ("node_table", "rel_table"):
            kind = self.node(ddl["name"]) if ddl["op"] == "node_table" else self.rel(ddl["name"])
            kind.seen(file, "defined")
            kind.written, kind.deleted = seq, None
            for col, type_ in ddl["cols"].items():
                prop = kind.prop(col)
                prop.add("primary key" if col in ddl["key"] else "defined", type_)
                prop.written, prop.removed = seq, None
            for a, b in ddl["pairs"]:
                kind.patterns[(a, b)] = {"evidence": "defined", "file": where, "written": seq, "deleted": None, "deleted_at": ""}
            return
        if ddl and ddl["op"] in ("drop_table", "add_column", "drop_column", "rename_table", "rename_column"):
            home = self.nodes if ddl["name"] in self.nodes else self.rels
            kind = home.get(ddl["name"])
            if kind is None:
                return
            if ddl["op"] == "drop_table":
                kind.deleted, kind.deleted_at = seq, where
            elif ddl["op"] == "add_column":
                prop = kind.prop(ddl["col"])
                prop.add("defined", ddl["type"])
                prop.written, prop.removed = seq, None
            elif ddl["op"] == "drop_column" and ddl["col"] in kind.props:
                kind.props[ddl["col"]].removed, kind.props[ddl["col"]].removed_at = seq, where
            elif ddl["op"] == "rename_table":
                home[ddl["to"]] = home.pop(ddl["name"])
                self.retired.append(f"- {ddl['name']}: renamed to {ddl['to']} in {where}")
                for other in self.rels.values():
                    other.patterns = {(ddl["to"] if a == ddl["name"] else a, ddl["to"] if b == ddl["name"] else b): v
                                      for (a, b), v in other.patterns.items()}
            elif ddl["op"] == "rename_column" and ddl["col"] in kind.props:
                kind.props[ddl["to"]] = kind.props.pop(ddl["col"])
                self.retired.append(f"- {ddl['name']}.{ddl['col']}: renamed to {ddl['to']} in {where}")
            return
        if ddl and ddl["op"] == "drop_named":
            self.constraints.pop(ddl["cname"], None)
            return

        def labels_for(owner_or_var) -> tuple[str, list[str]]:
            if isinstance(owner_or_var, Node):
                return "node", owner_or_var.labels or st.labels_of(owner_or_var.var)
            if isinstance(owner_or_var, Rel):
                return "rel", owner_or_var.types or st.labels_of(owner_or_var.var)
            entry = st.bind.get(owner_or_var)
            return (entry["kind"], entry["labels"]) if entry else ("", [])

        is_schema = bool(ddl)
        for node in st.nodes:
            for label in node.labels:
                kind = self.node(label)
                wrote = node.clause in WRITE_CLAUSES or node.clause == "SET"
                kind.seen(file, "defined" if is_schema else "written" if wrote else "read")
                if wrote or is_schema:
                    kind.written = seq
        for rel in st.rels:
            start, end = rel.ends()
            starts = (start.labels or st.labels_of(start.var)) if start else []
            ends = (end.labels or st.labels_of(end.var)) if end else []
            wrote = rel.clause in WRITE_CLAUSES
            for type_ in rel.types:
                kind = self.rel(type_)
                kind.seen(file, "defined" if is_schema else "written" if wrote else "read")
                if wrote:
                    kind.written = seq
                if rel.direction == "none":
                    if where not in kind.undirected:
                        kind.undirected.append(where)
                    continue
                for a in starts or ["?"]:
                    for b in ends or ["?"]:
                        entry = kind.patterns.setdefault((a, b), {"evidence": "read", "file": where, "written": None, "deleted": None, "deleted_at": ""})
                        if wrote:
                            if entry["evidence"] != "defined":
                                entry["evidence"] = "written"
                                entry["file"] = where if entry["written"] is None else entry["file"]
                            entry["written"] = seq
        if ddl and ddl.get("legacy"):
            label, props = ddl["legacy"]
            for name in props:
                self.node(label).prop(name).add("indexed")
            self.node(label).seen(file, "defined")
        for ref in st.refs:
            what, names = labels_for(ref.owner if ref.owner is not None else ref.var)
            if not names:
                continue
            home = self.node if what == "node" else self.rel
            type_, sample = value_type(ref.value or [], st.csv_vars) if ref.value is not None else ("", None)
            for name in names:
                prop = home(name).prop(ref.prop)
                if is_schema:
                    prop.add(ddl["kind"] if ddl["op"] == "constraint" else "indexed")
                    label = f"{ddl['kind']}: {name}.{ref.prop}"
                    self.constraints[ddl.get("cname") or label] = label + (f" ({ddl['cname']})" if ddl.get("cname") else "")
                elif ref.mode == "write":
                    prop.add("written", type_, sample)
                    prop.written = seq
                else:
                    prop.add("read", "", sample if type_ in ("STRING", "INTEGER", "FLOAT") else None)
        for var, name, literal in st.compares:
            if literal.kind == "func":
                continue
            what, names = labels_for(var)
            for owner in names:
                home = self.node if what == "node" else self.rel
                home(owner).prop(name).add("read", "", literal.text)
        whole = not st.has_params
        removed_props = {(var, prop) for var, prop, _label, _i in st.removed if prop}
        for var, prop_name, label, _i in st.removed:
            what, names = labels_for(var)
            if prop_name and whole and st.where_refs <= removed_props:
                for owner in names:
                    home = self.node if what == "node" else self.rel
                    prop = home(owner).prop(prop_name)
                    prop.removed, prop.removed_at = seq, where
            elif label and whole and not st.has_where and label in self.nodes:
                self.nodes[label].deleted, self.nodes[label].deleted_at = seq, where
        for var, _i in st.deleted:
            if not whole or st.has_where:
                continue
            for rel in st.rels:
                if rel.var != var or rel.props or rel.direction == "none":
                    continue
                start, end = rel.ends()
                if (start and start.props) or (end and end.props):
                    continue
                for type_ in rel.types:
                    for (a, b), entry in self.rel(type_).patterns.items():
                        if a in ((start.labels or st.labels_of(start.var)) or [a]) and b in ((end.labels or st.labels_of(end.var)) or [b]):
                            entry["deleted"], entry["deleted_at"] = seq, where
            for node in st.nodes:
                if node.var == var and node.labels and not node.props and not any(r.left is node or r.right is node for r in st.rels):
                    for label in node.labels:
                        self.nodes[label].deleted, self.nodes[label].deleted_at = seq, where

    # -- deciding what is retired ---------------------------------------------------
    def settle(self, keep: set[str]) -> None:
        def gone(written, removed) -> bool:
            return removed is not None and (written is None or removed > written)

        for home, shape in ((self.nodes, "node"), (self.rels, "rel")):
            for name in list(home):
                kind = home[name]
                for (a, b) in list(kind.patterns):
                    entry = kind.patterns[(a, b)]
                    shown = f"(:{a})-[:{name}]->(:{b})"
                    if gone(entry["written"], entry["deleted"]) and name not in keep:
                        self.retired.append(f"- {name} as {shown}: every match deleted in {entry['deleted_at']} and not written "
                                            f"again (first seen in {entry['file']}). Do not use.")
                        del kind.patterns[(a, b)]
                for prop_name in list(kind.props):
                    prop = kind.props[prop_name]
                    if gone(prop.written, prop.removed) and f"{name}.{prop_name}" not in keep:
                        self.retired.append(f"- {name}.{prop_name}: removed in {prop.removed_at} and not set again. Do not use.")
                        del kind.props[prop_name]
                emptied = shape == "rel" and not kind.patterns and not kind.undirected and any(name in line for line in self.retired)
                if (gone(kind.written, kind.deleted) or emptied) and name not in keep:
                    if not emptied:
                        self.retired.append(f"- {name}: dropped or deleted everywhere in {kind.deleted_at} and not written again. Do not use.")
                    del home[name]
        for line in self.retired:
            self.review.append("retired by rule (confirm, or re-run with --keep NAME): " + line[2:].split(":")[0])
        for name, kind in self.rels.items():
            known = {p for p in kind.patterns if "?" not in p}
            if known:
                for p in [p for p in kind.patterns if "?" in p]:
                    del kind.patterns[p]
            elif kind.patterns or kind.undirected:
                self.review.append(f"{name}: endpoint kinds or direction could not be read from these files.")

    # -- writing ----------------------------------------------------------------
    @staticmethod
    def prop_line(name: str, prop: Prop) -> str:
        parts = [f"- `{name}`" + (f" {'|'.join(prop.types)}" if prop.types else "")]
        tags = [e for e in prop.evidence if e in ("primary key", "unique", "node key", "not null", "typed", "indexed")]
        if tags:
            parts.append(", ".join(tags))
        if not prop.strong():
            parts.append("only read in these files, never defined or written: set by something outside them")
        if len(prop.types) > 1:
            parts.append("written with different types in different places")
        if prop.samples:
            parts.append("e.g. " + ", ".join(prop.samples[:4]))
        return SEP.join(parts)

    def render(self, inputs: list[str], files: list[Path]) -> tuple[dict, list[str]]:
        index, nodes, rels = [], [], []
        for name in sorted(self.nodes):
            kind = self.nodes[name]
            weak = "" if any(e in ("defined", "written") for e in kind.evidence) or any(p.strong() for p in kind.props.values()) \
                else " (only matched, never defined or written in these files)"
            index.append(f"- {name}{weak}: {', '.join(kind.props) or 'no properties seen'}")
            nodes.append(f"### {name}")
            nodes.append("seen in: " + ", ".join(kind.files[:4]) + (f" and {len(kind.files) - 4} more" if len(kind.files) > 4 else "") + weak)
            nodes += [self.prop_line(n, p) for n, p in kind.props.items()] + [""]
        for name in sorted(self.rels):
            kind = self.rels[name]
            rels.append(f"### {name}")
            props = ", ".join(kind.props)
            for (a, b), entry in kind.patterns.items():
                note = {"defined": "defined in", "written": "written in", "read": "only matched, never written, in"}[entry["evidence"]]
                rels.append(f"- pattern: (:{a})-[:{name}]->(:{b}){SEP}{note} {entry['file']}")
                index.append(f"- (:{a})-[:{name}]->(:{b})" + (f": {props}" if props else ""))
            if not kind.patterns:
                rels.append(f"- direction and endpoint kinds unknown: only seen without an arrow in {', '.join(kind.undirected[:3])}")
                index.append(f"- [:{name}] direction unknown" + (f": {props}" if props else ""))
            rels += [self.prop_line(n, p) for n, p in kind.props.items()] + [""]
        body = ["## Index", "",
                "One line per node kind (properties) and per relationship pattern, arrow as stored. Look the entry up below before using it.", ""]
        body += index + ["", "## Nodes", ""] + nodes + ["## Relationships", ""] + rels
        if self.constraints:
            body += ["## Constraints and indexes", ""] + [f"- {text}" for text in self.constraints.values()] + [""]
        if self.retired:
            body += ["## Retired or superseded", "",
                     "Names that older files still mention but that later files removed. They are not in the store any more.", ""]
            body += self.retired + [""]
        facts = {
            "taken": today(),
            "store": "graph database, not reachable when this was taken",
            "source": "files (static read, nothing was executed)",
            "refresh": "schema.py cypher-files " + " ".join(inputs),
            "method": "schema.py cypher-files (constraints, indexes, table DDL and every pattern in the inputs, in path order; a later file can retire an earlier one)",
            "files_read": str(len(files)),
            "coverage": f"what the inputs define, write or match: {len(self.nodes)} node kinds, {len(self.rels)} relationship types. "
                        "Anything created outside these files is missing; property types are known only where a file states or converts them",
            "fingerprint": fingerprint(inputs),
        }
        return facts, body


def take(inputs: list[str], keep: set[str] | None = None) -> tuple[dict, list[str], list[str]]:
    files = collect_files(inputs)
    inv = Inventory()
    inv.read(files)
    inv.settle(keep or set())
    if not inv.nodes and not inv.rels:
        raise SystemExit("No labels, relationship types or table definitions were found in: " + " ".join(inputs) +
                         "\nNothing was written. If no file in the repository defines the schema, there is no schema source: say so.")
    facts, body = inv.render(inputs, files)
    return facts, body, inv.review
