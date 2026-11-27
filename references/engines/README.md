# Engine packs

One markdown file per engine: `neo4j.md`, `ladybugdb.md`, and so on. A pack holds what an agent must know about that engine and would otherwise get wrong: which query language and version it speaks, how to introspect the schema, how to read a query plan, which packages and drivers are current, and where its dialect differs from what the agent expects.

A pack loads only when the repo's `docs/graph/CONTEXT.md` (written by `setup-graph`) names that engine.

## Rules

- Start from [`templates/engine-pack.template.md`](../../templates/engine-pack.template.md).
- Include a `Last verified: YYYY-MM-DD` line. The validator rejects packs without one.
- Every factual claim carries the engine version it applies to.
- Test against the real engine. Emulators that substitute a different query engine do not count.
- End with a pointer to the vendor's own skills or documentation.
- Say plainly that the pack is independent, unless you are the vendor and say that instead.

## Status

No packs yet. Neo4j and LadybugDB are planned first; the third slot is reserved for the first outside contributor. See the [roadmap](../../ROADMAP.md).

How packs travel with skills that are installed one folder at a time is settled together with the first skill that needs them.
