## schema-first / handoff / 2026-11-24

Models: haiku, sonnet. Skill version: 956ca58330dc.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 12/40 (30%, 95% CI 18% to 45%) | 0/40 (0%, 95% CI 0% to 9%) |
| skill | 38/40 (95%, 95% CI 84% to 99%) | 38/40 (95%, 95% CI 84% to 99%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 5/20 (25%, 95% CI 11% to 47%) |
| baseline/sonnet | 7/20 (35%, 95% CI 18% to 57%) |
| skill/haiku | 19/20 (95%, 95% CI 76% to 99%) |
| skill/sonnet | 19/20 (95%, 95% CI 76% to 99%) |

Paired by case, all models: skill better on 14, baseline better on 0, tied on 6; sign test p = 0.0001.
Paired by case, haiku: 14 / 0 / 6 ties; p = 0.0001.
Paired by case, sonnet: 12 / 0 / 8 ties; p = 0.0005.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 34229.5 tokens / 31.3 s; skill 40286.0 tokens / 41.5 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| handoff-control-networkx-reading-group-co-stars-with-a-normalising-loader | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass | pass |
| handoff-control-networkx-yeast-batches-with-a-loader-and-a-known-pair-test | pass | pass | pass | pass |
| handoff-control-sqlite-ferry-sailings-with-committed-table-script | pass | pass | pass | pass |
| handoff-control-sqlite-mirror-network-with-committed-sample-db | pass | pass | pass | pass |
| handoff-networkx-band-pieces-by-section-then-section-headcount | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-networkx-chargers-on-a-cabinet-then-kw-per-feeder-with-new-installs | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written |
| handoff-networkx-dojo-roster-by-club-then-member-tie-strength | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-networkx-food-bank-kilos-in-a-week-then-kilos-given-out-per-site | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-networkx-huts-in-a-valley-then-reach-with-the-planned-trails | pass | pass | pass | pass |
| handoff-networkx-podcast-episodes-of-a-show-then-guests-across-shows | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-networkx-repos-a-user-maintains-then-stars-across-forks | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | FAIL:stage2-result-correct,asked-instead-of-guessing | pass |
| handoff-networkx-society-calendar-events-attended-then-women-who-met | pass | pass | pass | pass |
| handoff-sqlite-accessions-propagated-from-one-plant-then-plants-in-ground-per-area | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-sqlite-decisions-per-court-then-citations-received-per-court | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-sqlite-depots-reachable-from-a-hub-then-units-on-hand-in-the-north | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-sqlite-issues-blocking-an-issue-then-open-issues-per-person | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-sqlite-junctions-next-to-a-saddle-then-longest-open-gravel-segments | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-sqlite-members-a-player-has-beaten-then-matches-per-venue-since-october | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-sqlite-nonstop-from-an-airport-then-late-arrivals-per-carrier | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-sqlite-spring-offerings-then-courses-requiring-stat-210 | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
