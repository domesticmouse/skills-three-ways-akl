"""Interactive Textualize (Textual) TUI for Brain Explorer with A2UI v1.0."""

from __future__ import annotations

import json
from typing import Any, Protocol

from a2ui.core.processing import MessageProcessor
from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Footer, Header, Input, Label, ListItem, ListView, Static

from brain_explorer.a2ui_textual import (
    A2UIActionDispatched,
    A2UISurfaceWidget,
    build_local_session_detail_messages,
    create_overview_processor,
    create_strict_processor,
    extract_surface_snapshot,
)
from brain_explorer.agent_service import BrainExplorerAgentService, configure_sdk_logging
from brain_explorer.models import ProjectSummary, SessionTrajectorySummary
from brain_explorer.trajectory_store import TrajectoryStore


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
        super().__init__(Label(label_text, markup=False))
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
        width: 45%;
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
    """

    BINDINGS = [
        Binding("ctrl+b", "toggle_sidebar", "Sidebar", show=True),
        Binding("ctrl+i", "toggle_inspector", "Inspector", show=True),
        Binding("/", "focus_prompt", "Ask", show=True),
        Binding("escape", "blur_prompt", "Canvas", show=False),
        Binding("ctrl+r", "reset_overview", "Overview", show=True),
        Binding("q", "quit", "Quit", show=True),
    ]

    def __init__(
        self,
        store: TrajectoryStore | None = None,
        agent_service: AgentServiceProtocol | None = None,
        *,
        show_sidebar: bool = True,
        show_inspector: bool = False,
        configure_logging: bool = True,
    ) -> None:
        super().__init__()
        self._store = store or TrajectoryStore()
        self._agent_service: AgentServiceProtocol = agent_service or BrainExplorerAgentService(store=self._store)
        self._show_sidebar = show_sidebar
        self._show_inspector = show_inspector
        self._configure_logging = configure_logging

        initial_projects: list[ProjectSummary] = self._store.list_projects().projects
        self._sessions_cache: list[SessionTrajectorySummary] = self._store.list_sessions(limit=25).sessions
        self._processor: MessageProcessor = create_overview_processor(
            self._store,
            projects=initial_projects,
            sessions=self._sessions_cache[:12],
        )

    @property
    def sidebar_visible(self) -> bool:
        """Return whether the local trajectory sidebar is shown."""
        return self._show_sidebar

    @property
    def inspector_visible(self) -> bool:
        """Return whether the A2UI protocol inspector is shown."""
        return self._show_inspector

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
            yield Button("Toggle Sidebar (Ctrl+B)", id="toggle-sidebar-btn", classes="preset-btn")
            yield Button("Toggle Inspector (Ctrl+I)", id="toggle-inspector-btn", classes="preset-btn")
        with Horizontal(id="workspace"):
            with Vertical(id="sidebar"):
                yield Static("Session Trajectories (Local)", id="sidebar-title", markup=False)
                yield ListView(
                    *(SessionNavItem(sess) for sess in self._sessions_cache),
                    id="session-list",
                )
            with Vertical(id="canvas-pane"):
                yield A2UISurfaceWidget(processor=self._processor, id="a2ui-canvas")
            with VerticalScroll(id="inspector-pane"):
                yield Static("A2UI v1.0 Protocol & DataModel Inspector", id="inspector-title", markup=False)
                yield Static("", id="inspector-body", markup=False)
        yield Static(
            "Ready — local A2UI overview loaded. Select a session, press / to ask, or Ctrl+I for protocol inspector.",
            id="status-line",
            markup=False,
        )
        yield Footer()

    async def on_mount(self) -> None:
        if self._configure_logging:
            configure_sdk_logging()
        self._apply_panel_visibility()
        self._update_inspector()

    def _apply_panel_visibility(self) -> None:
        self.query_one("#sidebar", Vertical).display = self._show_sidebar
        self.query_one("#inspector-pane", VerticalScroll).display = self._show_inspector

    def _update_inspector(self) -> None:
        inspector_body = self.query_one("#inspector-body", Static)
        payload = {
            "lastAgentMessages": self._agent_service.last_messages,
            "activeSurfaces": extract_surface_snapshot(self._processor),
        }
        inspector_body.update(json.dumps(payload, indent=2, default=str))

    def _set_status(self, message: str) -> None:
        self.query_one("#status-line", Static).update(message)

    def action_toggle_sidebar(self) -> None:
        """Toggle visibility of the local Session Trajectories sidebar."""
        self._show_sidebar = not self._show_sidebar
        self._apply_panel_visibility()

    def action_toggle_inspector(self) -> None:
        """Toggle visibility of the A2UI v1.0 protocol and DataModel inspector."""
        self._show_inspector = not self._show_inspector
        self._apply_panel_visibility()

    def action_focus_prompt(self) -> None:
        """Focus the agent prompt input box."""
        self.query_one("#prompt-input", Input).focus()

    def action_blur_prompt(self) -> None:
        """Return keyboard focus from the prompt input box to the workspace."""
        self.set_focus(None)

    async def _repopulate_sidebar(self) -> None:
        session_list = self.query_one("#session-list", ListView)
        await session_list.clear()
        await session_list.extend([SessionNavItem(sess) for sess in self._sessions_cache])

    async def action_reset_overview(self) -> None:
        """Cancel active agent workers and reload the deterministic local A2UI overview surface."""
        self.workers.cancel_all()
        projects = self._store.list_projects().projects
        self._sessions_cache = self._store.list_sessions(limit=25).sessions
        self._processor = create_overview_processor(
            self._store,
            projects=projects,
            sessions=self._sessions_cache[:12],
        )
        await self._repopulate_sidebar()
        canvas = self.query_one("#a2ui-canvas", A2UISurfaceWidget)
        await canvas.set_processor(self._processor)
        self._update_inspector()
        self._set_status("Refreshed deterministic local overview surface.")

    async def _show_local_session_detail(self, session_id: str) -> None:
        self.workers.cancel_all()
        try:
            detail = self._store.inspect_session(session_id)
        except (FileNotFoundError, ValueError) as exc:
            self._set_status(f"Local inspect error: {exc}")
            return
        self._processor = create_strict_processor(build_local_session_detail_messages(detail))
        canvas = self.query_one("#a2ui-canvas", A2UISurfaceWidget)
        await canvas.set_processor(self._processor)
        self._update_inspector()
        self._set_status(f"Loaded local Session Trajectory {detail.summary.session_id[:8]}.")

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
        elif btn_id == "toggle-sidebar-btn":
            self.action_toggle_sidebar()
        elif btn_id == "toggle-inspector-btn":
            self.action_toggle_inspector()
        elif btn_id == "preset-overview":
            await self.action_reset_overview()
        elif btn_id == "preset-skills":
            self._run_agent_prompt(
                "Summarise all Skill Activations across our recent Session Trajectories, grouped by Skills Three Ways tier, with buttons to inspect individual sessions."
            )
        elif btn_id == "preset-compare":
            if len(self._sessions_cache) >= 2:
                first_id = self._sessions_cache[0].session_id
                second_id = self._sessions_cache[1].session_id
                self._run_agent_prompt(
                    f"Compare Session Trajectories {first_id} and {second_id}, highlighting differences in steps, tools, and Skill Activations."
                )
            else:
                self._run_agent_prompt(
                    "Compare the two most recent Session Trajectories across discovered projects, highlighting differences in steps, tools, and Skill Activations."
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

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        if isinstance(event.item, SessionNavItem):
            await self._show_local_session_detail(event.item.summary.session_id)
