---
name: schema-first
description: "Use whenever you are about to write, change or fix a query or code that reads or writes a graph in a repository: Cypher, GQL, Gremlin, SPARQL, SQL over node, edge or hierarchy tables, NetworkX-style code. Reads the real schema from the database or the files that define it, keeps it as docs/graph/schema.md, and checks every label, table, relationship direction, property and stored value format against it. Not for explaining concepts, choosing an engine, performance tuning, reviewing a schema's design, GraphQL APIs or plain reporting SQL with no graph in it."
---

# schema-first

Model-invoked. Fixes schema hallucination: labels, tables, properties and relationship directions that were assumed instead of read, and values assumed to be stored the obvious way. Writes the schema snapshot `docs/graph/schema.md`, which later sessions, reviewers, CI and the other erdostack skills read in place of the database.

## When to use

Before writing, changing or fixing anything that reads or writes a graph in a repository: a Cypher, GQL, Gremlin or SPARQL query, SQL over node, edge or hierarchy tables, code on an in-process graph library. Also when asked to check existing queries against the schema.

Not when the task is to explain a concept, choose an engine, tune a slow query, review a model's design, or write SQL that involves no graph or hierarchy. Not for designing a schema that does not exist yet: there is nothing to read.

## Why a snapshot

You will usually read a schema that is in front of you. Three things still go wrong, and the steps are aimed at them:

- What you learned dies with the session. The next session, a colleague or CI may have no database, and guesses.
- With many queries in one request, the convention of one corner of the schema (a name, an arrow, a unit) leaks into the next.
- The names are right and the values are not what was assumed: a flag kept as a letter, a date kept as text, an amount in minor units, a two-way link stored once.

So the schema is read from the store once, kept in the repository, and every name is checked against it.

`S` below means `python3 SKILL_DIR/scripts/schema.py`, where SKILL_DIR is the folder this file is in. Run it from the repository root. It uses only the Python standard library, makes no network calls, opens stores read-only and writes nothing except the snapshot. If it cannot run where you are, do the same steps by hand with the engine's own introspection (see References).

## Steps

1. **See where you stand.** Read `docs/graph/CONTEXT.md` if it exists: engine, how to run queries, `access`, and `schema_snapshot` (the snapshot's path; otherwise it is `docs/graph/schema.md`). If a snapshot exists, run `S status`. It prints the snapshot's index, or all of it when it is small, and one of:
   - `fresh`: use the snapshot. Do not take it again; it is taken once and refreshed when stale, not rebuilt per query.
   - `stale`: the store changed. Run the refresh command it prints.
   - `unreachable`: the store or its data is not here. Use the snapshot as it is, do not edit it, and tell the user at the end that names come from the snapshot of that date and could not be re-verified.
   - `hand-written`: read the file and use it; leave it as it is. If you can reach the store and it contradicts an entry, correct that entry only and say so.

   If there is no snapshot, go to step 2.

2. **Take the snapshot from the store: all of it, once.** Not only the part this request touches, because the next request cannot be predicted and may arrive where the store is absent. Use the strongest source you can actually read now:
   - A SQLite file: `S sqlite PATH.db`
   - An in-process graph: `S networkx --load package.module:function`, naming the repository's own loader (`--file PATH` for a bare graph file)
   - A database you can query (a server, an embedded graph database): run the introspection listed for that engine in `references/` and write the file by hand in the layout of `references/snapshot-format.md`
   - No store, but files that define and load it (DDL, constraints, migrations, import scripts, code that writes): `S cypher-files PATH ...` for Cypher, `S sql-files PATH ...` for SQL table definitions, paths in the order they are applied. Model classes or other languages: read them and write the file by hand. Pass what defines or writes the graph. Add a folder of existing queries only when nothing else shows the relationships, and never the files you are about to write: they would become their own evidence. A snapshot from files knows names, not how values are stored: say so.
   - Only prose (a README, a diagram, the request itself): that is a lead, not a source. See "no schema source" below.

   When sources disagree, the one closer to the data and later in time wins: the live store, then migrations in applied order (a later one can rename, reverse or drop what an earlier one made), then code that writes, then existing queries, then model files and READMEs. The command prints what it wrote, so there is no need to open the file afterwards.

3. **Settle what only the data can say.** The command lists what it could not decide. For those, and for anything this request filters, sorts, sums or joins on, find out which end of a pair is which, the unit, what a code means, whether a missing value means zero: look at a few rows or at the code that writes them. Add one line each under `## Verified semantics` in the snapshot, with how you checked, and anything else you had to look at the data to learn while doing the task: the next session cannot look. That section survives a refresh. If nothing needed settling, add nothing.

4. **Write from the snapshot, not from the request's words.** If the snapshot was not printed whole, run `S show NAME ...` once for every table, label and relationship type you intend to use. It prints the exact spelling, where each property lives (node or relationship), the direction and endpoint kinds, and how values are stored. The user's vocabulary describes what they want; it is not a list of names. A value you filter on must be one the snapshot shows (`values:` lists are complete, `e.g.` are samples). If it is not shown, look in the store; if you cannot, say which value you assumed.

5. **Check every file before you call it done.** `S check FILE ...`, all files in one call (`.cypher`, `.sql`, and `.py` for in-process graphs). It reports names that are not in the snapshot, reversed arrows, endpoint kinds a relationship does not join, properties placed on the wrong element, literals of the wrong type or that a column never holds, and it recalls the stored form of what each file uses. Fix the file for each finding, or show that the snapshot is out of date and refresh it. Never edit the snapshot to silence a finding. Lines marked `?` are what it could not check: compare those by eye. With many files, check each against the entries for its own part of the schema: areas of a grown schema use different conventions for the same thing.

   If the store is reachable, also run each query and judge the result, not only that it ran. An empty result, or a number of the wrong size, usually means a wrong encoding, unit or direction.

6. **Tell the user**, in a line or two: where the snapshot is and whether it was taken, refreshed or used unverified (with its date), and anything from the cases below.

## The quiet cases

- **No schema source** (no store, no defining files, no snapshot; or a snapshot that does not cover what is needed while the store is out of reach). Do not write a snapshot: a file of guesses is read as fact later. If you can ask and wait, ask for the schema or for a way to reach the store. Otherwise write what was asked with conventional names, and mark every name as an assumption, both in a comment at the top of the file and in your reply, with what to run to confirm them. Do not call anything checked or validated that you could not check.
- **The request needs something the store does not have.** Say so and name what is missing. Then either write nothing, or write the nearest thing that uses only real names and label it, in the file and in the reply, as a stand-in for what was asked. Do not invent the missing piece and do not substitute quietly.
- **The user's description contradicts the store.** Follow the store, and say so: one sentence in the reply (what they said, what is there) and a comment in the file. A query that was silently corrected reads as a request that was misread.
- **The snapshot is fresh and the request is small.** Use it and change nothing in it.
- **Confidential data.** The snapshot copies a few sample values into a file that will be committed. Where rows are personal or confidential, add `--no-samples`.
- **Read-only.** Introspection only reads. Do not run a migration, loader or write to find out what the schema is.

## Output

`docs/graph/schema.md` (or the path `CONTEXT.md` names): Facts (date taken, store, source, method, coverage, fingerprint), an Index, one entry per node kind or table and per relationship type (properties with types and stored form; patterns with direction and endpoint kinds), names that are retired, and the hand-checked semantics. `query-review` and the other erdostack skills read it.

## References

Load only the one you need.

- `references/snapshot-format.md`: the layout, when writing or correcting a snapshot by hand
- `references/neo4j.md`, `references/ladybugdb.md`, `references/sql-and-in-process.md`: introspection for that engine, each fact with its version, date and whether it was executed
- `references/sources.md`: where the engine facts come from
