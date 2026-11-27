# Smells, and when they are fine

For each shape: the question that decides it, when it is a defect and roughly how bad, when it is sound, and which fix counts. Severities are starting points; the stated workload decides (SKILL.md, step 5). Engine behaviour these lean on is in `engines.md` with its verification status. Written in our own words; nothing here is copied from a source.

## A node or table that sits between two others

- **Decides it:** what else touches it? List every relationship type or foreign key that starts or ends at it, and every place its id is used.
- **Defect** when it has one link to each side, nothing else points at it, and its properties are facts about that one pairing (often with both endpoint keys copied onto it). Every traversal pays two hops and the loader keeps two links in step to say one thing. Usually `medium`.
- **Sound** when you can name a third thing in the files: something attaches to it (a relationship cannot start or end at another relationship, so whatever must point at "this particular occurrence" needs a node), it joins three or more things, another table or node refers to it by id, or it links to others of its kind. In SQL, also when the same pair has to be stored more than once and each row is referred to separately. Write the third thing in the "Holds up" line; if you cannot name one, it is the defect above.
- **Not a reason either way:** "it has properties" (relationships carry them too); "it has its own id" (so does every row copied from a relational table; what matters is whether anything uses the id); "one of its properties is filled in or changed later" (an end date or a status on a relationship can be set later too); "the same pair can be linked more than once" (property graphs generally allow parallel relationships of one type; check yours); "it looks like a join table" (so does every event).
- **Fix that counts:** one relationship, or one row keyed by the pair, carrying the properties; the old links and copied keys removed; the migration. Keeping the node and adding indexes is not it.

## A list packed into one value

Several ids or attributes in one delimited string, JSON text or blob. The same goes for any relationship that exists only as text: a chain of ancestors written into one string, a parent named by a prefix.

- **Decides it:** does anything search, join, traverse or validate by the individual items?
- **Defect** when the items refer to other rows or nodes, or are filtered on. Nothing can check that they exist, a lookup becomes a text match over every row, and the application walks the structure itself, one round trip per level. `medium` at least when a regular query does this; `high` when the match can return wrong rows or the path is hot at the stated size.
- **Sound** when the value is opaque to the database: stored and returned whole. On a small in-process graph, attributes parsed out of one text field are `low` unless a hot path re-parses them.
- **Statements already wrong:** when statements that match or rewrite the text return or change the wrong rows on the shipped data, file each at the damage it does, and file the stored value as well. Tightening every match so it is exact today is a stopgap: the text is still the only record of the relationship, nothing checks that the parts exist, and the next statement has to get the matching right again. Do not list the stored value under "Holds up" in the same review.
- **Fix that counts:** one row per item with keys to both sides, or one relationship per item, plus the index for the direction queried; for a hierarchy, a reference to the parent row walked with the engine's recursive query, or a table of ancestor pairs kept in step by the write path. An index on the packed text, an exact-match patch on its own, or keeping the text as the source of truth, is not it.

## A table or property that copies another

An ancestor or closure table beside a parent column, a property repeating what a relationship says, a stored count.

- **Decides it:** which stated read does the copy serve, and what keeps it in step?
- **Sound** when the README names a frequent read the copy makes cheap, writes are rare or go through one path, and that path rebuilds or updates the copy. Look for the rebuild script, the transaction, the trigger or the loader step before saying there is none. Maintained redundancy is a design choice.
- **Defect** when a write path in the files changes the original and not the copy, or queries read both and can disagree: `high` when a user-facing result depends on it. A copy nothing reads is dead weight: `low`.
- **"What if" only:** "someone could edit it by hand", "two writers might collide", "the rebuild could fail", with nothing in the files showing it happens. A `low` question at most.
- **Fix that counts:** update the copy in the same write path or transaction as the original, or delete it and read the original.

## A traversal with no guard

An unbounded variable-length pattern, a recursive query with no depth counter or cycle check, a recursive function.

- **Decides it:** what shape can the data actually take, and how large is the reachable set at the stated size?
- **Check in order.** (1) Does a constraint make a loop impossible or cap the depth (a key or check that forces each row strictly below its parent, a fixed number of levels)? (2) Is there data? Search it for a loop and run the walk under a row or time cap. (3) Are loops ordinary data here (peer links: A points at B, B points back)?
- **Defect** when a loop can exist and the walk revisits rows without end, or the reachable set is a large share of a large graph on an interactive path. It does not finish: `high` or `critical`.
- **Sound** when the schema bounds it, or the stated depth is small and each step is an index search. The verdict is then "safe as written", also when a rule or a reviewer wants a guard. Adding one is optional insurance: a line under "Holds up", or `low` and labelled optional.
- **In between:** a tree by convention only, no loop in the data shown. A `low` or `medium` hardening note that says what would have to go wrong first.
- **Fix that counts:** an upper bound, or tracking what was visited, and it must actually stop the walk (`engines.md`, SQLite: de-duplicating rows does not stop a loop when each row carries a counter). A figure read far more often than it changes can be precomputed. Raising a limit or timeout is not it.

## A lookup with no index behind it

- **Decides it:** which declared key or index, in any file, leads with the column or property the lookup filters on?
- **Before filing:** search every file. Check how this engine provides an index (a primary key or uniqueness constraint usually is one: `engines.md`), so another engine's habits do not produce "no indexes defined". A composite key or index serves its leading column only: an edge table keyed (a, b) is searchable by a, not by b.
- **Defect** when a regular or interactive query filters on something no key or index leads with, at a size where reading every row hurts: `medium`, `high` when the path is hot and the table large.
- **Sound** when the table is small or the query is rare or batch. Say so and move on.
- **Fix that counts:** the exact index statement, leading with the filtered column, valid for the engine. With a sample database, confirm the plan changes from a scan to a search.

## Patterns that share no variable

- **Decides it:** how many rows can each side produce?
- **Defect** when both sides can produce many rows and an aggregate follows: each row is counted once per row on the other side, and the totals are wrong while looking plausible. `high`.
- **Sound** when each side is a single row found by a unique key.
- **Fix that counts:** connect the patterns, or aggregate each side separately before combining. A DISTINCT on top hides duplicates without repairing counts.

## A hand-written graph algorithm

- **Decides it:** does it compute what its name and callers claim? Read what it does with weights, direction and termination; if the library is installed, compare answers on the shipped data.
- **Defect** when the result differs from what callers rely on (weights ignored, the walk going the wrong way, stopping early): wrong answers, `high`. Bundled tests that pass do not clear it; read what they assert.
- **Sound** when it is correct and the library has no call for the twist this problem needs. Correct but longer than the library call: `low`.
- **Also a defect** when it is correct but so much slower than the library's version that a stated job no longer finishes: rate by that job.
- **Fix that counts:** when the installed library has the algorithm, the library call with the right arguments (weight attribute named, iteration limit left at its default or raised if it stops early), compared with the old output on the shipped data. Lead with that call; a corrected loop is the fix only when the library has nothing for the twist this problem needs. A library call that keeps the same mistake is not it.

## A query that disagrees with the writer

- **Decides it:** for each relationship, key and property a query uses, what does the loader or DDL actually write: which direction, which property, which name?
- **Defect** when they differ: the query returns nothing or the opposite set and raises no error. `high`.
- **Which side to change:** the one that disagrees with everything else. Count the queries and tests that rely on the writer's convention before proposing to flip the writer.

## An upsert keyed on a value that changes

- **Decides it:** is every property in the match part of a MERGE or upsert part of the thing's permanent identity?
- **Defect** when one is not: the first load after that value changes matches nothing and creates a second node or row for the same thing, inflating every count that joins through it. `high` or `critical`.
- **Fix that counts:** match on the key alone and set the rest afterwards; remove the duplicates already stored; then make the key unique, in that order.

## Natural keys, nullable columns, missing checks

- **Decides it:** do the files or the data show the bad case (rows without the key, one key in two spellings, values out of range)?
- **No evidence:** not a defect. The lookups the README lists by that key are why it is the key. A `low` question at most.
- **Evidence** (the sample has such rows, the loader has a branch for them): rate by what breaks.

## Naming and style

Mixed conventions, an odd name, a leftover property. When every file spells it the same way nothing breaks: `low`, one line each, after the real ones. When the spelling differs between files it is "a query that disagrees with the writer".
