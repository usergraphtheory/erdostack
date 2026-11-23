# evals/

Skills are tested the way code is tested: give an agent a task where it is tempted to get graphs wrong, run it with and without the skill, and keep the results.

## What goes here

- **Task sets** on public datasets: a prompt, the engine and version, and how the result is judged.
- **The harness** that runs each task with and without erdostack installed, on at least two models.
- **Results**, including the cases where a skill made no difference or made things worse.

## Constraints

- No cloud account is needed. Neo4j runs in a container; LadybugDB runs in-process.
- Public datasets only.
- No number is published that cannot be reproduced from this directory.

## Status

The harness has not been built yet. It is the remaining Phase 0 item on the [roadmap](../ROADMAP.md), and no skill ships before it produces a baseline.

If you have a reproducible case of an agent mishandling a graph task, open an issue with the "Agent failure" template. Those reports seed the task sets.
