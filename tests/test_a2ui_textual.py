"""Headless Textual Pilot tests for the A2UI v1.0 renderer and BrainExplorerApp."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from a2ui.core.processing import MessageProcessor
from textual.widgets import Input, Static, TabbedContent

from brain_explorer.a2ui_textual import A2UI_BASIC_CATALOG_V1_0_ID, A2UIButton
from brain_explorer.trajectory_store import TrajectoryStore
from brain_explorer.tui import BrainExplorerApp


class _FakeAgentService:
    """Deterministic stub mimicking BrainExplorerAgentService for Textual Pilot tests."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, Any]] = []
        self._last_messages: list[dict[str, Any]] = []

    @property
    def last_messages(self) -> list[dict[str, Any]]:
        return list(self._last_messages)

    async def generate_a2ui(self, user_prompt: str, processor: MessageProcessor) -> str:
        self.calls.append(("prompt", user_prompt))
        msgs = [
            {
                "version": "1.0",
                "createSurface": {"surfaceId": "agent_view", "catalogId": A2UI_BASIC_CATALOG_V1_0_ID},
            },
            {
                "version": "1.0",
                "updateDataModel": {
                    "surfaceId": "agent_view",
                    "path": "/",
                    "value": {
                        "heading": "## Agent Generative View",
                        "promptEcho": user_prompt,
                    },
                },
            },
            {
                "version": "1.0",
                "updateComponents": {
                    "surfaceId": "agent_view",
                    "components": [
                        {"id": "root", "component": "Column", "children": ["hdr", "echo", "drill_btn"]},
                        {"id": "hdr", "component": "Text", "text": {"@path": "/heading"}, "variant": "body"},
                        {"id": "echo", "component": "Text", "text": {"@path": "/promptEcho"}, "variant": "body"},
                        {
                            "id": "drill_btn",
                            "component": "Button",
                            "child": "drill_lbl",
                            "variant": "primary",
                            "action": {
                                "event": {
                                    "name": "inspect_step",
                                    "context": {"session_id": "sess-123", "step_index": 0},
                                }
                            },
                        },
                        {"id": "drill_lbl", "component": "Text", "text": "Drill Into Step 0"},
                    ],
                },
            },
        ]
        for existing_id in list(processor.model.surfaces_map):
            processor.model.delete_surface(existing_id)
        processor.process_messages(msgs)
        self._last_messages = msgs
        return "Rendered generative A2UI view."

    async def handle_a2ui_action(
        self,
        action_name: str,
        context: dict[str, Any],
        processor: MessageProcessor,
    ) -> str:
        self.calls.append(("action", (action_name, context)))
        msgs = [
            {
                "version": "1.0",
                "createSurface": {"surfaceId": "action_view", "catalogId": A2UI_BASIC_CATALOG_V1_0_ID},
            },
            {
                "version": "1.0",
                "updateComponents": {
                    "surfaceId": "action_view",
                    "components": [
                        {"id": "root", "component": "Card", "child": "action_txt"},
                        {
                            "id": "action_txt",
                            "component": "Text",
                            "text": f"### Handled {action_name}: {context.get('session_id', '')}",
                            "variant": "body",
                        },
                    ],
                },
            },
        ]
        for existing_id in list(processor.model.surfaces_map):
            processor.model.delete_surface(existing_id)
        processor.process_messages(msgs)
        self._last_messages = msgs
        return f"Completed {action_name}."


def _seed_store(tmp_path: Path) -> TrajectoryStore:
    logs = tmp_path / "antigravity" / "brain" / "sess-123" / ".system_generated" / "logs"
    logs.mkdir(parents=True)
    steps = [
        {
            "step_index": 0,
            "source": "USER_EXPLICIT",
            "type": "USER_INPUT",
            "created_at": "2026-11-18T11:00:00Z",
            "content": "<USER_REQUEST>Test session prompt</USER_REQUEST>",
        },
        {
            "step_index": 1,
            "source": "MODEL",
            "type": "PLANNER_RESPONSE",
            "created_at": "2026-11-18T11:00:30Z",
            "content": "Done.",
            "tool_calls": [
                {
                    "name": "read_file",
                    "args": {"Path": "/repo/.agents/skills/agy-brain-explorer/SKILL.md"},
                }
            ],
        },
    ]
    (logs / "transcript_full.jsonl").write_text("\n".join(json.dumps(s) for s in steps) + "\n", encoding="utf-8")
    return TrajectoryStore(gemini_dir=tmp_path)


@pytest.mark.asyncio
async def test_brain_explorer_app_variants_and_a2ui_actions(tmp_path: Path) -> None:
    store = _seed_store(tmp_path)
    fake_agent = _FakeAgentService()
    app = BrainExplorerApp(store=store, agent_service=fake_agent, configure_logging=False)

    async with app.run_test() as pilot:
        await pilot.pause()

        # Initial A2UI overview surface rendered Tabs and an A2UIButton
        assert len(app.query(TabbedContent)) == 1
        assert any(isinstance(b, A2UIButton) for b in app.query(A2UIButton))

        # Variant switching via 1/2/3 when prompt input is not focused
        assert app.current_variant == "A"
        assert app.query_one("#sidebar").display is False
        assert app.query_one("#inspector-pane").display is False

        await pilot.press("2")
        assert app.current_variant == "B"
        assert app.query_one("#sidebar").display is True
        assert app.query_one("#inspector-pane").display is False

        await pilot.press("3")
        assert app.current_variant == "C"
        assert app.query_one("#inspector-pane").display is True

        await pilot.press("1")
        assert app.current_variant == "A"

        # Typing '2' inside focused Input must enter text rather than switching variants
        prompt_input = app.query_one("#prompt-input", Input)
        prompt_input.focus()
        await pilot.press("2", "a", "b")
        assert prompt_input.value == "2ab"
        assert app.current_variant == "A"

        # Submitting prompt invokes generate_a2ui and mounts the new A2UI surface
        await pilot.press("enter")
        await pilot.pause()
        assert ("prompt", "2ab") in fake_agent.calls
        assert "agent_view" in app.processor.model.surfaces_map

        # Clicking the A2UI button dispatches A2UIActionDispatched -> handle_a2ui_action
        drill_buttons = [b for b in app.query(A2UIButton) if b.action_name == "inspect_step"]
        assert len(drill_buttons) == 1
        drill_buttons[0].press()
        await pilot.pause()
        assert ("action", ("inspect_step", {"session_id": "sess-123", "step_index": 0})) in fake_agent.calls
        assert "action_view" in app.processor.model.surfaces_map
        inspector_text = str(app.query_one("#inspector-body", Static).render())
        assert "action_view" in inspector_text
