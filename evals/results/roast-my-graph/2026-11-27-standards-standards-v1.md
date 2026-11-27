## roast-my-graph / standards / 2026-11-27

Models: haiku, sonnet. Skill version: 328dae67cdaa.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 8/12 (67%, 95% CI 39% to 86%) | 0/12 (0%, 95% CI 0% to 24%) |
| skill | 10/12 (83%, 95% CI 55% to 95%) | 12/12 (100%, 95% CI 76% to 100%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 4/6 (67%, 95% CI 30% to 90%) |
| baseline/sonnet | 4/6 (67%, 95% CI 30% to 90%) |
| skill/haiku | 5/6 (83%, 95% CI 44% to 97%) |
| skill/sonnet | 5/6 (83%, 95% CI 44% to 97%) |

Paired by case, all models: skill better on 2, baseline better on 0, tied on 4; sign test p = 0.5.
Paired by case, haiku: 1 / 0 / 5 ties; p = 1.0.
Paired by case, sonnet: 1 / 0 / 5 ties; p = 1.0.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 24706.0 tokens / 60.1 s; skill 31548.0 tokens / 79.5 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| cypher-forum-graph-nightly-import-and-message-page-queries | FAIL:explains-comment-merge-duplicates-people,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:explains-comment-merge-duplicates-people,roast-md-path,roast-md-covers-findings,roast-md-footer | FAIL:finds-comment-merge-duplicates-people,explains-comment-merge-duplicates-people | FAIL:finds-comment-merge-duplicates-people,explains-comment-merge-duplicates-people |
| cypher-member-profile-queries-and-the-nightly-graph-load | pass | pass | pass | pass |
| cypher-thread-queries-and-a-ci-lint-on-variable-length-patterns | FAIL:no-critical-or-high,says-sound-reply-tree-walks,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass | pass |
| networkx-degrees-of-separation-package-for-the-members-app | pass | pass | pass | pass |
| sqlite-account-erasure-command-and-a-contractor-review | pass | FAIL:no-critical-or-high,roast-md-path,roast-md-covers-findings,roast-md-footer | pass | pass |
| sqlite-profile-page-latest-activity-box-on-the-messages-tables | pass | pass | pass | pass |
