"""The schema snapshot file: one markdown layout that people read and these scripts parse.

Standard library only. Layout (see references/snapshot-format.md beside the skill):

    # Graph schema snapshot
    ## Facts                 key: value lines (taken, store, source, refresh, coverage, fingerprint ...)
    ## Index                 one line per node kind / table and per relationship pattern
    ## Nodes | ## Tables     ### <name>, then "- `property` TYPE · details" lines
    ## Relationships         ### <TYPE>, then "- pattern: (:A)-[:TYPE]->(:B)" and property lines
    ## Retired or superseded names that exist in old files but not in the store any more
    ## Verified semantics    hand-written notes, kept when the generated part is refreshed
"""
from __future__ import annotations

import datetime
import hashlib
import re
from pathlib import Path

DEFAULT_PATH = "docs/graph/schema.md"
CONTEXT_PATH = "docs/graph/CONTEXT.md"
TITLE = "# Graph schema snapshot"
SEMANTICS = "Verified semantics"
GENERATED_BY = "erdostack schema-first"
SEP = " · "

PROP_RE = re.compile(r"^- `([^`]+)`(?:\s+([^\s·]+))?(.*)$")
PATTERN_RE = re.compile(r"^- pattern: \(:?([^)]*)\)(<?-)\[:([^\]]+)\](->?)\(:?([^)]*)\)(.*)$")


def today() -> str:
    return datetime.date.today().isoformat()


def digest(*parts: bytes | str) -> str:
    h = hashlib.sha256()
    for part in parts:
        h.update(part.encode("utf-8") if isinstance(part, str) else part)
        h.update(b"\x00")
    return h.hexdigest()[:16]


def snapshot_path(explicit: str | None = None) -> Path:
    """--snapshot wins; else the path docs/graph/CONTEXT.md names as schema_snapshot; else the default."""
    if explicit:
        return Path(explicit)
    context = Path(CONTEXT_PATH)
    if context.is_file():
        for line in context.read_text(encoding="utf-8", errors="replace").splitlines():
            match = re.match(r"^\s*schema_snapshot\s*:\s*(\S.*?)\s*$", line)
            if match and match.group(1).strip("`'\"").lower() not in ("none", "unknown", ""):
                return Path(match.group(1).strip("`'\""))
    return Path(DEFAULT_PATH)


class Element:
    """One `### name` entry: a node kind, a table or a relationship type, with its raw lines."""

    def __init__(self, name: str, lines: list[str] | None = None):
        self.name = name
        self.lines = lines or []

    def props(self) -> dict[str, tuple[str, str]]:
        """{property: (type, rest of the line)} from the "- `name` TYPE · ..." lines."""
        out = {}
        for line in self.lines:
            match = PROP_RE.match(line)
            if match:
                out[match.group(1)] = ((match.group(2) or "").strip(), match.group(3).strip(" ·"))
        return out

    def patterns(self) -> list[tuple[str, str, bool]]:
        """[(start kind, end kind, directed)] from "- pattern:" lines, arrows normalised left to right."""
        out = []
        for line in self.lines:
            match = PATTERN_RE.match(line)
            if not match:
                continue
            left, larrow, _type, rarrow, right = match.group(1, 2, 3, 4, 5)
            if larrow == "<-":
                out.append((right, left, True))
            else:
                out.append((left, right, rarrow == "->"))
        return out


class Snapshot:
    def __init__(self):
        self.facts: dict[str, str] = {}
        self.sections: dict[str, list[str]] = {}      # section title -> raw lines (without the heading)
        self.elements: dict[str, dict[str, Element]] = {}  # section title -> {name: Element}
        self.semantics: list[str] = []
        self.text = ""

    # -- reading ---------------------------------------------------------------
    @classmethod
    def parse(cls, text: str) -> "Snapshot":
        snap = cls()
        snap.text = text
        section = None
        element = None
        for raw in text.splitlines():
            line = raw.rstrip()
            if line.startswith("## "):
                section = line[3:].strip()
                snap.sections[section] = []
                snap.elements[section] = {}
                element = None
                continue
            if section is None:
                continue
            snap.sections[section].append(line)
            if section == "Facts":
                match = re.match(r"^([A-Za-z_][\w ]*?):\s*(.*)$", line)
                if match:
                    snap.facts[match.group(1).strip()] = match.group(2).strip()
            elif section == SEMANTICS:
                snap.semantics.append(line)
            elif line.startswith("### "):
                heading = line[4:].strip()
                as_pattern = PATTERN_RE.match("- pattern: " + heading.strip("`"))
                if as_pattern:   # a hand-written heading that is itself a pattern: file it under its type
                    element = snap.elements[section].setdefault(as_pattern.group(3), Element(as_pattern.group(3)))
                    element.lines.append("- pattern: " + heading.strip("`"))
                else:
                    name = heading.strip("`").lstrip(":").strip("`")
                    element = snap.elements[section].setdefault(name, Element(name))
            elif element is not None and line:
                element.lines.append(line)
        return snap

    @classmethod
    def load(cls, path: Path) -> "Snapshot | None":
        if not path.is_file():
            return None
        return cls.parse(path.read_text(encoding="utf-8", errors="replace"))

    def mentions(self, name: str) -> bool:
        """True when the name appears anywhere in the file as a whole word, parsed entry or not."""
        return bool(re.search(rf"(?<![\w]){re.escape(name)}(?![\w])", self.text))

    def parseable(self) -> bool:
        return bool(self.nodes() or self.rels())

    def is_generated(self) -> bool:
        return bool(self.facts.get("fingerprint")) and self.facts.get("fingerprint") != "none"

    def kinds(self, *titles: str) -> dict[str, Element]:
        out: dict[str, Element] = {}
        for title in titles:
            out.update(self.elements.get(title, {}))
        return out

    def _noted(self, home: dict[str, Element]) -> dict[str, Element]:
        """Hand-written notes of the form `Kind.property ...` add that property to the kind's entry."""
        for line in self.semantics:
            for kind, prop in re.findall(r"(?<![\w.])`?([A-Za-z_]\w*)\.([A-Za-z_]\w*)`?", line):
                if kind in home and prop not in home[kind].props():
                    home[kind].lines.append(f"- `{prop}` · noted by hand under {SEMANTICS}")
        return home

    def nodes(self) -> dict[str, Element]:
        return self._noted(self.kinds("Nodes", "Tables", "Views", "Node kinds", "Node tables", "Labels"))

    def rels(self) -> dict[str, Element]:
        return self._noted(self.kinds("Relationships", "Edges", "Relationship types", "Rel tables"))

    def retired(self) -> list[str]:
        return [l for l in self.sections.get("Retired or superseded", []) if l.startswith("- ")]


def render(facts: dict[str, str], body: list[str], semantics: list[str] | None) -> str:
    """Assemble the file. `body` is every generated line from "## Index" on; semantics is kept verbatim."""
    out = [TITLE, "",
           f"Generated by {GENERATED_BY}. Everything above \"## {SEMANTICS}\" is rewritten on refresh: do not edit it by hand.",
           f"Notes under \"## {SEMANTICS}\" are kept. Names are spelled exactly as the store spells them.",
           "", "## Facts", ""]
    out += [f"{key}: {value}" for key, value in facts.items()]
    out += [""] + body
    while out and not out[-1].strip():
        out.pop()
    notes = [l for l in (semantics or [])]
    while notes and not notes[0].strip():
        notes.pop(0)
    while notes and not notes[-1].strip():
        notes.pop()
    if not notes:
        notes = ["What a direction, unit, code or flag means, each checked against the data, one line each with how it",
                 "was checked. Nothing recorded yet."]
    out += ["", f"## {SEMANTICS}", ""] + notes + [""]
    return "\n".join(out)


def write_snapshot(path: Path, facts: dict[str, str], body: list[str], force: bool = False) -> str:
    """Write the snapshot, keeping hand-written notes. Refuses to replace a file this tool did not generate."""
    old = Snapshot.load(path)
    if old is not None and not old.is_generated() and not force:
        raise SystemExit(
            f"{path} exists and was not generated by this tool (no fingerprint line). It was left untouched.\n"
            "Treat it as the snapshot: read it, and correct single entries by hand if the store disagrees.\n"
            "Pass --force only if the user wants it replaced.")
    text = render(facts, body, old.semantics if old else None)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return text


def fmt_value(value, limit: int = 40) -> str:
    """A sample value as it would be written in a query: quoted text, bare numbers."""
    if isinstance(value, str):
        shown = value if len(value) <= limit else value[: limit - 1] + "…"
        return "'" + shown.replace("\n", " ") + "'"
    if isinstance(value, bytes):
        return f"<{len(value)} bytes>"
    if isinstance(value, float):
        return f"{value:g}"
    return str(value)
