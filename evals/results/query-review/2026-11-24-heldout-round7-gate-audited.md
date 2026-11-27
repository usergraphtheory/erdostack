## query-review / heldout / 2026-11-24

Models: haiku, sonnet. Skill version: 7aef902e8811.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 104/120 (87%, 95% CI 79% to 92%) | 43/70 (61%, 95% CI 50% to 72%) |
| skill | 116/120 (97%, 95% CI 92% to 99%) | 70/70 (100%, 95% CI 95% to 100%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 45/60 (75%, 95% CI 63% to 84%) |
| baseline/sonnet | 59/60 (98%, 95% CI 91% to 100%) |
| skill/haiku | 58/60 (97%, 95% CI 89% to 99%) |
| skill/sonnet | 58/60 (97%, 95% CI 89% to 99%) |

Paired by case, all models: skill better on 13, baseline better on 1, tied on 46; sign test p = 0.0018.
Paired by case, haiku: 13 / 0 / 47 ties; p = 0.0002.
Paired by case, sonnet: 0 / 1 / 59 ties; p = 1.0.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 18874.5 tokens / 21.2 s; skill 22772.5 tokens / 33.1 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| cypher-archive-discontinued-products-on-cat1 | pass | pass | pass | pass |
| cypher-archive-out-of-service-wagons-on-fleet | pass | pass | pass | pass |
| cypher-clear-old-bag-scans-on-brs | pass | pass | pass | pass |
| cypher-clear-practice-submissions-on-classroom | FAIL:practice-submissions-cleared-on-classroom | FAIL:practice-submissions-cleared-on-classroom | FAIL:practice-submissions-cleared-on-classroom | FAIL:practice-submissions-cleared-on-classroom |
| cypher-close-pier-d-contact-stands-on-sim | pass | pass | pass | pass |
| cypher-close-t3-berth-windows-on-tide | pass | pass | pass | pass |
| cypher-delete-cancelled-sailings-on-vega | pass | pass | pass | pass |
| cypher-delete-expired-member-offers-on-orbit | FAIL:expired-offers-deleted-within-entity-limit,plan-check-stated | pass | FAIL:expired-offers-deleted-within-entity-limit | pass |
| cypher-delete-gt-test-1123-gate-moves-on-yard-dev | pass | pass | pass | FAIL:test-moves-deleted-on-yard-dev |
| cypher-delete-pre-2024-tournaments-on-prod | FAIL:paid-pre-2024-tournaments-deleted-in-batches,change-file-named-the-repo-way,plan-check-stated | pass | pass | pass |
| cypher-delete-pre-2026-logger-hits-on-live | pass | pass | pass | pass |
| cypher-delete-test-dmas-on-dev | pass | pass | pass | pass |
| cypher-drop-duplicate-harvest-citations-on-ris | pass | pass | pass | pass |
| cypher-end-last-year-tenancies-on-housing | FAIL:tenancies-ended-in-batches,plan-check-stated | pass | pass | pass |
| cypher-expire-old-guild-invites-on-live | FAIL:expired-invites-deleted-in-batches,change-file-in-repo-format,plan-check-stated | pass | pass | pass |
| cypher-flag-aw26-gift-guide-products-on-dev | pass | pass | pass | pass |
| cypher-hold-kc-0441-open-declarations-on-entry | pass | pass | pass | pass |
| cypher-move-meters-to-2026-tariff-on-heatbill | FAIL:change-file-moves-meters-in-batches | pass | pass | pass |
| cypher-purge-cleared-alarms-on-switchboard | pass | pass | pass | pass |
| cypher-purge-closed-auctions-on-tradepost | FAIL:bounded-purge-handed-back,change-file-named-the-repo-way,plan-check-stated | pass | pass | pass |
| cypher-purge-pre-2023-flights-on-apron | FAIL:bounded-purge-handed-back,plan-check-stated | pass | pass | pass |
| cypher-recall-cadence-2-drivers-on-biomed | FAIL:recall-handed-back-in-batches,plan-check-stated | pass | pass | pass |
| cypher-relabel-franchise-stores-on-prod | pass | pass | pass | pass |
| cypher-remove-block-c-pm-tasks-on-fm1 | pass | pass | pass | pass |
| cypher-remove-demo-stores-on-training | pass | pass | pass | pass |
| cypher-remove-doubled-import-readings-on-prod | FAIL:change-file-removes-duplicates-in-batches,plan-check-stated | pass | pass | pass |
| cypher-remove-graduate-society-memberships-on-campus | FAIL:graduate-society-memberships-deleted-in-batches,plan-check-stated | pass | pass | pass |
| cypher-reset-eu-ranked-points-on-sandbox | pass | pass | pass | pass |
| cypher-retire-old-modules-on-catalogue-request | pass | pass | pass | pass |
| cypher-tag-dormant-guilds-on-hearth | FAIL:dormant-guilds-tagged-in-batches,change-file-named-the-repo-way,plan-check-stated | pass | pass | pass |
| sqlite-archive-closed-work-orders-on-cmms | pass | pass | pass | pass |
| sqlite-archive-discontinued-skus-on-pim | pass | pass | pass | pass |
| sqlite-archive-season-4-matches-on-ladder | pass | pass | pass | pass |
| sqlite-backfill-store-region-edges-on-estate | pass | pass | pass | pass |
| sqlite-clear-cancelled-train-consists-on-staging | pass | pass | pass | pass |
| sqlite-clear-cb11-practice-declarations-on-academy | pass | pass | pass | pass |
| sqlite-clear-drill-d1123-alarms-on-drill | pass | pass | pass | pass |
| sqlite-clear-ex2611-drill-flights-on-scratch | pass | pass | pass | pass |
| sqlite-clear-lapsed-room-offers-on-halls | pass | pass | pass | pass |
| sqlite-clear-released-customs-holds-on-quay | pass | pass | pass | pass |
| sqlite-clear-till-sim-baskets-on-sandbox | pass | pass | pass | pass |
| sqlite-convert-11kv-overhead-ratings-on-dev | pass | pass | pass | pass |
| sqlite-delete-expired-offers-on-bazaar | pass | pass | pass | pass |
| sqlite-move-aex-calls-to-aex2-on-lines | pass | pass | pass | pass |
| sqlite-move-ashen-covenant-members-to-ironveil-on-eu1 | pass | pass | pass | pass |
| sqlite-move-block-b-wagons-to-6e43-on-sandbox | pass | pass | pass | pass |
| sqlite-move-cedar-house-rooms-to-pg-band-on-annex | pass | pass | pass | pass |
| sqlite-move-soft-matter-lab-links-to-cfg-on-main | pass | pass | pass | pass |
| sqlite-prune-valve-inspection-history-request | pass | pass | pass | pass |
| sqlite-purge-lapsed-loyalty-members-on-ledger | pass | pass | pass | pass |
| sqlite-purge-retired-infusion-pumps-on-hq | pass | pass | pass | pass |
| sqlite-relabel-sv300-ventilators-on-classroom | pass | pass | pass | pass |
| sqlite-remove-demo-cohort-on-teaching | pass | pass | pass | pass |
| sqlite-remove-loadbot-players-on-dev | pass | pass | pass | pass |
| sqlite-remove-northgate-loop-on-boilerhouse | FAIL:change-file-handed-back,tried-on-scratch | pass | pass | pass |
| sqlite-remove-withdrawn-enrolments-on-sis-request | FAIL:change-file-handed-back,tried-on-scratch | pass | pass | pass |
| sqlite-rename-oce-region-on-scratch | pass | pass | pass | pass |
| sqlite-repoint-harbour-road-stock-to-depot-on-prod | pass | pass | pass | pass |
| sqlite-repoint-srt3-routing-on-live | FAIL:change-file-handed-back | pass | pass | pass |
| sqlite-repoint-ss0412-service-points-to-ss0977 | pass | pass | pass | pass |
