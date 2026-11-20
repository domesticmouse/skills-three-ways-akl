---
id: step-0
step: 0
title: Setup & Warm-Up
way: 0
duration: "~10 min"
slide: "S1-05"
slidePath: "./slides/#/9"
checkpoint: "codelab/start"
summary: "Verify your local toolchain, clone the starter branch, and ask Antigravity how 3-tier progressive disclosure works."
---

Instead of watching pre-recorded terminal demos, you are going to build and inspect **Brain Explorer**—a Python CLI and Textualize (`Textual`) TUI powered by the `google-antigravity` SDK—across **Skills Three Ways**:

1. **Way 1 · Ecosystem & Plugin Skills**: Official plugins pairing vendor SDK runbooks with specialist review subagents.
2. **Way 2 · Community Workflow Skills**: Discovering, evaluating, and locking open-source skill packs with `find-skills`.
3. **Way 3 · Bespoke In-Project Skills**: Turning real exploratory friction into a reusable 3-tier project skill without writing `SKILL.md` by hand.

Then, in Lab 5, you will launch **Brain Explorer** against your own `~/.gemini` **Session Trajectories** generated during Labs 0–4.

## Prerequisites

Make sure the following tools are installed and working before cloning:

| Tool | Requirement | Purpose in This Codelab |
| :--- | :--- | :--- |
| **Antigravity CLI (`agy`)** | Installed & authenticated | Interactive coding agent, `/plugin`, `/agy-customizations` |
| **`uv`** | Recent release | Fast Python 3.12+ virtual environments & dependency resolution |
| **Python** | `>= 3.12` | Runs `brain-explorer`, `ruff`, `mypy`, and `pytest` |
| **Node.js & `npx`** | Node `>= 18` | Runs `npx skills` (`find-skills` community registry CLI) |
| **`git`** | Any recent release | Branching from `codelab/start` and recovery checkpoints |

Run this sanity check in your terminal to confirm all prerequisites respond cleanly:

```bash label="Lab 0 · Verify CLI prerequisites"
agy --version
uv --version
python3 --version
node --version
npx --version
git --version
```

## Clone & Check Out the Clean Starter Branch

The `main` branch of `skills-three-ways-akl` holds the finished reference implementation (including this codelab and the Slidev deck). For a genuine lab run, start from `codelab/start` so your agent builds against a clean workspace rather than peeking at finished files:

```bash label="Lab 0 · Clone and branch from codelab/start"
git clone https://github.com/domesticmouse/skills-three-ways-akl.git
cd skills-three-ways-akl
git checkout -b my-lab codelab/start
ls -la .agents/skills/
```

:::callout info What Is Pre-Seeded in codelab/start?
`codelab/start` includes `pyproject.toml`, `GLOSSARY.md`, `AGENTS.md`, and two helper skills already in `.agents/skills/`: `agy-brain-explorer` (so your agent knows the schema of `~/.gemini/**/brain/` trajectories) and `writing-for-agents` (which shapes clean `SKILL.md` synthesis later in Lab 4). Nothing in `src/` or `tests/` exists yet.
:::

## Warm-Up: Ask Antigravity What Agent Skills Are

Launch `agy` inside the repository root and paste your first prompt:

```bash label="Lab 0 · Launch agy"
agy
```

Once the `agy` prompt box settles at `? for shortcuts`, ask:

```prompt label="Lab 0 · Ask Antigravity what agent skills are"
What are agent skills?
```

### What to Notice in the Answer

Watch how `agy` immediately consults its built-in customisation guidance and breaks down two core ideas from Act 1:

- **Directory anatomy**: A skill is a folder containing `SKILL.md` (required), plus optional `scripts/`, `references/`, and `resources/` directories.
- **3-Tier Progressive Disclosure**:
  1. **Tier 1 · Discovery (~100 tokens)**: Only `name` and `description` from YAML frontmatter load at session startup.
  2. **Tier 2 · Activation (< 5,000 tokens)**: The `SKILL.md` runbook loads only when a prompt matches the description.
  3. **Tier 3 · Execution (on demand)**: Deep `references/*.md` guides and executable `scripts/*.py` load or run only for the sub-task that needs them.

Keep this `agy` session open—or exit cleanly with `Ctrl+D` twice—before moving on to Lab 1.

:::details Troubleshooting Lab 0 Setup
- **`agy` prompts for authentication**: Run `agy` interactively outside restricted shells and complete sign-in before starting Lab 1.
- **`codelab/start` branch not found**: Run `git fetch origin && git checkout -b my-lab origin/codelab/start`.
- **`uv` missing**: Install from `https://docs.astral.sh/uv/` or via Homebrew (`brew install uv`).
:::

## Lab 0 Checklist

:::checklist
- [ ] All CLI prerequisites (`agy`, `uv`, `python3 >= 3.12`, `node`, `npx`, `git`) report versions cleanly.
- [ ] Repository cloned and `my-lab` branch checked out from `codelab/start`.
- [ ] Prompted `agy` with `"What are agent skills?"` and observed the 3-tier progressive disclosure breakdown.
:::
