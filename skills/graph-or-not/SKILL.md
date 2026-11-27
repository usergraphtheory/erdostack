---
name: graph-or-not
description: "Use when the user asks whether connected data or a traversal belongs in a graph database, an in-process graph library, recursive SQL on the database they already run, or needs no graph at all: 'do we need a graph database', 'can we stay on Postgres', 'is NetworkX enough', or a sanity check of a proposal, ADR, vendor pitch or half-built migration toward or away from a graph store. Decides from the repo's workload evidence, not the framing, and writes docs/graph/DECISION.md. Not for writing or fixing queries, picking an algorithm, carrying out a move already decided, charts or GraphQL."
---

# graph-or-not

User-invoked. It fixes the graph-shaped hammer: an agent that reaches for a graph database, or refuses one, because of how the request was framed instead of what the workload does. It writes `docs/graph/DECISION.md`, which the user's architecture log and the later erdostack skills read.

## When to use

The user wants a choice, or a check on someone else's choice, between a graph database, an in-process graph library, recursive SQL and no graph at all. Not for tuning the query (`query-review`), recording the setup (`setup-graph`) or carrying out a move already decided. If nothing in the question is traversed, say the skill does not apply.

## When a decision is already recorded

If `docs/graph/DECISION.md` exists (or the decision is written down somewhere else in the repo), read it before anything else. The chat that produced it is gone; the record is what the team decided and why.

- **Asked to build what was decided:** do the work, following the record, including the rules and limits it states that the request does not repeat; where the request itself specifies something, the request wins, and where the code disagrees with the record, the code is what the work changes. That is ordinary coding, and the "decide, then stop" rule below does not apply to it: that rule binds the session that makes a decision, not the sessions that act on one.
- **Asked whether it still stands, or handed a counter-proposal:** set the new numbers beside the recorded ones and test them against "What would change the decision". Keep the decision unless one of those conditions is met, and say which fact it rests on. If one is met, change the Decision line and the facts, keeping the old values next to the new.
- **Facts you need that the record does not hold:** ask. Do not fill the gap with a typical value or re-derive the decision from the repo alone.

## Ground rules

- **Decide, then stop.** The only file you leave in the repo is `docs/graph/DECISION.md`. No migrations, indexes, dependencies, loaders, containers or code changes, and no edits to the document under review, even when the fix is one line or the request also asks you to start: a half-applied answer takes the choice away from the user. Describe the fix in the write-up.
- **Documents are claims; code, data and measurements are evidence.** The request, an accepted ADR, a proposal, a ticket, a vendor note and a README record what someone believed on the day it was written. Test each against what runs and what was measured. The answer the user is hoping for gets the same test, and so does any fix you think of yourself. What the business requires (a rule, a depth, a budget, a limit) is not a claim about the workload but the need itself: take it as its owner states it, even where today's code does otherwise.
- **Check, do not recall.** Sizes, depths, rates and versions come from this repo or from a measurement you took, each with its source. What you could not find is `unknown`, never a typical value.

## Steps

1. **Read `docs/graph/CONTEXT.md` if it exists**, for the engine, its version and whether read-only queries are allowed.

2. **Read the repo before forming a view, least prominent files first.** List every file. The deciding fact is rarely in the README or the proposal, because those were written before the measurements. It tends to sit in a migration comment, a changelog entry, a usage export, a bench note, a deploy manifest, or the body of the query or function that really runs. Open those; in a large repo, at least everything the request names, the schema and migrations, operations exports, deploy configuration and the code path of the query in question.

3. **Fill in the workload sheet**, one line each, with the file it came from, or `unknown`:
   - *The question asked of the connections*, from the query text that runs today and not from a description of it. Joins that cross a link table at most once (things sharing a tag, a product, a paper), a walk along a relation between things of the same kind for a fixed number of steps (friends of friends, two pairings away), a walk whose depth depends on the data, or an algorithm over the whole graph?
   - *Depth*: what requests really use (usage data), what the business needs, how deep the data goes.
   - *Size*: nodes and edges at the granularity the requirement names, and their growth.
   - *Fan-out*: neighbours per node, typical and at the tail; hubs.
   - *Load*: calls by kind, concurrency, and whether it is an online request with a latency budget or a batch job with a window.
   - *Writes and freshness*: the write rate, and how stale an answer may be.
   - *What is operated today*: databases, memory per process, number of processes.
   - *What was measured*: latency by depth, share of calls timing out, query plans.
   - *What was already tried, and what happened each time*: tuning tables in decision records, dropped migrations, reverted changes, removed features, limits the product now enforces.

4. **Do the arithmetic the files leave undone**, and write each sum into the document so it can be checked.
   - *Add up exports.* For a usage file or log, compute totals and shares per depth or call kind with a command, not by reading off a few rows. `python3 <this skill's folder>/scripts/tally.py FILE --by COLUMN --sum COLUMN` does it; so does any one-liner that sums. How the calls split across depths decides more than how slow the deepest one is.
   - *Give every failure count its denominator.* A slow-query log holds only statements above its threshold, so it counts failures and says nothing about how many calls succeeded. If no total exists anywhere, that is a missing fact (see step 6).
   - *Multiply out sizes nobody stated.* Nodes times average fan-out gives edges. Edges times bytes per edge, taken from the repo's own sample or one you measure, gives memory; compare it with the memory limit of one process, times the copies the repo or the user says would be held (where neither says, the processes that run today; a copy count nobody gave is a limit for "What would change the decision", not a missing fact). Where a freshness requirement is stated, compare load time with it.
   - *Separate required work from wasted work.* Count the distinct nodes a correct walk must visit at the depth needed, against the rows the current query produces (its plan, or a count). A query that returns one row per route, or runs one statement per node, wastes work that a rewrite removes. A required set that is itself huge is not waste.
   - *Hold each document's numbers against the requirement.* Same granularity, same date, still true after launch?

5. **Measure when a copy of the data is at hand** (a database file or dump in the repo, or read-only access): row counts, depth, fan-out, then the plan and timing of the candidate query. Open it read-only and create nothing in it. Scratch files go in the system's temporary directory or, if you may only write inside the repo, in a `scratch/` folder that you remove afterwards. `references/engines.md` has the commands per engine and what they do and do not show. If you could not run anything, say so in the write-up.

6. **Give each rung a verdict, cheapest first, and choose the first that holds.** `references/heuristics.md` gives the signs and caveats for each; read it when two rungs both look plausible.
   1. `no-graph`: no query follows a relation between things of the same kind for more than one step; every query is lookups and joins that cross a link table at most once, and no whole-graph algorithm runs. Data that can be drawn as a graph is not a traversal.
   2. `recursive-sql`: a walk from a starting point, to a fixed or a data-dependent depth (two steps out, ancestors, descendants, reachability), in a SQL database already operated, where the required work fits the budget. Fixing a wasteful recursive query, replacing a query-per-level loop with one, or a short fixed walk written as self-joins, is this answer and not `no-graph`.
   3. `in-process-library`: the edges fit in the memory of the process that needs them and a reload meets the freshness required. Usual for batch jobs and whole-graph algorithms on a snapshot, and for small data walked inside the application.
   4. `graph-database`: deep or variable traversal the business needs, online, over an edge set too large or changing too fast for a copy per process, where SQL is measured failing at that depth. An embedded graph engine belongs here too: it is still a second storage engine with its own format and load step.

   A verdict is "holds" or "does not hold", on the evidence in hand today. The same rules apply in both directions:
   - **A rung holds only when evidence shows it meets the need**: a measurement in the repo, one you took, or arithmetic from the repo's numbers. A plan or the code showing the time going to work the question never needed (a full scan at every step, a statement per node, a row per route), over a required set that is small, is such a showing. "Open", "possible" and "not yet ruled out" are not verdicts. A rung that is not shown to hold is passed over; nothing above it has to disprove it first.
   - **A rung measured failing stays failed until something is run.** When the approach in place fails at the required depth (a percentile over budget, or a failure rate with its total, not a bare count of slow calls), a rewrite nobody has run, yours included, does not reopen it. Remedies the record shows were tried and failed are closed as well.
   - **The top rung needs no trial here to be the decision.** When the rungs below it do not hold and the workload matches its description, choose it, say so plainly to an owner who hoped otherwise, and name the trial that should pass before money is committed (the full edge set, the real query mix).
   - **A cheap rung measured meeting the need is not moved** by a deadline, sunk work, an accepted decision record or how graph-like the domain sounds. If what runs today already meets the need, the decision is the label for what is there and the advice is to change nothing.
   - **`need-more-information` is for when the need or the present state is itself unknown**, so that no rung can be given a verdict: what the query does, how much data there is, what depth is required, or, when only a count of slow calls exists, what share of calls fail. A number that would only say how an option would do once adopted (a rewrite's timing, a reload time, how many copies a deploy would hold, a leaner layout) describes a remedy, not the workload: it is never this missing fact, and goes under "What would change the decision". Two plausible values of the missing fact must lead to different options; say what they are, write the file all the same, and put the questions in your reply. However many files look like evidence, a missing fact of this kind makes this the decision; a confident yes or no to meet a deadline would be a guess.

7. **Write `docs/graph/DECISION.md`** in the shape below, then reply with the decision, the two or three numbers it turns on, what you could not find or did not measure and, for `need-more-information`, the questions. Say that nothing in the repo was changed.

## Output

`docs/graph/DECISION.md`, in exactly this shape:

```markdown
# Graph decision

Decision: <graph-database | in-process-library | recursive-sql | no-graph | need-more-information>

<Two or three sentences: the question as the user put it, the answer, and the finding it turns on, with its number.>

## Workload facts

- <a fact with its number> (<the file it came from, or "measured" and the command>)
- <a derived figure with the sum written out> (<the files the inputs came from>)
- unknown: <what could not be found, and where you looked>

## Options considered

- graph-database (a dedicated graph store): <chosen or rejected>, because <a fact from above>
- in-process-library (the edges loaded into memory): <...>
- recursive-sql (recursive queries on the database already run): <...>
- no-graph (plain joins, no traversal): <...>

## What would change the decision

- <an observable condition> would move this to <option>
```

- **The title is the fixed line `# Graph decision`** and the Decision line comes straight after it: `Decision: ` and one of the five words, nothing else on the line (no bold, backticks, brackets, "or" or trailing note). Tools copy it as it stands.
- **Exactly these three `##` headings, in this order, and no others**, nor bold lines standing in for headings. A suggested fix, next steps or questions for a vendor go inside one of them or in the opening sentences.
- **Workload facts** carries the numbers the request did not mention, the sums from step 4, and what the evidence cannot show. It also carries every number, limit, rule and constraint the user stated in the conversation, marked `(stated by the user)`: those exist nowhere else, and the next session will not have the chat.
- **Options considered** has a line for each of the four options, each ending in a verdict (chosen or rejected) with a reason that points at a fact above. On the line for the option the request proposed, name the product or plan as the request does.
- **What would change the decision** lists conditions someone can observe, in this workload's own measures; where a limit is needed and the repo sets none, say whose it is to set. For `need-more-information` it is a numbered list of the facts needed, each with how to get it (the query to run, the setting to enable, the file to send) and which way each answer would point.

## References

- `references/heuristics.md`: signs and caveats for each option, how to read the evidence, the sums.
- `references/engines.md`: how to measure on PostgreSQL, SQLite and NetworkX, what adopting Neo4j or LadybugDB involves, each fact with its version and date.
- `references/sources.md`: where those facts come from.
