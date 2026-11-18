"""Unit tests for BrainExplorerAgentService and SDK logging configuration."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pytest
from a2ui.core.basic_catalog import BasicCatalog
from a2ui.core.processing import MessageProcessor
from a2ui.core.processing.message_processor import MessageProcessorOptions
from a2ui.core.schema import ProtocolVersion
from a2ui.core.validation import STRICT_VALIDATION
from google.antigravity import types

import brain_explorer.agent_service as agent_service_mod
from brain_explorer.a2ui_textual import A2UI_BASIC_CATALOG_V1_0_ID
from brain_explorer.agent_service import BrainExplorerAgentService, configure_sdk_logging
from brain_explorer.trajectory_store import TrajectoryStore


class _FakeResponse:
    def __init__(self, text_value: str, stop_reason: types.StopReason = types.StopReason.UNSPECIFIED) -> None:
        self._text = text_value
        self.stop_reason = stop_reason

    async def text(self) -> str:
        return self._text


class _FakeAgent:
    def __init__(self, responses: list[_FakeResponse]) -> None:
        self._responses = list(responses)
        self.prompts: list[str] = []

    async def __aenter__(self) -> _FakeAgent:
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        return False

    async def chat(self, prompt: str) -> _FakeResponse:
        self.prompts.append(prompt)
        return self._responses.pop(0)


def _valid_a2ui_block(surface_id: str = "s1", text_val: str = "Hello") -> str:
    payload = [
        {"version": "1.0", "createSurface": {"surfaceId": surface_id, "catalogId": A2UI_BASIC_CATALOG_V1_0_ID}},
        {
            "version": "1.0",
            "updateComponents": {
                "surfaceId": surface_id,
                "components": [{"id": "root", "component": "Text", "text": text_val, "variant": "body"}],
            },
        },
    ]
    import json

    return f"Summary text.\n<a2ui-json>{json.dumps(payload)}</a2ui-json>"


def test_configure_sdk_logging_preserves_file_handlers_and_avoids_duplication(tmp_path: Path) -> None:
    logger = logging.getLogger("google.antigravity")
    old_handlers = list(logger.handlers)
    old_propagate = logger.propagate
    try:
        logger.handlers = [logging.StreamHandler()]
        log_path = configure_sdk_logging(tmp_path)
        assert log_path.parent == tmp_path.resolve()
        assert len(logger.handlers) == 1
        assert isinstance(logger.handlers[0], logging.FileHandler)

        # Calling twice keeps the single FileHandler without stripping or duplicating it
        configure_sdk_logging(tmp_path)
        assert len(logger.handlers) == 1
        assert isinstance(logger.handlers[0], logging.FileHandler)
    finally:
        for h in logger.handlers:
            if isinstance(h, logging.FileHandler):
                h.close()
        logger.handlers = old_handlers
        logger.propagate = old_propagate


def test_build_config_isolation_and_policies(tmp_path: Path) -> None:
    service = BrainExplorerAgentService(store=TrajectoryStore(tmp_path), app_data_dir=tmp_path / "sdk")
    cfg = service.build_config(include_a2ui=True)
    assert cfg.app_data_dir == str((tmp_path / "sdk").resolve())
    assert cfg.save_dir == str((tmp_path / "sdk" / "sessions").resolve())
    assert cfg.capabilities.enable_subagents is False
    assert cfg.capabilities.enabled_tools == [types.BuiltinTools.FINISH]
    assert cfg.budget_config is not None
    assert cfg.budget_config.max_model_calls == 15


@pytest.mark.asyncio
async def test_generate_a2ui_retries_on_missing_block_and_preserves_surface_on_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = BrainExplorerAgentService(store=TrajectoryStore(tmp_path), app_data_dir=tmp_path / "sdk")
    processor = MessageProcessor(
        [BasicCatalog(ProtocolVersion.V1_0)],
        options=MessageProcessorOptions(validation_config=STRICT_VALIDATION),
    )

    # 1. First turn lacks <a2ui-json>, retry succeeds
    fake_agent_retry = _FakeAgent(
        [
            _FakeResponse("Plain text without A2UI tags."),
            _FakeResponse(_valid_a2ui_block("surf_one", "First view")),
        ]
    )
    monkeypatch.setattr(agent_service_mod, "Agent", lambda _cfg: fake_agent_retry)

    reply = await service.generate_a2ui("Show overview", processor)
    assert reply == "Summary text."
    assert len(fake_agent_retry.prompts) == 2
    assert "surf_one" in processor.model.surfaces_map

    # 2. Both turns fail validation -> preserves existing "surf_one" surface cleanly
    invalid_block = (
        '<a2ui-json>[{"version":"1.0","createSurface":{"surfaceId":"surf_two","catalogId":"'
        + A2UI_BASIC_CATALOG_V1_0_ID
        + '"}},{"version":"1.0","updateComponents":{"surfaceId":"surf_two","components":[{"id":"root","component":"Text","text":"Hi","variant":"h1"}]}}]</a2ui-json>'
    )
    fake_agent_fail = _FakeAgent([_FakeResponse(invalid_block), _FakeResponse(invalid_block)])
    monkeypatch.setattr(agent_service_mod, "Agent", lambda _cfg: fake_agent_fail)

    with pytest.raises(RuntimeError, match="failed to emit valid A2UI"):
        await service.generate_a2ui("Break it", processor)
    assert "surf_one" in processor.model.surfaces_map

    # 3. Budget stop reason skips wasted retry turn
    fake_agent_budget = _FakeAgent(
        [_FakeResponse("Partial text", stop_reason=types.StopReason.MAX_MODEL_CALLS_EXCEEDED)]
    )
    monkeypatch.setattr(agent_service_mod, "Agent", lambda _cfg: fake_agent_budget)

    with pytest.raises(RuntimeError, match="MAX_MODEL_CALLS_EXCEEDED"):
        await service.generate_a2ui("Over budget", processor)
    assert len(fake_agent_budget.prompts) == 1
