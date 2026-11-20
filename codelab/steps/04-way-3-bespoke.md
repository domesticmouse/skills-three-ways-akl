---
id: step-4
step: 4
title: Way 3 · Bespoke In-Project Skills
way: 3
duration: "~15 min"
slide: "S4-03"
slidePath: "./slides/#/31"
checkpoint: "codelab/checkpoint-4-bespoke-skill"
summary: "Synthesise your hard-won A2UI v1.0 + Textual lessons into a reusable 3-tier skill via /agy-customizations, then prove it activates automatically in a brand-new cold session."
---

Notice what just happened in Lab 3: every time a fresh `agy` session opens on this codebase without a skill covering A2UI v1.0 and Textual 8+, it risks repeating the exact same 10 integration traps.

Rather than stuffing 200 lines of workarounds into `AGENTS.md` (which wastes context tokens on every unrelated turn) or hand-writing `SKILL.md` from scratch, let's use Antigravity's built-in `/agy-customizations` workflow to synthesise a **Way 3 Bespoke In-Project Skill** directly from the codebase and session friction.

## 1. Phase 2 Synthesis with `/agy-customizations`

In the same `agy` session where you just built or audited `agent_service.py` and `a2ui_textual.py`, run:

```prompt label="Lab 4 · Synthesise bespoke skill with /agy-customizations"
/agy-customizations Please turn what we learned building and reviewing our A2UI v1.0 Textual renderer and Antigravity SDK integration into a reusable workspace skill
```

### Inspect What `/agy-customizations` Generated

Open a second shell tab (or check the file tree once `agy` finishes) and inspect `.agents/skills/` to see what your agent created:

```bash label="Lab 4 · Inspect generated bespoke skill files"
ls -la .agents/skills/
```

Check three hallmarks of a well-structured 3-tier skill (comparing with our `writing-for-agents` guidelines):

1. **Tier 1 (`name` & `description` in YAML frontmatter)**: Under ~100 tokens, packed with exact domain triggers (`a2ui-core`, `MessageProcessor`, `BasicCatalog`, `Textual`, `LocalAgentConfig`, `"Use when..."`).
2. **Tier 2 (`SKILL.md` body)**: Concise operational runbook with clear completion criteria and explicit relative pointers into `references/`.
3. **Tier 3 (`references/*.md`)**: Deep `Symptom -> Root Cause -> Fix` troubleshooting catalogue—kept out of memory until an agent is actively debugging A2UI v1.0 or Textual widgets.

:::callout warn Critical Step: Start a Truly Cold Session!
To prove Tier 1 semantic routing actually works—and isn't just coasting on your existing conversation history—you **must exit `agy` completely** (`Ctrl+D` twice) and launch a brand-new session before running Phase 3!
:::

## 2. Phase 3 Cold-Session Verification

Exit `agy` (`Ctrl+D` twice), then start a fresh session with an empty context window:

```bash label="Lab 4 · Launch a brand-new cold agy session"
agy
```

Notice carefully: **the prompt below never mentions the name of your new skill**. If your YAML `description` did its job, Tier 1 discovery should recognise the keywords (`A2UI v1.0`, `Python Textual TUI`) and read `SKILL.md` + `references/` automatically:

```prompt label="Lab 4 · Cold-session verification prompt"
Build an A2UI v1.0 surface for our Python Textual TUI that compares Skill Activations across Way 1 plugins, Way 2 community skills, and Way 3 bespoke skills with interactive tabs and a tier filter.
```

### What to Watch For

- Watch the tool calls in the cold session: did `agy` immediately `read_file` your new `.agents/skills/<skill-name>/SKILL.md` (Tier 2) and its `references/` file (Tier 3)?
- Check whether the generated A2UI v1.0 payload uses `"@path"`, restricts `Text.variant` to `"body"` / `"caption"`, uses `List[str]` (`DynamicStringList`) for `ChoicePicker`, and passes `STRICT_VALIDATION` on the first run.
- Verify tests still pass after any edits:

```bash label="Lab 4 · Re-run verification after cold-session test"
uv run ruff check src tests
uv run mypy src
uv run pytest -v
```

:::details Compare Your Skill with the Reference Skill (a2ui-textual)
In our Exploratory Run, `/agy-customizations` produced `.agents/skills/a2ui-textual/SKILL.md` (94 lines) plus `references/a2ui-v1-textual-gotchas.md` (114 lines covering all 10 Cycle 2 traps). Notice that even if your agent chose a different folder name (like `textual-a2ui-surfaces`), **Brain Explorer** checks `skills-lock.json` dynamically—so any skill in `.agents/skills/` absent from `skills-lock.json` will still classify cleanly as `way_3_bespoke` in Lab 5!

If you ever want to switch directly to our reference skill snapshot:

```bash label="Lab 4 · Optional checkout of checkpoint-4-bespoke-skill"
git checkout -b my-lab-4 codelab/checkpoint-4-bespoke-skill
uv sync
```
:::

## Lab 4 Checklist

:::checklist
- [ ] Synthesised a bespoke skill in `.agents/skills/<your-skill>/` using `/agy-customizations`.
- [ ] Verified Tier 1 frontmatter, concise Tier 2 `SKILL.md` runbook, and Tier 3 `references/` isolation.
- [ ] Exited `agy` completely (`Ctrl+D` twice) and tested semantic activation from a fresh cold session without naming the skill.
- [ ] Confirmed `ruff`, `mypy`, and `pytest` pass.
:::
