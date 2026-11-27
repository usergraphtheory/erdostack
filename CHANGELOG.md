# Changelog

Notable changes to erdostack. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-11-27

### Added

- Five skills: `roast-my-graph`, `graph-or-not`, `setup-graph`, `schema-first` and `query-review`. Each has an eval spec with thresholds set before the runs, and each passed a gate on cases written from documented problems before it was included.
- `BENCHMARK.md`: the results for all five skills on one page, by model and with cost; a second track of thirty cases staged on the schema and tasks of two LDBC benchmarks (LDBC-derived work, not LDBC Benchmark Results); the method, the limits, and every gate that missed.
- Eval harness (`evals/harness/erdo_eval.py`, standard library only): with-skill and no-skill arms, script graders with self-tests, blind judge batches with calibration, two-session cases, a headless runner, Wilson intervals, a paired sign test, a `summary` command that recomputes any published table from saved reports, an `index` command that lists every case as one JSON line, and `export` and `regrade`, which publish what an agent changed in a run and grade it again.
- The case library is published separately as `erdostack/bench`, with a dataset mirror on Hugging Face: 1,527 cases with their graders, including the 30-case LDBC-derived core set, an index of every case (`cases.jsonl`), what the agents wrote in the 1,480 runs the results rest on (`recorded-runs/`), the harness and the skills at the versions measured. This repository keeps the claims, protocols and saved reports.
- `evals/REAL_PROBLEMS.md`: a register of 34 graph problems with sources. `evals/PROVENANCE.md`: how much of each skill's evidence rests on them. `evals/STANDARDS.md`: the published benchmarks the core set borrows from, with what was and was not taken.
- Every gate result under `evals/results/`, including the gates that missed.
- `evals/PASS_AUDIT.md`: an audit of the passing grades behind every published result, protocol first. Readers who were shown no grade, arm or model read all 710 runs that passed with a skill and found no false pass; of 44 unaided passes read, two readers called four false and one is unresolved. Three of the four are `setup-graph` records that the grader accepts, where its own requirement sentences ask for the library and for the locked version. Counted as failures, the four would move two results toward the skills and none away. Every answer is published in `erdostack/bench` under `audits/`.
- `evals/RUN_CONDITIONS.md`: what the recorded runs could see. Every run was made inside the maintainer's own agent session: isolation was an instruction, and both arms were given this repository's `AGENTS.md`, the maintainer's notes for the project and a list of unrelated skills besides the request. A re-run of 100 runs under a tripwire on about 850,000 files and folders, protocol first: none of 28 sessions opened a case, a grader, a result or a skill it had not been given; five listed a folder they had not been handed, and two more listings could not be tied to a session. It measures today's sessions, not the recorded ones. A clean run has not been made.
- Repository skeleton: `skills/`, `references/engines/`, `evals/` and authoring templates.
- Host manifests over the same markdown: Agent Plugins (`plugin.json`), Claude Code, Cursor, Codex and Gemini CLI.
- `erdostack` installers for npm and PyPI that copy bundled skills into an agent's skills directory.
- Validator for manifests, versions, skill frontmatter and engine packs.
- CI on Linux, macOS and Windows, and a tag-driven release workflow for npm, PyPI and GitHub Releases.
- An "Official sources" list in the README.
- Profile pictures in `assets/`, and `assets/README.md` describing the mark, palette and typeface.

### Changed

- The logo, share image and brand color now match [erdostack.com](https://erdostack.com): chalk on a chalkboard, with the source vertex in yellow.
- Package and plugin homepages point to erdostack.com.

### Fixed

- The release workflow no longer fails at startup.

### Measured

- `roast-my-graph`: 29 cases won, 8 lost, 83 tied of 120 (p = 0.0008). The gain is restraint on sound designs, not detection.
- `schema-first`: 14 won, 0 lost, 6 tied of 20 two-session cases (p = 0.0001). The gain is in a later session; within one session none was shown.
- `graph-or-not`: 30 won, 1 lost, 9 tied of 40 two-session cases (p under 0.000001), after three gates that missed. A decision survives into the next session; the skill does not decide better.
- `setup-graph`: 16 won, 2 lost, 62 tied of 80 (p = 0.0013). The claim is for three kinds of repo where bare agents record the wrong fact, which are 64 of the 80 cases and hold every win. On ordinary repos two gates showed no gain.
- `query-review`: 18 won, 0 lost, 62 tied of 80 (p = 0.000008), for bulk changes aimed at production, nearly all of it on the smaller model. The rest of the skill showed no measurable gain.
- All five on the core set: 11 won, 0 lost, 19 tied of 30 (p = 0.001). These cases adapt the schema and tasks of the LDBC Social Network Benchmark and LDBC Graphalytics. They are not an LDBC Benchmark, and these are not LDBC Benchmark Results.

### Dropped on the way

- The first design of `query-review` (read-query checks, writes and reviews in one skill) was gated three times on 140 fresh cases without showing a gain over the bare model. It was narrowed twice more before its ninth gate passed; `evals/query-review/EVALS.md` has all nine.
- Earlier gate results for all five skills, on generated cases not tied to documented problems. They are kept in `evals/results/` and are no longer what any claim rests on.

### Not yet

- Nothing has been run against a live Neo4j or LadybugDB. Cypher in the eval cases is read, not executed.
- No model outside Claude Haiku 5.5 and Claude Sonnet 5.5 has been measured.
