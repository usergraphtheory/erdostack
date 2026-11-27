# Decision heuristics for graph-or-not

Written 2026-11-23. These are rules of thumb in our own words, each with the caveat that breaks it. None of
them carries a threshold: where a rule needs a number, take it from the repository's own measurements or
measure it (`engines.md`), and say which.

## Is there a graph workload at all?

Three kinds of question get called "graph", and only two of them are:

- **Lookups across a link table.** "Customers who bought the same product", "recipes that share a tag". The
  query crosses a many-to-many table once and comes back. Such a table can always be drawn as dots and
  lines; that is a picture, not a traversal. This is `no-graph`.
- **A walk from a starting point.** Friends of friends, ancestors, descendants, everything reachable, how two
  things connect. It needs a relation from a thing to another thing of the same kind (parent, depends on,
  owns, linked to) and a question that follows it more than once: a fixed number of times (two steps out)
  or an unknown number. A short fixed walk is still a walk; it usually stays where the edges already live.
- **An algorithm over the whole graph.** Ranking, centrality, communities, all-pairs distances. Nothing is
  walked per request; a job reads every edge.

Caveats:

- Schemas drift away from their descriptions. A relation from a thing to its own kind may have been added
  after the documents were written, or removed. Read the newest migrations and the body of whatever the
  request path really calls before agreeing with anyone's description of the data, in either direction.
- Usage drifts away from plans. The depth that counts is the one requests use and the product still
  exposes, not the one a planning document expected.

## The four options, cheapest first

### no-graph

Fits when no query follows a relation between things of the same kind for more than one step. If such a
query is slow, the cause is an ordinary one (index, plan, ranking logic) and the fix is ordinary too.
Caveat: look for a depth or level parameter. An endpoint that looks fixed but takes one runs a walk.

### recursive-sql

Fits when the walk starts from one node, the database is already operated, and the set of rows the walk has
to touch is small against the time allowed.

Slowness that is not a reason to leave SQL, because a rewrite removes it:

- one statement per node or per level issued from application code;
- no index on the edge column the walk enters by, so every step scans the table;
- a recursive query that returns one row per route. With `UNION ALL`, or with `UNION` while a path or depth
  column is carried along, a node reachable by many routes comes back many times, and the count multiplies at
  every level (demonstrated on PostgreSQL 16.15 and SQLite 3.53.1, see `engines.md`);
- walking the whole reachable set and filtering afterwards when the question only needed the first hit.

Signs that it is the storage and not the query:

- the distinct set a correct walk must visit at the needed depth is itself large (see the sums below);
- the edge table and its indexes do not fit in the database's memory while many walks run at once;
- the record shows the tuning was done (indexes, caps, replicas, a precomputed table) and the failure rate at
  the needed depth is still there.

Caveats:

- A closure table or a precomputed "within N steps" table buys read speed with size and write cost. Its size
  follows the number of reachable pairs, not the number of edges. Estimate the pairs from the fan-out before
  proposing one, and look for a migration that already dropped one.
- Lowering the depth or capping hubs makes the query pass by changing the question. Check what the business
  loses (the record often says) before counting that as a fix.

### in-process-library

Fits batch and analytic work on a snapshot (the job reads all edges, computes, writes results back), and
small reference data walked inside the application. The edge list must fit, with room, in the memory of the
process that needs it, and a reload must meet the freshness the readers need.

Caveats:

- Memory per edge depends on the library and on the attributes kept. A general-purpose Python structure
  costs far more per edge than the rows it was loaded from; an array-based library costs much less. Use the
  repository's own sample measurement if there is one, or load a sample yourself and scale it; a guess in
  either direction decides nothing.
- Every process holds its own copy and reloads it on its own clock. Count the copies, and check that the
  platform has a machine as large as one copy.
- Size the right thing. A plan sized in a coarse unit (modules, say) for a requirement stated in a finer
  one (functions) is off by the fan-out between the two.
- One dedicated service holding a compact structure and applying changes as they arrive is a different design
  from a library in every replica. It is closer to operating a datastore. If that is what you mean, say so
  and say what feeds it.

### graph-database

The profile, all parts together: the traversals that matter to the business are deep or of unknown depth;
they run online with a latency budget and many at once; the edge set is too large for a copy per process;
it changes continuously and readers need recent data; and the SQL in place is measured failing at that
depth, with the cheaper remedies tried and recorded, or not shown to hold by any measurement or arithmetic.

When the whole profile is present, recommend it even to an owner who hoped for a tuning answer, and put the
cost on the table: a second stateful system to back up, upgrade and be paged for, a feed from the system of
record that can drift, and a new query language. An embedded engine removes the server but not the second
copy of the data or the load step (`engines.md`).

Caveats:

- It does not remove hubs or a giant connected component. Depth limits and hub caps are still needed, and
  the write-up should carry over the ones the team already found.
- "Unproven here" is not a reason to reject it once the cheaper rungs do not hold; it is a reason to name
  the trial that gates the spend: the full edge set, the real query mix, the real write rate.
- Sunk work, a decision already recorded and an offer that expires are not part of the profile.

## Reading the evidence

- **A failure count needs a total.** A slow-query log or an error log lists the calls that went wrong. The
  same count can be most of the workload or a handful of odd inputs. Look for the setting that defines what
  gets logged and for a per-statement call count; if neither total nor rate exists, the honest answer is
  `need-more-information`, and the request is for that total.
- **Means hide the shape.** A mean latency over all calls hides the split by depth; a mean that includes
  calls cancelled at the timeout is capped by the timeout. Prefer a breakdown by depth and the share
  cancelled.
- **A per-row file is not a total.** Daily or per-route rows have to be summed before they say what share of
  calls is deep.
- **Dates.** Order the documents and the measurements in time. A decision record written before launch is a
  forecast; a usage export after launch is the result.
- **History is evidence.** Each remedy the team tried, with what happened, closes or keeps open a rung. Look
  in decision records, migrations that drop things, changelogs and ticket threads.
- **Missing versus untested.** A fact about the workload as it is (what the query does, how much data, how
  many calls, what share fail, what depth is needed) can be missing, and then you ask for it. How a
  not-yet-built option or an unrun rewrite would perform is always unknown, and so is any number that only
  serves to predict it (how much of the current cost a rewrite would remove). That is what a trial is for;
  it does not hold up the decision and it does not keep a failing rung open.

## The sums

Identities, not thresholds. Show the inputs and where each came from.

- edges = nodes times average fan-out (use the finer-grained node count when the requirement is finer-grained).
- memory for an in-memory graph = edges times measured bytes per edge; needed in every process that loads it.
- rows a walk can touch by depth d grows roughly as fan-out to the power d until it runs out of distinct
  nodes; use the tail fan-out, not the median, for the calls that time out.
- rows a route-per-row query returns = number of routes, which can be far larger than the number of distinct
  nodes; the ratio of the two, read from a plan or a count, is the waste a rewrite removes.
- statements running at once is about calls per second times seconds each one takes.
- failure rate = failures divided by total calls over the same period. No total, no rate.
- load time at full size is about sample load time times (full edges divided by sample edges), to compare
  with the freshness required. Treat it as a first estimate and say it is an extrapolation.

## What would change the decision

Write conditions that someone can observe later, in this workload's own measures: the share of calls beyond
a given depth, the cancelled share at the timeout the team already set, the edge count against the memory
limit already configured, a feature returning or a cap being lifted. If a limit is needed and the repository
sets none, say whose call it is.
