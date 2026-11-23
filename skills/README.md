# skills/

One folder per skill, each with a `SKILL.md` whose `name` matches the folder:

```text
skills/
└── roast-my-graph/
    ├── SKILL.md        # frontmatter (name, description) and a short, procedural body
    ├── references/     # optional: longer material the agent loads on demand
    └── scripts/        # optional: helper scripts
```

No skill has shipped yet. The planned set and its order are in the [roadmap](../ROADMAP.md).

Every host reads this directory directly: the skills CLI, `gh skill`, the Claude Code, Cursor, Codex and Copilot plugins, the Gemini CLI extension, and the npm and PyPI packages. Nothing is generated or copied per host.

To add a skill, start from [`templates/SKILL.template.md`](../templates/SKILL.template.md) and read [CONTRIBUTING.md](../CONTRIBUTING.md). Run `npm run check` before you open a pull request.
