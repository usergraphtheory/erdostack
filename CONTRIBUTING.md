# Contributing to erdostack

Thanks for looking. Contributions are credited in the changelog, and small fixes are often finished and merged directly instead of bounced back with review comments.

## What helps most

1. **Engine packs.** If you maintain or work daily with a graph engine, a pack in `references/engines/` is the highest-value contribution. You must be able to test against the real engine.
2. **Agent failures.** A reproducible case where an agent got a graph task wrong, on a public dataset. Open an issue with the "Agent failure" template. These become eval cases.
3. **Eval cases** for an existing or planned skill, sent to [`erdostack/bench`](https://github.com/erdostack/bench).
4. **Skills.** Read the bar below first. A skill with no named failure behind it will not be merged.

## The bar for a skill

- It maps to a row in the README's failure table, or you can name a new failure people have actually hit.
- The author would reach for it at least weekly. Skills nobody uses get retired.
- It comes with at least one eval case showing the agent's behaviour with and without it. [`evals/README.md`](evals/README.md) has the case format and the rules; [`BENCHMARK.md`](BENCHMARK.md) shows what a result looks like, misses included. Cases live in [`erdostack/bench`](https://github.com/erdostack/bench): send the case there and link it from the skill's pull request.
- It works on more than one model. Do not lean on one model version's habits.

## House style

**Skills**

- One folder per skill: `skills/<name>/SKILL.md`, with `name` equal to the folder name. Start from [`templates/SKILL.template.md`](templates/SKILL.template.md).
- Frontmatter is plain `key: value` lines. Quote any value that contains a colon, or some installers silently skip the skill.
- Bodies are short and procedural, written as a briefing to a capable colleague. Research, tables and long explanations go in a `references/` folder, not in the body.
- Host-agnostic. No instructions that only work in one agent. Shell logic goes in scripts, not in the body.
- Say whether the skill is user-invoked or model-invoked, and what file it writes for the next skill to read.

**Engine packs**

- One file per engine: `references/engines/<engine>.md`. Start from [`templates/engine-pack.template.md`](templates/engine-pack.template.md).
- Every factual claim about an engine carries a version and a date, and the file has a `Last verified: YYYY-MM-DD` line. This is exactly the knowledge that goes stale.
- End with a pointer to the vendor's own skills or docs where they exist.
- Do not use naming that implies the vendor made or endorses the pack, unless you are the vendor and say so.

**Sources**

- Distill and cite. State the practice in your own words and link the source. Do not reproduce passages from books, papers or docs.
- Prefer official docs, standards and openly licensed material.
- No thresholds or benchmark numbers that you did not measure or cannot link.

**Data**

- Public datasets only. No schemas, queries, hostnames or data from an employer, a client or any private project.
- Nothing in a skill may surprise the person who installs it: no network calls, no data collection, no instructions that act against the user.

## Working in the repo

You need Node 20+ and, for the Python installer tests, Python 3.10+. There are no dependencies to install.

```bash
npm run check        # validate manifests and skills, then run the installer tests
npm run validate     # validation only
python3 -m unittest discover -s evals/harness -p 'test_*.py'   # eval harness tests
```

The validator checks every host manifest, version agreement, SKILL.md frontmatter against the [Agent Skills spec](https://agentskills.io/specification), and the `Last verified` line on engine packs. CI runs the same commands on Linux, macOS and Windows.

Do not bump versions in a pull request. Releases are cut by the maintainer; see [docs/RELEASING.md](docs/RELEASING.md).

## Pull requests

- Keep each PR to one skill, one pack or one fix.
- Fill in the checklist in the PR template.
- By contributing you agree that your work is released under the [MIT license](LICENSE).

## Ports and forks

Ports to other agents and forks that take the stack in a different direction are welcome. Keep the license and attribution intact, and open an issue if you would like yours linked from the README.
