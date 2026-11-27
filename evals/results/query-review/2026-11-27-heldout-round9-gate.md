## query-review / heldout / 2026-11-27

Models: haiku, sonnet. Skill version: 7aef902e8811.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 140/160 (88%, 95% CI 82% to 92%) | 82/104 (79%, 95% CI 70% to 86%) |
| skill | 159/160 (99%, 95% CI 96% to 100%) | 99/104 (95%, 95% CI 89% to 98%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 61/80 (76%, 95% CI 66% to 84%) |
| baseline/sonnet | 79/80 (99%, 95% CI 93% to 100%) |
| skill/haiku | 79/80 (99%, 95% CI 93% to 100%) |
| skill/sonnet | 80/80 (100%, 95% CI 95% to 100%) |

Paired by case, all models: skill better on 18, baseline better on 0, tied on 62; sign test p = 0.0.
Paired by case, haiku: 18 / 0 / 62 ties; p = 0.0.
Paired by case, sonnet: 1 / 0 / 79 ties; p = 1.0.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 19691.5 tokens / 19.5 s; skill 24359.0 tokens / 33.8 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| cypher-archive-2025-pool-sessions-on-live | pass | pass | pass | pass |
| cypher-backfill-ferry-booking-fare-class-on-prod | FAIL:backfill-change-handed-back,change-file-named-the-repo-way | FAIL:backfill-change-handed-back,change-file-named-the-repo-way | pass | pass |
| cypher-clear-eastgate-spring-language-enrolments-on-bw | pass | pass | pass | pass |
| cypher-clear-lapsed-carshare-waitlist-links-on-fleet | FAIL:bounded-clear-handed-back,change-file-named-the-repo-way | pass | pass | pass |
| cypher-clear-last-season-football-training-sessions-on-pitchside | FAIL:change-file-handed-back,change-file-named-the-repo-way | pass | pass | pass |
| cypher-clear-old-dental-recall-reminders-on-chairside | FAIL:bounded-purge-handed-back,change-file-named-the-repo-way | pass | pass | pass |
| cypher-delete-expired-hire-quotes-lighting-on-main | pass | pass | pass | pass |
| cypher-mark-lapsed-football-players-on-league | pass | pass | pass | pass |
| cypher-move-b-list-radio-tracks-to-c-list-on-library | pass | pass | pass | pass |
| cypher-move-kirkgate-laundrette-machines-to-ld-07-on-live | pass | pass | pass | pass |
| cypher-move-lapsed-language-students-to-alumni-on-prod | pass | pass | pass | pass |
| cypher-purge-expired-ferry-passes-on-harbour | pass | pass | pass | pass |
| cypher-purge-felled-street-trees-on-canopy | pass | pass | pass | pass |
| cypher-purge-lapsed-coach-seat-holds-on-prod | FAIL:change-file-keeps-deposit-holds,change-file-named-the-repo-way | pass | pass | pass |
| cypher-purge-old-donor-reminders-blood-on-vein | pass | pass | pass | pass |
| cypher-purge-old-hive-inspections-on-hivebook | pass | pass | pass | pass |
| cypher-purge-pre-2024-carshare-trips-on-prod | pass | pass | pass | pass |
| cypher-purge-pre-2024-radio-play-logs-on-studio-b | FAIL:bounded-purge-handed-back,change-file-named-the-repo-way | pass | pass | pass |
| cypher-rehome-northgate-tools-to-eastside-hub-on-catalogue | FAIL:change-file-handed-back,change-file-named-the-repo-way,plan-check-stated | pass | pass | pass |
| cypher-relabel-closed-bakery-accounts-on-orderbook | FAIL:relabel-file-handed-back,change-file-named-the-repo-way | pass | pass | pass |
| cypher-tag-dormant-coach-passengers-on-bookings | FAIL:change-file-tags-in-batches,change-file-named-the-repo-way | pass | FAIL:change-file-tags-in-batches | pass |
| cypher-tag-dormant-laundrette-loyalty-cards-on-prod | pass | pass | pass | pass |
| cypher-tag-pat-due-fixtures-lighting-on-prod | pass | pass | pass | pass |
| cypher-withdraw-unpaid-choir-festival-entries-on-programme | pass | pass | pass | pass |
| networkx-clear-demo-swarm-calls-from-practice-hivegraph | pass | pass | pass | pass |
| networkx-clear-pre-2025-tool-loan-edges-on-training | pass | pass | pass | pass |
| networkx-clear-trial-ferry-sailings-on-practice-graph | pass | pass | pass | pass |
| networkx-merge-duplicate-choir-venue-on-rehearsal | pass | pass | pass | pass |
| networkx-merge-duplicate-dental-lab-on-scratch | pass | pass | pass | pass |
| networkx-merge-duplicate-football-club-on-practice | pass | pass | pass | pass |
| networkx-merge-duplicate-laundrette-contractor-on-scratch-graph | pass | pass | pass | pass |
| networkx-move-b1-demo-learners-to-group-d3-on-sandbox | pass | pass | pass | pass |
| networkx-move-c14-coach-departures-to-c22-on-practice | pass | pass | pass | pass |
| networkx-move-otters-pool-lane-hires-on-sandbox-graph | pass | pass | pass | pass |
| networkx-remove-demo-bakery-shops-from-practice-graph | pass | pass | pass | pass |
| networkx-remove-fair-carshare-bays-on-scratch | pass | pass | pass | pass |
| networkx-remove-saturday-practice-trees-from-training-graph | pass | pass | pass | pass |
| networkx-remove-test-courier-hospitals-blood-on-practice | pass | pass | pass | pass |
| networkx-repoint-dr3-rig-fixtures-lighting-on-scratch | pass | pass | pass | pass |
| networkx-repoint-hilltop-radio-relay-feeds-in-sandbox-graph | pass | pass | pass | pass |
| sqlite-archive-2024-coach-tour-bookings-on-sandbox | pass | pass | pass | pass |
| sqlite-archive-fernlea-pool-enrolments-on-main | FAIL:change-file-handed-back,change-file-named-the-repo-way,tried-on-sandbox | pass | pass | pass |
| sqlite-archive-old-street-tree-inspections-on-arbor | pass | pass | pass | pass |
| sqlite-archive-pre-2024-radio-episodes-on-airlog | pass | pass | pass | pass |
| sqlite-archive-pre-2024-tool-loans-on-shed | pass | pass | pass | pass |
| sqlite-backfill-carshare-depot-links-on-live | pass | pass | pass | pass |
| sqlite-backfill-dental-assigned-dentist-edges-on-prod | pass | pass | pass | pass |
| sqlite-backfill-donor-home-centres-blood-on-core | pass | pass | pass | pass |
| sqlite-backfill-pool-lesson-levels-on-practice | pass | pass | pass | pass |
| sqlite-backfill-spring-course-language-links-on-rehearsal | pass | pass | pass | pass |
| sqlite-backfill-swarm-collector-edges-on-swarmline | pass | pass | pass | pass |
| sqlite-clear-laundrette-load-test-orders-on-scratch | pass | pass | pass | pass |
| sqlite-clear-trainee-session-bookings-blood-on-practice | pass | pass | pass | pass |
| sqlite-clear-training-choir-ticket-holds-on-practice | pass | pass | pass | pass |
| sqlite-clear-wednesday-trainee-tree-inspections-on-scratch | pass | pass | pass | pass |
| sqlite-clear-zztest-dental-patients-on-training | pass | pass | pass | pass |
| sqlite-dedupe-double-imported-tool-loans-on-scratch | pass | pass | pass | pass |
| sqlite-delete-test-import-radio-tracks-on-scratch | pass | pass | pass | pass |
| sqlite-merge-duplicate-bakery-customer-on-sandbox | pass | pass | pass | pass |
| sqlite-merge-duplicate-choir-singers-on-prod | FAIL:change-file-handed-back,change-file-named-the-repo-way,tried-on-copy | pass | pass | pass |
| sqlite-merge-duplicate-coach-pickup-points-on-ops | pass | pass | pass | pass |
| sqlite-merge-duplicate-ferry-terminal-on-scratch | pass | pass | pass | pass |
| sqlite-merge-duplicate-hire-client-lighting-on-sandbox | pass | pass | pass | pass |
| sqlite-merge-duplicate-linden-street-trees-on-live | FAIL:change-file-handed-back,tried-on-rehearsal,change-file-named-the-repo-way | pass | pass | pass |
| sqlite-move-harbour-street-dental-patients-on-live | FAIL:change-file-handed-back,change-file-named-the-repo-way,tried-on-rehearsal | pass | pass | pass |
| sqlite-move-hollin-moor-bee-colonies-to-ap-22-on-register | pass | pass | pass | pass |
| sqlite-move-hollins-pitch-3-football-fixtures-to-pitch-5-on-prod | FAIL:change-file-handed-back,change-file-named-the-repo-way,tried-on-rehearsal | pass | pass | pass |
| sqlite-move-hunslet-store-fixtures-lighting-on-prod | pass | pass | pass | pass |
| sqlite-move-orchard-carshare-cars-to-mill-on-sandbox | pass | pass | pass | pass |
| sqlite-move-ref-114-december-football-fixtures-to-ref-203-on-sandbox | pass | pass | pass | pass |
| sqlite-move-st-barnabas-choir-slots-to-corn-exchange-on-festival | FAIL:change-file-handed-back,change-file-named-the-repo-way,tried-on-rehearsal | pass | pass | pass |
| sqlite-purge-expired-tool-reservations-on-live | pass | pass | pass | pass |
| sqlite-purge-no-show-trial-lessons-on-prod | FAIL:change-file-handed-back,tried-on-practice,change-file-named-the-repo-way | pass | pass | pass |
| sqlite-purge-old-laundrette-service-washes-on-prod | pass | pass | pass | pass |
| sqlite-purge-old-pool-entry-scans-on-prod | FAIL:change-file-handed-back,change-file-named-the-repo-way,tried-on-scratch | pass | pass | pass |
| sqlite-purge-paused-bakery-standing-orders-on-prod | FAIL:change-file-handed-back,tried-on-scratch,change-file-named-the-repo-way | pass | pass | pass |
| sqlite-remove-pilot-signup-donors-blood-on-live | pass | pass | pass | pass |
| sqlite-repoint-dry-dock-ferry-bookings-on-ops | pass | pass | pass | pass |
| sqlite-repoint-eastgate-bakery-customers-to-northgate-on-live | FAIL:change-file-handed-back,tried-on-trial,change-file-named-the-repo-way | pass | pass | pass |
| sqlite-standstill-ap-05-bee-colonies-on-sandbox | pass | pass | pass | pass |
