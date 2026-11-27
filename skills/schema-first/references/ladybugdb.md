# LadybugDB: reading the schema

Last verified: 2026-11-23

LadybugDB is the maintained fork of Kuzu (Kuzu was archived in October 2025; its last release was 0.11.3). The Python package is `ladybug` on PyPI (0.22.3, released 2026-11-06; early releases were published as `real_ladybug`), the Node package is `@ladybugdb/core`, the Rust crate and the CLI binary are `lbug`. An agent that reaches for `import kuzu` or `pip install kuzu` is using the archived project: check which package the repository actually imports before running anything.

Status: **verified against documentation, not executed** (LadybugDB is not installed where this was written). Items marked *(unconfirmed)* could not be read on the documentation page on 2026-11-23 and come from how Kuzu 0.11 behaved.

## From a live database (it is embedded, so "live" means the database directory or file exists)

| Question | Statement | Version | Status |
|---|---|---|---|
| Engine version | `CALL db_version() RETURN *;` | 0.22.3 | documentation, 2026-11-23 |
| Every node and relationship table | `CALL show_tables() RETURN *;` | 0.22.3 | documentation, 2026-11-23 |
| Columns and types of one table | `CALL table_info('TableName') RETURN *;` | 0.22.3 | documentation, 2026-11-23 |
| Which node tables a relationship table joins | `CALL show_connection('RelTable') RETURN *;` | 0.22.3 | *(unconfirmed: check the CALL page)* |

Run `table_info` for every table that `show_tables` lists, node tables and relationship tables alike, and write the snapshot by hand in the layout of `snapshot-format.md`. If `show_connection` is not available, the FROM and TO tables are in the DDL that created the relationship table.

## From files

The schema is declared, not inferred: every node table and relationship table is created by a DDL statement that names its columns and types, and a relationship table names the node tables it runs FROM and TO. *(unconfirmed for 0.22.3: the statement shapes are those of Kuzu 0.11.)* So the DDL file in the repository is a strong source, and `scripts/schema.py cypher-files <ddl files>` reads `CREATE NODE TABLE`, `CREATE REL TABLE`, `ALTER TABLE` and `DROP TABLE` in order. A README diagram that disagrees with the DDL is the stale one.

## Traps

- Direction is part of the table definition. Read FROM and TO and point the arrow that way; do not go by the table's name or by how the request is worded.
- Two node tables with similar names can both exist while a relationship table joins only one of them. Check the endpoint pair of the relationship table you use, not just that both names exist.
- Whether table and column names are matched case-sensitively is *(unconfirmed)*. Write them exactly as declared and the question does not arise.
- Column types are fixed by the DDL (`INT64`, `STRING`, `DATE`, `TIMESTAMP` and so on). Check the declared type before writing a filter, and compare like with like; how a mismatched literal is treated is *(unconfirmed)*.

## Vendor material

The LadybugDB documentation (docs.ladybugdb.com) is the authority for syntax. This file is an independent note and is not endorsed by the LadybugDB project.
