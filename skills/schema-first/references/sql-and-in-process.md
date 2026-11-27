# Graphs stored in SQL tables or held in process

Last verified: 2026-11-23

## SQLite

Status: **executed** on 2026-11-23 with the SQLite library 3.53.1 through Python's `sqlite3` module. `scripts/schema.py sqlite PATH` does all of this; the list is here so the result can be checked by hand or repeated where Python is not available.

- Tables, views, indexes and triggers with their original DDL text, comments included: the `sqlite_schema` table (older name `sqlite_master`, which still works).
- Columns: `PRAGMA table_xinfo(t)` (like `table_info` but also lists generated and hidden columns).
- Declared references: `PRAGMA foreign_key_list(t)`. A legacy database often declares none; then a reference can only be inferred from the values, and the snapshot says "inferred".
- Unique and other indexes: `PRAGMA index_list(t)` then `PRAGMA index_info(index)`.
- What a column really holds: `typeof(col)` per row. SQLite column types are affinities, not guarantees, so a column declared INTEGER can hold text and the reverse.
- Open the file read-only (`file:PATH?mode=ro` as a URI) so introspection cannot change a shared database.

Dates have no storage class of their own in SQLite: they are text, or numbers. Executed on 3.53.1: `date('2026-10-05')` reads ISO text; `date(1788429600)` returns NULL while `date(1788429600, 'unixepoch')` returns the day, so integer seconds need the modifier; `date('05/10/2026')` returns NULL, and day-first text compares as text (`'05/10/2026' < '23/07/2025'` is true), so such a column has to be rebuilt into ISO order before it is compared or sorted.

## PostgreSQL

Status: **from documentation and long-standing behaviour, not executed, not re-read on 2026-11-23** (the `information_schema` chapter exists for every supported version, 14 to 18; its pages could not be opened that day).

- Columns and types: `information_schema.columns` filtered by `table_schema`.
- Keys and references: `information_schema.table_constraints` joined to `key_column_usage` (the referencing side) and `constraint_column_usage` (the referenced side).
- CHECK constraints: `information_schema.check_constraints`.
- In `psql`, `\d table` shows the same for one table, including indexes and triggers.

There is no script for PostgreSQL here because a driver is not part of the Python standard library. Run the queries through the repository's own connection (`run_queries` in `docs/graph/CONTEXT.md`), sample the values of the columns that matter as for SQLite, and write the snapshot by hand in the layout of `snapshot-format.md`. `schema.py check` can still compile `.sql` files against a hand-written `## Tables` section, but it does so with SQLite: PostgreSQL-only syntax is reported as "not checked", not as an error.

## What to look for in any SQL-stored graph

- **Which column is which end.** Names such as `src`/`dst`, `parent_id`/`child_id`, `from`/`to` do not say which way the meaning runs, and are sometimes the wrong way round. Settle it from a comment in the DDL, the code that writes the rows, or one example whose answer you know, then record it under "Verified semantics".
- **Once or twice.** An undirected link is stored either as one row (often with a rule such as smaller id first) or as two rows. Counting or joining on one column is wrong for the first; summing over all rows is wrong for the second.
- **Keys that are only unique inside something.** A composite primary key such as (tenant, number) means the number alone repeats: join on the whole key.
- **Rows that are logically gone.** Columns such as `deleted_at`, `is_deleted`, `valid_to` or `archived` mean "current" needs a filter. Look at how existing queries filter.
- **Units.** Grams against kilograms, cents against currency units, metres against kilometres. The column name, the range of values and the writer tell you; the type does not.
- **Which table is live.** Two tables with similar names and different row counts or latest dates: one may be frozen.

## NetworkX and other in-process graphs

Status: **executed** on 2026-11-23 with NetworkX 3.7. `scripts/schema.py networkx --load package.module:function` calls the repository's loader and reads the graph it returns; `--file` reads `.graphml`, `.gml`, `.gexf` or node-link `.json` directly.

- Graph class decides the semantics: `G.is_directed()` and `G.is_multigraph()`. In a multigraph, edges between the same two nodes repeat, so degree and edge counts are not counts of distinct neighbours.
- Node attributes: `G.nodes(data=True)`. Edge attributes: `G.edges(data=True)`, with `keys=True` on a multigraph.
- An attribute can live on the node or on the edge, and on only some of either. Reading a missing attribute with a default of 0 changes sums and means without failing.
- A directed graph that stores a two-way link as two edges doubles any total taken over edges; one that stores it once needs both directions followed. Compare each edge with its reverse before choosing.
- A weight name that does not exist is not an error: executed on 3.7, `shortest_path_length(G, a, c, weight='length')` on edges that only carry `distance_km` returned the hop count. Check the attribute name against the snapshot.
- The loader is the schema's author. Types come from what it does to the file (a CSV reader yields text unless the loader converts; GraphML carries declared types).
- From NetworkX 3.4 the node-link reader takes an `edges=` argument naming the key that holds the edge list; older exports use `links`. *(signature confirmed on 3.7 by execution; the 3.4 boundary is from the release notes and was not re-read.)*
