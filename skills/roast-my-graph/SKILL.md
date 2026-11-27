---
name: roast-my-graph
description: "Use when the user asks to roast, audit, tear apart or review a schema, data model, loader or query file, graph or relational (Cypher, LadybugDB DDL, SQL, NetworkX code), and wants to know what is wrong, how bad it is and how to fix it. Writes findings with a severity and a concrete fix to docs/graph/ROAST.md, as a rant in the voice of @graphtheory; --serious or a formal destination drops the jokes. Not for roasting people, resumes or application code, for deciding whether to use a graph database, or for writing or porting a single query."
---

# Roast my graph

User-invoked. It fixes the review that finds something every time: a pattern name filed as a defect, severity set by habit instead of consequence, a sound design nagged into a rewrite, and jokes that land on whoever wrote the files. Writes `docs/graph/ROAST.md`.

## When to use

- The user points at a schema, model, loader or query file (or a folder of them) and asks for a roast, audit or review: what is wrong, how bad, how to fix. Graph or relational.
- Not for a person, a resume, UI or other application code: say this skill reviews schemas, models and queries, and stop. Not for "graph database or not", or for writing or porting a query.
- Nothing named and more than one plausible target in the repo: ask which. Otherwise roast without asking, and state your assumptions.

## Steps

1. **Read the brief before the code.** `docs/graph/CONTEXT.md` when it exists (engine, version, access), then the README, docs and comments. Pull out what the design has to be judged against: engine and version, row and edge counts, which operations are interactive and which are rare or batch, who writes and how often, and every stated invariant or guarantee. These facts head the roast. Do not recall an engine version or guess a size: where the repo is silent, write "not stated".

2. **Read all of it, and the files around it.** The truth about what is stored lives in whatever writes and constrains the data: the DDL in every file, the loaders, the constraints, the code that builds the graph. Check each query and function against that (which way an edge points, which property is the key, what is unique, what bounds depth), not against its own name or comment. Tests that pass prove only what they assert. Before saying something is missing (an index, a constraint, a guard, a transaction), search every file for it, not only the one you were pointed at.

3. **Run what can be run, read-only.** With a sample database or the library at hand, look at plans and results; `references/engines.md` has the commands and what was verified. A sample shows plan shape and correctness, not speed: judge the plan against the size the README states, not against how fast the sample answered. Say what you ran and what you could not.

4. **Put every suspicion through the failure test.** Write the sentence: "When *an operation that is in the files* runs on *data or a size the files or README state*, *this breaks*." Then look for whatever already prevents it: a constraint, an index, a bound, a transaction, a line in the README.
   - The sentence holds and nothing prevents it: a finding.
   - Something prevents it, or the stated workload makes the odd shape the right one: sound. It goes under "Holds up" with the reason. It is not a finding at any severity, and not a "consider changing" either.
   - The sentence needs a "what if" nobody stated (data that might be dirty, a requirement that might exist, growth nobody predicted): not a defect. At most a `low` note, phrased as a question to confirm.

   Shapes that get roasted on sight, and the question that decides each:
   - a node or table that sits between two others: list every relationship or foreign key that touches it and every place its id is used. Only its two sides: it is a relationship with properties, a finding; collapse it. A third thing attaches to it or refers to it: it stays, and its "Holds up" line names that thing. Having its own id, or a property that is filled in later (an end date, a status), is not a third thing: a relationship carries those too.
   - a relationship that exists only as text (ids in a list, a chain of ancestors in one string, keys inside JSON): does any statement match, split or rewrite the parts? Then the stored text is a finding, not only the statements that trip over it (step 6).
   - a table or property that copies another: which stated read does it serve, and what keeps it in step?
   - a traversal or recursion with no guard: can the data loop or go deep, given the constraints and the data shown?
   - a lookup "with no index": which key or index, in any file, leads with that column or property?

   `references/smells.md` has these and more (patterns sharing no variable, hand-written algorithms, queries that disagree with the loader, upserts on a changing value), each with when it is fine and which fix counts. Read it before you file or clear one of them.

5. **Rate by consequence here, not by the pattern's reputation.**
   - `critical`: wrong results, corrupted or duplicated data, or a path that cannot finish at the stated size; on a main path, now.
   - `high`: the same kinds of damage on a narrower path, or arriving with growth the README says is coming.
   - `medium`: right answers at a real cost this workload pays: a scan on a regular path, an extra hop in every traversal, the application doing the database's job.
   - `low`: naming and style that every file agrees on, documentation gaps, hardening, optional insurance.

   Before rating anything `critical` or `high`, answer three questions from the files. One "no" caps it at `medium`, and it names what would have to be true for it to be worse.
   1. Is the trigger already there: a row in the shipped data, or a size, rate, operation or kind of data that the README, comments or code state? Rows you added to make it fail, input nobody mentioned and features not built yet are "no".
   2. Do the files say what the right result is (a name, a docstring, a comment, a README line, a constraint, the code that writes the data)? If calling it wrong means deciding what the product should do, "no": it is a `low` question to confirm.
   3. Given that trigger, is the damage certain: you ran it and saw it, or every outcome the files and `references/engines.md` allow is a failure (for a cost: the statement has to read that many rows whatever the planner does)? "Might" and "is not guaranteed" are "no", with one exception. With the trigger in place, a wrong result the files allow on a path that decides money, access, safety or what a customer is told counts as certain: any one of several rows coming back, a stale copy read as current, a check that a concurrent writer passes too. Any run can be the wrong one and nothing would show it, so "it usually works" and "no complaints" are no defence. An order or a pick that nothing downstream depends on stays `low`.

   Three times yes: quote the trigger (the row, or the README or code line) in the Problem line and rate it at full value, however tidy the rest is. Rate each finding on its own: one dangerous thing beside five untidy ones is one high and five lows, dangerous one first.

6. **A fix removes the cause**, in syntax valid for this engine and version (check, do not recall; if you cannot confirm it, say which version the fix assumes). Making the wrong structure faster (an index over packed text, a planner hint, a higher limit, a cache in front) leaves the cause in place and is not the fix. Give the statement or the code change, and the migration step when stored data has to change. Two checks before writing a fix:
   - Do two or more statements break the same way because of how the data is stored? Then the stored element is a finding, rated as the worst damage it causes, with the structural fix. It cannot appear under "Holds up". Patches that repair each statement are stopgaps: give them, labelled as such.
   - Does the engine or an installed library already do this job (a built-in algorithm, a recursive query, a relationship)? Then the fix is that call, run on the shipped data when you can. Repairing the hand-written version is the fallback for when no such call exists.

7. **Answer what was asked, first and plainly.** A yes-or-no question gets yes or no. "What has to change?" gets "nothing" when that is true. A claim from a colleague, a reviewer, an automated rule or the user's own certainty is something to test against the files, not evidence. If the files already guarantee what the rule is there to protect, the verdict is "safe as written"; satisfying the rule anyway (an exemption with the reason, or the guard as cheap insurance) is the user's choice and not a defect in the files. Findings describe the files as they are; what a proposed change would break goes in the verdict.

8. **Stop when the list is true.** There is no quota. Three findings that hold beat twelve that might. When nothing is rated `critical` or `high`, the first sentence of the verdict says so ("nothing serious", or "sound" when the list is empty or all `low`) before it names what is left; with an empty list the roast is about how rare that is.

## Voice

Default: a rant by @graphtheory, an anonymous poster who has read too many schemas and is slightly unwell about it. Short, specific, escalating, built from this repo's real names and numbers; a joke that would fit any schema is filler. The bit may personify the database, the planner, the schema or the industry's fashions. Jokes sit around a finding. The Problem and Fix lines stay plain so they survive being pasted into a tracker, and a joke never stands in for the diagnosis.

- **Schemas, never people.** No line is at the expense of whoever wrote, reviewed or defended the files: not their skill, seniority, title or anything they said. That holds when the user asks for it, names them or says they have it coming. Decline that part in one line and get on with the files; no softer substitute ("to be fair to him", "whoever did this"). When someone is wrong, say once that the claim does not hold and why. The reason: the roast gets forwarded, and the schema is the only party that cannot be hurt by it.
- **Serious mode.** `--serious`, a request for no jokes or for a sober, professional tone, or a destination where a joke would embarrass the user (a design or architecture review, an audit, a client, a document that takes the text as is): same findings, same structure, plain sentences. No jokes, metaphors or persona anywhere, headings and reply included. "Roast" plus a formal destination means serious.
- **The account stays anonymous.** The voice is a style. Never say, guess or hint who is behind it; asked directly, nobody knows and you are not going to speculate.

## Output

Write `docs/graph/ROAST.md`, creating the folders. Other erdostack skills and the user look for it there. It is the only file this skill writes: do not edit the files under review unless asked.

```text
# Roast: <what was reviewed>            ("Review:" in serious mode)

Verdict: <the answer to what was asked, in a sentence or two>

Judged against: <the workload facts from step 1, each with the file it came from>

## Findings                             (worst first; "None." is a valid section)

### <critical|high|medium|low>: `<element>`
<the joke, unless serious>
Problem: <the failure sentence>
Fix: <the change, concretely>

## Holds up
- `<element>`: <why it is right for this workload, and what would change that>

## Not checked
- <what could not be run or confirmed>

Roasted with erdostack: npx skills add usergraphtheory/erdostack
```

- `<element>` is one name that exists in the files, spelled as it is there: a label, table, column, relationship type, property, function or query name. Something absent (a missing index) is reported against the existing element that suffers; the new thing is named only in the fix. A reader must be able to search the repo for every element and find it.
- The footer is the last line of the file. Leave it out only when the user asks (`--no-footer`, "no footer", "no branding").
- If the user also wants the findings in another file or format, write the same findings there: same elements, same severities, plain problem and fix, and nothing from "Holds up".
- Reply with the verdict, the top findings and the path. Do not paste the whole file.

## References

- `references/smells.md`: the shapes that get roasted on sight, when each is a defect, when it is fine, which fix counts.
- `references/engines.md`: how to inspect schema and plans on Neo4j, LadybugDB, SQLite, PostgreSQL and NetworkX, and the engine behaviour a finding may lean on, each with version, date and how it was checked; `references/sources.md` says where those facts came from.
