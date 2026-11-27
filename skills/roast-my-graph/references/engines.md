# Engine notes for a roast

Last verified: 2026-11-23

How to look at the schema and the plan on each engine, and the engine behaviour a finding is allowed to lean on. Use it to check before filing; where the repo or a reachable database can answer, prefer that to this file.

Every line carries a status:

- **[docs]** verified against the official documentation on 2026-11-23, not executed (no graph database was installed on the machine where this was written).
- **[run]** executed on 2026-11-23 with the versions named.
- **[unverified]** long-stable behaviour written from experience; the official page was located by title only and not read on 2026-11-23, and nothing was executed. Confirm against the docs for the user's version before a `high` or `critical` finding rests on it alone, and say so under "Not checked" if you could not.

Inspection is read-only. If `docs/graph/CONTEXT.md` says `access: read-only`, or says nothing, do not run anything that writes, and remember that profiling a query executes it.

## Neo4j

Versions and language:

- **[docs]** Server releases were semantic versions through 5.x (5.26 is the last 5.x and a long-term-support release) and are calendar versions (`YYYY.MM.PATCH`) from 2025.01.
- **[docs]** From 2025.06 the query language is versioned apart from the server: Cypher 5 is frozen apart from bug fixes, and new features land in Cypher 25. A query can start with `CYPHER 5` or `CYPHER 25`, and each database has a default language. Which default a database has depends on when and how it was created, so read it from the repo or the database before writing a fix that uses newer syntax, and state the language the fix assumes.

Looking instead of recalling:

- **[unverified]** `SHOW INDEXES` and `SHOW CONSTRAINTS` list what exists (Neo4j 5.x and calendar versions).
- **[unverified]** Prefix a query with `EXPLAIN` for the plan without running it, or `PROFILE` to run it and see rows and database hits per operator. A label scan followed by a filter is the unindexed lookup; an operator that multiplies two unrelated row sets is the disconnected pattern.

Behaviour a finding may lean on (all **[unverified]**, unchanged across Neo4j 5.x as far as we know):

- A relationship joins exactly two nodes, has one type and a direction, and can carry properties. It cannot be the start or end of another relationship. Several relationships of one type may join the same two nodes.
- A directed pattern matches only relationships stored in that direction.
- A variable-length pattern with no upper bound keeps expanding as far as the data allows.
- Patterns in one query that share no variable produce every combination of their rows.
- `MERGE` matches its entire pattern, property map included, or creates all of it.
- Finding a node by a property that has neither an index nor a constraint examines every node with that label. A uniqueness constraint brings its own index, so a second index on the same property adds nothing.

## LadybugDB

Formerly Kuzu. Do not answer from Kuzu-era memory: package names and details have moved.

- **[docs]** Kuzu was archived in October 2025 (last Kuzu release 0.11.3). LadybugDB is the maintained fork. Python package `ladybug` (0.22.3 released 2026-11-06; early releases were named `real_ladybug`), Node package `@ladybugdb/core` (early: `lbug`), Rust crate `lbug`, CLI binary `lbug`.
- **[docs]** Introspection goes through `CALL`: `CALL show_tables() RETURN *;` lists tables, `CALL table_info('<Table>') RETURN *;` lists a table's columns, `CALL db_version() RETURN *;` gives the version.
- **[docs]** Prefix a query with `EXPLAIN` for the plan only, or `PROFILE` to run it and get per-operator timings.
- **[docs, read by the erdostack eval authors on 2026-11-23, not re-read for this file]** A node table must declare a primary key and the engine indexes it; a relationship table is declared with its `FROM ... TO ...` endpoints and cannot have a primary key; relationship multiplicity defaults to many-to-many. So "no indexes defined" on a schema whose lookups are all by primary key, and "the relationship table has no key", are not findings here.
- **[unverified]** Whether a Neo4j statement (`CREATE CONSTRAINT`, `CREATE INDEX`, a procedure call) exists in LadybugDB. Do not propose one as a fix without finding it in the LadybugDB docs for the user's version.

## SQLite

All **[run]** on SQLite 3.53.1 through Python 3.13 `sqlite3`.

- Open a sample read-only: `sqlite3.connect("file:<path>?mode=ro", uri=True)`; a write is refused.
- `EXPLAIN QUERY PLAN <statement>` prints one row per step. `SCAN <table>` reads every row; `SEARCH <table> USING ... INDEX ... (<column>=?)` uses an index.
- `PRAGMA index_list(<table>)`, `PRAGMA index_info(<index>)` and `PRAGMA foreign_key_list(<table>)` show what exists; `SELECT type, name, sql FROM sqlite_schema` shows all of it.
- Declaring a foreign key creates no index on the referencing column.
- A composite primary key serves lookups on its leading column only: with `PRIMARY KEY (src, dst)`, `WHERE src = ?` is a search and `WHERE dst = ?` is a scan until an index leading with `dst` exists.
- `PRAGMA foreign_keys` is off on a new connection. A guarantee that rests on a foreign key holds only if every writer switches it on; look for where the application does that.
- A recursive query with `UNION ALL` over data that contains a loop does not finish. Replacing it with `UNION` finishes only when the recursive rows carry the id alone: with a counter or path column every row is new and it still does not finish.

## PostgreSQL

Nothing was executed (no server on the authoring machine). All **[unverified]**, long-stable in current major versions:

- `EXPLAIN <statement>` shows the plan without running it; `EXPLAIN ANALYZE` runs the statement. `\d <table>` in `psql` lists a table's indexes and constraints.
- A foreign key does not create an index on the referencing column; a primary key or unique constraint does create one on its own columns, and a multi-column index serves its leading columns.
- Recursive queries accept a `CYCLE` clause from version 14. Confirm the server version before proposing it.

## NetworkX

All **[run]** on NetworkX 3.7, Python 3.13.

- Edge direction is whatever `add_edge(u, v)` was given. On a `DiGraph`, `nx.descendants(G, n)` follows edges forwards from `n` and `nx.ancestors(G, n)` backwards. Read the loader to learn what "forwards" means in this repo.
- `nx.shortest_path(G, s, t)` counts hops. It uses an edge attribute only when called with `weight="<attribute>"`.
- `G.is_directed()`, `G.is_multigraph()` and `nx.is_directed_acyclic_graph(G)` answer what kind of graph the loader really built.
