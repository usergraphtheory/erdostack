"""Tests for the eval harness. Run: python3 -m unittest discover -s evals/harness -p 'test_*.py'"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import erdo_eval  # noqa: E402

CHECK = '''import json, sys
from pathlib import Path
run = Path(sys.argv[1])
answer = (run / "work" / "answer.txt").read_text().strip() if (run / "work" / "answer.txt").exists() else ""
print(json.dumps({"assertions": [
    {"id": "answer-is-42", "text": "answer.txt holds 42", "kind": "substance", "passed": answer == "42", "evidence": answer},
    {"id": "polite", "text": "the reply is polite", "kind": "substance", "passed": None,
     "judge": {"question": "Is the reply polite?", "material": ["final.md"]}},
    {"id": "has-final", "text": "final.md exists", "kind": "contract", "passed": (run / "final.md").exists()},
]}))
'''


def make_repo(tmp: Path) -> None:
    case = tmp / "evals" / "toy" / "dev" / "adds-numbers"
    (case / "files").mkdir(parents=True)
    (case / "files" / "input.txt").write_text("40 + 2\n")
    (case / "prompt.md").write_text("---\ntags: [toy]\n---\n\nAdd the numbers in input.txt and write the result to answer.txt\n")
    (case / "case.yaml").write_text('schema_version: "1.1"\nname: adds-numbers\nexpected_outcome: |\n  answer.txt holds 42\n')
    (case / "check.py").write_text(CHECK)
    (case / "setup.py").write_text("import sys, pathlib\npathlib.Path(sys.argv[1], 'made-by-setup').write_text('x')\n")
    good, bad = case / "selfcheck" / "good", case / "selfcheck" / "bad-wrong-sum"
    (good / "work").mkdir(parents=True); (bad / "work").mkdir(parents=True)
    (good / "work" / "answer.txt").write_text("42"); (good / "final.md").write_text("Here you go, thanks!")
    (good / "JUDGE_LABELS.json").write_text('{"polite": true}')
    (bad / "work" / "answer.txt").write_text("41"); (bad / "EXPECT_FAIL").write_text("answer-is-42\n")
    skill = tmp / "skills" / "toy"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: toy\ndescription: toy\n---\nAdd carefully.\n")


def cli(tmp: Path, *args: str, cwd: Path | None = None) -> str:
    env = {**os.environ, "ERDO_REPO": str(tmp)}
    proc = subprocess.run([sys.executable, str(HERE / "erdo_eval.py"), *args], capture_output=True, text=True, env=env, cwd=cwd)
    if proc.returncode != 0:
        raise AssertionError(proc.stdout + proc.stderr)
    return proc.stdout


class Statistics(unittest.TestCase):
    def test_wilson_matches_known_values(self):
        lo, hi = erdo_eval.wilson(5, 5)
        self.assertAlmostEqual(lo, 0.566, places=3)
        self.assertEqual(hi, 1.0)
        lo, hi = erdo_eval.wilson(17, 20)
        self.assertAlmostEqual(lo, 0.640, places=3)
        self.assertAlmostEqual(hi, 0.948, places=3)
        self.assertEqual(erdo_eval.wilson(0, 0), (0.0, 1.0))

    def test_sign_test_matches_known_values(self):
        self.assertAlmostEqual(erdo_eval.sign_test(5, 0), 0.0625)
        self.assertAlmostEqual(erdo_eval.sign_test(6, 0), 0.03125)
        self.assertAlmostEqual(erdo_eval.sign_test(7, 1), 0.0703125)
        self.assertEqual(erdo_eval.sign_test(0, 0), 1.0)
        self.assertEqual(erdo_eval.sign_test(3, 3), 1.0)


class Summary(unittest.TestCase):
    REPORT = {"skill": "toy", "set": "dev", "date": "2026-01-01", "skill_version": ["abc"], "models": ["m1"],
              "by_arm": {"baseline": {"substance": {"passed": 1, "runs": 8, "rate": 0.125, "ci95": [0.022, 0.471]},
                                      "contract": {"passed": 0, "runs": 8, "rate": 0.0, "ci95": [0.0, 0.324]}},
                         "skill": {"substance": {"passed": 8, "runs": 8, "rate": 1.0, "ci95": [0.676, 1.0]},
                                   "contract": {"passed": 8, "runs": 8, "rate": 1.0, "ci95": [0.676, 1.0]}}},
              "by_arm_model": {"baseline/m1": {"passed": 1, "runs": 8}, "skill/m1": {"passed": 8, "runs": 8}},
              "cost": {"baseline": {"median_tokens": 1000, "median_seconds": 10.0}, "skill": {"median_tokens": 1250, "median_seconds": 15.0}},
              "paired_all_models": {"skill_wins": list("abcdefg"), "baseline_wins": [], "ties": ["h"], "regressions": [], "p": 0.0156},
              "paired_by_model": {"m1": {"skill_wins": list("abcdefg"), "baseline_wins": [], "ties": ["h"], "regressions": [], "p": 0.0156}}}

    def test_p_values_print_as_plain_decimals(self):
        self.assertEqual(erdo_eval.fmt_p(1.0), "1")
        self.assertEqual(erdo_eval.fmt_p(0.0625), "0.0625")
        self.assertEqual(erdo_eval.fmt_p(0.0127), "0.0127")
        self.assertEqual(erdo_eval.fmt_p(0.00098), "0.00098")
        self.assertEqual(erdo_eval.fmt_p(2 * 0.5 ** 18), "0.0000076")

    def test_summary_recomputes_the_exact_p_and_pools_reports(self):
        one = erdo_eval.summarise_report(self.REPORT)
        self.assertEqual((one["won"], one["lost"], one["tied"], one["cases"]), (7, 0, 1, 8))
        self.assertAlmostEqual(one["p"], 2 * 0.5 ** 7)
        self.assertEqual((one["tokens_ratio"], one["seconds_ratio"]), (1.25, 1.5))
        both = erdo_eval.pool([one, one])
        self.assertEqual((both["won"], both["lost"], both["cases"]), (14, 0, 16))
        self.assertAlmostEqual(both["p"], 2 * 0.5 ** 14)
        self.assertEqual((both["with"]["passed"], both["with"]["runs"]), (16, 16))

    def test_summary_command_prints_one_row_per_report(self):
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "r.json"
            path.write_text(json.dumps(self.REPORT))
            out = cli(Path(raw), "summary", str(path), str(path), "--pool")
            rows = [line for line in out.splitlines() if line.startswith("| `")]
            self.assertEqual(len(rows), 3)
            self.assertIn("| 14 / 0 / 2 | 0.00012 |", rows[2])


class EndToEnd(unittest.TestCase):
    def test_prepare_grade_judge_report(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            make_repo(tmp)
            runs = tmp / "runs"
            cli(tmp, "selftest", "--skill", "toy")
            base = json.loads(cli(tmp, "prepare", "--root", str(runs), "--skill", "toy", "--set", "dev", "--arm", "baseline", "--model", "m1"))
            with_skill = json.loads(cli(tmp, "prepare", "--root", str(runs), "--skill", "toy", "--set", "dev", "--arm", "skill", "--model", "m1"))
            b, s = Path(base[0]["run_dir"]), Path(with_skill[0]["run_dir"])
            self.assertTrue((b / "work" / "input.txt").exists() and (b / "work" / "made-by-setup").exists())
            self.assertFalse((b / "work" / ".agents").exists())
            self.assertTrue((s / "work" / ".agents" / "skills" / "toy" / "SKILL.md").exists())
            self.assertNotIn("agent skill", (b / "prompt.txt").read_text())
            self.assertIn("agent skill named `toy`", (s / "prompt.txt").read_text())
            self.assertIn("Add the numbers", (b / "prompt.txt").read_text())
            self.assertNotIn("tags:", (b / "prompt.txt").read_text())
            for leak in ("adds-numbers", "baseline", "toy/dev"):  # the path must not describe the test
                self.assertNotIn(leak, str(b))
            (b / "work" / "answer.txt").write_text("41"); (b / "final.md").write_text("done")
            (s / "work" / "answer.txt").write_text("42"); (s / "final.md").write_text("Done, thank you.")
            cli(tmp, "timing", f"{b}=1000,2000", f"{s}=1500,2500")
            counts = json.loads(cli(tmp, "grade", "--root", str(runs)))
            self.assertEqual(counts["graded"], 2)
            self.assertEqual(counts["pending_judge"], 2)
            judge = tmp / "judge"
            packed = json.loads(cli(tmp, "judge-pack", "--root", str(runs), "--skill", "toy", "--set", "dev", "--out", str(judge)))
            self.assertEqual(packed["items"], 3)  # two runs and one calibration item
            batch = json.loads((judge / "batch-01.json").read_text())
            self.assertFalse(any("baseline" in json.dumps(item) or str(runs) in json.dumps(item) for item in batch))
            (judge / "answers-01.json").write_text(json.dumps([{"id": item["id"], "answer": True, "evidence": "ok"} for item in batch]))
            applied = json.loads(cli(tmp, "judge-apply", "--out", str(judge)))
            self.assertEqual(applied, {"applied": 2, "unanswered": 0, "calibration_items": 1, "calibration_agree": 1})
            cli(tmp, "grade", "--root", str(runs))  # regrading keeps judge verdicts
            report = erdo_eval_report(tmp, runs)
            self.assertEqual(report["by_arm"]["baseline"]["substance"]["passed"], 0)
            self.assertEqual(report["by_arm"]["skill"]["substance"]["passed"], 1)
            self.assertEqual(report["paired_all_models"]["skill_wins"], ["adds-numbers"])
            self.assertEqual(report["cost"]["skill"]["median_tokens"], 1500)

    def test_a_relative_runs_directory_is_graded_like_an_absolute_one(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            make_repo(tmp)
            prepared = json.loads(cli(tmp, "prepare", "--root", "runs", "--skill", "toy", "--set", "dev", "--arm", "baseline", "--model", "m1", cwd=tmp))
            run = tmp / prepared[0]["run_dir"] if not Path(prepared[0]["run_dir"]).is_absolute() else Path(prepared[0]["run_dir"])
            (run / "work" / "answer.txt").write_text("42"); (run / "final.md").write_text("done")
            self.assertEqual(json.loads(cli(tmp, "grade", "--root", "runs", cwd=tmp))["graded"], 1)
            graded = json.loads((run / "grading.json").read_text())
            self.assertTrue(next(a for a in graded["assertions"] if a["id"] == "answer-is-42")["passed"])

    def test_selftest_rejects_a_grader_that_cannot_fail(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            make_repo(tmp)
            check = tmp / "evals" / "toy" / "dev" / "adds-numbers" / "check.py"
            check.write_text(check.read_text().replace('answer == "42"', "True"))
            env = {**os.environ, "ERDO_REPO": str(tmp)}
            proc = subprocess.run([sys.executable, str(HERE / "erdo_eval.py"), "selftest", "--skill", "toy"], capture_output=True, text=True, env=env)
            self.assertEqual(proc.returncode, 1)
            self.assertIn("known-bad output passed", proc.stdout)


class Index(unittest.TestCase):
    def test_case_yaml_reader_handles_scalars_lists_and_blocks(self):
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "case.yaml"
            path.write_text('schema_version: "1.1"\nname: a-case\nsources: [STD-01, RP-27]\nstandard: "IS 3"\n'
                            'expected_outcome: |\n  First line.\n    Indented: with a colon.\n\n  Last line.\nkind: build\n')
            got = erdo_eval.read_case_yaml(path)
            self.assertEqual(got["name"], "a-case")
            self.assertEqual(got["sources"], ["STD-01", "RP-27"])
            self.assertEqual(got["standard"], "IS 3")
            self.assertEqual(got["expected_outcome"], "First line.\n  Indented: with a colon.\n\nLast line.")
            self.assertEqual(got["kind"], "build")

    def test_index_lists_every_case_with_its_request(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            make_repo(tmp)
            case = tmp / "evals" / "toy" / "dev" / "adds-numbers"
            (case / "case.yaml").write_text('# KEEP OUT OF TRAINING DATA. toy canary GUID 0000\nname: adds-numbers\nsources: [RP-01]\n'
                                            'expected_outcome: |\n  answer.txt holds 42\n')
            (case / "stage2").mkdir()
            (case / "stage2" / "prompt.md").write_text("Now double it.\n")
            rows = [json.loads(line) for line in cli(tmp, "index").splitlines()]
            self.assertEqual(len(rows), 1)
            row = rows[0]
            self.assertEqual((row["id"], row["sessions"], row["sources"]), ("toy/dev/adds-numbers", 2, ["RP-01"]))
            self.assertIn("Add the numbers", row["prompt"])
            self.assertNotIn("tags:", row["prompt"])
            self.assertEqual(row["second_prompt"], "Now double it.")
            self.assertEqual(row["expected_outcome"], "answer.txt holds 42")
            self.assertEqual(row["selfcheck_variants"], 2)
            self.assertEqual(row["canary"], "KEEP OUT OF TRAINING DATA. toy canary GUID 0000")

            (tmp / "evals" / "provenance.json").write_text('{"toy/adds-numbers": {"pass": 1, "rp": ["RP-09"]}}')
            self.assertEqual(json.loads(cli(tmp, "index"))["sources"], ["RP-01"])  # what the case says wins
            (case / "case.yaml").write_text('name: adds-numbers\nexpected_outcome: |\n  answer.txt holds 42\n')
            self.assertEqual(json.loads(cli(tmp, "index"))["sources"], ["RP-09"])  # else the reviewer's tags


class PublishedRuns(unittest.TestCase):
    def prepared(self, tmp: Path) -> tuple[Path, Path, Path]:
        make_repo(tmp)
        (tmp / "evals" / "toy" / "dev" / "adds-numbers" / "files" / "notes").mkdir()
        (tmp / "evals" / "toy" / "dev" / "adds-numbers" / "files" / "notes" / "old.txt").write_text("stale\n")
        runs = tmp / "runs"
        dirs = {}
        for arm in erdo_eval.ARMS:
            out = json.loads(cli(tmp, "prepare", "--root", str(runs), "--skill", "toy", "--set", "dev", "--arm", arm, "--model", "m1"))
            dirs[arm] = Path(out[0]["run_dir"])
        base, skill = dirs["baseline"], dirs["skill"]
        (base / "work" / "answer.txt").write_text("42")
        (base / "work" / "notes" / "old.txt").unlink()
        (base / "work" / "notes").rmdir()
        (base / "work" / "scratch").mkdir()
        (base / "final.md").write_text(f"Done. I wrote {base}/work/answer.txt\n")
        (skill / "work" / "answer.txt").write_text("41")
        (skill / "work" / "dump.bin").write_bytes(b"\0\1\2")
        (skill / "final.md").write_text("Done.\n")
        cli(tmp, "grade", "--root", str(runs))
        return runs, base, skill

    def test_export_keeps_what_the_agent_changed_and_regrade_reproduces_the_grades(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            runs, base, _ = self.prepared(tmp)
            out = tmp / "published"
            counts = json.loads(cli(tmp, "export", "--root", str(runs), "--skill", "toy", "--set", "dev", "--out", str(out)))
            self.assertEqual((counts["exported"], counts["complete"], counts["with_omitted_files"]), (2, 1, 1))
            pub = out / "adds-numbers" / "baseline-m1"
            self.assertEqual(sorted(p.name for p in (pub / "work").iterdir()), ["answer.txt"])  # nothing the case already had
            self.assertEqual((pub / "removed.txt").read_text().split(), ["work/notes/old.txt", "work/notes/"])
            self.assertEqual((pub / "empty-dirs.txt").read_text().split(), ["work/scratch"])
            self.assertEqual((pub / "final.md").read_text(), "Done. I wrote /run/work/answer.txt\n")
            self.assertNotIn(str(base), (pub / "grading.json").read_text())
            self.assertNotIn("prepared_at", (pub / "run.json").read_text() + (pub / "grading.json").read_text())
            omitted = json.loads((out / "adds-numbers" / "skill-m1" / "omitted.json").read_text())
            self.assertEqual([(o["path"], o["bytes"], o["why"]) for o in omitted], [("work/dump.bin", 3, "not text")])
            result = json.loads(cli(tmp, "regrade", "--runs", str(out)))
            self.assertEqual((result["runs"], result["reproduced"], result["different"], result["skipped_omitted_files"]), (2, 1, 0, 1))

            (pub / "work" / "answer.txt").write_text("41")  # a published run that no longer earns its recorded grade
            env = {**os.environ, "ERDO_REPO": str(tmp)}
            proc = subprocess.run([sys.executable, str(HERE / "erdo_eval.py"), "regrade", "--runs", str(out)], capture_output=True, text=True, env=env)
            self.assertEqual(proc.returncode, 1)
            result = json.loads(proc.stdout)
            self.assertEqual(result["differences"][0]["assertions"], {"answer-is-42": [True, False]})

    def test_export_can_be_limited_to_the_runs_behind_a_saved_report(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            runs, _, _ = self.prepared(tmp)
            cli(tmp, "report", "--root", str(runs), "--skill", "toy", "--set", "dev", "--save", "--label", "t")
            report = next((tmp / "evals" / "results" / "toy").glob("*-dev-t.json"))
            data = json.loads(report.read_text())
            del data["cases"]["adds-numbers"]["skill/m1"]
            report.write_text(json.dumps(data))
            out = tmp / "published"
            counts = json.loads(cli(tmp, "export", "--root", str(runs), "--report", str(report), "--out", str(out)))
            self.assertEqual(counts["exported"], 1)
            self.assertEqual(json.loads((out / "adds-numbers" / "baseline-m1" / "run.json").read_text())["report"], report.name)

    def test_a_published_run_cannot_remove_anything_outside_its_working_directory(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            runs, _, _ = self.prepared(tmp)
            out = tmp / "published"
            cli(tmp, "export", "--root", str(runs), "--skill", "toy", "--set", "dev", "--out", str(out))
            (out / "adds-numbers" / "baseline-m1" / "removed.txt").write_text("../../outside.txt\n")
            with self.assertRaises(AssertionError) as caught:
                cli(tmp, "regrade", "--runs", str(out))
            self.assertIn("must be a relative path under work/", str(caught.exception))


class EmptyDirectories(unittest.TestCase):
    def test_listed_empty_directories_are_recreated_for_the_agent_and_for_selfcheck_variants(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            make_repo(tmp)
            case = tmp / "evals" / "toy" / "dev" / "adds-numbers"
            (case / "empty-dirs.txt").write_text("changes\ndata/incoming\n")
            check = case / "check.py"
            check.write_text(check.read_text().replace('answer == "42"', 'answer == "42" and (run / "work" / "changes").is_dir()'))
            (case / "selfcheck" / "good" / "empty-dirs.txt").write_text("work/docs/graph\n")
            cli(tmp, "selftest", "--skill", "toy")  # the grader now needs work/changes to exist
            prepared = json.loads(cli(tmp, "prepare", "--root", str(tmp / "runs"), "--skill", "toy", "--set", "dev", "--arm", "baseline", "--model", "m1"))
            work = Path(prepared[0]["run_dir"]) / "work"
            self.assertTrue((work / "changes").is_dir() and (work / "data" / "incoming").is_dir())
            run_dir = tmp / "variant-run"
            erdo_eval.overlay(case / "selfcheck" / "good", run_dir)
            self.assertTrue((run_dir / "work" / "docs" / "graph").is_dir())
            self.assertFalse((run_dir / "empty-dirs.txt").exists())

    def test_a_listed_directory_cannot_leave_the_case(self):
        with tempfile.TemporaryDirectory() as raw:
            listing = Path(raw) / "empty-dirs.txt"
            listing.write_text("../outside\n")
            with self.assertRaises(SystemExit):
                erdo_eval.make_listed_dirs(listing, Path(raw) / "work")


class Fixtures(unittest.TestCase):
    def test_no_case_file_is_hidden_by_an_ignore_rule(self):
        """A fixture repo may carry its own .gitignore, and git applies it to this repository too: a .env or a
        data file the case depends on would then never be committed. The same goes for a file an agent wrote in
        a recorded run. Such files have to be added with `git add -f`; this test fails while one is untracked."""
        repo = HERE.parents[1]
        try:
            inside = subprocess.run(["git", "-C", str(repo), "rev-parse", "--is-inside-work-tree"], capture_output=True, text=True)
        except FileNotFoundError:
            self.skipTest("git is not installed")
        if inside.returncode != 0 or inside.stdout.strip() != "true":
            self.skipTest("not a git checkout")
        listed = subprocess.run(["git", "-C", str(repo), "ls-files", "--others", "--ignored", "--exclude-standard", "--",
                                 "evals", "recorded-runs"], capture_output=True, text=True, check=True).stdout.splitlines()
        hidden = [p for p in listed if "__pycache__/" not in p and not p.endswith((".pyc", ".pyo"))]
        self.assertEqual(hidden, [], "ignored and untracked case files (add them with git add -f)")


class LfsPointers(unittest.TestCase):
    def test_no_stored_file_is_a_git_lfs_pointer(self):
        """A fixture may model a repository that keeps files in Git LFS, but the pointer files cannot be stored
        here: with no object behind them a git host refuses the push, and git-lfs stops a clone at checkout.
        A case writes such a file from its setup.py instead."""
        repo = HERE.parents[1]
        marker = b"version https://git-lfs.github.com/spec/v1"
        found = []
        for folder in ("evals", "recorded-runs"):
            for path in (repo / folder).rglob("*"):
                if "__pycache__" in path.parts or path.is_symlink() or not path.is_file() or path.stat().st_size >= 1024:
                    continue
                with path.open("rb") as handle:
                    if handle.read(len(marker)) == marker:
                        found.append(path.relative_to(repo).as_posix())
        self.assertEqual(found, [], "Git LFS pointer files (write them from the case's setup.py)")


class Canary(unittest.TestCase):
    def test_every_case_carries_the_same_canary_line_or_none_does(self):
        cases = [p.parent for p in erdo_eval.EVALS.glob("*/*/*/case.yaml") if p.parents[1].name in erdo_eval.SETS]
        found = {erdo_eval.read_canary(case) for case in cases}
        self.assertLessEqual(len(found), 1, "some cases carry a canary line and some do not, or two canaries are in use")
        for case in cases:
            if erdo_eval.read_canary(case):
                first = (case / "case.yaml").read_text(encoding="utf-8").splitlines()[0]
                self.assertTrue(first.startswith("#") and "canary GUID" in first, f"{case}: the canary is not the first line")


class HeadlessRunner(unittest.TestCase):
    AGENT = '''import pathlib, re, sys
prompt = sys.stdin.read()
run_dir = re.search(r"to (\\S+)/final\\.md", prompt).group(1)
pathlib.Path("answer.txt").write_text("42")  # the working directory is the case's work folder
pathlib.Path(run_dir, "final.md").write_text("done by " + sys.argv[1])
'''

    def test_run_pipes_each_prompt_to_the_command_and_skips_finished_runs(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            make_repo(tmp)
            runs = tmp / "runs"
            prepared = json.loads(cli(tmp, "prepare", "--root", str(runs), "--skill", "toy", "--set", "dev", "--arm", "baseline", "--model", "m1"))
            run = Path(prepared[0]["run_dir"])
            agent = tmp / "fake_agent.py"
            agent.write_text(self.AGENT)
            command = f"{sys.executable} {agent} {{model}}"
            first = cli(tmp, "run", "--root", str(runs), "--skill", "toy", "--cmd", command)
            self.assertIn("exit=0", first)
            self.assertEqual((run / "final.md").read_text(), "done by m1")
            self.assertGreaterEqual(json.loads((run / "timing.json").read_text())["duration_ms"], 0)
            self.assertEqual(cli(tmp, "run", "--root", str(runs), "--cmd", command).strip(), "")  # nothing left to run, any skill
            cli(tmp, "grade", "--root", str(runs))
            graded = json.loads((run / "grading.json").read_text())
            self.assertTrue(next(a for a in graded["assertions"] if a["id"] == "answer-is-42")["passed"])


class TwoStage(unittest.TestCase):
    def test_advance_strips_untracked_files_and_swaps_the_prompt(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp = Path(raw)
            make_repo(tmp)
            case = tmp / "evals" / "toy" / "dev" / "adds-numbers"
            (case / "stage2").mkdir()
            (case / "stage2" / "prompt.md").write_text("Now double the answer and write it to answer.txt\n")
            (case / "stage2" / "strip.txt").write_text("input.txt\n*.db\n")
            runs = tmp / "runs"
            prepared = json.loads(cli(tmp, "prepare", "--root", str(runs), "--skill", "toy", "--set", "dev", "--arm", "skill", "--model", "m1"))
            run = Path(prepared[0]["run_dir"])
            (run / "work" / "notes.md").write_text("committed by the first session")
            (run / "work" / "local.db").write_text("x")
            self.assertEqual(json.loads(cli(tmp, "advance", "--root", str(runs), "--skill", "toy")), [])  # stage one not finished
            (run / "final.md").write_text("stage one done")
            self.assertEqual(json.loads(cli(tmp, "grade", "--root", str(runs)))["awaiting_stage2"], 1)
            advanced = json.loads(cli(tmp, "advance", "--root", str(runs), "--skill", "toy"))
            self.assertEqual(len(advanced), 1)
            self.assertFalse((run / "work" / "input.txt").exists() or (run / "work" / "local.db").exists())
            self.assertTrue((run / "work" / "notes.md").exists())
            self.assertTrue((run / "work" / ".agents" / "skills" / "toy" / "SKILL.md").exists())
            self.assertIn("double the answer", (run / "prompt.txt").read_text())
            self.assertIn("agent skill named `toy`", (run / "prompt.txt").read_text())
            self.assertEqual((run / "final.stage1.md").read_text(), "stage one done")
            self.assertEqual(json.loads(cli(tmp, "advance", "--root", str(runs), "--skill", "toy")), [])  # only once


def erdo_eval_report(tmp: Path, runs: Path) -> dict:
    cli(tmp, "report", "--root", str(runs), "--skill", "toy", "--set", "dev", "--save", "--label", "t")
    saved = sorted((tmp / "evals" / "results" / "toy").glob("*.json"))
    return json.loads(saved[0].read_text())


if __name__ == "__main__":
    unittest.main()
