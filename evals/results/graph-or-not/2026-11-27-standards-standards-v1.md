## graph-or-not / standards / 2026-11-27

Models: haiku, sonnet. Skill version: a8ddcabe4a24.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 4/12 (33%, 95% CI 14% to 61%) | 0/12 (0%, 95% CI 0% to 24%) |
| skill | 11/12 (92%, 95% CI 65% to 98%) | 12/12 (100%, 95% CI 76% to 100%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 1/6 (17%, 95% CI 3% to 56%) |
| baseline/sonnet | 3/6 (50%, 95% CI 19% to 81%) |
| skill/haiku | 5/6 (83%, 95% CI 44% to 97%) |
| skill/sonnet | 6/6 (100%, 95% CI 61% to 100%) |

Paired by case, all models: skill better on 5, baseline better on 0, tied on 1; sign test p = 0.0625.
Paired by case, haiku: 4 / 0 / 2 ties; p = 0.125.
Paired by case, sonnet: 3 / 0 / 3 ties; p = 0.25.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 31890.0 tokens / 45.8 s; skill 47869.0 tokens / 160.9 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| handoff-control-sqlite-recent-activity-thread-roots-then-specified-query | pass | pass | pass | pass |
| handoff-networkx-follower-export-nightly-scores-then-build-job | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass | pass |
| handoff-networkx-relay-latency-graph-then-build-route-costs | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass |
| handoff-sql-connection-line-unsettled-depth-then-depth-four-measured | FAIL:stage1-decision-fits-workload,stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-sqlite-connection-degree-badge-then-build-lookup | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass | pass |
| handoff-sqlite-friends-tab-then-build-friend-list | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct | pass |
