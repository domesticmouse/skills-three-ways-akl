---
id: step-5
step: 5
title: Brain Explorer Payoff
way: mashup
duration: "~15 min"
slide: "S4-06"
slidePath: "./slides/#/34"
checkpoint: "codelab/checkpoint-4-bespoke-skill"
summary: "Launch Brain Explorer against your own ~/.gemini Session Trajectories from Labs 0–4 and watch the embedded SDK agent render an interactive A2UI v1.0 Skill Activations comparison."
---

Everything we built across Labs 0–4 comes full circle right here. You are not going to inspect canned sample data—you are going to launch **Brain Explorer** against the real `~/.gemini` **Session Trajectories** created on your own machine over the last 75 minutes!

Exit `agy` (`Ctrl+D` twice) so you are back in your regular terminal at the repository root.

## 1. Inspect Your Trajectories from the CLI

First, list the recent Antigravity trajectories for this workspace using the fast deterministic CLI (`TrajectoryStore`—zero LLM calls, zero latency):

```bash label="Lab 5 · List your own Session Trajectories via CLI"
uv run brain-explorer sessions --project "$(basename "$PWD")" --limit 20
```

You should see the sessions from Lab 0 (*What are agent skills?*), Lab 1 (`/plugin`), Lab 2 (`find-skills`), Lab 3 (EGM Cycle 1 & Cycle 2 + subagents), and Lab 4 (`/agy-customizations` + cold verification), along with their detected **Skill Activations** across `way_1_plugin`, `way_2_community`, and `way_3_bespoke`.

:::callout tip Renamed Folder or Multiple Workspaces?
Passing `"$(basename "$PWD")"` matches whatever directory name you cloned into. You can also omit `--project` (`uv run brain-explorer sessions --limit 20`) to browse trajectories across all projects under `~/.gemini`, or inspect a single session in detail with `uv run brain-explorer inspect <session-id-prefix>`.
:::

## 2. Launch the Brain Explorer Textual TUI

Now start the interactive TUI:

```bash label="Lab 5 · Launch Brain Explorer TUI"
uv run brain-explorer
```

Take 60 seconds to explore the deterministic local interface:

| Shortcut | Action |
| :--- | :--- |
| **`Ctrl+B`** | Toggle the local **Session Trajectories** sidebar |
| **`Enter` / Click** | Inspect any trajectory's steps and detected Skill Activations instantly |
| **`/`** | Focus the agent prompt bar at the bottom of the screen |
| **`Ctrl+I`** | Toggle the **A2UI v1.0** protocol envelope & `DataModel` inspector |
| **`Ctrl+R`** | Reset to the overview surface |
| **`q`** | Quit Brain Explorer |

## 3. Ask the Embedded SDK Agent for an A2UI v1.0 Breakdown

Press **`/`** to focus the `#prompt-input` bar inside **Brain Explorer**, paste this prompt, and press `Enter`:

```prompt label="Lab 5 · In-TUI A2UI v1.0 Skill Activations prompt"
Compare how Way 1 plugin skills, Way 2 community skills, and Way 3 bespoke skills were activated across our Brain Explorer build sessions, and group them into an interactive A2UI v1.0 tabbed breakdown.
```

### What to Explore in the Live Surface

1. **Click through the rendered A2UI v1.0 tabs**: Notice how Way 1 plugins (`google-antigravity-sdk`, `egm-*`, `agy-customizations`), Way 2 community skills (`wshobson/agents`, `find-skills`, `writing-for-agents`), and Way 3 bespoke skills (`agy-brain-explorer` plus your Lab 4 bespoke skill) worked **in concert** across your build sessions rather than as isolated silos.
2. **Press `Ctrl+I`**: Inspect the raw `"version": "1.0"` A2UI JSON payload, `DataModel`, and `"@path"` bindings emitted by `BrainExplorerAgentService`.
3. **Verify terminal hygiene**: Because `configure_sdk_logging()` strips console `StreamHandler` instances while preserving `FileHandler`, SDK logs stay out of Textual's alternate screen buffer.

:::callout info Zero Dataset Pollution
Remember EGM Cycle 1's biggest architectural save? `BrainExplorerAgentService` redirects `app_data_dir` and `save_dir` into a temporary directory outside `~/.gemini` and locks tools down with `policy.deny_all()`. Inspecting your build trajectories inside the TUI never writes noisy new sessions back into `~/.gemini`.
:::

## Choosing the Right Tier Back at Work

When you return to your own repositories tomorrow, keep this mental model handy:

- **Start with Way 1 (Plugins)** whenever a vendor platform SDK or multi-persona review workflow (like **EGM**) already exists.
- **Adopt & Vet Way 2 (Community)** via `find-skills` for standard language conventions—and treat empty search results as early radar for integration risk.
- **Synthesise Way 3 (Bespoke)** only after solving real exploratory friction once: invoke `/agy-customizations`, keep `SKILL.md` concise, isolate deep gotchas into `references/`, and always prove it in a clean cold session.

## Further Reading & Links

- **Matching Slidev Presentation Deck**: [`./slides/`](./slides/)
- **Source Repository & Checkpoints**: [github.com/domesticmouse/skills-three-ways-akl](https://github.com/domesticmouse/skills-three-ways-akl)
- **Open Agent Skills Registry**: [skills.sh](https://skills.sh)
- **Google Antigravity**: [antigravity.google](https://antigravity.google)

## Lab 5 Checklist

:::checklist
- [ ] Ran `uv run brain-explorer sessions` and saw your own Labs 0–4 Session Trajectories.
- [ ] Launched `uv run brain-explorer` and navigated the deterministic `TrajectoryStore` sidebar (`Ctrl+B`).
- [ ] Generated the tabbed A2UI v1.0 Skill Activations comparison via `/` and inspected the raw v1.0 envelope with `Ctrl+I`.
:::
