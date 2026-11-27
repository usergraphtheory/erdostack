# Neo4j: what setup-graph needs to know

Last verified: 2026-11-23
Status: verified against documentation, not executed. No Neo4j is installed where this was written. Lines marked
"not verified" come from prior knowledge and were not checked against a page on that date. Sources are in
`sources.md`. Independent notes, not written or endorsed by Neo4j.

## Server versions

- Up to the 5 series the server uses semantic versions. 5.26 (December 2024) is the last 5.x release and a
  long-term-support line. From 2025.01 on, versions are calendar versions, `YYYY.MM.PATCH`. So the release lines
  in order are 4.x, 5.x, 2025.x, 2026.x, and `2025.10.1` is newer than `5.26.14`. (Checked 2026-11-23.)
- Record the version part of an image tag and leave edition suffixes to Evidence. (Tag suffix naming: not
  verified.)
- A driver package has its own version numbers. Never copy a driver version into `engine_version` or the other
  way round. (Driver lines 4.4, 5.x and 6.x exist alongside calendar-versioned servers: not verified.)

## Which Cypher goes in `query_language`

Since Neo4j 2025.06 the query language is versioned apart from the server. Cypher 5 is frozen and only gets
fixes; Cypher 25 gets every new feature. Each database has a default language, and a single query can choose
with a `CYPHER 5` or `CYPHER 25` prefix. (Checked 2026-11-23, applies to 2025.06 and later.)

| Server the repo pins | Record |
|---|---|
| 4.x or older | `Cypher` (the 5 and 25 names do not apply) |
| 5.x | `Cypher 5`: the server speaks only that |
| 2025.01 to 2025.05 | `Cypher 5` (inferred from the split starting at 2025.06; not verified) |
| 2025.06 or later | whatever the repo shows as the default language; see below |
| `unknown` | `Cypher`, with the question listed as open |

For 2025.06 or later, look in the files the start path really uses, for any of these:

1. `db.query.default_language` in a `neo4j.conf` the server mounts or is installed with (`CYPHER_5` or
   `CYPHER_25`).
2. The same setting handed to the container as an environment variable, in a compose file, a Helm values file
   or a manifest. Match on a `NEO4J_`-prefixed name containing `default` and `language`. (Exact spelling of the
   variable: not verified.)
3. A `CREATE DATABASE ... DEFAULT LANGUAGE ...` or `ALTER DATABASE ... SET DEFAULT LANGUAGE ...` statement in a
   setup or migration script the repo runs, for the database the queries use.
4. A `CYPHER 5` or `CYPHER 25` prefix on the repo's queries. A prefix decides one query only; if every query
   file and the runner carry the same one, that is the language the repo's queries run in. Record it and say
   under Evidence that it comes from the prefix, not from the database default.

Then:

- One of them settles it: record `Cypher 5` or `Cypher 25` and cite the file.
- Two of them disagree: a statement on the database is more specific than a server-wide setting (order of
  precedence: not verified), so record that one and list the disagreement under Open questions.
- Nothing shows it: record `Cypher` and add an open question along the lines of "Neo4j <version> runs Cypher 5
  or Cypher 25 depending on the database's default language, and nothing in the repo shows which. Check the
  database, or prefix queries with CYPHER 5 or CYPHER 25." Do not put one version forward.

Why the server version does not answer it: the default was set by how and when the database was created.
Databases created on or migrated to 2025.06 and later kept Cypher 5 as their default. Databases created on
2026.02 and later are given Cypher 25 explicitly, and new self-managed installs from 2026.06 ship with
`db.query.default_language=CYPHER_25`. A database upgraded in place or restored from a dump carries its
history with it, so a 2025.10 server can be on Cypher 25 and a 2026.08 server on Cypher 5. (Checked
2026-11-23.)

## A driver far behind the server

Flag it when the locked driver's major line is two or more server lines behind what the repo runs (a 4.x
driver against a calendar-versioned server), or when the repo's own notes say the pairing is unsupported.
Record both facts as they are, then add an open question that says so in words: "driver <package> <version>
is from the 4.x line and the server is <version>; check the pairing against Neo4j's driver compatibility
table, or upgrade the driver". Listing the two numbers without saying they need checking does not warn
anyone. Do not claim what breaks: this note does not carry the compatibility table. (Which pairs are
supported: not verified; the table's address is in `sources.md`.)

## Confirming against a running database

Only when the user says one is running and the repo's own query command reaches it read-only.
`CALL dbms.components()` returns the server's name, version and edition. (Not verified.) A mismatch with the
pinned version is an open question, not a reason to change the recorded pin without saying so.

## Elsewhere

Neo4j publishes its own manuals and agent material; prefer them for anything beyond these notes. The pages
used here are listed in `sources.md`.
