## graph-or-not / handoff / 2026-11-24

Models: haiku, sonnet. Skill version: d986c4488518.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 19/40 (48%, 95% CI 33% to 62%) | 0/40 (0%, 95% CI 0% to 9%) |
| skill | 33/40 (82%, 95% CI 68% to 91%) | 40/40 (100%, 95% CI 91% to 100%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 8/20 (40%, 95% CI 22% to 61%) |
| baseline/sonnet | 11/20 (55%, 95% CI 34% to 74%) |
| skill/haiku | 13/20 (65%, 95% CI 43% to 82%) |
| skill/sonnet | 20/20 (100%, 95% CI 84% to 100%) |

Paired by case, all models: skill better on 12, baseline better on 2, tied on 6; sign test p = 0.0129.
Paired by case, haiku: 7 / 2 / 11 ties; p = 0.1797.
Paired by case, sonnet: 9 / 0 / 11 ties; p = 0.0039.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 35307.0 tokens / 36.3 s; skill 44539.5 tokens / 54.1 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| handoff-control-networkx-marriage-network-then-specified-distance | pass | pass | pass | pass |
| handoff-control-sql-help-articles-bench-in-repo-then-neo4j-pitch | pass | pass | pass | pass |
| handoff-control-sql-valve-downstream-bench-in-repo-then-merger | pass | pass | FAIL:stage1-decision-fits-workload,stage2-keeps-the-decision | pass |
| handoff-control-sqlite-session-tags-then-unrelated-no-show-report | pass | pass | pass | pass |
| handoff-networkx-character-ties-then-build-connection-path | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass |
| handoff-networkx-club-introductions-then-keep-own-search-pushback | pass | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass |
| handoff-networkx-contact-points-then-rewrite-group-records | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | FAIL:stage2-invents-no-facts,decision-record-at-docs-graph | FAIL:stage2-invents-no-facts | pass |
| handoff-networkx-event-attendance-then-build-close-groups | pass | pass | FAIL:stage2-invents-no-facts | pass |
| handoff-networkx-trail-segments-then-build-fastest-route | pass | pass | pass | pass |
| handoff-sql-alumni-mutual-connections-then-merger-growth | pass | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass |
| handoff-sql-artifact-reverse-deps-then-registry-merge | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-invents-no-facts | pass |
| handoff-sql-beneficial-ownership-chains-then-licence-review | FAIL:stage1-decision-fits-workload,stage2-outcome-correct,decision-record-at-docs-graph | pass | FAIL:stage1-decision-fits-workload,stage2-keeps-the-decision | pass |
| handoff-sql-drug-interaction-classes-then-nested-formulary | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct | pass |
| handoff-sql-fibre-topology-impact-then-recursive-cte-pushback | FAIL:stage2-outcome-correct,stage2-keeps-the-decision,decision-record-at-docs-graph | pass | FAIL:stage1-decision-fits-workload,stage2-keeps-the-decision | pass |
| handoff-sql-parcel-adjacency-letters-then-contractor-neo4j-pitch | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass | pass |
| handoff-sql-ticket-blockers-then-graph-database-pushback | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass |
| handoff-sqlite-coauthor-conflicts-then-build-reviewer-filter | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-sqlite-course-equivalences-then-build-transfer-matches | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass | pass |
| handoff-sqlite-share-holdings-then-build-controlled-companies | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-sqlite-url-redirects-then-build-flatten | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass | pass |
