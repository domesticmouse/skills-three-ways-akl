# Skills Three Ways — Codelab & Deck TODO

Status and remaining release tasks for the **90-minute self-paced codelab** (`codelab/`) and **matching Slidev deck** (`slides/`).

---

## Completed Conversion Milestones

- [x] **Brain Explorer Dynamic Tier Detection**: Updated [`src/brain_explorer/trajectory_store.py`](src/brain_explorer/trajectory_store.py) to classify any workspace skill in `.agents/skills/` absent from `skills-lock.json` as `way_3_bespoke` (backed by `test_dynamic_bespoke_skill_classification_via_skills_lock` in [`tests/test_trajectory_store.py`](tests/test_trajectory_store.py)).
- [x] **Self-Contained Dark-Theme Web Codelab (`codelab/`)**: Built [`codelab/build.mjs`](codelab/build.mjs), [`codelab/assets/style.css`](codelab/assets/style.css), [`codelab/assets/codelab.js`](codelab/assets/codelab.js), and 6 progressive labs (`codelab/steps/00-setup.md`–`05-brain-explorer.md`) with copy buttons, `localStorage` progress, collapsible troubleshooting/reference debriefs, and vector QR SVG generation (`codelab/dist/assets/codelab-qr.svg` & `slides/public/images/codelab-qr.svg`).
- [x] **Retired `asciinema` Pipeline & CAST Assets**: Uninstalled `asciinema-player`, removed `AsciinemaPlayer.vue`, `cast-full.vue`, `recordings/`, `slides/public/casts/`, and `RUNSHEET.md`.
- [x] **Refactored Matching Slidev Deck (`slides/`)**: Added [`QrBadge.vue`](slides/components/QrBadge.vue), [`PromptCard.vue`](slides/components/PromptCard.vue), and [`lab-step.vue`](slides/layouts/lab-step.vue); added QR onboarding slide `S1-01e`; converted all 6 cast slides (`S1-05`, `S2-03`, `S3-03`, `S3-06`, `S4-03`, `S4-06`) into `lab-step` slides; updated `S4-09` and speaker notes in `slides/acts/01`–`04`; enabled `routerMode: hash` for subpath deep links.
- [x] **Unified GitHub Pages Workflow**: Replaced `deploy-slides.yml` with [`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml) publishing `codelab/dist/` at `/skills-three-ways-akl/` and `slides/dist/` at `/skills-three-ways-akl/slides/`.
- [x] **Checkpoint Branch Generator & Docs**: Added [`scripts/create-codelab-checkpoints.sh`](scripts/create-codelab-checkpoints.sh) and updated [`GLOSSARY.md`](GLOSSARY.md) and [`README.md`](README.md).

---

## Remaining Release Tasks

- [ ] **Commit & Push `main` + `codelab/*` Checkpoint Branches**:
  - Review `git status` and commit the codelab + Slidev deck changes on `main`.
  - Push `main` and all 4 checkpoint branches (`codelab/start`, `codelab/checkpoint-2-skills`, `codelab/checkpoint-3-brain-explorer`, `codelab/checkpoint-4-bespoke-skill`) to `origin`.
- [ ] **Verify GitHub Pages Settings**:
  - In GitHub repository Settings, set **Pages > Build and deployment > Source** to **GitHub Actions** and confirm both `https://domesticmouse.github.io/skills-three-ways-akl/` and `https://domesticmouse.github.io/skills-three-ways-akl/slides/` render cleanly after workflow completion.
- [ ] **Timed 90-Minute Dry Run**:
  - Walk through `codelab/start` end-to-end as a fresh learner (verifying QR scan from projector/screen, copy buttons on `https:` / `localhost`, Lab 3 Path 1 & Path 2 timings, and Lab 5 Brain Explorer against fresh `~/.gemini` sessions).
