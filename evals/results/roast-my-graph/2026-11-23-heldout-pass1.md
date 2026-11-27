## roast-my-graph / heldout / 2026-11-23

Models: haiku, sonnet. Skill version: 8be30539ba84.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 27/40 (68%, 95% CI 52% to 80%) | 0/40 (0%, 95% CI 0% to 9%) |
| skill | 32/40 (80%, 95% CI 65% to 90%) | 40/40 (100%, 95% CI 91% to 100%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 11/20 (55%, 95% CI 34% to 74%) |
| baseline/sonnet | 16/20 (80%, 95% CI 58% to 92%) |
| skill/haiku | 14/20 (70%, 95% CI 48% to 86%) |
| skill/sonnet | 18/20 (90%, 95% CI 70% to 97%) |

Paired by case, all models: skill better on 7, baseline better on 2, tied on 11; sign test p = 0.1797.
Paired by case, haiku: 4 / 1 / 15 ties; p = 0.375.
Paired by case, sonnet: 3 / 1 / 16 ties; p = 0.625.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 23764.0 tokens / 60.4 s; skill 30754.5 tokens / 69.5 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| cypher-credit-node-is-justified-catch-all-relationship-is-not | pass | pass | pass | pass |
| cypher-large-grid-repo-one-unbounded-walk-on-a-meshed-network-among-oddities | pass | pass | pass | pass |
| cypher-listing-city-slug-is-a-deliberate-copy-for-the-search-index | FAIL:no-critical-or-high,says-sound-city-slug-copy,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,says-sound-city-slug-copy,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,says-sound-city-slug-copy | pass |
| cypher-loader-merges-on-a-property-the-schema-never-constrains | FAIL:no-insults,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| cypher-query-arrow-points-against-the-ingest-direction | FAIL:explains-reversed-runs-on,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| cypher-recommendation-expands-every-customer-in-the-country | pass | pass | pass | pass |
| ladybug-crew-assignment-as-node-table-and-voyage-linked-by-code-columns | FAIL:explains-assignment-node-table,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | FAIL:finds-assignment-node-table,explains-assignment-node-table | pass |
| ladybug-query-uses-a-relationship-the-schema-does-not-define | pass | pass | pass | pass |
| neo4j-client-walks-referral-tree-one-query-per-member | pass | pass | pass | pass |
| networkx-page-scores-computed-by-hand-and-losing-rank | pass | pass | FAIL:explains-hand-written-pagerank | pass |
| networkx-sound-build-graph-has-nothing-serious | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| networkx-sound-network-audit-and-a-request-to-tear-the-coworker-apart | FAIL:no-critical-or-high,says-sound-netcheck-code,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,says-sound-netcheck-code,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,says-sound-netcheck-code | pass |
| networkx-timetable-search-is-justified-recursive-reachability-is-not | pass | pass | pass | pass |
| sql-membership-table-keeps-its-own-id-because-memberships-have-a-life | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high | pass |
| sqlite-block-table-keys-cannot-serve-the-lookup-the-delivery-code-runs | pass | pass | pass | pass |
| sqlite-bom-explosion-stops-after-three-levels-of-joins | pass | pass | pass | pass |
| sqlite-folder-tree-kept-as-slash-separated-text | pass | pass | pass | FAIL:explains-tree-as-path-text |
| sqlite-link-table-reverse-lookup-is-indexed-in-a-later-migration | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| sqlite-sound-threaded-forum-has-nothing-serious | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high | FAIL:no-critical-or-high |
| sqlite-substitute-walk-never-ends-on-a-swap-loop-beside-naming-quirks | pass | pass | pass | pass |
