# Changelog

Notable changes to erdostack. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- Repository skeleton: `skills/`, `references/engines/`, `evals/` and authoring templates.
- Host manifests over the same markdown: Agent Plugins (`plugin.json`), Claude Code, Cursor, Codex and Gemini CLI.
- `erdostack` installers for npm and PyPI that copy bundled skills into an agent's skills directory.
- Validator for manifests, versions, skill frontmatter and engine packs.
- CI on Linux, macOS and Windows, and a tag-driven release workflow for npm, PyPI and GitHub Releases.
- An "Official sources" list in the README.

### Changed

- The logo, share image and brand color now match [erdostack.com](https://erdostack.com): chalk on a chalkboard, with the source vertex in yellow.
- Package and plugin homepages point to erdostack.com.

### Fixed

- The release workflow no longer fails at startup.

No skills have shipped yet.
