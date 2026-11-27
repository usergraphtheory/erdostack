## setup-graph / heldout / 2026-11-23

Models: haiku, sonnet. Skill version: dbfebb3c3cf9.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 41/52 (79%, 95% CI 66% to 88%) | 13/52 (25%, 95% CI 15% to 38%) |
| skill | 51/52 (98%, 95% CI 90% to 100%) | 52/52 (100%, 95% CI 93% to 100%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 18/26 (69%, 95% CI 50% to 84%) |
| baseline/sonnet | 23/26 (88%, 95% CI 71% to 96%) |
| skill/haiku | 25/26 (96%, 95% CI 81% to 99%) |
| skill/sonnet | 26/26 (100%, 95% CI 87% to 100%) |

Paired by case, all models: skill better on 8, baseline better on 0, tied on 18; sign test p = 0.0078.
Paired by case, haiku: 7 / 0 / 19 ties; p = 0.0156.
Paired by case, sonnet: 3 / 0 / 23 ties; p = 0.25.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 19430.0 tokens / 21.0 s; skill 25591.0 tokens / 27.1 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| agents-file-allows-writes-to-dev-graph | pass | pass | pass | pass |
| character-graph-in-graphml-and-pickle | pass | pass | pass | pass |
| compose-build-arg-overrides-dockerfile-default | pass | pass | pass | pass |
| compose-override-file-swaps-the-image | pass | pass | pass | pass |
| context-file-already-matches-repo | pass | pass | pass | pass |
| context-file-names-a-renamed-make-target | pass | pass | pass | pass |
| cypher-version-not-settled-by-repo | pass | pass | pass | pass |
| dockerfile-pin-newer-than-architecture-doc | pass | pass | pass | pass |
| driver-version-from-bom-in-parent-pom | pass | pass | pass | pass |
| early-npm-name-lbug-in-pnpm-lock | FAIL:engine-version-pinned,evidence-names-repo-files,open-questions-section | FAIL:engine-version-pinned | pass | pass |
| five-services-user-names-the-neo4j-one | pass | pass | pass | pass |
| hosted-instance-nothing-pins-the-server | pass | pass | pass | pass |
| kuzu-npm-pin-in-package-lock | FAIL:evidence-names-repo-files,open-questions-section,unmaintained-dependency-flagged | pass | pass | pass |
| ladybug-version-only-in-uv-lock | FAIL:engine-version-pinned,evidence-names-repo-files,open-questions-section | pass | pass | pass |
| large-repo-stale-copies-of-every-fact | pass | pass | pass | pass |
| lbug-crate-version-only-in-cargo-lock | pass | pass | pass | pass |
| memgraph-image-behind-neo4j-driver | FAIL:query-language-fits-engine,evidence-names-repo-files,open-questions-section | pass | FAIL:query-language-fits-engine | pass |
| monorepo-two-graph-stores | pass | FAIL:run-queries-real,evidence-names-repo-files,open-questions-section | pass | pass |
| named-service-uses-a-different-engine | FAIL:context-written,engine-correct,engine-version-pinned,query-language-fits-engine,driver-from-lockfile,run-queries-real,access-correct,schema-snapshot-exists-or-none,facts-seven-plain-keys,evidence-names-repo-files,open-questions-section,nothing-else-modified | FAIL:context-written,engine-correct,engine-version-pinned,query-language-fits-engine,driver-from-lockfile,run-queries-real,access-correct,schema-snapshot-exists-or-none,facts-seven-plain-keys,evidence-names-repo-files,open-questions-section,nothing-else-modified | pass | pass |
| no-graph-only-a-roadmap-idea | FAIL:empty-case-convention,says-no-graph-store | pass | pass | pass |
| old-driver-line-against-new-server | FAIL:query-language-fits-engine,evidence-names-repo-files,open-questions-section,driver-server-gap-flagged | pass | pass | pass |
| passwords-in-env-files-stay-out-of-docs | FAIL:query-language-fits-engine,evidence-names-repo-files,open-questions-section | pass | pass | pass |
| setup-script-sets-default-language-cypher-5 | pass | pass | pass | pass |
| stale-context-file-after-upgrades | pass | pass | pass | pass |
| stale-requirements-file-names-the-old-engine | pass | pass | pass | pass |
| testcontainers-image-string-in-test-code | pass | pass | pass | pass |
