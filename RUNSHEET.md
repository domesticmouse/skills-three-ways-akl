# Recording Run Runsheet — Skills Three Ways (`asciinema`)

Operator runsheet for recording, sanitising, trimming, chapter-marking, curating, and syncing the `.cast` files for the **Skills Three Ways** talk (DevFest Auckland 2026), derived from [`TODO.md`](TODO.md), [`GLOSSARY.md`](GLOSSARY.md), and the `slidev-deck` skill.

---

## 1. Recording Manifest

| # | Cast File (`recordings/final/`) | Act & File | Slide ID | Target Session Trajectory | `"m"` Stop Points | Status |
| :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| 0 | `what-are-agent-skills.cast` | Act 1 (`slides/acts/01-primer.md`) | `S1-05` | Standalone primer (*What are agent skills?*) | 0 | Complete (synced) |
| 1 | `way-1-plugins-setup.cast` | Act 2 (`slides/acts/02-way-1-plugins.md`) | `S2-03` | **Trajectory 1** — Way 1 Plugin Discovery | 6 (`m1`–`m6`) | Pending |
| 2 | `way-2-find-skills.cast` | Act 3 Part 1 (`slides/acts/03-way-2-community.md`) | `S3-03` | **Trajectory 2** — Way 2 Skill Evaluation | 4 (`m1`–`m4`) | Pending |
| 3 | `way-2-egm-cycle.cast` | Act 3 Part 2 (`slides/acts/03-way-2-community.md`) | `S3-06` | **Trajectory 3** — Two-Pass EGM Build Cycle (+ 8 **EGM** subagent trajectories) | 4 (`m1`–`m4`) | Pending |
| 4 | `way-3-agy-customizations.cast` | Act 4 Part 1 (`slides/acts/04-way-3-bespoke.md`) | `S4-03` | **Trajectory 4** — Way 3 Synthesis & Cold Verification | 4 (`m1`–`m4`) | Pending |
| 5 | `way-3-brain-explorer-payoff.cast` | Act 4 Part 2 (`slides/acts/04-way-3-bespoke.md`) | `S4-06` | **Brain Explorer** CLI & TUI Payoff (reads Trajectories 1–4) | 6 (`m1`–`m6`) | Pending |

- **Total Act 2–4 stop points**: **24** paired **Before / After** `"m"` chapter markers (`6 + 4 + 4 + 4 + 6`).

---

## 2. Pre-Flight Environment & Post-Processing Pipeline

### Terminal & Repo Setup

1. **Terminal geometry**: Open **Ghostty** (`xterm-ghostty`) sized to **116 columns × 30 rows** (`cols: 116`, `rows: 30`) so every Act 2–4 recording matches `what-are-agent-skills.cast`.
2. **Working directory**: Start every recording from the repository root:
   ```bash
   cd /Users/brett/Documents/GitHub/skills-three-ways-akl
   ```
3. **Clean baseline check**:
   ```bash
   git status
   uv run ruff check src tests
   uv run mypy src
   uv run pytest -v
   ```
4. **Recording directory check**: Ensure `recordings/final/` exists (`ls -la recordings/final/`).

### Paired Before / After Chapter Marker Convention

`AsciinemaPlayer.vue` sets `pauseOnMarkers: true` whenever `"m"` markers exist, splits the recording into segments bounded by those markers, and accelerates each segment to `>= speed` (default `2.0x`) so it completes within `maxSegmentDuration` (`30s`).

During delivery, every command or prompt uses a **Before / After** pair:
- **Before (`m1`, `m3`, `m5`)**: Clean, empty prompt (`zsh` prompt or empty `>` / `/` input box). Pause here while explaining what you are about to ask.
- **After (`m2`, `m4`, `m6`)**: Full command or prompt pasted/typed in normal video with the cursor at the end of the line (before execution output starts). Advance once with `]` to show the prompt clearly, then hit `]` (or `p`) again to watch execution play at accelerated speed up to the next clean prompt.

### Standard Post-Processing Pipeline (Per `.cast` File)

After finishing each take, run the `/asciinema` skill utilities in order on the canonical file in `recordings/final/`:

1. **Sanitise secrets**:
   ```bash
   sanitize-cast.py recordings/final/<name>.cast
   ```
2. **Strip trailing shell exit prompts**:
   ```bash
   trim-cast.py recordings/final/<name>.cast --in-place
   ```
3. **Inspect timestamps / duration** (also useful for multi-take `~/.gemini` correlation):
   ```bash
   trim-cast.py recordings/final/<name>.cast --info
   ```
4. **Place and verify `"m"` chapter markers**:
   ```bash
   mark-cast.py recordings/final/<name>.cast --set ...
   mark-cast.py recordings/final/<name>.cast --list
   ```
   > `mark-cast.py` handles `zsh` bracketed paste automatically—advancing past reverse-video `[REV]` to the un-reversed `[UNREV]` frame and splitting trailing `\x1b[1B\r\x1b[K` into a post-marker `"o"` event (`dt=0.02s`) so the cursor stays on the same line—and advances past consecutive `dt = 0.0` synchronized TUI frame chunks.

---

## 3. Recording Runbook (Recordings 0–5)

### Recording 0 (Reference — Complete): `what-are-agent-skills.cast`

- **Act & Slide**: Act 1 (`slides/acts/01-primer.md`), Slide `S1-05` (*Asking Antigravity: What Are Agent Skills?*)
- **Recorded Environment**: `xterm-ghostty` (`116x30`), `asciicast` v3, 604 events, no `"m"` markers.
- **Sync Status**: Already present in `recordings/final/what-are-agent-skills.cast` and `slides/public/casts/what-are-agent-skills.cast`.

---

### Recording 1: `recordings/final/way-1-plugins-setup.cast`

- **Act & Slide**: Act 2 (`slides/acts/02-way-1-plugins.md`) · Slide `S2-03`
- **Target Trajectory**: **Trajectory 1 — Way 1 Plugin Discovery**
- **Expected Skill Activations**: `plugin` / `google-antigravity-sdk` (`way_1_plugin`)
- **Stop Points**: 6 (`m1`–`m6`)

#### Start Recording

```bash
asciinema rec recordings/final/way-1-plugins-setup.cast
```

#### Action Sequence & Copy-Pasteable Prompts

1. Wait on the clean initial `zsh` prompt (`m1`).
2. Paste and run the `find-skills` global install command (`m2` sits on the command text before output):
   ```bash
   npx skills add vercel-labs/skills@find-skills -g -y
   ```
3. Wait for `find-skills` installation to complete and return to a clean `zsh` prompt (`m3`).
4. Type `agy` and press `Enter` (`m4` sits on `agy` before launch):
   ```bash
   agy
   ```
5. Wait until the `agy` banner finishes loading and the `>` prompt box is empty (`m5`).
6. Paste and submit the Way 1 verification prompt (`m6` sits on the entered prompt text):
   ```text
   /plugin Please check that the Google Antigravity SDK plugin (google-antigravity-sdk) and the EGM review subagents are enabled for this workspace, and show me what skills and specialist agents they provide.
   ```
7. Wait for `agy` to list the enabled skills and **EGM** specialist review subagents and return to an idle `>` prompt.
8. Exit `agy`, then exit the recorded shell (`exit`).

#### Chapter Stop Points (`m1`–`m6`)

| Marker | Chapter Label | Terminal State at Marker |
| :--- | :--- | :--- |
| `m1` | `Before: Install find-skills` | Initial `zsh` prompt ready |
| `m2` | `After: Install find-skills` | `npx skills add vercel-labs/skills@find-skills -g -y` |
| `m3` | `Before: Launch agy` | `find-skills` installation finished; `zsh` prompt ready |
| `m4` | `After: Launch agy` | `agy` |
| `m5` | `Before: Verify Way 1 plugins prompt` | `agy` banner loaded and `>` prompt box empty |
| `m6` | `After: Verify Way 1 plugins prompt` | `/plugin Please check that the Google Antigravity SDK plugin (google-antigravity-sdk) and the EGM review subagents are enabled for this workspace, and show me what skills and specialist agents they provide.` |

#### Post-Process

```bash
sanitize-cast.py recordings/final/way-1-plugins-setup.cast
trim-cast.py recordings/final/way-1-plugins-setup.cast --in-place
# Place m1..m6 using mark-cast.py --set, then verify:
mark-cast.py recordings/final/way-1-plugins-setup.cast --list
```

---

### Recording 2: `recordings/final/way-2-find-skills.cast`

- **Act & Slide**: Act 3 Part 1 (`slides/acts/03-way-2-community.md`) · Slide `S3-03`
- **Target Trajectory**: **Trajectory 2 — Way 2 Skill Evaluation**
- **Expected Skill Activations**: `find-skills` (`way_2_community`)
- **Stop Points**: 4 (`m1`–`m4`)

#### Start Recording

Launch directly into a fresh `agy` session (or start `asciinema rec` and run `agy`, placing `m1` after the banner settles):

```bash
asciinema rec -c agy recordings/final/way-2-find-skills.cast
```

#### Action Sequence & Copy-Pasteable Prompts

1. Wait until the `agy` prompt box is empty (`m1`).
2. Paste and submit the discovery prompt (`m2`):
   ```text
   We want to build Brain Explorer—a Python CLI and Textual TUI powered by the Google Antigravity SDK to inspect our ~/.gemini session trajectories. Use find-skills to search for Python and Textual TUI skills.
   ```
3. Wait for `npx skills find python` and `npx skills find textual` evaluation output to finish and the `>` prompt box to be ready (`m3`).
4. Paste and submit the installation prompt (`m4`):
   ```text
   Let's install the Python development skills from wshobson/agents into this repo so our agents follow uv, strict typing, async, and testing conventions.
   ```
5. Wait for the `wshobson/agents` Python skills installation and summary to complete and return to an idle `>` prompt.
6. Exit `agy`.

#### Chapter Stop Points (`m1`–`m4`)

| Marker | Chapter Label | Terminal State at Marker |
| :--- | :--- | :--- |
| `m1` | `Before: Search Python & Textual skills prompt` | `agy` prompt box empty |
| `m2` | `After: Search Python & Textual skills prompt` | `We want to build Brain Explorer—a Python CLI and Textual TUI powered by the Google Antigravity SDK to inspect our ~/.gemini session trajectories. Use find-skills to search for Python and Textual TUI skills.` |
| `m3` | `Before: Install wshobson/agents Python skills prompt` | `npx skills find python` and `npx skills find textual` evaluation complete; prompt box ready |
| `m4` | `After: Install wshobson/agents Python skills prompt` | `Let's install the Python development skills from wshobson/agents into this repo so our agents follow uv, strict typing, async, and testing conventions.` |

#### Post-Process

```bash
sanitize-cast.py recordings/final/way-2-find-skills.cast
trim-cast.py recordings/final/way-2-find-skills.cast --in-place
# Place m1..m4 using mark-cast.py --set, then verify:
mark-cast.py recordings/final/way-2-find-skills.cast --list
```

---

### Recording 3: `recordings/final/way-2-egm-cycle.cast`

- **Act & Slide**: Act 3 Part 2 (`slides/acts/03-way-2-community.md`) · Slide `S3-06`
- **Target Trajectory**: **Trajectory 3 — Two-Pass EGM Build Cycle** (plus Cycle 1 & Cycle 2 **EGM** subagent trajectories)
- **Expected Skill Activations**:
  - `way_1_plugin`: `google-antigravity-sdk` + `egm-*` (`egm-design`, `egm-zoom-out`, `egm-codebase-details`, `egm-implementation-readiness`)
  - `way_2_community`: `wshobson/agents` Python skills
  - `way_3_bespoke`: `agy-brain-explorer`
- **Stop Points**: 4 (`m1`–`m4`)

#### Start Recording

```bash
asciinema rec -c agy recordings/final/way-2-egm-cycle.cast
```

#### Action Sequence & Copy-Pasteable Prompts

1. Wait until the `agy` prompt box is empty (`m1`).
2. Paste and submit the Cycle 1 design & **EGM** audit prompt (`m2`):
   ```text
   Using google-antigravity-sdk, agy-brain-explorer, and our Python skills, design a Brain Explorer Python CLI and Textual TUI that inspects ~/.gemini session trajectories and skill activations, then run an EGM review cycle (egm-design, egm-zoom-out, egm-codebase-details, egm-implementation-readiness) on the design.
   ```
3. Wait for Cycle 1's four **EGM** subagents and resolution summary to render completely and return to an idle `>` prompt (`m3`).
4. Paste and submit the Cycle 2 implement, **EGM** audit, and verification prompt (`m4`):
   ```text
   Implement the hybrid TrajectoryStore, isolated AgentService, and Textual A2UI v1.0 renderer, then run a second EGM review pass and verify with ruff, mypy, and pytest.
   ```
5. Wait for implementation, the second **EGM** pass, and `ruff` / `mypy` / `pytest` output to complete cleanly and return to an idle `>` prompt.
6. Exit `agy`.

> [!NOTE]
> Even though Cycle 1 and Cycle 2 take several minutes in real time, `AsciinemaPlayer.vue` automatically computes a higher segment playback multiplier so each segment between `m1`–`m4` finishes in `<= 30s` on stage.

#### Chapter Stop Points (`m1`–`m4`)

| Marker | Chapter Label | Terminal State at Marker |
| :--- | :--- | :--- |
| `m1` | `Before: Cycle 1 design & EGM audit prompt` | `agy` prompt box empty |
| `m2` | `After: Cycle 1 design & EGM audit prompt` | `Using google-antigravity-sdk, agy-brain-explorer, and our Python skills, design a Brain Explorer Python CLI and Textual TUI that inspects ~/.gemini session trajectories and skill activations, then run an EGM review cycle (egm-design, egm-zoom-out, egm-codebase-details, egm-implementation-readiness) on the design.` |
| `m3` | `Before: Cycle 2 implement & EGM audit prompt` | Cycle 1 resolution summary rendered; prompt box ready |
| `m4` | `After: Cycle 2 implement & EGM audit prompt` | `Implement the hybrid TrajectoryStore, isolated AgentService, and Textual A2UI v1.0 renderer, then run a second EGM review pass and verify with ruff, mypy, and pytest.` |

#### Post-Process

```bash
sanitize-cast.py recordings/final/way-2-egm-cycle.cast
trim-cast.py recordings/final/way-2-egm-cycle.cast --in-place
# Place m1..m4 using mark-cast.py --set, then verify:
mark-cast.py recordings/final/way-2-egm-cycle.cast --list
```

---

### Recording 4: `recordings/final/way-3-agy-customizations.cast`

- **Act & Slide**: Act 4 Part 1 (`slides/acts/04-way-3-bespoke.md`) · Slide `S4-03`
- **Target Trajectory**: **Trajectory 4 — Way 3 Synthesis & Cold Verification**
- **Expected Skill Activations**:
  - `way_1_plugin`: `agy-customizations`
  - `way_2_community`: `writing-for-agents`
  - `way_3_bespoke`: `a2ui-textual` (reading `SKILL.md` and `references/a2ui-v1-textual-gotchas.md`)
- **Stop Points**: 4 (`m1`–`m4`)

#### Start Recording

Start inside a shell so you can run Phase 2 synthesis in one `agy` session, quit, and launch a **cold `agy` session** for Phase 3 verification without breaking the recording:

```bash
asciinema rec recordings/final/way-3-agy-customizations.cast
```

#### Action Sequence & Copy-Pasteable Prompts

1. Launch `agy` and wait until the `>` prompt box is empty (`m1`).
2. Paste and submit the Phase 2 synthesis prompt (`m2`):
   ```text
   /agy-customizations Please turn what we learned building and reviewing our A2UI v1.0 Textual renderer and Antigravity SDK integration into a reusable workspace skill
   ```
3. Wait until `.agents/skills/a2ui-textual/` (`SKILL.md` and `references/a2ui-v1-textual-gotchas.md`) is synthesised and registered.
4. **Exit `agy` and immediately launch a brand-new `agy` session** so Phase 3 starts with an empty context window. Wait until the cold-session `>` prompt box is empty (`m3`).
5. Paste and submit the Phase 3 cold-session verification prompt (`m4`):
   ```text
   Build an A2UI v1.0 surface for our Python Textual TUI that compares Skill Activations across Way 1 plugins, Way 2 community skills, and Way 3 bespoke skills with interactive tabs and a tier filter.
   ```
6. Wait for semantic routing to activate `a2ui-textual` (Tier 2 `SKILL.md` + Tier 3 `references/a2ui-v1-textual-gotchas.md`) and finish verification.
7. Exit `agy`, then exit the recorded shell (`exit`).

#### Chapter Stop Points (`m1`–`m4`)

| Marker | Chapter Label | Terminal State at Marker |
| :--- | :--- | :--- |
| `m1` | `Before: /agy-customizations synthesis prompt` | `agy` prompt box empty |
| `m2` | `After: /agy-customizations synthesis prompt` | `/agy-customizations Please turn what we learned building and reviewing our A2UI v1.0 Textual renderer and Antigravity SDK integration into a reusable workspace skill` |
| `m3` | `Before: Phase 3 cold-session verification prompt` | `.agents/skills/a2ui-textual/` synthesised and registered; cold-session prompt box empty |
| `m4` | `After: Phase 3 cold-session verification prompt` | `Build an A2UI v1.0 surface for our Python Textual TUI that compares Skill Activations across Way 1 plugins, Way 2 community skills, and Way 3 bespoke skills with interactive tabs and a tier filter.` |

#### Post-Process

```bash
sanitize-cast.py recordings/final/way-3-agy-customizations.cast
trim-cast.py recordings/final/way-3-agy-customizations.cast --in-place
# Place m1..m4 using mark-cast.py --set, then verify:
mark-cast.py recordings/final/way-3-agy-customizations.cast --list
```

---

### Recording 5: `recordings/final/way-3-brain-explorer-payoff.cast`

- **Act & Slide**: Act 4 Part 2 (`slides/acts/04-way-3-bespoke.md`) · Slide `S4-06`
- **Target Scope**: **Brain Explorer** CLI & Textual TUI inspecting the curated canonical `~/.gemini` dataset
- **Stop Points**: 6 (`m1`–`m6`)

> [!IMPORTANT]
> Complete **Section 4 (Canonical `~/.gemini` Dataset Curation & Multi-Take Cleanup)** *before* recording `way-3-brain-explorer-payoff.cast` so the CLI table and TUI sidebar display only the 4 headline build trajectories (plus the 8 **EGM** subagent trajectories) for `skills-three-ways-akl`.

#### Start Recording

```bash
asciinema rec recordings/final/way-3-brain-explorer-payoff.cast
```

#### Action Sequence & Copy-Pasteable Prompts

1. Wait on the clean `zsh` prompt (`m1`).
2. Paste and run the **Brain Explorer** CLI sessions command (`m2`):
   ```bash
   uv run brain-explorer sessions --project skills-three-ways-akl
   ```
3. Wait for the Rich sessions table to render and return to a clean `zsh` prompt (`m3`).
4. Paste and run the **Brain Explorer** TUI entrypoint (`m4`):
   ```bash
   uv run brain-explorer
   ```
5. Inside **Brain Explorer**:
   - Browse the local Session Trajectories sidebar (select a headline trajectory to show instant deterministic local inspection, and optionally toggle the sidebar with `Ctrl+B`).
   - Press `/` to focus the prompt input box while keeping it empty (`m5`).
6. Paste and submit the A2UI v1.0 breakdown prompt (`m6`):
   ```text
   Compare how Way 1 plugin skills, Way 2 community skills, and Way 3 bespoke skills were activated across our Brain Explorer build sessions, and group them into an interactive A2UI v1.0 tabbed breakdown.
   ```
7. Wait for the Antigravity SDK agent to compose and render the interactive tabbed A2UI v1.0 surface; click across the tabs or toggle `Ctrl+I` briefly if you want to show the live A2UI v1.0 protocol & DataModel inspector.
8. Press `q` to quit **Brain Explorer**, then exit the recorded shell (`exit`).

> [!NOTE]
> `BrainExplorerAgentService` isolates `app_data_dir` and `save_dir` outside `~/.gemini`, so running live in-TUI queries during Recording 5 will not add extra trajectories to `~/.gemini`.

#### Chapter Stop Points (`m1`–`m6`)

| Marker | Chapter Label | Terminal State at Marker |
| :--- | :--- | :--- |
| `m1` | `Before: CLI sessions overview command` | `zsh` prompt ready |
| `m2` | `After: CLI sessions overview command` | `uv run brain-explorer sessions --project skills-three-ways-akl` |
| `m3` | `Before: Launch Brain Explorer TUI command` | CLI sessions table rendered; `zsh` prompt ready |
| `m4` | `After: Launch Brain Explorer TUI command` | `uv run brain-explorer` |
| `m5` | `Before: In-TUI A2UI v1.0 prompt` | **Brain Explorer** TUI open (`Ctrl+B` sidebar browsed), `/` prompt input focused and empty |
| `m6` | `After: In-TUI A2UI v1.0 prompt` | `Compare how Way 1 plugin skills, Way 2 community skills, and Way 3 bespoke skills were activated across our Brain Explorer build sessions, and group them into an interactive A2UI v1.0 tabbed breakdown.` |

#### Post-Process

```bash
sanitize-cast.py recordings/final/way-3-brain-explorer-payoff.cast
trim-cast.py recordings/final/way-3-brain-explorer-payoff.cast --in-place
# Place m1..m6 using mark-cast.py --set, then verify:
mark-cast.py recordings/final/way-3-brain-explorer-payoff.cast --list
```

---

## 4. Canonical `~/.gemini` Dataset Curation & Multi-Take Cleanup

Before recording `way-3-brain-explorer-payoff.cast`, verify that **Brain Explorer** (`TrajectoryStore`) displays only the **4 headline build trajectories** (plus the 8 Cycle 1 and Cycle 2 **EGM** review subagent trajectories) for `skills-three-ways-akl`, excluding `/wayfinder`, `/grilling`, or aborted multi-take attempts.

### Expected Canonical Dataset

| Trajectory | Associated `.cast` | Expected Skill Activations & Tiers |
| :--- | :--- | :--- |
| **Trajectory 1 — Way 1 Plugin Discovery** | `way-1-plugins-setup.cast` | `plugin` / `google-antigravity-sdk` (`way_1_plugin`) |
| **Trajectory 2 — Way 2 Skill Evaluation** | `way-2-find-skills.cast` | `find-skills` (`way_2_community`) |
| **Trajectory 3 — Two-Pass EGM Build Cycle** (+ 8 Cycle 1 & 2 **EGM** subagents) | `way-2-egm-cycle.cast` | `google-antigravity-sdk` + `egm-*` (`way_1_plugin`), `wshobson/agents` Python skills (`way_2_community`), `agy-brain-explorer` (`way_3_bespoke`) |
| **Trajectory 4 — Way 3 Synthesis & Cold Verification** | `way-3-agy-customizations.cast` | `agy-customizations` (`way_1_plugin`), `writing-for-agents` (`way_2_community`), `a2ui-textual` (`way_3_bespoke` — reading `SKILL.md` and `references/a2ui-v1-textual-gotchas.md`) |

### Multi-Take Audit & Cleanup Commands

1. **List all `skills-three-ways-akl` trajectories in `~/.gemini`**:
   ```bash
   uv run .agents/skills/agy-brain-explorer/scripts/agy-brain-explorer.py --project skills-three-ways-akl
   ```
2. **Correlate `.cast` timestamps with `~/.gemini` sessions**:
   Read the `.cast` header `"timestamp"` (Unix epoch) and raw duration (`trim-cast.py <file> --info`) and match them against `Created (Local)` and `Duration` from `agy-brain-explorer.py`.
3. **Preview and trash superseded takes or meta-planning (`/wayfinder`, `/grilling`) sessions** (moves to macOS `~/.Trash` so they remain recoverable):
   ```bash
   uv run .agents/skills/agy-brain-explorer/scripts/agy-brain-explorer.py delete <OLD_ID_1> <OLD_ID_2> --dry-run
   uv run .agents/skills/agy-brain-explorer/scripts/agy-brain-explorer.py delete <OLD_ID_1> <OLD_ID_2> --force
   ```
4. **Confirm clean output in Brain Explorer**:
   ```bash
   uv run brain-explorer sessions --project skills-three-ways-akl --limit 20
   ```

---

## 5. Slidev Sync & Stage Verification

1. **Sync all 6 `.cast` files into `slides/public/casts/`**:
   ```bash
   npm --prefix slides run sync-casts
   ls -la slides/public/casts/
   ```
   Confirm all 6 files exist:
   - `what-are-agent-skills.cast`
   - `way-1-plugins-setup.cast`
   - `way-2-find-skills.cast`
   - `way-2-egm-cycle.cast`
   - `way-3-agy-customizations.cast`
   - `way-3-brain-explorer-payoff.cast`

2. **Preview in Slidev**:
   ```bash
   .agents/skills/slidev-deck/scripts/slides-server.sh start
   .agents/skills/slidev-deck/scripts/slides-server.sh status
   ```
   - Open `http://localhost:3030/` and `http://localhost:3030/presenter`.
   - Temporarily set `showChapterBar: true` on `cast-full` slides during rehearsal to inspect chapter stepper pills (`↺ 0. Start`, `1..N`, `→ End`), adaptive speed (`>= 2.0x`), and segment durations (`<= 30s`).
   - Test stage hotkeys across all 6 players:
     - `]` — Jump to next stop point (or `→ End`)
     - `[` — Step back to previous stop point (or `↺ 0. Start`)
     - `p` — Play / Pause
   - Reset `showChapterBar: false` (or remove the override) once chapter timing is verified, then confirm the static build:
     ```bash
     npm --prefix slides run build
     ```
