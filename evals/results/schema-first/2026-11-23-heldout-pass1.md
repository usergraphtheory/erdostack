## schema-first / heldout / 2026-11-23

Models: haiku, sonnet. Skill version: 956ca58330dc.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 58/74 (78%, 95% CI 68% to 86%) | 2/72 (3%, 95% CI 1% to 10%) |
| skill | 66/74 (89%, 95% CI 80% to 94%) | 72/72 (100%, 95% CI 95% to 100%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 29/37 (78%, 95% CI 63% to 89%) |
| baseline/sonnet | 29/37 (78%, 95% CI 63% to 89%) |
| skill/haiku | 32/37 (86%, 95% CI 72% to 94%) |
| skill/sonnet | 34/37 (92%, 95% CI 79% to 97%) |

Paired by case, all models: skill better on 6, baseline better on 3, tied on 28; sign test p = 0.5078.
Paired by case, haiku: 5 / 2 / 30 ties; p = 0.4531.
Paired by case, sonnet: 6 / 1 / 30 ties; p = 0.125.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 21914.0 tokens / 26.8 s; skill 26773.0 tokens / 36.7 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| cypher-annual-research-report-queries | pass | pass | pass | pass |
| cypher-model-file-is-stale-against-migrations | pass | pass | pass | pass |
| cypher-quantity-and-price-live-on-the-relationship | pass | pass | pass | pass |
| cypher-readme-diagram-is-stale | pass | pass | pass | pass |
| cypher-reviews-reach-hosts-through-listings | pass | pass | pass | pass |
| cypher-royalty-pack-queries-on-ladybug | pass | pass | pass | pass |
| cypher-two-similar-tables-one-carries-the-relationship | pass | pass | pass | pass |
| cypher-ward-report-pack-over-a-hospital-graph | FAIL:q-current-occupancy,schema-snapshot-written | pass | FAIL:q-current-occupancy | pass |
| cypher-weekly-plant-review-queries-on-ladybug | pass | pass | pass | pass |
| cypher-works-at-is-stored-as-employs | pass | pass | pass | pass |
| handoff-control-networkx-collection-documented-in-readme | pass | pass | pass | pass |
| handoff-control-sqlite-ticketing-with-data-dictionary | pass | pass | pass | pass |
| handoff-networkx-reporting-chain-then-skill-coverage | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-networkx-transit-routes-then-depot-seats | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-sqlite-blocked-accounts-then-report-outcomes | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-sqlite-library-loans-then-reservations | FAIL:stage1-result-correct,stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage1-result-correct | pass |
| handoff-sqlite-network-neighbours-then-circuit-bandwidth | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-sqlite-service-deps-then-flag-rollout | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| networkx-capacity-stored-as-text | pass | pass | pass | pass |
| networkx-eight-bibliometric-stats-over-a-research-graph | pass | FAIL:q-first-author-papers,schema-snapshot-written | FAIL:q-first-author-papers | FAIL:q-first-author-papers |
| networkx-eight-sourcing-metrics-over-a-supply-graph | FAIL:q-supplier-countries-per-plant,schema-snapshot-written | pass | FAIL:q-supplier-countries-per-plant | pass |
| networkx-parallel-edges-inflate-degree | pass | pass | pass | pass |
| networkx-rating-missing-on-unreviewed-venues | pass | pass | pass | pass |
| networkx-two-way-links-stored-once | pass | pass | pass | pass |
| networkx-user-says-edges-run-prerequisite-to-course | pass | pass | pass | pass |
| sql-remote-graph-no-schema-source | pass | pass | pass | pass |
| sqlite-amounts-are-minor-units-in-a-larger-repo | pass | pass | pass | pass |
| sqlite-amounts-stored-as-formatted-text | pass | pass | pass | pass |
| sqlite-clear-schema-mutual-follows | pass | pass | pass | pass |
| sqlite-column-named-parent-holds-the-child | pass | pass | pass | pass |
| sqlite-eight-performance-queries-over-a-rail-db | pass | pass | pass | FAIL:q-electrified-km-per-line,q-avg-delay-per-station-oct |
| sqlite-employee-numbers-repeat-across-orgs | pass | pass | pass | pass |
| sqlite-existing-query-reads-a-frozen-table | pass | pass | pass | pass |
| sqlite-nine-network-report-queries-over-a-utility-db | pass | FAIL:q-avg-restore-minutes-by-cause,schema-snapshot-written | FAIL:q-avg-restore-minutes-by-cause | FAIL:q-avg-restore-minutes-by-cause |
| sqlite-node-kinds-share-one-table | pass | pass | pass | pass |
| sqlite-request-needs-transit-time-not-stored | pass | pass | pass | pass |
| sqlite-unfollows-are-soft-deleted-rows | pass | pass | pass | pass |
