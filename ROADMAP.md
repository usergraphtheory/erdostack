# Roadmap

What is planned, in what order, and what has to be true before each phase is called done. Nothing here promises a date.

## Skill inventory

**U** is user-invoked, **M** is model-invoked. The five Phase 1 skills are released, and each has passed an eval gate on cases written from documented problems; [BENCHMARK.md](BENCHMARK.md) has the results and says how narrow each claim is. The rest are planned.

| Skill | Type | Phase | What it does | Writes |
|---|---|---|---|---|
| `roast-my-graph` | U | 1 | **Entry point.** Audits a schema, model or query file (graph or relational) and returns real findings with severity and fixes, with jokes. `--serious` drops the jokes | `docs/graph/ROAST.md` |
| `graph-or-not` | U | 1 | Decides between a graph database, an in-process library, recursive SQL, or nothing, and records the decision for later sessions | `docs/graph/DECISION.md` |
| `setup-graph` | U | 1 | Once per repo: engine, version, driver, how to run queries, read-only or write, where the schema snapshot lives | `docs/graph/CONTEXT.md` |
| `schema-first` | M | 1 | Introspect before writing; validate labels, types, direction, properties | Schema snapshot |
| `query-review` | M | 1 | Bulk changes scoped to the repo's rule, batched, proven on a copy and handed back for review; a wrong lint or review flag answered, not obeyed. Read-query checks were tried and dropped: no measured gain | Review note, appended to `docs/graph/REVIEW.md` when `docs/graph/` exists |
| `query-dialects` | M | 2 | Version-aware matrix across Cypher 25, openCypher, GQL, SQL/PGQ, Gremlin, SPARQL, AQL, GSQL. Rule: check, do not recall. First content: the Neo4j versus LadybugDB Cypher gap | n/a |
| `graph-modeling` | M | 2 | Node, edge or property; reification; supernodes; temporal and versioned graphs; relational to graph | Model sketch |
| `algorithm-picker` | M | 2 | Problem to algorithm to complexity to the library call or engine procedure; exact or approximate | n/a |
| `graph-crdts` | M | 2 | Replicated graphs and trees: add and remove semantics, concurrent delete versus edge creation, move operations, tombstones, which library fits | Merge-semantics note |
| `graphs-in-process` | M | 2 | NetworkX, igraph, rustworkx, graph-tool, GPU options; when to move off each | n/a |
| `graphs-in-sql` | M | 2 | Recursive CTEs, adjacency and closure tables, SQL/PGQ where it really exists, Apache AGE, DuckPGQ | n/a |
| `graph-import` | U | 3 | Constraints first, idempotent batched loads, id mapping, bulk loaders | Load plan |
| `graph-migrate` | U | 3 | Engine to engine and relational to graph, with dialect diffs and count and sample verification | Migration plan |
| `graph-testing` | U | 3 | Small deterministic fixture graphs, golden results, containerized engines, and what a local emulator does and does not prove | Test scaffolding |
| `graph-evals` | U | 3 | Builds a question-to-query eval set for the user's own schema; runs with and without skills | Eval report |
| `graph-rag` | U | 3 | Engine-neutral blueprint: extraction, entity resolution, hybrid retrieval; routes to vendor skills | Design note |
| `graph-viz` | M | 3 | Renders a schema or subgraph as Mermaid, DOT or HTML | Image or HTML |
| `graph` (router) | U | 3 | Picks the right skill once there are enough to need routing | n/a |
| `write-graph-skill` | U | 3 | Meta-skill: house style for new skills and engine packs | New skill folder |

### Engine packs

Engine-specific detail lives in `references/engines/<engine>.md`, loaded only when `CONTEXT.md` names that engine. No pack is written yet. The first two are planned, both for engines that run locally with no account:

- **Neo4j**: a server, run in a container.
- **LadybugDB**: a maintained Kuzu fork. Embedded, in-process, MIT licensed (its repository, checked 2026-11-27).

The third slot is left for the first outside contributor. After that the rest open up, in no particular order: Amazon Neptune, Apache AGE, ArangoDB, ArcadeDB, Dgraph, DuckPGQ, FalkorDB, JanusGraph, Memgraph, NebulaGraph, Spanner Graph, SurrealDB, TigerGraph. Each pack ends with a pointer to the vendor's own skills where they exist.

A pack is only accepted from someone who can test against the real engine. Emulators that substitute a different query engine do not count, so packs for cloud-only engines need a contributor with access to a real cluster.

### Why LadybugDB is the second engine

It installs as a library, so the eval harness and any reader can run it with no server, container or account. It speaks Cypher but is not Neo4j, so it exercises the dialect skill. It is also a live stale-knowledge trap: Kuzu's repository was archived on 10 October 2025 at 0.11.3, the fork ships under different package names, and agents still reach for the old ones. If it does not hold up under real use before launch, the fallbacks are Memgraph or Apache AGE.

### Possible later bet

A skill for querying codebase knowledge graphs well. Decided after Phase 3, based on demand.

## Phases and exit gates

### Phase 0: foundations

- [x] Repo skeleton: `skills/`, `references/engines/`, `evals/`, thin manifests per host over the same markdown, release pipeline.
- [x] Eval harness: task sets on public or generated data, run with and without skills, on two models, with a paired test and a blind judge that is itself checked. No cloud account is needed.
- [ ] Live engines in the harness: Neo4j in a container and LadybugDB in-process. Today's cases run SQLite and NetworkX and analyse Cypher statically.
- [ ] A failure log from real use, which seeds the eval cases.

**Gate:** the harness runs end to end and produces a baseline number.

### Phase 1: the wedge

- [x] Five skills written and gated: `roast-my-graph`, `graph-or-not`, `setup-graph`, `schema-first`, `query-review`.
- [x] A register of documented graph problems (`evals/REAL_PROBLEMS.md`), and every skill gated again on cases written from it, with an arm-blind review of failing grades.
- [x] All five passed a gate on register cases: `roast-my-graph` (version 3), `schema-first`, `graph-or-not` (after three misses), `setup-graph` (version 4, for three kinds of repo) and `query-review` (version 7, for bulk changes aimed at production).
- [x] A core set of thirty cases staged on the schema and tasks of two LDBC benchmarks, and one pooled test on it passed. It is LDBC-derived work, not an LDBC Benchmark Result. The whole case library is published separately as `erdostack/bench`.
- [x] An audit of passing grades, after the gates: readers who were shown no grade and no arm checked every run that passed with a skill against its requirements and found none false (`evals/PASS_AUDIT.md`).
- [x] A look at the conditions of the runs themselves, after the results: what an agent could read and what it had been given besides the request, and a re-run of 100 runs under a tripwire, in which no session opened a case, a grader, a result or a skill it had not been given. It measures today's sessions, not the recorded ones (`evals/RUN_CONDITIONS.md`).
- [ ] A clean run of the core set: a headless client started from an empty home, on a machine that does not hold the cases. Every run so far was made inside the maintainer's own agent session, which gives both arms this repository's `AGENTS.md` and the maintainer's notes. Until this is done, "without the skill" does not mean a bare agent.
- [ ] The harness: move `meta.json`, which names the case and the arm, out of the run directory the agent is pointed at; save what a session is given with its run; run the tripwire with every gate, with a sentinel in every wave and an idle control longer than the host's ten-minute cycle.
- [ ] `setup-graph` grading: bring the grader and the cases' requirement sentences into line. The sentences ask for the library and for the locked version, and the grader also accepts two forms of answer that put them second (`engine: none` followed by the library; a manifest's version requirement followed by the locked version), the first since its first version and the second since the gate's own blind audit of failing grades. The audit's readers followed the sentences and called the three such unaided records they met unmet, and a search found twelve more unaided passes of those forms that nobody had read. Decide which is right, change the other, say so in `evals/setup-graph/EVALS.md`, and if the grader changes, grade both arms again. Until then the results stand as graded, which is the kinder reading for an unaided agent.
- [ ] `graph-or-not` grading: the check for invented facts cannot see a false statement that names no figure; the audit's readers found one unaided reply passed that way. Give that requirement to a blind judge in the next revision of the cases.
- [ ] Read more of the unaided passes: the audit read 44 of 559.
- [ ] The next audit: run the readers on a machine that does not hold the grades, record which files each one opens, strip the lines in which a skill's output names the package, put an output known to fail in every batch, and publish the protocol before the first read so that its date is not ours to assert.
- [ ] Run the Cypher cases against live Neo4j and LadybugDB. Everything so far analyses Cypher statically.
- [ ] `query-review`: test a Cypher change on a live development database. With a stand-in that only logs, the skill held changes the bare agents sent.
- [ ] `roast-my-graph`: a whole-pattern `MERGE` that duplicates nodes was found and under-rated by both models in the core set. Fix it in the next version and gate on fresh cases.
- [ ] `graph-or-not`: Haiku with the skill took 1.75 times as long as without in its gate and 5.7 times as long on the core set. Find out why.
- [ ] `setup-graph`: the two cases it lost, and a gain on ordinary repos, which two gates did not show.
- [ ] An outside replication: somebody who is not the author runs the core set and publishes what they get.
- [ ] Daily use on both planned engines; anything not reached for weekly gets pruned.

**Gate:** a measured with-versus-without result worth stating, including where it made no difference; install tested on a clean machine per OS; at least one person who is not the author has used it.

### Phase 2: launch and depth

- [x] First tagged release, with the five Phase 1 skills and the benchmark.
- [ ] `query-dialects`, `graph-modeling`, `algorithm-picker`, `graph-crdts`, `graphs-in-process`, `graphs-in-sql`, on a regular release rhythm.
- [ ] The Neo4j and LadybugDB packs; the contributor path opens.

**Gate:** every new skill has eval cases; contributions are merged or absorbed quickly.

### Phase 3: workflows and loops

- [ ] `graph-import`, `graph-migrate`, `graph-testing`, `graph-evals`, `graph-rag`, `graph-viz`, the router and the meta-skill.
- [ ] An agent scorecard: how well each model writes each dialect, with and without the skills, re-run on each major model release.
- [ ] Skills nobody uses are retired.
