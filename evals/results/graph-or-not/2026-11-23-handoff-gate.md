## graph-or-not / handoff / 2026-11-23

Models: haiku, sonnet. Skill version: d986c4488518.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 10/28 (36%, 95% CI 21% to 54%) | 0/28 (0%, 95% CI 0% to 12%) |
| skill | 27/28 (96%, 95% CI 82% to 99%) | 28/28 (100%, 95% CI 88% to 100%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 4/14 (29%, 95% CI 12% to 55%) |
| baseline/sonnet | 6/14 (43%, 95% CI 21% to 67%) |
| skill/haiku | 14/14 (100%, 95% CI 78% to 100%) |
| skill/sonnet | 13/14 (93%, 95% CI 68% to 99%) |

Paired by case, all models: skill better on 10, baseline better on 0, tied on 4; sign test p = 0.002.
Paired by case, haiku: 10 / 0 / 4 ties; p = 0.002.
Paired by case, sonnet: 7 / 0 / 7 ties; p = 0.0156.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 40169.0 tokens / 36.7 s; skill 55095.0 tokens / 57.0 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| handoff-control-sql-rate-inheritance-bench-in-repo-then-acquisition | pass | pass | pass | pass |
| handoff-control-sqlite-mentor-tree-then-unrelated-lapsed-report | pass | pass | pass | pass |
| handoff-control-sqlite-referral-rule-in-repo-then-build-recipients | pass | pass | pass | pass |
| handoff-networkx-ci-target-graph-then-build-affected-tests | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass | pass |
| handoff-networkx-crash-grouping-then-recursive-sql-pushback | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass |
| handoff-networkx-quest-graph-ci-then-graph-database-pushback | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-networkx-ski-route-planner-then-two-more-resorts | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-networkx-tram-stops-then-build-critical-stops | pass | pass | pass | pass |
| handoff-sql-category-filter-then-growth-below-tripwire | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-sql-cms-page-tree-then-materialised-path-pushback | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-sql-direct-suppliers-then-tier-three-contract | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | FAIL:stage2-outcome-correct |
| handoff-sql-expense-approvals-then-management-chain-pushback | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-sqlite-legal-payer-chain-then-build-payer-lookup | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass | pass |
| handoff-sqlite-pairs-with-strip-then-build-two-step-pairs | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
