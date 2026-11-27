# Neo4j: what query-review needs

Last verified: 2026-11-23

Status: verified against documentation, not executed. No Neo4j was installed where this was written, so nothing below was run. Each line carries a tag:

- **[docs]** checked against the official page on 2026-11-23.
- **[unverified]** written from prior knowledge. The official page was located by title on 2026-11-23 but could not be opened, so the wording and the version numbers were not confirmed that day.

Before you rely on an **[unverified]** line, check it against the running server or the page listed in `sources.md`, and tell the user if you could not. The cheapest check for syntax: put `EXPLAIN` in front of the statement on a non-production database. The server compiles it, so a form its version does not accept is rejected there and nothing is executed. **[unverified]**

Independent notes, not written or endorsed by Neo4j.

## Version and language

- **[docs]** Server versions are semantic through 5.x (5.26 is the last 5.x and a long-term-support line) and calendar versions (`YYYY.MM.PATCH`) from 2025.01.
- **[docs]** From 2025.06 the query language has its own version: Cypher 5 is frozen apart from fixes and Cypher 25 gets the new features. Each database has a default language and one query can choose with a `CYPHER 5` or `CYPHER 25` prefix. The default depends on when and how the database was created, not on the server version: take it from `query_language` in `docs/graph/CONTEXT.md` or from the repo's config, and say which language a statement you hand back assumes.

## Checking a write without running it

- **[unverified]** (4.x to 2026.x) `EXPLAIN` returns the plan and runs nothing, so it is safe in front of a write, on production too. `PROFILE` runs the statement to the end, writes included: never on production, and only on a copy for a write.
- **[unverified]** (4.3 and later) `SHOW INDEXES` and `SHOW CONSTRAINTS` list what exists, including the uniqueness constraint that tells you a loader's identity key. Prefer them, or the repo's schema files, to memory.

## Batching a large write

- **[unverified]** The state of a transaction is held in memory until it commits. A delete or update of very many nodes in one transaction fails on memory instead of merely being slow.
- **[unverified]** (4.4 and later) `CALL { ... } IN TRANSACTIONS OF <n> ROWS` commits after each batch; without `OF` the batch is 1000 rows.
- **[docs]** (5.x) `CALL { ... } IN TRANSACTIONS` is accepted only in an implicit (auto-commit) transaction and fails inside an explicit one (GQL status 25N17). In a driver that means a plain `session.run`, not a managed transaction function. Check how the repo's runner opens its transaction.
- **[docs]** Passing the outer variable in: the scope clause `CALL (n) { ... }` exists from 5.23, and from 5.23 the importing `CALL { WITH n ... }` form is deprecated. Before 5.23 only the `WITH` form exists. Whether a Cypher 25 database still accepts it: check with `EXPLAIN` before relying on it.
- **[unverified]** `ON ERROR CONTINUE | BREAK | FAIL` and `REPORT STATUS AS <var>`: from 5.7. `IN <n> CONCURRENT TRANSACTIONS`: from 5.21; avoid it for deletes whose batches share relationships, because they contend for the same locks. `ON ERROR RETRY`: from 2025.03.
- **[unverified]** `USING PERIODIC COMMIT` was removed in 5.0.
- **[unverified]** `apoc.periodic.iterate` exists only where the APOC plugin is installed. Look for it in the image, the plugin settings or `SHOW PROCEDURES` before you write it.
- **[unverified]** A form that needs no special clause: match the scope, `WITH n LIMIT <n>`, delete, `RETURN count(*)`, and re-run until it returns 0.
- `DETACH DELETE` removes each node's relationships in the same batch, so one hub can make a batch far larger than its row count. Check the degree skew first, and if there is a hub, delete its relationships in batches before the node.
- Batches that committed stay committed when a later one fails. Re-running a scoped statement acts again on every row still in scope: harmless for a delete, wrong for an update that leaves its rows matching, which then change once per pass.
