# Skills Three Ways — 90-Minute Self-Paced Codelab & Deck

Companion repository for **Skills Three Ways** (*Ecosystem, Community, and Bespoke Agent Skills in Action*) — structured as a **90-minute self-paced web codelab** paired with a **matching Slidev facilitator deck**.

- **Interactive Web Codelab** (`codelab/` -> `https://domesticmouse.github.io/skills-three-ways-akl/`): 6 dark-theme labs (`Lab 0`–`Lab 5`) with cut'n'paste prompts, one-click copy buttons, local progress tracking, troubleshooting foldouts, and recovery git checkpoints.
- **Matching Slidev Deck** (`slides/` -> `https://domesticmouse.github.io/skills-three-ways-akl/slides/`): 37-slide dark-theme deck featuring scannable QR codes (`slides/public/images/codelab-qr.svg`), `PromptCard` copy widgets, `lab-step` layouts synced to each lab, and reference pattern debriefs.
- **Brain Explorer** (`src/brain_explorer/`): Python CLI and Textualize (`Textual`) TUI powered by the `google-antigravity` SDK and `a2ui-core` / `a2ui-agent-sdk` (`ProtocolVersion.V1_0`) to inspect your own `~/.gemini` Session Trajectories and Skill Activations.
- **Bespoke Workspace Skills** (`.agents/skills/`): Includes `.agents/skills/a2ui-textual/` (reference Way 3 skill), `agy-brain-explorer`, `slidev-deck`, and `bjm-voice`.

---

## Running the Codelab & Slidev Deck Locally

Prerequisites: Node.js 18+ and `npm`.

```bash
# Install Slidev and codelab build dependencies (from repo root)
npm --prefix slides install

# Build and validate the static web codelab (codelab/dist/ + slides/public/images/codelab-qr.svg)
node codelab/build.mjs --check

# Start the Slidev dev server on http://localhost:3030/ (runs predev -> build:codelab)
.agents/skills/slidev-deck/scripts/slides-server.sh start
.agents/skills/slidev-deck/scripts/slides-server.sh status

# Or build the Slidev static bundle (slides/dist/)
npm --prefix slides run build
```

Useful local Slidev endpoints while the dev server is running:
- Deck: `http://localhost:3030/`
- Presenter console (speaker notes + timer): `http://localhost:3030/#/presenter/`
- Slide overview grid: `http://localhost:3030/#/overview/`

To preview the compiled codelab locally over HTTP (`navigator.clipboard` requires `localhost` or `https:`):

```bash
python3 -m http.server 4173 --directory codelab/dist
```

---

## Codelab Checkpoint Branches

Learners start on `codelab/start` (`git checkout -b my-lab codelab/start`) so their agent cannot peek at finished code on `main`, and can jump to any verified checkpoint if time or quota runs short:

| Branch | Included State |
| :--- | :--- |
| `codelab/start` | Clean starter repo (`pyproject.toml`, `GLOSSARY.md`, `AGENTS.md`, `agy-brain-explorer`, `writing-for-agents`) |
| `codelab/checkpoint-2-skills` | Adds `find-skills`, 17 `wshobson/agents` Python skills, and `skills-lock.json` |
| `codelab/checkpoint-3-brain-explorer` | Adds verified `src/brain_explorer/`, `tests/`, `docs/research/a2ui-python.md`, and `uv.lock` |
| `codelab/checkpoint-4-bespoke-skill` | Adds reference `.agents/skills/a2ui-textual/` |

Maintainers can regenerate all four local checkpoint branches cleanly from `main` via a temporary worktree:

```bash
./scripts/create-codelab-checkpoints.sh
```

---

## Deploying to GitHub Pages

Automated deployment is configured in [`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml), building both `codelab/` (published at `/skills-three-ways-akl/`) and `slides/` (published at `/skills-three-ways-akl/slides/`) on pushes to `main` touching `codelab/**` or `slides/**`.

In your GitHub repository settings, set **Pages > Build and deployment > Source** to **GitHub Actions**.

---

## Running Brain Explorer (CLI & Textual TUI)

Prerequisites: Python 3.12+ and [`uv`](https://docs.astral.sh/uv/).

```bash
# Install Python dependencies
uv sync

# Launch the interactive Textual TUI
uv run brain-explorer

# Or use CLI subcommands
uv run brain-explorer projects
uv run brain-explorer sessions --project "$(basename "$PWD")"
uv run brain-explorer inspect <session-id>
uv run brain-explorer query "Compare Way 1, Way 2, and Way 3 Skill Activations"
```

TUI shortcuts: `/` focuses the prompt bar, `Ctrl+B` toggles the local trajectory sidebar, `Ctrl+I` toggles the A2UI v1.0 protocol & `DataModel` inspector, `Ctrl+R` resets to the overview surface, and `q` quits.

### Verification

```bash
uv run ruff check src tests
uv run mypy src
uv run pytest -v
```

---

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This is not an official Google product.
