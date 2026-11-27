# Evals for graph-or-not

> **Where the cases are.** This file is the whole record for the skill. The case sets it names live in the companion
> repository `erdostack/bench`, with their graders: `standards/` (six cases, see `evals/STANDARDS.md`) and
> `dev/` and `heldout/` (133 cases). That repository also carries this file. The skills repository keeps the reports in
> `evals/results/`.

Status (2026-11-27): version `a8ddcabe4a24` passed round 5, on 40 two-session cases written from the register (30 won, 1
lost, 9 tied after the audit, bar 0.0083). The claim that holds is that a decision survives into a later session; in a
single session the skill does not decide better than an unaided agent. Rounds 3 and 4 missed. What follows is the record
in the order it was written.

User-invoked. The skill decides between a graph database, an in-process library, recursive SQL, or
nothing, and writes `docs/graph/DECISION.md`. The failure it exists to fix (README failure table):
"Graph-shaped hammer. Reaches for a graph database, or refuses one, without looking at the workload."

## Correctness claim

Given a repository and a request to choose where graph-shaped work should live, a correct result
satisfies all of the following. Each is an assertion in the cases' `check.py`.

1. **It decides from the workload, not from the framing.** `docs/graph/DECISION.md` contains a line
   `Decision: <category>` and the category is in the case's set of defensible answers
   (`decision-line-parseable`, `decision-fits-workload`). The request always pushes somewhere else: a
   team that has already chosen Neo4j, an owner who wants no new database, a vendor pitch, an accepted
   ADR, a prototype that works on the easy inputs, a migration that is half done.
2. **It rests on this repository's evidence.** The write-up (DECISION.md plus the closing message) cites
   enough of the specific numbers and names that are in the fixture files and that the request did not
   mention: row counts, depth, call rates, latencies, timeout shares, what was already tried
   (`cites-workload-facts`). Each case lists 4 to 12 such facts and requires 2 to 4 of them.
3. **It finds the evidence the decision turns on** (`finds-the-deciding-evidence`, in the 10 cases added
   on 2026-11-23 that are not ask cases). In those cases one finding settles the question and it sits in
   the least prominent place: a migration comment, a usage export that has to be added up, a notes file,
   a database that has to be queried, two columns that have to be multiplied. The assertion passes when
   the write-up reports that finding, by its number or by the element it is about. It exists because in
   these cases the right label can also be reached for the wrong reason.
4. **It weighs what it did not choose.** The option the request proposed, and a cheaper rung where one
   is a live candidate in the repo, are discussed (`weighs-alternatives`). In three cases a blind judge
   also checks that the rejection is grounded in the repo's measurements and not in general claims.
5. **When the evidence to decide is missing, it says so and asks for it.** The decision is
   `need-more-information` (or, on a condition, the label for staying put: see below) and the write-up
   asks for the specific missing facts (`asks-for-missing-evidence`). In the two ask cases added on
   2026-11-23 the files look informative and lack one number; asking for that number is required.
6. **It does not start building.** Files that came with the repo are unchanged and no infrastructure,
   migration, dependency or source files were added (`nothing-built-or-migrated`). Reading a database,
   and scratch or measurement files, are fine.

### The five categories

Every prompt defines them, in one sentence, the way a user would:

> graph-database = adopt a dedicated graph database; in-process-library = load the data into memory and
> use a graph library; recursive-sql = stay on the existing SQL database and do the traversal there with
> recursive queries and indexes; no-graph = the problem needs no graph traversal at all;
> need-more-information = it can't be decided from the evidence at hand.

The sentence was added on 2026-11-23. Before that the prompts listed the five tokens without saying
what they meant, and the first no-skill baseline showed the cost: a correct answer ("no graph database;
add the missing index and keep the SQL") was filed as `no-graph` on a case whose gold was
`recursive-sql`. Under the definitions that answer is `recursive-sql`.

### Which answers are accepted

A case accepts every category a competent engineer could defend, and no case accepts the answer its
framing pushes. Three mechanisms, each stated in the case's `rationale`:

- **Two categories, unconditionally,** where they differ in taste and not in correctness: small data
  walked with a recursive query or in the application's memory (`recursive-sql` or `in-process-library`);
  "change nothing" where the repo already runs the bounded recursive SQL the decision keeps
  (`recursive-sql` or `no-graph`); tiny static content walked in memory (`in-process-library` or
  `no-graph`).
- **A neighbouring category on a condition** (`accepted_if` in the SPEC, `accepted_on_condition` in
  `case.yaml`). The label passes only when the write-up also contains something specific:
  - *Ask cases:* the label for holding the current course (staying on the SQL database that is there,
    or keeping the library a prototype or an ADR already uses) passes when the write-up names the gap
    in the evidence and asks for the missing facts. "Do not move yet, and get me these numbers" is the
    same action as `need-more-information`; a confident "it is fine" under the same label is not, and
    fails. The option the framing pushes hardest is never accepted this way.
  - *Graph-database cases whose trap is an in-memory plan:* `in-process-library` passes when the
    write-up has worked out why the plan as proposed cannot run (the size at the right granularity
    against the memory available) and replaces the periodic reload with changes applied as they arrive.
    That is a different design from the one the framing pushes, and a defensible one.
    `need-more-information` passes in the same cases when the write-up has done that arithmetic, so the
    plan is rejected on the repo's numbers, and names what has to be measured to choose its
    replacement: these fixtures show the plan failing but hold no record of the relational route being
    tuned and still failing.
  - *No-graph cases where nobody proposes recursion:* `recursive-sql` can only mean "stay on the SQL
    database" there, and passes when the write-up says the lookups are fixed-depth and nothing recurses.
- **Proof that the alternatives pass.** The harness's selftest knows one passing answer per case. Every
  other accepted answer has a worked example in `<case>/also-accepted/<name>/`, run by
  `lib/test_also_accepted.py`.

## Open questions

- **The `graph-database` cases can be contested by "build a custom in-memory service".** Where the
  framing itself is an in-memory plan, that answer is now accepted on a condition (above). Where it is
  not, each case documents in its fixture that the in-memory route was tried or measured and why it
  failed. If runs produce a well-argued alternative on one of them, read it before trusting the fail,
  and either add the missing blocker to the fixture or accept the second category, with a changelog
  entry. This happened once: see the changelog entry on `fraud-ring-check`.
- **Conditional acceptance is decided by patterns.** The condition is matched against fixture numbers
  and element names, like `cites-workload-facts`. It can be fooled by an answer that mentions the gap
  and still concludes confidently. Two such answers were written by hand and are rejected (they are
  the `bad-confident-*` and `bad-confirms-*` selfcheck variants); read the first real runs that pass by
  this route before relying on it.
- **`finds-the-deciding-evidence` can fail a right label.** "Reject the proposal, the data is small"
  with no account of why the system is slow passes the category check and fails this one. That is
  intended (claim 3), but it is the assertion most likely to draw disagreement from a human reader, so
  its per-case pass rate in the baseline should be looked at before the gate.
- **`weighs-alternatives` is a mention check.** A script can see that the alternative is discussed, not
  that the reason is good. The judge item covers reason quality in three cases only.
- **`asks-for-missing-evidence` matches topics by pattern.** It is lenient by design for the three
  older ask cases. In the two newer ones the deciding number is a required topic and its patterns want
  a question or a request, not a mention.
- **Single turn.** A real user would answer the questions and ask again. The follow-up turn (deciding
  once the facts arrive) is not tested.
- **Trigger eval is simulated**, not measured in a host: `trigger.json` is scored by showing a model the
  skill's description alongside the other erdostack descriptions.
- **Runs that never write the file.** One Haiku baseline run spent its turns benchmarking on a local
  PostgreSQL server and was still working when first graded. `max_turns: 30` is part of every prompt's
  settings block; a run that ends without DECISION.md fails, and that is a real failure, not an
  artifact. Worth watching whether the skill makes it more or less common.

## Case sets

| Set | Cases | Purpose |
|---|---|---|
| execution-dev | 10 | iterate against; the skill author sees these |
| execution-heldout | 20 | ship decision only; the skill author never opens them |
| trigger | 10 positive / 10 near-miss negative | description |

Dev cases. "Also on a condition" is the conditional acceptance described above.

| Case | Accepted | Framing pulls toward | Storage and where the truth is |
|---|---|---|---|
| `org-chart-reports-page` | recursive-sql or in-process-library | graph-database | Postgres schema, Python loop, monthly metrics, a ticket |
| `nightly-page-ranking` | in-process-library | graph-database | a proposal, iterative SQL job, run statistics |
| `fraud-ring-check` | graph-database | recursive-sql (sceptical owner) | ADR, dropped-table migration, statement statistics, capacity note, ticket; one judge item |
| `recipe-tags-related` | no-graph | graph-database or recursive-sql | Prisma schema, query report, idea note |
| `slow-recs-vendor-call` | need-more-information; recursive-sql or no-graph on a condition | graph-database, or a confident no | Go service whose query lives in another repo, an empty slow-query export |
| `yank-impact-cli` | recursive-sql or in-process-library | graph-database (embedded) | a real SQLite file built by `setup.py`; the agent can measure |
| `asset-tags-search-timeouts` (new) | recursive-sql or in-process-library | no-graph ("tags are flat, add an index") and graph-database | README and ADR say flat; a migration comment, a function body and a hand-run plan say otherwise |
| `company-links-loader-half-built` (new) | no-graph or recursive-sql | graph-database (accepted ADR, half a loader) | a month of usage by requested depth that has to be added up; two changelog entries |
| `lineage-in-memory-adr` (new) | graph-database; in-process-library or need-more-information on a condition | in-process-library (accepted ADR, a stub to fill in) | two CSV columns to multiply, a bench note, a deployment manifest |
| `ownership-slow-log-vendor-quote` (new) | need-more-information; recursive-sql on a condition | graph-database (timeouts, a quote that lapses), or a confident no | a slow-query log with no denominator; the README says why |

Held-out: 20 cases over other domains, engines, file layouts and document types. Details are in each
case's `case.yaml` and are not repeated here, because the skill author may read this file.

- By accepted answer: 3 graph-database (one also accepts in-process-library or need-more-information on
  a condition), 3
  in-process-library, 2 recursive-sql, 3 no-graph (two also accept recursive-sql on a condition), 6
  that accept two categories (one of them a third on a condition), and 3 need-more-information (each
  also accepts one other label on a condition).
- By direction: in 7 the right answer is heavier than what the asker or the plan wants, in 10 it is
  cheaper or is "change nothing", and 3 are ask cases. The 8 cases added on 2026-11-23 are 3 heavier, 4
  cheaper and 1 ask; with the 4 new dev cases (2 heavier, 1 cheaper, 1 ask) the additions are 5 heavier,
  5 cheaper and 2 ask. The framing pulls both ways (asker one way, a colleague the other) in 3.
- Four carry generated data the agent can query (SQLite, or a content file). Two carry a judge item.
- The 8 additions set the same kinds of trap as the four new dev cases (listed in the changelog), in
  other domains, engines and file types, with the deciding evidence in other kinds of file and other
  tempting actions.

Each set contains cases where the right behaviour is to ask (2 dev, 3 held-out) and, in held-out,
cases where it is to change nothing.

A skill that always answers "you do not need a graph database" would pass most cases by count, which is
why the thresholds below add a per-direction bar.

## Thresholds

Set before any with-skill run. Defaults from the Phase 1 brief, plus one tightening.

| Metric | Bar | Why |
|---|---|---|
| Held-out lift (substance), paired by case over two models | sign test p < 0.05 in the skill's favour | no detectable lift means the skill does not earn its context cost |
| Held-out substance pass rate with skill | observed >= 75% and 95% lower bound >= 55% | the output is advisory and reviewed by the user, but must be right most of the time |
| Regressions | no case the baseline always passes and the skill always fails | a skill must not break what already works |
| **Both directions (tightened)** | with the skill, on held-out: at most one failing run among the graph-database cases, and at most one among the need-more-information cases, counted over both models; and neither group below its baseline pass count | the named failure has two directions ("reaches for a graph database, or refuses one"). Most held-out cases are answered correctly by always choosing something cheap, so a skill that only ever says no could clear the pass-rate bar while making the second half of the failure worse. Each group has had 3 cases since 2026-11-23 (2 before); the bar was not relaxed to match, so it is slightly stricter than when it was set |
| Contract assertions with skill | >= 90% | downstream skills and the user's tooling parse DECISION.md |
| Tokens and time vs baseline (median) | <= 1.5x tokens, <= 2x time | a correct but expensive skill does not get used |
| Skill size | description <= 600 chars, SKILL.md body <= 150 lines | the description is always in context |
| Trigger recall / precision (simulated) | >= 80% / >= 80% | missed triggers hide the skill; false triggers waste context |
| Judge agreement on calibration items | at most one disagreement (>= 14 of 15) before any judge verdict is applied | a judge that cannot tell a grounded rejection from a jargon one makes the three judged cases noise. 15 items since 2026-11-23 (14 before, bar then 13 of 14) |

With 20 held-out cases, the sign test needs the arms to disagree on at least 6 cases, all in the
skill's favour, to reach p < 0.05 (6 of 6 gives 0.031; 8 of 9 gives 0.039; 9 of 10 gives 0.021; 10 of
12 gives 0.039). If the baseline already passes most cases, the honest report is "no detectable
difference", and the set needs harder cases rather than a looser bar. The 2026-11-23 additions were made
for that reason, before any with-skill run.

## Graders

All graders are scripts except three judge items. Shared logic is in `lib/decision_check.py` (unit tests
in `lib/test_decision_check.py`, 32 tests); each case's `check.py` holds only its SPEC: accepted
categories and conditions, the fixture facts, the deciding evidence, the alternatives to weigh, the ask
topics, and the judge question where there is one.

| Assertion | Kind | How it is decided |
|---|---|---|
| `decision-line-parseable` | substance | script: `docs/graph/DECISION.md` exists and has a line `Decision: <category>`. The decision is the first line that is not a heading and whose value, after stripping markdown emphasis, backticks, brackets and trailing punctuation, is one of the five categories; a short annotation after the category is tolerated ("recursive-sql (stay on Postgres)", "recursive-sql, not graph-database"). Headings and any other text beginning "Decision:" are ignored, so the title `# Decision: should we adopt a graph database?` is not an answer. A heading counts only when no such line exists and its value is exactly a category. A copied template, "X or Y" and "X now, Y later" are not decisions |
| `decision-fits-workload` | substance | script: the parsed category is in the case's accepted set, or is accepted on a condition that the write-up meets |
| `cites-workload-facts` | substance | script: at least N of the case's fact patterns match DECISION.md plus final.md. Numbers match however they are written (1,104,220, 1.1M, 1.10 million) but not when rounded by more than 3% |
| `finds-the-deciding-evidence` | substance (10 cases) | script: the one finding the decision turns on is reported, matched by its numbers or by the name of the element it is about; every pattern is something in the fixture or derivable from it, never a term of art |
| `weighs-alternatives` | substance | script: each required option is named in the write-up, by any of many common names or by its literal label (`no-graph`, `in-process-library`, ...) |
| `asks-for-missing-evidence` | substance (ask cases) | script: enough of the case's missing-fact topics are asked about (3 in the older cases; 2 including the required deciding number in the newer ones) |
| `nothing-built-or-migrated` | substance | script: compares the work directory with the fixture (regenerated through `setup.py`): modified or deleted fixture files, new files inside the repo's source directories, new infrastructure, dependency or migration files, and new tables in a fixture SQLite database all fail. A new file whose name says it measures or inspects something (`bench_`, `probe_`, `measure`, `explain`, `check_` ...) is scratch work wherever it is, unless it is an infrastructure or dependency file or sits in a migrations or deploy directory |
| `sql-rejection-rests-on-repo-evidence` (1 dev), and one each in 2 held-out cases | substance | **judge**, blind to the arm: is the rejection of the cheaper option, or of the plan as proposed, grounded in this system's recorded measurements rather than in general claims |
| `decision-leads-the-file` | contract | script: the Decision line is among the first five non-empty lines |
| `facts-options-reversal-order` | contract | script: heading-like lines for workload facts, then options considered, then what would change the decision. The document title and a heading that carries the Decision line are not sections, whatever words they contain |

The two layout assertions are conventions of the erdostack skills that no prompt states, so they are
`contract`: reported separately, never part of a case passing, never part of lift. A unit test pins
that these two, and only these two, are contract. In the 2026-11-23 no-skill baseline the first passed
in 12 of 12 runs once titles were parsed correctly and the second in 1 of 12, which is what one would
expect of a convention nobody was told about.

The reasoning may be in DECISION.md or in the closing message for substance purposes, because the
prompt asks for the decision file and one parseable line, not for a layout.

No assertion rewards vocabulary. The fact and evidence patterns are fixture numbers and names; the
option patterns accept product names and plain descriptions alike ("a dedicated graph store", "load it
into memory in the worker", "a WITH RECURSIVE query"); the selfcheck "good" answers for the judged cases
are written without graph jargon, and each judged case has a "bad" answer that is fluent in the jargon,
cites sizes correctly, picks the right category, and still fails the judge item.

**Judge calibration.** 15 labelled items across the three judged cases (7 labelled yes, 8 labelled no),
in `selfcheck/*/JUDGE_LABELS.json`: for each case the plain-language good answer (yes), a second
grounded answer in a different style that fails a script assertion for another reason (yes), the
jargon-but-ungrounded answer (no), and answers that side with the framing or give no evidence (no). One
held-out judge question was reworded on 2026-11-23 and gained a labelled item, so agreement measured
before that date does not cover it: re-measure before applying verdicts.

**Selfcheck.** 137 variants: every case has a known-good output and three to five known-bad ones, each
bad variant naming the assertion that must fail (wrong category in the direction of the framing, right
category with no evidence, right category reached without the deciding evidence, right decision but
something built, a vague ask, a confident answer where asking was right, a missing Decision line). Twenty
known-good outputs carry the title shape the baseline wrote (`# Decision: <the question>`) above the
Decision line (eight older ones were retitled for this), two bad variants have such a title and no Decision line, and two have a heading that
names one category above a line that names another. `selftest` passes: every grader passes its good
output and fails each bad one. 19 further answers in `also-accepted/` folders pass their scripted
substance assertions (`lib/test_also_accepted.py`).

### Not tested

- Whether the recommended design would perform: no graph database, MySQL or SQL Server is installed
  here, and no case grades a benchmark. (PostgreSQL 16 binaries are on the machine; see SOURCES.md.)
- The quality of the reasons beyond the three judged cases and the deciding-evidence check.
- Follow-up turns, repositories with no files at all, requests in languages other than English, and
  repositories that already contain `docs/graph/CONTEXT.md` from setup-graph (the skill is expected to
  read it; no case plants one yet).
- Workloads where the right answer is a specialised system outside the five categories (search engine,
  stream processor, warehouse). Out of scope for this skill; a near-miss negative covers the nearest
  trigger.

## How to run

```bash
python3 -m unittest discover -s evals/graph-or-not/lib -p 'test_*.py'    # grader tests and the also-accepted answers
python3 evals/harness/erdo_eval.py selftest --skill graph-or-not
python3 evals/harness/erdo_eval.py prepare --root runs --skill graph-or-not --set dev --arm baseline --model <model>
# run each prepared directory, then:
python3 evals/harness/erdo_eval.py grade --root runs --skill graph-or-not
python3 evals/harness/erdo_eval.py judge-pack --root runs --skill graph-or-not --set dev --out runs/judge-dev
python3 evals/harness/erdo_eval.py report --root runs --skill graph-or-not --set dev
```

Smoke tier (after every edit to the skill): the ten dev cases, script assertions only, one run each.
Full tier (before shipping, and on any model change): both sets, both arms, two models, three runs per
case, judge items applied, cost recorded.

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

## Gate protocol, round 2: the handoff set

Set on 2026-11-23 by the maintainer, after the first gate and before any run on the `handoff` set.

- **Why.** On the single-session held-out set the skill and the bare model chose the right category equally
  often (38 of 40 runs each). That set cannot show lift and the skill does not improve the decision itself. The
  remaining claim is about what the skill leaves behind: a record of the decision and of the facts the user
  stated in chat, which a later session that no longer has the chat can act on.
- **The set.** `handoff/`: 14 two-stage cases (11 + 3 controls), plus 4 in `dev/` to iterate on. Stage one is
  the question as a user types it, with workload facts stated only in the chat; nothing in the prompt asks
  for anything to be written down. Stage two is a later session on the same repo with the chat gone: build
  what was decided, say whether the decision still stands on new numbers, or answer a counter-proposal.
  Graders accept a record anywhere in the repo in any format; `docs/graph/DECISION.md` is a contract item
  only. An agent that asks instead of inventing passes "invents no facts" but not the outcome.
- **A correction made on the dev cases first.** The first draft of these prompts ended by telling the agent to
  put the decision in `docs/graph/DECISION.md`. That is the skill's convention in the user's mouth; with it
  the bare model passed 7 of 8 dev runs, because it had been told to write the record. The sentence was
  removed (the reply now starts with the `Decision:` line) and eight stage-two prompts that leaked the
  earlier decision or numbers were fixed. With natural prompts the bare model passed 3 of 8 dev runs and
  the skill 7 of 8; the miss was the skill refusing to build in the later session, fixed in the skill
  ("When a decision is already recorded"), after which it passed 8 of 8 on dev.
- **Runs and test.** No skill and skill, Claude Haiku and Claude Sonnet, one run per model per arm, four cases
  to an agent session with the same grouping in both arms. Unit: the case. Two-sided exact sign test on
  wins against losses, **one look, bar p < 0.05**.
- **Second bar: no regression on the single-session set.** Because the skill changed after the first gate,
  both arms are run again on `heldout/` (20 cases). Bar: no case the bare model always passes and the skill
  always fails, and the skill's pass rate not more than 10 points below the baseline's.
- **What a pass would and would not mean.** It would mean a decision made with the skill survives the
  session and is usable later. It would not mean the skill decides better than the bare model; the first
  gate found no such difference. A project instruction telling every agent to write decisions down might do
  the same job; that alternative was not tested.

## Round-2 gate result (2026-11-23)

Reports: `evals/results/graph-or-not/2026-11-23-handoff-gate.md` and `2026-11-23-heldout-single-session-regate.md`. Skill version d986c4488518.

| Threshold | Bar | Result | Met |
|---|---|---|---|
| Lift on `handoff/`, paired by case | sign test p < 0.05, one look | 10 skill / 0 baseline / 4 tied, p = 0.002 | yes |
| Handoff pass rate with skill | observed >= 75%, lower bound >= 55% | 27 / 28 (82% to 99%); baseline 10 / 28 | yes |
| No regression on `heldout/` (single session) | no case lost; pass rate within 10 points | skill 40 / 40, baseline 38 / 40; 2 / 0 / 18 | yes |
| Contract with skill | >= 90% | 28 / 28 handoff, 40 / 40 single session | yes |
| Tokens, time vs baseline (median) | <= 1.5x, <= 2x | handoff 1.37x, 1.55x; single session 1.40x, 1.97x | yes (time on single-session cases is at the limit) |

**Verdict: SHIP, for what it was shown to do.** A decision made with the skill is still usable by a later session that
has lost the chat: 27 of 28 such runs succeeded, against 10 of 28 without the skill (those passes are the three
controls and the few runs where the bare model wrote a note of its own). The skill does not choose better than
the bare model: on single-session decisions the two are level, as in the first gate. Read "graph-or-not" as a
decision record that survives, not as better judgement.

Not tested: whether one line in a project's agent instructions ("write architecture decisions to a file") would
do the same; stage two sessions more than one hop later; teams that already keep ADRs (the three controls
suggest the skill neither helps nor hurts there).

## Gate protocol, round 3: cases from the register

Written 2026-11-23, before any run on the new cases.

- **Why.** The handoff gate (10 won, 0 lost, 4 tied) was on generated cases. Checked against
  `evals/REAL_PROBLEMS.md`, 6 of the 14 staged a problem with outside evidence; the skill won all 6
  (p = 0.031), short of a bar for a repeated test. By the rule in `evals/PROVENANCE.md` the skill is gated
  again. What is claimed stays what round 2 claimed: a decision that survives into the next session. Within
  one session the skill showed no gain (40 of 40 against 38 of 40) and none is claimed.
- **Set.** 20 fresh two-session cases in `handoff/`, by two authors who have not read the skill. Every
  non-control case turns on a documented situation: a graph database proposed for a workload a recursive
  query or an in-process library handles, or the reverse (RP-30, RP-05, RP-12, RP-21, RP-22). Each case names
  its entry in `case.yaml` (`sources:`). The 14 cases of the round-2 gate moved to `dev/`.
- **Bar.** This is the fourth gate for this skill, so the lift bar is **p < 0.0125** (0.05 / 4): eight cases
  won with none lost, or better.
- **Runs.** One run per model (Haiku, Sonnet) in each arm, five cases per session, same grouping in both arms.
  The unit is the case; its score in an arm is the fraction of its runs that pass every substance assertion.
  Two-sided exact sign test on cases won against cases lost.
- **Audit.** Before the verdict, every failing run in both arms goes to reviewers who do not know which arm
  it came from. A script grader they find wrong is repaired in general terms, keeps every known-bad variant
  failing, gains a known-good variant, and all runs are regraded. Judge verdicts stand as given.
- **Verdict rule.** The lift bar must hold on the grades as first produced and on the audited grades. The
  no-regression, pass-rate, contract and cost bars of the thresholds table must hold on the audited grades.
- **If it misses,** the skill's gain is reported as not shown on real problems and the skill leaves the launch
  set until a later version passes a fresh gate. The used cases move to `dev/` either way.

## Round-3 gate result (2026-11-24): a miss, by 0.0004

Skill `d986c4488518`, 20 two-session cases (16 + 4 controls), Haiku
and Sonnet, one run per model per arm: 80 runs. Reports:
`evals/results/graph-or-not/2026-11-24-handoff-sourced-gate.md` and `...-sourced-gate-audited.md`.

- **As first graded:** skill 33 of 40, baseline 19 of 40. By case: 12 won, 2 lost, 6 tied, **p = 0.0129**. The
  bar was 0.0125. Missed.
- **Audit:** of the 28 failing runs (21 baseline, 7 skill), reviewers not told the arm disputed 15 grades, 12
  on baseline runs and 3 on skill runs. Thirteen were `stage2-invents-no-facts`: the checker counted a number
  from the agent's own self-test, a labelled illustration, or an assumption the reply named and asked to have
  confirmed, as an invented fact. Two were `stage2-outcome-correct`. Repaired in the 11 affected cases.
- **Audited:** skill 36 of 40, baseline 22 of 40. By case: 11 won, 1 lost, 8 tied, p = 0.0063.
- Contract 40 of 40; tokens 1.26x, time 1.49x. No regression case.

**Verdict: a miss.** The protocol required the bar on the grades as first produced and on the audited grades,
so that a regrade can never rescue a result. The first grading missed by 0.0004 and a near miss is a miss. The
audited figure is reported because it is the better measurement, not because it changes the verdict. By the
protocol the skill leaves the launch set until a later version passes a fresh gate.

The case lost under both gradings is a control: `handoff-control-sql-valve-downstream-bench-in-repo-then-merger`.
Haiku with the skill answered need-more-information although the numbers it needed were in `docs/`.

Open: the same `stage2-invents-no-facts` code is copied into the 9 handoff cases that had no disputed grade and
into the older dev handoff cases. Those copies were not changed.

The 20 cases are now in `dev/`. `handoff/` is empty.

## Gate protocol, round 4 (one sentence added to the skill)

Written 2026-11-24, before any run on the new cases.

- **What changed.** One sentence in step 6 of `SKILL.md`: a fact is missing only after looking where step 2
  says, and a question the repo already answers is no reason for need-more-information. It answers the one
  case round 3 lost under both gradings, a control where Haiku asked for numbers that were in `docs/`.
- **Dev check before freezing.** The changed skill is run on the 20 register cases now in `dev/`, both models.
  Freeze if that control passes on Haiku and no more than two runs that passed before fail; a lost run is
  repeated twice and counts only if it fails again.
- **Set.** 25 fresh two-session cases in `handoff/` (20 + 5 controls), by two authors who have not read the
  skill, each naming a register entry with outside evidence. The graders use the repaired
  `stage2-invents-no-facts` check from the start.
- **Bar.** Fifth gate for this skill: **p < 0.01** (0.05 / 5).
- **Runs, audit and verdict rule** are those of the previous protocol: one run per model (Haiku, Sonnet) per
  arm, five cases per session, sign test by case; every failing run audited by reviewers not told the arm; the
  lift bar must hold on the grades as first produced and on the audited grades, and the no-regression,
  contract and cost bars on the audited grades.
- **If it misses,** the skill stays out of the launch set and no further gate is run for this release. The
  cases move to `dev/` either way.

### Round 4, amended before any run on the new cases (2026-11-24)

The dev check did not meet its freeze rule. With the added sentence the skill passed 33 of 40 runs on the 20
dev cases, against 36 of 40 for the round-3 skill; the control it was written for still failed on Haiku
(Haiku asks how many processes would each hold the graph in memory, which the skill's own sizing step tells
it to work out), and four other runs failed that had passed. **The sentence is withdrawn.** `SKILL.md` is
back to the round-3 text, version `d986c4488518`.

Round 4 therefore runs the round-3 skill unchanged. That makes it a replication on fresh cases, not a test of
a later version, and it is recorded as such. What justifies a replication: round 3 missed by 0.0004 on a
grading that an arm-blind audit then found wrong in 15 places, 12 of them against the baseline and 3 against
the skill. The graders in the new set carry the repaired check, plus one fix made before any run (a
hard-wrapped line no longer splits a sentence). The bar stays at **p < 0.01**, the set, runs, audit, verdict
rule and consequence stay as written above, and no further gate follows this one in this release whatever it
shows.

## Round-4 result (2026-11-24): a miss

Skill `d986c4488518` (unchanged), 25 two-session cases (20 + 5 controls), Haiku and Sonnet, one run per model per
arm: 100 runs. Report: `evals/results/graph-or-not/2026-11-24-handoff-round4-gate.md`.

- **As first graded:** skill 38 of 50, baseline 24 of 50. By case: 12 won, 2 lost, 11 tied, **p = 0.0129**. The
  bar was 0.01. Missed. Haiku 12 won, 2 lost; Sonnet 6 won, 2 lost.
- **A regression:** `handoff-control-networkx-reading-guide-then-specified-nearby-characters`, a control. Both
  models with the skill decided `no-graph` for a fixed two-step walk; the case accepts in-process-library or
  recursive-sql, and both bare models gave one of those. The audit found those grades right.
- **Audit:** 38 failing runs (26 baseline, 12 skill), 58 failing grades, read by reviewers not told the arm.
  They disputed 9: 6 on baseline runs, 3 on skill runs, mostly `stage2-invents-no-facts` again (a number from
  the agent's own test, a figure the repo states, an assumption named in the reply). The graders were not
  repaired this time, because no repair could change the verdict. With the 9 disputed grades counted as
  passes: skill 39 of 50, baseline 26 of 50, 11 won, 2 lost, 12 tied, p = 0.023.
- Contract 50 of 50; tokens 1.22x, time 1.64x.

**Verdict: a miss, on both gradings, with a real regression.** Two gates in a row on cases written from the
register show the same picture: the skill wins about half the cases and loses one or two, and that is not
enough at the bar a fourth and fifth test require. The skill is out of the launch set. No further gate is run
for this release.

What the two gates do show, for whoever writes the next version:

- The gain is real in direction: 74 of 90 runs with the skill against 46 of 90 without, across both gates as
  first graded.
- The losses are over-caution and over-classification on controls: need-more-information when the numbers
  were in `docs/`, and `no-graph` for a short fixed walk. The next version should start there.
- `stage2-invents-no-facts` is the weakest check in this eval. It was wrong 13 times in round 3 and at least
  6 times in round 4, always against a correct answer. It needs a rewrite before another gate, not another
  patch.

The 25 cases are now in `dev/`. `handoff/` is empty.

## Gate protocol, round 5 (a new version, a rebuilt check, a larger set)

Written 2026-11-24, before any run of the new version and before the new cases existed.

- **Why a gate after "no further gate".** The round-4 protocol said no gate would follow it in this release
  whatever it showed. That limit is lifted here, openly: the project's standing rule is that a skill is
  not done until it shows a significant improvement, so work continued after the miss. The price is in the
  bar below, which counts every gate this skill has had.
- **What changed in the skill.** Not a bolt-on sentence this time; four existing instructions were corrected.
  (1) Rung 1 and the workload sheet: `no-graph` is for lookups that cross a link table at most once; following
  a relation between things of the same kind for more than one step is a walk, even a short fixed one, and
  stays where the edges already live. (2) Step 4: memory is compared against the copies the repo or the user
  states, else the processes that run today; a copy count nobody gave is not a missing fact. (3)
  `need-more-information`: a number that only says how an option would do once adopted describes a remedy and
  is never the missing fact; a percentile over budget counts as a measured failure. (4) Business rules the
  owner states are the need, are recorded in the decision file, and are followed by the session that builds.
- **What changed in the graders.** `stage2-invents-no-facts` was disputed 24 times by two arm-blind audits. It
  was rebuilt on a stated principle (see the changelog entry of this date) with unit tests made of every
  disputed example and every known-bad variant, by an engineer not told the arms. The new library is used by
  every new case and installed in the dev cases whose self-checks stay green.
- **A case defect found, and what it does not change.** The round-4 control
  `handoff-control-networkx-reading-guide-then-specified-nearby-characters` accepted `in-process-library` or
  `recursive-sql` and rejected `no-graph`, although "Which answers are accepted" above gives tiny static
  content walked in memory the pair `in-process-library` or `no-graph`. The case now accepts all three. The
  round-4 verdict stands as recorded: it missed on the grades as first produced, and no later repair can
  change that under the both-gradings rule.
- **Dev check before freezing.** The new version is run on the 45 register two-session cases now in `dev/`
  (rounds 3 and 4), both models, with the rebuilt check. Freeze if it passes at least 74 of 90 runs (what the
  previous version scored on these cases as first graded) and the two controls named in the round-4 result
  pass on both models. A failing run of a named control is repeated twice and counts only if it fails again.
  If the rule is not met, the previous version (`d986c4488518`) is gated instead, unchanged.
- **Set.** 40 fresh two-session cases by four authors who have not read the skill, each naming a register
  entry with outside evidence, about one in five a control. Before any run, a reviewer who has seen no run
  checks every case's accepted answers against "Which answers are accepted"; a case that rejects an answer
  that section accepts is corrected before the gate, not after.
- **Bar.** Sixth gate for this skill: **p < 0.0083** (0.05 / 6), two-sided exact sign test by case.
- **Runs, audit and verdict rule** as in round 3: one run per model (Haiku, Sonnet) per arm and stage, five
  cases per session, same grouping in both arms; every failing run audited by reviewers not told the arm; the
  lift bar must hold on the grades as first produced and on the audited grades; no regression, contract at
  least 90% and cost on the audited grades.
- **If it misses,** the skill stays out of the launch set. The cases move to `dev/` either way.


## Round-5 gate result (2026-11-24): the bar is met

Version `a8ddcabe4a24`, frozen after the dev check (83 of 90 runs on the 45 register two-session cases, bar
74; both named controls passed on both models). 40 fresh two-session cases, each naming a register entry with
outside evidence; Claude Haiku and Claude Sonnet, one run per model per arm and stage (160 runs, 320
sessions). Before any run two reviewers who had seen none checked every case against "Which answers are
accepted".

| Grading | With the skill | Without | Cases won / lost / tied | p (two-sided sign test) | Bar |
|---|---|---|---|---|---|
| As first produced | 74 / 80 | 34 / 80 | 29 / 1 / 10 | 0.00000006 | 0.0083 |
| After the audit | 77 / 80 | 35 / 80 | 30 / 1 / 9 | 0.00000003 | 0.0083 |

- **Verdict: SHIP for the claim this set tests.** The lift bar holds on both gradings with room to spare. No
  case passed on both models without the skill and failed on both with it. Contract 80 of 80 runs (the
  unaided agents cannot know the file's conventions and score 0). Cost: median 49,019 tokens against 36,131
  over the two sessions (1.36 times) and 70.8 s against 72.4 s.
- **What the claim is.** A decision made in one session is still the decision in the next. With the skill
  the first session leaves a decision record in the repo and the second session, which has no memory of the
  first, builds what was decided; without it the second session re-decides from the request in front of it,
  or builds on a store the first session had ruled out. It is a claim about carrying a decision across
  sessions, not about deciding better: on single-session cases (the first gate, 20 cases) the unaided agents
  already chose correctly and the skill showed no difference.
- **By kind, audited grades.** The 32 cases where the second session depends on the first decision: 62 of
  64 runs with the skill, 19 of 64 without. The 8 controls, where the second request settles the store by
  itself or has nothing to do with the decision: 15 of 16 with, 16 of 16 without.
- **By model, audited grades.** Haiku 10 of 40 without the skill and 37 with it; Sonnet 25 and 40. Both
  models gain, the weaker one more.
- **The one loss** is a control, `handoff-control-sqlite-roadworks-permits-then-specified-nearby-segments`:
  one Haiku run with the skill. It stays in `dev/` as a failing case.
- **Audit.** The 52 failing runs as first graded, and 9 more passing-but-doubtful ones, were read by
  reviewers not told the arm (61 runs). 16 grades were disputed, nearly all on `stage2-invents-no-facts`.
  A blind repairer upheld all 16, fixed the canonical library once in general terms (the principle is in the
  changelog entry of this date) and three case checks; 825 self-check variants are green afterwards. Four
  runs changed from fail to pass: three with the skill, one without.
- **What was not tested.** Live graph databases (nothing was installed; the fixtures are files and SQLite),
  models other than Haiku and Sonnet, repos that were not generated for the eval, more than two sessions,
  and triggering in a real host. This was the skill's sixth gate; the bars 0.05 / k for k = 1 to 6 sum to
  0.12, the honest ceiling on the chance that some gate passes by luck. (Note added 2026-11-27: the bars
  actually used, 0.025, 0.05, 0.0125, 0.01 and 0.0083, sum to 0.11, which is the figure `BENCHMARK.md` gives.) A result at p below one in ten
  million is not near that ceiling.
- The 40 cases are in `dev/` now.

## Results log

| Date | Skill version | Model | Set | Arm | Passed / runs (substance) | 95% interval | Contract | Judge agreement | Tokens (median) | Time (median) |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-11-23 | 7dafd02b4482 | Haiku + Sonnet, one run each per arm (gate, first look) | heldout, 20 cases | both | skill 38 / 40; baseline 38 / 40 | 84% to 99%; 84% to 99% | skill 40 / 40; baseline 0 / 40 | 15 / 15 calibration items | 27599 vs 20454 | 58.0 s vs 37.0 s |

Gate (2026-11-23), full report in `evals/results/graph-or-not/2026-11-23-heldout-pass1.md`. **No detectable difference on substance: bar not met.** Paired by case 1 skill / 1 baseline / 18 tied, p = 1.0. With no skill both models already choose the right category in 38 of 40 runs, so this set cannot show lift, and a second pass could not have reached the bar (it adds runs, not cases). The skill's measurable effect here is the contract: every skill run left `docs/graph/DECISION.md` in the agreed form and no baseline run did. Whether that record is worth anything is the question the `handoff` set (round 2) asks.

No runs recorded. A no-skill dev baseline was run on 2026-11-23 (Sonnet and Haiku, one run each on the
six cases of the time). It is not entered above because it was produced with prompts that have since
changed and graded by a parser that misread titles. Regraded with the corrected grader, 10 of the 12
runs pass every scripted substance assertion (one of them with its judge item still pending). The two
failures are the category confusion that the definitions in the prompt remove, and one run that
answered `need-more-information` on a case where the evidence to decide is in the repo. The baseline has to be rerun on the current prompts
and all ten dev cases before it says anything about difficulty.

## Standards track (2026-11-27)

Six cases in `standards/` stage this skill's claim on a workload from a published benchmark (`evals/STANDARDS.md` has the
sources and the protocol). They were run once, with the version frozen for release 0.1.0, as part of one test over all
five skills: 11 cases won, none lost, 19 tied of 30, p = 0.00098 against a bar of 0.05, on both gradings. Six cases carry
no verdict for one skill, so what follows is reported and not tested.

This skill, audited grades: 12 of 12 runs with the skill and 6 of 12 without (5 cases won, none lost, 1 tied); as first produced 11 of 12 and 4 of 12, with the same 5 / 0 / 1. The audit disputed three failing grades (one with the skill, two without) and a blind repairer upheld all three: a scan for named SQL parameters that an apostrophe inside a comment could derail, and a count measured on the repository's sample data read as an invented workload figure. The repaired library is in all six `standards/` cases, and the parameter scan was corrected in the 103 `dev/` cases that carry a copy; 893 self-check variants pass. Cost on this set: Haiku with the skill took 273 s per case over its two sessions against 48 s without, and 1.8 times the tokens; Sonnet 49 s against 44 s.

The six cases count as seen from now on. Reports: `evals/results/graph-or-not/2026-11-27-standards-standards-v1.md` and `...-standards-v1-audited.md`.

## Changelog

- 2026-11-27: before publication every `case.yaml` got a canary comment as its first line: it asks that the file be kept out of training data, and no grader reads it. The 184 runs behind round 5 and the standards set are published in `recorded-runs/graph-or-not/` of the case repository: the agent's closing messages, the files it wrote and every grade. 181 can be built again from the published files and regrade as recorded; 3 changed a database that is not published. The 160 round-5 runs were also graded again from the saved run directories with the grader library as repaired on this date: every grade came out as recorded.
- 2026-11-27: empty fixture directories are now listed in `empty-dirs.txt`, because git does not carry them, and
  `lib/test_also_accepted.py` recreates them. No grade changed.
- 2026-11-27: `standards/` added (six cases staged on published benchmark workloads, written and reviewed before any run) and run once in the pooled standards test; result recorded above. Two faults in the two-session grader library repaired after the audit and applied to every copy. A note at the top of this file says where the case sets live from release 0.1.0.
- 2026-11-24: round 5 recorded: SHIP (as first produced 29 / 1 / 10, audited 30 / 1 / 9; bar 0.0083). The
  rebuilt `stage2-invents-no-facts` check (canonical copy with unit tests; when in doubt it passes; a named
  assumption, arithmetic on given numbers, a figure about the agent's own test, or a description of code
  already in the repo is not an invented fact) is installed in all 103 two-session cases. After the audit the
  library was corrected once more for 16 upheld disputes and three case checks were fixed (quote cost, role
  inheritance, capacity planner). The reading-guide control now accepts `no-graph` as "Which answers are
  accepted" always said it should; the round-4 verdict is unchanged. A reviewer who had seen no run corrected
  cases of the new set before it was run. The 40 cases moved to `dev/`.
- 2026-11-23: round-2 gates run and recorded: handoff lift 10 / 0 / 4 (p = 0.002), single-session no-regression met on a fresh run of both arms with the revised skill. No case, grader or threshold changed after the protocol was set.
- 2026-11-23: handoff set added (14 two-stage cases, 4 more in dev) and the round-2 protocol set before any run on it. Thresholds changed: the lift bar moves from the single-session set, where the first gate found no difference, to the handoff set; the single-session set keeps a no-regression bar. Reason: the two sets answer different questions and the first one is at ceiling without a skill. The dev handoff prompts were corrected once before the gate (they told the agent where to file the decision); see the protocol.
- 2026-11-23: created. 6 dev and 12 held-out cases, 20 trigger queries, shared grader with unit tests,
  three judge items with 14 calibration labels. Thresholds are the Phase 1 defaults plus a
  both-directions bar, added because most cases are answered correctly by always choosing the cheaper
  option, which is one half of the failure this skill is meant to fix.
- 2026-11-23, revision after the first no-skill dev baseline and before any with-skill run. Every prompt
  changed, so results from before this entry are not comparable.
  - **Decision-line parser.** Agents titled the file `# Decision: <the question>` and then wrote the
    required line; the parser read the title as a second, conflicting decision and reported "Decision
    lines disagree" on 3 of 12 baseline runs, two of which had an accepted category on the line. Now the first non-heading line whose value is a category is
    the decision and other "Decision:" text is ignored; a heading counts only when there is no such
    line and its value is exactly a category. Two decision lines that disagree used to be an error; the
    first now wins, because that is what a tool reading the file does. Unit tests cover the five title
    shapes the baseline produced; selfcheck variants were added as described under Graders.
  - **Category definitions in every prompt.** One sentence, the same in all 30. Reason: without it a
    no-skill agent could not know that `no-graph` means "no traversal at all" and not "no graph
    database" (one baseline run failed on exactly that).
  - **Accepted sets widened where a neighbouring category is defensible.** `org-chart-reports-page` now
    also accepts in-process-library (one query and a walk in the API is a sound fix for 471 rows).
    `slow-recs-vendor-call` and two held-out ask cases accept the label for staying put when the
    write-up names the gap and asks for the missing facts; the previous author had flagged the strict
    label as the likeliest disagreement with a human reader. One held-out no-graph case accepts
    recursive-sql when the write-up says nothing recurses. One held-out graph-database case accepts
    in-process-library on the same kind of condition as `lineage-in-memory-adr`; its judge question was
    reworded to match and one calibration item was added (14 to 15). No accepted set was narrowed.
  - **Contract audit.** `decision-leads-the-file` and `facts-options-reversal-order` were already
    `contract` in the shared grader and no case overrides them; a unit test now pins it. Every other
    assertion was re-read against "passable by a careful no-skill agent from the prompt and files
    alone". One change came out of that: `nothing-built-or-migrated` no longer fails a measurement
    script because of where it was saved or because its name contains a word like "closure".
  - **`fraud-ring-check` fixture.** A baseline run declined to decide and proposed replacing the
    traversal with a connected-group label maintained on write, a route the fixture had not closed. The
    ADR's history table now records that it was tried in shadow mode and abandoned (63% of active
    accounts in one group). The accepted set is unchanged.
  - **Grader additions.** `accepted_if` (a category accepted on a condition), `key_evidence` (the
    `finds-the-deciding-evidence` assertion), required ask topics, and `lib/test_also_accepted.py` with
    the `also-accepted/` folders, because the harness's selftest can hold only one passing answer per
    case.
  - **Harder cases: 4 dev and 8 held-out added, none removed** (10 and 20). The baseline passed nearly
    everything once the artifacts were removed, so the sets could not have shown a lift. The additions
    are harder through the situation, not through the grading: the deciding evidence is in the least
    prominent file while the request and an ADR argue for the wrong option; numbers have to be combined
    (columns times upstream columns times bytes per edge; row counts across a manifest; steps times
    fan-out) to see whether a graph fits in memory or a recursion is small; a graph-shaped requirement
    whose usage is one-step lookups, and "flat" data whose log shows a recursive query timing out; a
    tempting action (finish the loader, add the dependency, sign the order) where the right move is to
    decide and stop; and ask cases whose files look complete and lack one number. Directions are
    balanced across the additions: 5 where the right answer is heavier than the plan, 5 where it is
    cheaper, 2 ask.
  - **Thresholds.** Not loosened. The judge-agreement bar is restated for 15 items; the both-directions
    bar now covers 3 cases per group instead of 2.
  - **SOURCES.md** corrected: PostgreSQL 16 is installed on this machine, and the PostgreSQL in the new
    fixtures was executed on it.
- 2026-11-23, second revision, after the first dev runs with a skill draft and before the held-out gate.
  No prompt or fixture changed, so dev runs made since the first revision stay valid and only need
  regrading.
  - **`weighs-alternatives`: every category's pattern now matches its own literal token.** The
    `no-graph` pattern matched "no graph" and many descriptions but not the hyphenated label, so an
    options section that named the alternatives by the labels the prompt gave was not credited. A
    pattern for `need-more-information` was added for completeness. Unit test over all five labels in
    four spellings; a worked example whose options section uses labels only (`also-accepted/`, on a
    held-out case, since no dev case requires `no-graph` to be discussed).
  - **`facts-options-reversal-order` (contract): a title containing "option" broke it.** The check took
    the first heading that matched each section word, so `# Decision: which option ...?` was read as the
    options section and the order came out wrong. The title and any heading carrying the Decision line
    are now skipped, and each section is looked for after the one before it. Three unit tests; the
    known-good answer of `company-links-loader-half-built` now has such a title.
  - **`lineage-in-memory-adr`: the gold was too narrow, and is widened.** Both no-skill baseline
    models multiplied out the 387 million column-level edges, rejected the ADR's plan, and answered
    `need-more-information`, arguing that the recursive query in the repo has never been tuned (it
    dedupes on column and depth together) and that nothing has been measured on the real edge set. On
    re-reading the fixture they are right: it contains everything needed to reject the ADR, which is
    what the case is about, and no record of the relational route being tuned and failing, which is what
    makes `fraud-ring-check` decidable. A careful engineer can defend waiting. `need-more-information`
    is now accepted on a condition (the column-level size worked out, and the deciding measurement
    named); `graph-database` stays accepted; following the ADR, or hedging without the arithmetic,
    still fails (new selfcheck variant `bad-hedges-without-the-arithmetic`). Regraded, both baseline
    runs pass the case. The fixture was left alone on purpose, so that existing runs remain comparable.
    The held-out case of the same kind has the same gap in its fixture and got the same condition, from
    this finding and not from any held-out run.
  - Counts: 137 selfcheck variants, 19 also-accepted answers, 32 grader unit tests.
- 2026-11-23: round 3 opened on 20 two-session cases written from `evals/REAL_PROBLEMS.md`; round-2 handoff cases moved to `dev/`. Reason: 6 of the 14 round-2 cases staged a problem with outside evidence, too few for a repeated test (see `evals/PROVENANCE.md`).
- 2026-11-24: round 3 run and recorded (miss: p = 0.0129 as first graded against a bar of 0.0125; 0.0063 audited). `stage2-invents-no-facts` and two `stage2-outcome-correct` checks repaired in 11 cases after the audit. The 20 cases moved to `dev/`.
- 2026-11-24: one sentence added to step 6 of the skill and round 4 opened on 25 fresh two-session register cases, bar 0.01.
- 2026-11-24: round 4 amended before any run on its cases: the added sentence failed its dev check and was withdrawn, so round 4 is a replication of the round-3 skill on fresh cases with repaired graders. Bar unchanged at 0.01.
- 2026-11-24: round 4 run and recorded (miss: p = 0.0129 against 0.01, one regression). Nine disputed grades from the audit were not repaired. The 25 cases moved to `dev/`.
