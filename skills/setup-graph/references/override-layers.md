# Which layer wins: image tags and lockfiles

Last verified: 2026-11-23
Status: tool behaviour written from prior knowledge. The official pages are listed in `sources.md` but were
not read on that date, so every rule below is "not verified against documentation, not executed". When two
layers disagree, record the value these rules give and list both values and both files under Open questions,
so a wrong rule here cannot hide.

Start from the command, not from the files: find what people run to start the database (a make target, a
package script, a CI job, a line in the contributor notes) and read off which files and variables it passes.
A file nothing passes is not a layer.

## Container image of a server engine

| Where | What replaces what |
|---|---|
| Compose, several files | With no `-f`, the default file is merged with its `override` sibling if one exists. With `-f` flags, only the listed files are used, and a later file replaces values of an earlier one |
| Compose, `image: name:${VAR:-fallback}` | `VAR` comes from the shell or the make recipe's environment first, then from the file given with `--env-file`, or from `.env` in the project directory when no such flag is given. The fallback is used only when none of them sets it |
| Compose, `env_file:` under a service | Sets variables inside the container. It does not fill `${VAR}` in the compose file itself |
| Dockerfile, `ARG X=default` used in `FROM` | Replaced by `--build-arg X=...` or by `build.args` in the compose file |
| Compose service with both `build:` and `image:` | The service is normally built, so the Dockerfile's `FROM` decides what runs and `image:` only names the result. If `image:` also names a public engine image, list both |
| Helm | Chart `values.yaml` is the default. Files given with `-f` or `--values` replace it, the rightmost last, and `--set` replaces those. `version` in `Chart.yaml` is the chart's own version. `appVersion` is a label unless the template falls back to it when the tag is empty: read the template |
| Kustomize | An overlay's `images:` entry (`newTag`) replaces the tag in the base manifest |
| Test containers | The image string in the fixture code is what the tests start. It is the engine version only when the repo runs no other database |
| CI service containers | The image under the job's services. It is the engine version only when the repo runs the database nowhere else |

A tag such as `latest`, or a tag given only as a variable that nothing in the repo sets, pins nothing: record
`unknown` and say which variable would decide it.

## Locked package versions

| Ecosystem | Where the resolved version is | Not a pin |
|---|---|---|
| Python | `poetry.lock`, `uv.lock`, `Pipfile.lock`, or a compiled requirements file with `==` lines | ranges in `pyproject.toml`, `Pipfile`, or a hand-written requirements input file |
| Node | `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock` | ranges in `package.json` |
| Rust | `Cargo.lock` | `Cargo.toml` |
| Go | the `require` line in `go.mod` | `go.sum`, which can list versions that are not used |
| Gradle | `gradle.lockfile`, else an exact version in the build file or version catalog | dynamic versions |
| Maven | the literal `<version>`, or the property it points to, or the version managed by the parent pom or an imported BOM: follow the chain to the file that states the number. A BOM published with the artifact itself (same group, named `<artifact>-bom`) versions its own modules, so its version is the artifact's version: record it and say it came through the BOM | the version of a platform or framework BOM (another publisher, managing many projects), when no repo file states the managed number. An own-project BOM is never this case, even though its file is not in the repo |

Two lockfiles for one ecosystem: the live one is the one the project installs from. Look for the
package-manager field in the manifest, the lockfile the Dockerfile copies, and the install command in CI.
Report the other as a leftover under Open questions, with the version it would have given.

Monorepos and workspaces: one root lockfile usually holds every member's dependencies. Find the entry that
belongs to the member the user named, not the first match in the file.
