# Kuzu and LadybugDB: what setup-graph needs to know

Last verified: 2026-11-23
Status: verified against documentation, not executed. Neither engine is installed where this was written. Lines
marked "not verified" come from prior knowledge and were not checked against a page on that date. Sources are
in `sources.md`. Independent notes, not written or endorsed by either project.

## What they are

Both are embedded graph databases: a library the application imports, with the database in a local file or
directory and no server. They are queried in Cypher, in their own dialect, which is not Neo4j's.

- **Kuzu** was archived upstream in October 2025. Its last release is 0.11.3. It receives no fixes.
  (Checked 2026-11-23.)
- **LadybugDB** is the maintained fork that continues it. (Checked 2026-11-23; PyPI `ladybug` was at 0.22.3,
  released 2026-11-06.)

## Package names

| Ecosystem | Current name | Earlier name still found in lockfiles |
|---|---|---|
| Python (PyPI) | `ladybug` | `real_ladybug` (also spelled `real-ladybug`) |
| Node (npm) | `@ladybugdb/core` | `lbug` |
| Rust (crates.io) | `lbug` | none known |
| Command line | `lbug` binary from the project's releases | none known |
| Kuzu, any ecosystem | `kuzu` | archived, see above |

(Names checked 2026-11-23. Which versions were published under the earlier names: not verified.)

Note the trap in the table: `lbug` is the current Rust crate and an abandoned npm name.

## What to record

- `engine`: what the repo installs. A repo that locks `kuzu` is on `kuzu`; do not write the successor. A repo
  that locks any LadybugDB package, under either name, is on `ladybugdb`.
- `engine_version`: the locked package version. The package contains the engine, so the lockfile settles it;
  `unknown` would be wrong when a lockfile is present. A range in the manifest is not the version.
- `driver`: the package name exactly as the lockfile spells it, and the same locked version.
- `query_language`: `Cypher`.
- Open questions and your reply, in words the user cannot miss:
  - on `kuzu`: the package is archived upstream since October 2025, 0.11.3 is the last release, and
    LadybugDB (`ladybug` on PyPI, `@ladybugdb/core` on npm, `lbug` on crates.io) is where it continues;
  - on an earlier LadybugDB name: the package is now published as the current name from the table. Write that
    name out; saying only "it was renamed" leaves the user to look it up;
  - a locked version many releases behind the current one is worth one line as well.
- Change nothing: do not edit the dependency, the import or the lockfile. Moving is the user's decision.

If the repo itself notes the archival or the rename anywhere, cite that file. If it does not, give the
warning anyway and say that it comes from this note and its date.

## Confirming against the database

Only when the user asks, and through the repo's own read-only query command, because opening an embedded
database with a write connection can lock or upgrade the file. `CALL db_version() RETURN *;` returns the
engine version on LadybugDB. (Checked 2026-11-23, documentation only. The same call on Kuzu: not verified.)

## Elsewhere

The LadybugDB documentation and repository are listed in `sources.md`; prefer them for anything beyond these
notes.
