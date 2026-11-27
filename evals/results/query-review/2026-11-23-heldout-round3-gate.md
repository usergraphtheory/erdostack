## query-review / heldout / 2026-11-23

Models: haiku, sonnet. Skill version: 77832fa71a31.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 147/160 (92%, 95% CI 87% to 95%) | 52/134 (39%, 95% CI 31% to 47%) |
| skill | 152/160 (95%, 95% CI 90% to 97%) | 122/134 (91%, 95% CI 85% to 95%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 69/80 (86%, 95% CI 77% to 92%) |
| baseline/sonnet | 78/80 (98%, 95% CI 91% to 99%) |
| skill/haiku | 75/80 (94%, 95% CI 86% to 97%) |
| skill/sonnet | 77/80 (96%, 95% CI 90% to 99%) |

Paired by case, all models: skill better on 8, baseline better on 3, tied on 69; sign test p = 0.2266.
Paired by case, haiku: 8 / 2 / 70 ties; p = 0.1094.
Paired by case, sonnet: 1 / 2 / 77 ties; p = 1.0.
Regressions (baseline always passed, skill never did): sqlite-purge-links-to-deleted-items.
Cost, median per run: baseline 18483.5 tokens / 26.4 s; skill 22745.5 tokens / 36.9 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| cypher-abandoned-carts-cleanup-change | pass | pass | pass | pass |
| cypher-backfill-accession-year-migration | pass | pass | pass | pass |
| cypher-batch-request-on-catalog-cutover | pass | pass | pass | pass |
| cypher-batch-request-on-code-expiry | pass | pass | pass | pass |
| cypher-batch-the-api-key-cleanup | pass | pass | pass | pass |
| cypher-drop-legacy-sku-on-prod-tonight | pass | pass | pass | pass |
| cypher-finish-gauge-basin-backfill | pass | pass | pass | pass |
| cypher-finish-play-count-fold-after-crash | pass | pass | pass | pass |
| cypher-history-panel-paging | pass | pass | pass | pass |
| cypher-hourly-employment-copy-job | FAIL:copy-is-idempotent,plan-check-stated | pass | FAIL:copy-is-idempotent | pass |
| cypher-hut-planner-suggests-unreachable-huts | pass | pass | pass | pass |
| cypher-leaderboard-csv-short-of-team | pass | pass | pass | pass |
| cypher-lint-deprecation-on-projects-page | FAIL:says-the-scope-clause-would-not-parse,query-text-untouched,build-made-green-in-the-lint-config,plan-check-stated | pass | pass | pass |
| cypher-mark-dormant-members-job | pass | pass | pass | pass |
| cypher-order-history-slow-on-account-page | pass | pass | pass | pass |
| cypher-placeholder-purge-detach-question | pass | pass | pass | pass |
| cypher-popular-this-week-empty-for-most-cuisines | pass | pass | pass | pass |
| cypher-price-loader-duplicate-worry | pass | pass | pass | pass |
| cypher-replay-device-reports-loader | pass | FAIL:devices-still-found-by-serial,older-report-never-overwrites-newer-state,newer-reports-still-applied,plan-check-stated | pass | FAIL:devices-still-found-by-serial,older-report-never-overwrites-newer-state,newer-reports-still-applied |
| cypher-retire-similar-tracks-change | pass | pass | pass | pass |
| cypher-retry-of-crashed-status-migration | pass | pass | pass | pass |
| cypher-reviewer-drops-language-prefix | pass | pass | pass | pass |
| cypher-reviewer-moves-optional-match-filter | pass | pass | pass | pass |
| cypher-reviewer-says-subquery-limit-is-global | FAIL:three-newest-for-every-restaurant,says-the-limit-is-per-restaurant,query-text-untouched,plan-check-stated | pass | pass | pass |
| cypher-reviewer-says-toupper-blocks-sku-index | pass | pass | pass | pass |
| cypher-reviewer-wants-unique-listeners-on-royalties | pass | pass | pass | pass |
| cypher-room-import-second-campus | FAIL:room-identified-by-building-and-number | pass | FAIL:room-identified-by-building-and-number | pass |
| cypher-run-orcid-change-on-staging | pass | pass | pass | pass |
| cypher-seller-card-revenue-vs-payouts | pass | pass | pass | pass |
| cypher-sensor-card-empty-on-mobile | pass | pass | pass | pass |
| cypher-service-due-query-fails-on-staging | pass | pass | pass | pass |
| cypher-speed-up-station-loader | pass | pass | FAIL:loader-merges-on-the-station-code,loader-still-writes-every-column | pass |
| cypher-stage-clear-scope-question | pass | pass | pass | pass |
| cypher-undo-bad-import-on-prod | pass | pass | pass | pass |
| ladybug-budget-rollup-short-of-finance | pass | pass | pass | pass |
| ladybug-lab-feed-nearly-empty | pass | pass | pass | pass |
| ladybug-list-reach-double-of-headcount | pass | pass | pass | pass |
| ladybug-reviewer-says-count-drops-members | pass | pass | pass | pass |
| ladybug-reviewer-wants-undirected-approval-line | pass | pass | pass | pass |
| ladybug-withdrawal-impact-lists-unrelated-courses | pass | pass | pass | pass |
| networkx-cheapest-trip-search | pass | pass | pass | pass |
| networkx-connection-chain-panel | pass | pass | pass | pass |
| networkx-impacted-services-function | pass | pass | pass | pass |
| networkx-nearest-clinic-coverage-job | pass | pass | pass | pass |
| networkx-review-says-graph-copy-is-wasteful | pass | pass | pass | pass |
| networkx-review-says-trails-should-be-directed | pass | pass | pass | pass |
| networkx-review-wants-minutes-on-stops-badge | pass | pass | pass | pass |
| networkx-route-card-distance | pass | pass | pass | pass |
| sqlite-allergen-dishes-query | pass | pass | pass | pass |
| sqlite-apply-gazetteer-merge-batch | pass | pass | pass | pass |
| sqlite-backfill-reply-depth-column | pass | pass | pass | pass |
| sqlite-backfill-segment-junction-ids | pass | pass | pass | pass |
| sqlite-cascade-unit-retirement-backfill | pass | pass | pass | FAIL:commits-in-chunks |
| sqlite-ci-lint-red-on-invite-purge | pass | pass | pass | pass |
| sqlite-dedupe-bought-together-pairs | pass | pass | pass | pass |
| sqlite-empty-board-trash-job | FAIL:trash-emptied-with-attachments,returns-cards-deleted | pass | pass | pass |
| sqlite-finish-contact-archive-after-crash | FAIL:archive-finished-without-duplicates,safe-to-rerun-after-a-crash | pass | pass | pass |
| sqlite-mention-purge-count-vs-dashboard | pass | pass | pass | pass |
| sqlite-move-folder-for-q4-reorg | pass | pass | pass | pass |
| sqlite-mutuals-tab-query | FAIL:other-accounts-that-follow-back,plan-inspected-before-run | pass | pass | pass |
| sqlite-normalise-clickstream-weights-job | FAIL:commits-in-chunks | pass | FAIL:commits-in-chunks | pass |
| sqlite-plan-guard-flags-pedigree-walk | pass | pass | pass | pass |
| sqlite-pr-comment-on-dependency-edge-dedupe | pass | pass | pass | pass |
| sqlite-pr-comment-on-share-expiry-count | pass | pass | pass | pass |
| sqlite-prereq-credit-load-too-high | pass | pass | pass | pass |
| sqlite-purge-links-to-deleted-items | pass | pass | FAIL:exactly-the-dangling-links-removed,commits-in-chunks,returns-links-removed | FAIL:exactly-the-dangling-links-removed,returns-links-removed |
| sqlite-reattach-under-retired-locations | pass | pass | pass | pass |
| sqlite-redirect-resolver-query | pass | pass | pass | pass |
| sqlite-remove-silent-mesh-devices | FAIL:silent-devices-and-their-links-gone,returns-devices-removed | pass | pass | pass |
| sqlite-retire-sdk-v1-doc-pages | pass | pass | pass | pass |
| sqlite-review-comment-on-territory-reassign | pass | pass | pass | pass |
| sqlite-review-comment-on-withdrawn-citations-purge | FAIL:says-deletes-are-already-batched,source-untouched | FAIL:says-deletes-are-already-batched,source-untouched | pass | pass |
| sqlite-review-says-ledger-rollup-can-loop | FAIL:says-the-chart-cannot-loop,source-untouched | pass | pass | pass |
| sqlite-review-says-release-closure-misses-deps | pass | pass | pass | pass |
| sqlite-review-wants-not-in-for-gc-report | pass | pass | pass | pass |
| sqlite-review-wants-union-all-in-recalc | pass | pass | pass | pass |
| sqlite-reviewer-wants-depth-cap-on-close-branch | pass | pass | pass | pass |
| sqlite-stop-neighbours-query | pass | pass | pass | pass |
| sqlite-thread-export-missing-messages | pass | pass | pass | pass |
| sqlite-would-create-cycle-query | pass | pass | pass | pass |
