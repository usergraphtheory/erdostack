# Releasing

One tag publishes one version to every channel. The skills are the same markdown everywhere; a release only changes which commit each channel serves.

## Channels

| Channel | What users run | How a release reaches it |
|---|---|---|
| skills CLI and skills.sh | `npx skills add usergraphtheory/erdostack` | Reads the repository directly. skills.sh lists the repo after its first install through the CLI |
| GitHub CLI | `gh skill install usergraphtheory/erdostack` | Reads the repository; users can pin to the tag |
| Claude Code | `/plugin install erdostack@erdostack` | `.claude-plugin/` at the tagged commit. The `version` in `plugin.json` is what tells clients to update |
| Codex | `codex plugin add erdostack@erdostack` | `.agents/plugins/marketplace.json` and `plugin.json` |
| Copilot CLI | `copilot plugin install usergraphtheory/erdostack` | Root `plugin.json` |
| Cursor | Cursor Marketplace, once listed | `.cursor-plugin/plugin.json`; listing is a one-time submission and review |
| Gemini CLI | `gemini extensions install <repo url>` | `gemini-extension.json` plus the GitHub release archive. The gallery indexes tagged public repos that carry the `gemini-cli-extension` topic |
| npm | `npx erdostack install` | `release.yml`, trusted publishing |
| PyPI | `uvx erdostack install` | `release.yml`, trusted publishing |
| ClawHub | Browse or install from the ClawHub registry | `release.yml`, optional |

## Cutting a release

```bash
node scripts/sync-version.mjs 0.1.0   # writes the version into every manifest
npm run check                         # validator and installer tests
# move the Unreleased notes in CHANGELOG.md under the new version
git commit -am "Release 0.1.0"
git tag v0.1.0
git push origin main v0.1.0
```

The `Release` workflow then:

1. **Verifies.** The tag must equal the version in every manifest, at least one skill must exist, the tests must pass and both packages must build.
2. **Publishes to npm** from the `npm` environment. By default this is a staged publish that a maintainer approves with 2FA on npmjs.com. Set the `NPM_PUBLISH_MODE` repository variable to `direct` to skip the approval step.
3. **Publishes to PyPI** from the `pypi` environment.
4. **Creates the GitHub release** with generated notes and one archive. That archive has `gemini-extension.json` at its root, because Gemini CLI installs from the release asset when there is one. Do not attach other assets to a release.
5. **Publishes each skill to ClawHub** if the `CLAWHUB_OWNER` repository variable is set.

To rehearse without publishing, run the workflow by hand from the Actions tab. A manual run verifies and builds and then stops.

## The case repository

The eval cases live in a second repository, `erdostack/bench`, so that this one stays small enough to install from. It is a snapshot: the full `evals/` tree with every case and grader, `skills/` at the versions the saved reports name, an index of the cases and the recorded runs. A workflow there mirrors it to the Hugging Face dataset `erdostack/bench`.

Cut a new snapshot whenever a release changes a skill, adds cases or adds results:

1. Copy `evals/` and `skills/` from the working tree that holds the cases into a checkout of `erdostack/bench`. Every new `case.yaml` starts with that repository's canary line; a harness test fails if one does not.
2. Regenerate the index: `python3 evals/harness/erdo_eval.py index --out cases.jsonl`.
3. For a result that a claim rests on, publish its runs: `python3 evals/harness/erdo_eval.py export --root <runs> --report <report.json> --out recorded-runs/<skill>/<gate>`. Read what it wrote before you commit it. An agent's output can hold anything, including the name of the machine it ran on.
4. There, run `python3 -m unittest discover -s evals/harness -p 'test_*.py'`, `python3 evals/harness/erdo_eval.py selftest` and `python3 evals/harness/erdo_eval.py regrade --runs recorded-runs`. All three must pass in a fresh clone, not only in the working tree: git drops empty directories and applies ignore rules that a working tree hides, so add files with `git add -f -A`.
5. Commit, tag it with the same version as this repository, and push. The tag starts the sync to Hugging Face.

A report under `evals/results/` here must never name a case that is not in a pushed snapshot.

## One-time setup

Nothing below is stored in the repository. No registry token is ever added as a secret for npm or PyPI.

**GitHub**

- Create two environments, `npm` and `pypi`. Add required reviewers if you want a human gate before each publish.
- Add the topics that directories crawl for, including `agent-skills` and `gemini-cli-extension`.
- Protect `v*` tags and turn on immutable releases. `gh skill publish --dry-run` reports what is missing.
- Upload `assets/social-preview.png` as the repository's social preview (Settings, General). Profile pictures use `assets/avatar.png`. [assets/README.md](../assets/README.md) describes every image.

**Hugging Face**

- The dataset `erdostack/bench` belongs to the `erdostack` organization. The sync workflow in the case repository needs one repository secret on GitHub, `HF_TOKEN`: a Hugging Face token that may write to that dataset. The workflow has not been run yet.

**PyPI**

- The project exists. Version 0.0.0 was published from this workflow to hold the name, and it bundles no skills.
- Its trusted publisher is bound to owner `usergraphtheory`, repository `erdostack`, workflow `release.yml`, environment `pypi`, so a tag release needs no further setup. If the repository is renamed or moved, add a publisher for the new location before the next release.

**npm**

- The package exists. Version 0.0.0 was published by hand to hold the name. It bundles no skills and is marked deprecated in favour of the first release.
- A trusted publisher can only be attached to a package that exists, which is now the case. On the package's settings page add one: user `usergraphtheory`, repository `erdostack`, workflow `release.yml`, environment `npm`.
- A new trusted publisher must complete a successful publish within two days or it expires, so add it just before a release.
- Trusted publishing needs npm 11.5.1 or later, so the workflow runs on Node 24 and upgrades npm before publishing. Provenance is attached automatically.

**Cursor Marketplace**

- Submit the repository link once at `cursor.com/marketplace/publish`. Review is manual. Later versions are picked up from the manifest in the repository.

**Claude Code plugin directory**

- The repository already works as its own marketplace. To be listed in the official directory as well, submit the plugin at `claude.ai/directory/manage`. The older form linked from `anthropics/claude-plugins-official` is no longer used.

**ClawHub (optional)**

- Create the owner, store a CLI token as the `CLAWHUB_TOKEN` secret and set the `CLAWHUB_OWNER` variable. This job calls ClawHub's reusable workflow, pinned to a commit, and has not been exercised yet. The job grants `id-token: write` because the called workflow requests it; without that grant GitHub refuses to start the whole release workflow.

## Not automated

- **Codex public directory.** It currently accepts only plugins that connect to a remote MCP server, so a skills-only plugin is installed through the repo marketplace instead.
- **Curated lists.** Awesome lists and community directories take a pull request or a form each.

## After a release

- Install from at least two channels on a clean machine and confirm the skill list matches.
- Check that `npm view erdostack version` and the PyPI page show the new version, and that the npm page shows provenance.
