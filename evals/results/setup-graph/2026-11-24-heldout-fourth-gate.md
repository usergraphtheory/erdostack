## setup-graph / heldout / 2026-11-24

Models: haiku, sonnet. Skill version: fbcd8fc16fef.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 135/160 (84%, 95% CI 78% to 89%) | 0/160 (0%, 95% CI 0% to 2%) |
| skill | 155/160 (97%, 95% CI 93% to 99%) | 158/160 (99%, 95% CI 96% to 100%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 65/80 (81%, 95% CI 71% to 88%) |
| baseline/sonnet | 70/80 (88%, 95% CI 78% to 93%) |
| skill/haiku | 77/80 (96%, 95% CI 90% to 99%) |
| skill/sonnet | 78/80 (98%, 95% CI 91% to 99%) |

Paired by case, all models: skill better on 20, baseline better on 3, tied on 57; sign test p = 0.0005.
Paired by case, haiku: 13 / 1 / 66 ties; p = 0.0018.
Paired by case, sonnet: 10 / 2 / 68 ties; p = 0.0386.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 19788.5 tokens / 20.0 s; skill 24591.5 tokens / 30.1 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| dotnet-aspire-apphost-heat-network-memgraph-postgres-redis | FAIL:engine-version-pinned,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass | pass |
| dotnet-ferry-transfers-testcontainers-and-runsettings | pass | pass | pass | pass |
| dotnet-graft-lineage-gitlab-ci-service-templates | pass | pass | pass | pass |
| dotnet-illgraph-devcontainer-container-env-and-makefile-default | pass | pass | pass | pass |
| dotnet-lighthouse-sightlines-workflow-service-and-migrations | FAIL:query-language-fits-engine,language-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass | pass |
| dotnet-neo4j-makefile-compose-and-override-file | pass | FAIL:query-language-version-stated,driver-from-lockfile,evidence-names-repo-files,open-questions-section | pass | pass |
| go-baggage-transfers-neo4j-kustomize-overlay-and-components | pass | pass | pass | pass |
| go-board-interlocks-neo4j-compose-environment-and-query-docs | pass | pass | pass | pass |
| go-cave-survey-passages-sqlite-schema-file-and-loaders | pass | pass | pass | pass |
| go-dock-flows-nightly-calls-reusable-workflow | pass | FAIL:engine-version-pinned,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass |
| go-etl-lineage-sqlite-vendored-pure-go-driver | pass | pass | pass | pass |
| go-heat-network-sqlite-driver-replaced-by-local-fork | pass | pass | pass | pass |
| go-mesh-radio-links-in-postgres-recursive-query-files | pass | pass | pass | pass |
| go-neo4j-service-env-file-and-cypher-5-style-guide | FAIL:query-language-fits-engine,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass | pass |
| go-seed-bank-pedigree-workspace-on-embedded-kuzu | FAIL:engine-version-pinned,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass | pass |
| go-trail-junctions-mattn-sqlite-cascade-note | pass | pass | pass | pass |
| go-wind-farm-cables-compose-include-with-env-file | pass | pass | pass | pass |
| helm-chart-config-values-and-query-style-doc | FAIL:query-language-fits-engine,language-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | FAIL:query-language-fits-engine,language-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass |
| helm-skaffold-release-values-pantry-substitutes | pass | pass | pass | pass |
| jvm-gradle-catalog-neo4j-harness-dev-graph | pass | pass | pass | pass |
| jvm-gradle-docker-compose-plugin-lists-two-compose-files | pass | pass | pass | pass |
| jvm-gradle-kuzu-java-binding-in-graph-subproject | pass | pass | pass | pass |
| jvm-gradle-orchard-pollination-compose-env-file-and-cypher-docs | FAIL:query-language-fits-engine,language-conflict-surfaced-under-open-questions,facts-seven-plain-keys,evidence-names-repo-files,open-questions-section | pass | pass | pass |
| jvm-gradle-pilgrim-ways-jenkinsfile-postgres-and-cycle-queries | pass | pass | pass | pass |
| jvm-gradle-seed-bank-lineage-compose-neo4j-and-postgres | FAIL:query-language-fits-engine,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass | pass |
| jvm-gradle-spring-boot-docker-compose-local-profile | pass | pass | pass | pass |
| jvm-gradle-test-fixtures-neo4j-container-and-query-style-guide | FAIL:query-language-fits-engine,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | FAIL:engine-version-pinned | pass |
| jvm-kotlin-sqlite-config-object-and-data-guide | pass | pass | FAIL:version-conflict-surfaced,version-conflict-surfaced-under-open-questions | pass |
| jvm-maven-failsafe-image-property-and-next-line-profile | pass | pass | pass | pass |
| jvm-maven-jgrapht-planner-module-and-kotlin-notebook | pass | pass | pass | pass |
| jvm-maven-sqlite-jdbc-corridor-queries-and-docs | pass | pass | pass | pass |
| jvm-maven-testcontainers-classpath-properties-image-substitutor | pass | pass | pass | pass |
| jvm-sbt-sqlite-jdbc-pin-and-label-coverage-report | pass | pass | pass | pass |
| node-campus-footpaths-sqlite-wasm-pnpm | pass | pass | pass | FAIL:engine-version-pinned |
| node-compose-override-file-beside-explicit-f-scripts | pass | pass | pass | pass |
| node-docker-bake-file-and-neo4j-dockerfile-arg | FAIL:query-language-fits-engine,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass | pass |
| node-duckdb-feeder-routes-package-lock-and-readme | pass | FAIL:engine-version-pinned,driver-from-lockfile,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass |
| node-env-file-flag-and-memgraph-container-helper | pass | pass | pass | pass |
| node-food-bank-routes-neo4j-compose-file-flag-and-override-file | pass | pass | pass | pass |
| node-gitlab-ci-nightly-report-memgraph-service | FAIL:engine-version-pinned,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass | pass |
| node-interloan-routes-yarn-workspaces-kuzu | pass | pass | pass | pass |
| node-mesh-relays-sqlite-cli-image-and-join-report | pass | pass | pass | pass |
| node-pnpm-workspace-fitment-package-and-shop-api | pass | pass | pass | pass |
| node-seedline-bun-lock-and-ladybug-core-range | FAIL:engine-version-pinned,driver-from-lockfile,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass | pass |
| node-talk-copresenters-typescript-ladybug-npm | pass | FAIL:engine-version-pinned,driver-from-lockfile,version-conflict-surfaced-under-open-questions,facts-seven-plain-keys,evidence-names-repo-files,open-questions-section | pass | pass |
| py-airline-hubs-pdm-lock-and-notebook-networkx | pass | pass | pass | pass |
| py-apiary-hive-splits-sqlite-and-records-guide | pass | pass | pass | pass |
| py-arangodb-makefile-adds-notebooks-compose-file | pass | pass | pass | pass |
| py-bus-depot-graph-invoke-support-compose-and-cypher-25-files | FAIL:query-language-fits-engine,query-language-version-stated,version-conflict-surfaced-under-open-questions,facts-seven-plain-keys,evidence-names-repo-files,open-questions-section | FAIL:query-language-fits-engine,query-language-version-stated,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass |
| py-choir-repertoire-devcontainer-and-rehearsal-compose-file | pass | pass | pass | pass |
| py-citation-graph-compose-override-for-benchmark-host | pass | pass | pass | pass |
| py-davis-rustworkx-pixi-lock-notebook-output | FAIL:engine-version-is-package-version,version-conflict-surfaced,version-conflict-surfaced-under-open-questions,facts-seven-plain-keys,evidence-names-repo-files,open-questions-section | pass | FAIL:run-queries-real | FAIL:run-queries-real,version-conflict-surfaced,version-conflict-surfaced-under-open-questions |
| py-dojo-split-igraph-over-exported-graphml | pass | pass | pass | pass |
| py-gallery-loans-compose-env-sets-cypher-25 | pass | pass | pass | pass |
| py-interlibrary-loans-igraph-uv-project-and-notebook | pass | pass | pass | pass |
| py-lesmis-walks-igraph-conda-lock-pip-section | pass | pass | pass | pass |
| py-memgraph-compose-yaml-beside-docker-compose-yml | pass | pass | pass | pass |
| py-package-mirror-dependency-graph-sqlite-yank-check | pass | pass | pass | pass |
| py-pantry-substitutions-ladybug-uv-docker | pass | pass | pass | pass |
| py-poetry-wildlife-corridor-compose-two-neo4j-services | pass | pass | pass | pass |
| py-seed-bank-lineage-kuzu-pip-compile | pass | pass | pass | pass |
| py-seed-library-sqlite-pandas-loader-and-data-model-doc | pass | pass | pass | pass |
| py-services-repo-part-supersession-sqlite-and-design-doc | pass | pass | pass | pass |
| py-ski-lift-graph-memgraph-kustomize-laptop-overlay-on-shared | pass | pass | pass | pass |
| py-starter-sharing-pipfile-lock-embedded-ladybug | FAIL:engine-version-pinned,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass | pass |
| py-tide-gauge-graph-testcontainers-compose-pair | pass | pass | pass | pass |
| py-uv-workspace-lineage-service-beside-postgres-and-redis | pass | pass | pass | pass |
| py-volunteer-shift-graph-nox-session-env | pass | pass | pass | pass |
| rust-batmap-xtask-graph-up-and-cargo-config-env | pass | pass | pass | pass |
| rust-garden-irrigation-rusqlite-import-and-image-sqlite | pass | pass | pass | pass |
| rust-manuscript-stemma-workspace-kuzu-crate | pass | FAIL:driver-from-lockfile,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass |
| rust-orienteering-memgraph-compose-and-override-file | pass | pass | pass | pass |
| rust-repeater-links-devcontainer-dotenv-and-cypher-25-queries | FAIL:query-language-fits-engine,query-language-version-stated,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | FAIL:query-language-fits-engine,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass |
| rust-ringwalk-petgraph-with-cargo-patch-section | pass | FAIL:query-language-fits-engine,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass |
| rust-toolshare-devcontainer-run-services-two-memgraph-services | pass | pass | pass | pass |
| rust-trailmap-workspace-rusqlite-and-devcontainer-libsqlite | pass | FAIL:driver-from-lockfile,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass |
| rust-workspace-trail-network-api-snapshot-and-reach-crates | pass | pass | pass | pass |
| ts-neo4j-compose-anchor-default-and-service-image | pass | pass | pass | pass |
| ts-npm-pantry-services-bake-file-and-neo4j-dockerfile | pass | pass | pass | pass |
| ts-route-planner-bake-file-sets-neo4j-base | pass | pass | pass | pass |
