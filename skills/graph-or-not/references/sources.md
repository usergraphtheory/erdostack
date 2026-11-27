# Sources for the graph-or-not references

Date checked for every row: 2026-11-23. Everything is restated in our own words; no sentence, table, example
or code is copied from any of these pages.

Status of a row:

- **read**: the page was read on that date in the erdostack fact check and the fact taken from it.
- **executed**: the behaviour was run on that date on the version named; the page is where to read more.
- **located**: the page was found by search and is the right place to verify the fact, but could not be
  opened on that date. Facts that rest only on a located page are marked "not verified" where they appear.

No graph database was installed where these notes were written, so nothing about Neo4j or LadybugDB was
executed.

## Neo4j

| Page | URL | Applies to | Licence | Status |
|---|---|---|---|---|
| Upgrade and migration guide | https://neo4j.com/docs/upgrade-migration-guide/current/ | 5.x to calendar versions | not checked | read |
| Operations manual, introduction | https://neo4j.com/docs/operations-manual/current/introduction/ | versioning scheme, server deployment | not checked | read |
| Cypher manual 25, select Cypher version | https://neo4j.com/docs/cypher-manual/25/queries/select-version | 2025.06 and later | not checked | read |
| Cypher manual 25, deprecations, additions, removals and compatibility | https://neo4j.com/docs/cypher-manual/25/deprecations-additions-removals-compatibility/ | default language by release | not checked | read |
| Release notes, Neo4j 2025.06 | https://neo4j.com/release-notes/database/neo4j-2025-06/ | 2025.06 | not checked | read |
| Cypher manual 25, understanding query plans | https://neo4j.com/docs/cypher-manual/25/planning-and-tuning/execution-plans | `EXPLAIN` and `PROFILE` | not checked | located |

## Kuzu and LadybugDB

| Page | URL | Applies to | Licence | Status |
|---|---|---|---|---|
| `ladybug` on PyPI | https://pypi.org/project/ladybug/ | 0.22.3, released 2026-11-06 | not checked | read |
| LadybugDB repository | https://github.com/LadybugDB/ladybug | package names, command-line binary, embedded use | MIT, per the erdostack roadmap; not re-checked | read |
| LadybugDB documentation, CALL clause | https://docs.ladybugdb.com/cypher/query-clauses/call | `show_tables`, `table_info`, `db_version` | not checked | read |
| LadybugDB documentation, performance debugging | https://docs.ladybugdb.com/developer-guide/performance-debugging | `EXPLAIN` and `PROFILE` | not checked | read |

Kuzu's archival month and last release (October 2025, 0.11.3) come from the same fact check. That LadybugDB
runs embedded in the application's process is stated in the erdostack roadmap and follows from how the
packages are installed; no page was read for that sentence alone.

## PostgreSQL

| Page | URL | Applies to | Licence | Status |
|---|---|---|---|---|
| WITH queries (common table expressions) | https://www.postgresql.org/docs/16/queries-with.html | recursive queries, `UNION` against `UNION ALL`, `CYCLE` | not checked | executed on 16.15; page located |
| pg_stat_statements | https://www.postgresql.org/docs/16/pgstatstatements.html | extension 1.10 on 16.15 | not checked | executed on 16.15; page located |
| Server configuration, error reporting and logging | https://www.postgresql.org/docs/16/runtime-config-logging.html | `log_min_duration_statement` | not checked | executed on 16.15; URL from prior knowledge, not returned by search |
| Using EXPLAIN | https://www.postgresql.org/docs/16/using-explain.html | `EXPLAIN (ANALYZE, BUFFERS)` | not checked | executed on 16.15; URL from prior knowledge, not returned by search |

Search returned the first two pages under other major versions (WITH queries for 18, pg_stat_statements
for 17); the version-16 addresses above were formed from those and not opened. That the `CYCLE` clause
arrived in PostgreSQL 14 is from prior knowledge of the release notes; it was run here on 16.15 only.

## SQLite

| Page | URL | Applies to | Licence | Status |
|---|---|---|---|---|
| The WITH clause | https://sqlite.org/lang_with.html | recursive common table expressions | not checked | executed on 3.53.1; page located |
| EXPLAIN QUERY PLAN | https://sqlite.org/eqp.html | plan output | not checked | executed on 3.53.1; page located |

That recursive queries date from SQLite 3.8.3 is from prior knowledge and was not verified.

## NetworkX and Python

| Page | URL | Applies to | Licence | Status |
|---|---|---|---|---|
| NetworkX reference, introduction | https://networkx.org/documentation/stable/reference/introduction.html | data structure | not checked | located |
| `tracemalloc` in the Python standard library | https://docs.python.org/3/library/tracemalloc.html | Python 3.13 | not checked | executed on 3.13.18; page located |

The NetworkX observations (reachability calls, the effect of edge attributes on memory) were executed on
NetworkX 3.7.

## Behind `heuristics.md`

The heuristics are engineering judgement written for this skill, not a summary of one source. Two ideas in
them have a published form worth reading:

| Work | URL | What it supports | Status |
|---|---|---|---|
| McSherry, Isard and Murray, "Scalability! But at what COST?", HotOS 2015 | https://www.usenix.org/conference/hotos15/workshop-program/presentation/mcsherry | compare a proposed system with the simplest thing that does the same job before adopting it | located, not re-read on the date above; no figure is taken from it |
| PostgreSQL manual, WITH queries (above) | https://www.postgresql.org/docs/16/queries-with.html | how duplicate rows and cycles arise in recursive queries | executed on 16.15 |

No threshold or benchmark figure in these references comes from a third party. The row counts in
`engines.md` are from the small test graph described there.
