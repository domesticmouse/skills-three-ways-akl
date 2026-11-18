# Skills Three Ways — Presentation TODO

Remaining tasks to complete the **Skills Three Ways** presentation (`PRESENTATION.md`) for DevFest Auckland 2026, based on the locked map [Skills Three Ways: DevFest Auckland 2026 Talk & Brain Explorer App](https://github.com/domesticmouse/skills-three-ways-akl/issues/1).

---

## Completed Foundations (Reference)

All planning and exploratory architecture tickets on [Skills Three Ways: DevFest Auckland 2026 Talk & Brain Explorer App](https://github.com/domesticmouse/skills-three-ways-akl/issues/1) are resolved:

- [x] **Brain Explorer Architecture & Contract**: [Define the Brain Explorer user journey and Python SDK Pydantic contract](https://github.com/domesticmouse/skills-three-ways-akl/issues/2)
- [x] **Talk Parameters & Four-Act Narrative Arc**: [Lock the Three Ways narrative arc and talk parameters](https://github.com/domesticmouse/skills-three-ways-akl/issues/3)
- [x] **Exploratory Run App & EGM Cycles**: [Prototype the Python Textual TUI + Antigravity SDK Brain Explorer with EGM review cycles](https://github.com/domesticmouse/skills-three-ways-akl/issues/4) (`src/brain_explorer/`, `tests/`, `prototype/brain-explorer-tui`)
- [x] **Way 3 Bespoke Skill Extraction & Verification**: [Extract and prototype the bespoke skill from the Exploratory Run with agy-customizations](https://github.com/domesticmouse/skills-three-ways-akl/issues/6) (`.agents/skills/a2ui-textual/`, `prototype/a2ui-textual-skill`)
- [x] **Recording Script, `.cast` Chapters & Dataset**: [Script the Recording Run prompt sequence, asciinema .cast chapters, and canonical Session Trajectory dataset](https://github.com/domesticmouse/skills-three-ways-akl/issues/7)
- [x] **Acts 2–4 Slide Blueprint & Speaker Notes**: [Lock the slide-by-slide layout blueprint and speaker notes for Acts 2–4 in slides/acts/](https://github.com/domesticmouse/skills-three-ways-akl/issues/8)
- [x] **Act 1 Primer & Recording**: `slides/acts/01-primer.md` (`S1-01`–`S1-10`, 13 slides) and `recordings/final/what-are-agent-skills.cast` (synced to `slides/public/casts/what-are-agent-skills.cast`)

---

## Phase 1: Curate Canonical Session Trajectories & Execute the `asciinema` Recording Run

Record the 5 modular `.cast` files under `recordings/final/` following the prompt script and 24 paired **Before / After** prompt-entry `"m"` chapter stop points locked in [Script the Recording Run prompt sequence, asciinema .cast chapters, and canonical Session Trajectory dataset](https://github.com/domesticmouse/skills-three-ways-akl/issues/7).

### 1.1 Curate the Canonical `~/.gemini` Session Trajectories Dataset
- [ ] Verify that **Brain Explorer** (`TrajectoryStore`) displays only the **4 headline build trajectories** (plus the 8 Cycle 1 and Cycle 2 **EGM** review subagent trajectories) for `skills-three-ways-akl`, excluding `/wayfinder` and `/grilling` meta-planning sessions:
  - **Trajectory 1 — Way 1 Plugin Discovery** (`way-1-plugins-setup.cast`): `plugin` / `google-antigravity-sdk` (`way_1_plugin`)
  - **Trajectory 2 — Way 2 Skill Evaluation** (`way-2-find-skills.cast`): `find-skills` (`way_2_community`)
  - **Trajectory 3 — Two-Pass EGM Build Cycle** (`way-2-egm-cycle.cast`, plus Cycle 1 & Cycle 2 **EGM** subagent trajectories): `google-antigravity-sdk` + `egm-*` (`way_1_plugin`), `wshobson/agents` Python skills (`way_2_community`), `agy-brain-explorer` (`way_3_bespoke`)
  - **Trajectory 4 — Way 3 Synthesis & Cold Verification** (`way-3-agy-customizations.cast`): `agy-customizations` (`way_1_plugin`), `writing-for-agents` (`way_2_community`), `a2ui-textual` (`way_3_bespoke` — reading `SKILL.md` and `references/a2ui-v1-textual-gotchas.md`)

### 1.2 Record, Sanitise, Trim & Chapter-Mark the 5 `.cast` Files
For each recording below, sanitise secrets (`sanitize-cast.py`), strip trailing shell exit prompts (`trim-cast.py --in-place`), and set/verify `"m"` chapter markers (`mark-cast.py --set` / `--list`):

- [ ] **`recordings/final/way-1-plugins-setup.cast` (Act 2 · 6 stop points)**
  - `m1` (`Before: Install find-skills`): Initial `zsh` prompt ready
  - `m2` (`After: Install find-skills`): `npx skills add vercel-labs/skills@find-skills -g -y`
  - `m3` (`Before: Launch agy`): `find-skills` installation finished; `zsh` prompt ready
  - `m4` (`After: Launch agy`): `agy`
  - `m5` (`Before: Verify Way 1 plugins prompt`): `agy` banner loaded and `>` prompt box empty
  - `m6` (`After: Verify Way 1 plugins prompt`): `/plugin Please check that the Google Antigravity SDK plugin (google-antigravity-sdk) and the EGM review subagents are enabled for this workspace, and show me what skills and specialist agents they provide.`
- [ ] **`recordings/final/way-2-find-skills.cast` (Act 3 Part 1 · 4 stop points)**
  - `m1` (`Before: Search Python & Textual skills prompt`): `agy` prompt box empty
  - `m2` (`After: Search Python & Textual skills prompt`): `We want to build Brain Explorer—a Python CLI and Textual TUI powered by the Google Antigravity SDK to inspect our ~/.gemini session trajectories. Use find-skills to search for Python and Textual TUI skills.`
  - `m3` (`Before: Install wshobson/agents Python skills prompt`): `npx skills find python` and `npx skills find textual` evaluation complete; prompt box ready
  - `m4` (`After: Install wshobson/agents Python skills prompt`): `Let's install the Python development skills from wshobson/agents into this repo so our agents follow uv, strict typing, async, and testing conventions.`
- [ ] **`recordings/final/way-2-egm-cycle.cast` (Act 3 Part 2 · 4 stop points)**
  - `m1` (`Before: Cycle 1 design & EGM audit prompt`): `agy` prompt box empty
  - `m2` (`After: Cycle 1 design & EGM audit prompt`): `Using google-antigravity-sdk, agy-brain-explorer, and our Python skills, design a Brain Explorer Python CLI and Textual TUI that inspects ~/.gemini session trajectories and skill activations, then run an EGM review cycle (egm-design, egm-zoom-out, egm-codebase-details, egm-implementation-readiness) on the design.`
  - `m3` (`Before: Cycle 2 implement & EGM audit prompt`): Cycle 1 resolution summary rendered; prompt box ready
  - `m4` (`After: Cycle 2 implement & EGM audit prompt`): `Implement the hybrid TrajectoryStore, isolated AgentService, and Textual A2UI v1.0 renderer, then run a second EGM review pass and verify with ruff, mypy, and pytest.`
- [ ] **`recordings/final/way-3-agy-customizations.cast` (Act 4 Part 1 · 4 stop points)**
  - `m1` (`Before: /agy-customizations synthesis prompt`): `agy` prompt box empty
  - `m2` (`After: /agy-customizations synthesis prompt`): `/agy-customizations Please turn what we learned building and reviewing our A2UI v1.0 Textual renderer and Antigravity SDK integration into a reusable workspace skill`
  - `m3` (`Before: Phase 3 cold-session verification prompt`): `.agents/skills/a2ui-textual/` synthesised and registered; cold-session prompt box empty
  - `m4` (`After: Phase 3 cold-session verification prompt`): `Build an A2UI v1.0 surface for our Python Textual TUI that compares Skill Activations across Way 1 plugins, Way 2 community skills, and Way 3 bespoke skills with interactive tabs and a tier filter.`
- [ ] **`recordings/final/way-3-brain-explorer-payoff.cast` (Act 4 Part 2 · 6 stop points)**
  - `m1` (`Before: CLI sessions overview command`): `zsh` prompt ready
  - `m2` (`After: CLI sessions overview command`): `uv run brain-explorer sessions --project skills-three-ways-akl`
  - `m3` (`Before: Launch Brain Explorer TUI command`): CLI sessions table rendered; `zsh` prompt ready
  - `m4` (`After: Launch Brain Explorer TUI command`): `uv run brain-explorer`
  - `m5` (`Before: In-TUI A2UI v1.0 prompt`): **Brain Explorer** TUI open (`Ctrl+B` sidebar browsed), `/` prompt input focused and empty
  - `m6` (`After: In-TUI A2UI v1.0 prompt`): `Compare how Way 1 plugin skills, Way 2 community skills, and Way 3 bespoke skills were activated across our Brain Explorer build sessions, and group them into an interactive A2UI v1.0 tabbed breakdown.`

### 1.3 Sync Cast Recordings into Slidev
- [ ] Run `npm --prefix slides run sync-casts` and confirm all 6 `.cast` files (`what-are-agent-skills.cast` + the 5 Act 2–4 recordings) are present in `slides/public/casts/`.

---

## Phase 2: Author Acts 2–4 Slidev Files (`slides/acts/`) & Wire `slides/slides.md`

Implement the 23 locked slides across Acts 2–4 per [Lock the slide-by-slide layout blueprint and speaker notes for Acts 2–4 in slides/acts/](https://github.com/domesticmouse/skills-three-ways-akl/issues/8), following `/slidev-deck` and `/bjm-voice`.

- [ ] **Author `slides/acts/02-way-1-plugins.md` (~8 mins, 6 slides: `S2-01`–`S2-06`)**
  - `S2-01` (`layout: center`): Way 1 Act Divider
  - `S2-02` (`layout: default`): *What Official Plugins Bring to the Table*
  - `S2-03` (`layout: cast-full`): `/casts/way-1-plugins-setup.cast`
  - `S2-04` (`layout: skill-breakdown`, `way: 1`): *Inside `google-antigravity-sdk`: In-Process Agent & `LocalAgentConfig`*
  - `S2-05` (`layout: skill-breakdown`, `way: 1`): *Inside the EGM Plugin: Specialist Review Subagents*
  - `S2-06` (`layout: default`): *Way 1 Takeaway: Guardrails Before We Write a Line of Python*
- [ ] **Author `slides/acts/03-way-2-community.md` (~10 mins, 8 slides: `S3-01`–`S3-08`)**
  - `S3-01` (`layout: center`): Way 2 Act Divider
  - `S3-02` (`layout: default`): *Evaluating Community Skills with `find-skills`*
  - `S3-03` (`layout: cast-full`): `/casts/way-2-find-skills.cast`
  - `S3-04` (`layout: skill-breakdown`, `way: 2`): *What We Installed vs. The Gap We Found*
  - `S3-05` (`layout: default`): *EGM Cycle 1: Naive Full-Delegation vs. Hybrid Architecture* (2-column red/emerald split)
  - `S3-06` (`layout: cast-full`): `/casts/way-2-egm-cycle.cast`
  - `S3-07` (`layout: skill-breakdown`, `way: mashup`): *EGM Cycle 2 Part 1: A2UI v1.0 Protocol & Schema Traps*
  - `S3-08` (`layout: skill-breakdown`, `way: mashup`): *EGM Cycle 2 Part 2: Textual Widget & Runtime Isolation Traps*
- [ ] **Author `slides/acts/04-way-3-bespoke.md` (~12 mins, 9 slides: `S4-01`–`S4-09`)**
  - `S4-01` (`layout: center`): Way 3 Act Divider
  - `S4-02` (`layout: default`): *Bespoke Skills Already Powering This Repo*
  - `S4-03` (`layout: cast-full`): `/casts/way-3-agy-customizations.cast`
  - `S4-04` (`layout: skill-breakdown`, `way: 3`): *Inside `.agents/skills/a2ui-textual/SKILL.md` (Tiers 1 & 2)*
  - `S4-05` (`layout: skill-breakdown`, `way: 3`): *Inside `references/a2ui-v1-textual-gotchas.md` (Tier 3 Deep Context)*
  - `S4-06` (`layout: cast-full`): `/casts/way-3-brain-explorer-payoff.cast`
  - `S4-07` (`layout: skill-breakdown`, `way: mashup`): *What Brain Explorer Revealed: 4 Build Trajectories Across Three Ways*
  - `S4-08` (`layout: default`): *Skills Three Ways: Choosing the Right Tier for the Job*
  - `S4-09` (`layout: default`): *Links & Resources*
- [ ] **Wire `slides/slides.md`**: Append `src: ./acts/02-way-1-plugins.md`, `src: ./acts/03-way-2-community.md`, and `src: ./acts/04-way-3-bespoke.md`.
- [ ] **Formatting & Voice Audit**:
  - Confirm every slide has a unique `<!-- S#-## -->` anchor tag, clean `<h2>` flex header (or dedicated layout title), and `<ol>` numbered concept lists where specified.
  - Confirm all fenced code blocks inside HTML `<div>` containers sit flush at column 0 with blank lines above and below.
  - Confirm Australian English spelling (`realise`, `colour`, `labelled`, `organisation`, `modelled`) and conversational speaker notes with zero bracketed stage directions (`[Click]`, `[Next slide]`).

---

## Phase 3: Slidev Verification, Stage Rehearsal & Deployment

- [ ] **Preview Local Slidev Deck**:
  - Start the dev server via `.agents/skills/slidev-deck/scripts/slides-server.sh start` and confirm `RUNNING` (`HTTP: 200` / `304`) via `status`.
  - Inspect all 36 slides across `http://localhost:3030/`, `/presenter` (speaker notes + timer), and `/overview`.
  - Test `[` / `]` / `p` chapter navigation and playback timing (`<= 30s` per segment at `speed: 2.0`) across all 6 embedded `.cast` players.
- [ ] **Verify Static Production Build**:
  - Run `npm --prefix slides run build` and confirm exit code `0` producing `slides/dist/index.html`.
- [ ] **Configure Automated GitHub Pages Deployment**:
  - Create `.github/workflows/deploy-slides.yml` from `.agents/skills/slidev-deck/resources/deploy-slides.yml` with `on.push.paths` covering `'slides/**'` and `'recordings/final/**'`.
  - Verify repository GitHub Pages settings use **Build and deployment > Source: GitHub Actions**.
- [ ] **Final Repo Hygiene & Map Closure**:
  - Run `uv run ruff check src tests`, `uv run mypy src`, and `uv run pytest -v` to confirm **Brain Explorer** checks remain green on `main`.
  - Update `README.md` with setup and run instructions for **Brain Explorer** and the Slidev deck.
  - Do a timed dry run (~35 mins talk + 5 mins Q&A) and close [Skills Three Ways: DevFest Auckland 2026 Talk & Brain Explorer App](https://github.com/domesticmouse/skills-three-ways-akl/issues/1).
