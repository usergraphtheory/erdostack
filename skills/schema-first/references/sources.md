# Sources

Everything in this skill is written in our own words. No sentences, tables, examples or code were copied from the sources below. "Opened" means the page's text was read on the date given; "located" means a search on that date returned the page but its text could not be opened from the authoring environment, so what the skill says on that topic rests on long-standing behaviour and is marked as such where it appears.

| Topic | Source | Version | Licence | Date | How used |
|---|---|---|---|---|---|
| Neo4j server versioning | Neo4j Upgrade and Migration Guide, https://neo4j.com/docs/upgrade-migration-guide/current/ ; Operations Manual introduction, https://neo4j.com/docs/operations-manual/current/introduction/ | 5.26 LTS, 2025.01 onwards | not recorded | 2026-11-23 | opened by the maintainers; restated in `neo4j.md` |
| Cypher 5 and Cypher 25, default language | Cypher Manual, https://neo4j.com/docs/cypher-manual/25/queries/select-version ; https://neo4j.com/docs/cypher-manual/25/deprecations-additions-removals-compatibility/ ; release notes https://neo4j.com/release-notes/database/neo4j-2025-06/ | 2025.06 onwards | not recorded | 2026-11-23 | opened by the maintainers; restated in `neo4j.md` |
| Neo4j schema procedures (`db.schema.*`, `dbms.components`) | Operations Manual, built-in procedures, https://neo4j.com/docs/operations-manual/current/procedures | current | not checked | 2026-11-23 | located, not opened |
| Neo4j `SHOW CONSTRAINTS`, `SHOW INDEXES` | Cypher Manual, https://neo4j.com/docs/cypher-manual/current/schema/constraints/list-constraints/ ; https://neo4j.com/docs/cypher-manual/current/indexes/performance-indexes/list-indexes/ | current | not checked | 2026-11-23 | located, not opened |
| LadybugDB packages and status of Kuzu | https://pypi.org/project/ladybug/ ; https://github.com/LadybugDB/ladybug | ladybug 0.22.3 (2026-11-06); Kuzu 0.11.3 archived | MIT (repository) | 2026-11-23 | opened by the maintainers; restated in `ladybugdb.md` |
| LadybugDB `CALL` introspection functions | https://docs.ladybugdb.com/cypher/query-clauses/call | 0.22.3 | not recorded | 2026-11-23 | opened by the maintainers for `show_tables`, `table_info`, `db_version`; `show_connection` not confirmed |
| LadybugDB table DDL | https://docs.ladybugdb.com/cypher/data-definition/create-table | 0.22.3 | not checked | 2026-11-23 | located, not opened |
| SQLite schema table and PRAGMAs | https://www.sqlite.org/pragma.html | library 3.53.1 | public domain | 2026-11-23 | located, not opened; every statement in `sql-and-in-process.md` marked "executed" was run here |
| PostgreSQL information schema | https://www.postgresql.org/docs/17/information-schema.html | 14 to 18 supported | PostgreSQL licence | 2026-11-23 | located, not opened |
| NetworkX graph classes and readers | https://networkx.org/documentation/latest/reference/classes/index.html | 3.7 | BSD-3-Clause | 2026-11-23 | located, not opened; behaviour marked "executed" was run here on 3.7 |
| Agent Skills layout | https://agentskills.io/specification | as linked from this repository's CONTRIBUTING.md | not checked | 2026-11-23 | followed through the repository validator; page not opened |

Nothing here is a benchmark or a measured threshold.
