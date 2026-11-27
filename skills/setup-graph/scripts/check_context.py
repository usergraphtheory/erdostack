#!/usr/bin/env python3
"""Check the shape of docs/graph/CONTEXT.md, the file setup-graph writes for the other erdostack skills.

    python3 check_context.py [path/to/CONTEXT.md] [--root REPO_ROOT]

Run it from the repository root (or pass --root). It only reads: it changes nothing, starts nothing and
makes no network call. Standard library only.

It checks the format, not the truth of the facts:

  - a `## Facts` section holding exactly the seven keys, once each, as plain `key: value` lines
  - one bare value per line (no bullets, backticks, parentheses or trailing remarks)
  - `access` is `read-only` or `read-write`; `schema_snapshot` is `none` or a path that exists
  - script files named in `run_queries` exist
  - an `## Evidence` section that names at least one file that exists in the repo
  - an `## Open questions` section
  - nothing that looks like a copied credential

Exit status 0 when there is nothing to fix, 1 otherwise. Problems are printed one per line.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

KEYS = ["engine", "engine_version", "query_language", "driver", "run_queries", "access", "schema_snapshot"]
PLAIN = re.compile(r"^(" + "|".join(KEYS) + r"): ?(.*)$")
LOOSE = re.compile(r"^\s*(?:[-*+]\s+)?[`*_]{0,2}(" + "|".join(KEYS) + r")[`*_]{0,2}\s*[:=]\s*(.*)$", re.I)
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.*?)\s*#*\s*$")
VERSION = re.compile(r"\d+(?:\.\d+)+")
SCRIPT_SUFFIXES = (".sh", ".py", ".js", ".mjs", ".cjs", ".ts", ".rb", ".pl", ".jar", ".bat", ".ps1")
SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__", "target", ".gradle", ".agents", ".claude", ".cursor",
             ".codex", ".gemini"}
CREDENTIAL = [
    (re.compile(r"[a-z][a-z0-9+.-]*://[^\s/:@]+:[^\s/@<$*]+@", re.I), "a connection string with a password in it"),
    (re.compile(r"(?:password|passwd|secret|token|api[_-]?key|auth)\w*\s*=\s*[\"']?(?![<$*{\s])"
                r"([^\s\"'`,;)]{4,})", re.I), "a credential value"),
]
NOT_A_SECRET = {"unknown", "none", "required", "unset", "empty", "redacted", "changeme", "true", "false", "null"}


def sections(text: str) -> dict[str, list[str]]:
    """Heading (lower-cased) -> its lines. Lines inside code fences are kept but headings there are ignored."""
    out: dict[str, list[str]] = {"": []}
    current, fenced = "", False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            fenced = not fenced
        match = None if fenced else HEADING.match(line)
        if match:
            current = match.group(1).strip().lower()
            out.setdefault(current, [])
        else:
            out[current].append(line)
    return out


def find_section(parts: dict[str, list[str]], pattern: str) -> list[str] | None:
    for name, body in parts.items():
        if re.match(pattern, name):
            return body
    return None


def exists_in_repo(root: Path, rel: str) -> bool:
    """True when rel exists under root, at the top or as the tail of a deeper path (a sub-project)."""
    rel = rel.strip().lstrip("./").rstrip("/")
    if not rel or rel.startswith(("/", "~")) or ".." in Path(rel).parts:
        return False
    if (root / rel).exists():
        return True
    parts = Path(rel).parts
    try:
        for path in root.rglob(parts[-1]):
            if SKIP_DIRS & set(path.relative_to(root).parts):
                continue
            if path.parts[-len(parts):] == parts:
                return True
    except OSError:
        pass
    return False


def check(text: str, root: Path) -> list[str]:
    problems: list[str] = []
    parts = sections(text)

    facts_body = find_section(parts, r"facts\b")
    facts: dict[str, str] = {}
    if facts_body is None:
        problems.append("no `## Facts` section")
    else:
        for line in facts_body:
            if not line.strip():
                continue
            plain = PLAIN.match(line)
            if plain:
                key, value = plain.group(1), plain.group(2).strip()
                if key in facts:
                    problems.append(f"Facts: `{key}` appears more than once")
                    continue
                facts[key] = value
                continue
            loose = LOOSE.match(line)
            if loose:
                key = loose.group(1).lower()
                problems.append(f"Facts: write `{key}` as a plain line `{key}: value` (no bullet, backticks, "
                                "bold or indentation)")
                facts.setdefault(key, loose.group(2).strip().strip("`*"))
            else:
                problems.append(f"Facts: move this line out of the section (only the seven key lines belong "
                                f"there): {line.strip()[:60]!r}")
        for key in KEYS:
            if key not in facts:
                problems.append(f"Facts: `{key}` is missing")
        if [k for k in facts if k in KEYS] != [k for k in KEYS if k in facts]:
            problems.append("Facts: keep the keys in the agreed order: " + ", ".join(KEYS))

    remarked: set[str] = set()
    for key, value in facts.items():
        if not value:
            problems.append(f"Facts: `{key}` has no value (use `unknown`)")
            continue
        if "`" in value or value.startswith(("*", "_", '"', "'")):
            problems.append(f"Facts: `{key}` value should be bare text, without backticks, quotes or emphasis")
        if key != "run_queries" and re.search(r"[(;]|\s[-\u2013\u2014]\s|,\s", value):
            remarked.add(key)
            problems.append(f"Facts: `{key}` carries a remark ({value[:50]!r}); keep one value on the line and "
                            "move the explanation to Evidence or Open questions")
        if key == "run_queries" and re.search(r"\s\(|\s[\u2013\u2014]\s|\s#\s", value):
            problems.append("Facts: `run_queries` should be the command alone; move the explanation to Evidence")

    access = facts.get("access")
    if access is not None and access not in ("read-only", "read-write") and "access" not in remarked:
        problems.append(f"Facts: `access` must be exactly `read-only` or `read-write`, found {access[:40]!r}")

    snapshot = facts.get("schema_snapshot")
    if snapshot and snapshot != "none":
        if snapshot.lower() in ("unknown", "n/a", "na", "-", "null"):
            problems.append("Facts: `schema_snapshot` is a path or `none`")
        elif not (root / snapshot.lstrip("./")).exists():
            problems.append(f"Facts: `schema_snapshot` path does not exist in the repo: {snapshot[:80]}")

    version = facts.get("engine_version")
    if version and version != "unknown" and "engine_version" not in remarked \
            and not re.fullmatch(r"v?\d+(?:\.\d+)*", version):
        problems.append(f"Facts: `engine_version` should be the pinned version number alone, or `unknown` "
                        f"(found {version[:40]!r})")

    driver = facts.get("driver")
    if driver and driver not in ("unknown", "none") and "driver" not in remarked \
            and not re.fullmatch(r"\S+ v?\d+(?:\.\d+)+\S*", driver):
        problems.append("Facts: `driver` should be `<package> <locked version>`, or `unknown` "
                        f"(found {driver[:50]!r})")

    engine = facts.get("engine")
    if engine and VERSION.search(engine):
        problems.append("Facts: `engine` should be the name alone; the version goes in `engine_version`")

    command = facts.get("run_queries")
    if command and command not in ("unknown", "none"):
        for token in command.split():
            token = token.strip("'\"")
            if re.search(r"[<>{}$*=]|://", token) or token.startswith(("-", "/", "~")):
                continue
            if token.lower().endswith(SCRIPT_SUFFIXES) and not exists_in_repo(root, token):
                problems.append(f"Facts: `run_queries` names a script that is not in the repo: {token}")

    evidence = find_section(parts, r"evidence\b")
    if evidence is None:
        problems.append("no `## Evidence` section (say which repo file each fact came from)")
    else:
        cited = False
        for token in re.findall(r"[\w./@+-]+", "\n".join(evidence)):
            token = token.strip(".").lstrip("./")
            looks_like_file = "." in token or "/" in token or token in ("Makefile", "Dockerfile", "justfile")
            if looks_like_file and not token.startswith("docs/graph") and exists_in_repo(root, token):
                cited = True
                break
        if not cited:
            problems.append("Evidence names no file that exists in the repo")

    if find_section(parts, r"open\s+questions\b") is None:
        problems.append("no `## Open questions` section (write `- None.` when there is nothing to raise)")

    for pattern, what in CREDENTIAL:
        for match in pattern.finditer(text):
            value = match.group(1) if match.groups() else ""
            if value.lower().strip(".") in NOT_A_SECRET:
                continue
            line = text.count("\n", 0, match.start()) + 1
            problems.append(f"line {line}: looks like {what}; name the variable and its file, never the value")
    return problems


def main(argv: list[str]) -> int:
    args = list(argv[1:])
    root = Path.cwd()
    if "--root" in args:
        index = args.index("--root")
        if index + 1 >= len(args):
            print("usage: check_context.py [path/to/CONTEXT.md] [--root REPO_ROOT]")
            return 2
        root = Path(args[index + 1])
        del args[index:index + 2]
    path = Path(args[0]) if args else Path("docs/graph/CONTEXT.md")
    if not path.is_absolute() and not path.exists():
        path = root / path
    if not path.is_file():
        print(f"not found: {path}")
        return 1
    problems = check(path.read_text(encoding="utf-8", errors="replace"), root)
    for problem in problems:
        print(problem)
    if not problems:
        print("ok: docs/graph/CONTEXT.md has the agreed shape (the facts themselves are not checked)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
