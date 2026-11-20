---
id: step-3
step: 3
title: Two-Pass EGM Build Cycle
way: 2
duration: "~30 min"
slide: "S3-06"
slidePath: "./slides/#/26"
checkpoint: "codelab/checkpoint-3-brain-explorer"
summary: "Run Cycle 1 architecture design with four EGM critic subagents, then implement (or Fast-Track inspect) the hybrid TrajectoryStore, isolated AgentService, and A2UI v1.0 Textual renderer."
---

This lab is the centrepiece of the 90-minute codelab: we combine **Way 1** (`google-antigravity-sdk` + `egm`), **Way 2** (`wshobson/agents` Python skills), and **Way 3** (`agy-brain-explorer`, pre-seeded in `codelab/start`) to design, audit, and build **Brain Explorer**.

Because LLM-generated architectures vary from run to run—and building a ~3,500-line Python TUI from scratch can chew through time or API quota—Lab 3 splits into two parts:

- **Part A (~10 min)**: Everyone runs **Cycle 1 (Design + EGM Review)** live to watch four independent critics catch the naive agent-first anti-pattern.
- **Part B (~20 min)**: Choose **Path 1 (Full Build)** if you have quota and want to watch Cycle 2 unfold end-to-end, or **Path 2 (Fast Track)** to check out `codelab/checkpoint-3-brain-explorer` and audit the reference traps interactively.

## Part A: Cycle 1 Design & EGM Architectural Audit (~10 min)

In your active `agy` session, paste this design + review prompt:

```prompt label="Lab 3 · Cycle 1 design and EGM audit prompt"
Using google-antigravity-sdk, agy-brain-explorer, and our Python skills, design a Brain Explorer Python CLI and Textual TUI that inspects ~/.gemini session trajectories and skill activations, then run an EGM review cycle (egm-design, egm-zoom-out, egm-codebase-details, egm-implementation-readiness) on the design.
```

### Watch What Happens While the 4 EGM Critics Run

Compare what your reviewers report with the classic anti-pattern caught during our reference run:

1. **Naive First Draft (Rejected by `egm-design` & `egm-zoom-out`)**: Routing *every* TUI list or selection event through the in-process LLM agent. That causes multi-second latency per keypress, burns tokens unnecessarily, and—worst of all—writes new SDK session trajectories straight back into `~/.gemini`, contaminating the very dataset you are inspecting.
2. **Cycle 1 Hybrid Architecture (Approved)**:
   - **`TrajectoryStore`**: Fast, deterministic local Python reader parsing `~/.gemini/*/brain/` (`transcript.jsonl` / `transcript_full.jsonl`) in milliseconds and classifying Skill Activations (`way_1_plugin`, `way_2_community`, `way_3_bespoke`).
   - **`BrainExplorerAgentService`**: Isolated, read-only `LocalAgentConfig` agent (with `app_data_dir` and `save_dir` redirected to a temporary directory outside `~/.gemini`) invoked **only** on explicit `/` user prompts to compose A2UI v1.0 surfaces.

---

## Part B: Cycle 2 Implementation & Verification (~20 min)

Pick the path that fits your clock and token budget:

### Path 1: Full Build (Run Cycle 2 Live)

If you want to watch your agent write `src/brain_explorer/`, hit Textual 8+ / A2UI v1.0 friction, and run a second EGM pass to fix it, submit:

```prompt label="Lab 3 · Cycle 2 implement and verify prompt"
Implement the hybrid TrajectoryStore, isolated AgentService, and Textual A2UI v1.0 renderer, then run a second EGM review pass and verify with ruff, mypy, and pytest.
```

:::callout info Running Out of Time or Quota?
If Cycle 2 takes longer than ~15 minutes, stop the run cleanly and switch to **Path 2** below—you will keep all of your Cycle 1 `Session Trajectory` history in `~/.gemini` and land on a clean, verified Python baseline ready for Labs 4 and 5.
:::

### Path 2: Fast Track (Checkout Reference Code & Audit It)

Check out the verified `codelab/checkpoint-3-brain-explorer` snapshot, install Python dependencies with `uv sync`, and verify the suite passes:

```bash label="Lab 3 · Fast Track checkout and test baseline"
git checkout -b my-lab-3 codelab/checkpoint-3-brain-explorer
uv sync
uv run ruff check src tests
uv run mypy src
uv run pytest -v
```

Then ask `agy` to audit how the reference renderer solved the A2UI v1.0 and Textual 8+ traps:

```prompt label="Lab 3 · Fast Track audit prompt"
Inspect src/brain_explorer/agent_service.py, src/brain_explorer/a2ui_textual.py, and tests/test_a2ui_textual.py, and run an egm-codebase-details review summarising the subtle A2UI v1.0 and Textual 8+ integration traps they handle.
```

## Reference Debrief: The 10 Cycle 2 Traps We Hit

Remember the `npx skills find textual` coverage gap we spotted in Lab 2? This is exactly where it bit us during our Exploratory Run. Open the foldout below to compare your agent's Cycle 2 findings against the 10 traps we uncovered:

:::details Reference Debrief: 10 A2UI v1.0, Textual 8+, and SDK Traps
1. **`@path` vs. `path` (`TemplateChildList`)**: A2UI v1.0 switched `DataBinding` from `{"path": "..."}` to `{"@path": "..."}`—except `TemplateChildList`, which still stores its array key under `"path"`. Wrapping `"path"` as `{"@path": template_path}` when `data_ctx.at_least_v10` avoids blank template `List` cards.
2. **`Text.variant` rejects `h1`–`h5`**: Under `STRICT_VALIDATION`, `BasicCatalog` v1.0 only permits `"body"` or `"caption"`. Use Markdown headings inside `"text"` rendered via Textual's `Markdown` widget.
3. **Silent masking without `STRICT_VALIDATION`**: Always validate incoming agent JSON on a throwaway staging `MessageProcessor([catalog], options=MessageProcessorOptions(validation_config=STRICT_VALIDATION))` before touching the live surface.
4. **`A2uiIntegrityError` on duplicate `createSurface`**: Delete existing surfaces in `processor.model.surfaces_map` after staging passes and before applying a new `createSurface`.
5. **Click-time `DataContext.resolve_action`**: Evaluating button actions at render time freezes initial values and ignores user edits in `Input`, `Checkbox`, and `Select`. Store `raw_action` and `data_context` on the button and resolve inside `on_button_pressed`.
6. **Off-mount `TabbedContent.compose_add_child`**: Calling `add_pane()` on an unmounted `TabbedContent` fails; use `tabbed.compose_add_child(TabPane(title, child))` during composition.
7. **Textual 8+ `Select.NULL` & `ChoicePicker` `list[str]`**: Textual 8 removed `Select.BLANK` in favour of `Select.NULL`, and A2UI v1.0 `ChoicePicker` expects `list[str]`, never a scalar string.
8. **`Static(markup=False)` & `AUTO_FOCUS = None`**: Brackets in raw JSON or `[way_3_bespoke]` crash Rich markup parsing unless `markup=False` is set on `Static`/`Label`; `AUTO_FOCUS = None` keeps global shortcuts like `/` and `Ctrl+B` active on launch.
9. **`logging.FileHandler` subclasses `logging.StreamHandler`**: Stripping `isinstance(h, logging.StreamHandler)` removes your own `FileHandler` unless you explicitly guard `not isinstance(h, logging.FileHandler)`.
10. **Isolated `app_data_dir`, policies & `StopReason` retries**: Default `LocalAgentConfig` logs into `~/.gemini` and exposes built-in tools; isolate `app_data_dir` / `save_dir`, apply `policy.deny_all()`, and retry missing `<a2ui-json>` blocks only when `response.stop_reason == types.StopReason.UNSPECIFIED`.
:::

## Lab 3 Verification Gate

Before moving to Lab 4, confirm all three checks pass cleanly in your terminal:

```bash label="Lab 3 · Run ruff, mypy, and pytest verification"
uv run ruff check src tests
uv run mypy src
uv run pytest -v
```

## Lab 3 Checklist

:::checklist
- [ ] Ran Cycle 1 design + 4-critic EGM review and observed the Hybrid Architecture (`TrajectoryStore` + isolated `AgentService`).
- [ ] Completed either Path 1 (Full Build) or Path 2 (Fast Track via `codelab/checkpoint-3-brain-explorer`).
- [ ] Confirmed `uv run ruff check src tests`, `uv run mypy src`, and `uv run pytest -v` are all green.
:::
