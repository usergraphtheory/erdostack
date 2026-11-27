## graph-or-not / handoff / 2026-11-24

Models: haiku, sonnet. Skill version: d986c4488518.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 24/50 (48%, 95% CI 35% to 62%) | 0/50 (0%, 95% CI 0% to 7%) |
| skill | 38/50 (76%, 95% CI 63% to 86%) | 50/50 (100%, 95% CI 93% to 100%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 8/25 (32%, 95% CI 17% to 52%) |
| baseline/sonnet | 16/25 (64%, 95% CI 44% to 80%) |
| skill/haiku | 18/25 (72%, 95% CI 52% to 86%) |
| skill/sonnet | 20/25 (80%, 95% CI 61% to 91%) |

Paired by case, all models: skill better on 12, baseline better on 2, tied on 11; sign test p = 0.0129.
Paired by case, haiku: 12 / 2 / 11 ties; p = 0.0129.
Paired by case, sonnet: 6 / 2 / 17 ties; p = 0.2891.
Regressions (baseline always passed, skill never did): handoff-control-networkx-reading-guide-then-specified-nearby-characters.
Cost, median per run: baseline 36702.0 tokens / 47.9 s; skill 44718.0 tokens / 78.4 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| handoff-control-networkx-centenary-kiosk-then-specified-shared-events | pass | pass | pass | pass |
| handoff-control-networkx-reading-guide-then-specified-nearby-characters | pass | pass | FAIL:stage1-decision-fits-workload,stage2-keeps-the-decision | FAIL:stage1-decision-fits-workload,stage2-keeps-the-decision |
| handoff-control-sql-news-tag-tree-bench-in-repo-then-regional-editions-pitch | pass | pass | pass | pass |
| handoff-control-sqlite-bike-parts-compatibility-then-unrelated-low-stock-report | pass | pass | pass | pass |
| handoff-control-sqlite-ledger-account-tree-then-build-subtotals | pass | pass | pass | pass |
| handoff-networkx-budget-formula-cells-then-build-circular-check | pass | pass | pass | pass |
| handoff-networkx-bylaw-cross-references-then-build-repeal-impact | pass | pass | pass | pass |
| handoff-networkx-dojo-friendships-then-build-split-cost | FAIL:stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass | pass |
| handoff-networkx-lab-switch-links-then-build-transfer-bandwidth | FAIL:stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass | pass |
| handoff-networkx-mod-hub-dependencies-then-console-catalogue | FAIL:stage1-decision-fits-workload,decision-record-at-docs-graph | FAIL:stage1-decision-fits-workload,decision-record-at-docs-graph | FAIL:stage1-decision-fits-workload,stage2-keeps-the-decision | pass |
| handoff-networkx-orchard-irrigation-lines-then-build-pipe-layout | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass | pass |
| handoff-networkx-related-papers-citations-then-preprint-merge | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-networkx-science-fair-judges-then-build-assignment | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass | pass |
| handoff-networkx-snow-plough-road-segments-then-build-cutoff-roads | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass |
| handoff-networkx-wiring-harness-circuits-then-neo4j-pushback | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-sql-flag-prerequisites-then-growth-team-merge | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass | FAIL:stage2-invents-no-facts |
| handoff-sql-museum-object-relations-then-trails-funded | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage1-decision-fits-workload,stage2-outcome-correct,stage2-keeps-the-decision | FAIL:stage1-decision-fits-workload,stage2-outcome-correct,stage2-keeps-the-decision |
| handoff-sql-reinsurance-cessions-then-spiral-pushback | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass | pass |
| handoff-sql-wiki-page-links-then-depth-capped-cte-pushback | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | FAIL:stage1-decision-fits-workload,stage2-keeps-the-decision | pass |
| handoff-sqlite-flight-legs-then-build-one-stop-itineraries | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass | pass |
| handoff-sqlite-fx-quotes-then-build-best-conversion | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | FAIL:stage1-decision-fits-workload,stage2-keeps-the-decision | FAIL:stage1-decision-fits-workload,stage2-keeps-the-decision |
| handoff-sqlite-mail-list-nesting-then-drop-path-guard-pushback | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-sqlite-oncall-escalation-then-build-page-order | FAIL:stage1-decision-fits-workload,stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | FAIL:stage1-decision-fits-workload,stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | FAIL:stage1-decision-fits-workload,stage2-keeps-the-decision | FAIL:stage1-decision-fits-workload,stage2-keeps-the-decision |
| handoff-sqlite-service-call-edges-then-build-upstream-warning | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass |
| handoff-sqlite-sheet-cell-references-then-build-recalc-set | pass | pass | FAIL:stage1-decision-fits-workload,stage2-keeps-the-decision | pass |
