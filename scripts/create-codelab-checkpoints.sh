#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
WORKTREE_DIR="$(mktemp -d "${TMPDIR:-/tmp}/skills-codelab-checkpoints.XXXXXX")"
TEMP_BRANCH="_tmp_codelab_build_$$"

cleanup() {
  git -C "$REPO_ROOT" worktree remove --force "$WORKTREE_DIR" >/dev/null 2>&1 || rm -rf "$WORKTREE_DIR"
  git -C "$REPO_ROOT" branch -D "$TEMP_BRANCH" >/dev/null 2>&1 || true
}
trap cleanup EXIT

git -C "$REPO_ROOT" worktree add --detach "$WORKTREE_DIR" HEAD >/dev/null

cd "$WORKTREE_DIR"
git checkout --orphan "$TEMP_BRANCH" >/dev/null 2>&1
git rm -rf --ignore-unmatch . >/dev/null 2>&1 || true
find "$WORKTREE_DIR" -mindepth 1 -maxdepth 1 -not -name '.git' -exec rm -rf {} +

# ---------------------------------------------------------------------------
# 1. codelab/start: clean starter workspace before Way 2 / Way 3 labs
# ---------------------------------------------------------------------------
cp "$REPO_ROOT/LICENSE" "$WORKTREE_DIR/LICENSE"
cp "$REPO_ROOT/GLOSSARY.md" "$WORKTREE_DIR/GLOSSARY.md"
cp "$REPO_ROOT/AGENTS.md" "$WORKTREE_DIR/AGENTS.md"
cp "$REPO_ROOT/.gitignore" "$WORKTREE_DIR/.gitignore"
cp "$REPO_ROOT/.python-version" "$WORKTREE_DIR/.python-version"
cp "$REPO_ROOT/pyproject.toml" "$WORKTREE_DIR/pyproject.toml"

mkdir -p "$WORKTREE_DIR/.agents/skills"
cp -R "$REPO_ROOT/.agents/skills/agy-brain-explorer" "$WORKTREE_DIR/.agents/skills/"
cp -R "$REPO_ROOT/.agents/skills/writing-for-agents" "$WORKTREE_DIR/.agents/skills/"

cat > "$WORKTREE_DIR/README.md" <<'EOF'
# Skills Three Ways — 90-Minute Codelab Starter

Starter branch (`codelab/start`) for the **Skills Three Ways** 90-minute self-paced codelab.

- **Interactive Codelab**: <https://domesticmouse.github.io/skills-three-ways-akl/>
- **Matching Presentation Deck**: <https://domesticmouse.github.io/skills-three-ways-akl/slides/>

## Getting Started

```bash
git checkout -b my-lab codelab/start
```

Follow **Lab 0** in the web codelab, or recover at any milestone with the checkpoint branches:

| Checkpoint Branch | State |
| :--- | :--- |
| `codelab/start` | Clean starter repo (`pyproject.toml`, `GLOSSARY.md`, `agy-brain-explorer`, `writing-for-agents`) |
| `codelab/checkpoint-2-skills` | After Lab 2 (`find-skills` + 17 `wshobson/agents` Python skills + `skills-lock.json`) |
| `codelab/checkpoint-3-brain-explorer` | After Lab 3 (verified `src/brain_explorer/`, `tests/`, and `uv.lock`) |
| `codelab/checkpoint-4-bespoke-skill` | After Lab 4 (adds reference `.agents/skills/a2ui-textual/`) |
EOF

git add -A
git commit -m "chore(codelab): start clean lab baseline (codelab/start)" >/dev/null
git branch -f codelab/start HEAD >/dev/null

# ---------------------------------------------------------------------------
# 2. codelab/checkpoint-2-skills: add find-skills + wshobson/agents + lockfile
# ---------------------------------------------------------------------------
WAY2_SKILLS=(
  find-skills
  async-python-patterns
  fastapi-templates
  python-anti-patterns
  python-background-jobs
  python-code-style
  python-configuration
  python-design-patterns
  python-error-handling
  python-observability
  python-packaging
  python-performance-optimization
  python-project-structure
  python-resilience
  python-resource-management
  python-testing-patterns
  python-type-safety
  uv-package-manager
)

for skill in "${WAY2_SKILLS[@]}"; do
  cp -R "$REPO_ROOT/.agents/skills/$skill" "$WORKTREE_DIR/.agents/skills/"
done

python3 - "$REPO_ROOT/skills-lock.json" "$WORKTREE_DIR/.agents/skills" "$WORKTREE_DIR/skills-lock.json" <<'PY'
import json
import sys
from pathlib import Path

src_lock, skills_dir, out_lock = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
data = json.loads(src_lock.read_text(encoding="utf-8"))
installed = {p.name for p in skills_dir.iterdir() if p.is_dir()}
filtered_skills = {k: v for k, v in data.get("skills", {}).items() if k in installed}
out_data = {
    "version": data.get("version", 2),
    "skills": dict(sorted(filtered_skills.items())),
}
out_lock.write_text(json.dumps(out_data, indent=2) + "\n", encoding="utf-8")
PY

git add -A
git commit -m "chore(codelab): add find-skills and wshobson/agents Python skills (checkpoint 2)" >/dev/null
git branch -f codelab/checkpoint-2-skills HEAD >/dev/null

# ---------------------------------------------------------------------------
# 3. codelab/checkpoint-3-brain-explorer: add Brain Explorer + tests + uv.lock
# ---------------------------------------------------------------------------
mkdir -p "$WORKTREE_DIR/src" "$WORKTREE_DIR/docs/research"
cp -R "$REPO_ROOT/src/brain_explorer" "$WORKTREE_DIR/src/"
cp -R "$REPO_ROOT/tests" "$WORKTREE_DIR/"
cp "$REPO_ROOT/docs/research/a2ui-python.md" "$WORKTREE_DIR/docs/research/a2ui-python.md"
cp "$REPO_ROOT/uv.lock" "$WORKTREE_DIR/uv.lock"
find "$WORKTREE_DIR/src" "$WORKTREE_DIR/tests" -name "__pycache__" -exec rm -rf {} +
find "$WORKTREE_DIR/src" "$WORKTREE_DIR/tests" -name "*.pyc" -delete

git add -A
git commit -m "feat(codelab): add Brain Explorer CLI, Textual TUI, and tests (checkpoint 3)" >/dev/null
git branch -f codelab/checkpoint-3-brain-explorer HEAD >/dev/null

# ---------------------------------------------------------------------------
# 4. codelab/checkpoint-4-bespoke-skill: add reference a2ui-textual skill
# ---------------------------------------------------------------------------
cp -R "$REPO_ROOT/.agents/skills/a2ui-textual" "$WORKTREE_DIR/.agents/skills/"

git add -A
git commit -m "feat(codelab): add bespoke a2ui-textual skill (checkpoint 4)" >/dev/null
git branch -f codelab/checkpoint-4-bespoke-skill HEAD >/dev/null

cd "$REPO_ROOT"
echo "Created local codelab checkpoint branches:"
git branch --list 'codelab/*'
echo ""
echo "Current branch: $(git branch --show-current)"
echo "To publish checkpoints to origin when ready:"
echo "  git push -f origin codelab/start codelab/checkpoint-2-skills codelab/checkpoint-3-brain-explorer codelab/checkpoint-4-bespoke-skill"
