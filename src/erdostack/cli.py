"""erdostack installer: copies the bundled skills into an agent's skills directory.

It reads and writes local files only. No network access, no telemetry.
Keep the AGENTS table in sync with bin/erdostack.mjs.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

from . import __version__

REPO = "https://github.com/usergraphtheory/erdostack"

# Skills directory per agent, relative to the project root (project) or the home directory (global).
AGENTS = {
    "universal": {"project": ".agents/skills", "global": ".agents/skills"},
    "claude-code": {"project": ".claude/skills", "global": ".claude/skills"},
    "cursor": {"project": ".cursor/skills", "global": ".cursor/skills"},
    "gemini-cli": {"project": ".gemini/skills", "global": ".gemini/skills"},
    "opencode": {"project": ".opencode/skills", "global": ".config/opencode/skills"},
    "copilot": {"project": ".github/skills", "global": None},
}


def source_dir() -> Path:
    override = os.environ.get("ERDOSTACK_SKILLS_DIR")
    if override:
        return Path(override).resolve()
    package = Path(__file__).parent.resolve()
    bundled = package / "_bundle" / "skills"
    if bundled.is_dir():
        return bundled
    # Running from a source checkout: src/erdostack/cli.py -> <repo>/skills
    return package.parent.parent / "skills"


def bundled_skills() -> list[str]:
    directory = source_dir()
    if not directory.is_dir():
        return []
    return sorted(
        entry.name
        for entry in directory.iterdir()
        if entry.is_dir() and (entry / "SKILL.md").is_file()
    )


def describe(skill: str) -> str:
    text = (source_dir() / skill / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r"^description:\s*(.+)$", text, flags=re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip().strip("\"'")


def target_dir(args: argparse.Namespace) -> Path:
    if args.dest:
        return Path(args.dest).resolve()
    agent = AGENTS[args.agent]
    if args.global_:
        if not agent["global"]:
            sys.exit(
                f'erdostack: no known global skills directory for "{args.agent}". Pass --dest <dir> instead.'
            )
        return Path.home() / agent["global"]
    return Path(agent["project"]).resolve()


def cmd_list(_: argparse.Namespace) -> int:
    skills = bundled_skills()
    if not skills:
        print(f"erdostack {__version__} bundles no skills yet. Roadmap: {REPO}/blob/main/ROADMAP.md")
        return 0
    for skill in skills:
        description = describe(skill)
        print(f"{skill}  {description}" if description else skill)
    return 0


def cmd_path(_: argparse.Namespace) -> int:
    print(source_dir())
    return 0


def cmd_install(args: argparse.Namespace) -> int:
    available = bundled_skills()
    if not available:
        print(f"erdostack {__version__} bundles no skills yet, so there is nothing to install.")
        print(f"Roadmap: {REPO}/blob/main/ROADMAP.md")
        return 0
    wanted = args.skills or available
    unknown = [skill for skill in wanted if skill not in available]
    if unknown:
        sys.exit(f'erdostack: unknown skill(s): {", ".join(unknown)}. Run "erdostack list".')

    target = target_dir(args)
    copied = 0
    for skill in wanted:
        destination = target / skill
        if destination.exists() and not args.force:
            print(f"skip  {skill} (already in {target}; use --force to replace)")
            continue
        if args.dry_run:
            print(f"would copy  {skill} -> {destination}")
            continue
        target.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source_dir() / skill, destination)
        print(f"copied  {skill} -> {destination}")
        copied += 1
    if not args.dry_run:
        print(f"{copied} skill(s) installed from erdostack {__version__}.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="erdostack",
        description="Graph skills for coding agents.",
        epilog=f"This tool only copies files. It makes no network requests and collects nothing. {REPO}",
    )
    parser.add_argument("-v", "--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command")

    commands.add_parser("list", help="list the bundled skills").set_defaults(run=cmd_list)
    commands.add_parser("path", help="print the directory that holds the bundled skills").set_defaults(run=cmd_path)

    install = commands.add_parser(
        "install", aliases=["add"], help="copy skills into an agent's skills directory (default: all)"
    )
    install.add_argument("skills", nargs="*", help="skill names; omit to install every bundled skill")
    install.add_argument(
        "-a",
        "--agent",
        choices=sorted(AGENTS),
        default="universal",
        help="target agent (default: universal, which writes to .agents/skills)",
    )
    install.add_argument(
        "-g",
        "--global",
        dest="global_",
        action="store_true",
        help="install for the current user instead of the current project",
    )
    install.add_argument("-d", "--dest", help="write to this directory instead (overrides --agent and --global)")
    install.add_argument("-f", "--force", action="store_true", help="replace skills that are already installed")
    install.add_argument("--dry-run", action="store_true", help="show what would be copied without writing anything")
    install.set_defaults(run=cmd_install)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "run", None):
        parser.print_help()
        return 0
    return args.run(args)


if __name__ == "__main__":
    sys.exit(main())
