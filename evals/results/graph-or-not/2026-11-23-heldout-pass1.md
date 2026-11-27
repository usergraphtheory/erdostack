## graph-or-not / heldout / 2026-11-23

Models: haiku, sonnet. Skill version: 7dafd02b4482.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 38/40 (95%, 95% CI 84% to 99%) | 0/40 (0%, 95% CI 0% to 9%) |
| skill | 38/40 (95%, 95% CI 84% to 99%) | 40/40 (100%, 95% CI 91% to 100%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 18/20 (90%, 95% CI 70% to 97%) |
| baseline/sonnet | 20/20 (100%, 95% CI 84% to 100%) |
| skill/haiku | 18/20 (90%, 95% CI 70% to 97%) |
| skill/sonnet | 20/20 (100%, 95% CI 84% to 100%) |

Paired by case, all models: skill better on 1, baseline better on 1, tied on 18; sign test p = 1.0.
Paired by case, haiku: 1 / 1 / 18 ties; p = 1.0.
Paired by case, sonnet: 0 / 0 / 20 ties; p = 1.0.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 20454.5 tokens / 37.0 s; skill 27599.0 tokens / 58.0 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| also-bought-edge-count | pass | pass | pass | pass |
| attack-path-triage | FAIL:decision-fits-workload,facts-options-reversal-order | pass | FAIL:decision-fits-workload | pass |
| bom-allocation-explosion | pass | pass | pass | pass |
| churn-call-communities | pass | pass | pass | pass |
| comment-thread-loading | pass | pass | pass | pass |
| expert-finder-prototype | pass | pass | pass | pass |
| follows-social-graph-proposal | pass | pass | pass | pass |
| formula-composition-timeouts | pass | pass | pass | pass |
| invoice-network-cluster-order | pass | pass | pass | pass |
| member-dedupe-erasure | pass | pass | pass | pass |
| outage-impact-topology | pass | pass | pass | pass |
| part-supersession-lookups | pass | pass | pass | pass |
| partner-hierarchy-vendor-pilot | pass | pass | pass | pass |
| research-kg-port-to-sql | pass | pass | pass | pass |
| revision-ancestry-big-table | pass | pass | pass | pass |
| sensor-topology-driver | pass | pass | pass | pass |
| shipment-trace-prod-timeouts | FAIL:nothing-built-or-migrated,facts-options-reversal-order | pass | pass | pass |
| skill-tree-prerequisites | pass | pass | pass | pass |
| task-slip-impact | pass | pass | pass | pass |
| warehouse-pick-routes | pass | pass | FAIL:decision-fits-workload,sql-rejection-rests-on-the-prototype | pass |
