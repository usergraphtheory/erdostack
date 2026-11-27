---
name: query-review
description: "Use before you write, fix or run a job that changes or deletes many rows, nodes or relationships in a graph (Cypher on Neo4j or LadybugDB, SQL over node and edge tables): a purge, backfill, rescale, merge, relabel, archive, loader or upsert, or a request to run one on a live database. Also when a linter, scanner, audit or reviewer flags such a job or a graph query and asks for a change. Makes the change exact, within the repo's limits and proven on a copy, hands production changes back for review, and leaves correct code alone with the reason. Not for tuning read queries."
---

# query-review

Model-invoked. It fixes two failures: a bulk change that touches the wrong rows, breaks the repo's transaction limit or runs on production unreviewed; and a correct statement rewritten because a tool or a person said so. It writes a review note in the reply, and appends it to `docs/graph/REVIEW.md` when `docs/graph/` already exists.

**A** applies when you write, fix, review or are asked to run a statement or job that changes many rows. **B** applies when a linter, scanner, audit or reviewer flags a statement or job. Not for speeding up reads, modelling or explaining a query.

## A. A change to many rows

1. **Target and rules.** Read `docs/graph/CONTEXT.md` if it exists, the runner's config and the repo's docs on jobs, maintenance or changes. Write: `target: <db the job or runner reaches by default>, production: yes/no · limit: <rows per transaction> (<source>) · re-runs: <does the repo re-run jobs or overlap windows> (<source>)`. If you cannot tell whether a target is production, it is.
2. **The rule, from the request and the repo.** When the request names its rows exactly (a statement, a filter, a list) and no repo text states a different rule for them, that set is the rule: change exactly it. Rows you think should also go, or stay, because of links or what the data shows, go to the user as a question, not into the change. Otherwise a request is shorthand; the repo usually states the same rule in full somewhere: a schema comment, a trigger or constraint that enforces it for new data, the app code that does it from now on, a doc on what an item consists of. Read those and write the rule so that the job leaves the existing data as that code would have left it. Check every way a row can fall under it: both ends of a relationship, each table a polymorphic id can point to, rows attached to an item but not marked themselves, and rows that qualify only after another row changes. Such a dependent is in scope only if the rule says rows like it go (being left unlinked is not enough) and this change is what makes it qualify: it had a link to a row the job removes or changes and has none left to a row that stays. A row that already matched before the job (never linked, empty on purpose) is not the job's, so pick dependents before the first write, not with a "has no links" test afterwards. Repeat level by level only when the rule itself cascades; when the request fixes the set at the start, take it once. For a loader or upsert the rule is identity: the key the repo calls unique and stable; two different input rows must never land on one node or row. Write: `rule: <one sentence> · sources: <files>`.
3. **Count it independently.** On a copy (step 5), select what the rule covers with a plain query or a short script, not with the job. Write: `should change: N` (per kind when there are several).
4. **Make the smallest change that does it, in the file.**
   - Edit the job or statement itself. A fix described only in the reply is not delivered; only a production run is held back.
   - If the existing job is wrong by the rule, fixing that is part of the task even when you were asked only to review it or make it faster. Say what it got wrong.
   - Keep the repo's job shape, the connection it is given and its return value. Change only rows the rule names: no new tables, columns or progress rows, and no restructuring of parts that already work.
   - Stay within the stated per-transaction limit and any stated rule about what readers may see mid-run. If they seem to conflict, read what you need (old values, totals) before writing so both hold, or ask.
   - Syntax that depends on the engine version is in `references/`; check it on the copy, not from memory.
5. **Prove it on a copy.** When the repo's docs name a scratch or development target for trying changes, run it there with the repo's own tool, as they say; reviewers expect those counts. Otherwise, for a single-file database, copy the file to a temporary folder. Never production. Run the job the way the repo runs it, to the end. Compare rows, not only counts, and write:
   - `should change: N · job changed: N · same rows: yes/no` (keys diffed; for an update, new values checked against expected, each row changed once)
   - `other rows or tables changed: 0`
   - `largest transaction: N rows (limit L)`
   - `second run: <same end state | changes nothing>` when the repo re-runs jobs or overlaps windows, or the request asks for crash safety (then also kill it partway and rerun). Otherwise state whether a rerun is safe; do not add machinery to make it so.
   Any mismatch means the job is wrong: fix the job, never the expectation. If nothing can run here (no server for this engine), write `untested` and give the reader the commands that would check it on their side: the count query for the rows, and `EXPLAIN` or `PROFILE` for the statement.
6. **Production: hand it back, do not run it**, even when the user asks and the wrapper works. `EXPLAIN` (plan only) is fine there; nothing that writes. Save the change in the repo's change format (folder, numbering, header) and show it in the reply: the count query with the copy's number, the statement within the limit, the check to run afterwards, and who applies it under the repo's process. Never save an unbounded or unscoped version anywhere. A doubt goes in the header as a question for the reviewer, never in place of the file. A development target the user asked you to change may be run after the copy checks out.
7. **Say what changed.** Lead with the rows it changes (N of what), then the rule and its sources and the step 5 lines. If the request had two readings, implement the one the repo's rule supports and name the other in one line.

## B. A flag on something that may be right

1. Write what the statement is for (its docs, callers, tests) and the concrete harm the flag predicts here: wrong rows, lost data, a long lock, a half-built table visible to readers, a large scan. A rule ("no unscoped delete", "no DISTINCT", "batch it") points at a harm; it is not one.
2. Check whether the harm happens. Read the code the flag says is missing (an inner loop, a transaction boundary, a subquery's scope, a guarantee the docs give about the data) and, where you can, run it on a copy and measure. Write: `flag predicts: <harm> · observed: <what the code and the copy show>`. When you cannot run it here, add the one command that would settle it for the reader: a count query for a claim about rows, `EXPLAIN` or `PROFILE` for a claim about the plan.
3. If the harm does not happen, the file stays byte for byte as it was: no equivalent rewrite to quiet the tool, no added index, LIMIT, scope or batching, no fix for a nearby nit. Following the flag can itself introduce the bug. If part of the claim is true, fix that part only. A defect you think you see while checking gets the same test as the flag: show on the copy the rows that come out wrong. If you cannot, it is not a defect and the file still stays as it was.
4. **If a build or check is red because of the flag, make it green the repo's way** and leave the flagged code alone: the tool's own ignore file, allow-list or inline marker for that one finding, with the reason beside it. Rerun the check and write `check: green (<what you added, where>)`. A red check that you explained is still red.
5. Tell the user plainly: what was flagged, why it does not apply here with the evidence (file and line, doc sentence, number), and what would make it apply.

## Output

Lead with what the user asked for or must decide. Then the note:

- **Target**: engine and version, and which database you used or did not touch.
- **Rule** (A) or **Flag** (B): the sentence and its sources, or the predicted versus observed harm.
- **Numbers**: the step A5 lines, or what you measured for B, and one check the reader can rerun to confirm them even when you ran everything: a count query (`count(...)`) or `EXPLAIN`/`PROFILE` for a database, the counting snippet for an in-process graph.
- **Production**: the file handed back and who runs it, or "none".
- **Not verified**: anything you could not run or confirm.

When `docs/graph/` exists, append the note under a dated heading to `docs/graph/REVIEW.md`. Do not create the folder for it.

## References

Read only the engine file in use, when step A4 or A6 needs version-dependent syntax.

- `references/neo4j.md`: language versions, plan-only checks, batched writes.
- `references/ladybugdb.md`: names, plan-only checks, transactions.
- `references/sql.md`: SQLite and PostgreSQL write and copy facts. Executed.
- `references/sources.md`: where the dated facts come from.
