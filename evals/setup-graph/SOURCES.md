# Sources for the setup-graph eval

Checked: 2026-11-23.

## How these were checked, and what that is worth

Page fetching was not available in the session that wrote this eval, only web search. So "seen in search" below
means: on 2026-11-23 a web search returned the official page at this URL and the fact is visible in the page title
or in the URL itself (for example a release-notes URL that contains the version number). The page body was not
read. Anything that could not be confirmed that way is marked **unverified**.

The rule the cases follow: **no gold answer depends on an unverified fact.** A gold version number is always the
one written in the fixture's own lockfile, compose file, Dockerfile or pom; the outside source only tells us the
number is a real release, so the fixture looks like a repo someone could have. The places where a gold answer
does depend on an outside fact are marked "gold depends: yes". Three of them (the Docker Compose rules in the
last table) rest on long-standing documented behaviour whose official page was found but whose body could not be
read here; read those pages before relying on the three cases that use them.

Engine facts go stale. Re-check this file before trusting a result recorded more than a few months after the date
above, and when a fixture is edited.

## Neo4j server

| Fact | Used in | Source | Status | Gold depends |
|---|---|---|---|---|
| Since 2025.01 the server uses calendar versions (YYYY.MM.patch); the 5.x line ended with 5.26, which is the long-term-support release | every Neo4j case | https://neo4j.com/blog/developer/neo4j-graph-database-versioning/ , https://neo4j.com/release-notes/database/neo4j-2025-01-0 , https://neo4j.com/blog/developer/neo4j-v5-lts-evolution/ | seen in search | no |
| The query language versions are named "Cypher 5" and "Cypher 25" | the first 27 cases grade `query_language` as naming Cypher only; four later cases grade the version, see "Cypher versions on Neo4j" below | https://neo4j.com/docs/cypher-manual/25/queries/select-version/ , https://neo4j.com/blog/developer/cypher-versioning/ | seen in search | no |
| 5.26.14 exists (released 20 October 2025) | dev/readme-version-older-than-compose-pin | https://neo4j.com/release-notes/database/neo4j-5-26-14/ | seen in search | no |
| 5.26.23 exists (19 March 2026) | heldout/monorepo-two-graph-stores | https://neo4j.com/release-notes/database/neo4j-5-26-23/ | seen in search | no |
| 5.26.24 exists (31 March 2026) | heldout/passwords-in-env-files-stay-out-of-docs | https://neo4j.com/release-notes/database/neo4j-5-26-24/ | seen in search | no |
| 5.26.29 exists (4 August 2026) | heldout/agents-file-allows-writes-to-dev-graph | https://neo4j.com/release-notes/database/neo4j-5-26-29/ | seen in search | no |
| 2025.10.1 exists | dev/readme-points-at-deleted-query-script | https://neo4j.com/release-notes/database/page/5 (title names 2025.10.1 as the then-current release) | seen in search | no |
| 2026.02.2 exists (6 March 2026) | dev/user-says-local-instance-is-writable | https://neo4j.com/release-notes/database/neo4j-2026-02-2/ | seen in search | no |
| 2026.05.0 exists | heldout/dockerfile-pin-newer-than-architecture-doc | https://neo4j.com/release-notes/ (archive pages titled "The most current release of Neo4j is 2026.05.0") | seen in search | no |
| 2026.08.1 exists | heldout/stale-context-file-after-upgrades | https://neo4j.com/release-notes/database/neo4j-2026-08-1/ | seen in search | no |
| 2026.09.0 exists | heldout/compose-override-file-swaps-the-image; elsewhere only as a wrong value in selfcheck/bad-* variants | https://neo4j.com/release-notes/database/page/2/ | seen in search | no |
| 2025.11.2 exists | heldout/compose-build-arg-overrides-dockerfile-default | https://neo4j.com/release-notes/page/10/ (titled "The most current release of Neo4j is 2025.11.2") | seen in search | no |
| 5.26.25 (21 April 2026) and 5.26.26 (12 May 2026) exist | heldout/compose-override-file-swaps-the-image, heldout/context-file-names-a-renamed-make-target | https://neo4j.com/release-notes/database/neo4j-5-26-25/ , https://neo4j.com/release-notes/database/neo4j-5-26-26/ | seen in search | no |
| A 4.4 line exists (4.4.0, December 2021; 4.4.48, February 2026) | the stale README value in dev/readme-version-older-than-compose-pin | https://neo4j.com/release-notes/database/neo4j-4-4-0/ , https://neo4j.com/release-notes/database/neo4j-4-4-48/ | seen in search | no |
| 5.11.0 and 5.18 were releases | stale values in heldout/stale-context-file-after-upgrades and heldout/dockerfile-pin-newer-than-architecture-doc | none found | **unverified** | no |
| Docker image tags look like `neo4j:<version>`, `neo4j:<version>-community`, `neo4j:<version>-enterprise` | every compose file and Dockerfile | https://hub.docker.com/_/neo4j (page returned by search; tag list not readable) | **unverified** | no (the grader reads the version out of the fixture's tag) |
| Environment variable names (`NEO4J_AUTH`, `NEO4J_ACCEPT_LICENSE_AGREEMENT`), `cypher-shell` flags (`-u`, `-p`, `-f`, `--format`, `--access-mode`) | fixture realism | not searched | **unverified** | no |
| AuraDB connection URIs look like `neo4j+s://<id>.databases.neo4j.io` | heldout/hosted-instance-nothing-pins-the-server | not searched | **unverified** | no |

## Neo4j drivers

| Fact | Used in | Source | Status | Gold depends |
|---|---|---|---|---|
| The Python driver's PyPI package is `neo4j`; 5.28.1 is a release | D1, H6 | https://pypi.python.org/pypi/neo4j (result titled "neo4j 5.28.1") | seen in search | no |
| `neo4j` 6.1.0 is a release; the current docs are for 6.3 | H5 | https://neo4j.com/docs/api/python-driver/current/index.html (titled "Neo4j Python Driver 6.3"); a PyPI mirror listing titled "neo4j 6.1.0" (https://simple-repository.app.cern.ch/project/neo4j) | seen in search (6.1.0 only on a mirror) | no |
| `neo4j-driver` on PyPI is a different, deprecated package name | the grader does not accept `neo4j-driver` where the lockfile says `neo4j` (true whatever its status: it is not the name in the lockfile) | https://socket.dev/pypi/package/neo4j-driver (title shows a warning) | partly seen | no |
| The JavaScript driver's npm package is `neo4j-driver`; 5.27.0, 6.0.0 and 6.0.1 are releases | D6, H1, H9, H13 | https://unpkg.com/neo4j-driver@5.27.0/README.md , https://newreleases.io/project/npm/neo4j-driver/release/6.0.0 , https://socket.dev/npm/package/neo4j-driver/overview/6.0.1 | seen in search (third-party indexes of npm) | no |
| `neo4j-driver` 5.12.0 was a release | stale value in H9 | none found | **unverified** | no |
| The Java driver is `org.neo4j.driver:neo4j-java-driver`; 5.28.1 is a release | H4, H12 | https://central.sonatype.com/artifact/org.neo4j.driver/neo4j-java-driver ; https://repository.jboss.org/nexus/repository/m2-proxy/org/neo4j/driver/neo4j-java-driver/5.28.1/neo4j-java-driver-5.28.1.pom | seen in search | no |
| `neo4j-java-driver` 6.1.0 is a release | D5 | https://repository.jboss.org/nexus/repository/m2-release-proxy/org/neo4j/driver/neo4j-java-driver-parent/6.1.0/neo4j-java-driver-parent-6.1.0.pom (the parent POM, not the driver artifact itself) | partly seen | no |
| `executableQuery(...)`, `execute_query(...)`, `executeQuery(...)` APIs as used in fixture code | fixture realism | not searched | **unverified** | no |
| A `neo4j-java-driver-bom` artifact exists for importing in `dependencyManagement` | heldout/driver-version-from-bom-in-parent-pom | https://mvnrepository.com/artifact/org.neo4j.driver/neo4j-java-driver-bom | seen in search | no (the version is the fixture's property; that a BOM import manages the versions of the artifacts it lists is standard Maven behaviour, not searched) |
| The Go driver's module path is `github.com/neo4j/neo4j-go-driver/v5` | heldout/compose-build-arg-overrides-dockerfile-default | https://pkg.go.dev/github.com/neo4j/neo4j-go-driver/v5/ | seen in search | no |
| `neo4j-go-driver` v5.28.1 is a release; Go API names used in the fixture | same | none found | **unverified** | no |

## Kuzu and LadybugDB

| Fact | Used in | Source | Status | Gold depends |
|---|---|---|---|---|
| Kuzu's upstream repository was archived in October 2025 and 0.11.3 is its last release | the judge items in dev/kuzu-requirements-pin-archived-upstream and heldout/kuzu-npm-pin-in-package-lock | https://github.com/kuzudb/kuzu ; https://www.theregister.com/2025/10/14/kuzudb_abandoned/ (URL and date); https://oneuptime.com/blog/post/2026-08-12-kuzu-archived-pin-0-11-3-fork-or-migrate/view (title: "Kuzu Was Archived: Should You Pin 0.11.3, Fork It, or Migrate?"; third party) | seen in search (the archive date from The Register's URL, 0.11.3 from a third-party title); also stated in this repo's README | **yes** |
| The Python package is `kuzu` on PyPI | D2, H4 | https://pypi.org/project/kuzu/ | seen in search | no |
| The `kuzu` npm package has a 0.11.3 release | H2 | none found (assumed: Kuzu released all bindings under one version) | **unverified** | no (gold is the fixture's lockfile) |
| LadybugDB is the maintained fork of Kuzu | case descriptions; calibration wording | https://dbdb.io/db/ladybugdb ; https://communityone.io/ar/servers/787399249741479977/neo4j/news/ladybugdb-launch-community-fork-kuzudb-2025-10-16/ (third party, titled "LadybugDB Launch: Community Fork of KuzuDB") | seen in search | no (the judge question accepts any wording, with or without the fork's name) |
| The PyPI package `ladybug` is LadybugDB, at 0.22.3 (released 2026-11-06, described as "formerly known as Kuzu") | heldout/ladybug-version-only-in-uv-lock | https://pypi.org/project/ladybug/ | checked on the page by the maintainer on 2026-11-23 (not re-read here) | no (gold is the fixture's uv.lock) |
| Early releases were published as `real_ladybug` (Python) and `lbug` (Node); the current names are `ladybug` and `@ladybugdb/core` | nothing graded. `real_ladybug` appears once, as a wrong value in a selfcheck/bad-* variant | checked on pypi.org by the maintainer on 2026-11-23; https://www.piwheels.org/project/real-ladybug/ , https://socket.dev/npm/package/lbug | given by the maintainer; existence seen in search | no |
| The npm package of LadybugDB is `@ladybugdb/core` | heldout/named-service-uses-a-different-engine (the fixture's code imports it and its lockfile pins it) | same maintainer check; https://socket.dev/npm/package/@ladybugdb/core | given by the maintainer; existence seen in search | no (gold is the fixture's lockfile) |
| `@ladybugdb/core` has a 0.22.3 release on npm, and its JavaScript API (`Database`, `Connection`, `query`, `getAll`) | same case | none found (assumed: one version across bindings, API carried over from Kuzu) | **unverified** | no |
| Python import name and API of the `ladybug` package (`import ladybug as lb`, `Database`, `Connection`, `execute`, `get_next`) | fixture code in H3 | https://docs.ladybugdb.com/client-apis/python/ (page returned, body not read) | **unverified** | no |
| Kuzu's Python and Node APIs and its DDL (`CREATE NODE TABLE`, `CREATE REL TABLE`, `COPY ... FROM`) as used in fixture code | D2, H2, H4 | not searched | **unverified** | no |

A case that grades "the `real_ladybug` name is flagged as renamed" was planned and dropped in the first version,
because the rename could not be verified from search. The maintainer has since confirmed the names on pypi.org.
No case grades that flag yet; see Open questions in EVALS.md.

## Memgraph

| Fact | Used in | Source | Status | Gold depends |
|---|---|---|---|---|
| Memgraph has a 3.5 release line | heldout/memgraph-image-behind-neo4j-driver | https://memgraph.com/blog/memgraph-3-5-release-announcement | seen in search | no |
| The exact image tag `memgraph/memgraph:3.5.0` exists | same | https://hub.docker.com/r/memgraph/memgraph (not readable) | **unverified** | no (gold is the tag in the fixture) |
| Memgraph speaks Bolt and is commonly used through the `neo4j` drivers; `mgconsole` is its console client; `*BFS` with a filter lambda is Memgraph syntax | fixture realism and the case description | https://memgraph.com/docs/getting-started/install-memgraph/docker (page returned, body not read) | **unverified** | no |

## PostgreSQL, SQLite, NetworkX

| Fact | Used in | Source | Status | Gold depends |
|---|---|---|---|---|
| PostgreSQL 17.7 and 18.1 were released together (November 2025) | D4, H10, H11; 18.1 as a wrong value in a selfcheck variant | https://www.postgresql.org/about/news/postgresql-181-177-1611-1515-1420-and-1323-released-3171/ , https://www.postgresql.org/docs/release/17.7/ | seen in search | no |
| `psycopg` 3.2.9 is a release | D4, H10 | not found | **unverified** | no |
| `better-sqlite3` 12.8.0 is a release | D3 | https://newreleases.io/project/npm/better-sqlite3/release/12.8.0 | seen in search (third-party index) | no |
| SQLite runs the recursive CTEs in the fixture | D3 | executed here against the database that setup.py builds (Python 3.13 `sqlite3`) | executed | no |
| NetworkX 3.5 is a release | H8 | https://networkx.org/documentation/stable/release/release_3.5.html | seen in search | no |
| `les_miserables_graph`, `write_graphml_xml`, `read_graphml`, `betweenness_centrality` exist | H8 fixture and setup.py | executed here with NetworkX 3.7 | executed | no |

## Docker Compose behaviour (three golds depend on these)

| Fact | Used in | Source | Status | Gold depends |
|---|---|---|---|---|
| `docker compose up` with no `-f` merges `compose.override.yaml` over `compose.yaml`, and a scalar such as `image` in the override replaces the base value | heldout/compose-override-file-swaps-the-image | https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/ ("Merge Compose files"), https://docs.docker.com/reference/compose-file/merge/ | official page found by search; body not read | **yes** |
| `${VAR:-default}` in a compose file uses the default only when the variable is unset, and `docker compose --env-file <file>` supplies variables for that interpolation | dev/env-file-overrides-compose-default-tag | https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/ ("Set, use, and manage variables in a Compose file with interpolation"), https://docs.docker.com/reference/compose-file/interpolation/ | official page found by search; body not read | **yes** |
| A build `args:` entry in a compose file replaces the default of the same `ARG` in the Dockerfile, including an `ARG` declared before `FROM` | heldout/compose-build-arg-overrides-dockerfile-default | not searched separately (Dockerfile reference and Compose build specification) | **unverified by search**; long-standing documented behaviour | **yes** |

Two of those three fixtures also say the same thing in their own prose (a comment at the top of
compose.override.yaml; a paragraph in docs/operations.md), so their gold does not rest on the rule alone. The
build-arg fixture does not. Read the pages above before using these cases for a ship decision.

## Added with the eleven cases of the second round (2026-11-23)

Checked the same way as above: web search only, page bodies not read in this session. "Orchestrator" means the
fact was read on the official page by the orchestrator on 2026-11-23 and handed to this session in
`work/ENGINE_FACTS.md`; it was not re-read here. Short names: D10 dev/default-language-set-in-neo4j-conf, D11
dev/early-package-name-real-ladybug-in-poetry-lock, D12 dev/helm-dev-values-replace-chart-image-tag, H19
heldout/lbug-crate-version-only-in-cargo-lock, H20 heldout/testcontainers-image-string-in-test-code, H21
heldout/setup-script-sets-default-language-cypher-5, H22 heldout/cypher-version-not-settled-by-repo, H23
heldout/early-npm-name-lbug-in-pnpm-lock, H24 heldout/old-driver-line-against-new-server, H25
heldout/five-services-user-names-the-neo4j-one, H26 heldout/large-repo-stale-copies-of-every-fact.

### Cypher versions on Neo4j (four golds depend on these)

| Fact | Used in | Source | Status | Gold depends |
|---|---|---|---|---|
| Since Neo4j 2025.06 the query language is versioned apart from the server: Cypher 5 (frozen) and Cypher 25. A database has a default language; a query can be prefixed `CYPHER 5` or `CYPHER 25` | claim 13; D10, H21, H22, H26 | https://neo4j.com/docs/cypher-manual/25/queries/select-version , https://neo4j.com/release-notes/database/neo4j-2025-06/ | orchestrator; the select-version page was also returned by search here ("Select Cypher version") | **yes** |
| The instance-wide setting is `db.query.default_language`, with the value `CYPHER_25` for Cypher 25 | D10 (the fixture's neo4j.conf line) | same pages; https://neo4j.com/docs/cypher-manual/25/deprecations-additions-removals-compatibility/ | orchestrator | **yes** (the gold reads Cypher 25 off that line; the line itself also spells the version) |
| A database's default language can be set with `CREATE DATABASE` / `ALTER DATABASE ... DEFAULT LANGUAGE` | H21 | same; https://neo4j.com/docs/operations-manual/current/database-administration/standard-databases/alter-databases/ ("Alter databases", returned by search) | orchestrator for the fact; the exact statement in the fixture, `ALTER DATABASE waterworks SET DEFAULT LANGUAGE CYPHER 5`, was written from memory of that page and **not verified** | **yes** for "the statement fixes Cypher 5"; no for its exact spelling |
| Which language a database defaults to depends on when and how it was created (kept at Cypher 5 for databases created on or migrated to 2025.06+; set to Cypher 25 explicitly from 2026.02; new self-managed deployments ship `CYPHER_25` from 2026.06), so it has to be checked, not assumed | H22 (gold: no version may be put forward), H21 and D10 (gold: the server version does not decide) | compatibility page above | orchestrator | **yes** |
| What happens to the default language when a dump is loaded over an existing database with `neo4j-admin database load` | H22 fixture story | not searched | **unverified**; the gold does not need it, because the fixture's runbook says nobody has checked | no |
| A 5.26 server cannot run Cypher 25 (it exists from 2025.06) | H26 (`Cypher 25` fails there) | follows from the first row and from 5.26 being the last 5.x release (December 2024) | orchestrator, by inference | **yes** |
| `ALTER DATABASE`, roles and `GRANT` need Enterprise Edition; `NEO4J_ACCEPT_LICENSE_AGREEMENT` and the `-enterprise` image tag | H21 fixture realism | not searched | **unverified** | no |
| neo4j.conf setting names other than the default language (`server.memory.*`, `db.tx_log.rotation.retention_policy`, `db.logs.query.*`, `dbms.security.auth_minimum_password_length`, `server.directories.import`); mounting a directory at `/conf` makes the official image read `neo4j.conf` from it | D10 fixture realism | not searched | **unverified** | no (but D10's story rests on the mount: read https://neo4j.com/docs/operations-manual/current/docker/ before relying on it) |
| `neo4j-admin database load` / `dump` flags | H22, H26 scripts | not searched | **unverified** | no |
| Neo4j 2025.06.0, 5.20, 5.22.0 were releases | prose and decoys in H24, H26 | 2025.06 from the release-notes URL above; 5.20 and 5.22.0 none found | 2025.06 seen; the others **unverified** | no (decoys) |

Every server tag that is a gold in the eleven cases (2025.10.1, 2025.11.2, 2026.02.2, 2026.05.0, 2026.08.1,
2026.09.0, 5.26.26) is already in the first table of this file.

### LadybugDB under its other names

| Fact | Used in | Source | Status | Gold depends |
|---|---|---|---|---|
| Early releases of the Python package were published as `real_ladybug`; the current name is `ladybug` | D11 (the successor that must be named) | https://pypi.org/project/ladybug/ ; https://www.piwheels.org/project/real-ladybug/ | orchestrator; both pages returned by search here | **yes** (also stated in the fixture's CONTRIBUTING.md) |
| The Node package is `@ladybugdb/core`; `lbug` on npm was the early name | H23 | https://github.com/LadybugDB/ladybug ; https://socket.dev/npm/package/@ladybugdb/core , https://socket.dev/npm/package/lbug | orchestrator; both index pages returned by search here | **yes** (also stated in the fixture's decision record) |
| `real-ladybug` had a 0.12.0 release on PyPI | D11 lockfile | none found. 0.12.0 is a LadybugDB release number (https://docs.rs/crate/lbug/0.12.0) | **unverified** | no (gold is the fixture's poetry.lock) |
| `lbug` on npm has a 0.14.0 release | H23 lockfile | https://socket.dev/npm/package/lbug/overview/0.14.0 | seen in search (third-party index) | no |
| The Rust crate is `lbug`; 0.21.2 and 0.22.0 are releases | H19 | https://docs.rs/crate/lbug/0.21.2 , https://docs.rs/crate/lbug/0.22.0 | seen in search (docs.rs URLs) | no (gold is the fixture's Cargo.lock) |
| The crate builds the engine into the binary (a `cmake`/`cxx` build), so the crate version is the engine version | H19 gold, claim 2 | https://docs.rs/crate/lbug/0.16.1/source/lbug-src/README.md (the crate ships the engine source: a `lbug-src` directory is in the URL) | seen in search, by the URL only | **yes** (the fixture's README also says the database is embedded) |
| Rust API (`Database::new`, `SystemConfig`, `Connection::new`, `query`), Node API of `lbug` (`Database`, `Connection`, `prepare`, `execute`, `getAll`), Python API of `real_ladybug` | fixture code in H19, H23, D11 | not searched; carried over from Kuzu's bindings | **unverified** | no |

### Drivers, Helm, Testcontainers

| Fact | Used in | Source | Status | Gold depends |
|---|---|---|---|---|
| The Python driver had a 4.4.11 release | H24 | https://pypi.org/project/neo4j-driver/4.4.11/ (the same release under the package's older alias); https://github.com/neo4j/neo4j-python-driver/wiki/4.4-Changelog | seen in search; under the name `neo4j` it is assumed | no (gold is requirements.txt) |
| `session.read_transaction` is the 4.x spelling (later `execute_read`); the 4.x driver depends on pytz | H24 fixture realism | not searched | **unverified** | no |
| Whether a 4.4 driver is supported against, or works with, a 2025.11 server | H24 | not searched | **unverified**, and deliberately not needed: the judge question asks whether the gap is flagged for checking or upgrading, not what breaks | no |
| `helm upgrade --install <release> <chart> -f <file>`: values in a file passed with `-f` take precedence over the chart's own values.yaml | D12 | https://helm.sh/docs/chart_template_guide/values_files ("Values Files") | official page found by search; body not read | **yes** |
| Testcontainers for Java has a Neo4j module (`org.testcontainers:neo4j`, class `Neo4jContainer`) that starts the image it is given | H20 | https://java.testcontainers.org/modules/databases/neo4j ("Neo4j Module"); https://javadoc.io/static/org.testcontainers/neo4j/1.20.0/org/testcontainers/containers/Neo4jContainer.html | official page found by search; body not read | **yes** (the image string in the fixture is what runs) |
| `withAdminPassword`, `getBoltUrl`, `DockerImageName.parse`, Testcontainers 1.21.3, the surefire/failsafe set-up of the fixture | H20 fixture realism | javadoc page above for the class; the rest not searched | **unverified** | no |
| Gradle dependency locking (`gradle.lockfile`, `lockAllConfigurations()`) resolves a dynamic version such as `6.+` to the locked one | H25 | not searched (same mechanism as heldout/agents-file-allows-writes-to-dev-graph) | **unverified by search**; documented Gradle behaviour | **yes** |
| Memgraph `*WSHORTEST` / `*BFS` syntax, `pymgclient` (`import mgclient`) and its 1.4.0 release, `mgconsole` | H25, the store that is NOT the answer | not searched | **unverified** | no |

## Not checked at all

Versions of packages that only pad the lockfiles (click, rich, pytest, typer, tsx, typescript, rxjs, fastapi,
strawberry-graphql, sqlalchemy, uvicorn, netty, junit, Spring Boot, pandas, numpy, the Rust crates around `lbug`,
cmake-js, node-addon-api, prettier, fastify, javalin, go-redis, pydantic, starlette and their transitive
dependencies), the image tag `redis:7.4` (`registry.example.org/curio/api:0.11` in one demo compose file is a made-up path), the exact layout of each lockfile format, and all hashes (which are made up and are not real
package hashes). None of them is graded.
