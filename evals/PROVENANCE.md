# How much of the evidence rests on real problems

Every eval case in this repo runs in a generated repository (see the top of `REAL_PROBLEMS.md` for why). This
file answers a narrower question: of the cases each skill was judged on, how many stage a problem that is
documented to happen, and does the skill's measured gain survive when only those cases are counted?

## Rule, written before the second tagging pass was run

1. Each case is tagged by a reviewer who sees the case's expected outcome and the register, and nothing else:
   no results, no skill text. A case gets an id only when its central problem (or, for a restraint case, the
   false alarm it is built on) is an instance of that entry. No stretching.
2. Entries count as **outside evidence** when their status is `read`, `executed` or `bundled`. Entries with
   status `repo` or `memory` are reported separately and do not count towards rule 3.
3. A skill's gain counts as **shown on real problems** when its deciding gate, cut down to the cases tagged
   with at least one outside-evidence entry, still meets the lift bar that gate was run under, with no case
   that the baseline always passes and the skill always fails. The other bars (cost, contract) are properties
   of the whole run and are not recomputed.
4. A skill that does not meet rule 3 gets a fresh gate on cases written from the register, or its claim is
   reported as not shown on real problems. No third option.

The first pass (register RP-01 to RP-24) is reported as it came out, including where it is unflattering.

## First pass (register RP-01 to RP-24)

Eight reviewers tagged the 712 cases that existed on 2026-11-23. The tags are in `evals/provenance.json`,
which is kept with the cases in `erdostack/bench` (`pass: 1`).

| Skill | Cases tagged | Deciding gate, all cases | Same gate, tagged cases only |
|---|---|---|---|
| query-review | 233 of 490 | 27 won, 6 lost of 240, p = 0.0003 | 7 won, 4 lost of 95, p = 0.55 |
| roast-my-graph | 39 of 70 | round 2: 10 won, 2 lost of 40, p = 0.039 | 7 won, 1 lost of 19, p = 0.070 |
| setup-graph | 2 of 38 | 8 won, 0 lost of 26, p = 0.0078 | 0 won, 0 lost of 1 |
| schema-first | 2 of 66 | handoff: 10 won, 0 lost of 12, p = 0.002 | no tagged case in the gate |
| graph-or-not | 2 of 48 | handoff: 10 won, 0 lost of 14, p = 0.002 | no tagged case in the gate |

The first register was built around query and model defects, so it had no entry for most of what three of the
skills are about. That is a gap in the register, and it is also the finding: the evidence for those skills did
not rest on anything documented outside this project.

## Second pass (register extended to RP-33)

Nine entries were added (RP-25 to RP-33), each with its own source, and seven reviewers re-tagged the 434
untagged cases against the whole register, again without seeing results (`pass: 2` in `evals/provenance.json`;
2 cases got no answer and stay untagged). The entries were chosen after seeing which kinds of case were
untagged. The tagging itself was blind.

Counting only entries with outside evidence at that time (so not RP-24 and RP-26, which rest on this project's
own runs, nor the entries then marked `memory`):

| Skill | Deciding gate, outside-evidence cases only | Rule 3 |
|---|---|---|
| query-review (round 5, audited) | 10 won, 5 lost, 112 tied of 127, p = 0.30 | not met |
| setup-graph | 2 won, 0 lost, 7 tied of 9, p = 0.5 | not met |
| schema-first (handoff) | none of the 12 cases | not met |
| graph-or-not (handoff) | 6 won, 0 lost of 6, p = 0.031 | not met (a repeated test needs better) |
| roast-my-graph (round 2) | 3 won, 1 lost of 13 | not met, and round 2 had already missed |

No skill's earlier result survived the cut. Rule 4 applied to all five.

## Fresh gates on cases written from the register (2026-11-24)

Protocols and bars were written into each skill's `EVALS.md` before any run. Every new case names its register
entry in `case.yaml` (`sources:`). The graders' failing grades were audited by reviewers not told the arm, and
a skill had to clear its bar on the grades as first produced and on the audited grades.

| Skill | Cases | With skill | Baseline | Won / lost / tied | p as graded | p audited | Bar | Verdict |
|---|---|---|---|---|---|---|---|---|
| roast-my-graph v3 | 120 (109 outside evidence) | 223 of 240 | 191 of 240 | 29 / 8 / 83 | 0.0002 | 0.0008 | 0.0167 | pass |
| schema-first | 20 two-session | 38 of 40 | 12 of 40 | 14 / 0 / 6 | 0.0001 | 0.0001 | 0.0167 | pass |
| graph-or-not | 20 two-session | 36 of 40 | 22 of 40 | 11 / 1 / 8 | 0.0129 | 0.0063 | 0.0125 | miss (first grading, by 0.0004) |
| setup-graph | 40 | 78 of 80 | 72 of 80 | 7 / 1 / 32 | 0.039 | 0.070 | 0.025 | miss, and one regression |
| query-review | not run | | | | | | | not shown |

Counts in the table are under the audited grading. For roast-my-graph the 109 outside-evidence cases alone give
26 won, 6 lost (p = 0.0005).

`query-review` got no fresh gate. Its gain on documented problems is two to three points over a baseline that
already passes 93%, and confirming a gap that small at the bar for a sixth test would take several hundred
cases.

## What "real" means here, and what it does not

- A case counts as staging a real problem when the thing that makes it hard is documented outside this project
  (vendor documentation, an engine's own notification or error code, a public engineering write-up) or was
  reproduced on the SQLite and NetworkX installed where the case was written, or uses a public dataset that
  ships with NetworkX.
- The repositories around those problems are still generated. No real user's repository, issue or data is in
  this library, and nothing was copied from the sources cited.
- Cypher behaviour was never executed: no Neo4j or LadybugDB server was available. Cypher cases are graded by
  reading the statements.
- Register statuses changed once: RP-14, RP-15, RP-16, RP-18 and RP-19 went from `memory` to `read` on
  2026-11-23, before the roast-my-graph gate ran. The second-pass table above uses the statuses as they were
  when it was computed.

## After the first fresh gates (2026-11-24)

- `graph-or-not` got one replication on 25 new register cases with its graders repaired and the skill
  unchanged: 12 won, 2 lost, 11 tied, p = 0.0129 against a bar of 0.01, with one regression. A miss again.
- `setup-graph` got a second version (one rule about Maven BOMs). It fixed the regression case on Sonnet but
  not on Haiku, short of the rule set for freezing it, so its third gate was not run. Sixty new register cases
  sit in `evals/setup-graph/heldout/`, never run with the skill. (Note added 27 November: they were run later, as
  the third gate in the next section, and are in `dev/` now.)

Where that leaves the five skills on real problems:

| Skill | Shown on real problems | Evidence |
|---|---|---|
| roast-my-graph | yes | 120 register cases: 29 won, 8 lost, p = 0.0008 |
| schema-first | yes | 20 two-session register cases: 14 won, 0 lost, p = 0.0001 |
| graph-or-not | no | two gates, 12 won and 2 lost each time, p = 0.0129 both times |
| setup-graph | no | 40 register cases: 8 won, 1 lost, p = 0.039; one regression |
| query-review | no | no fresh gate; 10 won, 5 lost on the 127 documented cases of round 5 |

That table is the position on 24 November, kept as it was written. Three of its rows changed afterwards.

## Later gates (24 to 27 November 2026)

The three skills that had not been shown on real problems were gated again, each on fresh cases written from
the register, with the protocol and the bar written into the skill's `EVALS.md` before any run. Counts are
under the audited grading, as above.

| Skill | Gate | Cases | With skill | Baseline | Won / lost / tied | p as graded | p audited | Bar | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| graph-or-not | round 5, a new version | 40 two-session | 77 of 80 | 35 of 80 | 30 / 1 / 9 | 0.00000006 | 0.00000003 | 0.0083 | pass |
| setup-graph | third gate, version 3 | 60 | 116 of 120 | 113 of 120 | 5 / 2 / 53 | 0.29 | 0.45 | 0.0167 | miss, one regression |
| setup-graph | fourth gate, version 4 | 80: 64 from three kinds of repo, 8 documentation cases, 8 controls | 156 of 160 | 139 of 160 | 16 / 2 / 62 | 0.0005 | 0.0013 | 0.0125 | pass, for a narrowed claim |
| query-review | round 6, version 6 | 120 | 234 of 240 | 224 of 240 | 10 / 1 / 109 | 0.0117 | not regraded | 0.0083 | miss |
| query-review | round 7, version 7 | 60 | 116 of 120 | 104 of 120 | 13 / 1 / 46 | 0.0074 | 0.0018 | 0.0071 | miss on the first grading, by 0.0003 |
| query-review | round 8, version 7 unchanged | 120 | 231 of 240 | 209 of 240 | 29 / 6 / 85 | 0.00002 | 0.0001 | 0.00625 | lift met; one regression and contract at 85%: not passed |
| query-review | round 9, version 7 unchanged | 80 | 159 of 160 | 140 of 160 | 18 / 0 / 62 | 0.000008 | the same | 0.0056 | pass, for a narrowed claim |

Two of these passes are for claims narrower than the skill's name suggests, and the narrowing was chosen from
dev data before the gate was run:

- `setup-graph` was gated on a set built around the three kinds of repo where unaided agents had recorded a
  wrong fact in the earlier gates (an embedded or in-process engine, an override layer that decides the
  version, a query language that has to follow the pinned server): 64 of the 80 cases, with every win. The
  other 16 are 8 repos whose documentation promises what the configuration does not deliver and 8 controls.
  On unselected register cases it missed twice.
- `query-review` was gated on requests to change production data in bulk, with controls on development
  copies. For the rest of what the skill covers, round 6 found 3 cases won and none lost of 88: no
  measurable gain. Round 8's regression came from Cypher development targets that were logging stand-ins;
  round 9 used only targets that really execute. What the skill does with a Cypher change on a live
  development database is untested.

Every case in these seven gates names a register entry with outside evidence. Two register changes were made
before the round-6 cases were written and are recorded in `REAL_PROBLEMS.md`: RP-24 was re-read and upgraded
from `repo`, and RP-34 was added from a public postmortem. Under today's statuses 115 of the 120 cases in the
`roast-my-graph` gate name an outside-evidence entry (109 when it ran).

Where the five skills stand on real problems, as of release 0.1.0:

| Skill | Shown on real problems | Evidence |
|---|---|---|
| roast-my-graph | yes | 120 register cases: 29 won, 8 lost, p = 0.0008 |
| schema-first | yes | 20 two-session register cases: 14 won, 0 lost, p = 0.0001 |
| graph-or-not | yes | 40 two-session register cases: 30 won, 1 lost, p = 0.00000003, after two misses on register cases at p = 0.0129 |
| setup-graph | yes, for three kinds of repo | 80 register cases: 16 won, 2 lost, p = 0.0013, after two misses on unselected cases |
| query-review | yes, for bulk changes aimed at production | 80 register cases: 18 won, 0 lost, p = 0.000008, after eight earlier gates |

## The standards track (27 November 2026)

Thirty further cases take their workload from two published benchmarks instead of the register, the LDBC
Social Network Benchmark (26 cases) and LDBC Graphalytics (4); each also names the register entry its trap
comes from. They are LDBC-derived work, not an LDBC Benchmark, and their result is not an LDBC Benchmark
Result. They were run once, as one test over all five skills: 11 cases won,
none lost, 19 tied, p = 0.00098 against a bar of 0.05, on both gradings. `STANDARDS.md` has the sources, the
protocol and the result. The repository's `BENCHMARK.md` puts both tracks on one page.
