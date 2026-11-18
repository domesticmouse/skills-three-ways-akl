# Skills Three Ways — DevFest Auckland 2026

Companion repository for **Skills Three Ways** (*Ecosystem, Community, and Bespoke Agent Skills in Action*) at DevFest Auckland 2026.

- **Slidev Presentation Deck** (`slides/`): 36-slide dark-theme deck with custom layouts, conversational presenter notes, and adaptive-speed `asciinema-player` embeds.
- **Brain Explorer** (`src/brain_explorer/`): Python CLI and Textualize (`Textual`) TUI powered by the `google-antigravity` SDK and `a2ui-core` / `a2ui-agent-sdk` (`ProtocolVersion.V1_0`) to inspect `~/.gemini` Session Trajectories and Skill Activations.
- **Bespoke Workspace Skills** (`.agents/skills/`): Includes `.agents/skills/a2ui-textual/` (synthesised from Exploratory Run findings) alongside `agy-brain-explorer`, `slidev-deck`, and `bjm-voice`.

---

## Running the Slidev Deck Locally

Prerequisites: Node.js 18+ and `npm`.

```bash
# Install dependencies (from repo root)
npm --prefix slides install

# Start the Slidev dev server on http://localhost:3030/
.agents/skills/slidev-deck/scripts/slides-server.sh start
.agents/skills/slidev-deck/scripts/slides-server.sh status

# Or build the static GitHub Pages bundle (slides/dist/)
npm --prefix slides run build
```

Useful local endpoints while the dev server is running:
- Deck: `http://localhost:3030/`
- Presenter console (speaker notes + timer): `http://localhost:3030/presenter`
- Slide overview grid: `http://localhost:3030/overview`

For slides whose `.cast` recordings have not yet been captured in `recordings/final/`, the deck renders structured placeholder cards listing the target `.cast` filename and `m1`–`mN` stop points. Once you record, sanitise, trim, and chapter-mark a `.cast` file into `recordings/final/` and run `npm --prefix slides run sync-casts` (or `predev`/`prebuild`), the corresponding slide automatically switches to the interactive `asciinema-player`.

---

## Deploying to GitHub Pages

Automated deployment is configured in [`.github/workflows/deploy-slides.yml`](.github/workflows/deploy-slides.yml), building `slides/` with `--base /skills-three-ways-akl/` on pushes to `main` touching `slides/**` or `recordings/final/**`.

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
uv run brain-explorer sessions --project skills-three-ways-akl
uv run brain-explorer inspect <session-id>
uv run brain-explorer query "Compare Way 1, Way 2, and Way 3 Skill Activations"
```

TUI shortcuts: `/` focuses the prompt bar, `Ctrl+B` toggles the local trajectory sidebar, `Ctrl+I` toggles the A2UI v1.0 protocol & DataModel inspector, `Ctrl+R` resets to the overview surface, and `q` quits.

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
