## query-review / standards / 2026-11-27

Models: haiku, sonnet. Skill version: 7aef902e8811.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 12/12 (100%, 95% CI 76% to 100%) | 8/8 (100%, 95% CI 68% to 100%) |
| skill | 12/12 (100%, 95% CI 76% to 100%) | 8/8 (100%, 95% CI 68% to 100%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 6/6 (100%, 95% CI 61% to 100%) |
| baseline/sonnet | 6/6 (100%, 95% CI 61% to 100%) |
| skill/haiku | 6/6 (100%, 95% CI 61% to 100%) |
| skill/sonnet | 6/6 (100%, 95% CI 61% to 100%) |

Paired by case, all models: skill better on 0, baseline better on 0, tied on 6; sign test p = 1.0.
Paired by case, haiku: 0 / 0 / 6 ties; p = 1.0.
Paired by case, sonnet: 0 / 0 / 6 ties; p = 1.0.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 21978.5 tokens / 34.1 s; skill 26284.0 tokens / 48.2 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| cypher-clear-archived-group-memberships-on-prod | pass | pass | pass | pass |
| cypher-remove-replayed-likes-on-hearth | pass | pass | pass | pass |
| networkx-remove-listed-friendships-on-practice-graph | pass | pass | pass | pass |
| sqlite-erase-closed-member-accounts-on-main | pass | pass | pass | pass |
| sqlite-remove-listed-memberships-on-scratch | pass | pass | pass | pass |
| sqlite-remove-spam-post-threads-on-prod | pass | pass | pass | pass |
