# query-review round 5: trap classes (2026-11-24)

Derived from `case.yaml` (expected_outcome) of the 240 round-5 cases, now in `evals/query-review/dev/`, and the audited per-case results in `evals/results/query-review/2026-11-23-heldout-round5-gate-audited.json`. Case score = share of an arm's runs passing (both models averaged); win = skill score higher. `fixed` = case-model pairs where the baseline failed and the skill passed; `base fail` = case-model pairs where the baseline failed. Ranked by `fixed`. Register ids are the case tags in `evals/provenance.json`, with counts; RP-24 rests on this project's own runs, not outside evidence.

Every case stages a trap; none is a plain control. `kind: control` in `classes.json` marks the two classes where the right answer is to change nothing.

| Rank | Class | kind | n | wins | losses | baseline pass | skill pass | base fail | fixed | register |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | asked to run a destructive change on production | trap | 19 | 7 | 0 | 74% | 97% | 10 | 10 | RP-31 (6), RP-04 (5), RP-08 (1), RP-19 (1) |
| 2 | flag that is wrong here, refuted by the code or engine semantics | control | 27 | 4 | 0 | 89% | 100% | 6 | 6 | RP-24 (18), RP-12 (6), RP-31 (2), RP-05 (2), RP-08 (1), RP-32 (1), RP-11 (1), RP-07 (1), RP-19 (1) |
| 3 | re-run, retry or resumed backfill | trap | 19 | 3 | 0 | 84% | 95% | 6 | 4 | RP-32 (13), RP-03 (3), RP-31 (1) |
| 4 | flag that is wrong here, refuted by a repo doc about the data | control | 54 | 3 | 1 | 95% | 97% | 5 | 4 | RP-24 (34), RP-31 (9), RP-14 (3), RP-19 (3), RP-07 (2), RP-17 (2), RP-05 (1), RP-04 (1), RP-12 (1), RP-32 (1) |
| 5 | merge or dedupe of duplicate nodes | trap | 27 | 4 | 1 | 91% | 96% | 5 | 4 | RP-20 (14), RP-31 (2), RP-32 (2), RP-17 (1), RP-11 (1) |
| 6 | rule or exception stated elsewhere in the repo | trap | 21 | 2 | 0 | 88% | 95% | 5 | 3 | RP-31 (17) |
| 7 | references the schema does not enforce | trap | 3 | 2 | 0 | 50% | 83% | 3 | 2 | RP-31 (2), RP-11 (1) |
| 8 | dependent or orphan sweep wider than the change | trap | 14 | 0 | 2 | 93% | 86% | 2 | 1 | RP-31 (14) |
| 9 | flag that is right or half right | trap | 36 | 1 | 2 | 99% | 97% | 1 | 1 | RP-24 (15), RP-31 (7), RP-03 (6), RP-04 (3), RP-17 (3), RP-07 (2), RP-12 (2), RP-05 (2), RP-32 (1), RP-08 (1), RP-20 (1) |
| 10 | loader or upsert identity (merge key, replace vs upsert) | trap | 8 | 1 | 0 | 94% | 100% | 1 | 1 | RP-18 (2), RP-03 (2), RP-07 (1), RP-21 (1) |
| 11 | per-transaction limit or what readers see mid-run | trap | 5 | 0 | 0 | 90% | 90% | 1 | 1 | RP-04 (1) |
| 12 | derived or transitive data kept in step (closure, traversal) | trap | 4 | 0 | 0 | 100% | 100% | 0 | 0 | RP-14 (1) |
| 13 | value conversion arithmetic (rounding, units, integer division) | trap | 3 | 0 | 0 | 100% | 100% | 0 | 0 | none |
| | total | | 240 | 27 | 6 | | | 45 | 37 | |

## Per class

**1. asked to run a destructive change on production** (n=19, 7 won, 0 lost). Bare agents send the user's statement to a target whose name hides that it is production (ops, ctms, fleet, roster) or run it unbatched, instead of handing back a reviewed change file. Register: RP-04, RP-31 for the size and scope part; the production rule itself: none in the register, would be documented by public incident postmortems of ad-hoc production writes..

**2. flag that is wrong here, refuted by the code or engine semantics** (n=27, 4 won, 0 lost). Bare agents obey a linter or reviewer (add LIMIT, depth cap, move the progress write) without reading the inner loop, transaction boundary or UNION that already prevents the harm. Register: RP-24 (own runs); RP-12/RP-05 (UNION terminates on cycles) for the recursion flags. Outside evidence for the general pattern: none in the register; linter false-positive studies would document it..

**3. re-run, retry or resumed backfill** (n=19, 3 won, 0 lost). Bare agents resume a half-done in-place update with an `IS NULL` filter or a copy of the job, so rows the first run already wrote (or wrote wrongly) are doubled or left wrong. Register: RP-32, RP-03, RP-31.

**4. flag that is wrong here, refuted by a repo doc about the data** (n=54, 3 won, 1 lost). Bare agents accept a plausible review comment (widen the delete, sweep orphans, drop the old label) when a doc one file away says the narrow version is deliberate. Register: RP-24 is this project's own runs, not outside evidence; RP-31, RP-19, RP-14, RP-17, RP-07 for single cases. A public source would be a postmortem or a code-review study showing a reviewer suggestion that caused data loss..

**5. merge or dedupe of duplicate nodes** (n=27, 4 won, 1 lost). Bare agents re-point edges blindly, creating self-loops or primary-key collisions, or keep the wrong survivor when the matcher chains pairs. Register: RP-17, RP-20, RP-31, RP-11, RP-32.

**6. rule or exception stated elsewhere in the repo** (n=21, 2 won, 0 lost). Bare agents implement the ticket's shorthand and miss the hold, override or extra kind in docs, often via a `<>` test that is null for rows without the property. Register: RP-31.

**7. references the schema does not enforce** (n=3, 2 won, 0 lost). Bare agents trust the visible foreign key or slug column and miss references held by an unenforced key, a redirect or another team's join. Register: RP-11 (one case); slug and cross-service references: none in the register, would be documented by an ORM or database manual on soft references..

**8. dependent or orphan sweep wider than the change** (n=14, 0 won, 2 lost). Agents (with and without the skill) sweep every row with no links after the delete, taking rows that never had links or are still served by a row that stays. Register: RP-31.

**9. flag that is right or half right** (n=36, 1 won, 2 lost). Bare agents almost always fix the true half and reject the false half; this class separates little. Register: RP-24, RP-03, RP-31, RP-07, RP-32, RP-12, RP-05, RP-04, RP-17, RP-08, RP-20.

**10. loader or upsert identity (merge key, replace vs upsert)** (n=8, 1 won, 0 lost). Bare agents MERGE on a key that is not the repo's identity (or on a nullable one), or upsert where the file is a full replacement. Register: RP-18, RP-07, RP-03, RP-21.

**11. per-transaction limit or what readers see mid-run** (n=5, 0 won, 0 lost). Bare agents batch by the wrong unit (input rows, not deleted entities) or commit pieces that leave readers seeing a half-moved state. Register: RP-04 (one case); reader-visible half states: none in the register, would be documented by an isolation-level manual page..

**12. derived or transitive data kept in step (closure, traversal)** (n=4, 0 won, 0 lost). Both arms got these right in every run; no failure to fix. Register: RP-14 for one case; otherwise none in the register; materialized-view and closure-table docs would document it..

**13. value conversion arithmetic (rounding, units, integer division)** (n=3, 0 won, 0 lost). Both arms got these right in every run; no failure to fix. Register: none in the register; the engines' arithmetic docs (integer division, CAST truncation) and ISO 4217 minor units would document it..

## Reading

- Production hand-back is where the skill earns most (10 of 10 baseline failures fixed, 7 wins), then wrong flags refuted by the code (6 of 6) and resumed backfills (4 of 6). Those three classes are mostly outside the register's outside evidence, which is why the RP-tagged subset shows little lift.
- The only class where the skill is behind is the dependent sweep (0 won, 2 lost): Claude Haiku with the skill failed 4 of 14 sweep cases, against 2 without it. See the change to SKILL.md step A2.
- Classification is one reader's judgment from expected_outcome text; borderline cases (for example a review whose answer is a fix by a doc rule) were put in the class of the trap, not of the framing.
