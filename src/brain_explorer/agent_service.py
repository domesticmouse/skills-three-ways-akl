"""In-process Google Antigravity SDK service generating A2UI v1.0 surfaces."""

from __future__ import annotations

import json
import logging
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

from a2ui.core import A2uiError
from a2ui.core.basic_catalog import BasicCatalog
from a2ui.core.processing import MessageProcessor
from a2ui.core.schema import ProtocolVersion
from a2ui.inference_formats.direct_json import DirectJsonFormatFactory
from a2ui.parser.response_part import A2uiPart, TextPart
from a2ui.processor import A2uiRequestProcessor
from google.antigravity import Agent, LocalAgentConfig, types
from google.antigravity.hooks import policy

from brain_explorer.trajectory_store import TrajectoryStore

ISOLATED_APP_DATA_DIR = (Path(tempfile.gettempdir()) / "brain_explorer_sdk_appdata").resolve()


def configure_sdk_logging(log_dir: Path | None = None) -> Path:
    """Redirect SDK and root warnings to a log file so Textual's terminal UI stays clean."""
    target_dir = (log_dir or ISOLATED_APP_DATA_DIR).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    log_file = target_dir / "brain_explorer_sdk.log"

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))

    for logger_name in ("", "google.antigravity", "absl"):
        logger_obj = logging.getLogger(logger_name)
        logger_obj.handlers = [h for h in logger_obj.handlers if not isinstance(h, logging.StreamHandler)]
        if not any(
            isinstance(h, logging.FileHandler) and Path(h.baseFilename) == log_file for h in logger_obj.handlers
        ):
            logger_obj.addHandler(file_handler)
        if logger_name:
            logger_obj.propagate = False

    return log_file


def _build_trajectory_tools(store: TrajectoryStore) -> list[Callable[..., Any]]:
    """Create read-only Python tools bound to a TrajectoryStore instance."""

    def list_projects_tool() -> dict[str, Any]:
        """List all Antigravity projects, session counts, and latest active timestamps."""
        return store.list_projects().model_dump()

    def list_sessions_tool(
        project: str | None = None,
        limit: int = 15,
        skill_filter: str | None = None,
        brain_root: str | None = None,
    ) -> dict[str, Any]:
        """List recent Antigravity session trajectories with detected Skill Activations."""
        clamped_limit = max(1, min(limit, 50))
        return store.list_sessions(
            project=project,
            limit=clamped_limit,
            skill_filter=skill_filter,
            brain_root=brain_root,
        ).model_dump()

    def inspect_session_tool(session_id: str, step_limit: int = 40) -> dict[str, Any]:
        """Inspect a session trajectory's metadata, models, tool counts, Skill Activations, and steps."""
        clamped_steps = max(1, min(step_limit, 200))
        return store.inspect_session(session_id=session_id, step_limit=clamped_steps).model_dump()

    def inspect_step_tool(session_id: str, step_index: int) -> dict[str, Any]:
        """Inspect one trajectory step's full prompt/content, model thinking, tool call args, and output."""
        return store.inspect_step(session_id=session_id, step_index=step_index).model_dump()

    def search_sessions_tool(
        query: str,
        project: str | None = None,
        limit: int = 15,
    ) -> dict[str, Any]:
        """Search across session prompts, step text, tool calls, and Skill Activations."""
        clamped_limit = max(1, min(limit, 50))
        return store.search_sessions(query=query, project=project, limit=clamped_limit).model_dump()

    def compare_sessions_tool(session_a: str, session_b: str) -> dict[str, Any]:
        """Compare two session trajectories side-by-side by metrics and Skill Activations."""
        return store.compare_sessions(session_a=session_a, session_b=session_b).model_dump()

    return [
        list_projects_tool,
        list_sessions_tool,
        inspect_session_tool,
        inspect_step_tool,
        search_sessions_tool,
        compare_sessions_tool,
    ]


class BrainExplorerAgentService:
    """Service orchestrating the Google Antigravity SDK Agent with A2UI v1.0 output."""

    def __init__(
        self,
        store: TrajectoryStore | None = None,
        app_data_dir: Path | None = None,
    ) -> None:
        """Initialise the agent service with an isolated app_data_dir and A2UI v1.0 catalog.

        Args:
            store: Local TrajectoryStore used by the Agent's read-only tools.
            app_data_dir: Isolated directory outside ``~/.gemini`` for SDK artifacts.
        """
        self._store = store or TrajectoryStore()
        self._app_data_dir = (app_data_dir or ISOLATED_APP_DATA_DIR).resolve()
        self._app_data_dir.mkdir(parents=True, exist_ok=True)
        self._catalog = BasicCatalog(ProtocolVersion.V1_0)
        self._a2ui_processor = A2uiRequestProcessor(
            catalogs=[self._catalog],
            format_factory=DirectJsonFormatFactory(),
        )
        self._tools = _build_trajectory_tools(self._store)
        self._last_messages: list[dict[str, Any]] = []

    @property
    def store(self) -> TrajectoryStore:
        """Return the underlying TrajectoryStore."""
        return self._store

    @property
    def last_messages(self) -> list[dict[str, Any]]:
        """Return the raw A2UI v1.0 JSON message dictionaries from the last turn."""
        return list(self._last_messages)

    def build_config(self, *, include_a2ui: bool = True) -> LocalAgentConfig:
        """Build an isolated, read-only, budget-capped LocalAgentConfig.

        Args:
            include_a2ui: Whether to embed the A2UI v1.0 catalog prompt instructions.

        Returns:
            Configured LocalAgentConfig instance.
        """
        base_instructions = (
            "You are the Brain Explorer agent helping the user explore Antigravity Session Trajectories "
            "and Skill Activations across Skills Three Ways (Way 1: Ecosystem & Plugin, Way 2: Community "
            "Workflow, Way 3: Bespoke In-Project). Always call the provided trajectory tools to read "
            "real data before answering; never invent session IDs, counts, timestamps, or skill names.\n"
        )
        if include_a2ui:
            instructions = (
                f"{base_instructions}\n"
                "Compose an expressive, well-structured UI answering the user's request using A2UI v1.0. "
                "Always emit a complete self-contained surface starting with `createSurface` (using "
                f"`catalogId`: `{self._catalog.catalog_id}` and `version`: `1.0`). Use interactive `Button` "
                "actions (e.g. `inspect_session`, `inspect_step`, `compare_sessions`, `search_sessions`) "
                "with relevant `context` fields so the user can drill down from the TUI.\n"
                f"{self._a2ui_processor.prompt_snippet}"
            )
        else:
            instructions = base_instructions

        tool_policies = [
            policy.deny_all(),
            policy.allow("view_file"),
            policy.allow("finish"),
            *(policy.allow(fn.__name__) for fn in self._tools),
        ]
        return LocalAgentConfig(
            system_instructions=instructions,
            capabilities=types.CapabilitiesConfig(
                enabled_tools=[types.BuiltinTools.VIEW_FILE, types.BuiltinTools.FINISH],
            ),
            tools=self._tools,
            policies=tool_policies,
            app_data_dir=str(self._app_data_dir),
            budget_config=types.BudgetConfig(
                max_model_calls=15,
                max_tool_calls=25,
                max_total_tokens=200_000,
            ),
        )

    def _apply_a2ui_messages(
        self,
        processor: MessageProcessor,
        raw_messages: list[dict[str, Any]],
    ) -> None:
        """Apply validated A2UI messages onto ``processor``, replacing colliding surfaces cleanly."""
        creating_ids = {
            msg["createSurface"]["surfaceId"]
            for msg in raw_messages
            if isinstance(msg.get("createSurface"), dict) and msg["createSurface"].get("surfaceId")
        }
        if creating_ids:
            for existing_id in list(processor.model.surfaces_map):
                processor.model.delete_surface(existing_id)

        processor.process_messages(raw_messages)

    async def generate_a2ui(self, user_prompt: str, processor: MessageProcessor) -> str:
        """Send an open-ended question to the Agent, validate its A2UI output, and update ``processor``.

        Args:
            user_prompt: Open-ended question or instruction from the user.
            processor: Active MessageProcessor holding the TUI's rendered surfaces.

        Returns:
            Accompanying conversational text from the Agent.

        Raises:
            ValueError: If ``user_prompt`` is blank.
            RuntimeError: If the Agent produces invalid A2UI output after retry.
        """
        clean_prompt = user_prompt.strip()
        if not clean_prompt:
            raise ValueError("'user_prompt' must not be empty.")

        config = self.build_config(include_a2ui=True)
        async with Agent(config) as agent:
            response = await agent.chat(clean_prompt)
            raw_text = await response.text()

            parts = None
            last_error: Exception | None = None
            for attempt in range(2):
                try:
                    parts = self._a2ui_processor.parse_response(raw_text)
                    break
                except A2uiError as exc:
                    last_error = exc
                    if attempt == 1:
                        break
                    repair_prompt = (
                        f"Your previous A2UI block failed schema/catalog validation with:\n{exc}\n\n"
                        "Please emit a corrected `<a2ui-json>[...]</a2ui-json>` array following A2UI v1.0 "
                        f"with `version: \"1.0\"` and `catalogId: \"{self._catalog.catalog_id}\"`."
                    )
                    retry_resp = await agent.chat(repair_prompt)
                    raw_text = await retry_resp.text()

            if parts is None:
                raise RuntimeError(f"Agent failed to emit valid A2UI v1.0 payload: {last_error}") from last_error

        text_chunks: list[str] = []
        serialized_messages: list[dict[str, Any]] = []
        for part in parts:
            if isinstance(part, TextPart):
                stripped = part.text.strip()
                if stripped:
                    text_chunks.append(stripped)
            elif isinstance(part, A2uiPart):
                for msg in part.a2ui:
                    serialized_messages.append(msg.model_dump(by_alias=True, exclude_none=True))

        if not serialized_messages:
            raise RuntimeError(
                "Agent responded without any `<a2ui-json>` surface blocks. "
                f"Text response: {raw_text[:250]}"
            )

        self._apply_a2ui_messages(processor, serialized_messages)
        self._last_messages = serialized_messages
        return "\n\n".join(text_chunks) if text_chunks else "Updated A2UI surface."

    async def handle_a2ui_action(
        self,
        action_name: str,
        context: dict[str, Any],
        processor: MessageProcessor,
    ) -> str:
        """Translate a clicked A2UI component action into an Agent turn that updates the surface."""
        context_json = json.dumps(context, ensure_ascii=False)
        prompt = (
            f"The user clicked an A2UI action `{action_name}` with context `{context_json}`.\n"
            "Use the appropriate trajectory inspection tools for that context and emit a new A2UI v1.0 "
            "surface displaying the requested detail, drill-down, or comparison."
        )
        return await self.generate_a2ui(prompt, processor)

    async def ask_narrative(self, prompt: str) -> str:
        """Run a concise plain-text analysis turn backed by the read-only trajectory tools."""
        clean_prompt = prompt.strip()
        if not clean_prompt:
            raise ValueError("'prompt' must not be empty.")
        config = self.build_config(include_a2ui=False)
        async with Agent(config) as agent:
            response = await agent.chat(clean_prompt)
            return str(await response.text()).strip()
