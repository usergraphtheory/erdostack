## query-review / heldout / 2026-11-23

Models: haiku, sonnet. Skill version: b438725549a1.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 172/200 (86%, 95% CI 80% to 90%) | 83/154 (54%, 95% CI 46% to 62%) |
| skill | 187/200 (94%, 95% CI 89% to 96%) | 127/154 (82%, 95% CI 76% to 88%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 82/100 (82%, 95% CI 73% to 88%) |
| baseline/sonnet | 90/100 (90%, 95% CI 83% to 94%) |
| skill/haiku | 92/100 (92%, 95% CI 85% to 96%) |
| skill/sonnet | 95/100 (95%, 95% CI 89% to 98%) |

Paired by case, all models: skill better on 14, baseline better on 3, tied on 83; sign test p = 0.0127.
Paired by case, haiku: 12 / 2 / 86 ties; p = 0.0129.
Paired by case, sonnet: 8 / 3 / 89 ties; p = 0.2266.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 18283.5 tokens / 25.7 s; skill 22282.0 tokens / 40.0 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| cypher-booking-purge-orphan-question | pass | pass | pass | pass |
| cypher-ci-lint-red-on-gift-loader | pass | pass | pass | pass |
| cypher-clear-qa-accounts-on-prod-request | pass | FAIL:only-qa-accounts-in-batches,record-is-not-the-requested-statement | pass | pass |
| cypher-delete-pre-gun-test-reads | pass | pass | pass | pass |
| cypher-digest-subscription-cleanup-scope-question | FAIL:says-the-narrow-scope-is-deliberate,plan-check-stated | pass | pass | pass |
| cypher-drop-v1-links-on-main-request | FAIL:bounded-delete-of-v1-links-handed-back,plan-check-stated | pass | pass | pass |
| cypher-episode-slug-backfill-keeps-looping | pass | pass | pass | pass |
| cypher-finish-measured-by-move | FAIL:old-links-dropped-only-once-copied,plan-check-stated | FAIL:old-links-dropped-only-once-copied | FAIL:old-links-dropped-only-once-copied | FAIL:old-links-dropped-only-once-copied |
| cypher-hub-split-after-manual-run | pass | pass | pass | pass |
| cypher-imaged-label-and-loader-review | pass | pass | pass | pass |
| cypher-link-branches-to-delivery-zones | pass | pass | pass | pass |
| cypher-merge-synonym-taxa-script | FAIL:no-taxon-becomes-its-own-parent,plan-check-stated | FAIL:no-taxon-becomes-its-own-parent | pass | pass |
| cypher-pr-comment-on-cottage-listing-sync | pass | pass | pass | pass |
| cypher-pr-comment-on-partner-pairing-merge | FAIL:says-the-undirected-merge-is-right | pass | pass | pass |
| cypher-purge-trashed-albums-job | pass | FAIL:photos-in-another-album-kept,plan-check-stated | FAIL:photos-in-another-album-kept | pass |
| cypher-pushback-on-tier-reset-batching-comment | pass | pass | pass | pass |
| cypher-rate-cents-backfill-resume-change | FAIL:truncated-rates-corrected-too,plan-check-stated | pass | pass | FAIL:cents-rounded |
| cypher-retire-stale-gigs-change-review | FAIL:only-freelancers-emptied-by-this-change,plan-check-stated | FAIL:only-freelancers-emptied-by-this-change,plan-check-stated | FAIL:only-freelancers-emptied-by-this-change | FAIL:only-freelancers-emptied-by-this-change |
| cypher-retire-v1-star-ratings-changeset | pass | pass | pass | pass |
| cypher-review-drops-order-by-in-invoice-numbering | pass | pass | pass | pass |
| cypher-review-says-ping-purge-fails-in-migrate | pass | pass | pass | pass |
| cypher-review-wants-bigger-batches-on-draft-purge | pass | pass | pass | pass |
| cypher-review-wants-one-transaction-for-leg-weights | pass | pass | pass | pass |
| cypher-review-widens-released-reservation-purge | pass | pass | pass | pass |
| cypher-reviewer-nitpick-on-reading-history-purge | pass | pass | pass | pass |
| cypher-reviewer-says-account-purge-takes-shared-tvs | pass | pass | pass | pass |
| cypher-reviewer-says-bin-labels-collide | pass | pass | pass | pass |
| cypher-reviewer-says-distinct-is-wasted-in-recall-apply | pass | pass | pass | pass |
| cypher-reviewer-says-dock-update-deletes-null | pass | pass | pass | pass |
| cypher-reviewer-says-undirected-coauthor-merge-duplicates | pass | pass | pass | pass |
| cypher-reviewer-wants-grace-period-on-tag-sweep | pass | pass | pass | pass |
| cypher-reviewer-wants-managed-tx-in-migrate-tool | pass | pass | pass | pass |
| cypher-reviewer-wants-merge-in-visits-migration | pass | pass | pass | pass |
| cypher-rode-to-took-rename-before-release | FAIL:one-trip-per-ride | pass | pass | pass |
| cypher-seat-hold-sweep-and-manifest-lint | pass | pass | pass | pass |
| cypher-security-review-on-volunteer-profile-patch | pass | pass | pass | pass |
| cypher-semgrep-finding-on-collection-search | pass | pass | pass | pass |
| cypher-site-loader-add-power-column | pass | pass | pass | pass |
| cypher-spam-tag-purge-try-locally | pass | pass | pass | FAIL:only-unkept-spam-tags-removed |
| cypher-supplier-to-vendor-relabel-migration | pass | pass | pass | pass |
| cypher-undo-autoblock-misfire | pass | pass | pass | pass |
| cypher-vessel-loader-merge-key-question | pass | pass | pass | pass |
| cypher-weekly-ticket-archive-job | pass | pass | pass | pass |
| cypher-who-is-right-on-ringer-merge-key | FAIL:trainee-rows-go-to-the-trainer | pass | FAIL:trainee-rows-go-to-the-trainer | pass |
| ladybug-pr-comment-on-insurance-headcount | FAIL:every-player-counted,query-text-untouched | pass | pass | pass |
| ladybug-reviewer-calls-distinct-pointless-in-supplier-exposure | pass | pass | pass | pass |
| ladybug-reviewer-says-fibre-link-count-doubles | FAIL:each-link-counted-once | FAIL:each-link-counted-once | pass | pass |
| ladybug-reviewer-simplifies-case-history-paging | pass | pass | pass | pass |
| ladybug-reviewer-wants-distinct-in-invoice-total | pass | pass | pass | pass |
| ladybug-reviewer-wants-union-all-in-incident-notice | pass | pass | pass | pass |
| networkx-pr-comment-on-amendment-impact | pass | pass | pass | pass |
| networkx-review-drops-list-around-isolates | pass | pass | pass | pass |
| networkx-review-flags-zero-latency-cross-connects | pass | pass | pass | pass |
| networkx-review-says-ring-count-is-a-hack | pass | pass | pass | pass |
| networkx-review-says-sorter-routes-ignore-belt-direction | pass | pass | pass | pass |
| networkx-review-wants-has-edge-guard-on-lane-refresh | pass | pass | pass | pass |
| networkx-review-wants-multigraph-for-backbone | pass | pass | pass | pass |
| networkx-review-wants-weak-components-for-deadlocks | pass | pass | pass | pass |
| networkx-static-analysis-on-contact-degrees | pass | pass | pass | pass |
| sqlite-apply-bom-change-order-job | FAIL:commits-in-chunks | FAIL:commits-in-chunks | FAIL:commits-in-chunks | pass |
| sqlite-apply-thesaurus-reorg-moves | pass | pass | pass | pass |
| sqlite-archive-dormant-mentorships-job | pass | pass | pass | pass |
| sqlite-band-fix-and-cabrillo-import-review | pass | pass | pass | pass |
| sqlite-dedupe-crossmatch-pairs | pass | pass | FAIL:one-row-per-pair-flags-kept,returns-duplicates-removed | pass |
| sqlite-delete-closed-org-album-tree | pass | pass | pass | pass |
| sqlite-drop-weak-related-article-edges | pass | pass | pass | pass |
| sqlite-expire-stale-squad-links | pass | pass | pass | pass |
| sqlite-fill-dock-flow-shares-job | pass | pass | pass | pass |
| sqlite-finish-coview-build-after-crash | FAIL:weights-right-after-tonights-run,safe-to-rerun-after-a-crash | pass | FAIL:weights-right-after-tonights-run,safe-to-rerun-after-a-crash | FAIL:weights-right-after-tonights-run,reports-visits-processed,transactions-within-limit,safe-to-rerun-after-a-crash |
| sqlite-fold-portable-callsign-contacts | pass | pass | pass | pass |
| sqlite-merge-duplicate-varieties-run-with-tool | pass | pass | pass | pass |
| sqlite-perf-alarm-on-recall-fitment-lookup | FAIL:says-it-is-not-one-query-per-part,source-untouched | pass | pass | pass |
| sqlite-pr-comment-on-interaction-partners-panel | pass | FAIL:says-both-indexes-are-used,source-untouched | pass | pass |
| sqlite-pr-comment-on-not-in-route-cleanup | pass | pass | pass | pass |
| sqlite-pr-comment-on-outfall-catchment-query | pass | pass | pass | pass |
| sqlite-pr-comment-on-shiftmates-rebuild | FAIL:shiftmates-rebuilt-for-every-volunteer,says-both-directions-are-read,source-untouched | FAIL:shiftmates-rebuilt-for-every-volunteer,says-both-directions-are-read,source-untouched | pass | pass |
| sqlite-pr-comment-on-taxon-outline-export | FAIL:says-the-inner-order-by-shapes-the-outline,source-untouched | pass | pass | pass |
| sqlite-prune-orphan-import-notes | pass | pass | pass | pass |
| sqlite-purge-sockpuppet-vouches | pass | pass | pass | pass |
| sqlite-remove-dangling-mod-dependencies | pass | pass | pass | pass |
| sqlite-rerun-worry-on-lane-capacity-conversion | pass | pass | pass | pass |
| sqlite-retired-fibre-purge-and-lint-bot | pass | pass | pass | pass |
| sqlite-review-asks-hop-cap-on-herd-trace | pass | pass | pass | pass |
| sqlite-review-comment-on-aisle-decommission-job | pass | pass | pass | pass |
| sqlite-review-comment-on-class-paths-purge | pass | pass | pass | pass |
| sqlite-review-comment-on-terminal-feeder-capacity | pass | pass | pass | pass |
| sqlite-review-says-buddy-purge-misreads-epoch-times | pass | pass | pass | pass |
| sqlite-review-says-closed-account-sweep-is-one-transaction | pass | pass | pass | pass |
| sqlite-review-says-downline-count-can-loop | pass | pass | pass | pass |
| sqlite-review-says-fanout-cone-can-loop | FAIL:cone-right-for-every-input | FAIL:cone-right-for-every-input | pass | pass |
| sqlite-review-says-offset-paging-skips-promos | pass | pass | pass | pass |
| sqlite-review-says-token-purge-cascades | FAIL:purges-exactly-the-tokens-unused-at-start,says-the-list-is-fixed-at-start,source-untouched | pass | FAIL:says-the-list-is-fixed-at-start | pass |
| sqlite-review-says-windowed-dedupe-misses-pairs | pass | pass | pass | pass |
| sqlite-review-wants-incremental-lift-reach-job | pass | pass | pass | pass |
| sqlite-review-wants-leaver-anonymiser-atomic | pass | pass | pass | pass |
| sqlite-review-wants-one-transaction-for-disposals | pass | pass | pass | pass |
| sqlite-revoke-shares-under-board-folder | pass | pass | pass | pass |
| sqlite-seed-starter-flow-graphs | pass | pass | pass | pass |
| sqlite-test-fleet-purge-via-make | pass | pass | pass | pass |
| sqlite-undo-double-decay-request | pass | pass | pass | pass |
