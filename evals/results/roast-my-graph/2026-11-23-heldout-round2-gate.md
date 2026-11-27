## roast-my-graph / heldout / 2026-11-23

Models: haiku, sonnet. Skill version: 861797c1f1d1.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 65/80 (81%, 95% CI 71% to 88%) | 0/80 (0%, 95% CI 0% to 5%) |
| skill | 73/80 (91%, 95% CI 83% to 96%) | 80/80 (100%, 95% CI 95% to 100%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 26/40 (65%, 95% CI 50% to 78%) |
| baseline/sonnet | 39/40 (98%, 95% CI 87% to 100%) |
| skill/haiku | 34/40 (85%, 95% CI 71% to 93%) |
| skill/sonnet | 39/40 (98%, 95% CI 87% to 100%) |

Paired by case, all models: skill better on 10, baseline better on 2, tied on 28; sign test p = 0.0386.
Paired by case, haiku: 10 / 2 / 28 ties; p = 0.0386.
Paired by case, sonnet: 1 / 1 / 38 ties; p = 1.0.
Regressions (baseline always passed, skill never did): ladybug-checkout-price-takes-any-row-of-a-price-history-it-never-closes-off.
Cost, median per run: baseline 23190.5 tokens / 54.5 s; skill 30095.5 tokens / 78.2 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| cypher-duplicate-finder-reaches-other-workspaces-through-shared-content-nodes | pass | pass | pass | pass |
| cypher-language-hub-with-millions-of-learners-is-only-ever-reached-from-the-learner-side | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| cypher-lease-dates-loaded-as-day-first-text-and-compared-as-text | pass | pass | pass | pass |
| cypher-linter-flags-three-comma-patterns-and-only-the-ridership-report-is-wrong | pass | pass | pass | pass |
| cypher-parcel-depot-copy-goes-stale-when-a-parcel-moves | pass | pass | pass | pass |
| cypher-retired-products-stay-because-ten-years-of-orders-point-at-them | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| cypher-room-number-declared-unique-across-hotels-that-number-their-own | pass | pass | pass | pass |
| cypher-sync-writes-reports-to-from-the-manager-beside-a-misspelt-property | pass | pass | pass | pass |
| ladybug-api-formats-table-names-from-a-fixed-map-and-a-scanner-calls-it-injection | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| ladybug-archive-schema-with-one-tag-table-for-two-kinds-of-item-is-sound | FAIL:says-sound-archive-schema,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | FAIL:says-sound-archive-schema | pass |
| ladybug-checkout-price-takes-any-row-of-a-price-history-it-never-closes-off | pass | pass | FAIL:finds-old-price-at-checkout | FAIL:finds-old-price-at-checkout |
| ladybug-invoice-keeps-the-billing-address-as-issued-and-a-reviewer-calls-it-duplication | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass |
| ladybug-monthly-ride-bill-passes-the-last-day-to-a-query-that-excludes-it | FAIL:explains-last-day-unbilled,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| ladybug-region-revenue-adds-each-order-total-once-per-line | pass | pass | pass | pass |
| neo4j-client-records-each-redelivered-stock-message-as-a-new-movement | pass | pass | pass | pass |
| neo4j-nightly-rebuild-creates-into-an-empty-graph-and-a-reviewer-wants-merge | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | FAIL:no-critical-or-high | pass |
| neo4j-queries-pinned-to-cypher-5-on-purpose-while-two-servers-disagree-on-the-default | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| neo4j-report-thresholds-in-euros-against-amounts-loaded-in-cents | pass | pass | pass | pass |
| neo4j-seat-hold-checks-in-one-transaction-and-creates-in-another | pass | pass | FAIL:finds-check-then-create-race | pass |
| neo4j-usage-export-pages-with-skip-over-sessions-it-has-just-marked-exported | pass | pass | pass | pass |
| networkx-cheapest-lane-keeps-whichever-carrier-quote-was-loaded-last | pass | pass | pass | pass |
| networkx-dag-check-lists-every-cycle-to-report-the-first-one | pass | pass | pass | pass |
| networkx-pipe-edges-load-manhole-ids-as-text-beside-integer-manhole-nodes | pass | pass | pass | pass |
| networkx-porter-routes-weigh-every-lift-ride-as-one-second | pass | pass | pass | pass |
| networkx-sound-all-pairs-table-is-small-and-saves-a-dijkstra-per-lookup | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| networkx-sound-fibre-plant-is-undirected-because-a-cable-has-no-direction | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| networkx-sound-kiosk-threads-share-a-frozen-graph-that-is-swapped-whole | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| networkx-sound-relay-route-counts-legs-because-the-price-is-per-leg | pass | pass | pass | pass |
| sqlite-alert-fanout-pages-followers-by-a-whole-second-timestamp-and-drops-ties | pass | pass | pass | pass |
| sqlite-award-search-has-a-leg-limit-and-still-walks-every-itinerary | pass | pass | pass | pass |
| sqlite-closure-rows-are-not-rewritten-when-a-storage-location-moves | pass | pass | pass | pass |
| sqlite-credit-transfer-walk-remembers-visited-colleges-as-digits-in-a-string | pass | pass | pass | pass |
| sqlite-door-access-walk-follows-crew-links-that-were-removed | pass | pass | pass | pass |
| sqlite-fitment-lookup-by-bike-lost-its-index-when-a-migration-rebuilt-the-table | pass | pass | pass | pass |
| sqlite-flock-book-withdrawal-cascades-through-sire-and-dam-to-the-descendants | FAIL:not-overrated-show-result-cascade,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | FAIL:not-overrated-show-result-cascade | pass |
| sqlite-incompatible-pairs-stored-once-and-the-shelf-check-reads-one-side | pass | pass | pass | pass |
| sqlite-sound-asset-paths-are-delimited-indexed-and-moved-in-one-statement | FAIL:no-critical-or-high,says-sound-id-paths-sound,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| sqlite-sound-ferry-walk-has-no-cycle-guard-because-every-step-is-later | FAIL:says-sound-time-ordered-walk-ends,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | FAIL:no-critical-or-high | pass |
| sqlite-sound-thread-page-joins-once-because-a-trigger-keeps-replies-one-level-deep | pass | pass | pass | pass |
| sqlite-topic-count-adds-an-article-once-per-route-through-a-shared-subtopic | pass | pass | pass | pass |
