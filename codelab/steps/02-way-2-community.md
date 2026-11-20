---
id: step-2
step: 2
title: Way 2 · Community Workflow Skills
way: 2
duration: "~10 min"
slide: "S3-03"
slidePath: "./slides/#/23"
checkpoint: "codelab/checkpoint-2-skills"
summary: "Use find-skills to search for Python and Textual TUI skills, evaluate trust signals, spot the coverage gap, and lock wshobson/agents into the repo."
---

With our platform plugins enabled, we do not need to re-invent everyday Python engineering conventions (`uv`, strict `mypy`, `pytest`, `asyncio`). Let's turn to **Way 2: Community Workflow Skills**.

Because `find-skills` is itself a skill installed globally in Lab 1, you do not have to memorise CLI flags—just ask `agy` to search and evaluate the registry for you.

## 1. Search for Python & Textual TUI Skills

In your active `agy` session, paste:

```prompt label="Lab 2 · Search Python and Textual skills"
We want to build Brain Explorer—a Python CLI and Textual TUI powered by the Google Antigravity SDK to inspect our ~/.gemini session trajectories. Use find-skills to search for Python and Textual TUI skills.
```

Approve any network prompt if `npx skills find` requests outbound access to query `skills.sh`.

### What to Look For in the Evaluation

Pay attention to two opposite signals in `agy`'s report:

1. **High-signal community coverage (`python`)**: You should see high-adoption suites such as `wshobson/agents` with install counts, GitHub star provenance, and security-scan summaries on `skills.sh`.
2. **An explicit coverage gap (`textual`)**: Searching for Textual TUI + A2UI v1.0 returns **zero mature community skills**. Finding an empty search result early is genuinely useful—it tells you ahead of time where the agent will lean on raw training weights and where you must aim your Way 1 **EGM** reviewers (and eventually extract a Way 3 bespoke skill).

## 2. Install & Lock Community Python Skills

Now ask `agy` to install the Python development skills into this repository's `.agents/skills/` directory:

```prompt label="Lab 2 · Install wshobson/agents Python skills"
Let's install the Python development skills from wshobson/agents into this repo so our agents follow uv, strict typing, async, and testing conventions.
```

:::callout warn Trust Before Installing
Never pull arbitrary skills blindly into a production repo. In real team work, review the skill's `SKILL.md` and `scripts/` before committing, and always commit `skills-lock.json` so every contributor (and our Brain Explorer tier classifier!) knows which skills came from pinned community sources.
:::

## 3. Inspect `.agents/skills/` and `skills-lock.json`

Once `agy` finishes installing, inspect what landed on disk in a second terminal tab (or after pausing in `agy`):

```bash label="Lab 2 · Inspect installed skills and lockfile"
ls -1 .agents/skills/
head -n 35 skills-lock.json
```

Notice that even with **17+ community skills** now living in `.agents/skills/` (covering `uv-package-manager`, `python-type-safety`, `async-python-patterns`, `python-testing-patterns`, and more), session startup context stays small because only Tier 1 (`name` + `description`) is loaded.

:::details Stuck or Offline? Jump to Checkpoint 2
If `npx skills` hits conference Wi-Fi issues or a registry rate limit, check out the clean post-Lab 2 snapshot directly:

```bash label="Lab 2 · Recover using checkpoint-2-skills"
git checkout -b my-lab-2 codelab/checkpoint-2-skills
ls -1 .agents/skills/
```
:::

## Lab 2 Checklist

:::checklist
- [ ] Searched Python and Textual skills via `find-skills` and observed the Textual + A2UI v1.0 ecosystem gap.
- [ ] Installed `wshobson/agents` Python development skills into `.agents/skills/`.
- [ ] Confirmed `skills-lock.json` is populated on disk.
:::
