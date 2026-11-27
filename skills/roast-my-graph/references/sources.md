# Sources for roast-my-graph

Date checked for every row: 2026-11-23. Nothing in this skill is copied from these pages; facts are restated in our own words. Licences are given only where the page states one.

Status words match `engines.md`: **docs** (official page checked on that date, nothing executed), **run** (executed locally), **located** (the official page was found by title in a web search, its content was not read; the fact is marked unverified in `engines.md`).

| Fact in the skill | Source | Version | Status |
|---|---|---|---|
| Neo4j server versioning (5.x, 5.26 LTS, calendar versions from 2025.01) | https://neo4j.com/docs/upgrade-migration-guide/current/ , https://neo4j.com/docs/operations-manual/current/introduction/ | Neo4j 5.26 to 2026.x | docs (checked by the erdostack maintainer's fact pass) |
| Cypher 5 and Cypher 25, per-query prefix, per-database default language | https://neo4j.com/docs/cypher-manual/25/queries/select-version , https://neo4j.com/docs/cypher-manual/25/deprecations-additions-removals-compatibility/ , https://neo4j.com/release-notes/database/neo4j-2025-06/ | Neo4j 2025.06 and later | docs (same fact pass) |
| `SHOW INDEXES` | https://neo4j.com/docs/cypher-manual/25/indexes/performance-indexes/list-indexes/ | Cypher 25 | located |
| `EXPLAIN` and `PROFILE` | https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/execution-plans/ | current | located |
| Lookup without an index examines every node with the label | https://neo4j.com/docs/cypher-manual/current/indexes/performance-indexes/using-indexes/ | current | located |
| Relationship model, pattern direction, unbounded variable-length patterns, disconnected patterns, `MERGE` matching | Cypher manual, pattern and clause pages (not looked up individually) | Neo4j 5.x | not read; written from long-stable behaviour |
| LadybugDB lineage and package names | https://pypi.org/project/ladybug/ , https://github.com/LadybugDB/ladybug | `ladybug` 0.22.3 (2026-11-06) | docs (same fact pass) |
| LadybugDB `CALL show_tables()`, `table_info`, `db_version` | https://docs.ladybugdb.com/cypher/query-clauses/call | 0.22.x | docs (same fact pass) |
| LadybugDB `EXPLAIN` and `PROFILE` | https://docs.ladybugdb.com/developer-guide/performance-debugging | 0.22.x | docs (same fact pass) |
| LadybugDB node tables need a primary key, which is indexed; relationship tables have none; default multiplicity | https://docs.ladybugdb.com/cypher/data-definition/create-table/ | 0.22.x | docs, read by the erdostack eval authors (recorded in the repository's `evals/roast-my-graph/SOURCES.md`); located but not re-read for this skill |
| SQLite plan output, pragmas, foreign keys and indexes, composite key order, recursive queries on a loop, read-only open | executed; see also https://www.sqlite.org/eqp.html (located) | SQLite 3.53.1, Python 3.13 `sqlite3` | run |
| PostgreSQL `EXPLAIN`, foreign keys and indexes, `CYCLE` clause | https://www.postgresql.org/docs/current/ (pages not looked up individually) | 14 and later for `CYCLE` | not read; written from long-stable behaviour |
| NetworkX `descendants`, `ancestors`, `shortest_path` and its `weight` argument, graph-kind checks | executed | NetworkX 3.7 | run |

The catalogue in `smells.md` and the severity ladder in `SKILL.md` are our own, written from the failures seen in the skill's eval baseline. They do not come from a book, vendor guide or other skill repository.
