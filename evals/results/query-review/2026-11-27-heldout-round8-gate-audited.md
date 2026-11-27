## query-review / heldout / 2026-11-27

Models: haiku, sonnet. Skill version: 7aef902e8811.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 209/240 (87%, 95% CI 82% to 91%) | 120/176 (68%, 95% CI 61% to 75%) |
| skill | 231/240 (96%, 95% CI 93% to 98%) | 149/176 (85%, 95% CI 79% to 89%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 92/120 (77%, 95% CI 68% to 83%) |
| baseline/sonnet | 117/120 (98%, 95% CI 93% to 99%) |
| skill/haiku | 113/120 (94%, 95% CI 88% to 97%) |
| skill/sonnet | 118/120 (98%, 95% CI 94% to 100%) |

Paired by case, all models: skill better on 29, baseline better on 6, tied on 85; sign test p = 0.0001.
Paired by case, haiku: 27 / 6 / 87 ties; p = 0.0003.
Paired by case, sonnet: 2 / 1 / 117 ties; p = 1.0.
Regressions (baseline always passed, skill never did): cypher-delete-freight-import-test-trains-on-dev.
Cost, median per run: baseline 18961.0 tokens / 22.6 s; skill 23758.0 tokens / 33.3 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| cypher-archive-2024-hydrant-flushing-orders-on-gis | pass | pass | pass | pass |
| cypher-archive-2025-seed-lots-coop-on-catalogue | pass | pass | pass | pass |
| cypher-archive-decommissioned-weather-stations-on-ingest | pass | pass | pass | pass |
| cypher-archive-pre-2020-coop-leavers-on-prod | FAIL:bounded-relabel-handed-back,change-file-named-the-repo-way | pass | pass | pass |
| cypher-backfill-bin-collection-days-on-crewlink | pass | pass | pass | pass |
| cypher-clear-past-conference-bookings-on-prod | FAIL:change-file-handed-back,change-file-named-the-repo-way | pass | pass | pass |
| cypher-clear-practice-coop-ballot-votes-on-scratch | pass | pass | pass | pass |
| cypher-clear-practice-parking-pcns-on-training | pass | pass | pass | pass |
| cypher-clear-simulated-fibre-faults-on-dev | pass | pass | pass | pass |
| cypher-clear-stale-vet-due-reminders-on-prod | FAIL:bounded-clear-handed-back,change-file-named-the-repo-way,plan-check-stated | pass | pass | pass |
| cypher-clear-trainee-seed-offers-on-practice | pass | pass | pass | pass |
| cypher-close-ashby-canal-locks-on-sandbox | pass | pass | pass | pass |
| cypher-close-moorside-bus-stops-on-dev | pass | pass | pass | pass |
| cypher-delete-2024-chess-online-arenas-on-ratings | pass | pass | pass | pass |
| cypher-delete-2024-pantry-volunteer-shifts-on-west | pass | pass | pass | pass |
| cypher-delete-demo-theatre-performances-on-sandbox | pass | pass | pass | pass |
| cypher-delete-expired-casualty-contacts-rescue-on-incidentlog | pass | pass | pass | pass |
| cypher-delete-freight-import-test-trains-on-dev | pass | pass | FAIL:test-trains-deleted-on-dev | FAIL:test-trains-deleted-on-dev |
| cypher-delete-old-parking-sensor-events-on-kerbsense | FAIL:bounded-delete-handed-back,change-file-named-the-repo-way,plan-check-stated | pass | pass | pass |
| cypher-delete-pre-october-forecast-runs-on-wxcore | FAIL:change-file-handed-back,change-file-named-the-repo-way,plan-check-stated | pass | pass | pass |
| cypher-delete-removed-backflow-test-reports-on-xconn | pass | pass | pass | pass |
| cypher-delete-simulated-casualties-rescue-on-dev | pass | pass | FAIL:simulated-casualties-deleted-on-dev | pass |
| cypher-delete-test-gedcom-import-people-on-scratch | pass | pass | FAIL:gedtest-people-deleted-on-scratch | pass |
| cypher-delete-trn1124-room-inspections-on-hk-sandbox | pass | pass | pass | pass |
| cypher-drop-pre-term-bus-pings-on-depot | FAIL:bounded-purge-handed-back,change-file-named-the-repo-way,plan-check-stated | pass | pass | pass |
| cypher-drop-unrenewed-plot-waitlist-entries-on-plots | pass | pass | pass | pass |
| cypher-expire-unclaimed-pantry-referrals-on-hub | pass | pass | pass | pass |
| cypher-flag-medtech-overdue-safety-tests-on-devices | pass | pass | pass | pass |
| cypher-flag-sb2209-humidity-sensors-on-registry | FAIL:change-file-handed-back,change-file-named-the-repo-way | pass | pass | pass |
| cypher-label-e2-e3-bikes-as-ebike-on-dev | pass | pass | pass | pass |
| cypher-label-lapsed-vet-clients-on-prod | FAIL:lapsed-label-change-handed-back,change-file-named-the-repo-way | pass | pass | pass |
| cypher-make-msc-admissions-offers-on-sandbox | pass | pass | FAIL:offers-made-on-sandbox | pass |
| cypher-mark-phase3-fibre-premises-ready-on-spine | pass | pass | pass | pass |
| cypher-merge-duplicate-library-works-on-lcn | pass | pass | pass | pass |
| cypher-move-freight-consignments-off-6m42-on-freightline | pass | pass | pass | pass |
| cypher-move-fx-test-farms-to-ellerby-coop-on-scratch | pass | pass | pass | pass |
| cypher-move-gallery-4-museum-objects-to-store-b | pass | pass | pass | pass |
| cypher-move-garden-bins-to-thursday-round-on-sandbox | pass | pass | pass | pass |
| cypher-move-medtech-ward-7b-devices-on-scratch | pass | pass | pass | pass |
| cypher-move-t-310-conference-bookings-to-t-318-on-sandbox | pass | pass | FAIL:bookings-moved-on-sandbox | pass |
| cypher-move-theatre-bookings-to-rescheduled-matinee-on-tickets | pass | pass | pass | pass |
| cypher-purge-closed-fibre-faults-on-netgraph | FAIL:bounded-purge-handed-back,change-file-named-the-repo-way,plan-check-stated | pass | pass | pass |
| cypher-purge-expired-boat-licences-on-moorings | pass | FAIL:bounded-purge-handed-back,record-is-not-the-requested-statement,change-file-named-the-repo-way,plan-check-stated | pass | pass |
| cypher-purge-medtech-condemned-devices-on-cmdb | FAIL:bounded-purge-handed-back,change-file-named-the-repo-way,plan-check-stated | pass | pass | pass |
| cypher-purge-old-bin-lift-events-on-depot | pass | pass | pass | pass |
| cypher-purge-old-borrowing-history-on-circ | pass | pass | pass | pass |
| cypher-purge-pager-test-callouts-rescue-on-live | FAIL:bounded-purge-handed-back,change-file-named-the-repo-way | pass | pass | pass |
| cypher-purge-pre-2020-parking-pcns-on-civic | pass | pass | pass | pass |
| cypher-purge-pre-2024-bike-rides-on-hub | FAIL:change-file-handed-back,change-file-named-the-repo-way,plan-check-stated | pass | pass | pass |
| cypher-purge-pre-june-housekeeping-tasks-on-live | FAIL:change-file-handed-back,change-file-named-the-repo-way | pass | pass | pass |
| cypher-purge-rejected-ancestry-hints-on-prod | pass | pass | pass | pass |
| cypher-rehome-st-12-bikes-to-st-40-on-prod | pass | pass | pass | pass |
| cypher-remove-cancelled-chess-congress-pairings-on-prod | FAIL:bounded-delete-handed-back,change-file-named-the-repo-way,tried-on-replay | pass | pass | pass |
| cypher-remove-loadgen-vet-appointments-on-dev | pass | pass | FAIL:loadgen-appointments-deleted-on-dev | pass |
| cypher-remove-test-museum-accessions-on-sandbox | pass | pass | pass | pass |
| cypher-tag-inactive-chess-players-on-register | pass | pass | pass | pass |
| cypher-tag-north-pantries-winter-hours-on-training | pass | pass | pass | pass |
| cypher-tag-reference-library-items-on-sandbox | pass | pass | pass | pass |
| cypher-withdraw-failed-seed-lots-on-library | pass | pass | pass | pass |
| cypher-withdraw-missed-condition-admissions-offers-on-prod | pass | pass | pass | pass |
| sqlite-archive-2023-24-grain-contracts-coop-on-prod | pass | pass | pass | pass |
| sqlite-archive-2024-chess-games-on-arbiter | FAIL:change-file-handed-back,change-file-named-the-repo-way,tried-on-spare | pass | pass | pass |
| sqlite-archive-2025-conference-sessions-on-prod | pass | pass | pass | pass |
| sqlite-archive-pre-2020-weather-stations-on-scratch | pass | pass | pass | pass |
| sqlite-archive-superseded-census-transcriptions-on-register | pass | pass | pass | pass |
| sqlite-backfill-farm-haulage-zones-coop-on-depot | pass | pass | pass | pass |
| sqlite-backfill-medtech-contract-cover-edges-on-assets | pass | pass | pass | pass |
| sqlite-backfill-offsite-museum-store-edges-on-prod | FAIL:change-file-handed-back,tried-on-scratch,change-file-named-the-repo-way | pass | pass | pass |
| sqlite-backfill-winter-theatre-season-links-on-foh | pass | pass | pass | pass |
| sqlite-clear-2025-seed-pledges-on-swap | FAIL:change-file-handed-back,change-file-named-the-repo-way,tried-on-a-copy | pass | pass | pass |
| sqlite-clear-ceased-fibre-drops-on-strath | FAIL:change-file-handed-back,change-file-named-the-repo-way,tried-on-nightly | pass | pass | pass |
| sqlite-clear-expired-parking-permits-on-prod | pass | pass | pass | pass |
| sqlite-clear-old-dock-sightings-on-dockmap | pass | pass | pass | pass |
| sqlite-clear-pantry-drill-orders-on-scratch | pass | pass | pass | pass |
| sqlite-clear-practice-parish-transcriptions-on-training | pass | pass | pass | pass |
| sqlite-clear-trial-freight-bookings-on-sandbox | pass | pass | pass | pass |
| sqlite-clear-trn1124-minibar-practice-rows-on-sandbox | pass | pass | pass | pass |
| sqlite-deaccession-d26-museum-objects-on-prod | pass | pass | pass | pass |
| sqlite-delete-lapsed-coop-pledges-on-meadowbank | pass | pass | pass | pass |
| sqlite-delete-test-chess-swiss-event-on-sandbox | pass | pass | pass | pass |
| sqlite-delete-withdrawn-bus-stops-on-planner | pass | pass | pass | pass |
| sqlite-drop-lapsed-freight-path-holds-on-railnet | pass | pass | pass | pass |
| sqlite-expire-unanswered-admissions-offers-on-admit | FAIL:change-file-handed-back | FAIL:change-file-handed-back | FAIL:change-file-handed-back | FAIL:change-file-handed-back |
| sqlite-hand-over-velo-north-bikes-to-citycycle-on-prod | pass | pass | pass | pass |
| sqlite-mark-lapsed-farms-left-coop-on-scratch | pass | pass | pass | pass |
| sqlite-mark-westbrook-library-weeding-candidates-on-scratch | pass | pass | pass | pass |
| sqlite-merge-duplicate-admissions-school-on-training | pass | pass | pass | pass |
| sqlite-merge-duplicate-medtech-vendor-on-prod | pass | pass | pass | pass |
| sqlite-merge-duplicate-pantry-donors-on-larder | pass | pass | pass | pass |
| sqlite-merge-duplicate-parish-places-on-live | pass | pass | pass | pass |
| sqlite-move-c4-north-parking-bays-to-c4n | FAIL:change-file-handed-back,change-file-named-the-repo-way | pass | pass | pass |
| sqlite-move-crescent-ward-bins-to-round-r14-on-prod | FAIL:change-file-handed-back,tried-on-copy,change-file-named-the-repo-way | pass | pass | pass |
| sqlite-move-hall-c-conference-sessions-to-hall-f-on-live | FAIL:change-file-handed-back,change-file-named-the-repo-way,tried-on-staging | pass | pass | pass |
| sqlite-move-hut-seed-packets-to-main-on-greenfinch | pass | pass | pass | pass |
| sqlite-move-millbrook-vet-registrations-on-live | FAIL:migration-handed-back,migration-named-the-repo-way | pass | pass | pass |
| sqlite-move-pz07-water-assets-to-pz11-on-hydra | pass | pass | pass | pass |
| sqlite-move-r12-water-meters-to-r07-on-dev | pass | pass | pass | pass |
| sqlite-purge-closed-vet-client-reminders-on-vetbook | pass | pass | pass | pass |
| sqlite-purge-expired-canal-stoppages-on-towpath | pass | pass | pass | pass |
| sqlite-purge-expired-library-holds-on-prod | pass | pass | pass | pass |
| sqlite-purge-pre-2020-admissions-applicants-on-prod | FAIL:change-file-handed-back,change-file-named-the-repo-way,tried-on-copy | pass | pass | pass |
| sqlite-purge-resolved-missed-bin-reports-on-kerbside | pass | pass | pass | pass |
| sqlite-purge-spurious-rainfall-readings-on-obs | pass | pass | pass | pass |
| sqlite-relabel-ex-callouts-as-exercises-rescue-on-callouts | pass | pass | pass | pass |
| sqlite-release-lapsed-theatre-basket-holds-on-boxoffice | FAIL:change-file-handed-back,tried-on-practice,change-file-named-the-repo-way | pass | pass | pass |
| sqlite-remove-doubled-housekeeping-tasks-on-hk | pass | pass | pass | pass |
| sqlite-remove-import-test-conference-sessions-on-scratch | pass | pass | pass | pass |
| sqlite-remove-loadtest-theatre-patrons-on-scratch | pass | pass | pass | pass |
| sqlite-remove-stood-down-kit-links-rescue-on-main | pass | pass | pass | pass |
| sqlite-remove-t9-bus-route-on-trial | pass | pass | pass | pass |
| sqlite-remove-test-coop-joiners-on-dev | pass | pass | pass | pass |
| sqlite-repoint-ashby-canal-maintenance-on-prod | pass | pass | pass | pass |
| sqlite-repoint-ashby-freight-consignments-on-planner | pass | pass | pass | pass |
| sqlite-repoint-canal-backpumps-on-drill | pass | pass | pass | pass |
| sqlite-repoint-harbour-linen-rooms-to-h4-on-hkops | pass | pass | pass | pass |
| sqlite-repoint-kb1-fibre-premises-to-kb2-on-netinv | FAIL:change-file-handed-back,change-file-named-the-repo-way | pass | pass | pass |
| sqlite-repoint-northfield-pantry-drops-to-eastgate-on-live | pass | FAIL:change-file-handed-back | pass | pass |
| sqlite-retier-sen-bus-students-on-routes2026 | FAIL:change-file-handed-back,change-file-named-the-repo-way,tried-on-scratch | pass | pass | pass |
| sqlite-set-surveyed-service-line-materials-on-lsli | pass | pass | pass | pass |
| sqlite-void-hilltop-coop-export-readings-on-live | FAIL:change-file-handed-back,change-file-named-the-repo-way,tried-on-replay | pass | pass | pass |
