"""Interactive Textualize (Textual) TUI prototype for Brain Explorer with A2UI v1.0."""

from __future__ import annotations

import json
from typing import Any, Literal, Protocol

from a2ui.core.processing import MessageProcessor
from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Footer, Header, Input, Label, ListItem, ListView, Static

from brain_explorer.a2ui_textual import (
    A2UIActionDispatched,
    A2UISurfaceWidget,
    create_overview_processor,
    extract_surface_snapshot,
)
from brain_explorer.agent_service import BrainExplorerAgentService, configure_sdk_logging
from brain_explorer.models import SessionTrajectorySummary
from brain_explorer.trajectory_store import TrajectoryStore

VariantKey = Literal["A", "B", "C"]
VARIANT_ORDER: tuple[VariantKey, ...] = ("A", "B", "C")
VARIANT_LABELS: dict[VariantKey, str] = {
    "A": "A (Canvas-First A2UI)",
    "B": "B (Split Navigator + A2UI)",
    "C": "C (Studio + A2UI Protocol)",
}


class AgentServiceProtocol(Protocol):
    """Structural interface for the A2UI-generating Antigravity SDK service."""

    @property
    def last_messages(self) -> list[dict[str, Any]]: ...

    async def generate_a2ui(self, user_prompt: str, processor: MessageProcessor) -> str: ...

    async def handle_a2ui_action(
        self,
        action_name: str,
        context: dict[str, Any],
        processor: MessageProcessor,
    ) -> str: ...


class SessionNavItem(ListItem):
    """Sidebar list entry representing a local Session Trajectory."""

    def __init__(self, summary: SessionTrajectorySummary) -> None:
        skills_tag = f" [{len(summary.skill_activations)} skills]" if summary.skill_activations else ""
        label_text = f"{summary.session_id[:8]} · {summary.project}{skills_tag}"
        super().__init__(Label(label_text))
        self.summary = summary


class BrainExplorerApp(App[None]):
    """Interactive Textual TUI rendering Antigravity SDK A2UI v1.0 surfaces."""

    TITLE = "Brain Explorer"
    SUB_TITLE = "A2UI v1.0 + Google Antigravity SDK"
    AUTO_FOCUS = None

    CSS = """
    Screen {
        layout: vertical;
    }
    #prompt-bar {
        height: auto;
        padding: 0 1;
        background: $panel;
        border-bottom: solid $primary;
    }
    #prompt-input {
        width: 1fr;
    }
    #preset-row {
        height: auto;
        padding: 0 1 1 1;
        background: $panel;
    }
    .preset-btn {
        margin-right: 1;
        min-width: 12;
        height: 3;
    }
    #workspace {
        height: 1fr;
    }
    #sidebar {
        width: 38;
        border-right: solid $primary;
        background: $surface;
        padding: 1;
    }
    #sidebar-title {
        text-style: bold;
        margin-bottom: 1;
        color: $accent;
    }
    #session-list {
        height: 1fr;
    }
    #canvas-pane {
        width: 1fr;
        height: 1fr;
    }
    #inspector-pane {
        width: 48%;
        border-left: solid $primary;
        background: $surface-darken-1;
        padding: 1;
    }
    #inspector-title {
        text-style: bold;
        color: $secondary;
        margin-bottom: 1;
    }
    #inspector-body {
        height: 1fr;
    }
    #status-line {
        height: auto;
        padding: 0 2;
        background: $surface;
        color: $text-muted;
        border-top: solid $panel;
    }
    #variant-bar {
        height: auto;
        align: center middle;
        padding: 0 1;
        background: $boost;
        border-top: solid $accent;
    }
    #variant-label {
        padding: 1 2;
        text-style: bold;
        color: $text;
    }
    .variant-nav-btn {
        min-width: 5;
        height: 3;
    }
    """

    BINDINGS = [
        Binding("1", "select_variant('A')", "Variant A", show=True),
        Binding("2", "select_variant('B')", "Variant B", show=True),
        Binding("3", "select_variant('C')", "Variant C", show=True),
        Binding("/", "focus_prompt", "Ask", show=True),
        Binding("escape", "blur_prompt", "Canvas", show=False),
        Binding("ctrl+r", "reset_overview", "Overview", show=True),
        Binding("q", "quit", "Quit", show=True),
    ]

    def __init__(
        self,
        store: TrajectoryStore | None = None,
        agent_service: AgentServiceProtocol | None = None,
        initial_variant: VariantKey = "A",
        *,
        configure_logging: bool = True,
    ) -> None:
        super().__init__()
        self._store = store or TrajectoryStore()
        self._agent_service: AgentServiceProtocol = agent_service or BrainExplorerAgentService(store=self._store)
        self._variant: VariantKey = initial_variant
        self._configure_logging = configure_logging
        self._processor: MessageProcessor = create_overview_processor(self._store)
        self._sessions_cache: list[SessionTrajectorySummary] = self._store.list_sessions(limit=25).sessions

    @property
    def current_variant(self) -> VariantKey:
        """Return the active prototype layout variant key."""
        return self._variant

    @property
    def processor(self) -> MessageProcessor:
        """Return the active A2UI MessageProcessor."""
        return self._processor

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="prompt-bar"):
            yield Input(
                placeholder="Ask the Antigravity SDK Agent anything about your Session Trajectories...",
                id="prompt-input",
            )
            yield Button("Ask Agent", id="ask-btn", variant="primary")
        with Horizontal(id="preset-row"):
            yield Button("Overview", id="preset-overview", classes="preset-btn")
            yield Button("Skill Activations", id="preset-skills", classes="preset-btn")
            yield Button("Compare Top 2", id="preset-compare", classes="preset-btn")
            yield Button("Three Ways Audit", id="preset-three-ways", classes="preset-btn")
        with Horizontal(id="workspace"):
            with Vertical(id="sidebar"):
                yield Static("Session Trajectories (Local)", id="sidebar-title")
                yield ListView(
                    *(SessionNavItem(sess) for sess in self._sessions_cache),
                    id="session-list",
                )
            with Vertical(id="canvas-pane"):
                yield A2UISurfaceWidget(processor=self._processor, id="a2ui-canvas")
            with VerticalScroll(id="inspector-pane"):
                yield Static("A2UI v1.0 Protocol & DataModel Inspector", id="inspector-title")
                yield Static("", id="inspector-body")
        yield Static("Ready — local A2UI overview loaded. Enter a prompt or click an A2UI action.", id="status-line")
        with Horizontal(id="variant-bar"):
            yield Button("◀", id="prev-variant-btn", classes="variant-nav-btn")
            yield Static(VARIANT_LABELS[self._variant], id="variant-label")
            yield Button("▶", id="next-variant-btn", classes="variant-nav-btn")
        yield Footer()

    async def on_mount(self) -> None:
        if self._configure_logging:
            configure_sdk_logging()
        self._apply_variant_layout()
        self._update_inspector()
        self.set_focus(None)

    def _apply_variant_layout(self) -> None:
        sidebar = self.query_one("#sidebar", Vertical)
        inspector = self.query_one("#inspector-pane", VerticalScroll)
        variant_label = self.query_one("#variant-label", Static)

        sidebar.display = self._variant == "B"
        inspector.display = self._variant == "C"
        variant_label.update(VARIANT_LABELS[self._variant])

    def _update_inspector(self) -> None:
        inspector_body = self.query_one("#inspector-body", Static)
        payload = {
            "lastAgentMessages": self._agent_service.last_messages,
            "activeSurfaces": extract_surface_snapshot(self._processor),
        }
        inspector_body.update(json.dumps(payload, indent=2, default=str))

    def _set_status(self, message: str) -> None:
        self.query_one("#status-line", Static).update(message)

    def action_select_variant(self, variant: VariantKey) -> None:
        """Switch directly to prototype layout variant A, B, or C."""
        self._variant = variant
        self._apply_variant_layout()

    def action_focus_prompt(self) -> None:
        """Focus the agent prompt input box."""
        self.query_one("#prompt-input", Input).focus()

    def action_blur_prompt(self) -> None:
        """Return keyboard focus from the prompt input box to the workspace."""
        self.set_focus(None)

    def _cycle_variant(self, step: int) -> None:
        idx = VARIANT_ORDER.index(self._variant)
        self._variant = VARIANT_ORDER[(idx + step) % len(VARIANT_ORDER)]
        self._apply_variant_layout()

    async def action_reset_overview(self) -> None:
        """Reload the deterministic local A2UI overview surface."""
        self._sessions_cache = self._store.list_sessions(limit=25).sessions
        self._processor = create_overview_processor(self._store)
        canvas = self.query_one("#a2ui-canvas", A2UISurfaceWidget)
        await canvas.set_processor(self._processor)
        self._update_inspector()
        self._set_status("Refreshed deterministic local overview surface.")

    @work(exclusive=True)
    async def _run_agent_prompt(self, prompt_text: str) -> None:
        self._set_status("Asking Google Antigravity SDK Agent to compose an A2UI surface...")
        try:
            reply_text = await self._agent_service.generate_a2ui(prompt_text, self._processor)
        except Exception as exc:
            self._set_status(f"Agent error: {exc}")
            return
        canvas = self.query_one("#a2ui-canvas", A2UISurfaceWidget)
        await canvas.refresh_surfaces()
        self._update_inspector()
        first_line = reply_text.splitlines()[0] if reply_text else "A2UI surface updated."
        self._set_status(f"Agent: {first_line[:140]}")

    @work(exclusive=True)
    async def _run_agent_action(self, action_name: str, context: dict[str, Any]) -> None:
        self._set_status(f"Running A2UI action '{action_name}' via Antigravity SDK Agent...")
        try:
            reply_text = await self._agent_service.handle_a2ui_action(action_name, context, self._processor)
        except Exception as exc:
            self._set_status(f"Action error ({action_name}): {exc}")
            return
        canvas = self.query_one("#a2ui-canvas", A2UISurfaceWidget)
        await canvas.refresh_surfaces()
        self._update_inspector()
        first_line = reply_text.splitlines()[0] if reply_text else f"Completed '{action_name}'."
        self._set_status(f"Agent: {first_line[:140]}")

    def _submit_prompt_input(self) -> None:
        prompt_input = self.query_one("#prompt-input", Input)
        text = prompt_input.value.strip()
        if not text:
            self._set_status("Enter a question before asking the Agent.")
            return
        prompt_input.value = ""
        self._run_agent_prompt(text)

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "prompt-input":
            self._submit_prompt_input()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        if btn_id == "ask-btn":
            self._submit_prompt_input()
        elif btn_id == "prev-variant-btn":
            self._cycle_variant(-1)
        elif btn_id == "next-variant-btn":
            self._cycle_variant(1)
        elif btn_id == "preset-overview":
            await self.action_reset_overview()
        elif btn_id == "preset-skills":
            self._run_agent_prompt(
                "Summarise all Skill Activations across our recent Session Trajectories, grouped by Skills Three Ways tier, with buttons to inspect individual sessions."
            )
        elif btn_id == "preset-compare":
            self._run_agent_prompt(
                "Compare the two most recent Session Trajectories in skills-three-ways-akl, highlighting differences in steps, tools, and Skill Activations."
            )
        elif btn_id == "preset-three-ways":
            self._run_agent_prompt(
                "Create a tabbed A2UI view breaking down our recent projects and which Skills Three Ways tiers (Way 1 Plugin, Way 2 Community, Way 3 Bespoke) fired in them."
            )

    async def on_a2uiaction_dispatched(self, event: A2UIActionDispatched) -> None:
        if event.action_name == "refresh_overview":
            await self.action_reset_overview()
            return
        self._run_agent_action(event.action_name, event.context)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if isinstance(event.item, SessionNavItem):
            sid = event.item.summary.session_id
            self._run_agent_action("inspect_session", {"session_id": sid})
