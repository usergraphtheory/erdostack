#!/usr/bin/env python3
"""Take, read and use the graph schema snapshot (default docs/graph/schema.md). Run from the repository root.

    schema.py status                         is there a snapshot, and does it still match the store?
    schema.py sqlite PATH.db                 snapshot a SQLite database (read-only)
    schema.py networkx --load pkg.mod:func   snapshot the graph the repository's loader returns
    schema.py networkx --file graph.graphml  ... or a graph file (.graphml .gml .gexf, node-link .json)
    schema.py cypher-files PATH [PATH ...]   snapshot from Cypher DDL, constraints, migrations and loaders (no database)
    schema.py sql-files PATH [PATH ...]      snapshot from .sql table definitions (no database, so no value formats)
    schema.py show NAME [NAME ...]           print the entries for these tables / labels / relationship types
    schema.py check FILE [FILE ...]          compare .cypher, .sql and .py files with the snapshot

Python standard library only. No network access. Nothing is written except the snapshot file.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True   # leave nothing behind in the skill folder
sys.path.insert(0, str(Path(__file__).resolve().parent))

import sf_check      # noqa: E402
import sf_inventory  # noqa: E402
import sf_networkx   # noqa: E402
import sf_sqlite     # noqa: E402
from sf_format import SEMANTICS, Snapshot, snapshot_path, write_snapshot  # noqa: E402


SMALL = 90   # snapshots up to this many lines are printed whole; larger ones print the Index only


def overview(snap: Snapshot, text: str) -> None:
    """Print what a query writer reads first: the whole snapshot when it is small, else its Index."""
    lines = text.splitlines()
    shown = ("store", "graph_class", "node_kind_attribute", "edge_kind_attribute", "values")
    print("## Facts")
    print("\n".join(f"{key}: {snap.facts[key]}" for key in shown if key in snap.facts))
    if len(lines) <= SMALL:
        start = next((n for n, l in enumerate(lines) if l.startswith("## Index")), 0)
        skip = ("What a direction, unit, code", "was checked. Nothing recorded yet.")
        body = [l for l in lines[start:] if l.strip() and not l.startswith(skip)]
        if body and body[-1].startswith(f"## {SEMANTICS}"):
            body.pop()
        print("\n".join(body))
        return
    print("## Index (entries with types, stored values and notes: `schema.py show NAME ...`)")
    print("\n".join(l for l in snap.sections.get("Index", []) if l.startswith("- ")))
    retired = snap.retired()
    if retired:
        print("## Retired or superseded")
        print("\n".join(retired))
    notes = [l for l in snap.semantics if l.strip() and "Nothing recorded yet" not in l and not l.startswith("What a direction")]
    if notes:
        print(f"## {SEMANTICS}")
        print("\n".join(notes))


def finish(path: Path, facts: dict, body: list[str], review: list[str], force: bool) -> None:
    existed = path.is_file()
    text = write_snapshot(path, facts, body, force)
    print(f"{'refreshed' if existed else 'wrote'} {path} ({len(text.splitlines())} lines) from: {facts['source']}. Coverage: {facts['coverage']}")
    overview(Snapshot.parse(text), text)
    if review:
        print(f"Only a look at the data or its writer can settle these; note each answer under \"## {SEMANTICS}\":")
        for line in review[:12]:
            print("  - " + line)
        if len(review) > 12:
            print(f"  ... and {len(review) - 12} more of the same kind")


def cmd_sqlite(args) -> int:
    try:
        facts, body, review = sf_sqlite.take(args.database, args.max_rows, not args.no_samples)
    except FileNotFoundError:
        print(f"unreachable: {args.database} does not exist here. Nothing was written.")
        return 2
    finish(snapshot_path(args.snapshot), facts, body, review, args.force)
    return 0


def networkx_inputs(args) -> str:
    extra = "".join(f" --{name}-kind {value}" for name, value in (("node", args.node_kind), ("edge", args.edge_kind)) if value)
    return (f"--load {args.load}" if args.load else f"--file {args.file}") + extra


def cmd_networkx(args) -> int:
    if not args.load and not args.file:
        print("give --load package.module:function (the repository's own loader) or --file PATH")
        return 2
    try:
        graph, origin, _deps = sf_networkx.load(args.load, args.file)
    except Exception as exc:  # noqa: BLE001 - the loader is the repository's code; report, do not trace
        print(f"unreachable: the graph could not be loaded ({type(exc).__name__}: {exc}). Nothing was written.")
        return 2
    facts, body, review = sf_networkx.take(graph, origin, networkx_inputs(args), args.node_kind, args.edge_kind, not args.no_samples)
    finish(snapshot_path(args.snapshot), facts, body, review, args.force)
    return 0


def cmd_cypher_files(args) -> int:
    facts, body, review = sf_inventory.take(args.paths, set(args.keep or []))
    facts["refresh"] += "".join(f" --keep {name}" for name in args.keep or [])
    finish(snapshot_path(args.snapshot), facts, body, review, args.force)
    print("This is evidence from files, not from the database: say so, and prefer a live introspection when one is possible.")
    return 0


def cmd_sql_files(args) -> int:
    try:
        con, ran, skipped = sf_sqlite.from_ddl(args.paths)
    except FileNotFoundError as exc:
        print(f"unreachable: {exc} does not exist here. Nothing was written.")
        return 2
    if not ran:
        print("No CREATE TABLE statement in these files could be read. Nothing was written."
              + ("".join("\n  skipped " + line for line in skipped[:8])))
        return 2
    facts, body, review = sf_sqlite.take("", 0, False, con)
    joined = " ".join(args.paths)
    facts.update({
        "store": "SQL database, not reachable when this was taken",
        "source": "files (table definitions run in an empty SQLite database; no rows were seen)",
        "refresh": f"schema.py sql-files {joined}",
        "method": "schema.py sql-files (CREATE / ALTER / DROP statements of the given .sql files, in path order)",
        "coverage": facts["coverage"].replace("complete: ", "names, types and declared keys only: ")
                    + (f"; {len(skipped)} statements were not understood and are missing" if skipped else "")
                    + ". Nothing is known about stored values, units or codes",
        "values": "none: there were no rows to look at",
        "fingerprint": sf_sqlite.ddl_fingerprint(args.paths),
    })
    body = [line.replace("rows: 0 · ", "").replace(" (0 rows)", "") for line in body if line != "rows: 0"]
    finish(snapshot_path(args.snapshot), facts, body, review, args.force)
    for line in skipped[:8]:
        print("not understood (another SQL dialect?): " + line)
    print("This is evidence from files, not from the database: say so, and look at real rows before trusting how a value is stored.")
    return 0


def current_fingerprint(snap: Snapshot) -> tuple[str | None, str]:
    """(fingerprint of the store as it is now, or None when it cannot be reached; the command that refreshes)."""
    refresh = snap.facts.get("refresh", "")
    words = refresh.split()
    if len(words) < 3 or words[0] != "schema.py":
        return None, refresh
    kind, rest = words[1], words[2:]
    try:
        if kind == "sqlite":
            return sf_sqlite.fingerprint(" ".join(rest)), refresh
        if kind == "sql-files":
            return sf_sqlite.ddl_fingerprint(rest), refresh
        if kind == "cypher-files":
            paths = [w for n, w in enumerate(rest) if not w.startswith("--") and not (n and rest[n - 1] == "--keep")]
            return sf_inventory.fingerprint(paths), refresh
        if kind == "networkx":
            load = rest[rest.index("--load") + 1] if "--load" in rest else None
            file = rest[rest.index("--file") + 1] if "--file" in rest else None
            graph, origin, _deps = sf_networkx.load(load, file)
            kinds = [snap.facts.get(k, "") for k in ("node_kind_attribute", "edge_kind_attribute")]
            kinds = [k if re.fullmatch(r"\w+", k) else "none" for k in kinds]
            if snap.facts.get("edge_kind_attribute") == "the edge key":
                kinds[1] = None
            facts, _body, _review = sf_networkx.take(graph, origin, " ".join(rest), kinds[0], kinds[1])
            return facts["fingerprint"], refresh
    except BaseException:  # noqa: BLE001 - a missing file, a loader that raises or exits: the store is not reachable
        return None, refresh
    return None, refresh


def cmd_status(args) -> int:
    path = snapshot_path(args.snapshot)
    snap = Snapshot.load(path)
    if snap is None:
        print(f"none: there is no snapshot at {path}. Take one from the store (see the other subcommands) before writing queries.")
        return 3
    taken = snap.facts.get("taken", "an unrecorded date")
    if not snap.is_generated():
        print(f"hand-written: {path} has no fingerprint line, so it cannot be compared with the store automatically. "
              f"Read it and use it as the snapshot; leave it as it is. If you can reach the store, spot-check the entries you rely on.")
        if not snap.parseable():
            print("Its layout is not one `show` and `check` can read: work from the file itself and compare names by eye.")
        return 0
    now, refresh = current_fingerprint(snap)
    text = path.read_text(encoding="utf-8", errors="replace")
    if now is None:
        print(f"unreachable: {path} was taken {taken} with `{refresh}` ({snap.facts.get('source', '?')}), and that source cannot be "
              f"read here now. Use the snapshot as it is, do not rewrite it, and tell the user it could not be re-verified.")
        overview(snap, text)
        return 2
    if now == snap.facts.get("fingerprint"):
        print(f"fresh: {path} (taken {taken}, {snap.facts.get('source', '?')}) still matches. Use it; do not take it again.")
        overview(snap, text)
        return 0
    print(f"stale: the store has changed since {path} was taken {taken}. Refresh it: {refresh}")
    return 1


def cmd_show(args) -> int:
    path = snapshot_path(args.snapshot)
    snap = Snapshot.load(path)
    if snap is None:
        print(f"there is no snapshot at {path}")
        return 3
    if not snap.parseable():
        print(f"{path} is not in the layout this tool reads: open the file and read the entries there.")
        return 0
    snap.nodes(), snap.rels()   # fold hand-written notes into the entries
    everything = {}
    for title, elements in snap.elements.items():
        for name, element in elements.items():
            everything.setdefault(name.lower(), []).append((title, element))
    index = snap.sections.get("Index", [])
    extra = snap.semantics + snap.sections.get("Retired or superseded", [])
    missing = 0
    for name in args.names:
        hits = everything.get(name.lower(), [])
        if not hits:
            missing += 1
            near = sf_check.closest(name, [e.name for group in everything.values() for _t, e in group], 5)
            retired = [l for l in snap.retired() if re.search(rf"(?<![\w.]){re.escape(name)}(?!\w)", l)]
            lines = [l for l in snap.text.splitlines() if re.search(rf"(?<!\w){re.escape(name)}(?!\w)", l)]
            if lines and not retired:
                missing -= 1
                print(f"### {name}\nNo entry of its own, but the snapshot mentions it here:\n" + "\n".join(lines[:12]) + "\n")
                continue
            print(f"### {name}\nNOT IN THE SNAPSHOT." + (f" Closest names: {', '.join(near)}." if near else "")
                  + ("".join("\n" + l for l in retired)) + "\n")
            continue
        for title, element in hits:
            print(f"### {element.name}   [{title}]")
            print("\n".join(element.lines))
            touching = [l for l in index if re.search(rf"\(:{re.escape(element.name)}\)", l)]
            if touching and title not in ("Relationships", "Tables"):
                print("relationships touching it:")
                print("\n".join(touching[:40]))
            referring = [l for l in index if re.search(rf"→{re.escape(element.name)}\.", l)] if title == "Tables" else []
            if referring:
                print("tables that point at it: " + ", ".join(l[2:].split(" (")[0] for l in referring[:30]))
            notes = [l for l in extra if l.strip() and re.search(rf"(?<!\w){re.escape(element.name)}(?!\w)", l)]
            if notes:
                print("notes:")
                print("\n".join(notes))
            print()
    return 1 if missing else 0


def cmd_check(args) -> int:
    path = snapshot_path(args.snapshot)
    snap = Snapshot.load(path)
    if snap is None:
        print(f"there is no snapshot at {path}: nothing to check against")
        return 3
    return sf_check.run(args.files, snap, args.quiet)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    where = "snapshot path (default: the path docs/graph/CONTEXT.md names, else docs/graph/schema.md)"
    parser.add_argument("--snapshot", default=None, help=where)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--snapshot", default=argparse.SUPPRESS, help=where)
    sub = parser.add_subparsers(dest="command", required=True)

    def taker(name, func, help_):
        p = sub.add_parser(name, help=help_, parents=[common])
        p.add_argument("--force", action="store_true", help="replace a snapshot that this tool did not generate")
        p.add_argument("--no-samples", action="store_true", help="describe stored formats without copying values into the snapshot")
        p.set_defaults(func=func)
        return p

    p = taker("sqlite", cmd_sqlite, "snapshot a SQLite database")
    p.add_argument("database")
    p.add_argument("--max-rows", type=int, default=100000, help="rows profiled per table (default 100000)")
    p = taker("networkx", cmd_networkx, "snapshot an in-process graph")
    p.add_argument("--load", help="package.module:function that returns the graph, called with no arguments")
    p.add_argument("--file", help="graph file to read with NetworkX when the repository has no loader")
    p.add_argument("--node-kind", help="node attribute that names the kind (default: detect; 'none' for a single kind)")
    p.add_argument("--edge-kind", help="edge attribute that names the kind (default: detect; 'none' for a single kind)")
    p = taker("cypher-files", cmd_cypher_files, "snapshot from files when no database can be asked")
    p.add_argument("paths", nargs="+", help="files or directories, in the order they are applied")
    p.add_argument("--keep", action="append", metavar="NAME", help="do not treat NAME (TYPE or Label.property) as retired")
    p = taker("sql-files", cmd_sql_files, "snapshot from .sql table definitions when no database can be asked")
    p.add_argument("paths", nargs="+", help=".sql files or directories, in the order they are applied")
    p = sub.add_parser("status", help="none / fresh / stale / unreachable / hand-written", parents=[common])
    p.set_defaults(func=cmd_status)
    p = sub.add_parser("show", help="print snapshot entries by name", parents=[common])
    p.add_argument("names", nargs="+")
    p.set_defaults(func=cmd_show)
    p = sub.add_parser("check", help="compare query and code files with the snapshot", parents=[common])
    p.add_argument("files", nargs="+")
    p.add_argument("--quiet", action="store_true", help="findings only, no stored-form reminders")
    p.set_defaults(func=cmd_check)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    try:
        code = main()
        sys.stdout.flush()
    except BrokenPipeError:   # output piped into head or similar: not an error
        import os
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        code = 0
    sys.exit(code)
