## setup-graph / heldout / 2026-11-24

Models: haiku, sonnet. Skill version: 359ccadb2cf0.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 113/120 (94%, 95% CI 88% to 97%) | 0/120 (0%, 95% CI 0% to 3%) |
| skill | 116/120 (97%, 95% CI 92% to 99%) | 120/120 (100%, 95% CI 97% to 100%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 55/60 (92%, 95% CI 82% to 96%) |
| baseline/sonnet | 58/60 (97%, 95% CI 89% to 99%) |
| skill/haiku | 58/60 (97%, 95% CI 89% to 99%) |
| skill/sonnet | 58/60 (97%, 95% CI 89% to 99%) |

Paired by case, all models: skill better on 5, baseline better on 2, tied on 53; sign test p = 0.4531.
Paired by case, haiku: 4 / 1 / 55 ties; p = 0.375.
Paired by case, sonnet: 2 / 2 / 56 ties; p = 1.0.
Regressions (baseline always passed, skill never did): run-makefile-builds-second-dockerfile-for-sqlite.
Cost, median per run: baseline 18162.0 tokens / 19.0 s; skill 21737.5 tokens / 25.2 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| dotnet-nearest-directory-build-props-wins | pass | pass | pass | pass |
| dotnet-packages-lock-resolves-floating-driver | pass | pass | pass | pass |
| dotnet-sqlite-lock-newer-than-readme | pass | pass | pass | pass |
| dotnet-version-override-in-query-project | pass | pass | pass | pass |
| go-mod-replace-directive-pins-newer-driver | pass | pass | pass | pass |
| go-nested-module-keeps-v4-driver | pass | pass | pass | pass |
| go-sum-lists-older-driver-hashes | pass | pass | pass | pass |
| jvm-gradle-convention-plugin-constraint-raises-driver | pass | pass | pass | pass |
| jvm-gradle-cypher-dsl-calendar-version-beside-server | pass | pass | pass | pass |
| jvm-gradle-java-platform-subproject-pins-driver | pass | pass | pass | pass |
| jvm-gradle-resolution-force-holds-embedded-neo4j | pass | pass | pass | pass |
| jvm-maven-config-overrides-embedded-neo4j-property | pass | pass | pass | pass |
| jvm-maven-driver-bom-import-agrees-with-readme | pass | pass | pass | pass |
| jvm-maven-module-declares-driver-over-managed | pass | pass | pass | pass |
| jvm-maven-sqlite-jdbc-foreign-keys-never-enabled | pass | pass | pass | FAIL:foreign-keys-not-enforced-flagged |
| jvm-sbt-driver-version-in-project-dependencies | pass | pass | pass | pass |
| jvm-sbt-sqlite-dangling-check-quotes-old-column | pass | pass | pass | pass |
| node-bird-survey-embedded-kuzu-yarn-berry | pass | pass | pass | pass |
| node-cable-landings-memgraph-yarn-classic-lock | pass | pass | pass | pass |
| node-campus-workspaces-legacy-report-driver | pass | pass | pass | pass |
| node-grant-coinvestigators-yarn-lock-version-table | pass | pass | pass | pass |
| node-ground-station-cli-shrinkwrap-and-package-lock | pass | pass | pass | pass |
| node-site-links-pnpm-catalog-embedded-ladybug | pass | pass | pass | pass |
| node-toll-plaza-memgraph-npm-lock-and-history-note | pass | pass | pass | pass |
| node-tram-outage-graph-pnpm-override-below-range | pass | pass | pass | pass |
| node-ward-handover-yarn-berry-resolutions | pass | pass | pass | pass |
| py-bike-dock-graph-sqlalchemy-connect-listener | pass | pass | pass | pass |
| py-canal-reaches-sqlite-from-conda-explicit-lock | pass | pass | pass | pass |
| py-court-citations-poetry-capped-networkx | pass | pass | pass | pass |
| py-freight-lanes-pip-compiled-graph-extra | pass | pass | pass | pass |
| py-kelp-forest-food-web-conda-lock-and-readme | pass | pass | pass | pass |
| py-les-miserables-seminar-conda-lock | pass | pass | pass | pass |
| py-permit-review-graph-poetry-tilde-constraint | FAIL:engine-version-pinned,query-language-version-stated,version-conflict-surfaced-under-open-questions,facts-seven-plain-keys,evidence-names-repo-files,open-questions-section | pass | pass | pass |
| py-pollinator-visits-memgraph-conda-pip-section | pass | pass | pass | pass |
| py-railhop-embedded-ladybug-uv-override | pass | pass | pass | pass |
| py-sewer-asset-graph-sqlalchemy-on-sqlite | pass | pass | pass | pass |
| py-uv-workspace-member-driver-locked-at-root | pass | pass | pass | pass |
| run-age-spare-dockerfile-not-built | pass | pass | pass | pass |
| run-ci-service-container-is-the-only-database | pass | pass | pass | pass |
| run-compose-build-target-picks-earlier-stage | pass | pass | pass | pass |
| run-compose-profile-flag-picks-current-service | pass | pass | pass | pass |
| run-compose-second-file-merges-build-args | pass | pass | pass | pass |
| run-devcontainer-build-arg-sets-sqlite-cli | FAIL:engine-version-pinned,version-conflict-surfaced-under-open-questions,facts-seven-plain-keys,evidence-names-repo-files,open-questions-section | FAIL:engine-version-pinned,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | FAIL:foreign-keys-not-enforced-flagged | pass |
| run-devcontainer-compose-files-replace-image | FAIL:engine-version-pinned,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass | pass |
| run-dotenv-compose-file-adds-second-file | pass | pass | pass | pass |
| run-helm-empty-tag-falls-back-to-app-version | pass | pass | pass | pass |
| run-helm-set-flag-overrides-values-file-tag | pass | pass | pass | pass |
| run-kustomize-overlay-images-newtag | pass | pass | pass | pass |
| run-kustomize-patch-replaces-memgraph-image | pass | pass | pass | pass |
| run-kustomize-staging-overlay-not-applied | pass | pass | pass | pass |
| run-makefile-builds-second-dockerfile-for-sqlite | pass | pass | FAIL:foreign-keys-not-enforced-flagged | FAIL:foreign-keys-not-enforced-flagged |
| run-makefile-export-beats-dotenv-tag | pass | pass | pass | pass |
| run-makefile-include-sets-postgres-build-arg | pass | pass | pass | pass |
| run-service-env-file-does-not-set-image-tag | FAIL:engine-version-pinned,query-language-version-stated,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | FAIL:engine-version-pinned,query-language-version-stated,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass |
| run-sqlite-canary-workflow-build-arg | pass | pass | pass | pass |
| run-tox-next-env-not-default | pass | pass | pass | pass |
| run-tox-setenv-picks-testcontainers-image | pass | pass | pass | pass |
| rust-excluded-bench-crate-keeps-own-lock | pass | pass | pass | pass |
| rust-renamed-dependency-key-for-lbug | FAIL:engine-version-pinned,version-conflict-surfaced-under-open-questions,facts-seven-plain-keys,evidence-names-repo-files,open-questions-section | pass | pass | pass |
| rust-workspace-member-lockfile-is-ignored | pass | pass | pass | pass |
