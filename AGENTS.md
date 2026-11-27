# Working in this repository

This repo packages Agent Skills about graphs for many agent hosts. The skills are plain markdown; everything else is thin packaging around them.

## Layout

- `skills/<name>/SKILL.md`: the skills. One folder each, `name` equal to the folder name.
- `references/engines/<engine>.md`: engine packs. Each needs a `Last verified: YYYY-MM-DD` line.
- `evals/`: eval cases and the harness.
- `templates/`: starting points for a new skill or engine pack. Named `*.template.md` so installers do not mistake them for skills.
- `plugin.json`, `.claude-plugin/`, `.cursor-plugin/`, `.codex-plugin/`, `.agents/plugins/`, `gemini-extension.json`: host manifests. They all point at the same `skills/` directory.
- `bin/erdostack.mjs` and `src/erdostack/`: the npm and PyPI installers. They only copy files, and their `AGENTS` tables must stay identical.
- `scripts/validate.mjs`: the single source of truth for what is valid here.
- `assets/`: the logo, share image and profile pictures, in the same chalkboard identity as erdostack.com. `assets/README.md` has the palette, the typeface and the rules for the mark.

## Rules

- Run `npm run check` before finishing any change. It must pass.
- Never edit a version by hand. `node scripts/sync-version.mjs X.Y.Z` updates every manifest together, and only for a release.
- Keep skill bodies short and procedural. Long material goes in a `references/` folder.
- Quote any frontmatter value that contains a colon.
- Every claim about a database engine needs a version and a date.
- Public datasets only. Never add schemas, queries, hostnames or data from a private or employer project.
- Nothing shipped from here may make network calls or collect data.
- Do not add dependencies to `package.json` or `pyproject.toml`. The installers and scripts are dependency-free on purpose.
- Do not add a file named `SKILL.md` outside `skills/<name>/`.

See `CONTRIBUTING.md` for the bar a new skill has to clear and `docs/RELEASING.md` for how releases work.
