# Installing erdostack

Every install path delivers the same markdown from `skills/`. Five skills are there now: `roast-my-graph`, `graph-or-not`, `setup-graph`, `schema-first` and `query-review`. The npm and PyPI packages carry the same five.

## Pick a model first

| | Subscribe | Own |
|---|---|---|
| How | Install as a plugin or extension | Copy the skill files into your project |
| Updates | Arrive when a new version is released | You pull them when you choose |
| Editing | Not intended; your edits are overwritten | The files are yours to change |
| Good for | Individuals who want the current set | Teams, pinned versions, heavy adaptation |

Choose one per project. With both, your agent sees every skill twice.

## Own: copy the files

### Skills CLI (any agent)

```bash
npx skills add usergraphtheory/erdostack              # choose skills and agents interactively
npx skills add usergraphtheory/erdostack --list       # look before installing
npx skills add usergraphtheory/erdostack --skill roast-my-graph -a claude-code
```

The skills CLI is a third-party tool. It sends anonymous install telemetry unless you set `DISABLE_TELEMETRY=1`.

### GitHub CLI

```bash
gh skill install usergraphtheory/erdostack                    # browse and choose
gh skill install usergraphtheory/erdostack roast-my-graph     # one skill
gh skill install usergraphtheory/erdostack roast-my-graph --pin v0.1.0   # pin to a release tag
```

### npm

```bash
npx erdostack list
npx erdostack install                         # every skill, into .agents/skills
npx erdostack install roast-my-graph -a claude-code
npx erdostack@0.1.0 install                   # pin a version
```

### PyPI

```bash
uvx erdostack list
uvx erdostack install                         # every skill, into .agents/skills
pipx run erdostack install -a cursor
uvx erdostack@0.1.0 install                   # pin a version
```

The npm and PyPI installers behave identically. They copy files, make no network requests and collect nothing.

| Option | Effect |
|---|---|
| `-a, --agent <name>` | `universal` (default), `claude-code`, `cursor`, `gemini-cli`, `opencode`, `copilot` |
| `-g, --global` | Install for your user instead of the current project |
| `-d, --dest <dir>` | Write to an explicit directory |
| `-f, --force` | Replace skills that are already installed |
| `--dry-run` | Show what would be copied |

Where each agent name writes:

| Agent | Project | Global |
|---|---|---|
| `universal` | `.agents/skills/` | `~/.agents/skills/` |
| `claude-code` | `.claude/skills/` | `~/.claude/skills/` |
| `cursor` | `.cursor/skills/` | `~/.cursor/skills/` |
| `gemini-cli` | `.gemini/skills/` | `~/.gemini/skills/` |
| `opencode` | `.opencode/skills/` | `~/.config/opencode/skills/` |
| `copilot` | `.github/skills/` | use `--dest` |

Most current agents also read `.agents/skills/`, which is why it is the default. For any agent not listed, pass `--dest`.

## Subscribe: install as a plugin

### Claude Code

```text
/plugin marketplace add usergraphtheory/erdostack
/plugin install erdostack@erdostack
```

### Codex

```bash
codex plugin marketplace add usergraphtheory/erdostack
codex plugin add erdostack@erdostack
```

### GitHub Copilot CLI

```bash
copilot plugin install usergraphtheory/erdostack
```

### Gemini CLI

```bash
gemini extensions install https://github.com/usergraphtheory/erdostack
gemini extensions install https://github.com/usergraphtheory/erdostack --ref v0.1.0   # pin
```

### Cursor

A Cursor Marketplace listing is a separate submission and review. Until it is listed, use the skills CLI with `-a cursor`, or `npx erdostack install -a cursor`.

## Teams

**Own.** Run an install in project scope and commit the result, for example `.agents/skills/`. Everyone who clones the repo has the skills, and changes go through code review like anything else.

**Subscribe (Claude Code).** Add the marketplace to the project's `.claude/settings.json` so teammates are offered the plugin when they trust the folder:

```json
{
  "extraKnownMarketplaces": {
    "erdostack": {
      "source": { "source": "github", "repo": "usergraphtheory/erdostack" }
    }
  },
  "enabledPlugins": {
    "erdostack@erdostack": true
  }
}
```

## Updating and removing

- **Plugins and extensions** update through the host: `/plugin` in Claude Code, `codex plugin`, `copilot plugin update erdostack`, `gemini extensions update erdostack`.
- **Skills CLI:** `npx skills update`. **GitHub CLI:** `gh skill update`.
- **npm and PyPI installers:** run `install --force` with the version you want.
- **Removing copied skills:** delete their folders from the skills directory. Nothing else is written anywhere.
