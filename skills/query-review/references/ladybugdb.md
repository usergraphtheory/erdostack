# LadybugDB (and Kuzu): what query-review needs

Last verified: 2026-11-23

Status: verified against documentation, not executed. No LadybugDB or Kuzu was installed where this was written and the package could not be downloaded, so nothing below was run. Each line carries a tag:

- **[docs]** checked against the official page on 2026-11-23.
- **[unverified]** written from prior knowledge of Kuzu up to 0.11.3. Not checked against LadybugDB 0.22 or its documentation. Treat it as a lead.

LadybugDB runs in process, so the installed library is the engine and you can check instead of recalling: `CALL db_version() RETURN *;` for the version, and `EXPLAIN` in front of a statement to see whether this version accepts it. Tell the user about any **[unverified]** line you relied on and could not check.

Independent notes, not written or endorsed by the LadybugDB project.

## Version and names

- **[docs]** LadybugDB is the maintained fork of Kuzu. Kuzu was archived in October 2025 and its last release is 0.11.3. PyPI `ladybug` 0.22.3 was released on 2026-11-06 (early releases: `real_ladybug`); Node `@ladybugdb/core` (early: `lbug`); Rust crate and command-line binary `lbug`.
- It speaks Cypher but is not Neo4j. Do not carry Neo4j clauses or procedures over without checking them here.

## Plans and introspection

- **[docs]** `EXPLAIN <query>` prints the plan and runs nothing. `PROFILE <query>` runs the query and reports the time spent per operator, so it is for reads you have bounded.
- **[docs]** `CALL show_tables() RETURN *;` lists node and relationship tables. `CALL table_info('<Table>') RETURN *;` describes one table's properties (in Kuzu 0.11 the output also marked the primary key: **[unverified]**). `CALL show_connection('<RelTable>') RETURN *;` gives a relationship table's endpoints (confirm the name on the CALL page).

## Writes and transactions

- **[unverified]** Each statement commits on its own unless you open a transaction (`BEGIN TRANSACTION`, then `COMMIT` or `ROLLBACK`). A destructive statement can be tried inside a transaction that you roll back, on a copy of the database directory, never on the live one.
- **[unverified]** There is no `CALL { } IN TRANSACTIONS` and no APOC. Batch from the client: a statement scoped by a primary-key range, or the scope with a `LIMIT` before the delete, re-run until it removes nothing.
- **[unverified]** One process writes at a time. A database can be opened read-only (a `read_only` flag when the database object is created), which is the right mode for plans and probes.
- **[unverified]** A per-connection query timeout exists (a `timeout` setting in milliseconds). Set it before a probe on a large database if the repo's runner does not.
