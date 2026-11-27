# Evals for roast-my-graph

> **Where the cases are.** This file is the whole record for the skill. The case sets it names live in the companion
> repository `erdostack/bench`, with their graders: `standards/` (six cases, see `evals/STANDARDS.md`) and
> `dev/` (190 cases). That repository also carries this file. The skills repository keeps the reports in
> `evals/results/`.

Status (2026-11-27): version 3 of the skill (`328dae67cdaa`) passed its third gate, on 120 cases written from the register
(29 won, 8 lost, 83 tied, p = 0.0008 against 0.0167). The gain is restraint on sound designs, not detection of more
defects. Two earlier gates did not pass. What follows is the record in the order it was written, starting before the
skill existed.

The skill does not exist yet. This file, the cases and the graders were written first (2026-11-23); the baseline
runs next; the skill is drafted after that by someone who sees `dev/` and never `heldout/`.

Second round, same day: the first no-skill baseline on the dev set passed 9 of 12 runs, and all three failures
were failures of restraint (a serious finding on a sound schema, a sound table rated as the main problem, the
author insulted), not of detection. The sets were extended from 6 + 12 to 10 + 20 cases to measure that; see
the changelog.

## Correctness claim

Given a schema, model or query file (Neo4j-style Cypher, LadybugDB DDL, SQL that stores a graph, or a
NetworkX/Python model) and a request to roast or review it, the result:

1. **Finds the planted, harmful defects and names the element each is about** (label, table, column,
   relationship type, function or query). Checked per planted defect by a script (`finds-<id>`: a finding in
   `findings.json` names the element) and a judge item (`explains-<id>`: the diagnosis is the right one).
2. **Gives severities that are not absurd.** A planted defect that returns wrong results, corrupts data or takes
   an interactive path down is rated high or critical; any other planted defect at least medium, with one
   exception that only has to be found (`finds-<id>`; see Severity floors). An element that looks odd but is
   right for the workload stated in the README or a comment, and an issue that is only cosmetic (naming), is
   not rated critical or high (`not-overrated-<id>`). Script.
3. **Proposes a fix that is concrete and valid for that engine.** Part of the same judge item (`explains-<id>`),
   whose question says which fixes do not count (an index on the string, a hint, raising the recursion limit,
   keeping the join node). Where the engine runs here, a script settles it first: in the SQLite index case the
   proposed `CREATE INDEX` is executed against the schema and the query plan is inspected.
4. **Invents nothing.** Every element named in `findings.json` exists in the input files
   (`no-invented-elements`). Script.
5. **Says so when the input is sound.** On a clean input no finding is rated critical or high
   (`no-critical-or-high`); an empty list is a pass. Script. In the six clean cases added in the second round
   the review must also tell the user the design is sound (`says-sound-<id>`): each of those prompts asks for
   a verdict ("is he right?", "what actually has to change?", "anything to fix first?"), so the answer is part
   of what was requested. Judge item.
6. **Contains no jokes when asked for a serious or professional review** (`no-jokes`). Judge item, only in
   the five cases that ask; two of them ask without the words "serious" or "jokes".
7. **Never insults the author** (`no-insults`). Judge item, only in the five cases whose prompt invites it.

Not graded: whether the jokes are funny, the voice, the order of findings, extra true findings beyond the planted
ones, and wording of any kind. No assertion passes or fails on vocabulary.

Contract (reported separately, never counts toward lift): the roast is at `docs/graph/ROAST.md`, it names the
element and severity of every finding in `findings.json`, and its last line is
`Roasted with erdostack: npx skills add usergraphtheory/erdostack`.

Every prompt ends with one request a user could plausibly make: also save the findings to `findings.json` in the
repo root as a list of `{element, severity, problem, fix}`. Both arms get it. All scripted substance checks read
that file and nothing else, so a baseline that answers well in its own format can pass them.

## Open questions

- **Neo4j facts were not read against the manual.** Neither authoring session could open pages. Four
  long-stable definitions (unbounded `*`, disconnected patterns multiply rows, a directed pattern matches only
  the stored direction, a lookup on an unindexed property examines every node with the label) were accepted
  as fact by the maintainer on 2026-11-23 and are graded on. `host_by_serial` in the held-out direction case
  stays ungraded all the same: adding a second planted defect to an existing case would make it stricter, and
  the unindexed-lookup fact now has its own case.
- **MERGE semantics are not on the accepted list.** `dev/cypher-loader-merges-on-a-changing-property...`
  rests on one more long-stable definition: MERGE matches the whole pattern, properties included, or creates
  all of it. It is recorded in SOURCES.md as not read. If the maintainer does not accept it, that case comes
  out; no held-out gold depends on it (the held-out constraint case passes on the accepted scan fact alone).
- **Power.** The ship gate needs at least six held-out cases where the arms disagree, all in the skill's favour
  (sign test). With 20 held-out cases the baseline has to fail, at least some of the time, on six or more. If
  it does not, the honest verdict is "no detectable difference"; add harder held-out cases then, do not loosen
  the gate.
- **A skill that always says "sound" is not ruled out by the restraint cases alone.** Six of the 20 held-out
  cases are clean. Such a skill passes those and fails the other 14, so the overall bar catches it, but read
  the restraint and detection results side by side, not only the total.
- **`says-sound` is only asked where the prompt requests a verdict.** The three clean cases from the first
  round have no such item and were left as they were. A review that hedges on them ("could go either way")
  passes; the new cases are where that is measured.
- **A finding about the user's plan can look like a finding about the files.** In four clean cases the user
  proposes a change that would do harm. A review could record "this refactor would orphan the history" as a
  critical finding and be right. Those four prompts therefore ask for "one object per problem you find in the
  files as they are now". If a run still fails `no-critical-or-high` only because of a correctly argued
  finding about the plan, read it before counting it.
- **Decoy check is lenient by construction.** It only fires when the decoy is named in a finding's `element`.
  A review that condemns the decoy under a vague element ("the schema") escapes the script. Watch for this in
  transcripts; if it happens, add a judge item to the four decoy cases. (The six second-round clean cases are
  covered: their `says-sound` item fails such a review.)
- **Invention check false alarms.** The check separates names from ordinary words with a word list. An honest
  finding whose element is one or two unusual plain words that appear nowhere in the input could be flagged. If
  a baseline or skill run fails only on `no-invented-elements`, read the evidence before trusting it, and extend
  the list (with a unit test) if it was a false alarm.
- **Invention check is an existence check.** It catches a criticised name that is not in the input. It does not
  catch a false claim about a real element (for example "no index on X" when one exists). One held-out case
  now sets that trap (the index is in a later migration file) and grades it through `no-critical-or-high` and
  a `says-sound` item; a false claim rated medium is caught only by the judge.
- **`--serious` as a flag** appears in one held-out prompt, always with the plain-words meaning beside it so the
  baseline can comply. Whether the skill honours the bare flag with no explanation is not tested.
- **"No footer" requests** are not tested. The footer is only checked as present (contract).
- **Fix validity for Cypher engines is judged, not executed.** There is no Neo4j or LadybugDB on the eval
  machine. If the harness gains LadybugDB in-process, the two LadybugDB defect cases can execute the proposed
  DDL the way the SQLite index case does.
- **Judge agreement on the new items is unmeasured.** 132 labelled calibration items ship with the cases, 58 of
  them new in the second round, including all 19 for the new `says-sound` question type. Run the calibration
  again before any verdict on a second-round case counts.
- **Three judge items can be settled by a script** (a proposed CREATE INDEX or WITH RECURSIVE statement is run
  against the schema or a fresh sample database). They can only be settled as passed. A baseline that explains
  the fix in words goes to the judge; an answer that ships the statement does not. Both routes ask the same
  thing, but watch for a difference in pass rate between them.

## Case sets

| Set | Cases | Purpose |
|---|---|---|
| execution-dev | 10 | iterate against; the skill author sees these |
| execution-heldout | 20 | ship decision only; same claim, different domains, storage and file layouts |
| trigger | 10 positive / 10 negative | description; negatives are near misses (other erdostack skills' requests, roasts of non-graph things) |

### dev

| Case | Input | Planted defect(s) | Trap | Judge items |
|---|---|---|---|---|
| cypher-schema-enrollment-node-and-prerequisites-in-a-string | Neo4j schema, load and query files | join row kept as a node; list of codes in a string property | prompt invites mocking a teammate | 3 |
| cypher-queries-unbounded-follow-walk-and-row-multiplying-match | Neo4j query file, 7 queries | unbounded variable-length walk on 1.9B edges; disconnected MATCH that multiplies rows | defects sit among ordinary queries; one returns plausible numbers | 2 |
| sqlite-dependency-table-reverse-lookup-has-no-index | SQLite DDL, queries, generated database | edge table searchable in one direction only | table has a primary key and the sample is fast; serious review requested | 2 (one settled by script when a CREATE INDEX is given) |
| networkx-route-finder-ignores-minutes-and-stops-kept-as-json-text | NetworkX package with tests and data | hand-written "fastest route" that is a breadth-first search; node attributes in one JSON string | bundled tests pass; an unweighted library call keeps the bug | 2 |
| ladybug-sound-citation-schema-has-nothing-serious | LadybugDB DDL | none (clean) | asked to roast something sound; Neo4j reflexes ("no indexes", "rel table needs a key") | 0 |
| sql-closure-table-is-right-for-the-workload-id-list-column-is-not | PostgreSQL-style DDL and queries | delimited id list in a text column | decoy: a closure table that looks redundant and is right for the workload | 1 |
| cypher-visit-node-carries-its-own-relationships-and-should-stay *(round 2)* | Neo4j model doc, schema, queries | none (clean) | a tech lead calls the in-between node a join table; prescriptions and follow-ups attach to it | 1 |
| cypher-loader-merges-on-a-changing-property-beside-naming-quirks *(round 2)* | Neo4j schema, loader, queries | MERGE on a property that changes, duplicating nodes nightly | severity: two naming quirks sit next to it and catch the eye first | 1 |
| sqlite-territory-walks-have-no-depth-guard-and-the-schema-makes-one-unnecessary *(round 2)* | SQLite DDL, statements, generated database | none (clean) | a lint rule and a reviewer demand depth guards; constraints bound the tree at six levels | 1 |
| networkx-blast-radius-walks-toward-sources-against-the-loader *(round 2)* | NetworkX package, tests, CSVs | traversal direction in one function contradicts the loader | truth is in the other file; bundled test passes; "keep it professional" without the word serious | 2 |

### heldout

| Case | Input | Planted defect(s) | Trap | Judge items |
|---|---|---|---|---|
| ladybug-crew-assignment-as-node-table-and-voyage-linked-by-code-columns | LadybugDB DDL and queries | join table kept as a node table; foreign-key columns with no relationship tables | fixes that keep the node table and add indexes | 2 |
| cypher-query-arrow-points-against-the-ingest-direction | Neo4j queries, ingest, model doc | relationship direction in one query contradicts the rest of the repo | truth is in other files; a neighbouring correct query is easy to blame | 1 |
| cypher-recommendation-expands-every-customer-in-the-country | Neo4j queries | traversal through a 9-node hub with millions of relationships | "anchor on the hub" is not a fix; prompt invites mocking a contractor | 2 |
| sqlite-folder-tree-kept-as-slash-separated-text | SQLite DDL, statements, generated database | hierarchy as delimited path text, giving wrong results | looks like a legitimate pattern until run; serious review requested with `--serious` | 2 |
| sqlite-bom-explosion-stops-after-three-levels-of-joins | SQLite DDL, reports, generated database | traversal hand-unrolled to a fixed depth | query runs and looks tidy; schema is sound | 1 |
| networkx-page-scores-computed-by-hand-and-losing-rank | NetworkX package and data | hand-written PageRank, quadratic and leaking rank | prompt invites mocking an intern | 2 |
| networkx-timetable-search-is-justified-recursive-reachability-is-not | NetworkX package, generated timetable | recursive traversal that hits the recursion limit | decoy: a hand-written time-dependent search the library cannot replace | 1 |
| sqlite-sound-threaded-forum-has-nothing-serious | SQLite DDL, statements, generated database | none (clean) | user is "sure it's terrible"; adjacency list and constrained denormalisation look roastable | 0 |
| networkx-sound-build-graph-has-nothing-serious | NetworkX package with tests | none (clean) | "go wild"; one justified hand-written loop | 0 |
| cypher-credit-node-is-justified-catch-all-relationship-is-not | Neo4j schema, load and query files | one relationship type with a kind property for five meanings | decoy: an intermediate node that looks like a join table and is required | 1 |
| ladybug-query-uses-a-relationship-the-schema-does-not-define | LadybugDB DDL and queries | query names a relationship table that does not exist | sits among five correct queries; "add the table" and "rename the schema" are wrong fixes; serious review requested | 2 |
| neo4j-client-walks-referral-tree-one-query-per-member | Python driver code with embedded Cypher | traversal done in application code, one query per node | every individual query is fine | 1 |
| cypher-listing-city-slug-is-a-deliberate-copy-for-the-search-index *(round 2)* | Neo4j schema, writes, reads | none (clean) | a property repeats what a relationship says; README gives the read pattern and why it cannot drift | 1 |
| sql-membership-table-keeps-its-own-id-because-memberships-have-a-life *(round 2)* | PostgreSQL-style DDL and queries | none (clean) | the user plans to flatten a join table that has its own lifecycle and is referenced by id | 1 |
| networkx-sound-network-audit-and-a-request-to-tear-the-coworker-apart *(round 2)* | NetworkX package, tests, CSVs | none (clean) | "tear him apart" over code that is fine | 2 |
| sqlite-substitute-walk-never-ends-on-a-swap-loop-beside-naming-quirks *(round 2)* | SQLite DDL, statements, generated database | recursive walk that never ends on loops the sample data contains | severity: naming quirks beside it; the walk reads like a textbook query | 1 (settled by script when a working statement is given) |
| cypher-loader-merges-on-a-property-the-schema-never-constrains *(round 2)* | Neo4j schema, loader, queries | the constraint is on a different property from the one every MERGE and MATCH uses | needs both files; "be brutal about them" (a junior) | 2 |
| sqlite-block-table-keys-cannot-serve-the-lookup-the-delivery-code-runs *(round 2)* | SQLite migrations, Python, generated database | key and index both lead with the wrong column for the hot lookup | needs the migration and the Python; plan says "USING COVERING INDEX"; "dry and factual" for a client | 2 (one settled by script when a CREATE INDEX is given) |
| cypher-large-grid-repo-one-unbounded-walk-on-a-meshed-network-among-oddities *(round 2)* | Neo4j, 9 files, 230 lines, 26 statements | unbounded walk over a meshed network on an interactive screen | a second unbounded pattern that is fine (four-level tree), a leftover property, odd timestamps | 1 |
| sqlite-link-table-reverse-lookup-is-indexed-in-a-later-migration *(round 2)* | SQLite migrations, statements, generated database | none (clean) | the user is sure the reverse lookup has no index; it is created one migration later | 1 |

Coverage (dev + held-out): clean input 3 + 6; decoy next to a real defect 1 + 3; cosmetic issue next to a
dangerous one 1 + 2; defect that needs two files 1 + 4; serious or professional tone 2 + 3; insult temptation
1 + 4. "Restraint cases" below means the cases with a clean, decoy or cosmetic check: 5 dev, 10 held-out.
Storage in held-out: Neo4j 7 (one of them Cypher embedded in Python), LadybugDB 2, SQL 7 (6 SQLite, 1
PostgreSQL-style), NetworkX 4.

Measured baseline on the first-round dev set (2026-11-23, no skill, one run each on two models, reported by the
maintainer): 9 of 12 runs passed substance. The three failures: a high or critical finding on the clean
LadybugDB schema; the closure table rated as a serious problem; the teammate insulted and the enrollment join
node not explained. Every plain planted defect was found.

Expected baseline on the second-round cases (a guess, to be replaced by the measured run): the planted
defects will mostly be found again, including the cross-file ones. Failures are most likely where the textbook
rule and the workload disagree and someone in the prompt has already taken the textbook side (the Visit node,
the lint rule, the planned membership refactor, the index the user is sure is missing), on the two cosmetic
items when a review rates everything at one volume, on the second unbounded pattern in the large repo, and on
the two new prompts that invite going after a person.

## Thresholds

Set before any with-skill run. Defaults from the eval authors' brief unless marked.

| Metric | Bar | Why |
|---|---|---|
| Held-out lift (substance), paired by case over two models | sign test p < 0.05 in the skill's favour | no detectable lift means the skill does not earn its context cost |
| Held-out substance pass rate with skill | observed >= 75% and 95% lower bound >= 55% | output is advisory and reviewed by the user, but must be right most of the time |
| Regressions | no case the baseline always passes and the skill always fails | a skill must not break what already works |
| Restraint cases with skill (held-out: the 10 cases with a clean, decoy or cosmetic check) | not below the baseline's count on the same 10 | **added; widened from 4 cases to 10 on 2026-11-23 (second round), before any with-skill run.** A roast skill's characteristic way to do harm is to find something every time. A skill that gains on defect cases by losing here is a net loss for trust, and the overall rate could hide it |
| Judge agreement with the shipped labels | >= 90% overall and >= 85% on the items labelled false, before any judge verdict counts | **added.** 41 substance assertions are judge items; a judge that says yes to jargon would hand the skill unearned wins |
| Contract assertions with skill | >= 90% | downstream skills parse these files |
| Tokens and time vs baseline (median) | <= 1.5x tokens, <= 2x time | a correct but expensive skill does not get used |
| Skill size | description <= 600 chars, SKILL.md body <= 150 lines | the description is always in context |
| Trigger recall / precision (simulated) | >= 80% / >= 80% | missed triggers hide the skill; false triggers waste context |

Severity floors (claim 2) are part of the cases, not thresholds: `min_severity` in each check.py. Of the 25
planted defects, 13 have a floor of `high` (wrong results, corrupted data, or an interactive path that cannot
finish at the stated scale), 11 have `medium`, and one has `low`, meaning it only has to be found (the JSON
`blob` attribute in the dev NetworkX case; see the changelog). Changing one is a change to the eval and goes
in the changelog with a reason.

## Graders

All graders are `check.py` per case, each a small gold SPEC over `lib/roastcheck.py` (unit tests in
`lib/test_roastcheck.py`, 26 tests). Offline, deterministic, standard library only.

**Scripts (101 substance assertions across the 30 cases, plus 90 contract assertions):**

- `findings-json-usable`: the file parses; every finding has element, severity (one of four; common synonyms
  such as "moderate" are mapped), problem, fix.
- `no-invented-elements`: for each finding's element, at least one specific word exists in the input files; in
  `Owner.member` the member exists when the owner does; a `:Label` or `[:TYPE]` exists. Vague elements ("overall
  schema", "error handling", a plain-word description of something absent) are let through: vague is not
  invented. The evidence field quotes the offending name, so a false alarm is visible in the report.
- `finds-<id>`: some finding names the planted element in its element or problem text, rated at or above the
  floor. Lenient on purpose; the judge item decides whether the diagnosis is right.
- `not-overrated-<id>`: no finding whose element names the decoy, or the cosmetic issue, is critical or high.
  The SPEC keeps `decoys` and `cosmetic` apart only so the report says which kind of restraint failed.
- `no-critical-or-high`: clean cases.
- Three execution checks, each of which can only settle a judge item as passed (otherwise the judge decides):
  in the two SQLite index cases a `CREATE INDEX` statement found anywhere in the output is run against the
  schema in memory (single statement, progress-handler timeout) and the plan for the lookup in question must
  become an index search; in the substitute-walk case a `WITH RECURSIVE` statement from the output is run
  read-only against a freshly built sample database, with every parameter bound to an ingredient that sits on
  a loop, and must finish and return exactly the reachable ingredients.

**Judge items (41: 15 dev, 26 held-out), `passed: null` with a yes/no question:**

- `explains-<id>`, one per planted defect (25). Each question names the element, states the diagnosis and the
  fix that counts, and ends with the fix that does not.
- `says-sound-<id>` (6, second round only): does the review tell the user that the sound design is sound?
  Each question names the element or the verdict asked for, and ends with what does not count (endorsing the
  change, calling for a fix, leaving it open).
- `no-jokes` (5) and `no-insults` (5), each with one fixed question.

The judge never sees the run directory. check.py writes three files under `<run_dir>/judge/` (closing message,
findings.json, review documents) with the footer line, the skill's name and the `docs/graph/ROAST.md` path
removed, so the two arms look alike. A review the agent wrote anywhere in its working directory is included.

**Calibration.** Every judge question has labelled examples in the selfcheck variants (`JUDGE_LABELS.json`):
132 items, 77 labelled true and 55 false. Each `says-sound` question has a plain-words answer labelled true and
two labelled false: one that condemns the sound element outright, and one in textbook vocabulary that rates
it medium and leaves the decision open or asks for the change anyway. The `good` variants are written in plain words without the
anti-patterns' names and are labelled true; each defect case has a `bad-jargon-*` variant that uses the names,
points at the right element, rates it plausibly and proposes a fix that misses the point, labelled false. Tone
and insult items have a serious-but-joking variant and an insulting variant labelled false. Agreement so far:
not yet measured (see Open questions).

**Checking the eval.** `python3 evals/harness/erdo_eval.py selftest --skill roast-my-graph` runs every grader on
its `good` variant and on 77 `bad-*` variants (107 in all); each scripted bad variant must fail the assertions
listed in its `EXPECT_FAIL`.

## Running it

    python3 evals/harness/erdo_eval.py selftest --skill roast-my-graph
    python3 -m unittest discover -s evals/roast-my-graph/lib -p 'test_*.py'
    python3 evals/harness/erdo_eval.py prepare --root runs --skill roast-my-graph --set dev --arm baseline --model <id> --runs 3

Smoke tier (every edit to the skill): dev set, script assertions only, 1 run. Full tier (before shipping, on a
model change, or when SOURCES.md is re-verified): both sets, 3 runs per case per arm on two models, judge items,
cost.

## Gate protocol

Set on 2026-11-23 by the maintainer, before any with-skill run on the held-out set. It replaces the default
"paired by case over two models" wording above where they differ.

- **Runs.** Every held-out case is run with no skill (baseline) and with the skill installed, on two models
  (Claude Haiku and Claude Sonnet, the versions current on the run date), one run per model per arm. Both arms
  get the identical prompt and run in the same session. Cases are run four or five to an agent session; the
  grouping is the same for both arms, so each case has the same batch-mates with and without the skill.
- **Unit of analysis.** The case. A case's score in an arm is the fraction of its runs that pass every
  substance assertion. The skill "wins" a case if its score is higher, the baseline if lower, otherwise a tie.
  A two-sided exact sign test is applied to wins against losses. Contract assertions never count.
- **Two looks.** If the first pass does not reach the bar, the whole pass is repeated once (a second run per
  model per arm) and the test is applied to the pooled runs. No third pass. To keep the overall false-positive
  rate at 5% across two looks, the bar at each look is p < 0.025.
- **Fresh baseline.** Baseline runs made earlier to judge how hard the cases are do not count. The baseline
  used for the comparison is run alongside the with-skill runs.
- **Other bars** (pass rate, regressions, cost) are as in the thresholds table.
- **What a pass does not show.** The cases execute SQL on SQLite and Python on NetworkX and analyse Cypher
  statically; no Cypher is executed against Neo4j or LadybugDB. Only two Claude models are tested. The skill
  author worked from the dev set and never opened held-out cases, but held-out case names are visible in this
  file's tables.

## Results log

| Date | Skill version | Model | Set | Passed / runs | 95% interval | Baseline | Tokens | Time |
|---|---|---|---|---|---|---|---|---|
| 2026-11-23 | 8be30539ba84 | Haiku + Sonnet | first held-out set (now in dev), pass 1 | 32 / 40 | 65% to 90% | 27 / 40 (52% to 80%); paired by case 7 skill / 2 baseline / 11 tied, p = 0.1797 | 30754 vs 23764 | 69.5 s vs 60.4 s |
| 2026-11-23 | 8be30539ba84 | Haiku + Sonnet | first held-out set (now in dev), both passes pooled (second look) | 62 / 80 | 67% to 85% | 54 / 80 (57% to 77%); paired by case 8 skill / 2 baseline / 10 tied, p = 0.1094 | 30754 vs 23934 | 64.1 s vs 55.2 s |
| 2026-11-23 | 861797c1f1d1 | Haiku + Sonnet | second held-out set (40 cases), round-2 gate, one look | 73 / 80 | 83% to 96% | 65 / 80 (71% to 88%); paired by case 10 skill / 2 baseline / 28 tied, p = 0.0386 | 30096 vs 23190 | 78.2 s vs 54.5 s |
First gate verdict: NOT ENOUGH EVIDENCE at either look (bar p < 0.025). Reports: `evals/results/roast-my-graph/`.

## Gate protocol, round 2

Set on 2026-11-23 by the maintainer, after the first gate and before any run on the new held-out set.

- **Why a second round.** The first gate did not reach its bar (see the results log). Pooled over two passes the skill was ahead on 8 cases and behind on 2 of 20 (p = 0.11): ahead, not shown. Haiku with the skill still over-rated sound designs, and one case got worse with the skill. Under the
  rules of this repo the cases of a used held-out set move to `dev/`, a new held-out set is written, and the
  skill is gated again on cases nothing has been tuned against.
- **The new set.** 40 cases, written after the first gate by authors who had read this file, the old cases
  and the first-gate report, and had not read the skill. They were asked for real problems of the kinds an
  unaided agent got wrong in the first gate, with about a third restraint cases, and told not to repeat kinds
  every arm passed. The set is therefore harder than a random sample of graph work; the pass rates it yields
  describe hard cases, not everyday ones.
- **Skill under test.** Revised after the first gate from the old held-out failures (severity gate before critical/high, relationships stored only as text are a finding, verdict wording). The revision was made from transcripts and has not been run on dev.
- **Runs.** As in the first gate: no skill and skill, Claude Haiku and Claude Sonnet, one run per model per
  arm, five cases to an agent session with the same grouping in both arms, baseline run alongside.
- **Test.** Same unit (the case) and the same two-sided exact sign test on wins against losses. **One look,
  bar p < 0.05. No repeat pass.** The first gate showed that a repeat pass adds runs but not cases, and the
  evidence comes from cases, so the runs are spent on twice as many cases instead of on a second look.
- **Other bars** are unchanged.
- **Multiplicity, stated plainly.** This is the second gate this skill has faced. Each gate is a separate
  5% test on fresh cases; a reader who wants the family-wise rate across both should halve the bar.

## Round-2 gate result (2026-11-23)

Report: `evals/results/roast-my-graph/2026-11-23-heldout-round2-gate.md`. Skill version 861797c1f1d1 (the revision made after the first gate).

| Threshold | Bar | Result | Met |
|---|---|---|---|
| Lift, paired by case | sign test p < 0.05, one look | 10 skill / 2 baseline / 28 tied, p = 0.0386 | yes |
| Pass rate with skill | observed >= 75%, lower bound >= 55% | 73 / 80 (83% to 96%) | yes |
| Regressions | no case the baseline always passes and the skill always fails | 1 case | **no** |
| Contract with skill | >= 90% | 80 / 80 | yes |
| Tokens, time vs baseline (median) | <= 1.5x, <= 2x | 1.30x, 1.43x | yes |

**Verdict: the improvement is shown; one bar is missed, and it is recorded here as a known failure rather than waived.**

- The whole difference is on the smaller model. Haiku: 34 of 40 with the skill, 26 of 40 without. Sonnet: 39 of 40 in both arms. On Sonnet this set shows no difference.
- What the skill changes is restraint: 9 of the 10 cases it wins are sound or justified designs that the bare Haiku rated critical or high.
- **Known failure.** `ladybug-checkout-price-takes-any-row-of-a-price-history-it-never-closes-off`: with the skill, both models found the defect (a checkout query that can return a superseded price), explained it and proposed the right fix, and both rated it medium; the bare model rated it critical on both. The severity questions added after the first gate treat "which row comes back is not guaranteed" as uncertain damage. For a result that decides what a customer is charged, that is the wrong call. The same over-caution lowered one more rating on Haiku (`neo4j-seat-hold-checks-in-one-transaction-and-creates-in-another`).
- Not fixed in this version on purpose: a skill changed after its gate is an ungated skill. The fix (nondeterministic or stale results on a path the repo shows carries money, access or safety count as certain damage) belongs in the next revision, gated on a fresh set.
- This is the second gate the skill has faced; halve the bar to read both as one family, and p = 0.0386 no longer clears it.

## Gate protocol, round 3

Set on 2026-11-23 by the maintainer, after the round-2 result above and before any run on a third held-out set.

- **Why a third round.** Round 2 met the lift bar and missed the regression bar, and the skill was kept in the
  launch set with the miss written up as a known failure. That was the wrong call by this repo's own rule: a
  missed bar means a new set, not a footnote. The 40 round-2 cases are now in `dev/` (70 dev cases).
- **Skill under test.** Version 3: version 2 with the severity questions revised so that a result which is
  nondeterministic or stale on a path the files show carries money, access, safety or what a customer is
  told counts as certain damage. Before the gate it is run on the 40 round-2 cases on both models. It is
  frozen when it passes both known-failure cases on both models and its total on those 40 is not below
  version 2's 73 of 80; a case-and-model pair that version 2 passed and version 3 fails is run twice more
  and counts as lost only if it fails again both times.
- **Dev check, as run (recorded before any round-3 run).** Version 3 changes one sentence of the third
  severity question. On the 40 round-2 cases it passed 76 of 80 runs (version 2: 73), including both
  known-failure cases on both models. One pair that version 2 passed failed (`networkx-dag-check-lists-every-cycle-to-report-the-first-one`
  on Haiku, rated medium); run twice more it passed both times. Frozen as version 3.
- **The set.** 120 fresh cases by six authors who have not read the skill. Every case stages a problem from
  `evals/REAL_PROBLEMS.md` and names it in its `case.yaml`; about a third are restraint cases built from that
  register's "also fine when" column. NetworkX cases that need data use the real networks that ship with the
  library (RP-23) where the problem allows. The repositories themselves are still generated.
- **Runs.** As before: no skill and skill, Claude Haiku and Claude Sonnet, one run per model per arm, five
  cases to a session, same grouping in both arms.
- **Judge.** The judge's agreement with the shipped labels of the new cases is measured before any verdict
  counts (bar unchanged: 90% overall, 85% on items labelled false).
- **Audit, part of the protocol this time.** `query-review`'s fifth gate showed that script graders fail
  correct answers written in a form their author did not expect. So after grading and judging, every failing
  run in both arms is re-read without its arm; each disputed script grade goes to a repairer who may disagree,
  and a repaired grader must keep every existing known-bad variant failing and gain a known-good variant for
  the form it missed. Judge items, and grades the readers call unsure, stay as they are. All runs are then
  graded again.
- **Test and bars.** Same unit (the case) and two-sided exact sign test, one look. **Bar: p < 0.0167**, which is
  0.05 divided by the three gates this skill has faced. The skill passes only if that bar holds under both
  gradings (as first graded and audited) and the regression, pass-rate, restraint, contract and cost bars hold
  under the audited grading.
- **Outside evidence (added 2026-11-23, before any run on this set).** `evals/PROVENANCE.md` counts a gain as
  shown on real problems only on cases whose register entry was read, reproduced or ships as real data. 109
  of the 120 cases qualify; 11 rest only on RP-08, RP-17 or RP-24, which were not. The lift bar must hold on
  the 109 as well as on the 120, under both gradings. This only tightens the bar above.
- **If it misses**, `roast-my-graph` leaves the launch set until a later version passes a fresh gate.

## Round-3 gate result (2026-11-24)

Skill version 3 (`328dae67cdaa`), 120 cases, Haiku and Sonnet, one run per model per arm: 480 runs. Full reports:
`evals/results/roast-my-graph/2026-11-24-heldout-round3-gate.md` (as first graded) and
`...-round3-gate-audited.md`.

**Judge agreement, measured before any verdict was applied.** 240 labelled items (120 labelled true, 120
labelled false, a seeded sample of the 713 available) were mixed unmarked into the judge's batches. The judge
agreed on 238 of 240, and on 120 of 120 labelled false. Both bars met.

**As first graded.** Skill 223 of 240 (89% to 96%), baseline 189 of 240. By case: 30 won, 7 lost, 83 tied,
**p = 0.0002**. On the 109 cases with outside evidence: 27 won, 5 lost, 77 tied, p = 0.0001.

**Audit.** 58 runs had a failing script-graded assertion (48 baseline, 10 skill). Reviewers who were not told
the arm, and were not shown `docs/graph/ROAST.md`, called 56 grades right and 2 wrong. Both wrong grades were
`no-invented-elements` on baseline runs: the checker did not read `.conf` files and did not know about files a
case's `setup.py` generates, so it called a real setting and a real input file invented. Repaired in
`lib/roastcheck.py`, with a known-good and a near-miss variant in each case; self-check 731 variants, 0
failures. Judge verdicts were left as given.

**Audited.** Skill 223 of 240, baseline 191 of 240. By case: 29 won, 8 lost, 83 tied, **p = 0.0008**. On the 109
outside-evidence cases: 26 won, 6 lost, 77 tied, p = 0.0005.

| Threshold | Bar | Result | Met |
|---|---|---|---|
| Lift, all 120 cases, as graded and audited | p < 0.0167 | 0.0002 and 0.0008 | yes |
| Lift, 109 outside-evidence cases, as graded and audited | p < 0.0167 | 0.0001 and 0.0005 | yes |
| Regressions (baseline always passes, skill always fails) | 0 | 0 | yes |
| Pass rate with skill | >= 75%, lower bound >= 55% | 93% (89% to 96%) | yes |
| Restraint cases with skill (42 clean cases, 84 runs) | not below baseline | 76 against 43 | yes |
| Contract | >= 90% of runs | 237 of 240 | yes |
| Tokens, time against baseline (median) | <= 1.5x, <= 2x | 1.32x, 1.54x | yes |
| Judge agreement | >= 90%, >= 85% on labelled false | 238 of 240, 120 of 120 | yes |

**Verdict: SHIP version 3.**

What the result is and is not:

- The gain is restraint. On the 42 cases where the design is sound, the skill passed 76 of 84 runs and the
  bare models 43 of 84. On the 78 cases with a planted defect the two are level: 147 of 156 with the skill,
  148 of 156 without. The skill does not find more defects than a bare model; it stops calling sound designs
  broken.
- By model, as graded: Sonnet 20 won, 0 lost. Haiku 22 won, 8 lost.
- Known failures (the 8 cases lost under the audited grading, all on Haiku): `neo4j-dock-availability-queries-beside-the-compose-file`,
  `neo4j-timetable-queries-tested-on-compose-and-deployed-by-helm`, `neo4j-sensor-heartbeat-consumers-and-fleet-dashboard`,
  `neo4j-telemetry-retention-job-and-the-meter-dashboards`, `neo4j-trail-reports-migration-runner-and-a-segment-backfill`,
  `networkx-florentine-worksheet-lists-every-marriage-route`, `sqlite-package-registry-db-layer-and-a-lint-report-on-its-foreign-keys`,
  `sqlite-service-catalogue-connection-helper-and-decommission-command`. Five of the eight are Neo4j cases
  where the defect depends on the server version or on write behaviour, and the skill's caution turns a
  correct finding into a hedged one.
- Not tested: a live Neo4j or LadybugDB server (Cypher findings were graded statically), any model other than
  Haiku and Sonnet, triggering (not re-measured for version 3), repositories larger than these fixtures.
- One Haiku session of the 96 scheduled a reminder task against its instructions. Its five runs finished and
  were graded like the rest.

The 120 cases are now in `dev/` (190 dev cases). `heldout/` is empty.

## Standards track (2026-11-27)

Six cases in `standards/` stage this skill's claim on a workload from a published benchmark (`evals/STANDARDS.md` has the
sources and the protocol). They were run once, with the version frozen for release 0.1.0, as part of one test over all
five skills: 11 cases won, none lost, 19 tied of 30, p = 0.00098 against a bar of 0.05, on both gradings. Six cases carry
no verdict for one skill, so what follows is reported and not tested.

This skill, audited grades: 10 of 12 runs with the skill and 8 of 12 without (2 cases won, none lost, 4 tied). The two wins are sound designs that one unaided model each rated high. One case failed in all four runs and is a known failure for the next version: `cypher-forum-graph-nightly-import-and-message-page-queries`, a whole-pattern `MERGE` that creates a duplicate person for every new comment; with the skill both models named the load step and rated it low. 20 judge items; the judge agreed with 40 of 40 calibration labels from this set's own variants. The audit found every failing grade right.

The six cases count as seen from now on. Reports: `evals/results/roast-my-graph/2026-11-27-standards-standards-v1.md`.

## Changelog

- 2026-11-23: round 3 opened. Keeping the skill in the launch set after round 2's missed regression bar is recorded as a mistake. Round-2 cases moved to `dev/`. Protocol set before any run: 120 fresh cases tied to `evals/REAL_PROBLEMS.md`, one look, bar tightened from 0.05 to 0.0167, arm-blind audit of failing grades built in, and removal from the launch set on a miss.

- 2026-11-23: round-2 gate recorded (lift bar met at p = 0.039; regression bar missed by one case, kept as a known failure). The new held-out set of 40 cases stays in `heldout/` as the record of this gate; before the next revision it moves to `dev/` and a third set is written. No threshold was changed.
- 2026-11-23: fixture fixed in `sqlite-sound-threaded-forum-has-nothing-serious` (now a dev case). Its page query keyed on a whole-second timestamp alone, which skips posts that share a second at a page boundary: a real defect in a case whose gold says nothing is serious. All 8 gate runs, in both arms, flagged it and were failed for it. The query now keys on (created_at, id). The gate results above were computed with the old fixture and are not restated; the case was a tie either way.
- 2026-11-23: first gate recorded; it did not reach the bar. The 20 held-out cases moved to `dev/` (they have been learned from), a new held-out set is being written, and the round-2 protocol above was set before any run on it. One look at p < 0.05 on twice as many cases replaces two looks at p < 0.025, because cases, not repeat runs, carry the evidence.
- 2026-11-23: created. 6 dev and 12 held-out cases, shared grader with unit tests, 20 trigger queries, thresholds
  set before any run. Two thresholds added to the defaults (clean/decoy cases must not get worse; judge
  agreement must be shown before judge verdicts count). During authoring, before any run: the second planted
  defect of the direction case (lookup on an unindexed Neo4j property) was removed from the gold answer because
  the Neo4j indexing facts could not be read against the manual; the clean LadybugDB case was reduced to DDL only
  so that it rests solely on the one LadybugDB page that was read.
- 2026-11-23, second round, part 1: fairness audit of the 18 first-round cases, before any with-skill run.
  The question asked of every substance assertion: could a careful agent with no skill pass this from the
  prompt and the files alone?
  - Conventions. No prompt names `docs/graph/ROAST.md`, the footer line or any heading format, and the three
    assertions about them (`roast-md-path`, `roast-md-covers-findings`, `roast-md-footer`) were already
    `contract` in all 18 cases. Nothing in the judge questions depends on where or how the review is laid
    out, and the judge material has the path and footer stripped. No change needed.
  - `findings.json`. Every scripted substance check reads it. All 18 prompts state where it goes, the four
    fields, the four severity values and that `element` is an exact name from the files, so
    `findings-json-usable` and `no-invented-elements` are reachable from the prompt. No change needed.
  - **Changed:** the severity floor of `attributes-in-json-text` in
    dev/networkx-route-finder-ignores-minutes-and-stops-kept-as-json-text, from `medium` to `low`. The JSON
    `blob` attribute is the case's secondary defect; at the stated 12,000 stops it is a maintainability point
    and a careful reviewer can fairly call it low. A floor of medium failed exactly the severity discipline
    the second round sets out to measure. The defect still has to be found, and its judge item is unchanged.
    Both baseline runs of this case passed before the change, so no recorded result moves.
  - Tried and reverted: adding `Reviewed` to the names that count for `finds-undefined-relationship` in the
    held-out LadybugDB query case. It let the known-bad "rename the schema" answer pass the script (its
    problem text mentions the name), which selftest caught. The prompt asks for the query name as the
    element, so `genre_top` alone stays.
  - Looked at and left: the other eleven `medium` floors (each defect returns wrong numbers, costs a scan or
    extra hops on a stated hot path, or is what the user's complaint is about, so medium is the natural
    rating); the `--serious` flag in one held-out prompt (its meaning is spelled
    out beside it); the `no-insults` items, although three prompts ask for the opposite (declining is possible
    from the prompt alone, and the maintainer counts going after the person as a failure of substance);
    `host_by_serial`, which stays ungraded (see Open questions).
- 2026-11-23, second round, part 2: 4 dev and 8 held-out cases added (now 10 and 20); nothing removed. Reason:
  the dev baseline showed that current models find planted defects easily and fail on restraint, and a
  12-case held-out set with four restraint cases could not measure that. The new cases are harder through
  their situation, not through stricter grading:
  - precision under temptation (6, all clean): an in-between node that carries its own relationships; a
    property that deliberately repeats a relationship for a stated read pattern; unguarded recursive walks
    over a tree the schema limits to six levels; a join table with its own lifecycle; sound NetworkX code the
    user wants torn apart; a reverse-lookup index that exists in a later migration. In five of the six,
    someone in the prompt has already taken the wrong side. Graded by `no-critical-or-high` and a new judge
    item, `says-sound-<id>`;
  - severity discipline (2, plus the large case): a data-corrupting MERGE and a never-ending recursive walk,
    each beside naming quirks. Graded by a `high` floor on the dangerous one and `not-overrated-<id>` on the
    cosmetic one;
  - defects that take two files to see (3): traversal direction against the loader (NetworkX), the
    uniqueness constraint on a different property from the one every MERGE uses, an edge table whose key and
    index both lead with the wrong column for the lookup the code runs;
  - one larger input (9 files, 230 lines) with one serious defect, a sound look-alike and harmless oddities;
  - people: two new insult prompts in different words, both about a named kind of colleague, one of them
    over code that is sound; two requests for a sober review that never say "serious" or "jokes".
  Grader changes, all additive: SPEC keys `cosmetic` (graded like `decoys`) and `sound` (judge items), and
  three SQL helpers for the execution checks, with five new unit tests (26 in all). One threshold row was
  widened (restraint cases: 4 to 10 held-out cases) and the judge-item count in another updated (25 to 41).
  16 judge items were added (5 dev, 11 held-out) with 58 labelled calibration items.
  Not verified: the Neo4j MERGE semantics behind the new dev severity case (SOURCES.md); judge agreement on
  the 58 new calibration items; no model has been run on any second-round case.
- 2026-11-24: round 3 run and recorded: version 3 ships. Two `no-invented-elements` grades were repaired in `lib/roastcheck.py` after the arm-blind audit (the checker now reads `.conf`, `.cnf` and `.properties` files and files generated by `setup.py`). Judge agreement was measured on a seeded sample of 240 of the 713 labelled items. The 120 round-3 cases moved to `dev/`.
- 2026-11-27: `standards/` added (six cases staged on published benchmark workloads, written and reviewed before any run) and run once in the pooled standards test; result recorded above. A note at the top of this file says where the case sets live from release 0.1.0.
- 2026-11-27: empty fixture directories are now listed in `empty-dirs.txt`, because git does not carry them. No grade changed.
- 2026-11-27: before publication every `case.yaml` got a canary comment as its first line: it asks that the file be kept out of training data, and no grader reads it. The 504 runs behind round 3 and the standards set are published in `recorded-runs/roast-my-graph/` of the case repository: the agent's closing message, the files it wrote and every grade. All 504 can be built again from the published files and regrade as recorded, with the judge's 476 verdicts kept as given.
