<p align="center">
  <img src="https://raw.githubusercontent.com/usergraphtheory/erdostack/main/assets/logo.svg" width="96" height="96" alt="erdostack logo: three joined vertices drawn in chalk on a chalkboard, one of them yellow">
</p>

<h1 align="center">erdostack</h1>

<p align="center">
  <strong>Graph skills for coding agents.</strong><br>
  Graph databases, graph algorithms, data structures and visualization in one vendor-neutral skill profile.<br>
  <a href="https://erdostack.com">erdostack.com</a>
</p>

<p align="center">
  <a href="https://github.com/usergraphtheory/erdostack/actions/workflows/ci.yml"><img src="https://github.com/usergraphtheory/erdostack/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/usergraphtheory/erdostack/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-93cbe8?labelColor=22302a" alt="MIT license"></a>
  <a href="https://github.com/usergraphtheory/erdostack/releases"><img src="https://img.shields.io/github/v/tag/usergraphtheory/erdostack?label=release&color=f0d264&labelColor=22302a" alt="Latest release"></a>
  <a href="https://github.com/usergraphtheory/erdostack/blob/main/BENCHMARK.md"><img src="https://img.shields.io/badge/benchmark-with%20vs%20without-f0d264?labelColor=22302a" alt="Benchmark: with the skill against without"></a>
  <a href="https://agentskills.io"><img src="https://img.shields.io/badge/format-Agent%20Skills-edeae0?labelColor=22302a" alt="Agent Skills format"></a>
</p>

```bash
npx skills add usergraphtheory/erdostack
```

> **Five skills, each one measured.** Every skill here beat the same agent without it at one specific thing, on cases it was never tuned against, before it shipped. The numbers, the method and every test that missed on the way are in [BENCHMARK.md](https://github.com/usergraphtheory/erdostack/blob/main/BENCHMARK.md). What comes next is in the [roadmap](https://github.com/usergraphtheory/erdostack/blob/main/ROADMAP.md).

## Where your agent is confidently wrong about graphs

Coding agents write decent application code, and most of the time decent graph code too. Then, some of the time, they walk into a graph like it owes them money. They write last year's Cypher. They write one engine's Cypher for a different engine. They invent labels, point relationships the wrong way, and ship queries that are fine on 100 nodes and a denial of service on 100 million. Ask for a data model and you get a relational schema in a trench coat.

erdostack is the engine-neutral layer: decide whether you need a graph at all, model it, query it in the right dialect and version, pick the algorithm instead of reinventing it, and avoid melting the database. That is the plan. Five skills of it exist today, and [Measured](#measured) says what each one was shown to do and what it was not.

It is a set of small, composable [Agent Skills](https://agentskills.io) that you adapt to your repo. It is not a process framework and it does not take over your workflow. Where a database vendor publishes its own skills, erdostack routes to them instead of competing with them.

## What it fixes

| What the agent does | Skills | What changes |
|---|---|---|
| **Stale or wrong-engine syntax.** Writes last year's Cypher, writes one engine's Cypher for another, installs the `kuzu` package (repository archived on 10 October 2025, at 0.11.3) instead of a maintained fork, or assumes SQL/PGQ shipped in PostgreSQL 19 (it was reverted on 7 September 2026, before release) | `query-dialects` | The agent states engine and version, checks support, then writes |
| **Schema hallucination.** Invents labels and properties, reverses relationship direction | `schema-first`, `setup-graph` | The schema is read and written down, and a later session writes its queries from that snapshot instead of guessing |
| **Works on 100 nodes, dies on 100M.** A purge or backfill that touches the wrong rows, runs as one giant transaction, or is run straight on production because somebody asked | `query-review` | A bulk change aimed at production is scoped to the repo's own rule, batched, and handed back for review instead of run. Read-query tuning (cartesian products, unbounded paths) is left to the model: in our tests it already does that without help |
| **Graph-shaped hammer.** Reaches for a graph database, or refuses one, without looking at the workload | `graph-or-not` | A short written decision with the cheaper alternatives considered |
| **Tables in a trench coat.** Join tables as nodes, everything as a property, the wrong algorithm reimplemented by hand | `graph-modeling`, `algorithm-picker`, `roast-my-graph` | A model review with named anti-patterns; a library call or engine procedure instead of hand-rolled code |
| **Last-write-wins brain.** Syncs a shared graph by overwriting, leaving dangling edges, resurrected nodes or cycles after concurrent edits | `graph-crdts` | Merge semantics are chosen and written down before any sync code |

Five of these skills are in this release; the rest are on the roadmap. Every skill maps to one of these rows, and a proposed skill with no row gets cut.

## Who it is for

**For you if** you point a coding agent at a graph database; write Cypher for more than one engine; keep graphs in plain SQL, NetworkX or another in-process library; need to pick a graph algorithm or draw a graph; sync graph-shaped data between replicas; or are trying to work out whether you need a graph database at all.

**Not for you if** you want deep coverage of a single vendor's product (use that vendor's own skills), or a tool that turns your codebase into a knowledge graph (a different and already crowded category).

## Install

The one-liner above uses the open [skills CLI](https://github.com/vercel-labs/skills), which works with Claude Code, Cursor, Codex, Gemini CLI, Copilot, OpenCode and most other agents. Every path below reads the same markdown.

| Host | Command | Model |
|---|---|---|
| Any agent | `npx skills add usergraphtheory/erdostack` | own |
| GitHub CLI | `gh skill install usergraphtheory/erdostack` | own |
| Claude Code | `/plugin marketplace add usergraphtheory/erdostack` then `/plugin install erdostack@erdostack` | subscribe |
| Codex | `codex plugin marketplace add usergraphtheory/erdostack` then `codex plugin add erdostack@erdostack` | subscribe |
| Copilot CLI | `copilot plugin install usergraphtheory/erdostack` | subscribe |
| Gemini CLI | `gemini extensions install https://github.com/usergraphtheory/erdostack` | subscribe |
| Cursor | `npx skills add usergraphtheory/erdostack -a cursor` (marketplace listing to follow) | own |
| npm | `npx erdostack install` | own |
| PyPI | `uvx erdostack install` | own |

**Subscribe or own, not both.** A plugin install *subscribes*: updates arrive when a new version is released. A file install *owns*: the skills are copied into your project and are yours to edit. Pick one per project, or your agent sees two copies of every skill.

**Teams.** Commit the copied skills (for example `.agents/skills/`) so everyone who clones the repo gets them, or register the marketplace in your shared agent settings. [docs/INSTALL.md](https://github.com/usergraphtheory/erdostack/blob/main/docs/INSTALL.md) covers both, plus per-agent directories, pinning and uninstalling.

**No telemetry.** erdostack makes no network calls, collects nothing, runs no install scripts and does not auto-update. The `erdostack` installers on npm and PyPI only copy files. Third-party installers have their own policies: the skills CLI, for one, sends anonymous install telemetry unless you set `DISABLE_TELEMETRY=1`.

## What a roast looks like

Start with `roast-my-graph`. Point it at a schema, a loader or a folder of queries and it tells you what is wrong, how bad it is and how to fix it. This is what it wrote for "the new member profile pages go live next week. roast townsquare-graph for me", with cuts marked `[...]`:

```markdown
# Roast: townsquare-graph (schema, nightly load, page queries)

Verdict: Not ready for next week. Nothing in the schema or the load is wrong, but `person_friends` walks
KNOWS against the way the loader stores it and shows every member only the friends with a higher id. Fix
that one line and the rest is sound.

[...]

### critical: `person_friends`
The friends tab has been told that friendship is a one-way street, and the loader has been told it is a
two-way street, and they have never been introduced. Half the town is invisible to the other half.
Problem: When `person_friends` runs for a person, `(p)-[k:KNOWS]->(friend)` matches only relationships
stored out of that person, and `load/02_knows.cypher` stores each pair from the lower id to the higher. So
a member sees only friends with a higher id. On the shipped data it returns 900 of the 1800 friendship
ends; 41 of 260 people have friends and get an empty tab (person 250 has 5 friends and sees 0). [...] No
error is raised.
Fix: Make the pattern undirected and leave the loader alone [...]

[...]

## Holds up
- `friend_count`: the undirected `COUNT { (p)-[:KNOWS]-(:Person) }` is the right read of a one-per-pair
  store [...]. It is the correct number; it is `person_friends` that disagrees with it.
- Nightly load: every step is a MERGE keyed on the id alone with the rest set afterwards, so a rerun
  creates no duplicates [...]

## Not checked
- No Neo4j or `cypher-shell` on this machine, so nothing was run as Cypher and no plans were read. [...]
```

That is a recorded run: Claude Sonnet with the skill on the case [`cypher-member-profile-queries-and-the-nightly-graph-load`](https://github.com/erdostack/bench/tree/main/evals/roast-my-graph/standards/cypher-member-profile-queries-and-the-nightly-graph-load), a small generated repository you can run it on yourself. Its schema is adapted from the LDBC Social Network Benchmark ([attribution](https://github.com/usergraphtheory/erdostack/blob/main/BENCHMARK.md#attribution)). The part that was measured is "Holds up". A bare model finds the bug too; what the skill changes is that the review stops calling sound designs broken ([Measured](#measured)). `--serious` drops the jokes.

## The skills

The five Phase 1 skills are in this release, and each has passed its eval gate ([Measured](#measured)). The others are planned, in the order shown. **U** is user-invoked: you call it. **M** is model-invoked: the agent picks it up when the task calls for it.

| Skill | Type | Phase | What it does |
|---|---|---|---|
| `roast-my-graph` | U | 1 | **Start here.** Audits a schema, model or query file (graph or relational) and returns real findings with severity and fixes, with jokes. `--serious` drops the jokes |
| `graph-or-not` | U | 1 | Decides between a graph database, an in-process library, recursive SQL, or nothing, and writes the decision down so the next session builds on it instead of deciding again |
| `setup-graph` | U | 1 | Once per repo: engine, version, driver, how to run queries, read-only or write, where the schema snapshot lives. Read from the lockfile, image pin or override that decides, not from the README |
| `schema-first` | M | 1 | Introspects before writing; validates labels, types, direction and properties |
| `query-review` | M | 1 | Before a job changes or deletes many rows: finds the repo's rule for it, scopes and batches the change, proves it on a copy and hands production back for review. When a linter or reviewer flags code that is right, leaves it alone and says why. Not for tuning read queries |
| `query-dialects` | M | 2 | Version-aware matrix across Cypher 25, openCypher, GQL, SQL/PGQ, Gremlin, SPARQL, AQL and GSQL. The rule: check, do not recall |
| `graph-modeling` | M | 2 | Node, edge or property; reification; supernodes; temporal and versioned graphs; relational to graph |
| `algorithm-picker` | M | 2 | Problem to algorithm to complexity to the library call or engine procedure; exact or approximate |
| `graph-crdts` | M | 2 | Replicated graphs and trees: add and remove semantics, concurrent delete versus edge creation, move operations, tombstones |
| `graphs-in-process` | M | 2 | NetworkX, igraph, rustworkx, graph-tool, GPU options; when to move off each |
| `graphs-in-sql` | M | 2 | Recursive CTEs, adjacency and closure tables, SQL/PGQ where it really exists, Apache AGE, DuckPGQ |
| `graph-import` | U | 3 | Constraints first, idempotent batched loads, id mapping, bulk loaders |
| `graph-migrate` | U | 3 | Engine to engine and relational to graph, with dialect diffs and count and sample verification |
| `graph-testing` | U | 3 | Small deterministic fixture graphs, golden results, containerized engines |
| `graph-evals` | U | 3 | Builds a question-to-query eval set for your own schema; runs with and without skills |
| `graph-rag` | U | 3 | Engine-neutral blueprint: extraction, entity resolution, hybrid retrieval |
| `graph-viz` | M | 3 | Renders a schema or subgraph as Mermaid, DOT or HTML |
| `graph` | U | 3 | Router: picks the right skill once there are enough to need routing |
| `write-graph-skill` | U | 3 | House style for writing your own skills and engine packs |

Skills hand off through files in your repo, so one skill's output is the next one's input: `setup-graph` writes `docs/graph/CONTEXT.md`, `graph-or-not` writes `docs/graph/DECISION.md`, `schema-first` writes `docs/graph/schema.md`, `roast-my-graph` writes `docs/graph/ROAST.md`, and `query-review` appends its notes to `docs/graph/REVIEW.md` when that folder exists.

## Engine packs

Engine-specific detail will live in `references/engines/<engine>.md` and load only when your repo's `CONTEXT.md` names that engine. No pack is written yet. The first two are planned because both engines run locally with no account:

- **Neo4j**: a server, run in a container.
- **LadybugDB**: a maintained fork of Kuzu. Embedded, in-process, MIT licensed (its repository, checked 2026-11-27).

Until then the Phase 1 skills carry the engine notes they need in their own `references/` folder, so a skill installed on its own works.

The third slot is reserved for the first outside contributor. If you maintain or work on a graph engine, a pack is the highest-value thing you can add. See [CONTRIBUTING.md](https://github.com/usergraphtheory/erdostack/blob/main/CONTRIBUTING.md).

## Measured

No skill ships here until it beats the same agent without it. The same request goes to an agent with the skill and to one without, on Claude Haiku 5.5 and Claude Sonnet 5.5, on cases the skill was never tuned against, and scripts grade what the agent left behind. The bar is written down before the run. Reviewers who are not told which arm a run came from re-read every run that failed a scripted check, and the bar has to hold before and after that review.

| Skill | Cases | Passed with the skill | Without | Cases won / lost / tied | p |
|---|---|---|---|---|---|
| `roast-my-graph` | 120 | 223 of 240 runs | 191 of 240 | 29 / 8 / 83 | 0.0008 |
| `schema-first` | 20 two-session | 38 of 40 | 12 of 40 | 14 / 0 / 6 | 0.0001 |
| `graph-or-not` | 40 two-session | 77 of 80 | 35 of 80 | 30 / 1 / 9 | under 0.000001 |
| `setup-graph` | 80 | 156 of 160 | 139 of 160 | 16 / 2 / 62 | 0.0013 |
| `query-review` | 80 | 159 of 160 | 140 of 160 | 18 / 0 / 62 | 0.000008 |

Every case stages a problem from a [register of 34 graph problems](https://github.com/usergraphtheory/erdostack/blob/main/evals/REAL_PROBLEMS.md), 29 of them documented outside this project (a vendor's documentation, an engine's own error code, a public engineering write-up, most of them read as search excerpts) or reproduced on SQLite or NetworkX. A second, smaller set stages the same kinds of work on the schema and tasks of the LDBC Social Network Benchmark and LDBC Graphalytics: 30 cases, 11 won and none lost with the skills (p = 0.001). That set is not an LDBC Benchmark and these are not LDBC Benchmark Results: LDBC's benchmarks measure databases, and this measures agents. [BENCHMARK.md](https://github.com/usergraphtheory/erdostack/blob/main/BENCHMARK.md) has both, with the method, the cost and the commands to re-run it.

What each skill was shown to do, which is narrower than its name:

- **`roast-my-graph` adds restraint, not detection.** On the 42 cases where the design is sound, the agent with the skill passed 76 of 84 runs and the bare agent 43 of 84. On the 78 cases with a real defect they are level. It does not find more bugs than a bare model. It stops your agent calling a sound design broken.
- **`schema-first` works across sessions, not within one.** A later session writes correct queries from the snapshot an earlier one left. Without it, a bare model in the second session got 12 of 40 right: a misspelled attribute that silently counts one per edge, a double-quoted column SQLite reads as text, an edge read the wrong way round. Within a single session it adds nothing you can measure.
- **`graph-or-not` makes a decision last.** The next session builds what was decided instead of deciding again: 62 of 64 runs against 19 of 64 where the second request depends on the first. It does not decide better than a bare model in one sitting.
- **`setup-graph` reads the layer that decides.** It helps where bare agents record the wrong fact: an embedded or in-process engine, an override that sets the version, a query language that has to follow the pinned server. On ordinary repos a bare model already reads the pin correctly nine times in ten, and the skill showed no gain there.
- **`query-review` hands production back.** Asked to purge, backfill or merge rows on a production target, Haiku left a usable, bounded change for review in 29 of 48 runs without the skill and 47 of 48 with it. Sonnet barely needs it: 47 and 48. The rest of the skill, such as answering a wrong lint flag, showed no measurable gain. Untested: a Cypher change on a live development database. On a stand-in that only logged, agents with the skill declined to send it in 7 of 42 runs; bare agents sent all 42.

It took 24 gates to get these five results. Fifteen missed. Four passed and were set aside: three ran on cases of our own invention, and the fourth did not hold on its documented-problem cases. All of them are in [BENCHMARK.md](https://github.com/usergraphtheory/erdostack/blob/main/BENCHMARK.md#every-gate-including-the-ones-that-missed).

What these numbers do not say:

- **The bare models are already good.** That is the main finding. On documented problems a current model gets most cases right without help, and a skill has room to add something only in a few places. These five are the places we found.
- **The repositories are generated.** The problems are documented; the repos around them were written for the test. No real user's repository, issue or data is in the library.
- **No Cypher was executed.** The cases run SQL on SQLite and Python on NetworkX, and read Cypher without running it. Nothing here was run against a live Neo4j or LadybugDB.
- **Two models, one run each per case.** No other vendor's model was tested, and whether an agent loads a skill at the right moment was only simulated.
- **Not a clean room.** Every run, with a skill or without, was made inside the maintainer's own agent session, on the machine that held the cases. Both arms were given this repository's `AGENTS.md`, the maintainer's notes for the project and a list of unrelated skills as well as the request, and staying inside the working directory was an instruction. A later re-run of 100 runs under a tripwire found no session opening a case, a grader or a skill it had not been given. That measures today's sessions, not the recorded ones, and what an agent started clean would do has not been measured ([Run conditions](https://github.com/usergraphtheory/erdostack/blob/main/evals/RUN_CONDITIONS.md)).
- **We built both the skills and the test.** Authors, reviewers and auditors worked in separate sessions that were not shown the skill or the results, and nobody outside this project has checked the work yet. The harness, the protocols and every saved report are in [`evals/`](https://github.com/usergraphtheory/erdostack/tree/main/evals). The cases, about 1,500 of them, are in [erdostack/bench](https://github.com/erdostack/bench), with what each agent wrote in the 1,480 runs behind the table above and a command that grades those runs again. After the results were in, readers who were shown no grade and no arm read every run that had passed with a skill and found no false pass. They called four of the 44 bare-agent passes they read false, three of them on a point where a grader is kinder than its own written requirement; counting all four as failures would move two of the results slightly toward the skills. That check has limits of its own: the readers are Claude models, most runs had one reader, two in five of the skill-arm results they read name the package, and only 44 of the 559 bare-agent passes were read. Every one of their answers is [published](https://github.com/erdostack/bench/tree/main/audits/pass-audit-2026-11-27). Break it and tell us.

## Honest limits

- **Skills are instructions, not guarantees.** An agent can still ignore one. None of them replaces query timeouts and read-only credentials.
- **Engine facts go stale.** Every engine claim carries a version and a date for that reason. A pack is only as current as its last check.
- **It is a niche.** If your data has no relationships worth traversing, most of this will not help you. Start with `roast-my-graph` on what you already have.

## Ground rules

- No inflated install counts, bought stars or planted praise.
- No success stories that cannot be reproduced from the public eval harness.
- No naming that implies a vendor made or endorses a pack. This is independent work.
- No hidden network calls and no undisclosed telemetry. The default is none.
- The roast punches at schemas, never at people.

## Contributing

Fork it, adapt it, and send back what works. Engine packs, eval cases and reports of agent failures that you can reproduce on a public dataset are all welcome, and contributions are credited. Start with [CONTRIBUTING.md](https://github.com/usergraphtheory/erdostack/blob/main/CONTRIBUTING.md).

## The name

Paul Erdős wrote more than 1,500 papers with over 500 coauthors, many of them on graphs, and carried everything he owned in two suitcases. Small, portable and built for collaboration seemed like the right design goals for a skill stack. Installing it will not lower your Erdős number. It might stop your agent deleting production because somebody asked nicely.

## Official sources

An anonymous project is easy to imitate, so this is the whole list. Anything else using the name is not this project.

- Website: [erdostack.com](https://erdostack.com)
- Source: this repository. The [erdostack](https://github.com/erdostack) organization on GitHub belongs to the project and holds the case library.
- Eval cases: [`erdostack/bench`](https://github.com/erdostack/bench), the case library behind [BENCHMARK.md](https://github.com/usergraphtheory/erdostack/blob/main/BENCHMARK.md).
- npm: [`erdostack`](https://www.npmjs.com/package/erdostack). PyPI: [`erdostack`](https://pypi.org/project/erdostack/).
- Hugging Face: [erdostack](https://huggingface.co/erdostack), which mirrors the case library as the dataset [`erdostack/bench`](https://huggingface.co/datasets/erdostack/bench).
- Announcements: [@graphtheory on X](https://x.com/graphtheory).

The name is one word, lowercase.

## Updates

Release notes are in [CHANGELOG.md](https://github.com/usergraphtheory/erdostack/blob/main/CHANGELOG.md). New failure modes, engine changes and rants are posted at [@graphtheory on X](https://x.com/graphtheory).

## License

[MIT](https://github.com/usergraphtheory/erdostack/blob/main/LICENSE). erdostack is independent and is not affiliated with, sponsored by or endorsed by any database vendor, agent vendor or benchmark body named in this repository, LDBC included. Product names belong to their owners. [`evals/STANDARDS.md`](https://github.com/usergraphtheory/erdostack/blob/main/evals/STANDARDS.md) restates parts of the LDBC Social Network Benchmark specification, which is licensed CC BY 4.0; the [attribution](https://github.com/usergraphtheory/erdostack/blob/main/BENCHMARK.md#attribution) applies to that material.
