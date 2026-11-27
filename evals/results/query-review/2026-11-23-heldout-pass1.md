## query-review / heldout / 2026-11-23

Models: haiku, sonnet. Skill version: 7d920c82ad2c.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 35/40 (88%, 95% CI 74% to 94%) | 14/38 (37%, 95% CI 23% to 53%) |
| skill | 40/40 (100%, 95% CI 91% to 100%) | 29/38 (76%, 95% CI 61% to 87%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 17/20 (85%, 95% CI 64% to 95%) |
| baseline/sonnet | 18/20 (90%, 95% CI 70% to 97%) |
| skill/haiku | 20/20 (100%, 95% CI 84% to 100%) |
| skill/sonnet | 20/20 (100%, 95% CI 84% to 100%) |

Paired by case, all models: skill better on 4, baseline better on 0, tied on 16; sign test p = 0.125.
Paired by case, haiku: 3 / 0 / 17 ties; p = 0.25.
Paired by case, sonnet: 2 / 0 / 18 ties; p = 0.5.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 19352.0 tokens / 28.8 s; skill 23175.5 tokens / 37.1 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| cypher-linter-flagged-call-chain | pass | FAIL:says-the-pattern-is-already-safe,plan-check-stated | pass | pass |
| cypher-log-warning-on-price-card | FAIL:says-the-pairing-is-intended-and-tiny,query-text-untouched,plan-check-stated | pass | pass | pass |
| cypher-promo-sales-report-oom | pass | pass | pass | pass |
| cypher-retire-v2-recommender | FAIL:bounded-relationship-delete-handed-back,migration-file-in-the-repo-format,plan-check-stated | pass | pass | pass |
| cypher-slow-isbn-lookup | pass | pass | pass | pass |
| cypher-tenant-offboarding-script | pass | pass | pass | pass |
| js-orders-sort-parameter | pass | pass | pass | pass |
| ladybug-member-suggestions-never-returns | pass | pass | pass | pass |
| python-descendants-follow-shortcuts | pass | pass | pass | pass |
| python-injection-report-on-catalogue-search | pass | pass | pass | pass |
| sqlite-cleanup-leaked-scratch-nodes | pass | pass | pass | pass |
| sqlite-clear-shipments-on-prod-request | pass | pass | pass | pass |
| sqlite-dependents-within-hops | pass | pass | pass | pass |
| sqlite-incident-purge-read-notifications | pass | pass | pass | pass |
| sqlite-index-request-for-activity-panel | pass | pass | pass | pass |
| sqlite-purge-deactivated-edges-job | pass | pass | pass | pass |
| sqlite-repo-card-timeout-popular-repos | pass | pass | pass | pass |
| sqlite-reviewer-flagged-coverage-grid | FAIL:says-the-join-is-intentional,plan-inspected-before-run | FAIL:says-the-join-is-intentional,plan-inspected-before-run | pass | pass |
| sqlite-tag-autocomplete-query | pass | pass | pass | pass |
| sqlite-what-links-here-query | pass | pass | pass | pass |
