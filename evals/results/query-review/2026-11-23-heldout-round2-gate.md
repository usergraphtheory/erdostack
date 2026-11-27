## query-review / heldout / 2026-11-23

Models: haiku, sonnet. Skill version: 7d920c82ad2c.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 71/80 (89%, 95% CI 80% to 94%) | 25/72 (35%, 95% CI 25% to 46%) |
| skill | 76/80 (95%, 95% CI 88% to 98%) | 64/72 (89%, 95% CI 80% to 94%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 34/40 (85%, 95% CI 71% to 93%) |
| baseline/sonnet | 37/40 (92%, 95% CI 80% to 97%) |
| skill/haiku | 38/40 (95%, 95% CI 84% to 99%) |
| skill/sonnet | 38/40 (95%, 95% CI 84% to 99%) |

Paired by case, all models: skill better on 5, baseline better on 2, tied on 33; sign test p = 0.4531.
Paired by case, haiku: 5 / 1 / 34 ties; p = 0.2188.
Paired by case, sonnet: 3 / 2 / 35 ties; p = 1.0.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 19160.0 tokens / 33.1 s; skill 22316.0 tokens / 33.2 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| cypher-add-pick-tasks-to-order-release | pass | pass | pass | pass |
| cypher-audit-flags-invoices-after-erasure | pass | pass | pass | pass |
| cypher-check-buyer-erasure-script | pass | pass | pass | pass |
| cypher-fold-likes-into-reactions-migration | pass | pass | pass | pass |
| cypher-follower-counts-too-high-on-profiles | pass | pass | pass | pass |
| cypher-instrument-card-two-seconds | pass | pass | pass | pass |
| cypher-last-look-at-revision-purge | pass | pass | pass | pass |
| cypher-lint-fails-on-settings-merge | FAIL:settings-found-or-created-from-the-account,defaults-and-columns-kept,says-the-merge-is-right-here,query-text-untouched,finding-silenced-the-repo-way,plan-check-stated | pass | FAIL:settings-found-or-created-from-the-account,defaults-and-columns-kept,says-the-merge-is-right-here,query-text-untouched,finding-silenced-the-repo-way,plan-check-stated | pass |
| cypher-merge-duplicate-venues-script | pass | pass | pass | pass |
| cypher-password-reset-token-query | pass | pass | pass | pass |
| cypher-pr-asks-for-order-date-index | pass | pass | pass | pass |
| cypher-review-next-departures-before-pr | pass | pass | pass | pass |
| cypher-reviewer-flags-collect-in-standings | pass | pass | pass | pass |
| cypher-reviewer-says-call-syntax-is-invalid | FAIL:says-the-syntax-is-valid,change-text-untouched,plan-check-stated | pass | pass | pass |
| cypher-reviewer-says-session-cleanup-stops-early | pass | pass | pass | pass |
| cypher-scan-load-fails-on-parcel-constraint | pass | pass | pass | pass |
| cypher-search-key-backfill-half-done | pass | pass | pass | pass |
| cypher-unflag-observations-after-bot-glitch | FAIL:scoped-batched-unflag-handed-back,change-file-in-the-repo-format,plan-check-stated | pass | pass | pass |
| ladybug-add-tracks-to-genre-leaderboard | pass | pass | pass | pass |
| ladybug-pr-comment-on-coauthor-network | pass | pass | pass | pass |
| networkx-dispatch-route-with-stops | pass | pass | pass | pass |
| networkx-lineage-sources-only-flag | pass | pass | pass | FAIL:lineage-right-on-the-catalog |
| networkx-review-comment-on-downstream-gates | pass | pass | pass | pass |
| sqlite-apply-account-merges-job | pass | pass | pass | pass |
| sqlite-archive-seasonal-catalogue-job | pass | pass | pass | pass |
| sqlite-audit-finding-on-reach-refresh | pass | FAIL:says-the-full-rebuild-is-intended,source-untouched | FAIL:says-the-full-rebuild-is-intended,source-untouched | pass |
| sqlite-drop-unused-indexes-request | pass | pass | pass | pass |
| sqlite-explain-access-for-audit-log | pass | pass | pass | pass |
| sqlite-lint-finding-on-batch-requirements | pass | pass | pass | pass |
| sqlite-mentions-panel-slow-for-some | pass | pass | pass | pass |
| sqlite-outage-map-missing-substations | FAIL:every-substation-that-lost-supply,plan-inspected-before-run | FAIL:every-substation-that-lost-supply,plan-inspected-before-run | pass | pass |
| sqlite-page-escalation-reach-query | pass | pass | pass | pass |
| sqlite-plan-guard-on-latest-endorsements | pass | pass | pass | pass |
| sqlite-portfolio-totals-for-board-pack | pass | pass | pass | pass |
| sqlite-pr-comment-on-costars-panel | FAIL:costs-no-more,says-the-distinct-is-needed,query-text-untouched,plan-inspected-before-run | FAIL:costs-no-more,query-text-untouched,plan-inspected-before-run | pass | pass |
| sqlite-pre-freeze-chores | pass | pass | pass | pass |
| sqlite-remove-closed-stops-job | pass | pass | pass | pass |
| sqlite-rescale-dormant-affinity-job | pass | pass | pass | FAIL:halves-exactly-the-dormant-edges,commits-in-chunks |
| sqlite-review-comment-on-expiry-loop | pass | pass | pass | pass |
| sqlite-review-comment-on-suggestions-query | FAIL:says-the-exclusion-is-intended,query-text-untouched | pass | pass | pass |
