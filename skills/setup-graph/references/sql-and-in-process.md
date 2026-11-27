# Graphs in SQL tables and in in-process libraries

Last verified: 2026-11-23
Status: conventions of the erdostack skills, plus a few tool facts from prior knowledge that were not checked
against documentation on that date; those are marked "not verified". Only the SQLite foreign-key line was executed (dated there).

## Recognising them

- **Graph in SQL.** Node and edge tables, a self-referencing parent column, an adjacency or closure table,
  and queries that walk them with `WITH RECURSIVE`. There is no graph database: the engine is the SQL database
  that holds the tables.
- **Graph in process.** The code imports a graph library (NetworkX, igraph, rustworkx, graph-tool and the like)
  and builds the graph at start from files or query results. The library is the engine.
- **Neither.** Foreign keys in an ordinary schema, an ORM, a GraphQL API, a dependency chart in the docs. That
  is the no-graph case in the skill body.

## What to record

| Key | Graph in SQL | Graph in process |
|---|---|---|
| `engine` | the SQL database: `sqlite`, `postgresql`, ... | the library: `networkx`, `igraph`, ... |
| `engine_version` | see below | the locked library version |
| `query_language` | `SQL` | `none` (it is called from code) |
| `driver` | the client package and its locked version | the same library and locked version |
| `run_queries` | the repo's command for running a saved query | the repo's command for running an analysis, or `unknown` |
| `schema_snapshot` | a schema dump or the DDL the repo applies, else `none` | `none`, unless the repo keeps a description generated from the data |

- **Server SQL databases** (PostgreSQL, MySQL and so on): the version is the image tag or package pin, traced
  through the same override layers as any other server. See `override-layers.md`.
- **SQLite**: the SQLite library is compiled into the driver package or the language runtime, at a version of
  its own. The driver's version is not SQLite's. Unless the repo pins SQLite itself (a base image, a vendored
  copy), `engine_version` is `unknown`, with an open question saying where the real version can be read once
  the dependencies are installed. A version found inside a database file describes the library that last
  wrote the file, not the one that will run the next query. (Bundling and file-header behaviour: not verified.)
- **SQLite foreign keys**: declared in the schema but not enforced unless the connection runs
  `PRAGMA foreign_keys = ON`; a new connection starts with it off. When the repo's docs say the foreign keys
  keep edges attached, find every place a connection is opened (driver code, ORM connect hook, `sqlite3` shell
  scripts) and check that each turns it on; if not, that is an open question (skill step 7). (SQLite 3.53.1 via
  Python 3 `sqlite3`, executed 2026-11-24: the pragma reads 0 and a dangling reference inserts.)
- **In-process libraries**: take the locked version, not the manifest's lower bound. If you can see that the
  installed version differs from the locked one, record the locked one and mention the other under Evidence.
- **A graph extension inside a SQL database** (a Cypher or SQL/PGQ extension): not covered by this note. Record
  the host database as the engine and the language the repo's query files are written in, and list the
  extension and its pinned version under Open questions so the next skill does not assume plain SQL.

`access` and the ground rules apply unchanged. For file-backed graphs, read-only also means the data files:
do not rewrite, re-export or "normalise" them while looking.
