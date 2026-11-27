## graph-or-not / handoff / 2026-11-24

Models: haiku, sonnet. Skill version: a8ddcabe4a24.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 34/80 (42%, 95% CI 32% to 53%) | 0/80 (0%, 95% CI 0% to 5%) |
| skill | 74/80 (92%, 95% CI 85% to 96%) | 80/80 (100%, 95% CI 95% to 100%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 9/40 (22%, 95% CI 12% to 38%) |
| baseline/sonnet | 25/40 (62%, 95% CI 47% to 76%) |
| skill/haiku | 36/40 (90%, 95% CI 77% to 96%) |
| skill/sonnet | 38/40 (95%, 95% CI 84% to 99%) |

Paired by case, all models: skill better on 29, baseline better on 1, tied on 10; sign test p = 0.0.
Paired by case, haiku: 28 / 1 / 11 ties; p = 0.0.
Paired by case, sonnet: 14 / 1 / 25 ties; p = 0.001.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 36131.0 tokens / 72.4 s; skill 49019.0 tokens / 70.8 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| handoff-control-networkx-florentine-seminar-then-specified-reach-list | pass | pass | pass | pass |
| handoff-control-networkx-southern-women-circles-then-specified-co-attendees | pass | pass | pass | pass |
| handoff-control-sqlite-degree-requirement-tree-then-specified-course-list | pass | pass | pass | pass |
| handoff-control-sqlite-org-unit-headcount-then-unrelated-unstaffed-report | pass | pass | pass | pass |
| handoff-control-sqlite-rail-line-groups-then-unrelated-late-departures | pass | pass | pass | pass |
| handoff-control-sqlite-roadworks-permits-then-specified-nearby-segments | pass | pass | FAIL:stage1-decision-fits-workload,stage2-keeps-the-decision | pass |
| handoff-control-sqlite-routing-machines-then-unrelated-scrap-report | pass | pass | pass | pass |
| handoff-control-sqlite-tool-crib-kits-then-specified-kit-tools | pass | pass | pass | pass |
| handoff-networkx-access-review-grants-then-sso-consolidation | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass |
| handoff-networkx-bakery-step-graph-then-build-batch-lead-time | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-networkx-biobank-tube-derivations-then-extend-with-recall-list | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass | pass |
| handoff-networkx-bus-recovery-depots-then-build-nearest-depot | pass | pass | pass | pass |
| handoff-networkx-club-encounter-rows-then-build-introduction-count | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass | pass |
| handoff-networkx-consortium-working-groups-then-build-liaison-chain | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass | pass |
| handoff-networkx-conveyor-segments-then-build-shutdown-check | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass | pass |
| handoff-networkx-handwritten-paper-rank-then-build-reading-list | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass | pass |
| handoff-networkx-hgv-diversion-prototype-then-supplier-extract | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass | pass |
| handoff-networkx-one-way-scheme-then-build-trapped-junctions | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass | pass |
| handoff-sql-capacity-planner-where-used-then-plant-exports-arrive | FAIL:stage1-decision-fits-workload,stage2-outcome-correct,stage2-keeps-the-decision,decision-record-at-docs-graph | FAIL:stage1-decision-fits-workload,stage2-outcome-correct,stage2-keeps-the-decision,decision-record-at-docs-graph | pass | pass |
| handoff-sql-grid-switching-trace-then-postgres-upgrade-replay | FAIL:stage1-decision-fits-workload,stage2-outcome-correct,stage2-keeps-the-decision,decision-record-at-docs-graph | FAIL:stage1-decision-fits-workload,decision-record-at-docs-graph | pass | pass |
| handoff-sqlite-advisor-lineage-query-then-national-register-import | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass | FAIL:stage2-invents-no-facts |
| handoff-sqlite-brake-lot-genealogy-then-dba-faster-trace | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass | pass |
| handoff-sqlite-bus-stop-pairs-then-build-connections-board | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass | pass |
| handoff-sqlite-citation-path-explorer-then-new-lead-asks-why | FAIL:stage1-decision-fits-workload,stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage1-decision-fits-workload,stage2-outcome-correct,stage2-keeps-the-decision,decision-record-at-docs-graph | pass | pass |
| handoff-sqlite-community-reach-badge-unsettled-depth-then-product-settles | FAIL:stage1-decision-fits-workload,stage2-outcome-correct,decision-record-at-docs-graph | pass | pass | pass |
| handoff-sqlite-company-register-links-then-sample-benchmark-pushback | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage1-decision-fits-workload,stage2-keeps-the-decision | pass |
| handoff-sqlite-customer-org-rollup-then-merger-numbers | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-sqlite-eco-impact-where-used-then-plant-merge-p95 | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-sqlite-heat-network-isolation-then-contractor-loop-claim | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-sqlite-kitchen-ingredient-swaps-then-build-stand-ins | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-sqlite-mower-bom-then-build-gross-requirements | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass | pass |
| handoff-sqlite-org-billing-parents-then-build-invoice-owner | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass | pass |
| handoff-sqlite-prerequisite-kinds-then-build-eligibility-chain | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass | pass |
| handoff-sqlite-quote-cost-rollup-orphan-lines-then-build-rolled-cost | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass | pass |
| handoff-sqlite-rail-section-closures-then-national-network-merge | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-sqlite-reporting-lines-then-build-signoff-chain | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | FAIL:stage1-decision-fits-workload,stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-sqlite-role-inheritance-untimed-tenant-then-timing-arrives | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct | FAIL:stage2-invents-no-facts |
| handoff-sqlite-sewer-manhole-pipes-then-build-upstream-trace | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | pass | pass |
| handoff-sqlite-shared-signal-accounts-then-build-linked-group | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct,decision-record-at-docs-graph | FAIL:stage2-outcome-correct | pass |
| handoff-sqlite-staff-directory-teams-then-build-visible-people | FAIL:stage2-outcome-correct,stage2-invents-no-facts,decision-record-at-docs-graph | pass | pass | pass |
