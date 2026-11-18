"""PROTOTYPE — throwaway Phase 3 cold-session verification for a2ui-textual.

Spins up a brand-new, empty-context Google Antigravity SDK Agent pointing at
``.agents/skills/a2ui-textual`` inside an isolated temporary ``app_data_dir``
and ``save_dir`` outside ``~/.gemini``, verifies that a cold prompt activates
Tier 1/2/3 progressive disclosure, validates the emitted A2UI v1.0 payload with
``STRICT_VALIDATION``, renders it inside a headless Textual ``App.run_test()``
pilot, and inspects the recorded transcript with ``TrajectoryStore``.
"""

from __future__ import annotations

import asyncio
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

from a2ui.core.basic_catalog import BasicCatalog
from a2ui.core.processing import MessageProcessor
from a2ui.core.processing.message_processor import MessageProcessorOptions
from a2ui.core.schema import ProtocolVersion
from a2ui.core.validation import STRICT_VALIDATION
from a2ui.inference_formats.direct_json import DirectJsonFormatFactory
from a2ui.parser.messages import to_message_dicts
from a2ui.parser.response_part import A2uiPart, TextPart
from a2ui.processor import A2uiRequestProcessor
from google.antigravity import Agent, LocalAgentConfig, types
from google.antigravity.hooks import policy
from textual.app import App, ComposeResult
from textual.widgets import Markdown, Static, TabbedContent

from brain_explorer.a2ui_textual import (
    A2UIButton,
    A2UIChoicePicker,
    A2UISurfaceWidget,
)
from brain_explorer.agent_service import configure_sdk_logging
from brain_explorer.trajectory_store import TrajectoryStore, detect_skill_activations


class _PrototypeVerifyApp(App[None]):
    """Minimal headless Textual app hosting an A2UISurfaceWidget."""

    AUTO_FOCUS = None

    def __init__(self, processor: MessageProcessor) -> None:
        super().__init__()
        self._processor = processor

    def compose(self) -> ComposeResult:
        yield A2UISurfaceWidget(processor=self._processor, id="a2ui-canvas")


def _print_section(title: str, data: Any) -> None:
    print(f"\n=== {title} ===")
    if isinstance(data, str):
        print(data)
    else:
        print(json.dumps(data, indent=2, default=str))


async def _verify_cold_session() -> int:
    skill_dir = (Path.cwd() / ".agents" / "skills" / "a2ui-textual").resolve()
    if not (skill_dir / "SKILL.md").is_file():
        print(f"ERROR: Missing skill directory at {skill_dir}", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory(prefix="proto_a2ui_textual_") as tmp_root_str:
        isolated_dir = Path(tmp_root_str).resolve()
        save_dir = isolated_dir / "sessions"
        save_dir.mkdir(parents=True, exist_ok=True)

        log_file = configure_sdk_logging(log_dir=isolated_dir)
        catalog = BasicCatalog(ProtocolVersion.V1_0)
        request_processor = A2uiRequestProcessor(
            catalogs=[catalog],
            format_factory=DirectJsonFormatFactory(),
        )

        # Deliberately omit hand-coded v1.0 gotchas from system_instructions so
        # the cold Agent must read .agents/skills/a2ui-textual/SKILL.md and its
        # references/ file on its own.
        config = LocalAgentConfig(
            system_instructions=(
                "You are a UI generation agent building A2UI v1.0 surfaces for a Python Textual TUI. "
                "Always read and follow the relevant skill instructions (and any referenced files) "
                "before emitting your response.\n\n"
                f"{request_processor.prompt_snippet}"
            ),
            skills_paths=[str(skill_dir)],
            workspaces=[str(Path.cwd().resolve())],
            capabilities=types.CapabilitiesConfig(
                enabled_tools=[
                    types.BuiltinTools.FINISH,
                    types.BuiltinTools.VIEW_FILE,
                    types.BuiltinTools.LIST_DIR,
                ],
                enable_subagents=False,
            ),
            policies=[
                policy.deny_all(),
                policy.allow("finish"),
                policy.allow("view_file"),
                policy.allow("list_directory"),
            ],
            app_data_dir=str(isolated_dir),
            save_dir=str(save_dir),
            budget_config=types.BudgetConfig(
                max_model_calls=12,
                max_tool_calls=20,
                max_total_tokens=150_000,
            ),
        )

        cold_prompt = (
            "Please use the a2ui-textual skill (reading its SKILL.md and references first) "
            'to emit a valid A2UI v1.0 `<a2ui-json>[...]</a2ui-json>` surface with `surfaceId`: "cold_skill_verify". '
            "Include:\n"
            "1. A `Column` root component.\n"
            '2. A `Text` title and a `Text` caption bound via `"@path"` (respecting v1.0 Text variants).\n'
            "3. A `Tabs` container with two tabs.\n"
            '4. Inside the first tab, a `List` template bound to `"/items"` rendering `Card`s, each with a `Button` action (using `@path` context).\n'
            '5. Inside the second tab, a `ChoicePicker` bound to `"/filter"` with at least two options.'
        )

        print("PROTOTYPE: Launching fresh empty-context google-antigravity SDK Agent...")
        async with Agent(config) as agent:
            conversation_id = agent.conversation_id
            response = await agent.chat(cold_prompt)
            raw_text = str(await response.text())
            stop_reason = getattr(response, "stop_reason", types.StopReason.UNSPECIFIED)

        _print_section(
            "1. Cold SDK Session Metadata",
            {
                "conversation_id": conversation_id,
                "stop_reason": str(stop_reason),
                "isolated_app_data_dir": str(isolated_dir),
                "sdk_log_file": str(log_file),
            },
        )

        # Parse and strictly validate the A2UI v1.0 payload
        parts = request_processor.parse_response(raw_text)
        narrative_chunks = [p.text.strip() for p in parts if isinstance(p, TextPart) and p.text.strip()]
        raw_messages: list[dict[str, Any]] = []
        for part in parts:
            if isinstance(part, A2uiPart) and part.a2ui:
                raw_messages.extend(to_message_dicts(part.a2ui))

        if not raw_messages:
            print("ERROR: Agent emitted no <a2ui-json> messages.\nRaw text:\n" + raw_text, file=sys.stderr)
            return 1

        strict_processor = MessageProcessor(
            [catalog],
            options=MessageProcessorOptions(validation_config=STRICT_VALIDATION),
        )
        strict_processor.process_messages(raw_messages)

        surface = strict_processor.model.get_surface("cold_skill_verify")
        if surface is None:
            print(
                f"ERROR: Expected surface 'cold_skill_verify', got {list(strict_processor.model.surfaces_map)}",
                file=sys.stderr,
            )
            return 1

        _print_section(
            "2. STRICT_VALIDATION Passed",
            {
                "narrative_preview": "\n".join(narrative_chunks)[:300],
                "message_count": len(raw_messages),
                "component_count": len(list(surface.components_model.entries)),
                "root_id": surface.root_id,
            },
        )

        # Render inside a headless Textual Pilot
        app = _PrototypeVerifyApp(strict_processor)
        async with app.run_test() as pilot:
            await pilot.pause()
            card_count = len(app.query(".a2ui-card"))
            tabbed_count = len(app.query(TabbedContent))
            picker_count = len(app.query(A2UIChoicePicker))
            button_count = len(app.query(A2UIButton))
            markdown_texts = [str(w._markdown) for w in app.query(Markdown)]
            static_texts = [str(w.render()) for w in app.query(Static)]

            pilot_state = {
                "cards_rendered": card_count,
                "tabbed_content_count": tabbed_count,
                "choice_pickers": picker_count,
                "buttons": button_count,
                "markdown_count": len(markdown_texts),
                "static_count": len(static_texts),
                "unresolved_path_dict_leaks": [
                    txt for txt in (markdown_texts + static_texts) if "{'path'" in txt or '{"path"' in txt
                ],
            }
            _print_section("3. Headless Textual Pilot Widget Verification", pilot_state)

            if card_count < 1 or tabbed_count < 1 or picker_count < 1 or button_count < 1:
                print("ERROR: Missing expected rendered Textual widgets.", file=sys.stderr)
                return 1
            if pilot_state["unresolved_path_dict_leaks"]:
                print("ERROR: Unresolved v0.9 path dict leaked into rendered text.", file=sys.stderr)
                return 1

        # Inspect recorded trajectory using TrajectoryStore / detect_skill_activations
        store = TrajectoryStore(gemini_dir=isolated_dir)
        listed_sessions = store.list_sessions(limit=10).sessions
        transcript_files = sorted(str(p) for p in isolated_dir.rglob("transcript*.jsonl"))

        activations_report: list[dict[str, Any]] = []
        if listed_sessions:
            for sess in listed_sessions:
                for act in sess.skill_activations:
                    activations_report.append(act.model_dump())
        else:
            # Inspect any raw JSONL trajectory files created under isolated_dir if stored outside brain/
            for tf in transcript_files:
                steps = store._load_steps(Path(tf))
                for act in detect_skill_activations(steps):
                    activations_report.append(act.model_dump())

        _print_section(
            "4. TrajectoryStore & Skill Activation Inspection",
            {
                "sessions_indexed_by_store": [s.model_dump() for s in listed_sessions],
                "transcript_files_found": transcript_files,
                "detected_skill_activations": activations_report,
                "isolated_files_sample": sorted(str(p.relative_to(isolated_dir)) for p in isolated_dir.rglob("*") if p.is_file())[:30],
            },
        )

        bespoke_hits = [
            a for a in activations_report if a.get("skill_name") == "a2ui-textual" and a.get("tier") == "way_3_bespoke"
        ]
        if not bespoke_hits:
            print(
                "WARNING: Did not detect a2ui-textual Skill Activation in isolated transcript; check transcript path format.",
                file=sys.stderr,
            )
            return 2

        print("\nSUCCESS: Phase 3 cold-session verification passed end-to-end!")
        return 0


def main() -> int:
    return asyncio.run(_verify_cold_session())


if __name__ == "__main__":
    raise SystemExit(main())
