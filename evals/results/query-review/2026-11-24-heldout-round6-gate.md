## query-review / heldout / 2026-11-24

Models: haiku, sonnet. Skill version: 1c913119c8fc.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 224/240 (93%, 95% CI 89% to 96%) | 55/140 (39%, 95% CI 32% to 48%) |
| skill | 234/240 (98%, 95% CI 95% to 99%) | 124/140 (89%, 95% CI 82% to 93%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 108/120 (90%, 95% CI 83% to 94%) |
| baseline/sonnet | 116/120 (97%, 95% CI 92% to 99%) |
| skill/haiku | 117/120 (98%, 95% CI 93% to 99%) |
| skill/sonnet | 117/120 (98%, 95% CI 93% to 99%) |

Paired by case, all models: skill better on 10, baseline better on 1, tied on 109; sign test p = 0.0117.
Paired by case, haiku: 10 / 1 / 109 ties; p = 0.0117.
Paired by case, sonnet: 3 / 2 / 115 ties; p = 1.0.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 18642.0 tokens / 27.0 s; skill 22695.0 tokens / 45.8 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| cypher-check-olt-merge-script-before-reconciliation | pass | pass | pass | pass |
| cypher-ci-explain-check-on-imprint-loader | pass | pass | pass | pass |
| cypher-ci-findings-on-vhs-retirement-change | FAIL:title-move-stays-merge,plan-check-stated | pass | pass | pass |
| cypher-ci-lint-red-on-coop-membership-loader | pass | pass | pass | pass |
| cypher-ci-lint-red-on-loans-loader | pass | pass | pass | pass |
| cypher-cylint-red-on-provenance-loader | pass | pass | pass | pass |
| cypher-delete-label-exit-recordings-on-blue | FAIL:label-exit-recordings-deleted-in-batches,plan-check-stated | pass | pass | pass |
| cypher-drop-2019-tracking-frames-on-primary | FAIL:bounded-purge-handed-back,plan-check-stated | pass | pass | FAIL:bounded-purge-handed-back |
| cypher-drop-inactive-supporter-memberships-change | pass | pass | pass | pass |
| cypher-evict-cold-blobs-on-cas-request | pass | pass | pass | pass |
| cypher-finish-stop-sequence-migration | pass | pass | pass | pass |
| cypher-fix-crop-planting-migration-for-reapply | pass | pass | pass | pass |
| cypher-fold-alias-stub-packages-change | pass | pass | pass | pass |
| cypher-follow-up-for-failed-caps-migration | pass | pass | pass | pass |
| cypher-label-organic-lots-on-trace-request | pass | pass | pass | pass |
| cypher-lint-red-on-assign-trailer-to-door | pass | pass | pass | pass |
| cypher-lint-red-on-splice-loss-backfill | pass | FAIL:lint-green-the-repo-way,plan-check-stated | pass | pass |
| cypher-mark-dormant-water-accounts-change | pass | pass | pass | pass |
| cypher-mark-inactive-shippers-change | pass | pass | pass | pass |
| cypher-pr-comment-on-squad-loader-merge | pass | pass | pass | pass |
| cypher-pr-comment-on-summer-season-close | pass | pass | pass | pass |
| cypher-pr-comment-on-upstream-port-trace | pass | pass | pass | pass |
| cypher-pr-review-on-hollins-papers-closure | pass | pass | pass | pass |
| cypher-purge-cancelled-forward-contracts-on-atlas | pass | pass | pass | pass |
| cypher-purge-ceased-circuits-change | pass | pass | pass | pass |
| cypher-purge-old-ci-builds-change | pass | pass | pass | pass |
| cypher-relabel-decommissioned-cell-sites-on-ran | FAIL:migration-relabels-only-decommissioned,plan-check-stated | pass | pass | pass |
| cypher-remove-expired-excerpts-on-feed | pass | pass | pass | pass |
| cypher-remove-load-test-viewers-on-reel-01 | FAIL:synthetic-viewers-deleted-within-entity-limit,plan-check-stated | pass | pass | pass |
| cypher-rerun-box-to-shelf-migration | pass | pass | pass | pass |
| cypher-rerun-director-migration-after-failover | pass | pass | pass | pass |
| cypher-rerun-hydrant-flow-test-import-after-failure | pass | pass | pass | pass |
| cypher-rerun-maintained-by-migration-0031 | pass | pass | pass | pass |
| cypher-retry-cabinet-feed-migration-after-timeout | pass | pass | pass | pass |
| cypher-review-asks-hop-cap-on-chute-reach | pass | pass | pass | pass |
| cypher-review-comments-on-checkin-purge | pass | pass | pass | pass |
| cypher-review-on-backhaul-link-loader | pass | pass | pass | pass |
| cypher-review-on-cup-archive-change | pass | pass | pass | pass |
| cypher-review-on-eu-mirror-retirement-change | pass | pass | pass | pass |
| cypher-review-on-expired-booking-purge | pass | pass | pass | pass |
| cypher-review-on-light-maintenance-contract-handover | pass | pass | pass | pass |
| cypher-reviewer-wants-distinct-dropped-in-shutoff-letters | pass | pass | pass | pass |
| cypher-reviewer-wants-one-merge-in-park-facility-loader | pass | pass | pass | pass |
| cypher-revoke-galley-access-after-publication | pass | pass | pass | pass |
| cypher-tag-cast-iron-mains-on-grid-request | pass | pass | pass | pass |
| cypher-unassign-pitches-of-lapsed-permits-change | pass | pass | pass | pass |
| cypher-web-412-unpublish-deaccessioned-objects | pass | pass | pass | pass |
| cypher-withdraw-elm-street-items-on-shared | pass | pass | pass | pass |
| cypher-write-off-lost-pallets-on-wh-east | FAIL:batched-write-off-handed-back,plan-check-stated | FAIL:batched-write-off-handed-back,plan-check-stated | pass | pass |
| networkx-fold-duplicate-manholes-before-solver-run | pass | pass | pass | pass |
| networkx-merge-duplicate-artist-nodes | pass | pass | pass | pass |
| networkx-merge-duplicate-authority-records | pass | pass | pass | pass |
| networkx-merge-duplicate-grounds-in-travel-planner | pass | pass | pass | pass |
| networkx-merge-duplicate-traders-in-grain-flows | pass | pass | pass | pass |
| networkx-merge-hub-aliases-in-lane-graph | pass | pass | pass | pass |
| networkx-prune-unused-legacy-targets | pass | pass | pass | pass |
| sqlite-annual-opening-of-closed-files | pass | pass | pass | pass |
| sqlite-cat-902-purge-withdrawn-releases | pass | pass | pass | pass |
| sqlite-ci-lint-on-allergen-carry-rebuild | pass | pass | pass | pass |
| sqlite-ci-lint-on-authority-lineage-job | pass | pass | pass | pass |
| sqlite-ci-lint-red-on-storm-catchment-query | pass | pass | pass | pass |
| sqlite-clear-ceased-circuit-hops-on-core | pass | pass | pass | pass |
| sqlite-clear-old-crate-scans-on-stalls | FAIL:change-file-handed-back | pass | pass | pass |
| sqlite-clear-old-loan-links-on-registry | FAIL:change-file-handed-back | pass | pass | pass |
| sqlite-clear-sim-pick-edges-request | pass | pass | pass | pass |
| sqlite-clear-training-sale-bids-on-train | pass | pass | pass | pass |
| sqlite-clear-training-session-work-orders-on-classroom | pass | pass | pass | FAIL:classroom-cleared |
| sqlite-drop-compilation-chart-entries-on-mirror | pass | pass | pass | pass |
| sqlite-drop-lapsed-supplier-approvals-job | pass | pass | pass | pass |
| sqlite-drop-retired-antenna-models-from-catalogue | pass | pass | pass | pass |
| sqlite-drop-retired-trailers-job | pass | pass | pass | pass |
| sqlite-expire-stale-building-permits-change | pass | pass | pass | pass |
| sqlite-finish-cable-adjacency-backfill-after-crash | pass | pass | pass | pass |
| sqlite-finish-head-to-head-backfill-after-timeout | pass | pass | pass | pass |
| sqlite-finish-parcel-leg-backfill-after-crash | pass | pass | pass | pass |
| sqlite-finish-performer-edges-backfill | pass | pass | pass | pass |
| sqlite-finish-sbom-component-backfill-after-kill | FAIL:finishes-last-nights-run,safe-to-kill-and-rerun | pass | pass | pass |
| sqlite-finish-ships-to-backfill-after-crash | FAIL:reports-edges-written | pass | FAIL:reports-edges-written | pass |
| sqlite-finish-translator-share-backfill | pass | pass | pass | pass |
| sqlite-fold-duplicate-bus-stops-after-feed-reimport | pass | pass | pass | pass |
| sqlite-fold-duplicate-clubs-from-county-import | pass | pass | pass | pass |
| sqlite-jobcheck-red-on-released-holds-purge | pass | pass | pass | pass |
| sqlite-lic-88-expired-availability-change | pass | pass | pass | pass |
| sqlite-mark-dormant-lanes-on-core | pass | pass | pass | pass |
| sqlite-merge-double-registered-vendors | pass | pass | pass | pass |
| sqlite-merge-duplicate-bin-locations-job | pass | pass | pass | pass |
| sqlite-merge-duplicate-pop-sites-from-second-feed | pass | pass | pass | pass |
| sqlite-merge-matched-contributor-duplicates | pass | pass | pass | pass |
| sqlite-merge-migrated-maintainer-accounts | pass | pass | pass | pass |
| sqlite-merge-reconciled-maker-records | pass | pass | pass | pass |
| sqlite-move-nx4-grid-to-epping-on-fieldsync | pass | pass | pass | pass |
| sqlite-move-zone-3-hydrants-after-pressure-zone-merge | pass | pass | pass | pass |
| sqlite-pr-comment-on-transitive-dependents-query | pass | pass | pass | pass |
| sqlite-purge-closed-311-requests-on-civic | pass | pass | pass | pass |
| sqlite-purge-expired-site-access-grants | pass | pass | pass | pass |
| sqlite-purge-itemless-bib-records-job | pass | pass | pass | pass |
| sqlite-purge-lapsed-swim-memberships-job | pass | pass | pass | pass |
| sqlite-purge-last-season-registrations-on-regdb | FAIL:change-file-handed-back,change-file-named-the-repo-way | pass | pass | pass |
| sqlite-purge-ocr-v1-access-copies-on-vault | FAIL:change-file-handed-back | FAIL:change-file-handed-back | FAIL:change-file-handed-back | FAIL:change-file-handed-back |
| sqlite-purge-old-pipeline-runs-on-prod-request | pass | pass | pass | pass |
| sqlite-purge-retired-commodities-job | pass | pass | pass | pass |
| sqlite-purge-unreleased-old-artifacts-job | pass | pass | pass | pass |
| sqlite-quarantine-runner-builds-on-vault-request | pass | pass | pass | pass |
| sqlite-relabel-august-friendlies-on-staging | pass | pass | pass | pass |
| sqlite-relabel-legacy-olt-models-on-inventory | pass | FAIL:relabel-applied-to-the-dev-copy | FAIL:relabel-applied-to-the-dev-copy | pass |
| sqlite-remove-retired-lift-stations-job | pass | pass | pass | pass |
| sqlite-remove-retired-referees-job | pass | pass | pass | pass |
| sqlite-remove-timing-test-entries-on-hub-request | pass | pass | pass | pass |
| sqlite-rerun-bin-route-link-job-after-lock-timeout | pass | pass | pass | pass |
| sqlite-review-comment-on-lineage-rebuild | pass | pass | pass | pass |
| sqlite-review-comments-on-closed-market-quote-purge | pass | pass | pass | pass |
| sqlite-review-comments-on-reading-list-rollover | pass | pass | pass | pass |
| sqlite-review-on-preview-build-purge-job | pass | pass | pass | pass |
| sqlite-run-cancelled-appointment-purge-on-sandbox | pass | pass | pass | pass |
| sqlite-run-spdx-rename-on-sandbox | pass | pass | pass | pass |
| sqlite-sql-lint-red-on-switching-domain-query | pass | pass | pass | pass |
| sqlite-sqlcheck-red-on-credits-loader | pass | pass | pass | pass |
| sqlite-sqlcheck-red-on-pathway-rebuild | pass | pass | pass | pass |
| sqlite-tidy-paperback-formats-on-dev | pass | pass | pass | pass |
| sqlite-tracking-retention-purge-change | pass | pass | pass | pass |
