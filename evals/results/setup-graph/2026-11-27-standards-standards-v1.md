## setup-graph / standards / 2026-11-27

Models: haiku, sonnet. Skill version: fbcd8fc16fef.

| Arm | Substance (case passes when every substance assertion passes) | Contract |
|---|---|---|
| baseline | 10/12 (83%, 95% CI 55% to 95%) | 0/12 (0%, 95% CI 0% to 24%) |
| skill | 11/12 (92%, 95% CI 65% to 98%) | 11/12 (92%, 95% CI 65% to 98%) |

| Arm / model | Substance |
|---|---|
| baseline/haiku | 5/6 (83%, 95% CI 44% to 97%) |
| baseline/sonnet | 5/6 (83%, 95% CI 44% to 97%) |
| skill/haiku | 5/6 (83%, 95% CI 44% to 97%) |
| skill/sonnet | 6/6 (100%, 95% CI 61% to 100%) |

Paired by case, all models: skill better on 1, baseline better on 0, tied on 5; sign test p = 1.0.
Paired by case, haiku: 0 / 0 / 6 ties; p = 1.0.
Paired by case, sonnet: 1 / 0 / 5 ties; p = 1.0.
Regressions (baseline always passed, skill never did): none.
Cost, median per run: baseline 17335.5 tokens / 18.8 s; skill 22821.0 tokens / 30.9 s.
Flaky: none observed.

| Case | baseline/haiku | baseline/sonnet | skill/haiku | skill/sonnet |
|---|---|---|---|---|
| cypher-embedded-ladybug-social-reads-pdm-lock | pass | pass | pass | pass |
| cypher-friend-paths-justfile-server-and-cypher-25-files | FAIL:engine-version-pinned,query-language-fits-engine,query-language-version-stated,version-conflict-surfaced-under-open-questions,language-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | FAIL:query-language-fits-engine,query-language-version-stated,version-conflict-surfaced-under-open-questions,language-conflict-surfaced-under-open-questions,evidence-names-repo-files,open-questions-section | FAIL:query-language-fits-engine,query-language-version-stated | pass |
| cypher-social-short-reads-npm-scripts-second-compose-file | pass | pass | pass | pass |
| networkx-nightly-person-ranks-uv-lock-and-readme | pass | pass | pass | pass |
| networkx-reply-graph-labels-lock-and-compat-workflow | pass | pass | pass | pass |
| sqlite-thread-reads-cli-image-makefile-include-build-arg | pass | pass | pass | pass |
