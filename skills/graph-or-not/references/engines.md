# Engine notes for graph-or-not

Last verified: 2026-11-23

What each engine means for the decision, and how to measure on the ones a repo usually already has. Every
fact carries the version it was checked on and one of three statuses:

- **executed**: run on 2026-11-23 on the version named.
- **documentation, not executed**: taken from the official page on 2026-11-23 in the erdostack fact check;
  no graph database was installed where these notes were written.
- **not verified**: from prior knowledge; the official page was located but could not be opened that day.
  Confirm it against the engine in front of you before relying on it.

Engines age faster than these notes. If the repo runs a different version, check there and say what you
checked. Pages are listed in `sources.md`.

## Neo4j

All **documentation, not executed**.

- It is a server: a separate stateful process to deploy, back up, upgrade and be paged for. That cost belongs
  in "Options considered" whenever `graph-database` means Neo4j.
- Version numbers changed scheme. Releases run as semantic versions through 5.x, where 5.26 (December 2024)
  is the last 5.x line and a long-term-support release, and as calendar versions (`YYYY.MM.PATCH`) from
  2025.01 on. A proposal's version claim is checked against the image tag or lockfile the repo pins, not
  against memory.
- The query language is versioned separately from Neo4j 2025.06: Cypher 5 receives only fixes, new features
  land in Cypher 25, and which one a database speaks by default depends on when and how it was created. A
  proposal that rests on a particular query feature has to say which Cypher it assumes; you cannot settle
  that from the server version alone.
- Query plans, for a repo that already runs Neo4j and asks whether to keep it: prefixing a query with
  `EXPLAIN` shows the plan without running it, `PROFILE` runs it and reports rows and database hits per
  operator. **Not verified** on 2026-11-23 (the Cypher manual's execution-plans page was located, not read).

## LadybugDB (formerly Kuzu)

All **documentation, not executed**.

- It is embedded: installed as a library and run inside the application's process, with no server. That
  removes the on-call cost of a server, not the second copy of the data, its file format or the load step,
  so choosing it is still `graph-database`.
- Kuzu was archived in October 2025 (last release 0.11.3) and continues as LadybugDB. A proposal that names
  Kuzu or installs a `kuzu` package is proposing an archived project: say so in the write-up.
- Current package names, as of `ladybug` 0.22.3 (released 2026-11-06): Python `ladybug` (early releases
  were `real_ladybug`), Node `@ladybugdb/core` (early: `lbug`), Rust crate `lbug`, command-line binary `lbug`.
- For a repo that already uses it: `CALL show_tables() RETURN *;`, `CALL table_info('<Table>') RETURN *;`
  and `CALL db_version() RETURN *;` describe what is loaded; `EXPLAIN` before a query shows the plan and
  `PROFILE` runs it and reports time per operator.

## PostgreSQL

**Executed** on PostgreSQL 16.15 (a throwaway local server) unless marked. Other major versions: check.

Measuring safely:

- `BEGIN READ ONLY;` or `SET default_transaction_read_only = on;` makes the session refuse writes and DDL
  (an `INSERT` and a `CREATE TABLE` were both rejected).
- `SET statement_timeout = '<duration>';` cancels a statement that runs longer, with the error "canceling
  statement due to statement timeout". Set one before timing anything on a shared server.
- `EXPLAIN (ANALYZE, BUFFERS) <query>` runs the query and prints, per plan node, actual rows, loops and
  buffer hits. A recursive query appears as a "Recursive Union" node whose actual row count is the number of
  rows the walk produced; compare it with the number of distinct nodes it reached.

Sizes:

- `pg_relation_size`, `pg_indexes_size` and `pg_total_relation_size` give bytes for a table, its indexes and
  both. `pg_class.reltuples` is the planner's row estimate, refreshed by `ANALYZE`; `count(*)` is exact and
  scans.

Call counts and failure rates:

- `log_min_duration_statement` is off (`-1`) by default. When set, only statements that ran at least that
  long are logged (with 100 ms set, a 300 ms statement was logged and a fast one was not). Such a log is a
  list of slow calls with no total.
- `pg_stat_statements` (extension version 1.10 on 16.15) keeps, per statement, `calls`, `total_exec_time`,
  `mean_exec_time` and `rows`. It only works when the library is in `shared_preload_libraries`, which needs a
  server restart; without it, reading the view fails with an error that says so. When a repo says it is not
  enabled, per-statement totals do not exist and have to be asked for from the application side.

Recursive queries, on a test graph of four layers where every node links to every node of the next layer
(10 nodes reachable from the start):

- `UNION ALL` in the recursive part returned 40 rows, one per route; `UNION` over the node column alone
  returned 10, one per node. Carrying a path array through a `UNION` brought it back to 40, because rows that
  differ in the path are not duplicates. Carrying a depth column returned 14 once a shortcut edge made some
  nodes reachable at two depths.
- `UNION` over the node column alone also terminated on a cyclic graph. The `CYCLE <column> SET <flag>
  USING <path>` clause marks the rows that close a loop (documented from PostgreSQL 14; run here on 16.15).

## SQLite

**Executed** on SQLite 3.53.1 through Python 3.13's `sqlite3` module unless marked.

- A database file in the repo is a copy you can question directly. Open it read-only with the URI
  `file:PATH?mode=ro`; a write then fails with "attempt to write a readonly database".
- Recursive queries behave as above: on the same test graph `UNION ALL` returned 40 rows and `UNION` 10;
  `UNION` terminated on a cycle, `UNION ALL` on a cycle ran until its `LIMIT`. Recursive common table
  expressions date from SQLite 3.8.3 (**not verified** on 2026-11-23).
- `EXPLAIN QUERY PLAN <query>` does not run the query. It showed `SCAN e` for a lookup with no usable index
  and `SEARCH e USING INDEX e_src (src=?)` once one existed; inside a recursive query the same line appears
  under `RECURSIVE STEP`. A `SCAN` of the edge table there means every step of the walk reads the whole table.
- It reports no timings. Time the query with a clock around the call, and count the rows it returns.

## NetworkX and other in-process libraries

**Executed** on NetworkX 3.7 with Python 3.13 unless marked.

- NetworkX keeps nodes, edges and attributes in nested Python dictionaries (**not verified** against the
  reference introduction on 2026-11-23; consistent with what was run). Memory per edge is therefore many
  times the size of the row it came from, and depends on the attributes kept: in one synthetic run of
  200,000 edges, keeping three attributes per edge raised traced memory to about one and a half times that
  of bare edges. That ratio is an observation, not a constant; measure with your own edges.
- To measure: load a sample of the real edge list, with the attributes the design would keep, between
  `tracemalloc.start()` and `tracemalloc.get_traced_memory()` (standard library), or read the process's
  resident memory after loading. Scale by the full edge count and call the result an extrapolation.
- `networkx.descendants` and `networkx.ancestors` answer reachability; `pagerank` and
  `betweenness_centrality` exist for whole-graph work.
- It is not in the standard library, and this skill does not install anything. Where it is absent, a
  dictionary of adjacency lists and a breadth-first loop in plain Python measures a walk just as well.
- igraph, rustworkx, graph-tool and GPU libraries were not checked for these notes. Their memory per edge
  differs widely from NetworkX's; measure before sizing a plan on any of them.
