## setup-graph / heldout / 2026-11-24

Models: haiku, sonnet. Skill version: dbfebb3c3cf9.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 72/80 (90%, 95% CI 82% to 95%) | 0/80 (0%, 95% CI 0% to 5%) |
| skill | 78/80 (98%, 95% CI 91% to 99%) | 80/80 (100%, 95% CI 95% to 100%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 33/40 (82%, 95% CI 68% to 91%) |
| baseline/sonnet | 39/40 (98%, 95% CI 87% to 100%) |
| skill/haiku | 39/40 (98%, 95% CI 87% to 100%) |
| skill/sonnet | 39/40 (98%, 95% CI 87% to 100%) |

Paired by case, all models: skill better on 7, baseline better on 1, tied on 32; sign test p = 0.0703.
Paired by case, haiku: 7 / 1 / 32 ties; p = 0.0703.
Paired by case, sonnet: 1 / 1 / 38 ties; p = 1.0.
Regressions (baseline always passed, skill never did): compose-env-example-file-next-to-default-tag.
Cost, median per run: baseline 18722.0 tokens / 18.6 s; skill 23653.0 tokens / 23.6 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| airline-routes-typescript-pnpm-and-neo4j | pass | pass | pass | pass |
| compose-dotenv-sets-the-image-tag | pass | pass | pass | pass |
| compose-env-example-file-next-to-default-tag | pass | pass | FAIL:driver-from-lockfile | FAIL:driver-from-lockfile |
| compose-extends-image-from-base-file | pass | pass | pass | pass |
| compose-memgraph-image-and-ops-runbook | pass | pass | pass | pass |
| compose-profiled-service-beside-built-image | pass | pass | pass | pass |
| course-prerequisites-in-embedded-kuzu-with-poetry | pass | pass | pass | pass |
| davis-attendance-pip-compile-and-design-note | pass | pass | pass | pass |
| dockerfile-pin-and-cypher-25-query-files | FAIL:query-language-fits-engine,query-language-version-stated,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | FAIL:query-language-fits-engine,query-language-version-stated,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass |
| dockerfile-plugin-built-against-older-neo4j | pass | pass | pass | pass |
| film-crew-collaboration-graph-go-and-neo4j | pass | pass | pass | pass |
| florentine-marriages-notebook-and-poetry-project | FAIL:engine-correct,engine-version-is-package-version,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass | pass |
| go-service-links-sqlite-built-in-dockerfile | pass | pass | pass | pass |
| gradle-embedded-neo4j-dynamic-version-locked | pass | pass | pass | pass |
| gradle-range-in-build-file-locked-in-lockfile | pass | pass | pass | pass |
| gradle-sqlite-jdbc-edges-table | pass | pass | pass | pass |
| gradle-testcontainers-image-in-gradle-properties | pass | pass | pass | pass |
| gradle-version-catalog-alias-hides-driver | pass | pass | pass | pass |
| helm-lts-values-file-and-cypher-25-docs | FAIL:query-language-fits-engine,query-language-version-stated,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass | pass |
| helm-second-values-file-wins | pass | pass | pass | pass |
| helm-umbrella-values-set-subchart-tag | FAIL:engine-version-pinned,version-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | pass | pass | pass |
| helm-values-file-leaves-chart-tag-alone | pass | pass | pass | pass |
| karate-club-course-repo-on-uv | pass | pass | pass | pass |
| maven-child-pom-overrides-driver-property | pass | pass | pass | pass |
| maven-embedded-neo4j-version-in-property | pass | pass | pass | pass |
| maven-failsafe-property-sets-testcontainers-image | pass | pass | pass | pass |
| maven-spring-boot-app-adr-names-newer-driver | pass | pass | pass | pass |
| museum-provenance-graph-adr-and-package-lock | FAIL:engine-version-pinned,version-conflict-surfaced-under-open-questions,facts-seven-plain-keys,evidence-names-repo-files,open-questions-section | pass | pass | pass |
| node-tool-builds-better-sqlite3-against-vendored-sqlite | pass | pass | pass | pass |
| org-chart-sqlite-readme-version-list | pass | pass | pass | pass |
| parish-register-family-graph-pip-constraints | pass | pass | pass | pass |
| payment-rings-memgraph-design-note | pass | pass | pass | pass |
| reaction-network-kuzu-held-at-last-release | pass | pass | pass | pass |
| river-network-go-service-on-embedded-kuzu | FAIL:engine-version-pinned,version-conflict-surfaced-under-open-questions,facts-seven-plain-keys,evidence-names-repo-files,open-questions-section | pass | pass | pass |
| road-segments-route-script-with-inline-dependencies | pass | pass | pass | pass |
| rust-cli-rusqlite-range-in-cargo-toml | pass | pass | pass | pass |
| service-dependency-graph-compose-older-than-readme | pass | pass | pass | pass |
| sqlite-link-graph-with-aiosqlite-and-architecture-note | pass | pass | pass | pass |
| supply-trace-requirements-lock-and-readme | pass | pass | pass | pass |
| warehouse-floor-graph-in-rust | FAIL:engine-correct,engine-version-is-package-version,version-conflict-surfaced-under-open-questions,facts-seven-plain-keys,evidence-names-repo-files,open-questions-section | pass | pass | pass |
