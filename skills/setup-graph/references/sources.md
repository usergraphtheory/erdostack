# Sources for the setup-graph references

Date checked for every row: 2026-11-23. Nothing was executed: no graph database is installed where these
notes were written. Everything is restated in our own words; no text, table or example is copied.

"Read" means the page was read on that date in the erdostack fact check and the fact taken from it. "Located"
means the page was found by search and is the right place to verify the fact, but was not read on that date;
facts that rest only on a located page are marked "not verified" where they appear.

## Neo4j

| Page | URL | Applies to | Licence | Status |
|---|---|---|---|---|
| Upgrade and migration guide | https://neo4j.com/docs/upgrade-migration-guide/current/ | 5.x to calendar versions | not checked | read |
| Operations manual, introduction | https://neo4j.com/docs/operations-manual/current/introduction/ | versioning scheme | not checked | read |
| Cypher manual 25, select Cypher version | https://neo4j.com/docs/cypher-manual/25/queries/select-version | 2025.06 and later | not checked | read |
| Cypher manual 25, deprecations, additions, removals and compatibility | https://neo4j.com/docs/cypher-manual/25/deprecations-additions-removals-compatibility/ | default language by release | not checked | read |
| Release notes, Neo4j 2025.06 | https://neo4j.com/release-notes/database/neo4j-2025-06/ | 2025.06 | not checked | read |
| Operations manual, Docker, modify the default configuration | https://neo4j.com/docs/operations-manual/current/docker/configuration | settings as container environment variables | not checked | located |
| Upgrade and migration guide, driver compatibility | https://neo4j.com/docs/upgrade-migration-guide/current/migration/drivers/compatibility | driver and server pairs | not checked | located |

## Kuzu and LadybugDB

| Page | URL | Applies to | Licence | Status |
|---|---|---|---|---|
| `ladybug` on PyPI | https://pypi.org/project/ladybug/ | 0.22.3, released 2026-11-06 | not checked | read |
| LadybugDB repository | https://github.com/LadybugDB/ladybug | package names, command-line binary | MIT, per the erdostack roadmap; not re-checked | read |
| LadybugDB documentation, CALL clause | https://docs.ladybugdb.com/cypher/query-clauses/call | `db_version` and the other built-in calls | not checked | read |
| Kuzu repository | https://github.com/kuzudb/kuzu | archived October 2025, last release 0.11.3 | not checked | located (the archival month and last release come from the same fact check) |

## Tooling behind `override-layers.md` and `sql-and-in-process.md`

Written from prior knowledge of Docker Compose, Dockerfile build arguments, Helm, Kustomize, the common
lockfile formats and SQLite. No official page was read for them on the date above. Verify against the
tools' own documentation before relying on a rule where two layers disagree; the skill tells the agent to
list both values in that case.
