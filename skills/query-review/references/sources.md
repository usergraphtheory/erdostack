# Sources for the query-review references

Date checked for every row: 2026-11-23. Everything is restated in our own words; no text, table, example or code is copied from these pages.

Status values:

- **read**: the page was read on that date in the erdostack fact check and the fact was taken from it.
- **located**: the page was found by search on that date and is the right place to verify the fact, but it could not be opened. Facts that rest only on a located page are tagged **[unverified]** where they appear.
- **executed**: nothing was read; the behaviour was observed by running it, on the version named.

Licences were not checked for any page.

## Neo4j (nothing executed)

| Page | URL | Applies to | Status |
|---|---|---|---|
| Upgrade and migration guide | https://neo4j.com/docs/upgrade-migration-guide/current/ | 5.x to calendar versions | read |
| Operations manual, introduction | https://neo4j.com/docs/operations-manual/current/introduction/ | versioning scheme | read |
| Cypher manual 25, select Cypher version | https://neo4j.com/docs/cypher-manual/25/queries/select-version | 2025.06 and later | read |
| Cypher manual 25, deprecations, additions, removals and compatibility | https://neo4j.com/docs/cypher-manual/25/deprecations-additions-removals-compatibility/ | default language by release; when each clause arrived | read for the default language only |
| Cypher manual 5, CALL subqueries in transactions | https://neo4j.com/docs/cypher-manual/5/subqueries/subqueries-in-transactions | batching forms; implicit transactions only | read (orchestrator fact check) |
| Neo4j status codes, GQL error 25N17 | https://neo4j.com/docs/status-codes/current/errors/gql-errors/25N17 | `IN TRANSACTIONS` inside an explicit transaction | read (orchestrator fact check) |
| Cypher manual 5, CALL subquery and clause composition | https://neo4j.com/docs/cypher-manual/5/subqueries/call-subquery | `CALL (x) { }` from 5.23, importing `WITH` deprecated | read (orchestrator fact check) |

## LadybugDB and Kuzu (nothing executed)

| Page | URL | Applies to | Status |
|---|---|---|---|
| `ladybug` on PyPI | https://pypi.org/project/ladybug/ | 0.22.3, released 2026-11-06 | read |
| LadybugDB repository | https://github.com/LadybugDB/ladybug | package names, command-line binary | read |
| LadybugDB documentation, CALL clause | https://docs.ladybugdb.com/cypher/query-clauses/call | built-in calls | read |
| LadybugDB documentation, performance debugging | https://docs.ladybugdb.com/developer-guide/performance-debugging | `EXPLAIN`, `PROFILE` | read |

## SQLite and PostgreSQL

| Page | URL | Applies to | Status |
|---|---|---|---|
| SQLite library 3.53.1 through Python `sqlite3` | none | every **[run]** line under SQLite in `sql.md` | executed |
| PostgreSQL 16.15 through `psql`, local throwaway cluster | none | every **[run]** line under PostgreSQL in `sql.md` | executed |
| SQLite, EXPLAIN QUERY PLAN | https://sqlite.org/eqp.html | plan output | located |

## Not from a source

The procedure itself (state the rule from the repo, count independently, prove on a copy, hand production changes back, leave correct code alone) was written from the failures in the erdostack evals for this skill, not taken from a book or another skill.
