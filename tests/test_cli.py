"""CLI tests for brain-explorer commands using Typer CliRunner."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from brain_explorer.cli import app

runner = CliRunner()


def _create_cli_fixture(gemini_dir: Path) -> None:
    ws = gemini_dir.parent / "cli-workspace"
    ws.mkdir(parents=True, exist_ok=True)
    (ws / ".git").mkdir(exist_ok=True)
    py_file = ws / "main.py"
    py_file.write_text("print('ok')\n", encoding="utf-8")

    for sid, prompt, ts in (
        ("aaaa0001-0000-0000-0000-000000000001", "First prompt [/SKILL]", "2026-11-18T08:00:00Z"),
        ("bbbb0002-0000-0000-0000-000000000002", "Second prompt [bold]", "2026-11-18T09:00:00Z"),
    ):
        logs = gemini_dir / "antigravity" / "brain" / sid / ".system_generated" / "logs"
        logs.mkdir(parents=True, exist_ok=True)
        steps = [
            {
                "step_index": 0,
                "source": "USER_EXPLICIT",
                "type": "USER_INPUT",
                "created_at": ts,
                "content": f"<USER_REQUEST>{prompt}</USER_REQUEST>",
            },
            {
                "step_index": 1,
                "source": "MODEL",
                "type": "PLANNER_RESPONSE",
                "created_at": ts,
                "thinking": "Thinking [bracket] check",
                "content": "Done.",
                "tool_calls": [
                    {"name": "view_file", "args": {"AbsolutePath": str(py_file)}},
                    {
                        "name": "read_file",
                        "args": {"Path": str(ws / ".agents/skills/agy-brain-explorer/SKILL.md")},
                    },
                ],
            },
        ]
        (logs / "transcript_full.jsonl").write_text(
            "\n".join(json.dumps(s) for s in steps) + "\n",
            encoding="utf-8",
        )


def test_cli_commands_and_markup_safety(tmp_path: Path) -> None:
    gemini_dir = tmp_path / "gemini_home"
    _create_cli_fixture(gemini_dir)

    res_projects = runner.invoke(app, ["projects", "--gemini-dir", str(gemini_dir)])
    assert res_projects.exit_code == 0
    assert "cli-workspace" in res_projects.output

    res_sessions = runner.invoke(app, ["sessions", "--gemini-dir", str(gemini_dir)])
    assert res_sessions.exit_code == 0
    assert "aaaa0001" in res_sessions.output
    assert "bbbb0002" in res_sessions.output

    res_search = runner.invoke(app, ["search", "[/SKILL]", "--gemini-dir", str(gemini_dir)])
    assert res_search.exit_code == 0
    assert "aaaa0001" in res_search.output

    res_inspect = runner.invoke(app, ["inspect", "aaaa0001", "--gemini-dir", str(gemini_dir)])
    assert res_inspect.exit_code == 0
    assert "agy-brain-explorer" in res_inspect.output

    res_step = runner.invoke(app, ["step", "aaaa0001", "1", "--gemini-dir", str(gemini_dir)])
    assert res_step.exit_code == 0
    assert "Thinking [bracket] check" in res_step.output

    res_compare = runner.invoke(app, ["compare", "aaaa0001", "bbbb0002", "--gemini-dir", str(gemini_dir)])
    assert res_compare.exit_code == 0
    assert "Session Trajectory Comparison" in res_compare.output

    res_missing = runner.invoke(app, ["inspect", "does-not-exist", "--gemini-dir", str(gemini_dir)])
    assert res_missing.exit_code == 1
