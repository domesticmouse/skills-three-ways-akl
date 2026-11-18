"""Pydantic response and domain schemas for Brain Explorer."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

SkillTier = Literal["way_1_plugin", "way_2_community", "way_3_bespoke", "unknown"]


class ProjectSummary(BaseModel):
    """Summary of an Antigravity project discovered in ~/.gemini brain storage."""

    name: str = Field(description="Project name derived from workspace path or '(no workspace)'.")
    workspace_path: str | None = Field(default=None, description="Workspace filesystem path if known.")
    session_count: int = Field(ge=0, description="Total number of session trajectories in this project.")
    latest_active: str | None = Field(default=None, description="Most recent session timestamp.")


class ProjectListResult(BaseModel):
    """Structured result containing discovered projects."""

    projects: list[ProjectSummary] = Field(default_factory=list)


class SkillActivationItem(BaseModel):
    """An observed activation of an agent skill within a session trajectory."""

    skill_name: str = Field(description="Name of the activated skill.")
    activation_kind: Literal["slash_command", "skill_md_read", "other"] = Field(
        default="other",
        description="Whether the activation was an explicit <SKILL> slash command or a SKILL.md file read.",
    )
    step_index: int | None = Field(default=None, description="Step index where the skill activation occurred.")
    evidence: str | None = Field(default=None, description="Brief evidence snippet or file path.")
    skill_path: str | None = Field(default=None, description="Resolved path to SKILL.md if present.")
    tier: SkillTier = Field(
        default="unknown",
        description="Classification under Skills Three Ways (plugin, community, or bespoke).",
    )


class SessionTrajectorySummary(BaseModel):
    """High-level summary of a single Antigravity session trajectory."""

    session_id: str = Field(description="Full UUID or identifier of the session trajectory.")
    project: str = Field(description="Associated project name.")
    workspace_path: str | None = Field(default=None, description="Workspace path associated with the session.")
    brain_root: str | None = Field(default=None, description="Brain root directory name (e.g. antigravity).")
    created_at: str | None = Field(default=None, description="Creation timestamp of the session.")
    duration: str | None = Field(default=None, description="Elapsed session duration.")
    step_count: int = Field(ge=0, description="Number of recorded steps in the trajectory.")
    initial_prompt: str | None = Field(default=None, description="Opening user prompt snippet.")
    skill_activations: list[SkillActivationItem] = Field(
        default_factory=list,
        description="Skill activations detected during this session.",
    )


class SessionListResult(BaseModel):
    """Structured result containing session trajectory summaries."""

    sessions: list[SessionTrajectorySummary] = Field(default_factory=list)


class TrajectoryStepSummary(BaseModel):
    """Summary of a single step within a session trajectory."""

    step_index: int = Field(ge=0)
    source: str = Field(description="Step source such as USER_EXPLICIT, MODEL, or SYSTEM.")
    step_type: str = Field(description="Step type such as USER_INPUT or PLANNER_RESPONSE.")
    created_at: str | None = None
    preview: str = Field(description="Short summary of the step content or action.")
    tools_used: list[str] = Field(default_factory=list, description="Tool names invoked in this step.")


class TrajectoryStepDetail(BaseModel):
    """Full drill-down detail for a single step within a session trajectory."""

    step_index: int = Field(ge=0)
    source: str
    step_type: str
    status: str | None = None
    created_at: str | None = None
    content: str = ""
    thinking: str = ""
    tool_calls: list[dict[str, Any]] = Field(default_factory=list)
    step_output: str | None = None


class ToolUsageCount(BaseModel):
    """Frequency count for a single tool invoked in a session trajectory."""

    tool_name: str
    count: int = Field(ge=0)


class SessionTrajectoryDetail(BaseModel):
    """Detailed view of a single Antigravity session trajectory."""

    summary: SessionTrajectorySummary
    workspace_path: str | None = None
    transcript_path: str | None = None
    models_used: list[str] = Field(default_factory=list)
    tool_counts: list[ToolUsageCount] = Field(default_factory=list)
    steps: list[TrajectoryStepSummary] = Field(default_factory=list)


class SessionComparisonResult(BaseModel):
    """Structured comparison between two Antigravity session trajectories."""

    session_a: SessionTrajectorySummary
    session_b: SessionTrajectorySummary
    key_differences: list[str] = Field(default_factory=list)
    summary_comparison: str = Field(description="Concise narrative comparing both sessions.")
