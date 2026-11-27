## schema-first / handoff / 2026-11-23

Models: haiku, sonnet. Skill version: 956ca58330dc.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 4/24 (17%, 95% CI 7% to 36%) | 0/24 (0%, 95% CI 0% to 14%) |
| skill | 24/24 (100%, 95% CI 86% to 100%) | 23/24 (96%, 95% CI 80% to 99%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 2/12 (17%, 95% CI 5% to 45%) |
| baseline/sonnet | 2/12 (17%, 95% CI 5% to 45%) |
| skill/haiku | 12/12 (100%, 95% CI 76% to 100%) |
| skill/sonnet | 12/12 (100%, 95% CI 76% to 100%) |

Paired by case, all models: skill better on 10, baseline better on 0, tied on 2; sign test p = 0.002.
Paired by case, haiku: 10 / 0 / 2 ties; p = 0.002.
Paired by case, sonnet: 10 / 0 / 2 ties; p = 0.002.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 40924.0 tokens / 37.2 s; skill 49417.0 tokens / 49.6 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| handoff-control-networkx-programme-with-committed-builder | pass | pass | pass | pass |
| handoff-control-sqlite-apiary-with-committed-migrations | pass | pass | pass | pass |
| handoff-networkx-river-reaches-upstream-then-gauge-peaks-in-metres | FAIL:stage2-result-correct,schema-snapshot-written | FAIL:stage2-result-correct,schema-snapshot-written | pass | pass |
| handoff-networkx-sampled-tracks-then-label-running-time | FAIL:stage2-result-correct,schema-snapshot-written | FAIL:stage2-result-correct,schema-snapshot-written | pass | pass |
| handoff-networkx-wiki-subcategories-then-live-pages-per-category | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-networkx-word-ancestry-then-donor-languages | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-sqlite-ci-upstream-jobs-then-artifact-bytes-still-stored | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-sqlite-dishes-using-an-ingredient-then-cheapest-price-per-kilo | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-sqlite-food-web-predators-then-threatened-by-habitat | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-sqlite-league-away-wins-then-transfer-spend | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-sqlite-motion-sponsors-then-votes-for-by-party | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-sqlite-parish-register-grandchildren-then-weddings-by-decade | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
