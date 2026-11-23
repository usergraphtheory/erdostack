# Roadmap

What is planned, in what order, and what has to be true before each phase is called done. Nothing here promises a date.

## Skill inventory

**U** is user-invoked, **M** is model-invoked. No skill has shipped yet.

| Skill | Type | Phase | What it does | Writes |
|---|---|---|---|---|
| `roast-my-graph` | U | 1 | **Entry point.** Audits a schema, model or query file (graph or relational) and returns real findings with severity and fixes, with jokes. `--serious` drops the jokes | `docs/graph/ROAST.md` |
| `graph-or-not` | U | 1 | Decides between a graph database, an in-process library, recursive SQL, or nothing | `docs/graph/DECISION.md` |
| `setup-graph` | U | 1 | Once per repo: engine, version, driver, how to run queries, read-only or write, where the schema snapshot lives | `docs/graph/CONTEXT.md` |
| `schema-first` | M | 1 | Introspect before writing; validate labels, types, direction, properties | Schema snapshot |
| `query-review` | M | 1 | EXPLAIN or PROFILE before run; anti-pattern checks; bounded writes; parameterization | Review notes |
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

Engine-specific detail lives in `references/engines/<engine>.md`, loaded only when `CONTEXT.md` names that engine. Two packs are seeded, both for engines that run locally with no account:

- **Neo4j**: a server, run in a container.
- **LadybugDB**: the maintained Kuzu fork. Embedded, in-process, MIT licensed.

The third slot is left for the first outside contributor. After that the rest open up, in no particular order: Amazon Neptune, Apache AGE, ArangoDB, ArcadeDB, Dgraph, DuckPGQ, FalkorDB, JanusGraph, Memgraph, NebulaGraph, Spanner Graph, SurrealDB, TigerGraph. Each pack ends with a pointer to the vendor's own skills where they exist.

A pack is only accepted from someone who can test against the real engine. Emulators that substitute a different query engine do not count, so packs for cloud-only engines need a contributor with access to a real cluster.

### Why LadybugDB is the second engine

It installs as a library, so the eval harness and any reader can run it with no server, container or account. It speaks Cypher but is not Neo4j, so it exercises the dialect skill. It is also a live stale-knowledge trap: Kuzu was archived in October 2025, the fork ships under different package names, and agents still reach for the old ones. If it does not hold up under real use before launch, the fallbacks are Memgraph or Apache AGE.

### Possible later bet

A skill for querying codebase knowledge graphs well. Decided after Phase 3, based on demand.

## Phases and exit gates

### Phase 0: foundations

- [x] Repo skeleton: `skills/`, `references/engines/`, `evals/`, thin manifests per host over the same markdown, release pipeline.
- [ ] Eval harness: a fixed task set on public datasets, run with and without skills, on at least two models. Neo4j runs in a container; LadybugDB runs in-process. No cloud account is needed.
- [ ] A failure log from real use, which seeds the eval cases.

**Gate:** the harness runs end to end and produces a baseline number.

### Phase 1: the wedge

- [ ] Five skills: `roast-my-graph`, `graph-or-not`, `setup-graph`, `schema-first`, `query-review`.
- [ ] Daily use on both seeded engines; anything not reached for weekly gets pruned.

**Gate:** a measured with-versus-without result worth stating, including where it made no difference; install tested on a clean machine per OS; at least one person who is not the author has used it.

### Phase 2: launch and depth

- [ ] First tagged release with the Phase 1 five.
- [ ] `query-dialects`, `graph-modeling`, `algorithm-picker`, `graph-crdts`, `graphs-in-process`, `graphs-in-sql`, on a regular release rhythm.
- [ ] The Neo4j and LadybugDB packs; the contributor path opens.

**Gate:** every new skill has eval cases; contributions are merged or absorbed quickly.

### Phase 3: workflows and loops

- [ ] `graph-import`, `graph-migrate`, `graph-testing`, `graph-evals`, `graph-rag`, `graph-viz`, the router and the meta-skill.
- [ ] An agent scorecard: how well each model writes each dialect, with and without the skills, re-run on each major model release.
- [ ] Skills nobody uses are retired.
