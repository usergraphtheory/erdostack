## roast-my-graph / heldout / 2026-11-23

Models: haiku, sonnet. Skill version: 8be30539ba84.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 54/80 (68%, 95% CI 57% to 77%) | 0/80 (0%, 95% CI 0% to 5%) |
| skill | 62/80 (78%, 95% CI 67% to 85%) | 80/80 (100%, 95% CI 95% to 100%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 22/40 (55%, 95% CI 40% to 69%) |
| baseline/sonnet | 32/40 (80%, 95% CI 65% to 90%) |
| skill/haiku | 26/40 (65%, 95% CI 50% to 78%) |
| skill/sonnet | 36/40 (90%, 95% CI 77% to 96%) |

Paired by case, all models: skill better on 8, baseline better on 2, tied on 10; sign test p = 0.1094.
Paired by case, haiku: 5 / 2 / 13 ties; p = 0.4531.
Paired by case, sonnet: 4 / 1 / 15 ties; p = 0.375.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 23933.5 tokens / 55.2 s; skill 30754.5 tokens / 64.1 s.
Flaky: networkx-page-scores-computed-by-hand-and-losing-rank [baseline/haiku] ['pass', 'FAIL:explains-hand-written-pagerank,no-insults,roast-md-path,roast-md-covers-findings,roast-md-footer']; cypher-query-arrow-points-against-the-ingest-direction [baseline/haiku] ['FAIL:explains-reversed-runs-on,roast-md-path,roast-md-covers-findings,roast-md-footer', 'pass']; cypher-query-arrow-points-against-the-ingest-direction [baseline/sonnet] ['FAIL:explains-reversed-runs-on,roast-md-path,roast-md-covers-findings,roast-md-footer', 'pass']; cypher-large-grid-repo-one-unbounded-walk-on-a-meshed-network-among-oddities [baseline/haiku] ['pass', 'FAIL:not-overrated-zone-tree-walk,roast-md-path,roast-md-covers-findings,roast-md-footer']; sqlite-link-table-reverse-lookup-is-indexed-in-a-later-migration [skill/haiku] ['FAIL:no-critical-or-high', 'pass']; sql-membership-table-keeps-its-own-id-because-memberships-have-a-life [baseline/sonnet] ['FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer', 'pass']; sqlite-folder-tree-kept-as-slash-separated-text [skill/haiku] ['pass', 'FAIL:explains-tree-as-path-text']; cypher-loader-merges-on-a-property-the-schema-never-constrains [baseline/haiku] ['FAIL:no-insults,roast-md-path,roast-md-covers-findings,roast-md-footer', 'pass'].

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| cypher-credit-node-is-justified-catch-all-relationship-is-not | pass; pass | pass; pass | pass; pass | pass; pass |
| cypher-large-grid-repo-one-unbounded-walk-on-a-meshed-network-among-oddities | pass; FAIL:not-overrated-zone-tree-walk,roast-md-path,roast-md-covers-findings,roast-md-footer | pass; pass | pass; pass | pass; pass |
| cypher-listing-city-slug-is-a-deliberate-copy-for-the-search-index | FAIL:no-critical-or-high,says-sound-city-slug-copy,roast-md-path,roast-md-covers-findings,roast-md-footer; FAIL:no-critical-or-high,says-sound-city-slug-copy,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,says-sound-city-slug-copy,roast-md-path,roast-md-covers-findings,roast-md-footer; FAIL:no-critical-or-high,says-sound-city-slug-copy,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,says-sound-city-slug-copy; FAIL:no-critical-or-high,says-sound-city-slug-copy | pass; pass |
| cypher-loader-merges-on-a-property-the-schema-never-constrains | FAIL:no-insults,roast-md-path,roast-md-covers-findings,roast-md-footer; pass | pass; pass | pass; pass | pass; pass |
| cypher-query-arrow-points-against-the-ingest-direction | FAIL:explains-reversed-runs-on,roast-md-path,roast-md-covers-findings,roast-md-footer; pass | FAIL:explains-reversed-runs-on,roast-md-path,roast-md-covers-findings,roast-md-footer; pass | pass; pass | pass; pass |
| cypher-recommendation-expands-every-customer-in-the-country | pass; pass | pass; pass | pass; pass | pass; pass |
| ladybug-crew-assignment-as-node-table-and-voyage-linked-by-code-columns | FAIL:explains-assignment-node-table,roast-md-path,roast-md-covers-findings,roast-md-footer; FAIL:explains-assignment-node-table,roast-md-path,roast-md-covers-findings,roast-md-footer | pass; pass | FAIL:finds-assignment-node-table,explains-assignment-node-table; FAIL:finds-assignment-node-table,explains-assignment-node-table | pass; pass |
| ladybug-query-uses-a-relationship-the-schema-does-not-define | pass; pass | pass; pass | pass; pass | pass; pass |
| neo4j-client-walks-referral-tree-one-query-per-member | pass; pass | pass; pass | pass; pass | pass; pass |
| networkx-page-scores-computed-by-hand-and-losing-rank | pass; FAIL:explains-hand-written-pagerank,no-insults,roast-md-path,roast-md-covers-findings,roast-md-footer | pass; pass | FAIL:explains-hand-written-pagerank; FAIL:explains-hand-written-pagerank | pass; pass |
| networkx-sound-build-graph-has-nothing-serious | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer; FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass; pass | pass; pass | pass; pass |
| networkx-sound-network-audit-and-a-request-to-tear-the-coworker-apart | FAIL:no-critical-or-high,says-sound-netcheck-code,roast-md-path,roast-md-covers-findings,roast-md-footer; FAIL:no-critical-or-high,says-sound-netcheck-code,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:says-sound-netcheck-code,roast-md-path,roast-md-covers-findings,roast-md-footer; FAIL:no-critical-or-high,says-sound-netcheck-code,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,says-sound-netcheck-code; FAIL:no-critical-or-high,says-sound-netcheck-code | pass; pass |
| networkx-timetable-search-is-justified-recursive-reachability-is-not | pass; pass | pass; pass | pass; pass | pass; pass |
| sql-membership-table-keeps-its-own-id-because-memberships-have-a-life | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer; FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer; pass | FAIL:no-critical-or-high; FAIL:no-critical-or-high | pass; pass |
| sqlite-block-table-keys-cannot-serve-the-lookup-the-delivery-code-runs | pass; pass | pass; pass | pass; pass | pass; pass |
| sqlite-bom-explosion-stops-after-three-levels-of-joins | pass; pass | pass; pass | pass; pass | pass; pass |
| sqlite-folder-tree-kept-as-slash-separated-text | pass; pass | pass; pass | pass; FAIL:explains-tree-as-path-text | FAIL:explains-tree-as-path-text; FAIL:explains-tree-as-path-text |
| sqlite-link-table-reverse-lookup-is-indexed-in-a-later-migration | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer; FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass; pass | FAIL:no-critical-or-high; pass | pass; pass |
| sqlite-sound-threaded-forum-has-nothing-serious | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer; FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer; FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high; FAIL:no-critical-or-high | FAIL:no-critical-or-high; FAIL:no-critical-or-high |
| sqlite-substitute-walk-never-ends-on-a-swap-loop-beside-naming-quirks | pass; pass | pass; pass | pass; pass | pass; pass |
