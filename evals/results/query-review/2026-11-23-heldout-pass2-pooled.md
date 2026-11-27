## query-review / heldout / 2026-11-23

Models: haiku, sonnet. Skill version: 7d920c82ad2c.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 71/80 (89%, 95% CI 80% to 94%) | 24/76 (32%, 95% CI 22% to 43%) |
| skill | 79/80 (99%, 95% CI 93% to 100%) | 59/76 (78%, 95% CI 67% to 86%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 34/40 (85%, 95% CI 71% to 93%) |
| baseline/sonnet | 37/40 (92%, 95% CI 80% to 97%) |
| skill/haiku | 39/40 (98%, 95% CI 87% to 100%) |
| skill/sonnet | 40/40 (100%, 95% CI 91% to 100%) |

Paired by case, all models: skill better on 4, baseline better on 1, tied on 15; sign test p = 0.375.
Paired by case, haiku: 4 / 1 / 15 ties; p = 0.375.
Paired by case, sonnet: 3 / 0 / 17 ties; p = 0.25.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 19157.0 tokens / 28.0 s; skill 22879.5 tokens / 35.1 s.
Flaky: cypher-retire-v2-recommender [baseline/sonnet] ['pass', 'FAIL:bounded-relationship-delete-handed-back,migration-file-in-the-repo-format,plan-check-stated']; sqlite-purge-deactivated-edges-job [skill/haiku] ['pass', 'FAIL:removes-exactly-the-deactivated-edges,commits-in-chunks,returns-rows-removed']; cypher-linter-flagged-call-chain [baseline/sonnet] ['FAIL:says-the-pattern-is-already-safe,plan-check-stated', 'pass']; cypher-linter-flagged-call-chain [baseline/haiku] ['pass', 'FAIL:says-the-pattern-is-already-safe,plan-check-stated']; sqlite-reviewer-flagged-coverage-grid [baseline/haiku] ['FAIL:says-the-join-is-intentional,plan-inspected-before-run', 'pass']; sqlite-reviewer-flagged-coverage-grid [baseline/sonnet] ['FAIL:says-the-join-is-intentional,plan-inspected-before-run', 'pass'].

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| cypher-linter-flagged-call-chain | pass; FAIL:says-the-pattern-is-already-safe,plan-check-stated | FAIL:says-the-pattern-is-already-safe,plan-check-stated; pass | pass; pass | pass; pass |
| cypher-log-warning-on-price-card | FAIL:says-the-pairing-is-intended-and-tiny,query-text-untouched; FAIL:says-the-pairing-is-intended-and-tiny,query-text-untouched,plan-check-stated | pass; pass | pass; pass | pass; pass |
| cypher-promo-sales-report-oom | pass; pass | pass; pass | pass; pass | pass; pass |
| cypher-retire-v2-recommender | FAIL:bounded-relationship-delete-handed-back,migration-file-in-the-repo-format,plan-check-stated; FAIL:bounded-relationship-delete-handed-back,migration-file-in-the-repo-format,plan-check-stated | pass; FAIL:bounded-relationship-delete-handed-back,migration-file-in-the-repo-format,plan-check-stated | pass; pass | pass; pass |
| cypher-slow-isbn-lookup | pass; pass | pass; pass | pass; pass | pass; pass |
| cypher-tenant-offboarding-script | pass; pass | pass; pass | pass; pass | pass; pass |
| js-orders-sort-parameter | pass; pass | pass; pass | pass; pass | pass; pass |
| ladybug-member-suggestions-never-returns | pass; pass | pass; pass | pass; pass | pass; pass |
| python-descendants-follow-shortcuts | pass; pass | pass; pass | pass; pass | pass; pass |
| python-injection-report-on-catalogue-search | pass; pass | pass; pass | pass; pass | pass; pass |
| sqlite-cleanup-leaked-scratch-nodes | pass; pass | pass; pass | pass; pass | pass; pass |
| sqlite-clear-shipments-on-prod-request | pass; pass | pass; pass | pass; pass | pass; pass |
| sqlite-dependents-within-hops | pass; pass | pass; pass | pass; pass | pass; pass |
| sqlite-incident-purge-read-notifications | pass; pass | pass; pass | pass; pass | pass; pass |
| sqlite-index-request-for-activity-panel | pass; pass | pass; pass | pass; pass | pass; pass |
| sqlite-purge-deactivated-edges-job | pass; pass | pass; pass | pass; FAIL:removes-exactly-the-deactivated-edges,commits-in-chunks,returns-rows-removed | pass; pass |
| sqlite-repo-card-timeout-popular-repos | pass; pass | pass; pass | pass; pass | pass; pass |
| sqlite-reviewer-flagged-coverage-grid | FAIL:says-the-join-is-intentional,plan-inspected-before-run; pass | FAIL:says-the-join-is-intentional,plan-inspected-before-run; pass | pass; pass | pass; pass |
| sqlite-tag-autocomplete-query | pass; pass | pass; pass | pass; pass | pass; pass |
| sqlite-what-links-here-query | pass; pass | pass; pass | pass; pass | pass; pass |
