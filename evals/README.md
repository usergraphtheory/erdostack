# evals/

Skills are tested the way code is tested: give an agent a task where it is tempted to get graphs wrong, run it with and without the skill, and keep the results. Every skill in `skills/` has a folder here, and no skill ships until a set it was never tuned against shows a lift over the no-skill baseline. The results are on one page in [`../BENCHMARK.md`](../BENCHMARK.md).

## Layout

```text
evals/
├── harness/erdo_eval.py     prepare, run, advance, grade, selftest, judge-pack, judge-apply, timing, report, summary, index, export, regrade
├── harness/test_harness.py  unit tests for the harness (statistics included)
├── REAL_PROBLEMS.md         register of documented graph problems that cases stage
├── STANDARDS.md             published benchmarks the standards track borrows from, its protocol and its result
├── PROVENANCE.md            how much of each skill's evidence rests on documented problems
├── <skill>/
│   ├── EVALS.md             correctness claim, thresholds, graders, every gate, results log, changelog
│   ├── SOURCES.md           outside facts the cases rely on, with the date each was checked
│   └── trigger.json         messages that should and should not load the skill
└── results/<skill>/         one dated report per recorded run (JSON and markdown), misses included
```

The cases themselves are not in this repository. All 1,527 of them, every `standards/`, `dev/`, `heldout/` and `handoff/` set that the `EVALS.md` files refer to, are in the companion repository [`erdostack/bench`](https://github.com/erdostack/bench), with their graders, a copy of this harness and the skills at the versions that were measured. A case library is large and its paths are long, and neither belongs in a repository people install from. What stays here is what a reader of the results needs: the claims, the protocols, the reports and the code that computes them.

A case is a folder: `prompt.md` (the request as a user would type it), `files/` (the repo the agent works in), an optional `setup.py` (builds databases so binaries are not committed), `check.py` (the grader) and `selfcheck/` (a known-good output and known-bad ones, so a grader that cannot fail is caught). A two-session case adds `stage2/`: a second request for a fresh session in the same checkout.

## How a result is produced

1. `prepare` copies a case into a fresh run directory whose path does not name the case, the skill or the arm. The `skill` arm also gets `skills/<skill>/` installed at `.agents/skills/<skill>/`; the `baseline` arm gets nothing. Apart from one sentence saying the skill applies, both arms receive the identical prompt.
2. A runner works in that directory and writes its closing message to `final.md`. The harness does not care which runner: `run` pipes `prompt.txt` to any headless agent command, or the prompt can be handed to an agent session. For two-session cases `advance` then swaps in the second request.
3. `grade` runs each case's `check.py`. Assertions are of two kinds:
   - **substance**: is the graph work right (the query runs and matches gold, the planted defect is found, the recorded version is the pinned one). A no-skill agent can pass these from the prompt and files alone. A case passes when every substance assertion passes.
   - **contract**: conventions only the skills define (file locations and formats). Reported separately. They never count toward lift.
4. Assertions a script cannot decide are packed into blind batches (`judge-pack`) for a model to answer yes or no, together with labelled calibration items that measure how often that judge agrees with the labels (`judge-apply` reports the agreement).
5. `report` gives pass rates with 95% Wilson intervals, and a paired sign test over cases: for each case, did the skill arm pass more often than the baseline arm. Counting cases, not runs, is deliberate: two models on one case are not two independent observations.
6. Before a result decides anything, every run with a failing script-graded assertion is re-read by a reviewer who is not told the arm. A disputed grader is repaired in general terms, with a known-good variant and a near miss that still fails, and the set is graded again. A bar has to hold on the grades as first produced and on the audited grades.
7. `summary` recomputes the deciding numbers from saved reports, with exact p-values, and `--pool` runs one sign test over the cases of several reports.
8. `export` writes what each agent created or changed as an overlay on its case, and `regrade` builds such a run again and checks that the graders give the grades recorded with it. The runs behind the five deciding gates and the core set are published that way, in `recorded-runs/` of the case repository.

Here, with nothing but Python:

```bash
python3 -m unittest discover -s evals/harness -p 'test_*.py'    # harness tests
python3 evals/harness/erdo_eval.py summary evals/results/roast-my-graph/*.json   # any published table, from the saved reports
```

In a checkout of `erdostack/bench`, where the cases are:

```bash
python3 evals/harness/erdo_eval.py selftest                      # every grader passes good and fails bad
python3 evals/harness/erdo_eval.py prepare --root runs --skill roast-my-graph --set standards --arm baseline --model sonnet
python3 evals/harness/erdo_eval.py prepare --root runs --skill roast-my-graph --set standards --arm skill --model sonnet
python3 evals/harness/erdo_eval.py run --root runs --cmd '<a headless agent command that reads the prompt on stdin>'
python3 evals/harness/erdo_eval.py grade --root runs
python3 evals/harness/erdo_eval.py report --root runs --skill roast-my-graph --set standards
```

The harness is standard library only. The cases need Python 3.10 or later with its bundled `sqlite3`, and NetworkX; the recorded runs used Python 3.13.18, SQLite 3.53.1 and NetworkX 3.7.

## Rules

- **The eval comes first.** A skill's claim, cases, graders and thresholds are written before the skill, and a gate's protocol and bar are written into `EVALS.md` before the run.
- **A used set is never used for a decision again.** Its cases count as seen and become development material; the next version needs fresh ones. Every set published so far has been used, the thirty-case `standards/` set included.
- **A miss is recorded and kept.** No bar is loosened after a run, and a near miss is a miss.
- **No cloud account and no network.** The cases recorded so far run on SQLite (graphs stored in SQL), NetworkX and static analysis of Cypher. They do not execute Cypher against a live Neo4j or LadybugDB; each skill's `EVALS.md` says so under "Not tested".
- **Public or generated data only.** No data, query text or example is copied from a source: cases name the register entry or standard they stage, in `case.yaml`. The `standards/` cases adapt a published schema and task statements under CC BY 4.0; `STANDARDS.md` has the attribution.
- **Every published number comes from a saved report.** Each report in `results/` names the date, the models and the skill version hash. Running the cases again needs `erdostack/bench`.
- **Fixtures are data.** A case has to reach a reader byte for byte as it was measured. In the case repository everything under `evals/` is tracked whatever an ignore rule says, line endings are left alone, and a case lists the empty directories its fixture needs in `empty-dirs.txt`, because git carries none; a grader that rebuilds the fixture has to create them too. A fixture repo with its own `.gitignore` can still hide a file: add such files with `git add -f`. A harness test fails while one is untracked. A fixture that models Git LFS writes its pointer files from `setup.py`: stored as files, a git host refuses the push and git-lfs stops a clone, each looking for an object that never existed. A harness test fails if one is stored.

If you have a reproducible case of an agent mishandling a graph task, open an issue with the "Agent failure" template. Those reports become cases.
