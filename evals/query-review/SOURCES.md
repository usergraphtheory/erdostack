# Sources for query-review evals

Checked 2026-11-23 (rows for the twelve cases added the same day were appended in a second pass). Engine facts go stale: re-check this file before any result is published and whenever
a pinned version changes.

## How to read the status column

The authoring session could search the web but could not open pages: search returned page titles and URLs
only. So each fact has one of three statuses, and they are not equally strong.

- **listing**: the search result for the official page confirms the fact by its title or URL (for example a
  release-notes page titled with the version number). The page body was not read.
- **executed**: verified by running it on this machine (SQLite 3.53.1, Python 3.13.18, Node 22.23.5).
- **memory**: stated from the author's prior knowledge of the official documentation. The official page is
  listed so it can be checked, but it was not re-read on this date. Treat as unverified.

A URL marked † was not returned by search in the session; it is where the author expects the page to be
and has to be confirmed along with the fact.

No gold answer depends on a **memory** fact: cases pin engine versions on which every accepted construct is
valid, and graders accept every form listed below.

## Neo4j

| Fact | Used by | Status | Source |
|---|---|---|---|
| Neo4j 2026.10.2 exists and was the most current release on the date checked; 2026.10.0 was released 20 October 2026 | fixtures pinning `neo4j:2026.10.2` (dev `cypher-papers-by-orcid-lookup`, `cypher-purge-events-on-prod-request`; held-out `cypher-tenant-offboarding-script`, `cypher-linter-flagged-call-chain`) | listing | https://neo4j.com/release-notes/database/neo4j-2026-10-2/ , https://neo4j.com/release-notes/database/neo4j-2026-10-0/ |
| Neo4j 5.26 is the long-term-support line of version 5 | fixtures that say "Neo4j 5.26 LTS" (held-out `cypher-promo-sales-report-oom`, `cypher-slow-isbn-lookup`) | listing for "v5 long-term support" (the number 5.26 is from memory) | https://neo4j.com/blog/developer/neo4j-v5-lts-evolution/ , https://neo4j.com/developer/kb/neo4j-supported-versions/ |
| Docker image tags have the form `neo4j:<version>` and `neo4j:<version>-enterprise` | docker-compose fixtures | memory | https://hub.docker.com/_/neo4j † |
| `CALL { ... } IN TRANSACTIONS` is documented for Cypher 5, Cypher 25 and current | batching accepted in the two delete cases | listing (page "CALL subqueries in transactions" exists in the 5, 25 and current manuals) | https://neo4j.com/docs/cypher-manual/current/subqueries/subqueries-in-transactions/ , https://neo4j.com/docs/cypher-manual/5/subqueries/subqueries-in-transactions/ , https://neo4j.com/docs/cypher-manual/25/subqueries/subqueries-in-transactions/ |
| Introduced in Neo4j 4.4; `OF n ROWS` sets the batch size, default 1000; must run in an implicit (auto-commit) transaction; `:auto` prefix in Browser | `cypher_lint.form_valid`; wording of good selfcheck outputs | memory | same pages |
| `ON ERROR CONTINUE / BREAK / FAIL` and `REPORT STATUS AS` from 5.7 | `form_valid` | memory | same pages |
| `IN [n] CONCURRENT TRANSACTIONS` from 5.21 | `form_valid` | listing for the feature (blog "Introducing concurrent writes to Cypher subqueries"); the version number is from memory | https://neo4j.com/blog/developer/concurrent-writes-cypher-subqueries/ |
| Variable scope clause `CALL (x) { ... }` from 5.23; the importing `WITH` form still parses but is deprecated | `form_valid`; both spellings accepted | memory | https://neo4j.com/docs/cypher-manual/current/subqueries/call-subquery/ |
| `ON ERROR RETRY [FOR n SECONDS] [THEN ...]` from 2025.03 | `form_valid` | memory | subqueries-in-transactions page above |
| `apoc.periodic.iterate` exists (APOC plugin) and `CALL { } IN TRANSACTIONS` is the documented replacement | accepted as a batching form | listing (GraphAcademy post "Replacing your APOC Periodic Iterate with CALL {} IN TRANSACTIONS") | https://graphacademy.neo4j.com/blog/replace-apoc-periodic-iterate-with-call-in-transactions |
| `USING PERIODIC COMMIT` was removed in 5.0 and only applied to LOAD CSV | `form_valid` (reported invalid on 5.x and later) | memory | https://neo4j.com/docs/cypher-manual/current/deprecations-additions-removals-compatibility/ † |
| `EXPLAIN` shows the plan without running; `PROFILE` runs and reports rows and db hits | contract assertion "says how to check the plan" | listing (page "Understanding query plans" / "Execution plans") | https://neo4j.com/docs/cypher-manual/current/planning-and-tuning/execution-plans/ |
| Variable-length syntax `*`, `*n`, `*n..m`, `*..m`, `*n..`; quantified path patterns `{n,m}`, `+`, `*` (5.9 and later); `shortestPath()`, `SHORTEST k` | `cypher_lint.var_lengths` | listing for the pages; details from memory | https://neo4j.com/docs/cypher-manual/current/patterns/reference/variable-length-paths/ , https://neo4j.com/docs/cypher-manual/current/patterns/variable-length-paths/ |
| `CREATE INDEX name IF NOT EXISTS FOR (n:L) ON (n.p)`; `CREATE CONSTRAINT ... REQUIRE n.p IS UNIQUE` / `IS NODE KEY` create a backing index; existence and type constraints do not; full-text and vector indexes do not serve equality seeks; a property inside a function call cannot be index-seeked; there is no index on an expression | `cypher_lint.schema_indexes`, `equality_lookups`; the two index cases | listing for "The impact of indexes on query performance"; details from memory | https://neo4j.com/docs/cypher-manual/current/indexes/performance-indexes/using-indexes/ |
| A MATCH with disconnected patterns is planned as a cartesian product and the server emits a notification for it | `cypher_lint.cartesian_products` | memory | https://neo4j.com/docs/status-codes/current/notifications/all-notifications/ † |
| ASC/DESC cannot be supplied as a query parameter, and a parameter cannot stand for the name in `n.name`; a property can be read dynamically with `n[$key]`, so a sort field can travel as a parameter that way. Corrected on the second pass of 2026-11-23: the first version of this row said a property name cannot be a parameter at all, and the grader of the case rejected `ORDER BY o[$sort]` | held-out `js-orders-sort-parameter` (both forms accepted), `python-injection-report-on-catalogue-search` (wording of the notes and selfcheck replies only) | memory | https://neo4j.com/docs/cypher-manual/current/syntax/parameters/ † |
| Labels and relationship types can be supplied dynamically (`MATCH (n:$($label))`) in recent versions; a fixed lookup table in application code is still a safe way to choose a label | held-out `python-injection-report-on-catalogue-search`: the fixture chooses the label from a table; no grader depends on the dynamic form, and an agent that switched to it would fail that case's "sends the same Cypher" check (EVALS.md, open questions) | listing (search on 2026-11-23 returned the Neo4j developer blog post "Cypher dynamism: a step toward simpler and more secure queries"); the version it arrived in, 5.26, is from memory | https://neo4j.com/blog/developer/cypher-dynamism/ |
| The server attaches a notification with code `Neo.ClientNotification.Statement.CartesianProduct` and the title "This query builds a cartesian product between disconnected patterns." to a query whose MATCH lists disconnected patterns, whatever their size | held-out `cypher-log-warning-on-price-card` (the log line quoted in the prompt; the grader does not parse it) | listing for the page (search on 2026-11-23 returned "List of notification codes" and community threads quoting the title); the exact code string is from memory | https://neo4j.com/docs/status-codes/current/notifications/all-notifications/ |
| Python driver: `execute_query` returns records, a summary and keys; `summary.notifications` is a list of dicts (or None) with `code` and `title` | fixture `api/queries.py` of the same case (not graded, never executed) | memory | https://neo4j.com/docs/api/python-driver/current/api.html † |
| A relationship variable can be deleted inside `CALL (r) { DELETE r } IN TRANSACTIONS OF n ROWS` the same way a node can | held-out `cypher-retire-v2-recommender` | memory (same pages as the CALL IN TRANSACTIONS rows above) | https://neo4j.com/docs/cypher-manual/current/subqueries/subqueries-in-transactions/ |
| Fixtures pinning `neo4j:2026.10.2` or "Neo4j 5.26 LTS" added on the second pass | dev `cypher-pr-comment-on-category-subtree`; held-out `cypher-retire-v2-recommender`, `python-injection-report-on-catalogue-search` (2026.10), `cypher-log-warning-on-price-card` (5.26) | same status as the first two rows of this table | same pages |
| Python driver: 6.x is current (API docs titled "Neo4j Python Driver 6.3"); 6.0.3 is a published release; `driver.execute_query(query, parameters_=None, **kwargs)`, keyword arguments ending in `_` are configuration, others are query parameters; `session.run(query, parameters, **kwargs)` | dev `python-people-search-handler` fixture (`neo4j==6.0.3`) and the stand-in driver | listing for the versions; signature from memory | https://neo4j.com/docs/api/python-driver/current/ , https://pypi.org/project/neo4j/6.0.3/ |
| JavaScript driver: `neo4j-driver` 6.0.1 is a published release; `driver.executeQuery(query, params, config)`, `session.run(query, params)` | held-out `js-orders-sort-parameter` fixture and the stand-in driver | listing for the version; signature from memory | https://neo4j.com/docs/javascript-manual/current/query-simple/ , https://www.npmjs.com/package/neo4j-driver |
| With `ON ERROR CONTINUE` or `ON ERROR BREAK` on `CALL { ... } IN TRANSACTIONS`, a failed inner transaction is skipped (or stops the rest) and the outer transaction still succeeds; `ON ERROR FAIL` is the default. The clause is allowed only in implicit transactions | round-5 held-out `cypher-review-wants-on-error-continue-in-size-backfill`, and the cases that reject the clause inside a managed transaction | read on 2026-11-23 (search result excerpts of the Cypher Manual pages for 5 and current, section "Error behavior") | https://neo4j.com/docs/cypher-manual/5/subqueries/subqueries-in-transactions/ |

## LadybugDB

| Fact | Used by | Status | Source |
|---|---|---|---|
| A LadybugDB release numbered 0.19.1 exists | `engine_version: 0.19.1` in held-out `ladybug-member-suggestions-never-returns` | listing (NuGet "LadybugDB 0.19.1", docs.rs "lbug 0.19.1") | https://www.nuget.org/packages/LadybugDB/ , https://docs.rs/crate/lbug/0.19.1/source/lbug-src/README.md |
| Documentation for MATCH, recursive relationships and performance debugging lives at docs.ladybugdb.com | the same case | listing | https://docs.ladybugdb.com/cypher/query-clauses/match , https://docs.ladybugdb.com/cypher/expressions/recursive-rel-functions , https://docs.ladybugdb.com/developer-guide/performance-debugging |
| Recursive relationship syntax is `-[:T*min..max]-`; a pattern with no upper bound extends up to a configured maximum depth (30 by default in Kuzu 0.11, set with `var_length_extend_max_depth`); `* SHORTEST`, `* ALL SHORTEST` forms exist | trap of the same case. The grader only requires explicit bounds that add up to two hops; it does not depend on the default value | memory (Kuzu 0.11.3 documentation) | https://docs.ladybugdb.com/cypher/query-clauses/match |
| `EXPLAIN` and `PROFILE` are supported | contract assertion of the same case | listing for the performance-debugging page; details from memory | https://docs.ladybugdb.com/developer-guide/performance-debugging |
| DDL: `CREATE NODE TABLE T(col TYPE, ..., PRIMARY KEY (col))`, `CREATE REL TABLE R(FROM A TO B, col TYPE)` | `schema.cypher` fixture of the same case (not graded) | memory (Kuzu 0.11.3 documentation) | https://docs.ladybugdb.com/cypher/data-definition/create-table † |
| There is no server-side batching clause equivalent to `CALL { } IN TRANSACTIONS` | `form_valid` returns invalid for LadybugDB; no case relies on it | memory | none found |
| Python package `ladybug` (earlier `real_ladybug`), npm `@ladybugdb/core` (earlier `lbug`); Kuzu archived October 2025 at 0.11.3 | **not used by any fixture** | could not verify. A PyPI project page named `ladybug` and an npm listing for `@ladybugdb/core` exist, but their contents were not read, and unrelated "Ladybug Tools" packages share the name space | https://pypi.org/project/ladybug/ , https://packages.ecosyste.ms/api/v1/registries/npmjs.org/packages/@ladybugdb%2Fcore |

## SQLite

| Fact | Used by | Status | Source |
|---|---|---|---|
| In a recursive CTE, `UNION` discards rows already produced, so recursion over a cyclic graph ends when no new row appears; `UNION ALL` does not | dev `sqlite-downstream-accounts-query`, held-out `sqlite-dependents-within-hops` | executed (`lib/test_sqlgrade.py`, and every selfcheck variant of the two cases) | https://sqlite.org/lang_with.html |
| `EXPLAIN QUERY PLAN` detail lines read `SCAN <name>`, `SEARCH <name> USING [COVERING] INDEX <index> (...)`, `SEARCH <name> USING INTEGER PRIMARY KEY` | `sqlgrade.scans`, `index_searches`; held-out `sqlite-what-links-here-query` | executed on 3.53.1 (the format has changed between releases; re-check on upgrade) | https://sqlite.org/eqp.html |
| An index on (a, b) does not serve a lookup on b alone unless skip-scan applies, which needs many rows per distinct a | held-out `sqlite-what-links-here-query` | executed (the plan without the index is a full pass; with it, a SEARCH) | https://sqlite.org/optoverview.html † |
| The progress handler is called every N virtual-machine instructions and can interrupt a statement; the count is the same on any machine for the same build, database and statement | step budgets in every execution-graded case | executed | https://sqlite.org/c3ref/progress_handler.html † |
| One writer at a time; a write transaction blocks other writers until it commits | held-out `sqlite-purge-deactivated-edges-job` (stated in the fixture's own docs) | memory | https://sqlite.org/lockingv3.html † , https://sqlite.org/wal.html † |
| `DELETE ... LIMIT` needs a compile-time option that this build does not have; `DELETE ... WHERE key IN (SELECT ... LIMIT ?)` works everywhere | chunked-delete fixtures and selfcheck outputs | executed (`PRAGMA compile_options` shows no `ENABLE_UPDATE_DELETE_LIMIT`) | https://sqlite.org/lang_delete.html † |
| In LIKE, `_` matches any one character and `%` any run of characters unless an `ESCAPE` character is given; GLOB uses `*` and `?` and treats `_` literally | held-out `sqlite-cleanup-leaked-scratch-nodes` | executed (on the case database `LIKE 'tmp_%'` matches 6,520 keys; `LIKE 'tmp\_%' ESCAPE '\'`, `GLOB 'tmp_*'` and `substr(key, 1, 4) = 'tmp_'` each match 6,180) | https://sqlite.org/lang_expr.html † |
| A LIKE or GLOB prefix test is turned into an index range only when the pattern is a string literal or a bound parameter, not an expression such as `:prefix || '%'`; for LIKE the index must also be NOCASE (or `case_sensitive_like` on). Otherwise the plan is `SCAN t USING INDEX ...`, a walk of the whole index. `col >= :p AND col < :p || char(1114111)` plans as `SEARCH ... (col>? AND col<?)` | held-out `sqlite-tag-autocomplete-query` | executed on 3.53.1 (plans and VM step counts for six spellings were measured while writing the case; the selfcheck variants keep three of them). Version-sensitive: re-run the selfcheck on upgrade | https://sqlite.org/optoverview.html † |
| A WITHOUT ROWID table is stored as a B-tree on its PRIMARY KEY, so a lookup on the leading key column plans as `SEARCH t USING PRIMARY KEY (col=?)` and returns rows in key order without a sort | held-out `sqlite-index-request-for-activity-panel` | executed (the plan line is printed in the grader's evidence) | https://sqlite.org/withoutrowid.html † |
| The index behind a UNIQUE text column is case-sensitive: `col = ? COLLATE NOCASE` and `lower(col) = ?` cannot seek on it, and the plan for them reads `SCAN t USING COVERING INDEX ...`, which is still a full pass. An index declared `ON t(col COLLATE NOCASE)` serves the first form and an expression index `ON t(lower(col))` the second, each only when the query uses the matching form | dev `python-handle-lookups-ignore-case` | executed (all four combinations appear in the selfcheck variants or were run while writing the case) | https://sqlite.org/expridx.html † , https://sqlite.org/datatype3.html † |
| In a recursive CTE, UNION compares whole rows, so a row that carries a depth is new on every lap of a cycle and the recursion does not end | held-out `python-descendants-follow-shortcuts` | executed (selfcheck variant `bad-union-keeps-depth-in-the-row`) | https://sqlite.org/lang_with.html |
| `json_each` is available in this build | reference implementation of the same case; two selfcheck variants of dev `sqlite-scanner-flagged-subgraph-query` | executed | https://sqlite.org/json1.html † |

## Facts the round-4 and round-5 cases lean on that were not re-checked

The authors of the 340 cases added in rounds 4 and 5 could not open web pages. Beyond the rows above, their
fixtures, gold answers or accepted alternatives rely on the following, all at status **memory** for Neo4j 5.26
unless a row above covers them. They are listed so that a reader with a server can check them; a case found to
rest on a wrong one should be reported as a grader bug.

- `MERGE` on a node or relationship fails when a property in the pattern is null.
- `DELETE` of a node that still has relationships fails; `DETACH DELETE` removes them with the node.
- Integer division truncates (`7 / 2` is `3`); `round()` returns a float.
- A `MERGE` on a whole path creates the whole path when any part of it is missing.
- An index cannot be created on a label and property that a uniqueness constraint already covers.
- One accepted alternative in a loader case assumes a node key constraint is checked at commit.
- LadybugDB: `MERGE` followed by `SET` on the merged relationship is accepted (one case).

## Not sources

Fixture schemas, data, queries, hostnames and prose are original and generated by the `setup.py` scripts
with fixed seeds. No dataset, schema or example was copied from vendor documentation, books or other
repositories. The notification title quoted in one prompt is the server's own message, used as a log line. The scanner rule id mentioned in one selfcheck reply (Bandit B608) is a real rule name used
only as a label.
