## graph-or-not / handoff / 2026-11-24

Models: haiku, sonnet. Skill version: d986c4488518.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 22/40 (55%, 95% CI 40% to 69%) | 0/40 (0%, 95% CI 0% to 9%) |
| skill | 36/40 (90%, 95% CI 77% to 96%) | 40/40 (100%, 95% CI 91% to 100%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 8/20 (40%, 95% CI 22% to 61%) |
| baseline/sonnet | 14/20 (70%, 95% CI 48% to 86%) |
| skill/haiku | 16/20 (80%, 95% CI 58% to 92%) |
| skill/sonnet | 20/20 (100%, 95% CI 84% to 100%) |

Paired by case, all models: skill better on 11, baseline better on 1, tied on 8; sign test p = 0.0063.
Paired by case, haiku: 9 / 1 / 10 ties; p = 0.0215.
Paired by case, sonnet: 6 / 0 / 14 ties; p = 0.0312.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 35307.0 tokens / 36.3 s; skill 44539.5 tokens / 54.1 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| handoff-control-networkx-marriage-network-then-specified-distance | pass | pass | pass | pass |
| handoff-control-sql-help-articles-bench-in-repo-then-neo4j-pitch | pass | pass | pass | pass |
| handoff-control-sql-valve-downstream-bench-in-repo-then-merger | pass | pass | FAIL:stage1-decision-fits-workload,stage2-keeps-the-decision | pass |
| handoff-control-sqlite-session-tags-then-unrelated-no-show-report | pass | pass | pass | pass |
| handoff-networkx-character-ties-then-build-connection-path | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-networkx-club-introductions-then-keep-own-search-pushback | pass | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-networkx-contact-points-then-rewrite-group-records | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass | pass |
| handoff-networkx-event-attendance-then-build-close-groups | pass | pass | pass | pass |
| handoff-networkx-trail-segments-then-build-fastest-route | pass | pass | pass | pass |
| handoff-sql-alumni-mutual-connections-then-merger-growth | pass | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-sql-artifact-reverse-deps-then-registry-merge | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass | pass |
| handoff-sql-beneficial-ownership-chains-then-licence-review | FAIL:stage1-decision-fits-workload,stage2-outcome-correct,decision-record-at-docs-graph | pass | FAIL:stage1-decision-fits-workload,stage2-keeps-the-decision | pass |
| handoff-sql-drug-interaction-classes-then-nested-formulary | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | FAIL:stage2-outcome-correct | pass |
| handoff-sql-fibre-topology-impact-then-recursive-cte-pushback | FAIL:stage2-outcome-correct,stage2-keeps-the-decision,decision-record-at-docs-graph | pass | FAIL:stage1-decision-fits-workload,stage2-keeps-the-decision | pass |
| handoff-sql-parcel-adjacency-letters-then-contractor-neo4j-pitch | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass | pass |
| handoff-sql-ticket-blockers-then-graph-database-pushback | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-sqlite-coauthor-conflicts-then-build-reviewer-filter | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-sqlite-course-equivalences-then-build-transfer-matches | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass | pass |
| handoff-sqlite-share-holdings-then-build-controlled-companies | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-sqlite-url-redirects-then-build-flatten | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass | pass |
