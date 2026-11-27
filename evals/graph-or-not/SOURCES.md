# Sources for the graph-or-not eval

Checked on 2026-11-23. The gold answers in this eval rest on workload reasoning (data size, traversal
depth, concurrency, freshness, what is already operated), not on engine trivia. No case's accepted
decision depends on a fact marked "not verified" below. Fetching pages was not available in the
authoring sessions, so anything not executed locally is marked by how far it was checked.

Revised on 2026-11-23 when 4 dev and 8 held-out cases were added. One correction to the first version:
it said there is no PostgreSQL on this machine. There is: PostgreSQL 16.15 binaries are installed under
`/usr/lib/postgresql/16/bin` and `psql` is on the PATH. No server runs by default, but one can be
started in a temporary directory as the `postgres` user, which is how the PostgreSQL in the new fixtures
was checked, and which a baseline agent also discovered for itself. There is no `sqlite3` command-line
tool; SQLite is used through Python's `sqlite3` module (SQLite 3.53.1).

Held-out cases are described here without their names or numbers, because the skill author may read
this file and must not learn the held-out set from it. Each held-out case that relies on a checked fact
repeats the details under `sources:` in its own `case.yaml`.

## Verified by running it on this machine

| Fact | Used in | How |
|---|---|---|
| SQLite answers transitive-closure questions with `WITH RECURSIVE` (SQLite 3.53.1) | dev/yank-impact-cli and one held-out case (the agent can run it; the selfcheck "good" answers quote timings from a run here) | executed against the databases built by each case's `setup.py` |
| The generated registry has 8,400 packages, 53,849 dependency rows, and 8,332 transitive dependents of `corelib`; the per-node loop took about 11 s here against 0.06 s for one recursive query (no index leads with `dependency_id`) | dev/yank-impact-cli | counted and timed locally; timings are machine-dependent and no assertion requires a particular timing |
| Row counts, longest chain and the planted example in a generated SQLite database; node and link counts in a generated JSON content file | two held-out cases | counted locally from the output of each case's `setup.py` |
| NetworkX 3.7 provides `pagerank`, `betweenness_centrality`, `shortest_path`, `community.louvain_communities` and `les_miserables_graph()` (77 nodes, 254 edges) | dev/nightly-page-ranking (selfcheck text) and two held-out cases (one fixture script was run) | imported and called locally |
| NetworkX 3.7 `pagerank` takes a `personalization` argument and `weakly_connected_components` exists; SciPy 1.18.1 has `scipy.sparse.csgraph.connected_components` | one held-out case added 2026-11-23 (what its model spec asks for) | imported and inspected locally |
| The PostgreSQL in the four dev cases added 2026-11-23 runs on PostgreSQL 16.15: `asset-tags-search-timeouts` (migrations apply in order; `expanded_tag_ids` returns one row per route, 17 rows for 8 terms on a small hierarchy with two broader terms per term; the search statement runs), `company-links-loader-half-built` (schema and the links query), `lineage-in-memory-adr` (schema and the downstream query), `ownership-slow-log-vendor-quote` (schema and the resolve query, with a circular holding) | those four cases | executed on a throwaway server; the plans, timings and row counts quoted in the fixtures are invented and no assertion depends on PostgreSQL behaviour |
| `log_min_duration_statement`, `statement_timeout` and `log_parameter_max_length` are PostgreSQL settings; `pg_stat_statements` 1.10 reports queryid, query, calls, total, mean, standard deviation and maximum execution time, and rows; a statement stopped by the timeout reports "canceling statement due to statement timeout" | dev/ownership-slow-log-vendor-quote, dev/asset-tags-search-timeouts and one held-out case | `SHOW`, `CREATE EXTENSION` and a timed-out statement on the local PostgreSQL 16.15 |
| The schemas and SQL statements in six held-out fixtures added 2026-11-23 run on PostgreSQL 16.15, and two PostgreSQL behaviours that two of those cases rely on are as the cases assume | six held-out cases; details under `sources:` in each `case.yaml` | executed on the throwaway server |
| Row counts, group sizes, the planted examples and query results in two generated SQLite databases | two held-out cases added 2026-11-23 | counted locally from the output of each case's `setup.py`; timings are machine-dependent and not asserted |

## Taken from the orchestrator's engine notes (official pages, checked 2026-11-23, not re-checked here)

| Fact | Used in | Source |
|---|---|---|
| Kuzu was archived in October 2025; LadybugDB is its maintained fork and runs embedded, in process | dev/yank-impact-cli (the proposal a contributor wrote; the case does not grade it) | https://github.com/LadybugDB/ladybug , https://pypi.org/project/ladybug/ |
| Neo4j uses calendar versions (YYYY.MM) from 2025.01 | one selfcheck "bad" variant uses the image tag `neo4j:2026.10`; the agent never sees it and the tag's existence was not checked | https://neo4j.com/docs/operations-manual/current/introduction/ |
| Neo4j 5.26 is the last 5.x release line and an LTS | dev/company-links-loader-half-built (the image tag `neo4j:5.26` in an existing compose file; that the tag exists on a registry was not checked) and one held-out fixture's README | https://neo4j.com/docs/upgrade-migration-guide/current/ |

## Seen in search results only (the page exists; its content was not read)

| Fact as used | Used in | Page |
|---|---|---|
| SQL Server supports recursive common table expressions and an `OPTION (MAXRECURSION n)` query hint | one held-out case (existing T-SQL in the fixture; not executed, no SQL Server here) | https://learn.microsoft.com/en-us/sql/t-sql/queries/with-common-table-expression-transact-sql , https://learn.microsoft.com/en-us/sql/t-sql/queries/recursive-common-table-expression-transact-sql |
| PostgreSQL's `pg_stat_statements` reports per-statement call counts and execution times | several fixtures present exports "from pg_stat_statements" with their own column headings; no fixture claims a real column name | https://www.postgresql.org/docs/16/pgstatstatements.html |
| Neo4j's Graph Data Science library includes centrality and community-detection algorithms | dev/nightly-page-ranking (the proposal says "graph data science plugin") and one held-out fixture's plan | https://neo4j.com/docs/graph-data-science/current/algorithms/centrality/ |
| MySQL 8.0 limits recursive common table expressions with the system variable `cte_max_recursion_depth` | one held-out case added 2026-11-23 (an error message in its fixture; the default value and the message text are written from general knowledge, and no assertion depends on their exact wording) | https://dev.mysql.com/worklog/task/?id=10972 , https://dev.mysql.com/blog-archive/a-new-simple-way-to-figure-out-why-your-recursive-cte-is-running-away/ |

## Not verified (written from general knowledge; realism only)

- PostgreSQL recursive CTE syntax in the fixtures of the first 18 cases (`WITH RECURSIVE`, array-based
  cycle guard). Not executed by the first author, who believed there was no PostgreSQL here, and not
  re-run in the revision. The queries are evidence for the agent to read, and no assertion executes or
  parses them. (The PostgreSQL in the 12 cases added on 2026-11-23 was executed; see above.)
- Log line formats, `EXPLAIN ANALYZE` output, MySQL slow-log entries and error-tracker text in the new
  fixtures. Written by hand in the shape the real tools produce; their numbers are invented.
- Cypher in one new held-out fixture (variable-length patterns and `shortestPath`, Cypher 5 syntax).
  Not executed: no graph database is installed.
- MySQL stored-procedure syntax, PHP, Kotlin, TypeScript, Go, Terraform and Kubernetes YAML in the new
  fixtures. None is executed.
- Memory-per-edge figures for NetworkX, SciPy and igraph quoted inside fixtures (a team's own bench
  notes or an ADR). They are invented, of a realistic order, and are the fixture's evidence: the gold
  answers follow from the fixture's figures, not from what the libraries really use.
- A statement about how a radio protocol's devices connect, in one new held-out fixture's hardware
  note. General knowledge, not re-checked.
- Container image tags in fixtures' compose files (other than as noted above).
- T-SQL, Django, Prisma, Rails, Spring and Go snippets in fixtures. None is executed; they are there to
  be read.
- Statements that fictional people make about products in tickets, plans and proposals (what a product
  needs to install, what it has built in, how fast it is). They are part of the framing, not claims of
  the eval.

## Data

All fixture data is invented or generated by seeded scripts (a `setup.py` in five cases; one-off
scripts for the CSV, JSON and log exports in several others, written so that their rows add up to the
totals the cases quote). The only public dataset is the Les Miserables co-appearance
graph that ships with NetworkX. No private, employer or personal data.
