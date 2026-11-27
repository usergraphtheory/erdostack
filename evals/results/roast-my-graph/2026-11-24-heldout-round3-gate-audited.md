## roast-my-graph / heldout / 2026-11-24

Models: haiku, sonnet. Skill version: 328dae67cdaa.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 191/240 (80%, 95% CI 74% to 84%) | 0/240 (0%, 95% CI 0% to 2%) |
| skill | 223/240 (93%, 95% CI 89% to 96%) | 237/240 (99%, 95% CI 96% to 100%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 89/120 (74%, 95% CI 66% to 81%) |
| baseline/sonnet | 102/120 (85%, 95% CI 78% to 90%) |
| skill/haiku | 103/120 (86%, 95% CI 78% to 91%) |
| skill/sonnet | 120/120 (100%, 95% CI 97% to 100%) |

Paired by case, all models: skill better on 29, baseline better on 8, tied on 83; sign test p = 0.0008.
Paired by case, haiku: 22 / 8 / 90 ties; p = 0.0161.
Paired by case, sonnet: 18 / 0 / 102 ties; p = 0.0.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 22828.5 tokens / 47.9 s; skill 30098.5 tokens / 73.6 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| cypher-air-sensor-inventory-import-with-two-merges | pass | pass | pass | pass |
| cypher-contact-dedupe-statements-and-the-referral-credit-report | pass | pass | pass | pass |
| cypher-depot-closure-script-and-a-review-comment-on-detach-delete | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| cypher-distribution-grid-model-loader-and-outage-queries | pass | pass | pass | pass |
| cypher-electronic-parts-weekly-import-and-site-queries | FAIL:explains-maker-per-part,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:not-overrated-offers-merge-correct,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:finds-maker-per-part,explains-maker-per-part | pass |
| cypher-expense-approval-graph-and-the-automated-leaver-process | pass | pass | pass | pass |
| cypher-freelance-marketplace-contracts-and-skill-claims | pass | pass | pass | pass |
| cypher-library-loans-and-a-pr-comment-about-join-tables | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass |
| cypher-maintenance-procedure-steps-walked-with-open-ended-next-patterns | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| cypher-marketplace-payouts-and-the-currency-nodes | FAIL:says-sound-currency-end-point,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | FAIL:says-sound-currency-end-point | pass |
| cypher-municipal-borders-graph-and-an-undirected-pattern-lint | pass | pass | pass | pass |
| cypher-music-catalogue-loader-and-a-one-statement-rewrite-pr | FAIL:no-critical-or-high,says-sound-separate-merges,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:says-sound-separate-merges | pass |
| cypher-package-registry-browse-site-queries | pass | pass | pass | pass |
| cypher-procurement-offers-load-and-the-spot-purchase-rows | pass | pass | pass | pass |
| cypher-quarterly-purge-of-closed-merchants-and-expired-coupons | pass | pass | pass | pass |
| cypher-reading-tracker-model-and-book-page-queries | pass | pass | pass | pass |
| cypher-rental-lease-model-and-a-consultant-who-wants-it-flattened | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| cypher-research-office-coauthor-graph-and-annual-report-queries | pass | pass | pass | pass |
| cypher-research-office-collaboration-report-and-profile-queries | FAIL:not-overrated-keyed-link-pair,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | FAIL:explains-pairs-counted-twice,not-overrated-keyed-link-pair | pass |
| cypher-room-booking-grid-and-booking-statements-fail-a-ci-linter | FAIL:no-critical-or-high,says-sound-room-slot-grid,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| cypher-seed-bank-subqueries-and-a-contractor-note-on-cypher-25 | FAIL:no-critical-or-high,says-sound-scope-clause-on-5-26,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | FAIL:says-sound-scope-clause-on-5-26 | pass |
| cypher-shop-customer-merge-statements | pass | pass | pass | pass |
| cypher-streaming-home-screen-rails-and-title-page-queries | pass | pass | pass | pass |
| cypher-team-health-card-and-shift-handover-queries | FAIL:not-overrated-pinned-handover,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:not-overrated-pinned-handover,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass |
| cypher-tram-planner-orders-matched-paths-by-length-and-keeps-one | pass | pass | pass | pass |
| cypher-workspace-offboarding-and-four-unbatched-delete-lint-errors | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass |
| ladybug-board-queries-and-a-lint-report-with-four-flags | pass | pass | pass | pass |
| ladybug-diy-guides-sidebar-and-country-availability | pass | pass | pass | pass |
| ladybug-hotel-search-schema-with-amenity-and-booking-tables | pass | pass | pass | pass |
| ladybug-month-end-billing-export-and-a-query-linter | FAIL:no-critical-or-high,says-sound-export-needs-every-row,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,says-sound-export-needs-every-row,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high | pass |
| ladybug-parcel-tracking-schema-and-a-carrier-bucketing-proposal | pass | pass | pass | pass |
| ladybug-record-catalogue-releases-credits-and-liner-notes | FAIL:no-critical-or-high,says-sound-liner-notes-list,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| ladybug-shelf-tablet-promotion-and-transfer-queries | FAIL:not-overrated-pinned-store-pair,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:not-overrated-pinned-store-pair,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass |
| neo4j-allotment-queries-and-a-lint-report-about-importing-with | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high | pass |
| neo4j-bibliography-ingest-logs-cartesian-warnings-on-every-link-batch | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass |
| neo4j-bookshop-stock-loader-and-the-october-feed | pass | pass | pass | pass |
| neo4j-climbing-gym-member-sync-and-a-teammate-worried-about-nulls | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | FAIL:no-critical-or-high,says-sound-nulls-only-in-set | pass |
| neo4j-departure-backfill-and-a-teammate-who-wants-one-transaction-per-file | FAIL:no-critical-or-high,says-sound-auto-commit-batching,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| neo4j-dock-availability-queries-beside-the-compose-file | pass | pass | FAIL:finds-scope-clause-on-5-20,explains-scope-clause-on-5-20 | pass |
| neo4j-library-circulation-loader-and-branch-report-queries | FAIL:explains-loan-merge-duplicates,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | FAIL:finds-loan-merge-duplicates,explains-loan-merge-duplicates | pass |
| neo4j-local-news-social-api-publish-and-timeline | pass | pass | pass | pass |
| neo4j-member-erasure-job-after-the-big-account-memory-fix | pass | pass | pass | pass |
| neo4j-merchandising-admin-handlers-for-categories-and-brands | pass | pass | pass | pass |
| neo4j-parts-catalogue-sku-migration-and-its-ledger | pass | pass | pass | pass |
| neo4j-rain-gauge-ingest-asks-for-batch-status | pass | pass | pass | pass |
| neo4j-router-peering-ingest-from-device-reports-and-noc-queries | pass | pass | pass | pass |
| neo4j-sensor-heartbeat-consumers-and-fleet-dashboard | pass | pass | FAIL:finds-concurrent-merge-unconstrained | pass |
| neo4j-session-statements-and-the-five-minute-sweeper | pass | pass | pass | pass |
| neo4j-telemetry-retention-job-and-the-meter-dashboards | pass | pass | FAIL:finds-purge-in-one-transaction,explains-purge-in-one-transaction | pass |
| neo4j-timetable-queries-tested-on-compose-and-deployed-by-helm | pass | pass | FAIL:explains-scope-clause-on-prod-5-21 | pass |
| neo4j-trail-reports-migration-runner-and-a-segment-backfill | pass | pass | FAIL:explains-batched-backfill-in-explicit-transaction | pass |
| neo4j-water-meter-ingest-with-sixteen-consumers-and-a-review-comment | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass |
| networkx-bastion-reachability-tool-walks-jump-hosts-by-hand | pass | pass | pass | pass |
| networkx-bus-journey-planner-loads-segments-csv-with-blank-minute-cells | pass | pass | pass | pass |
| networkx-ci-pipeline-validator-with-a-handwritten-loop-check | pass | pass | pass | pass |
| networkx-davis-attendance-loaded-into-a-plain-graph-for-co-attendance | pass | pass | pass | pass |
| networkx-festival-seat-capacity-max-flow-over-a-day-of-services | pass | pass | pass | pass |
| networkx-file-share-access-check-over-nested-groups | pass | pass | pass | pass |
| networkx-florentine-marriage-blocs-reach-table | pass | pass | pass | pass |
| networkx-florentine-marriage-network-seminar-package | pass | pass | pass | pass |
| networkx-florentine-worksheet-lists-every-marriage-route | pass | pass | FAIL:no-critical-or-high | pass |
| networkx-fraud-ring-linker-and-a-colleague-on-contracted-nodes | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| networkx-grocery-promise-zones-from-a-reachable-within-cutoff | pass | pass | pass | pass |
| networkx-karate-club-cohesion-report-with-its-own-clustering | pass | pass | pass | pass |
| networkx-karate-inner-circle-from-a-hand-counted-tightness-score | pass | pass | pass | pass |
| networkx-karate-introduction-chains-on-the-weighted-club-graph | pass | pass | pass | pass |
| networkx-karate-referral-chains-listed-up-to-three-links | pass | pass | pass | pass |
| networkx-karate-tie-distance-dijkstra-written-by-hand | pass | pass | pass | pass |
| networkx-les-miserables-coappearance-stats-page | pass | pass | pass | pass |
| networkx-lesmis-poster-ranks-characters-by-two-step-reach | pass | pass | pass | pass |
| networkx-lesmis-separation-widget-built-on-all-simple-paths | pass | pass | pass | pass |
| networkx-lesmis-static-site-finds-chains-in-browser-javascript | pass | pass | pass | pass |
| networkx-lesmis-study-guide-bonds-counted-from-a-chapter-log | pass | pass | pass | pass |
| networkx-running-club-friend-suggestions-and-interest-nodes | pass | pass | pass | pass |
| networkx-southern-women-attendance-module-for-a-seminar-handout | pass | pass | pass | pass |
| networkx-southern-women-attendance-package-and-a-projection-request | pass | pass | pass | pass |
| networkx-southern-women-events-and-a-request-to-drop-the-event-nodes | pass | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass |
| networkx-supplier-network-dedupe-and-the-single-source-report | pass | pass | pass | pass |
| networkx-water-main-network-loader-edits-and-contamination-trace | pass | pass | pass | pass |
| networkx-wiki-cleanup-bot-groups-pages-with-its-own-cluster-search | pass | pass | pass | pass |
| sql-build-provenance-schema-and-a-foreign-key-lint-report | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass |
| sql-knowledge-graph-entity-aliases-and-mention-resolution | pass | pass | pass | pass |
| sql-postgres-crawl-entity-graph-nightly-purge-and-foreign-keys | pass | pass | pass | pass |
| sql-postgres-expense-approver-delegation-chain-and-a-blocked-pr | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| sql-postgres-supplier-map-tier-query-for-the-risk-page | pass | pass | pass | pass |
| sql-professional-network-schema-with-recommendations-endorsements-and-account-deletion | pass | pass | pass | pass |
| sql-referral-club-member-lookup-sponsor-chain-and-a-query-linter | pass | pass | pass | pass |
| sql-storefront-category-tree-placements-and-slug-renames | pass | pass | pass | pass |
| sqlite-access-groups-schema-and-the-provisioning-code | pass | pass | pass | pass |
| sqlite-approval-delegation-walk-and-team-rollup-queries | pass | pass | pass | pass |
| sqlite-association-mentoring-graph-member-lookup-and-mention-resolver | pass | pass | pass | pass |
| sqlite-audience-estimate-queries-after-a-lint-cleanup | pass | pass | pass | pass |
| sqlite-bom-compliance-queries-and-two-sql-lint-warnings | pass | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass |
| sqlite-bookmark-tag-graph-related-tags-page | pass | pass | pass | pass |
| sqlite-bus-network-snapshot-build-and-a-colleague-review-on-foreign-keys | pass | pass | pass | pass |
| sqlite-citation-graph-reference-importer-and-ranking-export | pass | pass | pass | pass |
| sqlite-city-transit-routes-stops-and-journey-planner | pass | pass | pass | pass |
| sqlite-community-follow-graph-handle-lookup-and-a-contractor-proposal | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass |
| sqlite-crm-intro-graph-person-lookup-and-mutual-connections | pass | pass | pass | pass |
| sqlite-family-tree-app-connection-helper-and-parent-links | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass |
| sqlite-fibre-plant-closures-spans-and-the-outage-notification-query | pass | pass | pass | pass |
| sqlite-follow-graph-audience-query-and-a-ci-lint-failure | pass | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass |
| sqlite-gazetteer-place-merge-and-a-rewrite-proposal | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| sqlite-help-centre-topic-tree-article-listing-and-a-closure-table-proposal | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| sqlite-kiosk-fewest-stops-query-carries-a-visited-path-string | pass | pass | pass | pass |
| sqlite-microblog-follow-graph-and-mention-resolver | pass | pass | pass | pass |
| sqlite-notes-tag-graph-autocomplete-and-review-comments | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| sqlite-org-chart-repo-with-a-nightly-hr-import-and-eight-reports | pass | pass | pass | pass |
| sqlite-package-registry-db-layer-and-a-lint-report-on-its-foreign-keys | pass | pass | FAIL:says-sound-foreign-keys-are-on | pass |
| sqlite-plant-equipment-dependency-graph-web-app-and-erp-sync-job | pass | pass | pass | pass |
| sqlite-road-network-regional-loader-and-its-lint-suppressions | pass | pass | pass | pass |
| sqlite-service-catalogue-connection-helper-and-decommission-command | pass | pass | FAIL:explains-pragma-inside-transaction | pass |
| sqlite-staff-directory-reporting-lines-imported-from-hr | pass | pass | pass | pass |
| sqlite-storefront-category-graph-migrations-and-breadcrumb-queries | FAIL:no-critical-or-high,says-sound-triggers-keep-it-acyclic,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass |
| sqlite-taskboard-card-tree-with-subtasks-labels-and-comments | pass | pass | pass | pass |
| sqlite-team-drive-folder-tree-stored-by-path-and-the-folder-view | pass | pass | pass | pass |
| sqlite-trail-map-migrations-and-route-planner | pass | pass | pass | pass |
| sqlite-trail-network-area-retirement-script | pass | pass | pass | pass |
| sqlite-transit-hop-rebuild-and-a-code-scanner-high | FAIL:no-critical-or-high,says-sound-rebuild-delete-is-right,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass |
| sqlite-wiki-link-store-and-the-popular-pages-sidebar | pass | pass | pass | pass |
