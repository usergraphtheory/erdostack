#!/usr/bin/env python3
"""erdostack eval harness. Standard library only, no network.

A case lives at evals/<skill>/<set>/<case>/ (set is "dev" or "heldout"):

    prompt.md        the request exactly as a user would type it
    case.yaml        name and expected outcome (human-readable); may open with a canary comment, see `index`
    files/           copied into the agent's working directory (optional)
    setup.py         run as `python3 setup.py <work_dir>` after the copy (optional)
    check.py         the grader: `python3 check.py <run_dir>` prints JSON on stdout
    selfcheck/       good/ and bad-*/ outputs that prove the grader can pass and fail
    empty-dirs.txt   directories under files/ that must exist but hold nothing (git drops them); optional,
                     and a selfcheck variant may carry one of its own
    stage2/          optional second request in a fresh checkout: prompt.md and strip.txt (see `advance`)

A run directory holds one attempt at one case by one arm ("baseline" has no skill,
"skill" has skills/<skill>/ installed) on one model:

    <root>/r/<opaque id>/      (the id hides the case, skill and arm from the agent)
        work/          the agent's working directory
        prompt.txt     the full prompt handed to the runner
        final.md       the agent's closing message to the user
        meta.json      case, arm, model, run, skill version hash
        timing.json    tokens and duration, when the runner reports them
        grading.json   written by `grade`

A published run is the same attempt stored for readers: the files the agent created or changed, laid over
the freshly built case again when it is graded (see `export` and `regrade`):

    <dir>/<case>/<arm>-<model>/
        run.json         case, arm, model, skill version hash, tokens and duration
        final.md         the agent's closing message (final.stage1.md too, for a two-session case)
        grading.json     every assertion's grade as recorded, with the grader's evidence
        work/            files the agent created or changed
        removed.txt      files and directories the agent removed, relative to this folder
        empty-dirs.txt   directories the agent left empty
        omitted.json     changed files that are not published (not text, or large); such a run cannot be re-graded

Subcommands: prepare, advance, runs, grade, selftest, judge-pack, judge-apply, timing, report, summary, index, export,
regrade, run. See evals/README.md for the workflow.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time
from math import comb, sqrt
from pathlib import Path
from statistics import median

ROOT = Path(os.environ.get("ERDO_REPO") or Path(__file__).resolve().parents[2])  # ERDO_REPO is for tests
EVALS = ROOT / "evals"
SKILLS = ROOT / "skills"
SETS = ("dev", "heldout", "handoff", "standards")  # "handoff": a second held-out set, for two-stage cases; "standards": see evals/STANDARDS.md
ARMS = ("baseline", "skill")

RUNNER_PROMPT = """You are a coding agent. Your working directory for this task is:
{work}

Do all of your work inside that directory. Do not read or write anything outside it; other directories on this machine belong to other tasks. There is no network access and nothing can be installed, so use only what is already on the machine.
{skill_block}
The user's request:
---
{prompt}
---

When you are finished, write the message you would send back to the user to {run_dir}/final.md (that one file outside the working directory is allowed). Then reply with only the word DONE.
"""

SKILL_BLOCK = """
An agent skill named `{skill}` is installed at {work}/.agents/skills/{skill}/SKILL.md and applies to this request. Read that file first, then follow it while you do the task. Read the files it points to only when it tells you to.
"""


# --- statistics ----------------------------------------------------------------

def wilson(passes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """95% Wilson score interval for a pass rate."""
    if n == 0:
        return (0.0, 1.0)
    p = passes / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def sign_test(b_wins: int, a_wins: int) -> float:
    """Two-sided exact sign test on the cases where the two arms disagree."""
    n = b_wins + a_wins
    if n == 0:
        return 1.0
    k = max(b_wins, a_wins)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n)


# --- cases ---------------------------------------------------------------------

def case_dirs(skill: str, set_name: str, only: str | None = None) -> list[Path]:
    base = EVALS / skill / set_name
    if not base.is_dir():
        return []
    dirs = sorted(p for p in base.iterdir() if p.is_dir() and (p / "prompt.md").exists())
    return [p for p in dirs if only in (None, p.name)]


def read_prompt(case: Path) -> str:
    text = (case / "prompt.md").read_text(encoding="utf-8")
    if text.startswith("---\n"):  # optional settings block, used by other runners
        end = text.find("\n---\n", 4)
        if end != -1:
            text = text[end + 5:]
    return text.strip()


def skill_hash(skill: str) -> str:
    """Short content hash of skills/<skill>/, so a result can be tied to a version."""
    base = SKILLS / skill
    if not base.is_dir():
        return "none"
    digest = hashlib.sha256()
    for path in sorted(p for p in base.rglob("*") if p.is_file()):
        digest.update(str(path.relative_to(base)).encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()[:12]


EMPTY_DIRS = "empty-dirs.txt"  # git carries no empty directories: a case or a selfcheck variant lists the ones it needs


def make_listed_dirs(listing: Path, base: Path) -> None:
    """Create the directories named in an empty-dirs.txt (one relative path per line) under base."""
    if not listing.is_file():
        return
    for line in listing.read_text(encoding="utf-8").splitlines():
        rel = Path(line.strip())
        if not line.strip():
            continue
        if rel.is_absolute() or ".." in rel.parts:
            raise SystemExit(f"{listing}: {line.strip()!r} must be a relative path inside the case")
        (base / rel).mkdir(parents=True, exist_ok=True)


def overlay(variant: Path, run_dir: Path) -> None:
    """Lay a selfcheck variant (work/ files, final.md, labels) over a prepared run directory."""
    shutil.copytree(variant, run_dir, dirs_exist_ok=True)
    make_listed_dirs(variant / EMPTY_DIRS, run_dir)
    (run_dir / EMPTY_DIRS).unlink(missing_ok=True)


def materialize(case: Path, work: Path) -> None:
    """Copy the case's input files into work/ and run its optional setup script."""
    work.mkdir(parents=True, exist_ok=True)
    files = case / "files"
    if files.is_dir():
        shutil.copytree(files, work, dirs_exist_ok=True)
    make_listed_dirs(case / EMPTY_DIRS, work)
    setup = case / "setup.py"
    if setup.exists():
        subprocess.run([sys.executable, str(setup), str(work)], check=True, cwd=case)


def install_skill(skill: str, work: Path) -> None:
    src = SKILLS / skill
    if not (src / "SKILL.md").exists():
        raise SystemExit(f"skills/{skill}/SKILL.md does not exist; cannot prepare the skill arm")
    shutil.copytree(src, work / ".agents" / "skills" / skill, dirs_exist_ok=True)


def run_id(skill: str, set_name: str, case: str, arm: str, model: str, run: int) -> str:
    """Opaque, stable directory name for one run."""
    return hashlib.sha256(f"{skill}|{set_name}|{case}|{arm}|{model}|{run}".encode()).hexdigest()[:12]


def prepare_one(case: Path, skill: str, set_name: str, arm: str, model: str, run: int, root: Path) -> Path:
    # The path the agent sees must not name the case, the skill or the arm: a folder called
    # "readme-version-is-stale" or "baseline" would tell the agent what is being tested.
    run_dir = root / "r" / run_id(skill, set_name, case.name, arm, model, run)
    if run_dir.exists():
        shutil.rmtree(run_dir)
    work = run_dir / "work"
    materialize(case, work)
    if arm == "skill":
        install_skill(skill, work)
    block = SKILL_BLOCK.format(skill=skill, work=work) if arm == "skill" else ""
    prompt = RUNNER_PROMPT.format(work=work, run_dir=run_dir, skill_block=block, prompt=read_prompt(case))
    (run_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
    meta = {
        "skill": skill, "set": set_name, "case": case.name, "arm": arm, "model": model, "run": run,
        "skill_version": skill_hash(skill) if arm == "skill" else "none",
        "prepared_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (run_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return run_dir


def strip_untracked(stage2: Path, work: Path) -> None:
    strip = stage2 / "strip.txt"
    for pattern in strip.read_text().split() if strip.exists() else []:
        for path in sorted(work.glob(pattern), reverse=True):
            if ".agents" in path.parts:
                continue
            shutil.rmtree(path) if path.is_dir() else path.unlink()


def advance_one(run_dir: Path) -> bool:
    """Move a finished run to its case's second stage, if the case has one.

    A two-stage case models a later session in a fresh checkout: stage2/strip.txt lists glob patterns
    for things that are not under version control (a local database file, data dumps) and are removed;
    whatever the first session committed to the repo stays. The second request is stage2/prompt.md and is
    handled by a new agent with no memory of the first. check.py grades the state after stage two."""
    meta = json.loads((run_dir / "meta.json").read_text())
    stage2 = EVALS / meta["skill"] / meta["set"] / meta["case"] / "stage2"
    if not (stage2 / "prompt.md").exists() or meta.get("stage") == 2 or not (run_dir / "final.md").exists():
        return False
    work = run_dir / "work"
    (run_dir / "final.md").rename(run_dir / "final.stage1.md")
    (run_dir / "prompt.txt").rename(run_dir / "prompt.stage1.txt")
    strip_untracked(stage2, work)
    block = SKILL_BLOCK.format(skill=meta["skill"], work=work) if meta["arm"] == "skill" else ""
    text = (stage2 / "prompt.md").read_text(encoding="utf-8")
    if text.startswith("---\n") and "\n---\n" in text[4:]:
        text = text[text.find("\n---\n", 4) + 5:]
    (run_dir / "prompt.txt").write_text(
        RUNNER_PROMPT.format(work=work, run_dir=run_dir, skill_block=block, prompt=text.strip()), encoding="utf-8")
    meta["stage"] = 2
    (run_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return True


def cmd_advance(args) -> None:
    out = [{"run_dir": str(d), "prompt_file": str(d / "prompt.txt")}
           for d, _ in iter_runs(Path(args.root), args.skill, args.set) if advance_one(d)]
    print(json.dumps(out, indent=2))


def cmd_prepare(args) -> None:
    out = []
    for case in case_dirs(args.skill, args.set, args.case):
        for run in range(1, args.runs + 1):
            run_dir = prepare_one(case, args.skill, args.set, args.arm, args.model, run, Path(args.root))
            out.append({"run_dir": str(run_dir), "prompt_file": str(run_dir / "prompt.txt")})
    if not out:
        raise SystemExit(f"no cases found under evals/{args.skill}/{args.set}")
    print(json.dumps(out, indent=2))


# --- grading -------------------------------------------------------------------

def run_check(case: Path, run_dir: Path) -> dict:
    """Run a case's check.py on a run directory and normalise its JSON."""
    try:
        # check.py runs with the case folder as its working directory, so it must be handed an absolute path
        proc = subprocess.run([sys.executable, str(case / "check.py"), str(Path(run_dir).resolve())],
                              capture_output=True, text=True, timeout=300, cwd=case)
        data = json.loads(proc.stdout)
    except subprocess.TimeoutExpired:
        return {"error": "grader timed out", "assertions": []}
    except (json.JSONDecodeError, ValueError):
        return {"error": f"grader did not print JSON (exit {proc.returncode}): {proc.stderr[-400:]}", "assertions": []}
    for a in data.get("assertions", []):
        a.setdefault("kind", "substance")
        a.setdefault("evidence", "")
    return data


def summarise(assertions: list[dict]) -> dict:
    """A case passes when every substance assertion passed. Pending judge items leave it undecided."""
    sub = [a for a in assertions if a["kind"] == "substance"]
    con = [a for a in assertions if a["kind"] == "contract"]

    def verdict(items):
        if not items:
            return None
        if any(a["passed"] is False for a in items):
            return False
        if any(a["passed"] is None for a in items):
            return None
        return True
    return {"substance_pass": verdict(sub), "contract_pass": verdict(con),
            "substance_passed": sum(a["passed"] is True for a in sub), "substance_total": len(sub),
            "contract_passed": sum(a["passed"] is True for a in con), "contract_total": len(con)}


RUN_FILTER: int | None = None  # set by --only-run: restrict grade/judge/report to one run index (e.g. a re-gate of a revised skill)


def iter_runs(root: Path, skill: str | None = None, set_name: str | None = None):
    for meta_path in sorted(root.glob("r/*/meta.json")):
        meta = json.loads(meta_path.read_text())
        if skill and meta["skill"] != skill:
            continue
        if set_name and meta["set"] != set_name:
            continue
        if RUN_FILTER is not None and meta.get("run") != RUN_FILTER:
            continue
        if not (EVALS / meta["skill"] / meta["set"] / meta["case"]).is_dir():
            continue  # the case has left this set (e.g. a used held-out case moved to dev); saved reports keep its record
        yield meta_path.parent, meta


def cmd_grade(args) -> None:
    root = Path(args.root)
    counts = {"graded": 0, "missing_final": 0, "errors": 0, "pending_judge": 0}
    for run_dir, meta in iter_runs(root, args.skill, args.set):
        case = EVALS / meta["skill"] / meta["set"] / meta["case"]
        if (case / "stage2" / "prompt.md").exists() and meta.get("stage") != 2:
            counts["awaiting_stage2"] = counts.get("awaiting_stage2", 0) + 1
            continue
        previous = {}
        gpath = run_dir / "grading.json"
        if gpath.exists():  # keep judge verdicts already applied
            previous = {a["id"]: a for a in json.loads(gpath.read_text()).get("assertions", []) if a.get("judged")}
        data = run_check(case, run_dir)
        if not (run_dir / "final.md").exists():
            counts["missing_final"] += 1
        for a in data.get("assertions", []):
            if a["passed"] is None and a["id"] in previous:
                a.update({k: previous[a["id"]][k] for k in ("passed", "evidence", "judged")})
        data["summary"] = summarise(data.get("assertions", []))
        data["meta"] = meta
        gpath.write_text(json.dumps(data, indent=2), encoding="utf-8")
        counts["graded"] += 1
        counts["errors"] += 1 if data.get("error") else 0
        counts["pending_judge"] += sum(a["passed"] is None for a in data.get("assertions", []))
    print(json.dumps(counts))


def cmd_selftest(args) -> None:
    """Every grader must pass its known-good output and fail each known-bad one."""
    failures, checked = [], 0
    skills = [args.skill] if args.skill else sorted(p.name for p in EVALS.iterdir() if any((p / s).is_dir() for s in SETS))
    for skill in skills:
        for set_name in SETS:
            for case in case_dirs(skill, set_name):
                if getattr(args, "case", None) and case.name != args.case:
                    continue
                sc = case / "selfcheck"
                variants = sorted(p for p in sc.iterdir() if p.is_dir()) if sc.is_dir() else []
                if not any(v.name == "good" for v in variants) or not any(v.name.startswith("bad") for v in variants):
                    failures.append(f"{skill}/{set_name}/{case.name}: needs selfcheck/good and at least one selfcheck/bad-*")
                    continue
                for variant in variants:
                    with tempfile.TemporaryDirectory() as tmp:
                        run_dir = Path(tmp) / "run"
                        materialize(case, run_dir / "work")
                        strip_untracked(case / "stage2", run_dir / "work")  # no-op for one-stage cases
                        overlay(variant, run_dir)
                        data = run_check(case, run_dir)
                    checked += 1
                    where = f"{skill}/{set_name}/{case.name}/selfcheck/{variant.name}"
                    if data.get("error"):
                        failures.append(f"{where}: {data['error']}")
                        continue
                    script_sub = [a for a in data["assertions"] if a["kind"] == "substance" and a["passed"] is not None]
                    failed = [a["id"] for a in data["assertions"] if a["passed"] is False]
                    if variant.name == "good" or variant.name.startswith("good-"):
                        if failed:
                            failures.append(f"{where}: known-good output failed {failed}")
                    else:
                        expect_file = variant / "EXPECT_FAIL"
                        expect = expect_file.read_text().split() if expect_file.exists() else []
                        judge_only = expect and all(
                            any(a["id"] == e and a["passed"] is None for a in data["assertions"]) for e in expect)
                        if judge_only:
                            continue  # this variant exists to calibrate the judge, not the script
                        if not any(a["passed"] is False for a in script_sub):
                            failures.append(f"{where}: known-bad output passed every scripted substance assertion")
                        missing = [e for e in expect if e not in failed and not any(
                            a["id"] == e and a["passed"] is None for a in data["assertions"])]
                        if missing:
                            failures.append(f"{where}: expected {missing} to fail, failed {failed}")
    for line in failures:
        print("FAIL", line)
    print(json.dumps({"variants_checked": checked, "failures": len(failures)}))
    if not checked and not failures:
        sys.exit("no cases found under evals/: the case library is published in the erdostack/bench repository")
    sys.exit(1 if failures else 0)


# --- model-applied rubric items (the "judge") ----------------------------------

def read_material(run_dir: Path, names: list[str], limit: int = 12000) -> str:
    parts = []
    for name in names:
        path = run_dir / name
        if path.is_file():
            parts.append(f"=== {name} ===\n{path.read_text(encoding='utf-8', errors='replace')[:limit]}")
        else:
            parts.append(f"=== {name} === (file was not produced)")
    return "\n\n".join(parts)


def cmd_judge_pack(args) -> None:
    """Collect undecided rubric items into blind batches; the arm is never shown to the judge.

    Calibration items come from selfcheck variants that carry JUDGE_LABELS.json
    ({"assertion-id": true|false}); they measure how often the judge agrees with the labels."""
    root, out = Path(args.root), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)
    items, key = [], {}

    def add(question, material, ref):
        item_id = f"i{len(key):04d}"
        key[item_id] = ref
        items.append({"id": item_id, "question": question, "material": material})

    for run_dir, meta in iter_runs(root, args.skill, args.set):
        gpath = run_dir / "grading.json"
        if not gpath.exists():
            continue
        for a in json.loads(gpath.read_text()).get("assertions", []):
            if a["passed"] is None and a.get("judge"):
                add(a["judge"]["question"], read_material(run_dir, a["judge"].get("material", ["final.md"])),
                    {"type": "run", "run_dir": str(run_dir), "assertion": a["id"]})
    for set_name in () if args.no_calibration else SETS:
        for case in case_dirs(args.skill, set_name):
            sc = case / "selfcheck"
            for variant in sorted(p for p in sc.iterdir() if p.is_dir()) if sc.is_dir() else []:
                labels_file = variant / "JUDGE_LABELS.json"
                if not labels_file.exists():
                    continue
                labels = json.loads(labels_file.read_text())
                with tempfile.TemporaryDirectory() as tmp:
                    run_dir = Path(tmp) / "run"
                    materialize(case, run_dir / "work")
                    overlay(variant, run_dir)
                    for a in run_check(case, run_dir).get("assertions", []):
                        if a.get("judge") and a["id"] in labels:
                            add(a["judge"]["question"], read_material(run_dir, a["judge"].get("material", ["final.md"])),
                                {"type": "calibration", "case": f"{set_name}/{case.name}/{variant.name}",
                                 "assertion": a["id"], "label": labels[a["id"]]})
    order = list(range(len(items)))
    rng.shuffle(order)
    items = [items[i] for i in order]
    batches = [items[i:i + args.batch_size] for i in range(0, len(items), args.batch_size)]
    for n, batch in enumerate(batches, 1):
        (out / f"batch-{n:02d}.json").write_text(json.dumps(batch, indent=2), encoding="utf-8")
    (out / "KEY.json").write_text(json.dumps(key, indent=2), encoding="utf-8")
    print(json.dumps({"items": len(items), "batches": len(batches), "dir": str(out)}))


def cmd_judge_apply(args) -> None:
    """Merge the judge's answers (answers-*.json: [{"id", "answer": true|false, "evidence"}]) into grading.json."""
    out = Path(args.out)
    key = json.loads((out / "KEY.json").read_text())
    answers = {}
    for path in sorted(out.glob("answers-*.json")):
        for row in json.loads(path.read_text()):
            answers[row["id"]] = row
    applied, agree, calib, touched = 0, 0, 0, {}
    for item_id, ref in key.items():
        row = answers.get(item_id)
        if row is None or not isinstance(row.get("answer"), bool):
            continue
        if ref["type"] == "calibration":
            calib += 1
            agree += int(row["answer"] == ref["label"])
            continue
        gpath = Path(ref["run_dir"]) / "grading.json"
        data = touched.get(gpath) or json.loads(gpath.read_text())
        for a in data["assertions"]:
            if a["id"] == ref["assertion"]:
                a.update({"passed": row["answer"], "evidence": row.get("evidence", ""), "judged": True})
                applied += 1
        data["summary"] = summarise(data["assertions"])
        touched[gpath] = data
    for gpath, data in touched.items():
        gpath.write_text(json.dumps(data, indent=2), encoding="utf-8")
    result = {"applied": applied, "unanswered": len(key) - applied - calib,
              "calibration_items": calib, "calibration_agree": agree}
    (out / "judge-agreement.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result))


# --- cost ----------------------------------------------------------------------

def cmd_timing(args) -> None:
    """Record tokens and duration. Each entry is run_dir=tokens,duration_ms"""
    for entry in args.entries:
        run_dir, _, rest = entry.partition("=")
        tokens, _, ms = rest.partition(",")
        Path(run_dir, "timing.json").write_text(json.dumps(
            {"total_tokens": int(tokens), "duration_ms": int(ms), "total_duration_seconds": round(int(ms) / 1000, 1)}))
    print(json.dumps({"recorded": len(args.entries)}))


def cmd_runs(args) -> None:
    """List run directories with what they are (the directory names themselves are opaque)."""
    for run_dir, meta in iter_runs(Path(args.root), args.skill, args.set):
        state = "graded" if (run_dir / "grading.json").exists() else "ran" if (run_dir / "final.md").exists() else "prepared"
        print(f"{meta['skill']}\t{meta['set']}\t{meta['case']}\t{meta['arm']}\t{meta['model']}\tr{meta['run']}\t{state}\t{run_dir}")


# --- report --------------------------------------------------------------------

def load_results(root: Path, skill: str, set_name: str) -> list[dict]:
    rows = []
    for run_dir, meta in iter_runs(root, skill, set_name):
        gpath = run_dir / "grading.json"
        if not gpath.exists():
            continue
        data = json.loads(gpath.read_text())
        timing = json.loads((run_dir / "timing.json").read_text()) if (run_dir / "timing.json").exists() else {}
        rows.append({**meta, **data["summary"], "tokens": timing.get("total_tokens"),
                     "duration_ms": timing.get("duration_ms"), "error": data.get("error"),
                     "failed": [a["id"] for a in data["assertions"] if a["passed"] is False]})
    return rows


def rate(rows: list[dict], field: str) -> dict:
    decided = [r for r in rows if r[field] is not None]
    passes = sum(r[field] for r in decided)
    lo, hi = wilson(passes, len(decided))
    return {"passed": passes, "runs": len(decided), "rate": passes / len(decided) if decided else None,
            "ci95": [round(lo, 3), round(hi, 3)]}


def paired(rows: list[dict], models: list[str]) -> dict:
    """Per case, compare the number of passing runs in each arm (summed over the given models)."""
    score: dict[str, dict[str, list[bool]]] = {}
    for r in rows:
        if r["model"] in models and r["substance_pass"] is not None:
            score.setdefault(r["case"], {a: [] for a in ARMS})[r["arm"]].append(bool(r["substance_pass"]))
    skill_wins, base_wins, ties, regress = [], [], [], []
    for case, arms in sorted(score.items()):
        if not arms["baseline"] or not arms["skill"]:
            continue
        b = sum(arms["baseline"]) / len(arms["baseline"])
        s = sum(arms["skill"]) / len(arms["skill"])
        (skill_wins if s > b else base_wins if b > s else ties).append(case)
        if b == 1.0 and s == 0.0:
            regress.append(case)
    return {"skill_wins": skill_wins, "baseline_wins": base_wins, "ties": ties, "regressions": regress,
            "p": round(sign_test(len(skill_wins), len(base_wins)), 4)}


def build_report(root: Path, skill: str, set_name: str) -> dict:
    rows = load_results(root, skill, set_name)
    models = sorted({r["model"] for r in rows})
    report = {"skill": skill, "set": set_name, "models": models, "date": time.strftime("%Y-%m-%d", time.gmtime()),
              "skill_version": sorted({r["skill_version"] for r in rows if r["arm"] == "skill"}),
              "by_arm": {}, "by_arm_model": {}, "cost": {}, "cases": {}}
    for arm in ARMS:
        arm_rows = [r for r in rows if r["arm"] == arm]
        report["by_arm"][arm] = {"substance": rate(arm_rows, "substance_pass"), "contract": rate(arm_rows, "contract_pass")}
        tokens = [r["tokens"] for r in arm_rows if r["tokens"]]
        durations = [r["duration_ms"] for r in arm_rows if r["duration_ms"]]
        report["cost"][arm] = {"median_tokens": median(tokens) if tokens else None,
                               "median_seconds": round(median(durations) / 1000, 1) if durations else None,
                               "runs_with_timing": len(tokens)}
        for model in models:
            report["by_arm_model"][f"{arm}/{model}"] = rate([r for r in arm_rows if r["model"] == model], "substance_pass")
    report["paired_all_models"] = paired(rows, models)
    report["paired_by_model"] = {m: paired(rows, [m]) for m in models}
    for r in rows:
        cell = report["cases"].setdefault(r["case"], {})
        cell.setdefault(f"{r['arm']}/{r['model']}", []).append(
            "pass" if r["substance_pass"] else "undecided" if r["substance_pass"] is None else "FAIL:" + ",".join(r["failed"]))
    flaky = []
    for case, cells in report["cases"].items():
        for cell, outcomes in cells.items():
            kinds = {o.split(":")[0] for o in outcomes}
            if len(outcomes) > 1 and len(kinds) > 1:
                flaky.append(f"{case} [{cell}] {outcomes}")
    report["flaky"] = flaky
    report["grader_errors"] = [f"{r['case']}/{r['arm']}/{r['model']}: {r['error']}" for r in rows if r["error"]]
    return report


def fmt_rate(r: dict) -> str:
    if not r["runs"]:
        return "n/a"
    return f"{r['passed']}/{r['runs']} ({r['rate']:.0%}, 95% CI {r['ci95'][0]:.0%} to {r['ci95'][1]:.0%})"


def render(report: dict) -> str:
    p = report["paired_all_models"]
    lines = [f"## {report['skill']} / {report['set']} / {report['date']}", "",
             f"Models: {', '.join(report['models'])}. Skill version: {', '.join(report['skill_version']) or 'n/a'}.", "",
             "| Arm | Substance (case passes when every substance assertion passes) | Contract |", "|---|---|---|"]
    for arm in ARMS:
        lines.append(f"| {arm} | {fmt_rate(report['by_arm'][arm]['substance'])} | {fmt_rate(report['by_arm'][arm]['contract'])} |")
    lines += ["", "| Arm / model | Substance |", "|---|---|"]
    lines += [f"| {k} | {fmt_rate(v)} |" for k, v in report["by_arm_model"].items()]
    lines += ["", f"Paired by case, all models: skill better on {len(p['skill_wins'])}, baseline better on "
              f"{len(p['baseline_wins'])}, tied on {len(p['ties'])}; sign test p = {p['p']}."]
    for model, pm in report["paired_by_model"].items():
        lines.append(f"Paired by case, {model}: {len(pm['skill_wins'])} / {len(pm['baseline_wins'])} / {len(pm['ties'])} ties; p = {pm['p']}.")
    lines.append(f"Regressions (baseline always passed, skill never did): {', '.join(p['regressions']) or 'none'}.")
    cost = report["cost"]
    lines.append(f"Cost, median per run: baseline {cost['baseline']['median_tokens']} tokens / {cost['baseline']['median_seconds']} s; "
                 f"skill {cost['skill']['median_tokens']} tokens / {cost['skill']['median_seconds']} s.")
    lines.append(f"Flaky: {'; '.join(report['flaky']) or 'none observed'}.")
    if report["grader_errors"]:
        lines.append(f"Grader errors: {'; '.join(report['grader_errors'])}.")
    lines += ["", "| Case | " + " | ".join(report["by_arm_model"].keys()) + " |",
              "|---|" + "---|" * len(report["by_arm_model"])]
    for case, cells in sorted(report["cases"].items()):
        lines.append(f"| {case} | " + " | ".join("; ".join(cells.get(k, ["-"])) for k in report["by_arm_model"]) + " |")
    return "\n".join(lines) + "\n"


def cmd_report(args) -> None:
    report = build_report(Path(args.root), args.skill, args.set)
    text = render(report)
    if args.save:
        dest = EVALS / "results" / args.skill
        dest.mkdir(parents=True, exist_ok=True)
        stem = f"{report['date']}-{args.set}-{args.label}"
        (dest / f"{stem}.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        (dest / f"{stem}.md").write_text(text, encoding="utf-8")
    print(text)


# --- summary of saved reports ----------------------------------------------------

def fmt_p(p: float) -> str:
    """A p-value as a plain decimal: four places down to 0.001, two significant digits below that."""
    if p >= 0.001:
        return f"{p:.4f}".rstrip("0").rstrip(".") if p < 1 else "1"
    digits = 1
    while p < 10 ** -digits:
        digits += 1
    return f"{p:.{digits + 1}f}"


def summarise_report(report: dict) -> dict:
    """The numbers a gate is decided on, recomputed from a saved report (no run directory is read)."""
    paired_all = report["paired_all_models"]
    won, lost, tied = (len(paired_all[k]) for k in ("skill_wins", "baseline_wins", "ties"))
    cost = report.get("cost", {})

    def ratio(field: str):
        base, skill = (cost.get(arm, {}).get(field) for arm in ARMS)
        return round(skill / base, 2) if base and skill else None

    by_model = {}
    for model, pm in report.get("paired_by_model", {}).items():
        w, l = len(pm["skill_wins"]), len(pm["baseline_wins"])
        by_model[model] = {"won": w, "lost": l, "tied": len(pm["ties"]), "p": sign_test(w, l),
                           "with": report["by_arm_model"][f"skill/{model}"],
                           "without": report["by_arm_model"][f"baseline/{model}"]}
    return {"skill": report["skill"], "set": report["set"], "date": report["date"],
            "skill_version": report["skill_version"], "models": report["models"], "cases": won + lost + tied,
            "with": report["by_arm"]["skill"]["substance"], "without": report["by_arm"]["baseline"]["substance"],
            "won": won, "lost": lost, "tied": tied, "p": sign_test(won, lost),
            "regressions": paired_all["regressions"], "contract": report["by_arm"]["skill"]["contract"],
            "tokens_ratio": ratio("median_tokens"), "seconds_ratio": ratio("median_seconds"), "by_model": by_model}


def pool(summaries: list[dict]) -> dict:
    """One sign test over the cases of several reports: wins and losses add up, cases are never counted twice
    because each report covers its own skill and set."""
    won, lost, tied = (sum(s[k] for s in summaries) for k in ("won", "lost", "tied"))

    def total(arm: str) -> dict:
        passed, runs = (sum(s[arm][k] for s in summaries) for k in ("passed", "runs"))
        lo, hi = wilson(passed, runs)
        return {"passed": passed, "runs": runs, "rate": passed / runs if runs else None, "ci95": [round(lo, 3), round(hi, 3)]}

    return {"skill": "pooled", "set": "+".join(sorted({s["set"] for s in summaries})), "cases": won + lost + tied,
            "with": total("with"), "without": total("without"), "won": won, "lost": lost, "tied": tied,
            "p": sign_test(won, lost), "regressions": [r for s in summaries for r in s["regressions"]]}


def summary_row(s: dict) -> str:
    def cell(r: dict) -> str:
        return f"{r['passed']} / {r['runs']} ({r['ci95'][0]:.0%} to {r['ci95'][1]:.0%})" if r["runs"] else "n/a"

    def times(x) -> str:
        return f"{x}x" if x else "n/a"

    contract = s.get("contract")
    return (f"| `{s['skill']}` | {s['set']} | {', '.join(s.get('skill_version', [])) or '-'} | {s['cases']} | {cell(s['with'])} | "
            f"{cell(s['without'])} | {s['won']} / {s['lost']} / {s['tied']} | {fmt_p(s['p'])} | {len(s['regressions'])} | "
            f"{(str(contract['passed']) + ' / ' + str(contract['runs'])) if contract and contract['runs'] else '-'} | "
            f"{times(s.get('tokens_ratio'))} | {times(s.get('seconds_ratio'))} |")


def cmd_summary(args) -> None:
    """Print the deciding numbers of saved reports as one table; --pool adds one sign test over all their cases."""
    summaries = [summarise_report(json.loads(Path(f).read_text())) for f in args.reports]
    if args.pool:
        summaries.append(pool(summaries))
    if args.json:
        print(json.dumps(summaries, indent=2))
        return
    print("| Skill | Set | Version | Cases | Runs passed with the skill (95% interval) | Without | Won / lost / tied | p | Regressions | Contract | Tokens | Time |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for s in summaries:
        print(summary_row(s))
    if args.by_model:
        print("\n| Skill | Model | With the skill | Without | Won / lost / tied | p |\n|---|---|---|---|---|---|")
        for s in summaries:
            for model, m in s.get("by_model", {}).items():
                print(f"| `{s['skill']}` | {model} | {m['with']['passed']} / {m['with']['runs']} | "
                      f"{m['without']['passed']} / {m['without']['runs']} | {m['won']} / {m['lost']} / {m['tied']} | {fmt_p(m['p'])} |")


# --- index of cases ---------------------------------------------------------------

def read_case_yaml(path: Path) -> dict:
    """The top-level keys of a case.yaml: plain scalars, inline lists and block scalars. That is all the cases
    use, and it keeps the harness free of a YAML dependency. Anything else is returned as its raw text."""
    data: dict = {}
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        if not line or line[0] in " \t#-" or ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if value[:1] in ("|", ">"):  # block scalar: the indented lines that follow
            block = []
            while i < len(lines) and (not lines[i].strip() or lines[i][0] in " \t"):
                block.append(lines[i])
                i += 1
            indent = min((len(b) - len(b.lstrip()) for b in block if b.strip()), default=0)
            text = "\n".join(b[indent:] for b in block).strip("\n")
            data[key] = " ".join(text.split()) if value[0] == ">" else text
        elif value.startswith("[") and value.endswith("]"):
            data[key] = [v.strip().strip("'\"") for v in value[1:-1].split(",") if v.strip()]
        elif value:
            data[key] = value.strip("'\"") if value[0] in "'\"" and value[-1] == value[0] else value
        else:  # a nested mapping or list: keep its text
            block = []
            while i < len(lines) and (not lines[i].strip() or lines[i][0] in " \t-"):
                block.append(lines[i])
                i += 1
            data[key] = "\n".join(block).strip("\n")
    return data


def read_canary(case: Path) -> str | None:
    """A case's canary line, if it has one: a comment in case.yaml asking that the file be kept out of training
    data. Anything built from the case (an index row, a published run) carries it along."""
    path = case / "case.yaml"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("#") and "canary GUID" in line:
                return line.lstrip("#").strip()
    return None


def cmd_index(args) -> None:
    """One JSON line per case: what it asks, what it stages and where it is. Written for readers and for tools
    that want the library as a table (the dataset viewer on a model hub, a spreadsheet, a script). `sources` is
    what the case names in its case.yaml; for an older case with none, the register entries a reviewer tagged
    it with afterwards (evals/provenance.json)."""
    tagged = json.loads((EVALS / "provenance.json").read_text(encoding="utf-8")) if (EVALS / "provenance.json").exists() else {}
    rows = []
    for skill_dir in sorted(p for p in EVALS.iterdir() if p.is_dir()):
        for set_name in SETS:
            for case in case_dirs(skill_dir.name, set_name):
                meta = read_case_yaml(case / "case.yaml") if (case / "case.yaml").exists() else {}
                stage2 = case / "stage2" / "prompt.md"
                second = None
                if stage2.exists():
                    second = stage2.read_text(encoding="utf-8")
                    if second.startswith("---\n") and "\n---\n" in second[4:]:
                        second = second[second.find("\n---\n", 4) + 5:]
                    second = second.strip()
                sc = case / "selfcheck"
                rows.append({
                    "id": f"{skill_dir.name}/{set_name}/{case.name}", "skill": skill_dir.name, "set": set_name,
                    "case": case.name, "sessions": 2 if second is not None else 1,
                    "sources": (meta.get("sources") if isinstance(meta.get("sources"), list) else [])
                    or tagged.get(f"{skill_dir.name}/{case.name}", {}).get("rp", []),
                    "standard": meta.get("standard"), "kind": meta.get("trap_class") or meta.get("kind"),
                    "prompt": read_prompt(case), "second_prompt": second,
                    "expected_outcome": meta.get("expected_outcome"),
                    "selfcheck_variants": sum(1 for v in sc.iterdir() if v.is_dir()) if sc.is_dir() else 0,
                    "path": f"evals/{skill_dir.name}/{set_name}/{case.name}", "canary": read_canary(case)})
    text = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(json.dumps({"cases": len(rows), "out": args.out}))
    else:
        sys.stdout.write(text)


# --- published runs ---------------------------------------------------------------

PUBLISH_LIMIT = 256 * 1024  # a changed file that is larger than this, or is not text, is listed and not copied
CACHE_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
REMOVED = "removed.txt"
OMITTED = "omitted.json"
CLOSING = ("final.md", "final.stage1.md")


def locate_case(skill: str, set_name: str | None, case: str) -> Path | None:
    """The case folder: in the set named, or in the one set that holds it now (a used set moves to dev/)."""
    if set_name and (EVALS / skill / set_name / case).is_dir():
        return EVALS / skill / set_name / case
    hits = [EVALS / skill / s / case for s in SETS if (EVALS / skill / s / case).is_dir()]
    return hits[0] if len(hits) == 1 else None


def tree_state(base: Path) -> tuple[dict[str, tuple], set[str]]:
    """What is under base: {relative path: signature} for files and links, and the set of directories.
    Interpreter and test caches are left out; no grader reads them."""
    files: dict[str, tuple] = {}
    dirs: set[str] = set()
    for root, dnames, fnames in os.walk(base):
        rel_root = Path(root).relative_to(base)
        for d in list(dnames):
            if d in CACHE_DIRS:
                dnames.remove(d)
            elif (Path(root) / d).is_symlink():
                files[(rel_root / d).as_posix()] = ("link", os.readlink(Path(root) / d))
                dnames.remove(d)
            else:
                dirs.add((rel_root / d).as_posix())
        for f in fnames:
            path = Path(root) / f
            if f.endswith((".pyc", ".pyo")):
                continue
            if path.is_symlink():
                files[(rel_root / f).as_posix()] = ("link", os.readlink(path))
            elif path.is_file():
                files[(rel_root / f).as_posix()] = ("file", hashlib.sha256(path.read_bytes()).hexdigest(),
                                                    bool(path.stat().st_mode & 0o111))
    return files, dirs


def is_text(data: bytes) -> bool:
    if b"\0" in data:
        return False
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def export_one(run_dir: Path, meta: dict, case: Path, dest: Path, limit: int, extra: dict) -> dict:
    """Write one graded run to dest as an overlay on its freshly built case."""
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    here = str(run_dir.resolve())

    def clean(data: bytes) -> bytes:  # where the run was made says nothing about it
        return data.replace(here.encode(), b"/run")

    with tempfile.TemporaryDirectory() as raw:
        fresh = Path(raw) / "work"
        materialize(case, fresh)
        if meta["arm"] == "skill":
            install_skill(meta["skill"], fresh)
        was_files, was_dirs = tree_state(fresh)
    now_files, now_dirs = tree_state(run_dir / "work")
    omitted, copied = [], 0
    for rel, sig in sorted(now_files.items()):
        if was_files.get(rel) == sig:
            continue
        src, dst = run_dir / "work" / rel, dest / "work" / rel
        if sig[0] == "link":
            dst.parent.mkdir(parents=True, exist_ok=True)
            os.symlink(sig[1], dst)
            copied += 1
            continue
        data = src.read_bytes()
        if len(data) > limit or not is_text(data):
            omitted.append({"path": f"work/{rel}", "bytes": len(data), "sha256": sig[1],
                            "why": "over the size limit" if is_text(data) else "not text"})
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(clean(data))
        shutil.copymode(src, dst)
        copied += 1
    removed = sorted(f"work/{rel}" for rel in was_files if rel not in now_files)
    removed += sorted(f"work/{d}/" for d in was_dirs if d not in now_dirs)
    if removed:
        (dest / REMOVED).write_text("".join(line + "\n" for line in removed), encoding="utf-8")
    kept = set(now_files) - {o["path"][5:] for o in omitted}
    empty = sorted(d for d in now_dirs - was_dirs if not any(rel.startswith(d + "/") for rel in kept))
    if empty:
        (dest / EMPTY_DIRS).write_text("".join(f"work/{d}\n" for d in empty), encoding="utf-8")
    if omitted:
        (dest / OMITTED).write_text(json.dumps(omitted, indent=1) + "\n", encoding="utf-8")
    for name in CLOSING:
        if (run_dir / name).exists():
            (dest / name).write_bytes(clean((run_dir / name).read_bytes()))
    grading = json.loads((run_dir / "grading.json").read_text(encoding="utf-8"))
    grading.pop("meta", None)
    (dest / "grading.json").write_bytes(clean((json.dumps(grading, indent=1, ensure_ascii=False) + "\n").encode("utf-8")))
    timing = json.loads((run_dir / "timing.json").read_text()) if (run_dir / "timing.json").exists() else {}
    record = {"skill": meta["skill"], "set": meta["set"], "case": meta["case"], "arm": meta["arm"], "model": meta["model"],
              "run": meta.get("run", 1), "skill_version": meta.get("skill_version"), "sessions": 2 if meta.get("stage") == 2 else 1,
              "total_tokens": timing.get("total_tokens"), "duration_ms": timing.get("duration_ms"), **extra}
    if read_canary(case):
        record["canary"] = read_canary(case)
    (dest / "run.json").write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    return {"files": copied, "omitted": len(omitted), "removed": len(removed)}


def cmd_export(args) -> None:
    """Write graded runs as overlays that `regrade` can check: the runs behind one saved report, or every graded
    run of a skill and set. Changed files that are not text, or are over --max-bytes, are listed in omitted.json."""
    root, out = Path(args.root), Path(args.out).resolve()
    wanted, versions, extra = None, set(), {}
    skill, set_name = args.skill, args.set
    if args.report:
        report = json.loads(Path(args.report).read_text(encoding="utf-8"))
        skill, set_name = report["skill"], report["set"]
        wanted = {(case, cell) for case, cells in report["cases"].items() for cell in cells}
        versions = set(report.get("skill_version") or [])
        extra = {"report": Path(args.report).name}
    if not skill or not set_name:
        raise SystemExit("export needs --report, or both --skill and --set")
    counts = {"exported": 0, "complete": 0, "with_omitted_files": 0, "files": 0, "omitted_files": 0, "not_graded": 0, "case_not_found": 0}
    for meta_path in sorted(root.glob("r/*/meta.json")):
        meta = json.loads(meta_path.read_text())
        if meta["skill"] != skill or meta["set"] != set_name or (RUN_FILTER is not None and meta.get("run") != RUN_FILTER):
            continue
        if wanted is not None and ((meta["case"], f"{meta['arm']}/{meta['model']}") not in wanted
                                   or (meta["arm"] == "skill" and versions and meta.get("skill_version") not in versions)):
            continue
        run_dir = meta_path.parent
        case = locate_case(skill, set_name, meta["case"])
        if case is None or not (run_dir / "grading.json").exists():
            counts["case_not_found" if case is None else "not_graded"] += 1
            continue
        name = f"{meta['arm']}-{meta['model']}" + (f"-r{meta['run']}" if meta.get("run", 1) != 1 else "")
        stats = export_one(run_dir, meta, case, out / meta["case"] / name, args.max_bytes, extra)
        counts["exported"] += 1
        counts["complete" if not stats["omitted"] else "with_omitted_files"] += 1
        counts["files"] += stats["files"]
        counts["omitted_files"] += stats["omitted"]
    print(json.dumps(counts))


def lay_published(src: Path, run_dir: Path) -> None:
    """Turn a freshly built case into the state a published run left: removals first, then its files."""
    removed = (src / REMOVED).read_text(encoding="utf-8").splitlines() if (src / REMOVED).is_file() else []
    for line in removed:
        rel = line.strip()
        if not rel:
            continue
        if Path(rel).is_absolute() or ".." in Path(rel).parts or Path(rel).parts[0] != "work":
            raise SystemExit(f"{src / REMOVED}: {rel!r} must be a relative path under work/")
        target = run_dir / rel
        if rel.endswith("/") and target.is_dir() and not target.is_symlink():
            shutil.rmtree(target)
        elif target.is_symlink() or target.is_file():
            target.unlink()
    for root, dnames, fnames in os.walk(src / "work") if (src / "work").is_dir() else []:
        rel_root = Path(root).relative_to(src)
        (run_dir / rel_root).mkdir(parents=True, exist_ok=True)
        for name in list(dnames) + fnames:
            path, dst = Path(root) / name, run_dir / rel_root / name
            if path.is_symlink():
                if name in dnames:
                    dnames.remove(name)
                if dst.is_symlink() or dst.is_file():
                    dst.unlink()
                os.symlink(os.readlink(path), dst)
            elif path.is_file():
                if dst.is_symlink():
                    dst.unlink()
                shutil.copy2(path, dst)
    make_listed_dirs(src / EMPTY_DIRS, run_dir)
    for name in CLOSING:
        if (src / name).is_file():
            shutil.copy2(src / name, run_dir / name)


def cmd_regrade(args) -> None:
    """Build each published run again from its case and grade it: the graders in this checkout must give the
    grades recorded with the run. Runs with omitted files are counted and skipped. Graders can execute files a
    run contains, so only regrade runs you trust, or do it in a container."""
    counts = {"runs": 0, "reproduced": 0, "different": 0, "skipped_omitted_files": 0, "skipped_case_not_found": 0}
    different = []
    for record_path in sorted(Path(args.runs).rglob("run.json")):
        src = record_path.parent
        record = json.loads(record_path.read_text(encoding="utf-8"))
        if args.skill and record["skill"] != args.skill:
            continue
        counts["runs"] += 1
        case = locate_case(record["skill"], record.get("set"), record["case"])
        if (src / OMITTED).exists() or case is None:
            counts["skipped_omitted_files" if case is not None else "skipped_case_not_found"] += 1
            continue
        with tempfile.TemporaryDirectory() as raw:
            run_dir = Path(raw) / "run"
            materialize(case, run_dir / "work")
            if record["arm"] == "skill":
                install_skill(record["skill"], run_dir / "work")
            lay_published(src, run_dir)
            data = run_check(case, run_dir)
        recorded = json.loads((src / "grading.json").read_text(encoding="utf-8")).get("assertions", [])
        judged = {a["id"]: a["passed"] for a in recorded if a.get("judged")}  # a judge's verdict is kept as given
        was = {a["id"]: a["passed"] for a in recorded}
        now = {a["id"]: judged[a["id"]] if a["passed"] is None and a["id"] in judged else a["passed"] for a in data.get("assertions", [])}
        if was == now and not data.get("error"):
            counts["reproduced"] += 1
        else:
            counts["different"] += 1
            different.append({"run": src.relative_to(Path(args.runs)).as_posix(), "error": data.get("error"),
                              "assertions": {k: [was.get(k, "absent"), now.get(k, "absent")]
                                             for k in sorted(set(was) | set(now)) if was.get(k, "absent") != now.get(k, "absent")}})
    print(json.dumps({**counts, "differences": different}, indent=1))
    if different:
        sys.exit(1)


# --- optional headless runner ---------------------------------------------------

def cmd_run(args) -> None:
    """Run prepared directories with a headless agent CLI: the command receives the prompt on stdin.

    Example: erdo_eval.py run --root runs --skill query-review --cmd 'claude -p --model {model} --permission-mode acceptEdits'
    The recorded results in evals/results/ were produced with subagents handed prompt.txt directly."""
    for run_dir, meta in iter_runs(Path(args.root), args.skill, args.set):
        if (run_dir / "final.md").exists() and not args.force:
            continue
        cmd = args.cmd.format(model=meta["model"])
        start = time.time()
        with open(run_dir / "prompt.txt", encoding="utf-8") as prompt:
            proc = subprocess.run(cmd, shell=True, stdin=prompt, capture_output=True, text=True,
                                  cwd=run_dir / "work", timeout=args.timeout)
        (run_dir / "runner.log").write_text(proc.stdout + "\n--- stderr ---\n" + proc.stderr, encoding="utf-8")
        (run_dir / "timing.json").write_text(json.dumps({"total_tokens": None, "duration_ms": int((time.time() - start) * 1000)}))
        print(f"{run_dir.relative_to(args.root)} exit={proc.returncode}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    def common(p, need_skill=True):
        p.add_argument("--root", default=os.environ.get("ERDO_RUNS", "runs"), help="directory holding run directories")
        p.add_argument("--skill", required=need_skill)
        p.add_argument("--set", choices=SETS, default=None)
        p.add_argument("--only-run", type=int, default=None, help="look only at runs with this run index")

    p = sub.add_parser("prepare"); common(p)
    p.add_argument("--arm", choices=ARMS, required=True); p.add_argument("--model", required=True)
    p.add_argument("--runs", type=int, default=1); p.add_argument("--case", default=None)
    p.set_defaults(func=cmd_prepare)
    p = sub.add_parser("grade"); common(p, need_skill=False); p.set_defaults(func=cmd_grade)
    p = sub.add_parser("advance"); common(p, need_skill=False); p.set_defaults(func=cmd_advance)
    p = sub.add_parser("runs"); common(p, need_skill=False); p.set_defaults(func=cmd_runs)
    p = sub.add_parser("selftest"); p.add_argument("--skill", default=None)
    p.add_argument("--case", default=None, help="check only the case with this name"); p.set_defaults(func=cmd_selftest)
    p = sub.add_parser("judge-pack"); common(p); p.add_argument("--out", required=True)
    p.add_argument("--batch-size", type=int, default=12); p.add_argument("--seed", type=int, default=7)
    p.add_argument("--no-calibration", action="store_true", help="skip labelled calibration items (measure them once per judge)")
    p.set_defaults(func=cmd_judge_pack)
    p = sub.add_parser("judge-apply"); p.add_argument("--out", required=True); p.set_defaults(func=cmd_judge_apply)
    p = sub.add_parser("timing"); p.add_argument("entries", nargs="+"); p.set_defaults(func=cmd_timing)
    p = sub.add_parser("report"); common(p); p.add_argument("--save", action="store_true")
    p.add_argument("--label", default="run"); p.set_defaults(func=cmd_report)
    p = sub.add_parser("summary"); p.add_argument("reports", nargs="+", help="saved report .json files from evals/results/")
    p.add_argument("--pool", action="store_true", help="add one sign test over the cases of all the reports")
    p.add_argument("--by-model", action="store_true"); p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_summary)
    p = sub.add_parser("index"); p.add_argument("--out", default=None, help="write the JSON lines here instead of stdout")
    p.set_defaults(func=cmd_index)
    p = sub.add_parser("export"); common(p, need_skill=False); p.add_argument("--out", required=True)
    p.add_argument("--report", default=None, help="a saved report .json: export the runs behind it")
    p.add_argument("--max-bytes", type=int, default=PUBLISH_LIMIT, help="largest changed file that is copied")
    p.set_defaults(func=cmd_export)
    p = sub.add_parser("regrade"); p.add_argument("--runs", required=True, help="a folder of published runs")
    p.add_argument("--skill", default=None); p.set_defaults(func=cmd_regrade)
    p = sub.add_parser("run"); common(p, need_skill=False); p.add_argument("--cmd", required=True)
    p.add_argument("--timeout", type=int, default=1200); p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_run)
    args = parser.parse_args()
    if getattr(args, "root", None):
        args.root = str(Path(args.root).resolve())  # setup.py and check.py run from the case folder
    global RUN_FILTER
    RUN_FILTER = getattr(args, "only_run", None)
    if args.command in ("prepare", "report", "judge-pack") and args.set is None:
        parser.error("--set is required for this command")
    args.func(args)


if __name__ == "__main__":
    main()
