# Security

## Reporting a vulnerability

Report privately through GitHub: open the repository's **Security** tab and choose **Report a vulnerability**. Please do not open a public issue for anything exploitable.

You will get an acknowledgement, and a fix or a decision is published as a GitHub security advisory.

## What counts

Skills are instructions that an agent follows with your permissions, so the threat model is closer to a dependency than to documentation. Reports are welcome for:

- A skill, engine pack or script that causes an agent to exfiltrate data, weaken a safeguard, run destructive queries or commands, or act against the person who installed it.
- Prompt injection carried by repository content, including text hidden in markdown or references.
- A flaw in the `erdostack` installers on npm or PyPI, for example writing outside the chosen target directory.
- A compromised release artifact or a mismatch between a published package and the tagged source.

## What this project commits to

- No network calls, no telemetry, no install scripts and no auto-update in anything shipped from this repository.
- Releases are built by GitHub Actions from a tagged commit. The release workflow publishes to npm and PyPI through trusted publishing (OIDC), and no long-lived registry token is stored in the repository.
- Skills never ask for credentials and never instruct an agent to bypass a permission prompt.

## Using the skills safely

- Read a skill before you install it. They are short on purpose.
- Give your agent read-only database credentials unless a task needs writes, and set query timeouts on the server. A skill reduces risk; it is not an access control.
- Pin to a tag if you need reproducibility. See [docs/INSTALL.md](docs/INSTALL.md).
