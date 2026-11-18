# Recording Run Runsheet — Skills Three Ways (`asciinema`)

Operator checklist for provisioning, recording, correlating, post-processing, `pyte`-verifying, curating, and syncing the `.cast` recordings for the **Skills Three Ways** talk (DevFest Auckland 2026), aligned with [`TODO.md`](TODO.md), [`GLOSSARY.md`](GLOSSARY.md), the `slidev-deck` [ASCIINEMA-INTEGRATION.md](.agents/skills/slidev-deck/references/ASCIINEMA-INTEGRATION.md) reference, and the incremental capture patterns from `nuttxspace/EXPERIMENT_RUNBOOK.md`.

---

## 1. Recording Manifest & Incremental Workflow

Store unedited captures in `recordings/raw/` and post-processed outputs in `recordings/final/` (never mutate raw captures in place), then sync into `slides/public/casts/`.

| # | Recording (`recordings/raw/` → `recordings/final/`) | Act & File | Slide ID | Target Session Trajectory | `"m"` Stop Points | Status |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| 0 | `what-are-agent-skills.cast` | Act 1 (`slides/acts/01-primer.md`) | `S1-05` | Standalone primer (*What are agent skills?*) | 0 | Complete (synced) |
| 1 | `way-1-plugins-setup.cast` | Act 2 (`slides/acts/02-way-1-plugins.md`) | `S2-03` | **Trajectory 1** — Way 1 Plugin Discovery | 6 (`m1`–`m6`) | Pending |
| 2 | `way-2-find-skills.cast` | Act 3 Part 1 (`slides/acts/03-way-2-community.md`) | `S3-03` | **Trajectory 2** — Way 2 Skill Evaluation | 4 (`m1`–`m4`) | Pending |
| 3 | `way-2-egm-cycle.cast` | Act 3 Part 2 (`slides/acts/03-way-2-community.md`) | `S3-06` | **Trajectory 3** — Two-Pass EGM Build Cycle (+ 8 **EGM** subagent trajectories) | 4 (`m1`–`m4`) | Pending |
| 4 | `way-3-agy-customizations.cast` | Act 4 Part 1 (`slides/acts/04-way-3-bespoke.md`) | `S4-03` | **Trajectory 4** — Way 3 Synthesis & Cold Verification | 4 (`m1`–`m4`) | Pending |
| 5 | `way-3-brain-explorer-payoff.cast` | Act 4 Part 2 (`slides/acts/04-way-3-bespoke.md`) | `S4-06` | **Brain Explorer** CLI & TUI Payoff (reads Trajectories 1–4) | 6 (`m1`–`m6`) | Pending |

- **Total Act 2–4 stop points**: **24** paired **Before / After** `"m"` chapter markers (`6 + 4 + 4 + 4 + 6`).

### Incremental `Record → Correlate → Post-Process → Verify` Loop

Do **not** record all five Act 2–4 `.cast` files back-to-back before inspecting outputs. After each recording finishes:

1. **Correlate & Clean Takes**: Match `recordings/raw/<name>.cast` (`timestamp` and raw duration) against `~/.gemini/**/brain/` using [agy-brain-explorer.py](.agents/skills/agy-brain-explorer/scripts/agy-brain-explorer.py), and move any aborted or superseded takes to Trash immediately.
2. **Verify Skill Activations**: Confirm the expected **Skill Activations** (`way_1_plugin`, `way_2_community`, `way_3_bespoke`) appear cleanly in the canonical **Session Trajectory**.
3. **Sanitise, Trim, Tighten & Mark**: Produce `recordings/final/<name>.cast` from `recordings/raw/<name>.cast`, verify frame boundaries with `pyte` (`--render`), and inspect adaptive segment speeds with `mark-cast.py --list`.
4. **Log Telemetry for `S4-07`**: Fill in that recording's **Cast ↔ Trajectory Correlation Table** below so numbers are locked before building `slides/acts/04-way-3-bespoke.md` (`S4-07`).

---

## 2. Phase 0: Pre-Flight Environment, Tooling & Post-Processing Pipeline

Run these checks **before starting any recording** so missing tools, mismatched terminal dimensions, or workspace drift never derail a take mid-cast.

### 2.1 Toolchain & Directory Setup

```bash
cd /Users/brett/Documents/GitHub/skills-three-ways-akl
mkdir -p recordings/raw recordings/final

# Verify required recording, agent, Node, and Python tooling
asciinema --version
agy --version
npx --version
uv --version
python3 --version
node --version

# Verify Brain Explorer baseline and clean repo state
git status -sb
uv run ruff check src tests
uv run mypy src
uv run pytest -v
```

### 2.2 `/asciinema` Script Availability

The `/asciinema` skill and processing scripts (`sanitize-cast.py`, `trim-cast.py`, `mark-cast.py`) are installed locally in [`.agents/skills/asciinema/`](.agents/skills/asciinema/SKILL.md):

```bash
ls -la .agents/skills/asciinema/scripts/{sanitize-cast.py,trim-cast.py,mark-cast.py}
```

### 2.3 Pre-Flight Checklist

- [ ] **Terminal geometry**: Open **Ghostty** (`xterm-ghostty`) sized to **120 columns × 36 rows** (`120x36`) matching `nuttxspace/EXPERIMENT_RUNBOOK.md`.
- [ ] **CLI versions**: `asciinema` (3.x recording `asciicast v3`), `agy`, `npx`, `uv`, `python3`, and `node` verified on `PATH`.
- [ ] **`/asciinema` scripts**: `sanitize-cast.py`, `trim-cast.py`, and `mark-cast.py` accessible; `uv run --with pyte` tested cleanly.
- [ ] **Git commit anchors noted**:
  - `97ab6fc` — Domain docs, `find-skills`, and `wshobson/agents` Python skills (pre-**Brain Explorer** baseline).
  - `45d1905` — **Brain Explorer** A2UI v1.0 Textual TUI and `TrajectoryStore` implementation.
  - `f0182ab` — Bespoke `a2ui-textual` skill and `way_3_bespoke` tier registration.
  - `8b62665` — `TODO.md` checklist on `main`.
- [ ] **Workspace hygiene**: If re-recording state-mutating takes (Recordings 1–4), run in a clean scratch branch/worktree or reset transient edits between takes so `main` stays pristine for Recording 5.

### 2.4 `asciinema rec` Guardrails & Interactive Hotkeys

- **Required flags**: Always record with `-i 2.0 --window-size 120x36 --overwrite` so idle pauses cap at `2.0s`, dimensions stay locked to `120x36`, and retakes overwrite cleanly.
- **Security guardrail**: **Never** pass `-I` / `--stdin` to `asciinema rec` (keeps raw keystrokes and any typed tokens out of the `.cast`).
- **Live recording controls**:
  - `Ctrl+\`: Pause/resume capture (useful if stepping away mid-run).
  - `Ctrl+x`: Optional live `"m"` marker during capture (refined afterwards in post-processing).
  - `Ctrl+D` twice inside `agy`, then `Ctrl+D` / `exit` in `zsh`: Ends the capture cleanly.

### 2.5 Paired Before / After Chapter Marker Convention

[`AsciinemaPlayer.vue`](slides/components/AsciinemaPlayer.vue) enables `pauseOnMarkers: true` whenever `"m"` markers exist and computes per-segment playback speeds (`>= 2.0x`, completing each segment in `<= 30s`). Every command or prompt uses a **Before / After** stop-point pair:

- **Before (`m1`, `m3`, `m5`)**: Settled, empty prompt (`zsh` prompt or settled `agy` `? for shortcuts` / TUI `/` input box). Pause here to frame what you are about to ask.
- **After (`m2`, `m4`, `m6`)**: Complete command or prompt echoed in normal video (`[UNREV]`, cursor on the command line before execution output starts). Advance once with `]` to show the prompt clearly, then hit `]` (or `p`) to play execution at accelerated speed to the next settled prompt.

### 2.6 Standard Post-Processing Pipeline (Per `.cast` File)

1. **Sanitise secrets & OSC sequences** (preserves 0-based event indices `#0000..#NNNN`):
   ```bash
   python3 .agents/skills/asciinema/scripts/sanitize-cast.py \
     recordings/raw/<name>.cast recordings/final/<name>.cast
   ```
2. **Inspect timing & trailing exit sequences**:
   ```bash
   python3 .agents/skills/asciinema/scripts/trim-cast.py recordings/final/<name>.cast --info
   ```
   - For single-session captures, trim trailing exit prompts in place (`3.0s` hold):
     ```bash
     python3 .agents/skills/asciinema/scripts/trim-cast.py recordings/final/<name>.cast --in-place
     ```
   - If the cast exits `agy` mid-stream (e.g., Recording 1 or Recording 4), trim explicitly past the final action using `--cut-index <IDX> --hold 3.0` so intermediate `press ctrl+d again to exit` prompts never truncate the recording early.
3. **Locate exact event boundaries**:
   ```bash
   python3 .agents/skills/asciinema/scripts/mark-cast.py recordings/final/<name>.cast --search "<pattern>" --context 2
   python3 .agents/skills/asciinema/scripts/mark-cast.py recordings/final/<name>.cast --inspect <START>:<END>
   ```
   - Watch `[REV]` (bracketed-paste reverse video), `[UNREV]` (`Enter` redraw), and `[OSC]` tags.
   - Always place `"Before: ..."` stop points on the **settled** `? for shortcuts` frame (`dt > 1s`), never on transient `Loading...` frames.
4. **Verify 2D terminal state with `pyte` (via `uv`)**:
   ```bash
   uv run --with pyte python3 .agents/skills/asciinema/scripts/mark-cast.py \
     recordings/final/<name>.cast --render <EVENT_IDX>
   ```
   - If an unwanted mid-stream turn (e.g. a manual status check) needs excision, verify first with `--verify-strip <START>:<END>` before running `--strip-range <START>:<END> --in-place`.
5. **Tighten cut-and-paste & typing delays, place `"m"` markers & verify**:
   ```bash
   python3 .agents/skills/asciinema/scripts/mark-cast.py recordings/final/<name>.cast --tighten-pastes --in-place
   # Set/add markers with --add-event / --set, adjusting slow pauses via --set-dt <IDX> <SEC> if needed
   python3 .agents/skills/asciinema/scripts/mark-cast.py recordings/final/<name>.cast --list
   ```

---

## 3. Recording Runbook (Recordings 0–5)

### Recording 0 (Reference — Complete): `what-are-agent-skills.cast`

- **Act & Slide**: Act 1 ([`slides/acts/01-primer.md`](slides/acts/01-primer.md#L220-L233)), Slide `S1-05` (*Asking Antigravity: What Are Agent Skills?*)
- **Recorded Environment**: `xterm-ghostty` (`116x30` historical capture), `asciicast v3`, `604` events, `0` `"m"` markers (leave as-is or re-record at `120x36` if uniform geometry across all 6 slides is desired).
- **Sync Status**: Verified in [`recordings/final/what-are-agent-skills.cast`](recordings/final/what-are-agent-skills.cast) and [`slides/public/casts/what-are-agent-skills.cast`](slides/public/casts/what-are-agent-skills.cast).

---

### Recording 1: `way-1-plugins-setup.cast`

- **Act & Slide**: Act 2 (`slides/acts/02-way-1-plugins.md`) · Slide `S2-03`
- **Target Trajectory**: **Trajectory 1 — Way 1 Plugin Discovery**
- **Expected Skill Activations**: `plugin` / `google-antigravity-sdk` (`way_1_plugin`)
- **Stop Points**: 6 (`m1`–`m6`)

#### Pre-Step State Checks

- Verify `google-antigravity-sdk` and `egm` plugins are installed and enabled for `agy`, and remove any stale local `find-skills` state if you want the global `npx skills add` install to read freshly on camera.
- Confirm you are on a clean `zsh` prompt at `/Users/brett/Documents/GitHub/skills-three-ways-akl`.

#### Start Recording

```bash
asciinema rec -i 2.0 --window-size 120x36 --overwrite \
  recordings/raw/way-1-plugins-setup.cast
```

#### Action Sequence & Copy-Pasteable Prompts

1. Wait briefly on the clean initial `zsh` prompt (`m1`).
2. Paste and run (`m2` sits on the command before output):
   ```bash
   npx skills add vercel-labs/skills@find-skills -g -y
   ```
3. Wait for `find-skills` installation to finish and return to a clean `zsh` prompt (`m3`).
4. Type `agy` and press `Enter` (`m4` sits on `agy` before TUI launch):
   ```bash
   agy
   ```
5. Wait until the `agy` banner finishes loading and the `>` prompt box settles at `? for shortcuts` (`m5`).
6. Paste and submit the Way 1 verification prompt (`m6`):
   ```text
   /plugin Please check that the Google Antigravity SDK plugin (google-antigravity-sdk) and the EGM review subagents are enabled for this workspace, and show me what skills and specialist agents they provide.
   ```
7. Wait for `agy` to list the enabled `google-antigravity-sdk` skills and **EGM** specialist review subagents and settle at an idle `>` prompt.
8. Exit `agy` (`Ctrl+D` twice), then exit `zsh` (`exit` or `Ctrl+D`).

> [!NOTE]
> `trim-cast.py --info` will spot `agy`'s `press ctrl+d again to exit` / `Resume with ...` sequence right before the outer `zsh` exit. Trim cleanly past the settled `agy` response (or after the exit back to `zsh` if you prefer `agy`'s completion screen as the final held frame).

#### Chapter Stop Points (`m1`–`m6`)

| Marker | Chapter Label | Terminal State at Marker |
| :--- | :--- | :--- |
| `m1` | `Before: Install find-skills` | Initial `zsh` prompt ready |
| `m2` | `After: Install find-skills` | `npx skills add vercel-labs/skills@find-skills -g -y` |
| `m3` | `Before: Launch agy` | `find-skills` installation finished; `zsh` prompt ready |
| `m4` | `After: Launch agy` | `agy` |
| `m5` | `Before: Verify Way 1 plugins prompt` | `agy` banner loaded and `>` prompt box empty |
| `m6` | `After: Verify Way 1 plugins prompt` | `/plugin Please check that the Google Antigravity SDK plugin (google-antigravity-sdk) and the EGM review subagents are enabled for this workspace, and show me what skills and specialist agents they provide.` |

#### Post-Recording Verification Checklist

- [ ] `recordings/raw/way-1-plugins-setup.cast` saved (`120x36`, `asciicast v3`, no `-I`/`--stdin`).
- [ ] Correlated with canonical **Trajectory 1** in `~/.gemini/**/brain/`; aborted takes trashed.
- [ ] `plugin` / `google-antigravity-sdk` (`way_1_plugin`) **Skill Activation** confirmed in trajectory.
- [ ] `recordings/final/way-1-plugins-setup.cast` sanitised, trimmed, paste-tightened, `pyte`-rendered at `m1`–`m6`, and verified with `mark-cast.py --list`.

#### Cast ↔ Trajectory Correlation (Fill After Capture)

- **AGY Session**: `<UUID>` (`<brain-root>`, `<model>`), active `<HH:MM:SS>`–`<HH:MM:SS>`, `<N>` steps, `<N>` tool calls (`read_file`: `<N>`, `run_command`: `<N>`), Skill Activations: `<list>`.
- **Final Cast**: `<raw>` raw / `<1x>` 1x / `<warped>` warped (`m1` `#idx`, `m2` `#idx`, `m3` `#idx`, `m4` `#idx`, `m5` `#idx`, `m6` `#idx`).

---

### Recording 2: `way-2-find-skills.cast`

- **Act & Slide**: Act 3 Part 1 (`slides/acts/03-way-2-community.md`) · Slide `S3-03`
- **Target Trajectory**: **Trajectory 2 — Way 2 Skill Evaluation**
- **Expected Skill Activations**: `find-skills` (`way_2_community`)
- **Stop Points**: 4 (`m1`–`m4`)

#### Pre-Step State Checks

- Verify `find-skills` is active from Recording 1.
- Keep `main` or an isolated take branch clean (`97ab6fc` represents the baseline where `wshobson/agents` Python skills were added).

#### Start Recording

```bash
asciinema rec -i 2.0 --window-size 120x36 --overwrite \
  recordings/raw/way-2-find-skills.cast
```

Inside the recorded shell, launch `agy` immediately:

```bash
agy
```

#### Action Sequence & Copy-Pasteable Prompts

1. Wait until the `agy` prompt box is empty and settled at `? for shortcuts` (`m1`). *(Trim or skip past the initial `agy` launch if you want the recording to open directly on the empty `agy` prompt box, or place `m1` cleanly after `agy` settles.)*
2. Paste and submit the discovery prompt (`m2`):
   ```text
   We want to build Brain Explorer—a Python CLI and Textual TUI powered by the Google Antigravity SDK to inspect our ~/.gemini session trajectories. Use find-skills to search for Python and Textual TUI skills.
   ```
3. Wait for `npx skills find python` and `npx skills find textual` evaluation output to finish and return to the settled `>` prompt box (`m3`). *(Approve any `run_command` / `BypassSandbox` prompt if `npx skills find` requests network access.)*
4. Paste and submit the installation prompt (`m4`):
   ```text
   Let's install the Python development skills from wshobson/agents into this repo so our agents follow uv, strict typing, async, and testing conventions.
   ```
5. Wait for the `wshobson/agents` Python skills installation and summary to finish cleanly at an idle `>` prompt.
6. Exit `agy` (`Ctrl+D` twice) and exit `zsh` (`exit`).

#### Chapter Stop Points (`m1`–`m4`)

| Marker | Chapter Label | Terminal State at Marker |
| :--- | :--- | :--- |
| `m1` | `Before: Search Python & Textual skills prompt` | `agy` prompt box empty |
| `m2` | `After: Search Python & Textual skills prompt` | `We want to build Brain Explorer—a Python CLI and Textual TUI powered by the Google Antigravity SDK to inspect our ~/.gemini session trajectories. Use find-skills to search for Python and Textual TUI skills.` |
| `m3` | `Before: Install wshobson/agents Python skills prompt` | `npx skills find python` and `npx skills find textual` evaluation complete; prompt box ready |
| `m4` | `After: Install wshobson/agents Python skills prompt` | `Let's install the Python development skills from wshobson/agents into this repo so our agents follow uv, strict typing, async, and testing conventions.` |

#### Post-Recording Verification Checklist

- [ ] `recordings/raw/way-2-find-skills.cast` saved (`120x36`, `asciicast v3`).
- [ ] Correlated with canonical **Trajectory 2** in `~/.gemini/**/brain/`; aborted takes trashed.
- [ ] `find-skills` (`way_2_community`) **Skill Activation** confirmed in trajectory.
- [ ] `recordings/final/way-2-find-skills.cast` sanitised, trimmed, paste-tightened, `pyte`-rendered at `m1`–`m4`, and verified with `mark-cast.py --list`.

#### Cast ↔ Trajectory Correlation (Fill After Capture)

- **AGY Session**: `<UUID>` (`<brain-root>`, `<model>`), active `<HH:MM:SS>`–`<HH:MM:SS>`, `<N>` steps, `<N>` tool calls, Skill Activations: `<list>`.
- **Final Cast**: `<raw>` raw / `<1x>` 1x / `<warped>` warped (`m1` `#idx`, `m2` `#idx`, `m3` `#idx`, `m4` `#idx`).

---

### Recording 3: `way-2-egm-cycle.cast`

- **Act & Slide**: Act 3 Part 2 (`slides/acts/03-way-2-community.md`) · Slide `S3-06`
- **Target Trajectory**: **Trajectory 3 — Two-Pass EGM Build Cycle** (plus 8 Cycle 1 & Cycle 2 **EGM** subagent trajectories)
- **Expected Skill Activations**:
  - `way_1_plugin`: `google-antigravity-sdk` + `egm-*` (`egm-design`, `egm-zoom-out`, `egm-codebase-details`, `egm-implementation-readiness`)
  - `way_2_community`: `wshobson/agents` Python skills
  - `way_3_bespoke`: `agy-brain-explorer`
- **Stop Points**: 4 (`m1`–`m4`)

#### Pre-Step State Checks

- Verify `google-antigravity-sdk`, `egm-*` subagents, `wshobson/agents` Python skills, and `agy-brain-explorer` are available in the workspace.
- If re-recording the build over an already-implemented `main`, use a dedicated worktree/branch checked out at the pre-implementation baseline (`97ab6fc`) so **EGM** Cycle 1 and Cycle 2 run genuinely against an empty `src/brain_explorer/` rather than peeking at finished files.

#### Start Recording

```bash
asciinema rec -i 2.0 --window-size 120x36 --overwrite \
  recordings/raw/way-2-egm-cycle.cast
```

Launch `agy` directly inside the recorded shell:

```bash
agy
```

#### Action Sequence & Copy-Pasteable Prompts

1. Wait until the `agy` prompt box is empty and settled (`m1`).
2. Paste and submit the Cycle 1 design & **EGM** audit prompt (`m2`):
   ```text
   Using google-antigravity-sdk, agy-brain-explorer, and our Python skills, design a Brain Explorer Python CLI and Textual TUI that inspects ~/.gemini session trajectories and skill activations, then run an EGM review cycle (egm-design, egm-zoom-out, egm-codebase-details, egm-implementation-readiness) on the design.
   ```
3. Wait for Cycle 1's four **EGM** subagents (`egm-design`, `egm-zoom-out`, `egm-codebase-details`, `egm-implementation-readiness`) and resolution summary to finish rendering and return to an idle `>` prompt (`m3`).
4. Paste and submit the Cycle 2 implement, **EGM** audit, and verification prompt (`m4`):
   ```text
   Implement the hybrid TrajectoryStore, isolated AgentService, and Textual A2UI v1.0 renderer, then run a second EGM review pass and verify with ruff, mypy, and pytest.
   ```
5. Wait for implementation, the second **EGM** pass (4 subagents), and `uv run ruff check` / `uv run mypy` / `uv run pytest` output to finish cleanly at an idle `>` prompt.
6. Exit `agy` (`Ctrl+D` twice) and exit `zsh` (`exit`).

> [!NOTE]
> Because Cycle 1 and Cycle 2 span several minutes in real time, [`AsciinemaPlayer.vue`](slides/components/AsciinemaPlayer.vue) automatically scales the per-segment speed multiplier so every segment between `m1`–`m4` finishes within `<= 30s` on stage.

#### Chapter Stop Points (`m1`–`m4`)

| Marker | Chapter Label | Terminal State at Marker |
| :--- | :--- | :--- |
| `m1` | `Before: Cycle 1 design & EGM audit prompt` | `agy` prompt box empty |
| `m2` | `After: Cycle 1 design & EGM audit prompt` | `Using google-antigravity-sdk, agy-brain-explorer, and our Python skills, design a Brain Explorer Python CLI and Textual TUI that inspects ~/.gemini session trajectories and skill activations, then run an EGM review cycle (egm-design, egm-zoom-out, egm-codebase-details, egm-implementation-readiness) on the design.` |
| `m3` | `Before: Cycle 2 implement & EGM audit prompt` | Cycle 1 resolution summary rendered; prompt box ready |
| `m4` | `After: Cycle 2 implement & EGM audit prompt` | `Implement the hybrid TrajectoryStore, isolated AgentService, and Textual A2UI v1.0 renderer, then run a second EGM review pass and verify with ruff, mypy, and pytest.` |

#### Post-Recording Verification Checklist

- [ ] `recordings/raw/way-2-egm-cycle.cast` saved (`120x36`, `asciicast v3`).
- [ ] Correlated with canonical **Trajectory 3** parent + all **8 EGM subagent trajectories** (4 in Cycle 1 + 4 in Cycle 2) in `~/.gemini/**/brain/`; aborted takes trashed.
- [ ] `google-antigravity-sdk`, `egm-*`, `wshobson/agents` Python skills, and `agy-brain-explorer` **Skill Activations** confirmed.
- [ ] `ruff`, `mypy`, and `pytest` output green on camera.
- [ ] `recordings/final/way-2-egm-cycle.cast` sanitised, trimmed, paste-tightened, `pyte`-rendered at `m1`–`m4`, and verified with `mark-cast.py --list`.

#### Cast ↔ Trajectory Correlation (Fill After Capture)

- **AGY Sessions**: Parent `<UUID>` + 8 **EGM** subagents (`C1`: `<id1,id2,id3,id4>`; `C2`: `<id5,id6,id7,id8>`), combined `<N>` steps, `<N>` tool calls, Skill Activations: `<list>`.
- **Final Cast**: `<raw>` raw / `<1x>` 1x / `<warped>` warped (`m1` `#idx`, `m2` `#idx`, `m3` `#idx`, `m4` `#idx`).

---

### Recording 4: `way-3-agy-customizations.cast`

- **Act & Slide**: Act 4 Part 1 (`slides/acts/04-way-3-bespoke.md`) · Slide `S4-03`
- **Target Trajectory**: **Trajectory 4 — Way 3 Synthesis & Cold Verification**
- **Expected Skill Activations**:
  - `way_1_plugin`: `agy-customizations`
  - `way_2_community`: `writing-for-agents`
  - `way_3_bespoke`: `a2ui-textual` (reading `SKILL.md` and `references/a2ui-v1-textual-gotchas.md`)
- **Stop Points**: 4 (`m1`–`m4`)

#### Pre-Step State Checks

- Start from the implemented **Brain Explorer** codebase (`45d1905`) prior to `.agents/skills/a2ui-textual/` (`f0182ab`) if re-running synthesis live, or ensure `.agents/skills/a2ui-textual/` is not pre-cached in the Phase 2 conversation context.

#### Start Recording

Start inside `zsh` so you can exit the Phase 2 `agy` session after `m2` and launch a **cold `agy` session** for Phase 3 (`m3`–`m4`) in one continuous cast:

```bash
asciinema rec -i 2.0 --window-size 120x36 --overwrite \
  recordings/raw/way-3-agy-customizations.cast
```

#### Action Sequence & Copy-Pasteable Prompts

1. Launch `agy` and wait until the `>` prompt box is empty and settled (`m1`).
2. Paste and submit the Phase 2 synthesis prompt (`m2`):
   ```text
   /agy-customizations Please turn what we learned building and reviewing our A2UI v1.0 Textual renderer and Antigravity SDK integration into a reusable workspace skill
   ```
3. Wait until `.agents/skills/a2ui-textual/` (`SKILL.md` and `references/a2ui-v1-textual-gotchas.md`) is synthesised and registered.
4. **Exit `agy` (`Ctrl+D` twice) and immediately launch a brand-new `agy` session** so Phase 3 starts with a completely empty context window. Wait until the cold-session `>` prompt box is empty and settled (`m3`).
5. Paste and submit the Phase 3 cold-session verification prompt (`m4`):
   ```text
   Build an A2UI v1.0 surface for our Python Textual TUI that compares Skill Activations across Way 1 plugins, Way 2 community skills, and Way 3 bespoke skills with interactive tabs and a tier filter.
   ```
6. Wait for semantic routing to activate `a2ui-textual` (Tier 2 `SKILL.md` + Tier 3 `references/a2ui-v1-textual-gotchas.md`) and complete verification cleanly.
7. Exit `agy` (`Ctrl+D` twice), then exit `zsh` (`exit`).

> [!WARNING]
> **`trim-cast.py` pitfall on `way-3-agy-customizations.cast`**: Exiting the Phase 2 `agy` session between `m2` and `m3` emits a mid-stream `press ctrl+d again to exit` / `Resume with ...` sequence inside `recordings/raw/way-3-agy-customizations.cast`. Do **not** auto-truncate at that mid-recording exit; run `trim-cast.py --info` first and pass `--cut-index <FINAL_EXIT_IDX> --hold 3.0` so all Phase 3 cold-session events (`m3`–`m4`) are preserved!

#### Chapter Stop Points (`m1`–`m4`)

| Marker | Chapter Label | Terminal State at Marker |
| :--- | :--- | :--- |
| `m1` | `Before: /agy-customizations synthesis prompt` | `agy` prompt box empty |
| `m2` | `After: /agy-customizations synthesis prompt` | `/agy-customizations Please turn what we learned building and reviewing our A2UI v1.0 Textual renderer and Antigravity SDK integration into a reusable workspace skill` |
| `m3` | `Before: Phase 3 cold-session verification prompt` | `.agents/skills/a2ui-textual/` synthesised and registered; cold-session prompt box empty |
| `m4` | `After: Phase 3 cold-session verification prompt` | `Build an A2UI v1.0 surface for our Python Textual TUI that compares Skill Activations across Way 1 plugins, Way 2 community skills, and Way 3 bespoke skills with interactive tabs and a tier filter.` |

#### Post-Recording Verification Checklist

- [ ] `recordings/raw/way-3-agy-customizations.cast` saved (`120x36`, `asciicast v3`), capturing both Phase 2 synthesis (`m1`–`m2`) and Phase 3 cold verification (`m3`–`m4`).
- [ ] Correlated with canonical **Trajectory 4** session(s) in `~/.gemini/**/brain/`; aborted takes trashed.
- [ ] `agy-customizations` (`way_1_plugin`), `writing-for-agents` (`way_2_community`), and `a2ui-textual` (`way_3_bespoke`, reading `SKILL.md` and `references/a2ui-v1-textual-gotchas.md`) **Skill Activations** confirmed.
- [ ] `recordings/final/way-3-agy-customizations.cast` sanitised, trimmed past Phase 3 exit only (not mid-stream Phase 2 exit), paste-tightened, `pyte`-rendered at `m1`–`m4`, and verified with `mark-cast.py --list`.

#### Cast ↔ Trajectory Correlation (Fill After Capture)

- **AGY Session(s)**: Phase 2 `<UUID>` + Phase 3 cold `<UUID>`, combined `<N>` steps, `<N>` tool calls, Skill Activations: `<list>`.
- **Final Cast**: `<raw>` raw / `<1x>` 1x / `<warped>` warped (`m1` `#idx`, `m2` `#idx`, `m3` `#idx`, `m4` `#idx`).

---

### Recording 5: `way-3-brain-explorer-payoff.cast`

- **Act & Slide**: Act 4 Part 2 (`slides/acts/04-way-3-bespoke.md`) · Slide `S4-06`
- **Target Scope**: **Brain Explorer** CLI & Textual TUI inspecting the curated canonical `~/.gemini` dataset
- **Stop Points**: 6 (`m1`–`m6`)

> [!IMPORTANT]
> Complete **Section 4 (Canonical `~/.gemini` Dataset Curation & Multi-Take Cleanup)** *before* recording `way-3-brain-explorer-payoff.cast` so [`cli.py`](src/brain_explorer/cli.py) and [`tui.py`](src/brain_explorer/tui.py) display **only** the 4 headline build trajectories (plus the 8 Cycle 1 & Cycle 2 **EGM** review subagent trajectories) for `skills-three-ways-akl`.

#### Pre-Step State Checks

- `main` is clean and tests pass (`uv run ruff check src tests`, `uv run mypy src`, `uv run pytest -v`).
- `uv run brain-explorer sessions --project skills-three-ways-akl --limit 20` prints the exact curated canonical dataset with zero `/wayfinder`, `/grilling`, or aborted-take noise.

#### Start Recording

```bash
asciinema rec -i 2.0 --window-size 120x36 --overwrite \
  recordings/raw/way-3-brain-explorer-payoff.cast
```

#### Action Sequence & Copy-Pasteable Prompts

1. Wait briefly on the clean `zsh` prompt (`m1`).
2. Paste and run the **Brain Explorer** CLI sessions overview command (`m2`):
   ```bash
   uv run brain-explorer sessions --project skills-three-ways-akl
   ```
3. Wait for the Rich sessions table to render and return to a clean `zsh` prompt (`m3`).
4. Paste and run the **Brain Explorer** TUI entrypoint (`m4`):
   ```bash
   uv run brain-explorer
   ```
5. Inside **Brain Explorer**:
   - Browse the local **Session Trajectories** sidebar (`Ctrl+B` toggles sidebar visibility; selecting an entry loads deterministic local detail).
   - Press `/` to focus the `#prompt-input` box while leaving it empty (`m5`).
6. Paste and submit (`Enter` or click `Ask Agent`) the A2UI v1.0 tabbed comparison prompt (`m6`):
   ```text
   Compare how Way 1 plugin skills, Way 2 community skills, and Way 3 bespoke skills were activated across our Brain Explorer build sessions, and group them into an interactive A2UI v1.0 tabbed breakdown.
   ```
7. Wait for the in-process `google-antigravity` SDK agent to compose and render the interactive tabbed A2UI v1.0 surface; click across the tabs (or briefly toggle `Ctrl+I` to show the live A2UI v1.0 protocol & DataModel inspector).
8. Press `q` to quit **Brain Explorer**, then exit `zsh` (`exit`).

> [!NOTE]
> `BrainExplorerAgentService` isolates `app_data_dir` and `save_dir` outside `~/.gemini`, so live in-TUI queries during Recording 5 will **not** pollute `~/.gemini` with extra Session Trajectories.

#### Chapter Stop Points (`m1`–`m6`)

| Marker | Chapter Label | Terminal State at Marker |
| :--- | :--- | :--- |
| `m1` | `Before: CLI sessions overview command` | `zsh` prompt ready |
| `m2` | `After: CLI sessions overview command` | `uv run brain-explorer sessions --project skills-three-ways-akl` |
| `m3` | `Before: Launch Brain Explorer TUI command` | CLI sessions table rendered; `zsh` prompt ready |
| `m4` | `After: Launch Brain Explorer TUI command` | `uv run brain-explorer` |
| `m5` | `Before: In-TUI A2UI v1.0 prompt` | **Brain Explorer** TUI open (`Ctrl+B` sidebar browsed), `/` prompt input focused and empty |
| `m6` | `After: In-TUI A2UI v1.0 prompt` | `Compare how Way 1 plugin skills, Way 2 community skills, and Way 3 bespoke skills were activated across our Brain Explorer build sessions, and group them into an interactive A2UI v1.0 tabbed breakdown.` |

#### Post-Recording Verification Checklist

- [ ] `recordings/raw/way-3-brain-explorer-payoff.cast` saved (`120x36`, `asciicast v3`).
- [ ] CLI table and TUI sidebar display only the curated canonical dataset (zero meta-planning or aborted-take sessions).
- [ ] A2UI v1.0 tabbed breakdown renders cleanly without terminal corruption (`configure_sdk_logging()` active).
- [ ] `recordings/final/way-3-brain-explorer-payoff.cast` sanitised, trimmed, paste-tightened, `pyte`-rendered at `m1`–`m6`, and verified with `mark-cast.py --list`.

#### Cast ↔ Trajectory Correlation (Fill After Capture)

- **Dataset Verified**: 4 headline trajectories + 8 **EGM** subagents rendered in `brain-explorer sessions --project skills-three-ways-akl`.
- **Final Cast**: `<raw>` raw / `<1x>` 1x / `<warped>` warped (`m1` `#idx`, `m2` `#idx`, `m3` `#idx`, `m4` `#idx`, `m5` `#idx`, `m6` `#idx`).

---

## 4. Per-Recording Audit Prompt & Canonical `~/.gemini` Curation

### 4.1 Copy-Pasteable Post-Recording Audit & Post-Processing Prompt

Run this prompt in `agy` inside `/Users/brett/Documents/GitHub/skills-three-ways-akl` immediately after each recording (approve `BypassSandbox` so `/agy-brain-explorer` can inspect `~/.gemini/**/brain/`):

```text
/agy-brain-explorer /asciinema I just finished capturing `recordings/raw/<name>.cast` in `/Users/brett/Documents/GitHub/skills-three-ways-akl`. Before I move to the next recording:

1. Discover all `~/.gemini/**/brain/` Session Trajectories for `skills-three-ways-akl`, read the `.cast` header `timestamp` and duration (`trim-cast.py --info`) for `recordings/raw/<name>.cast`, and correlate it to the canonical parent + subagent trajectory IDs.
2. Flag any aborted takes or `/wayfinder` / `/grilling` meta-planning sessions and ask confirmation before moving them to Trash via `agy-brain-explorer.py delete ... --force`.
3. Verify the expected Skill Activations (`way_1_plugin`, `way_2_community`, `way_3_bespoke`) detected for this trajectory and print a concise telemetry summary (Session UUID, steps, tool calls, Skill Activations) for slide `S4-07`.
4. Sanitise (`sanitize-cast.py`), trim (`trim-cast.py`, preserving any mid-recording `agy` exit in `way-3-agy-customizations.cast`), tighten paste/typing delays (`--tighten-pastes`), place the exact `"m"` stop points from `RUNSHEET.md` (`mark-cast.py`), verify key frames via `uv run --with pyte ... --render`, and output `recordings/final/<name>.cast` plus `mark-cast.py --list`.
```

### 4.2 Expected Canonical `~/.gemini` Dataset (Pre-Recording 5 Gate)

Before recording `way-3-brain-explorer-payoff.cast`, confirm **Brain Explorer** ([`TrajectoryStore`](src/brain_explorer/trajectory_store.py)) displays only these **4 headline build trajectories** (plus the 8 Cycle 1 and Cycle 2 **EGM** review subagent trajectories) for `skills-three-ways-akl`, excluding `/wayfinder`, `/grilling`, or aborted takes:

| Trajectory | Associated `.cast` | Expected Skill Activations & Tiers |
| :--- | :--- | :--- |
| **Trajectory 1 — Way 1 Plugin Discovery** | `way-1-plugins-setup.cast` | `plugin` / `google-antigravity-sdk` (`way_1_plugin`) |
| **Trajectory 2 — Way 2 Skill Evaluation** | `way-2-find-skills.cast` | `find-skills` (`way_2_community`) |
| **Trajectory 3 — Two-Pass EGM Build Cycle** (+ 8 Cycle 1 & 2 **EGM** subagents) | `way-2-egm-cycle.cast` | `google-antigravity-sdk` + `egm-*` (`way_1_plugin`), `wshobson/agents` Python skills (`way_2_community`), `agy-brain-explorer` (`way_3_bespoke`) |
| **Trajectory 4 — Way 3 Synthesis & Cold Verification** | `way-3-agy-customizations.cast` | `agy-customizations` (`way_1_plugin`), `writing-for-agents` (`way_2_community`), `a2ui-textual` (`way_3_bespoke` — reading `SKILL.md` and `references/a2ui-v1-textual-gotchas.md`) |

### 4.3 Multi-Take Audit & Cleanup CLI Commands

```bash
# 1. Inspect all sessions currently discovered under skills-three-ways-akl
uv run .agents/skills/agy-brain-explorer/scripts/agy-brain-explorer.py --project skills-three-ways-akl

# 2. Preview and move superseded takes or /wayfinder / /grilling meta-sessions to Trash
uv run .agents/skills/agy-brain-explorer/scripts/agy-brain-explorer.py delete <OLD_ID_1> <OLD_ID_2> --dry-run
uv run .agents/skills/agy-brain-explorer/scripts/agy-brain-explorer.py delete <OLD_ID_1> <OLD_ID_2> --force

# 3. Verify clean canonical listing directly via Brain Explorer CLI
uv run brain-explorer sessions --project skills-three-ways-akl --limit 20
```

---

## 5. Slidev Sync, Stage Rehearsal & Build Verification

1. **Sync all 6 canonical `.cast` files into `slides/public/casts/`**:
   ```bash
   npm --prefix slides run sync-casts
   ls -lh slides/public/casts/
   ```
   Confirm all 6 files are present:
   - `what-are-agent-skills.cast`
   - `way-1-plugins-setup.cast`
   - `way-2-find-skills.cast`
   - `way-2-egm-cycle.cast`
   - `way-3-agy-customizations.cast`
   - `way-3-brain-explorer-payoff.cast`

2. **Preview & rehearse in Slidev**:
   ```bash
   .agents/skills/slidev-deck/scripts/slides-server.sh start
   .agents/skills/slidev-deck/scripts/slides-server.sh status
   ```
   - Inspect `http://localhost:3030/`, `/presenter` (speaker notes + timer), and `/overview`.
   - Temporarily set `showChapterBar: true` on `cast-full` slides during rehearsal to check stepper pills (`↺ 0. Start`, `1..N`, `→ End`), adaptive speed (`>= 2.0x`), and segment durations (`<= 30s`).
   - Verify stage hotkeys on every embedded player:
     - `]` — Jump to next stop point (or `→ End`)
     - `[` — Step back to previous stop point (or `↺ 0. Start`)
     - `p` — Play / Pause
   - Reset `showChapterBar: false` (or remove the override) once rehearsal checks pass.

3. **Verify static production build & Brain Explorer checks**:
   ```bash
   npm --prefix slides run build
   ls -lh slides/dist/index.html
   uv run ruff check src tests
   uv run mypy src
   uv run pytest -v
   ```
