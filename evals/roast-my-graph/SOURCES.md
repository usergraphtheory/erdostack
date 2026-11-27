# Sources for the roast-my-graph eval

Every outside fact a case relies on, where it came from, and how well it was checked. Engine facts go stale:
re-check this file whenever a case fails for a reason that smells like the engine moved.

Date of all checks: 2026-11-23 (both authoring rounds).

## How to read the status column

- **read**: the official page was fetched and read on the date above.
- **executed**: confirmed by running it on the eval machine (Python 3.13.18, SQLite 3.53.1 through Python's
  `sqlite3` module, NetworkX 3.7).
- **not read**: a web search located the official page (URL given) but its content could not be read in the
  authoring session, which had search results as titles and links only. By this eval's rule these are
  **unverified**. The last column says whether any gold answer rests on the fact.
- **accepted**: not read by an author, but accepted as fact by the maintainer on 2026-11-23 as long-stable
  Cypher semantics. Gold answers may rest on these.

## LadybugDB

| Fact | Source | Status | Used by | Does a gold answer rest on it? |
|---|---|---|---|---|
| `CREATE NODE TABLE Name(col TYPE, ..., PRIMARY KEY (col))`, or `col TYPE PRIMARY KEY` inline | https://docs.ladybugdb.com/cypher/data-definition/create-table/ | read | dev/ladybug-sound-citation-schema..., heldout/ladybug-crew-assignment..., heldout/ladybug-query-uses-a-relationship... | yes |
| A node table must have a primary key; key types are STRING, numeric, DATE or BLOB; the engine builds an index for primary-key lookups | same page | read | the clean LadybugDB case ("no indexes defined" is not a finding) | yes |
| `SERIAL` can be used for an auto-incremented primary key | same page | read | fixture of heldout/ladybug-crew-assignment... | no (fixture text) |
| `CREATE REL TABLE Name(FROM A TO B, prop TYPE, ...)`; several `FROM .. TO ..` pairs allowed; relationship tables cannot have a primary key | same page | read | fixes expected in heldout/ladybug-crew-assignment...; "Cites needs a primary key" is a manufactured finding in the clean case | yes |
| Multiplicity keywords `MANY_ONE`, `ONE_MANY`, `MANY_MANY`, `ONE_ONE`; default is many-to-many | same page | read | selfcheck text only | no |
| `IF NOT EXISTS` on both statements; column `DEFAULT` values | same page | read | fixture of the clean case | no (fixture text) |
| Ordinary query clauses used in the LadybugDB query fixtures (`MATCH`, `WHERE`, `RETURN`, `ORDER BY`, `LIMIT`, `count`/`avg`, `$param`, `IS NULL`, `DISTINCT`) | https://docs.ladybugdb.com/cypher/syntax/ | not read | heldout/ladybug-crew-assignment..., heldout/ladybug-query-uses-a-relationship... | no. Those golds rest on table names and structure in the DDL. The clean LadybugDB case was made schema-only so that it does not depend on this |
| Recursive (variable-length) pattern syntax and its default upper bound | https://docs.ladybugdb.com/cypher/expressions/recursive-rel-functions | not read | nothing | no. Deliberately not used in any fixture or gold |
| Python package is `ladybug` on PyPI (earlier `real_ladybug`); a 0.19.1 release exists for the Rust crate `lbug` and the NuGet package | https://pypi.org/project/ladybug/ , https://docs.rs/crate/lbug/0.19.1 , https://www.nuget.org/packages/LadybugDB/ | not read (titles only) | nothing | no. No fixture names a package or a version |
| Kuzu was archived in October 2025 | the eval authors' brief | not checked | nothing | no |

## Neo4j and Cypher

None of the Neo4j pages could be read in either authoring session. The cases were arranged so that the
version-sensitive items are fixture text only. What the gold answers do rest on is the second table:
definitions of the language and the property-graph model that have not changed since openCypher 9. Four of
them were accepted by the maintainer on 2026-11-23; the rows still marked **not read** are unverified by this
eval's rule.

Fixture text only (a mistake here would show up as an agent finding on that file, not as a wrong gold answer):

| Fact | Source | Status | Used by |
|---|---|---|---|
| `CREATE CONSTRAINT name IF NOT EXISTS FOR (n:Label) REQUIRE n.prop IS UNIQUE` | https://neo4j.com/docs/cypher-manual/current/schema/constraints/create-constraints/ , https://neo4j.com/docs/cypher-manual/5/constraints/syntax/ | not read | every Neo4j schema fixture |
| `CREATE INDEX name IF NOT EXISTS FOR (n:Label) ON (n.prop)` | https://neo4j.com/docs/cypher-manual/current/indexes/search-performance-indexes/create-indexes/ | not read | dev/cypher-schema-enrollment..., heldout/cypher-query-arrow... |
| `UNWIND $rows AS row MERGE ... SET ...` load statements | Cypher manual (clause pages not looked up) | not read | load/ingest fixtures |
| Python driver: `session.run(query, **params)`, `.single()`, records readable as mappings | https://neo4j.com/docs/api/python-driver/current/api.html | not read | heldout/neo4j-client-walks-referral-tree... |
| Composite index `CREATE INDEX name IF NOT EXISTS FOR (n:Label) ON (n.a, n.b)` | https://neo4j.com/docs/cypher-manual/current/indexes/search-performance-indexes/create-indexes/ | not read | heldout/cypher-listing-city-slug... (the before/after timings are the fixture README's own claim, not an engine fact) |
| `shortestPath((a)-[:T*..40]-(b))`, `none(x IN list WHERE ...)`, `ON CREATE SET`, `DETACH DELETE`, `SET n:Label`, `date()`/`datetime()` | Cypher manual (pages not looked up) | not read | fixtures and selfcheck fixes of the second-round Neo4j cases |
| Four parallel writers running MERGE on a property with no uniqueness constraint can each create the node | https://neo4j.com/developer/kb/understanding-how-merge-works/ (title located by search, 2026-11-23) | not read | expected-outcome text of heldout/cypher-loader-merges-on-a-property-the-schema-never-constrains; its judge question also passes on the accepted scan fact alone |

Definitions the gold answers rest on:

| Definition | Source to read | Status | Gold answers that rest on it |
|---|---|---|---|
| A relationship pattern with `*` and no bounds has no upper limit on the number of hops; `*1..6` bounds it | https://neo4j.com/docs/cypher-manual/current/patterns/variable-length-paths/ , https://neo4j.com/docs/cypher-manual/current/patterns/reference/variable-length-paths/ | accepted | dev/cypher-queries-unbounded-follow-walk... (follower_reach); the fix expected in heldout/neo4j-client-walks-referral-tree...; heldout/cypher-large-grid-repo... (downstream_meters is the defect; zone_rollup, the same syntax over a four-level tree, is the sound look-alike) |
| Two `MATCH` patterns that share no variable return every combination of their rows | https://neo4j.com/docs/cypher-manual/current/patterns/ | accepted | dev/cypher-queries-unbounded-follow-walk... (listener_stats) |
| A directed pattern `(a)-[:T]->(b)` only matches relationships stored from a to b | https://neo4j.com/docs/cypher-manual/current/patterns/ | accepted | heldout/cypher-query-arrow-points-against-the-ingest-direction |
| Relationships carry properties and connect exactly two nodes; a relationship cannot be the start or end of another relationship | https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/ | not read | dev/cypher-schema-enrollment... (fix), heldout/cypher-credit-node-is-justified... (why the Credit node is right), dev/cypher-visit-node-carries-its-own-relationships... (why the Visit node is right) |
| Looking a node up by a property that has no index or constraint means examining every node with that label | https://neo4j.com/docs/cypher-manual/current/indexes/search-performance-indexes/using-indexes/ | accepted | heldout/cypher-loader-merges-on-a-property-the-schema-never-constrains (MERGE and MATCH on `accession_no`); `legacy_ref` in heldout/cypher-large-grid-repo... (a harmless instance: a few calls a week). `host_by_serial` in heldout/cypher-query-arrow... has this defect too and stays ungraded (EVALS.md, Open questions) |
| `MERGE` matches its whole pattern, property map included, or creates all of it: `MERGE (s:Subscriber {email: e, plan: p})` finds no node once the stored plan differs, and creates a second node with that email | https://neo4j.com/developer/kb/understanding-how-merge-works/ (title located by search, 2026-11-23), https://neo4j.com/docs/cypher-manual/current/clauses/merge/ | **not read, not on the accepted list** | dev/cypher-loader-merges-on-a-changing-property-beside-naming-quirks: the whole gold answer. Needs the maintainer's acceptance or one reading; if it fails, the case comes out |

The supernode case (heldout/cypher-recommendation-expands-every-customer...) rests on the pattern's shape and the
cardinalities stated in its own README, not on an engine fact.

## SQLite

| Fact | Source | Status | Used by |
|---|---|---|---|
| Declaring a foreign key creates no index on the referencing columns (`PRAGMA index_list` shows none) | executed; see also https://www.sqlite.org/foreignkeys.html (located through its www2 mirror, not read) | executed | dev/sqlite-dependency-table... |
| A composite primary key serves lookups on its leading column only; `EXPLAIN QUERY PLAN` shows `SCAN d` for the reverse lookup and `SEARCH ... USING ... INDEX ... (depends_on_id=?)` once an index leading with `depends_on_id` exists | executed against the case's generated database | executed | dev/sqlite-dependency-table... (also done by its check.py) |
| A join with no usable index can get `AUTOMATIC ... INDEX` in the plan, rebuilt on each run | executed; see also https://www.sqlite.org/draft/optoverview.html (not read) | executed | dev/sqlite-dependency-table... (expected outcome text) |
| `WITH RECURSIVE` works, including carrying a multiplied quantity and a depth guard | executed (SQLite 3.53.1); see also https://sqlite.org/lang_with.html (not read) | executed | fixes expected in heldout/sqlite-bom-explosion..., heldout/sqlite-folder-tree...; fixtures of the clean forum case |
| `LIKE` is case-insensitive for ASCII and treats `%` and `_` as wildcards; `replace()` is case-sensitive | executed | executed | heldout/sqlite-folder-tree... |
| The wrong results claimed for the folder case (sibling folder matched by the subtree statement; rename rewriting other folders) | executed against the case's generated database | executed | heldout/sqlite-folder-tree... |
| The truncation claimed for the BOM case (62 of 90 components missing for PUMP-9000) | executed against the case's generated database, at build time | executed | heldout/sqlite-bom-explosion... |
| Every statement of the clean forum case uses an index (no `SCAN` of a base table) | executed against the case's generated database | executed | heldout/sqlite-sound-threaded-forum... |
| `WITHOUT ROWID`, `CHECK` constraints, `ALTER TABLE ... ADD COLUMN ... REFERENCES` | executed | executed | fixtures and selfcheck fixes |

| Second round: on `territory`, the CHECK plus the composite foreign key onto `UNIQUE (id, level)` reject a skipped level, a level above 5, re-parenting onto a deeper node, giving the root a parent, and changing the level of a node that has children (five attempts, all refused with foreign keys on); so no cycle and at most six levels | executed against the case's generated database | executed | dev/sqlite-territory-walks-have-no-depth-guard... |
| The three unguarded recursive statements of that case finish and every recursive step is an index or primary-key search | executed (`EXPLAIN QUERY PLAN`) | executed | dev/sqlite-territory-walks-have-no-depth-guard... |
| `can_swap_for` does not finish for 53 of the 61 ingredients in the generated database; replacing `UNION ALL` with `UNION` while keeping the counter column still does not finish; `UNION` on the id alone returns the 9 ingredients reachable from butter; so does a cap of 6 swaps | executed with a progress-handler cut-off | executed | heldout/sqlite-substitute-walk-never-ends... (the last one is also what its check.py does to a statement from the output) |
| `SELECT blocker_id FROM block WHERE blocked_id = ?` plans as `SCAN block USING COVERING INDEX block_recent` (every entry read; unchanged after `ANALYZE`), and as a `SEARCH ... (blocked_id=?)` once an index leading with `blocked_id` exists; the other four statements in social.py are searches | executed against the case's generated database and in its check.py | executed | heldout/sqlite-block-table-keys-cannot-serve... |
| With all five migrations applied, `blocked_by` and both steps of `blocker_chain` are searches on `issue_link_dst`; every other statement is an index search with no sort of a large set; `blocker_chain` finishes on the blocking loop in the sample | executed against the case's generated database | executed | heldout/sqlite-link-table-reverse-lookup-is-indexed-in-a-later-migration |

## PostgreSQL

heldout/sql-membership-table-keeps-its-own-id... is written as PostgreSQL 16 DDL and queries and cannot be
executed here. Its schema and all six statements were run through SQLite only to catch typos and to confirm
that each statement has a usable index (every plan is a search). The gold answer rests on the lifecycle
described in the README and on the foreign keys that reference `circle_membership.id`, not on an engine fact.
Partial unique indexes (`CREATE UNIQUE INDEX ... WHERE ended_at IS NULL`) are fixture text and were **not
read** against https://www.postgresql.org/docs/current/indexes-partial.html .

The decoy case dev/sql-closure-table-is-right... is written as PostgreSQL DDL and cannot be executed here.
Nothing in its gold answer is PostgreSQL-specific: the decoy rests on the workload in its README and the defect
(a delimited id list in a text column) is engine-independent. `WITH RECURSIVE` inside its rebuild script is
fixture text and was **not read** against https://www.postgresql.org/docs/18/queries-with.html .

## NetworkX and Python

| Fact | Source | Status | Used by |
|---|---|---|---|
| `nx.shortest_path(G, s, t, weight=...)`, `nx.dijkstra_path`, `nx.path_weight`, `nx.single_source_dijkstra_path_length` exist in 3.7 | executed (`inspect.signature`) ; see also https://networkx.org/documentation/latest/reference/algorithms/shortest_paths.html (not read) | executed | dev/networkx-route-finder... |
| The shipped `find_route` differs from the weighted shortest path for 36 of 41 stops from DEPOT | executed at build time | executed | dev/networkx-route-finder... |
| `nx.pagerank(G, alpha=0.85, ...)` exists and its scores sum to 1 on a graph with dangling nodes; the hand-written version sums to 0.344 on the shipped export | executed | executed | heldout/networkx-page-scores... |
| A weight function passed to the Dijkstra family receives the two endpoints and the edge's attribute dictionary, nothing else, so it cannot depend on arrival time | executed (docstring of `nx.dijkstra_path` in 3.7) | executed | heldout/networkx-timetable-search... (why the custom search is justified) |
| `earliest_arrival` in that case is correct: it agrees with a brute-force relaxation on 25 random queries | executed | executed | heldout/networkx-timetable-search... |
| `reachable_from` raises `RecursionError` on the shipped timetable from city stops; the default recursion limit is 1000; `nx.descendants` returns the same set | executed | executed | heldout/networkx-timetable-search... |
| `nx.dag_longest_path(G, weight='weight', default_weight=1)` sums edge weights; `slowest_chain` in the clean case agrees with it once node times are copied onto edges | executed | executed | heldout/networkx-sound-build-graph... |
| `nx.descendants`, `nx.ancestors`, `nx.topological_generations`, `nx.lexicographical_topological_sort`, `nx.find_cycle`, `nx.is_directed_acyclic_graph`; the clean case's own tests pass | executed | executed | heldout/networkx-sound-build-graph... |
| With edges added from a dataset to its inputs, `nx.descendants` returns a dataset's sources and `nx.ancestors` what is built from it: on the shipped CSVs `blast_radius(G, 'raw_purchase_orders')` is empty while 26 datasets depend on that table, and `blast_radius` of `report_board_pack` returns its 14 sources; the bundled tests pass | executed | executed | dev/networkx-blast-radius-walks-toward-sources... |
| `nx.articulation_points`, `nx.bridges`, `nx.connected_components`, `nx.maximum_flow_value` on an undirected `Graph` with a `capacity` attribute, `nx.multi_source_dijkstra_path_length(G, sources, weight=None)` (hop counts); the seven bundled tests pass and the report runs on the shipped CSVs | executed | executed | heldout/networkx-sound-network-audit... |
| `nx.maximum_flow_value` raises `NetworkXError` on a `MultiGraph` ("not supported (yet)"), which is why the case's `bundled` projection is needed | executed | executed | heldout/networkx-sound-network-audit... (why folding parallel links is right) |

## Conventions graded as contract

The path `docs/graph/ROAST.md` and the footer line `Roasted with erdostack: npx skills add usergraphtheory/erdostack`
come from the eval authors' brief (shared conventions of the erdostack skills), not from an outside source.

## Data

All fixtures were written for this eval. Names, counts and schemas are invented; the generated databases and CSVs
come from the seeded `setup.py` in each case. Nothing is taken from a book, vendor documentation, another
repository or any private project.
