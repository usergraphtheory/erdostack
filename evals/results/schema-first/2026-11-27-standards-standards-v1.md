## schema-first / standards / 2026-11-27

Models: haiku, sonnet. Skill version: 956ca58330dc.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 6/12 (50%, 95% CI 25% to 75%) | 0/12 (0%, 95% CI 0% to 24%) |
| skill | 12/12 (100%, 95% CI 76% to 100%) | 12/12 (100%, 95% CI 76% to 100%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 3/6 (50%, 95% CI 19% to 81%) |
| baseline/sonnet | 3/6 (50%, 95% CI 19% to 81%) |
| skill/haiku | 6/6 (100%, 95% CI 61% to 100%) |
| skill/sonnet | 6/6 (100%, 95% CI 61% to 100%) |

Paired by case, all models: skill better on 3, baseline better on 0, tied on 3; sign test p = 0.25.
Paired by case, haiku: 3 / 0 / 3 ties; p = 0.25.
Paired by case, sonnet: 3 / 0 / 3 ties; p = 0.25.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 31202.0 tokens / 42.4 s; skill 37551.5 tokens / 54.5 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| handoff-control-sqlite-friends-and-hops-with-committed-migrations | pass | pass | pass | pass |
| handoff-networkx-comment-subtree-size-then-ten-latest-messages | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-networkx-friends-since-then-friendship-hops | pass | pass | pass | pass |
| handoff-networkx-thread-size-of-a-post-then-replies-and-friendship | pass | pass | pass | pass |
| handoff-sqlite-friends-with-dates-then-replies-to-a-post | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
| handoff-sqlite-person-profile-then-ten-latest-messages | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | FAIL:stage2-result-correct,asked-instead-of-guessing,schema-snapshot-written | pass | pass |
