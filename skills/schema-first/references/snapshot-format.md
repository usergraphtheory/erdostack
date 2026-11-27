# The schema snapshot file

Default path `docs/graph/schema.md`, or the path `docs/graph/CONTEXT.md` gives as `schema_snapshot`. One layout for every store, so that people, later sessions and `scripts/schema.py` (`show`, `check`) can all read it. Write it by hand in this layout when no `schema.py` subcommand fits the store.

```markdown
# Graph schema snapshot

## Facts

taken: 2026-11-23
store: <engine and where: "Neo4j 5.26, dev container", "sqlite data/app.db", "in-process graph built by pkg.load:load()">
source: <live store | files (which) | a person's description (who)>
method: <the exact commands or files it was read from, so anyone can repeat it>
coverage: <complete, or what is missing and why>
fingerprint: none

## Index

- Person: email, fullName, startedOn
- (:Person)-[:MEMBER_OF]->(:Team): role, since

## Nodes

### Person
- `email` STRING · unique
- `startedOn` DATE
- `status` STRING · values: 'active' (212), 'left' (31)

## Relationships

### MEMBER_OF
- pattern: (:Person)-[:MEMBER_OF]->(:Team)
- `role` STRING
- `since` DATE

## Retired or superseded

- HAS_MEMBER: replaced by MEMBER_OF in migrations/0012 (direction reversed). Do not use.

## Verified semantics

- MEMBER_OF points from the person to the team (checked: 3 sampled rows, 2026-11-23).
- Invoice.amount is in cents (checked: the writer in billing/money.py, and 1999 for a 19.99 invoice).
```

## Rules the scripts rely on

- **Facts** are `key: value` lines. `taken` (date), `store`, `source`, `method` and `coverage` are always present. A snapshot written by `schema.py` also has `refresh` (the command that takes it again) and `fingerprint` (a hash of the store's structure, which `schema.py status` compares with the store). By hand, write `fingerprint: none`: a snapshot without a real fingerprint is never overwritten by the scripts.
- **Index** has one line per node kind or table and one per relationship pattern. It is what a query writer reads first, so keep names and arrows exact.
- **Entries** are `### Name` under `## Nodes` (graph stores) or `## Tables` (SQL), and `### TYPE` under `## Relationships`. Spell names exactly as the store does, including case and plural.
- **A property or column** is a line starting ``- `name` TYPE``, then details separated by ` · `. Leave the type out when it is not known; do not guess one.
- **A relationship pattern** is a line `- pattern: (:Start)-[:TYPE]->(:End)`, arrow as stored. One line per pair of endpoint kinds. Use `-[:TYPE]-` only for a store that has no direction (an undirected in-process graph).
- **Where a property lives** is shown by where its line is: under the node kind or under the relationship type. A property that both carry appears in both places.
- **Stored form** goes on the property line when a query could get it wrong: `values: 'Y' (40), 'N' (2)` for a complete list of values, the date layout for dates kept as text, `epoch seconds` or `epoch milliseconds` for integer times, the unit when the name does not say it, `null in 31 of 140 rows`, `on 36 of 60 only` for an attribute some nodes lack.
- **Pairs.** For two columns or two endpoints of the same kind, say how a link is stored: once per pair (and in which order), twice (both directions), or directed.
- **Retired or superseded** lists names that old files, old queries or people still use but the store no longer has.
- **Verified semantics** is the only hand-edited section of a generated snapshot and survives a refresh. One line per fact, with how it was checked. A line that starts with `Kind.property` also tells `schema.py check` that this property exists (for one the generated part could not see).

## For SQL stores

Tables go under `## Tables`, one `### table` each, columns as property lines with the declared type. Show a reference on the column that holds it: `-> other_table.key (foreign key)` when declared, `(inferred ...)` when it was worked out from the values. Keep the `CREATE TABLE` text in a fenced `sql` block under the table when it carries comments or CHECK constraints, since those often state what a column means. Views go under `## Views` with their SQL in a fenced block.

## What a snapshot is not

It is not the schema someone described, a README diagram or a model file copied out. Those are leads. An entry belongs in the snapshot once it has been read from the store, or from the files that define and load the store, and `source` says which.
