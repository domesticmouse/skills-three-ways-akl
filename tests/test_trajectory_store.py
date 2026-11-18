"""Tests for TrajectoryStore and deterministic Skill Activation detection."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from brain_explorer.trajectory_store import TrajectoryStore


def _write_session(
    gemini_dir: Path,
    brain_root: str,
    session_id: str,
    steps: list[dict[str, object]],
    *,
    step_outputs: dict[int, str] | None = None,
    raw_extra_lines: list[str] | None = None,
) -> Path:
    session_dir = gemini_dir / brain_root / "brain" / session_id
    logs_dir = session_dir / ".system_generated" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(step) for step in steps]
    if raw_extra_lines:
        lines.insert(1, raw_extra_lines[0])
    (logs_dir / "transcript_full.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")

    if step_outputs:
        for idx, output_text in step_outputs.items():
            out_dir = session_dir / ".system_generated" / "steps" / str(idx)
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "output.txt").write_text(output_text, encoding="utf-8")

    return session_dir


def test_skill_activation_detection_and_tiers(tmp_path: Path) -> None:
    workspace_dir = tmp_path / "demo-repo"
    workspace_dir.mkdir()
    (workspace_dir / ".git").mkdir()
    target_file = workspace_dir / "src" / "app.py"
    target_file.parent.mkdir(parents=True)
    target_file.write_text("print('hi')\n", encoding="utf-8")

    _write_session(
        tmp_path,
        "antigravity",
        "aaaa1111-0000-0000-0000-000000000001",
        steps=[
            {
                "step_index": 0,
                "source": "USER_EXPLICIT",
                "type": "USER_INPUT",
                "created_at": "2026-11-18T08:00:00Z",
                "content": (
                    "<USER_REQUEST>\n/wayfinder explore map and inspect <SKILL>quoted</SKILL>\n</USER_REQUEST>\n"
                    "/wayfinder is a [Slash Command]:\n"
                    '<SKILL>The user requested you read and use the "wayfinder" skill. '
                    "The path to the skill file is:\n"
                    ".agents/skills/wayfinder/SKILL.md</SKILL>"
                ),
            },
            {
                "step_index": None,
                "source": "MODEL",
                "type": "PLANNER_RESPONSE",
                "created_at": "2026-11-18T08:01:30Z",
                "thinking": "Inspecting skills and workspace carefully.",
                "content": "Checking skills.",
                "tool_calls": [
                    {
                        "name": "read_file",
                        "args": {"Path": "/Users/test/.gemini/config/plugins/egm/skills/egm-design/SKILL.md"},
                    },
                    {
                        "name": "read_file",
                        "args": {"Path": str(workspace_dir / ".agents/skills/agy-brain-explorer/SKILL.md")},
                    },
                    {
                        "name": "view_file",
                        "args": {"AbsolutePath": str(target_file)},
                    },
                ],
            },
            {
                "step_index": 2,
                "source": "USER_EXPLICIT",
                "type": "USER_INPUT",
                "created_at": "2026-11-18T08:02:00Z",
                "content": (
                    "<SKILL>The user has explicitly invoked the (grilling) skill. Here are its contents:</SKILL>\n"
                    "The user changed setting `Model Selection` from None to Gemini 3 Pro."
                ),
            },
        ],
        step_outputs={1: "Plugin skill loaded cleanly."},
        raw_extra_lines=["{broken-json-line"],
    )

    store = TrajectoryStore(gemini_dir=tmp_path)
    projects = store.list_projects()
    assert len(projects.projects) == 1
    assert projects.projects[0].name == "demo-repo"
    assert projects.projects[0].session_count == 1

    sessions = store.list_sessions(limit=5).sessions
    assert len(sessions) == 1
    sess = sessions[0]
    assert sess.duration == "2m 00s"
    assert sess.step_count == 3
    assert sess.initial_prompt == "/wayfinder explore map and inspect <SKILL>quoted</SKILL>"

    by_name = {item.skill_name: item for item in sess.skill_activations}
    assert "quoted" not in by_name
    assert by_name["wayfinder"].activation_kind == "slash_command"
    assert by_name["wayfinder"].tier == "way_2_community"
    assert by_name["egm-design"].activation_kind == "skill_md_read"
    assert by_name["egm-design"].tier == "way_1_plugin"
    assert by_name["agy-brain-explorer"].activation_kind == "skill_md_read"
    assert by_name["agy-brain-explorer"].tier == "way_3_bespoke"
    assert by_name["grilling"].activation_kind == "slash_command"

    detail = store.inspect_session("aaaa1111")
    assert detail.models_used == ["Gemini 3 Pro"]
    assert detail.steps[1].step_index == 1
    assert any(tc.tool_name == "read_file" and tc.count == 2 for tc in detail.tool_counts)

    step_detail = store.inspect_step("aaaa1111", 1)
    assert step_detail.thinking == "Inspecting skills and workspace carefully."
    assert step_detail.step_output == "Plugin skill loaded cleanly."


def test_search_thinking_project_ordering_and_compare(tmp_path: Path) -> None:
    proj_old = tmp_path / "older-repo"
    proj_old.mkdir()
    (proj_old / ".git").mkdir()
    old_file = proj_old / "main.py"
    old_file.write_text("x = 1\n", encoding="utf-8")

    proj_new = tmp_path / "newer-repo"
    proj_new.mkdir()
    (proj_new / ".git").mkdir()
    new_file = proj_new / "main.py"
    new_file.write_text("x = 2\n", encoding="utf-8")

    _write_session(
        tmp_path,
        "antigravity",
        "11111111-aaaa-bbbb-cccc-000000000001",
        steps=[
            {
                "step_index": 0,
                "source": "USER_EXPLICIT",
                "type": "USER_INPUT",
                "created_at": "2026-11-18T09:00:00Z",
                "content": "<USER_REQUEST>Build Textual widget</USER_REQUEST>",
                "tool_calls": [{"name": "view_file", "args": {"Path": str(old_file)}}],
            }
        ],
    )
    _write_session(
        tmp_path,
        "antigravity",
        "22222222-aaaa-bbbb-cccc-000000000002",
        steps=[
            {
                "step_index": 0,
                "source": "USER_EXPLICIT",
                "type": "USER_INPUT",
                "created_at": "2026-11-18T10:00:00Z",
                "content": "<USER_REQUEST>Audit A2UI schema</USER_REQUEST>",
            },
            {
                "step_index": 1,
                "source": "MODEL",
                "type": "PLANNER_RESPONSE",
                "created_at": "2026-11-18T10:01:00Z",
                "thinking": "Reasoning token: unicorn-signal inside thinking.",
                "content": "Checking A2UI schema.",
                "tool_calls": [
                    {
                        "name": "read_file",
                        "args": {"Path": str(proj_new / ".agents/skills/python-type-safety/SKILL.md")},
                    },
                    {
                        "name": "view_file",
                        "args": {"Path": str(new_file)},
                    },
                ],
            },
        ],
    )

    store = TrajectoryStore(gemini_dir=tmp_path)
    projects = store.list_projects().projects
    assert [p.name for p in projects] == ["newer-repo", "older-repo"]

    hits = store.search_sessions("unicorn-signal")
    assert [s.session_id for s in hits.sessions] == ["22222222-aaaa-bbbb-cccc-000000000002"]

    comparison = store.compare_sessions("11111111", "22222222")
    assert comparison.session_a.step_count == 1
    assert comparison.session_b.step_count == 2
    assert any("python-type-safety" in diff for diff in comparison.key_differences)

    with pytest.raises(ValueError, match="compare a session with itself"):
        store.compare_sessions("11111111", "11111111-aaaa-bbbb-cccc-000000000001")
