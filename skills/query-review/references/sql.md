# Graphs in SQL tables: SQLite and PostgreSQL, for writes

Last verified: 2026-11-23

Status: **executed** on 2026-11-23, on SQLite 3.53.1 through Python's `sqlite3` module and on PostgreSQL 16.15 through `psql`, against small invented tables. Every line tagged **[run]** was observed on those versions; **[unverified]** lines were not run. Other versions can differ: repeat the check on the repo's own engine when it matters.

## SQLite (3.53.1)

- **[run]** `EXPLAIN QUERY PLAN <statement>` returns the plan and runs nothing: in front of a `DELETE` it left every row in place. Through a driver the statement's parameters still have to be bound.
- **[run]** `PRAGMA query_only = ON`, or opening the file with the URI `file:<path>?mode=ro`, makes every write fail. Use one of them when you only read.
- **[run]** `DELETE ... LIMIT` is a syntax error in a default build. A subquery that picks the batch (`WHERE <key> IN (SELECT <key> ... LIMIT <n>)`) works in its place.
- **[run]** A `WITHOUT ROWID` table has no `rowid` ("no such column: rowid"). Read the table's definition first (`SELECT sql FROM sqlite_master WHERE name = '<t>'`) and use its primary key columns.
- **[run]** A loop that re-selects "the next n rows that match" ends for a delete, and for an update that takes rows out of the scope. An update that leaves rows matching (halving a value, say) picks the same rows again on every pass and never ends.
- **[run]** A correlated subquery inside an `UPDATE` that reads the column being updated sees rows the same statement has already rewritten. A value computed from other rows of the same table (a share of a total, say) has to be read before the write starts.
- **[run]** `conn.total_changes` in Python counts the rows changed so far on the connection, so the difference across a commit is the size of that transaction. Use it on the copy to report the largest transaction.
- **[run]** A single-file database can be copied with Python's `sqlite3`: `src.backup(sqlite3.connect('<tmp>/copy.db'))` gives a consistent copy, including what is still in a `-wal` file. Point the job at the copy.

## PostgreSQL (16.15)

- **[run]** `EXPLAIN <statement>` plans and runs nothing; a `DELETE` behind it removed no rows. `EXPLAIN ANALYZE` executes the statement: the `DELETE` really deleted, and only the surrounding `BEGIN` ... `ROLLBACK` brought the rows back. Never use it on a write outside a transaction you roll back, and not on production at all.
- **[run]** `BEGIN READ ONLY` refused a `DELETE`. `SET LOCAL statement_timeout` inside a transaction lasted only for that transaction.
- **[run]** `DELETE ... LIMIT` is a syntax error. A subquery that picks the batch by key or by `ctid` works, re-run until it removes nothing.
