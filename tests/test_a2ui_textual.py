"""Headless Textual Pilot tests for the A2UI v1.0 renderer and BrainExplorerApp."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from a2ui.core.processing import MessageProcessor
from textual.widgets import Checkbox, Input, ListView, Markdown, Select, Static, TabbedContent

from brain_explorer.a2ui_textual import (
    A2UI_BASIC_CATALOG_V1_0_ID,
    A2UIButton,
    A2UISurfaceWidget,
    create_overview_processor,
    create_strict_processor,
)
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
                        "filterText": "initial",
                        "includeThinking": False,
                        "tierChoice": ["way_3_bespoke"],
                    },
                },
            },
            {
                "version": "1.0",
                "updateComponents": {
                    "surfaceId": "agent_view",
                    "components": [
                        {
                            "id": "root",
                            "component": "Column",
                            "children": ["hdr", "echo", "filter_inp", "think_chk", "tier_sel", "drill_btn"],
                        },
                        {"id": "hdr", "component": "Text", "text": {"@path": "/heading"}, "variant": "body"},
                        {"id": "echo", "component": "Text", "text": {"@path": "/promptEcho"}, "variant": "body"},
                        {
                            "id": "filter_inp",
                            "component": "TextField",
                            "label": "Filter [bracket]",
                            "value": {"@path": "/filterText"},
                        },
                        {
                            "id": "think_chk",
                            "component": "CheckBox",
                            "label": "Include Thinking",
                            "value": {"@path": "/includeThinking"},
                        },
                        {
                            "id": "tier_sel",
                            "component": "ChoicePicker",
                            "label": "Skill Tier",
                            "options": [
                                {"label": "Way 1 Plugin", "value": "way_1_plugin"},
                                {"label": "Way 3 Bespoke", "value": "way_3_bespoke"},
                            ],
                            "value": {"@path": "/tierChoice"},
                        },
                        {
                            "id": "drill_btn",
                            "component": "Button",
                            "child": "drill_lbl",
                            "variant": "primary",
                            "action": {
                                "event": {
                                    "name": "inspect_step",
                                    "context": {
                                        "session_id": "sess-123",
                                        "filter": {"@path": "/filterText"},
                                        "include_thinking": {"@path": "/includeThinking"},
                                        "tiers": {"@path": "/tierChoice"},
                                    },
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
        return "Rendered generative A2UI view [/ok]."

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
    ws = tmp_path / "sample-proj"
    ws.mkdir()
    (ws / ".git").mkdir()
    target_py = ws / "app.py"
    target_py.write_text("print(1)\n", encoding="utf-8")

    logs = tmp_path / "antigravity" / "brain" / "sess-123" / ".system_generated" / "logs"
    logs.mkdir(parents=True)
    steps = [
        {
            "step_index": 0,
            "source": "USER_EXPLICIT",
            "type": "USER_INPUT",
            "created_at": "2026-11-18T11:00:00Z",
            "content": "<USER_REQUEST>Test session prompt with [/SKILL] brackets</USER_REQUEST>",
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
                    "args": {"Path": str(ws / ".agents/skills/agy-brain-explorer/SKILL.md")},
                },
                {
                    "name": "view_file",
                    "args": {"AbsolutePath": str(target_py)},
                },
            ],
        },
    ]
    (logs / "transcript_full.jsonl").write_text("\n".join(json.dumps(s) for s in steps) + "\n", encoding="utf-8")
    return TrajectoryStore(gemini_dir=tmp_path)


def test_overview_processor_strict_validation_and_resolved_bindings(tmp_path: Path) -> None:
    store = _seed_store(tmp_path)
    processor = create_overview_processor(store)
    surface = processor.model.get_surface("brain_overview")
    assert surface is not None
    assert surface.data_model.get("/header") == "# Brain Explorer — A2UI v1.0 Generative Surface"


@pytest.mark.asyncio
async def test_brain_explorer_app_unified_flow_and_two_way_bindings(tmp_path: Path) -> None:
    store = _seed_store(tmp_path)
    fake_agent = _FakeAgentService()
    app = BrainExplorerApp(store=store, agent_service=fake_agent, configure_logging=False)

    async with app.run_test() as pilot:
        await pilot.pause()

        # Overview renders Tabs + TemplateChildList session/project/skill cards (resolved @path text!)
        assert len(app.query(TabbedContent)) == 1
        markdown_sources = [str(w._markdown) for w in app.query(Markdown)]
        assert any("Brain Explorer — A2UI v1.0 Generative Surface" in md for md in markdown_sources)
        assert any("sess-123" in md for md in markdown_sources)
        assert all("{'path'" not in md for md in markdown_sources)

        static_texts = [str(w.render()) for w in app.query(Static)]
        assert any("agy-brain-explorer [way_3_bespoke]" in text for text in static_texts)

        # Verify template-expanded session card button resolved @path session_id
        inspect_buttons = [b for b in app.query(A2UIButton) if b.component_id == "sess_btn"]
        assert len(inspect_buttons) == 1

        # Sidebar visible by default, inspector hidden by default; Ctrl+B / Ctrl+I toggle cleanly
        assert app.sidebar_visible is True
        assert app.inspector_visible is False
        assert app.query_one("#sidebar").display is True
        assert app.query_one("#inspector-pane").display is False

        await pilot.press("ctrl+b")
        assert app.sidebar_visible is False
        assert app.query_one("#sidebar").display is False

        await pilot.press("ctrl+i")
        assert app.inspector_visible is True
        assert app.query_one("#inspector-pane").display is True

        await pilot.press("ctrl+b")
        assert app.sidebar_visible is True

        # Selecting a sidebar item loads local session detail offline (no agent call)
        list_view = app.query_one("#session-list", ListView)
        list_view.index = 0
        list_view.action_select_cursor()
        await pilot.pause()
        assert len(fake_agent.calls) == 0
        assert "session_sess-123" in app.processor.model.surfaces_map

        # Focus prompt via '/' and submit an open-ended question with brackets
        await pilot.press("slash")
        await pilot.press("f", "i", "n", "d", " ", "[", "s", "k", "i", "l", "l", "]")
        await pilot.press("enter")
        await pilot.pause()
        assert ("prompt", "find [skill]") in fake_agent.calls
        assert "agent_view" in app.processor.model.surfaces_map

        # Mutate bound A2UI TextField, CheckBox, and ChoicePicker before clicking button
        canvas = app.query_one("#a2ui-canvas", A2UISurfaceWidget)
        a2ui_input = canvas.query_one(Input)
        a2ui_input.value = "updated-query"
        a2ui_checkbox = canvas.query_one(Checkbox)
        a2ui_checkbox.value = True
        a2ui_select = canvas.query_one(Select)
        a2ui_select.value = "way_1_plugin"
        await pilot.pause()

        # Clearing Select via Select.NULL writes [] (DynamicStringList)
        a2ui_select.value = Select.NULL
        await pilot.pause()
        assert app.processor.model.get_surface("agent_view").data_model.get("/tierChoice") == []

        a2ui_select.value = "way_1_plugin"
        await pilot.pause()

        drill_btn = next(b for b in canvas.query(A2UIButton) if b.component_id == "drill_btn")
        drill_btn.press()
        await pilot.pause()

        action_calls = [c for c in fake_agent.calls if c[0] == "action"]
        assert len(action_calls) == 1
        action_name, action_ctx = action_calls[0][1]
        assert action_name == "inspect_step"
        assert action_ctx == {
            "session_id": "sess-123",
            "filter": "updated-query",
            "include_thinking": True,
            "tiers": ["way_1_plugin"],
        }

        # Reset overview clears back to brain_overview and repopulates sidebar
        await pilot.press("ctrl+r")
        await pilot.pause()
        assert "brain_overview" in app.processor.model.surfaces_map
        assert len(app.query_one("#session-list", ListView).children) == 1
        assert create_strict_processor is not None
