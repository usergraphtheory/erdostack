---
name: setup-graph
description: "Use when the user asks to set up, record, refresh or check the graph context of a repo: which graph engine and version it really runs, the driver, how queries are run, whether writes are allowed, or asks for docs/graph/CONTEXT.md. Run once per repo and again after an engine or driver upgrade. Reads the repo, resolves what is actually pinned, and writes docs/graph/CONTEXT.md in the fixed format the other erdostack skills parse. Not for writing or tuning queries, snapshotting a schema, choosing, installing, upgrading or migrating a database, or GraphQL APIs."
---

# setup-graph

User-invoked, once per repo and again after an upgrade. It fixes two agent failures: recording the graph setup in a shape nothing downstream can parse, and recording a version from prose, a default or memory instead of what the repo pins. It writes `docs/graph/CONTEXT.md`, which the other erdostack skills read before they write or review a query.

## When to use

The user wants the repo's graph setup written down, refreshed or checked. Not for writing queries, taking a schema snapshot (`schema-first`), deciding whether to use a graph (`graph-or-not`), or installing or upgrading anything.

## Ground rules

- **Read, do not recall.** Every fact comes from a file you opened in this repo or from the user's request. What neither settles is the literal `unknown`; a plausible guess is worse, because the next skill will trust it.
- **Change nothing outside `docs/graph/`.** No installs, no lockfile refresh, no starting containers, no seed, load or migration commands, no fixing a stale README. Report what is stale; the user asked for a record, not a clean-up.
- **Never copy a secret value.** Name the variable and the file it lives in. Passwords, tokens and connection strings that embed them stay where they are.
- **Read-only by default.** `access` is `read-write` only when the user in this request, or the repo's instructions to agents, clearly allow writes. A seed script, a write-capable credential or a "dev only" note is not permission.

## Steps

1. **Start from what exists.** If `docs/graph/CONTEXT.md` is there, treat each line as a claim and re-check it with the steps below. Edit only the lines the repo contradicts, add a section that is missing, leave everything else as written, and tell the user which facts you confirmed and which you changed.

2. **Find the store, or find that there is none.** Go by what runs or is imported, not by what is described: container images, embedded database packages, graph libraries, node and edge tables walked with recursive queries.
   - The engine is the thing that executes the queries: the image or process, not the name on the client package (a wire-compatible engine is often reached through another vendor's driver), and not a successor the repo has not moved to.
   - A graph kept in SQL tables: the engine is that SQL database and the language is SQL. A graph loaded by an in-process library: the library is the engine. Read `references/sql-and-in-process.md`.
   - No graph store at all (the word "graph" only in an API layer such as GraphQL, in a charting library, in prose): say so in the first sentence of your reply. Write the file with `engine`, `engine_version`, `query_language`, `driver` and `run_queries` all `unknown`, and describe the database that is there under Evidence. Putting the application database in Facts would tell the next skill it is a graph engine.
   - Several stores, or a monorepo: answer for the service the user named, with all seven facts taken from that one service's files. If they named none and you can ask, ask. If you cannot, record the store the main query path uses and list every other store under Open questions with its engine, version and query command.

3. **Resolve each version from what pins it.** Sources, strongest first:
   1. A lockfile entry, or an image reference after every override on the path the repo's own start command takes.
   2. The default those overrides replace (base compose file, chart default values, a `${VAR:-fallback}`, an `ARG` default), only when nothing replaces it.
   3. A manifest range (`^2.1.0`, `>=1.4`): it names the package, never the version.
   4. Prose (README, docs, comments, changelogs): a lead to check, never a value. If prose is all there is, record `unknown` and quote the claim under Open questions.

   Applying it:
   - **Server engines.** Find the command people really use to start the database (make target, package script, CI job) and follow it: which files it passes (`-f`, `--env-file`, `--values`, `--build-arg`), which variables it sets. Resolve the image tag through each layer in the order the tool applies them; the last one wins. Layers hide in compose override files, env files, build args, Helm values files, kustomize overlays, and the image string of a test-container fixture when that is the only database the repo runs. If you are not sure which of two layers wins, read `references/override-layers.md`.
   - **Embedded engines and in-process libraries.** The package contains the engine, so the locked package version is the engine version: take it from the lockfile, not the manifest. The same package and version go in `driver`.
   - **Drivers.** The package name as the lockfile spells it, and the locked version. With two lockfiles, the live one is the one the manifest's package-manager field, the Dockerfile or CI installs from; the other is a leftover to report.
   - **Versions managed by another artifact** (an imported BOM, a Gradle `platform`, a parent): ask who publishes it, not whether its file is in the repo. One the package's own project releases alongside it (same group or namespace, named after the package, such as `<package>-bom`) moves in lockstep with it, so the number the repo gives that artifact is the package's version: record it and say under Evidence that it came through the BOM. A platform or framework BOM manages other projects at numbers of its own: when no repo file states the managed number, record `unknown` and name the BOM and its version under Open questions, never the BOM's own number.
   - A driver's version, a chart version, a toolchain version and a runtime version are not the engine's version.
   - Nothing pins it (a hosted instance, an untagged or `latest` image): `unknown`.

4. **Engine-specific checks.** These rest on facts that change faster than training data, so read the file; do not answer from memory.
   - The engine is Neo4j: `references/neo4j.md`, before you fill `query_language`. From Neo4j 2025.06 on (checked 2026-11-23) the Cypher version is a property of the database, not of the server version, and it has to be recorded or raised.
   - The repo installs Kuzu or LadybugDB (a package named `kuzu`, `ladybug`, `real_ladybug`, `lbug` or `@ladybugdb/core`): `references/ladybugdb-kuzu.md`.

5. **Find how queries are really run.** Trace the entry point hop by hop (make target, then script, then module or class) and confirm each hop exists. Record one command, typed from the repo root, with `<placeholders>` for arguments. If prose names a script that is gone, record the one that exists and report the stale mention. No runner in the repo: `unknown`.

6. **Schema snapshot.** `docs/graph/schema.md` if it exists; otherwise a schema dump, or the DDL the repo itself applies to build the store; otherwise `none`. List the path before you write it, because a path taken from prose may not exist. Hand-written model notes are not a snapshot; mention them under Evidence.

7. **Collect what the user must be told.** Each item goes under Open questions and in your reply:
   - Two sources disagree: record the stronger one and name the losing value and its file. Do not pick silently; the user may not know that the README or the default is stale.
   - The repo's docs promise a behaviour of the store that its code or configuration does not deliver: an integrity rule the engine leaves off unless each connection turns it on, a check whose query cannot match. Docs state intent; where connections are opened and what the queries say decide what happens. Name the claim, its file, and what the code does instead. No fact key holds this, which is why it is easy to drop.
   - The engine or driver is archived, unmaintained or renamed upstream (the engine reference lists the known cases; the repo's own notes may say so too): record what is installed, and name the successor or the current package name.
   - The driver is from a much older release line than the server: record both as they are and say that the pairing needs checking or upgrading. Two numbers side by side do not warn anyone.
   - Anything else that would make the next query wrong: a leftover lockfile, a schema file nothing applies, a runner that cannot pass parameters.

8. **Write `docs/graph/CONTEXT.md`** in the format below, then check it. `scripts/check_context.py` sits beside this file and only reads; from the repo root run `python3 <this skill's folder>/scripts/check_context.py docs/graph/CONTEXT.md` and fix what it reports. If you cannot run Python, check the Output rules by eye.

9. **Reply.** Lead with anything from step 7. Then give the seven facts, and what stayed `unknown` and why. Say that you read the repo and did not connect to a database, unless you did.

Connecting is optional and rare: only if the user says a database is already running and the repo's own query command reaches it read-only may you confirm the version with the call in the engine reference, and record a mismatch as an open question. Never start a database to check.

## Output

`docs/graph/CONTEXT.md`, in exactly this shape. The values are an invented illustration:

```markdown
# Graph context

## Facts

engine: neo4j
engine_version: 5.26.3
query_language: Cypher 5
driver: neo4j-driver 5.27.0
run_queries: scripts/run-query.sh <query-file>
access: read-only
schema_snapshot: none

## Evidence

- engine, engine_version: compose.yaml (image tag); nothing on the `make up` path replaces it
- query_language: the server is 5.x, which speaks one Cypher
- driver: package-lock.json (package.json only gives a range)
- run_queries: scripts/run-query.sh, which runs tools/query.ts
- access: nothing in the repo or the request allows writes
- schema_snapshot: no dump in the repo; docs/model.md is hand-written

## Open questions

- engine_version: docs/setup.md says 5.18, compose.yaml pins 5.26.3. Recorded 5.26.3.
```

Rules for `## Facts`, which the other skills read line by line:

- Exactly these seven keys, once each, in this order, as plain `key: value` lines. No bullets, backticks, bold or other lines in the section.
- One value per line and nothing after it: no parentheses, no "see below", no second clause. The explanation belongs under Evidence, the doubt under Open questions.
- `engine`: the engine's name alone. `engine_version`: the full version as pinned, without edition or image suffix.
- `query_language`: the language, with its version when the setup fixes one (`Cypher 25`, `SQL`); `none` for an in-process library that is called from code.
- `driver`: `<package> <version>`.
- `access`: `read-only` or `read-write`, nothing else. The scope of a permission (which instance) goes under Evidence.
- `schema_snapshot`: a path that exists, or `none`.
- Anything not settled is the literal `unknown`.

`## Evidence`: one bullet per key naming the repo file the value came from and what in it says so. `## Open questions`: everything from step 7, each with both sides and their files; `- None.` when there is nothing.

## References

- `references/neo4j.md`: server versioning, Cypher 5 and Cypher 25, where a repo shows the default language, a driver far behind the server.
- `references/ladybugdb-kuzu.md`: Kuzu's archival, LadybugDB package names old and new, the version call.
- `references/sql-and-in-process.md`: graphs in SQL tables and in graph libraries.
- `references/override-layers.md`: which compose, Docker, Helm or lockfile layer wins.
- `references/sources.md`: where the dated facts come from.
