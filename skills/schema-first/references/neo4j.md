# Neo4j: reading the schema from a live database

Last verified: 2026-11-23

Status of every statement below: **from documentation and long-standing behaviour, not executed** (no Neo4j is installed where this was written). On 2026-11-23 the documentation pages listed in `sources.md` could be located but not opened, so the items marked *(not re-read)* rest on how these features have behaved since Neo4j 4.x and 5.x. Run each once against your server and correct this file if it differs.

Run them through whatever `run_queries` in `docs/graph/CONTEXT.md` names (cypher-shell, a driver script, the browser). All are reads.

## What to run

| Question | Statement | Applies to | Status |
|---|---|---|---|
| Server version | `CALL dbms.components()` | 4.x, 5.x, 2025.x | *(not re-read)* |
| Labels with their properties and types | `CALL db.schema.nodeTypeProperties()` | 4.x, 5.x, 2025.x | *(not re-read)* |
| Relationship types with their properties and types | `CALL db.schema.relTypeProperties()` | 4.x, 5.x, 2025.x | *(not re-read)* |
| Which labels each type connects | `CALL db.schema.visualization()` | 4.x, 5.x, 2025.x | *(not re-read)* |
| Constraints (uniqueness, keys, existence, type) | `SHOW CONSTRAINTS` | 5.x, 2025.x (late 4.x has it too) | *(not re-read)* |
| Indexes | `SHOW INDEXES` | 5.x, 2025.x (late 4.x has it too) | *(not re-read)* |

Server versions run 4.x, 5.x (5.26 is the last 5.x and a long-term-support release) and then calendar versions from 2025.01; the query language is versioned separately from 2025.06 (Cypher 5 and Cypher 25, with a per-database default). Those two facts were checked against the Neo4j upgrade guide and the Cypher 25 manual on 2026-11-23. Record the server version in the snapshot's `store` line, and confirm that the statements above run under the database's default language before relying on them.

## Direction is the part to check by hand

The property procedures list names and types. They do not show an arrow. Get the stored direction and endpoint labels from the data itself, bounded so it stays cheap:

```cypher
MATCH (a)-[r]->(b)
WITH labels(a) AS startLabels, type(r) AS relType, labels(b) AS endLabels
RETURN DISTINCT startLabels, relType, endLabels
LIMIT 500
```

This is plain Cypher (`labels()`, `type()`, a directed pattern) and works on every version above. On a large graph, sample instead of scanning: add `WITH a, r, b LIMIT 200000` after the `MATCH`, and say in `coverage` that the patterns come from a sample.

## Stored form

For each property a query will filter or sort on, look at real values before writing the filter: `MATCH (n:Label) RETURN n.prop, count(*) ORDER BY count(*) DESC LIMIT 12`. A property typed STRING can hold dates or numbers; an INTEGER can be a year, an epoch in seconds or an epoch in milliseconds. The type column of `db.schema.nodeTypeProperties()` tells you which comparison is legal, not what the value means.

## Traps

- Procedures that describe the schema read existing data, so a label or property that no node currently has does not appear, and a property key that was used once can linger in key listings after its last value is gone. *(not re-read)* Trust the per-label procedures over a bare list of keys.
- A constraint proves a property is intended to exist and be unique; it does not prove every node has it, unless it is an existence or key constraint.
- When only files are available (constraints, migrations, `LOAD CSV` scripts), `scripts/schema.py cypher-files` reads them instead. A `LOAD CSV` field is text until the script converts it, so a property set straight from `row.x` is a STRING whatever it looks like. *(not re-read)*

## Vendor material

Neo4j publishes its own documentation and agent tooling; prefer it for anything beyond schema introspection. This file is an independent note and is not endorsed by Neo4j.
