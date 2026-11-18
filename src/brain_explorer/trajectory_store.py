"""Deterministic local filesystem store for Antigravity session trajectories."""

from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from brain_explorer.models import (
    ProjectListResult,
    ProjectSummary,
    SessionComparisonResult,
    SessionListResult,
    SessionTrajectoryDetail,
    SessionTrajectorySummary,
    SkillActivationItem,
    SkillTier,
    ToolUsageCount,
    TrajectoryStepDetail,
    TrajectoryStepSummary,
)

BESPOKE_PROJECT_SKILLS: frozenset[str] = frozenset(
    {"agy-brain-explorer", "slidev-deck", "bjm-voice", "a2ui-textual"}
)

_USER_REQUEST_RE = re.compile(r"<USER_REQUEST>\s*(.*?)\s*</USER_REQUEST>", re.DOTALL)
_SKILL_INVOKED_RE = re.compile(r"The user has explicitly invoked the \(([^)]+)\) skill\.")
_SKILL_REQUESTED_RE = re.compile(
    r'The user requested you read and use the "([^"]+)" skill\.(?:\s*The path to the skill file is:\s*([^\s<]+))?'
)
_SLASH_CMD_LINE_RE = re.compile(r"^/([a-zA-Z0-9_.:-]+)\s+is a \[Slash Command\]", re.MULTILINE)
_MODEL_SELECTION_RE = re.compile(r"setting\s+`Model Selection`\s+from\s+.*?\s+to\s+([^\n.<`]+)")
_PATH_ARG_KEYS: tuple[str, ...] = (
    "AbsolutePath",
    "TargetFile",
    "Path",
    "file_path",
    "path",
    "DirectoryPath",
    "directory_path",
)


@dataclass
class _CachedTranscript:
    mtime_ns: int
    size: int
    steps: list[dict[str, Any]]
    path: Path


@dataclass
class _SessionRecord:
    session_id: str
    brain_root: str
    session_dir: Path
    transcript_path: Path
    steps: list[dict[str, Any]]
    summary: SessionTrajectorySummary
    models_used: list[str]
    tool_counts: Counter[str]


def _parse_iso_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def _format_timestamp(value: str | None) -> str | None:
    dt = _parse_iso_datetime(value)
    if dt is None:
        return value
    return dt.astimezone().strftime("%Y-%m-%d %H:%M")


def _format_duration(start_iso: str | None, end_iso: str | None) -> str | None:
    start_dt = _parse_iso_datetime(start_iso)
    end_dt = _parse_iso_datetime(end_iso)
    if start_dt is None or end_dt is None:
        return None
    seconds = max(0, int((end_dt - start_dt).total_seconds()))
    if seconds < 60:
        return f"{seconds}s"
    minutes, rem_s = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes}m {rem_s:02d}s"
    hours, rem_m = divmod(minutes, 60)
    return f"{hours}h {rem_m:02d}m"


def _classify_skill_tier(skill_name: str, skill_path: str | None) -> SkillTier:
    """Classify a detected Skill Activation under Skills Three Ways."""
    clean_name = skill_name.strip().lstrip("/")
    if skill_path:
        norm = skill_path.replace("\\", "/")
        if "/.gemini/config/plugins/" in norm or "/.gemini/antigravity/builtin/" in norm:
            return "way_1_plugin"
        if "/.agents/skills/" in norm:
            return "way_3_bespoke" if clean_name in BESPOKE_PROJECT_SKILLS else "way_2_community"
    if clean_name in BESPOKE_PROJECT_SKILLS:
        return "way_3_bespoke"
    return "unknown"


def _clean_path(raw: Any) -> str | None:
    if not isinstance(raw, str):
        return None
    val = raw.strip("\"' \t\r\n")
    return val if val else None


def _is_ignored_workspace_prefix(path_str: str, home: Path) -> bool:
    ignored = (
        str(home / ".gemini"),
        str(home / ".agents"),
        str(home / ".cache"),
        "/tmp",
        "/private/tmp",
        "/var/folders",
    )
    return any(path_str == prefix or path_str.startswith(prefix + "/") for prefix in ignored)


def _infer_workspace_from_steps(steps: list[dict[str, Any]]) -> str | None:
    """Infer the most likely project workspace path across session tool calls."""
    home = Path.home()
    candidates: list[str] = []

    for step in steps:
        for tc in step.get("tool_calls") or []:
            if not isinstance(tc, dict):
                continue
            args = tc.get("args")
            if not isinstance(args, dict):
                continue

            cwd = _clean_path(args.get("Cwd") or args.get("cwd"))
            if cwd and cwd != "." and not _is_ignored_workspace_prefix(cwd, home):
                candidates.append(cwd)

            for key in _PATH_ARG_KEYS:
                val = _clean_path(args.get(key))
                if not val or not val.startswith("/") or _is_ignored_workspace_prefix(val, home):
                    continue
                p = Path(val)
                if key in ("DirectoryPath", "directory_path") and p.is_dir():
                    candidates.append(str(p))
                    break
                matched_root: str | None = None
                for parent in p.parents:
                    if parent == home or parent == Path("/"):
                        break
                    if (parent / ".git").is_dir() or (parent / ".agents").is_dir():
                        matched_root = str(parent)
                        break
                candidates.append(matched_root or str(p.parent))

    if not candidates:
        return None
    most_common, _ = Counter(candidates).most_common(1)[0]
    return most_common


def _project_name_from_workspace(workspace: str | None) -> str:
    if not workspace:
        return "(no workspace)"
    p = Path(workspace)
    name = p.name
    if name in ("src", "lib", "bin", "test", "tests", "scripts") and len(p.parents) > 1:
        name = p.parent.name
    return name or workspace


def _extract_user_prompt(content: str) -> str:
    match = _USER_REQUEST_RE.search(content)
    text = match.group(1) if match else content
    return " ".join(text.split())


def detect_skill_activations(steps: list[dict[str, Any]]) -> list[SkillActivationItem]:
    """Deterministically detect Skill Activations across a Session Trajectory.

    Evidenced either by an explicit ``<SKILL>`` slash-command payload in user input
    or by reading a ``SKILL.md`` file during tool execution.
    """
    activations: list[SkillActivationItem] = []
    seen: set[tuple[int | None, str, str]] = set()

    for step in steps:
        step_index = step.get("step_index")
        step_type = str(step.get("type") or "")
        content = str(step.get("content") or "")

        if step_type == "USER_INPUT" and ("<SKILL>" in content or "is a [Slash Command]" in content):
            matched_in_step = False
            for match in _SKILL_REQUESTED_RE.finditer(content):
                name = match.group(1).strip()
                path = match.group(2).strip() if match.group(2) else None
                key = (step_index, name, "slash_command")
                if key not in seen:
                    seen.add(key)
                    activations.append(
                        SkillActivationItem(
                            skill_name=name,
                            activation_kind="slash_command",
                            step_index=step_index,
                            evidence=path or f"/{name} slash command",
                            skill_path=path,
                            tier=_classify_skill_tier(name, path),
                        )
                    )
                    matched_in_step = True

            for match in _SKILL_INVOKED_RE.finditer(content):
                name = match.group(1).strip()
                key = (step_index, name, "slash_command")
                if key not in seen:
                    seen.add(key)
                    activations.append(
                        SkillActivationItem(
                            skill_name=name,
                            activation_kind="slash_command",
                            step_index=step_index,
                            evidence=f"/{name} slash command",
                            skill_path=None,
                            tier=_classify_skill_tier(name, None),
                        )
                    )
                    matched_in_step = True

            if not matched_in_step:
                for match in _SLASH_CMD_LINE_RE.finditer(content):
                    name = match.group(1).strip()
                    key = (step_index, name, "slash_command")
                    if key not in seen:
                        seen.add(key)
                        activations.append(
                            SkillActivationItem(
                                skill_name=name,
                                activation_kind="slash_command",
                                step_index=step_index,
                                evidence=f"/{name} slash command",
                                skill_path=None,
                                tier=_classify_skill_tier(name, None),
                            )
                        )

        for tc in step.get("tool_calls") or []:
            if not isinstance(tc, dict):
                continue
            tool_name = str(tc.get("name") or "")
            if tool_name not in ("read_file", "view_file", "read_resource"):
                continue
            args = tc.get("args")
            if not isinstance(args, dict):
                continue
            for key_name in _PATH_ARG_KEYS:
                raw_path = _clean_path(args.get(key_name))
                if not raw_path:
                    continue
                norm_path = raw_path.replace("\\", "/")
                if norm_path.endswith("/SKILL.md") or norm_path == "SKILL.md":
                    skill_name = Path(norm_path).parent.name or "unknown"
                    key = (step_index, skill_name, "skill_md_read")
                    if key not in seen:
                        seen.add(key)
                        activations.append(
                            SkillActivationItem(
                                skill_name=skill_name,
                                activation_kind="skill_md_read",
                                step_index=step_index,
                                evidence=raw_path,
                                skill_path=raw_path,
                                tier=_classify_skill_tier(skill_name, raw_path),
                            )
                        )
                    break

    return activations


class TrajectoryStore:
    """Fast local repository reading ~/.gemini/*/brain/ session trajectories."""

    def __init__(self, gemini_dir: Path | None = None) -> None:
        """Initialise the local trajectory store.

        Args:
            gemini_dir: Root directory containing brain subdirectories (defaults to ``~/.gemini``).
        """
        self._gemini_dir = (gemini_dir or (Path.home() / ".gemini")).expanduser()
        self._cache: dict[Path, _CachedTranscript] = {}

    @property
    def gemini_dir(self) -> Path:
        """Return the root Gemini storage directory."""
        return self._gemini_dir

    def _find_brain_roots(self) -> list[tuple[str, Path]]:
        """Discover bounded brain directories without descending into step subdirectories."""
        if not self._gemini_dir.is_dir():
            return []
        roots: list[tuple[str, Path]] = []
        direct_brain = self._gemini_dir / "brain"
        if direct_brain.is_dir():
            roots.append((self._gemini_dir.name, direct_brain))
        for child in sorted(self._gemini_dir.iterdir()):
            if not child.is_dir() or child.name.startswith("."):
                continue
            brain_dir = child / "brain"
            if brain_dir.is_dir():
                roots.append((child.name, brain_dir))
        return roots

    def _load_steps(self, transcript_path: Path) -> list[dict[str, Any]]:
        try:
            stat = transcript_path.stat()
        except OSError:
            return []

        cached = self._cache.get(transcript_path)
        if cached is not None and cached.mtime_ns == stat.st_mtime_ns and cached.size == stat.st_size:
            return cached.steps

        steps: list[dict[str, Any]] = []
        try:
            with transcript_path.open(encoding="utf-8", errors="replace") as handle:
                for raw_line in handle:
                    line = raw_line.strip()
                    if not line:
                        continue
                    try:
                        parsed = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if isinstance(parsed, dict):
                        steps.append(parsed)
        except OSError:
            return []

        self._cache[transcript_path] = _CachedTranscript(
            mtime_ns=stat.st_mtime_ns,
            size=stat.st_size,
            steps=steps,
            path=transcript_path,
        )
        return steps

    def _pick_transcript_path(self, session_dir: Path, *, prefer_full: bool = True) -> Path | None:
        logs_dir = session_dir / ".system_generated" / "logs"
        full_path = logs_dir / "transcript_full.jsonl"
        compact_path = logs_dir / "transcript.jsonl"
        order = (full_path, compact_path) if prefer_full else (compact_path, full_path)
        for candidate in order:
            if candidate.is_file():
                return candidate
        return None

    def _build_record(self, brain_root: str, session_dir: Path) -> _SessionRecord | None:
        transcript_path = self._pick_transcript_path(session_dir, prefer_full=True)
        if transcript_path is None:
            return None
        steps = self._load_steps(transcript_path)
        if not steps:
            return None

        start_iso: str | None = None
        end_iso: str | None = None
        initial_prompt: str | None = None
        models: list[str] = []
        tool_counts: Counter[str] = Counter()

        for step in steps:
            ts = step.get("created_at")
            if isinstance(ts, str) and ts:
                if start_iso is None:
                    start_iso = ts
                end_iso = ts

            step_type = str(step.get("type") or "")
            content = str(step.get("content") or "")

            if step_type == "USER_INPUT":
                if initial_prompt is None and content:
                    prompt_text = _extract_user_prompt(content)
                    if prompt_text:
                        initial_prompt = prompt_text[:200]
                for model_match in _MODEL_SELECTION_RE.finditer(content):
                    model_name = model_match.group(1).strip()
                    if model_name and model_name not in models:
                        models.append(model_name)

            for tc in step.get("tool_calls") or []:
                if isinstance(tc, dict):
                    name = str(tc.get("name") or "")
                    if name:
                        tool_counts[name] += 1

        workspace_path = _infer_workspace_from_steps(steps)
        project_name = _project_name_from_workspace(workspace_path)
        activations = detect_skill_activations(steps)

        summary = SessionTrajectorySummary(
            session_id=session_dir.name,
            project=project_name,
            workspace_path=workspace_path,
            brain_root=brain_root,
            created_at=_format_timestamp(start_iso),
            duration=_format_duration(start_iso, end_iso),
            step_count=len(steps),
            initial_prompt=initial_prompt,
            skill_activations=activations,
        )
        return _SessionRecord(
            session_id=session_dir.name,
            brain_root=brain_root,
            session_dir=session_dir,
            transcript_path=transcript_path,
            steps=steps,
            summary=summary,
            models_used=models,
            tool_counts=tool_counts,
        )

    def _iter_records(self) -> list[_SessionRecord]:
        records: list[_SessionRecord] = []
        for brain_root, brain_dir in self._find_brain_roots():
            for entry in brain_dir.iterdir():
                if not entry.is_dir() or entry.name.startswith("."):
                    continue
                rec = self._build_record(brain_root, entry)
                if rec is not None:
                    records.append(rec)

        records.sort(
            key=lambda r: _parse_iso_datetime(
                next((str(s.get("created_at")) for s in r.steps if s.get("created_at")), None)
            )
            or datetime.min.replace(tzinfo=UTC),
            reverse=True,
        )
        return records

    def _resolve_record(self, session_id: str) -> _SessionRecord:
        clean_id = session_id.strip()
        if not clean_id:
            raise ValueError("'session_id' must not be empty.")

        records = self._iter_records()
        exact = [r for r in records if r.session_id == clean_id]
        if exact:
            return exact[0]

        prefix_matches = [r for r in records if r.session_id.startswith(clean_id)]
        if len(prefix_matches) == 1:
            return prefix_matches[0]
        if len(prefix_matches) > 1:
            ids = ", ".join(r.session_id[:12] for r in prefix_matches[:5])
            raise ValueError(f"Ambiguous session prefix '{clean_id}'; matched: {ids}")
        raise FileNotFoundError(f"No session trajectory found matching '{clean_id}'.")

    def list_projects(self) -> ProjectListResult:
        """Discover all projects across ~/.gemini brain directories."""
        grouped: dict[tuple[str, str], dict[str, Any]] = {}
        for rec in self._iter_records():
            key = (rec.summary.project, rec.summary.workspace_path or "")
            bucket = grouped.get(key)
            if bucket is None:
                grouped[key] = {
                    "name": rec.summary.project,
                    "workspace_path": rec.summary.workspace_path,
                    "session_count": 1,
                    "latest_active": rec.summary.created_at,
                }
            else:
                bucket["session_count"] += 1

        projects = [
            ProjectSummary(
                name=data["name"],
                workspace_path=data["workspace_path"],
                session_count=data["session_count"],
                latest_active=data["latest_active"],
            )
            for data in grouped.values()
        ]
        projects.sort(key=lambda p: (p.latest_active or "", p.session_count), reverse=True)
        return ProjectListResult(projects=projects)

    def list_sessions(
        self,
        project: str | None = None,
        limit: int = 20,
        skill_filter: str | None = None,
        brain_root: str | None = None,
    ) -> SessionListResult:
        """List session trajectories ordered newest-first with optional filters."""
        if limit < 1:
            raise ValueError(f"'limit' must be at least 1, got {limit}")

        project_q = project.strip().lower() if project else None
        skill_q = skill_filter.strip().lower() if skill_filter else None
        brain_q = brain_root.strip().lower() if brain_root else None

        filtered: list[SessionTrajectorySummary] = []
        for rec in self._iter_records():
            summary = rec.summary
            if project_q:
                proj_match = project_q in summary.project.lower()
                ws_match = bool(summary.workspace_path and project_q in summary.workspace_path.lower())
                if not (proj_match or ws_match):
                    continue
            if brain_q and (summary.brain_root or "").lower() != brain_q:
                continue
            if skill_q and not any(skill_q in act.skill_name.lower() for act in summary.skill_activations):
                continue

            filtered.append(summary)
            if len(filtered) >= limit:
                break

        return SessionListResult(sessions=filtered)

    def inspect_session(
        self,
        session_id: str,
        step_limit: int | None = None,
    ) -> SessionTrajectoryDetail:
        """Return detailed metadata, Skill Activations, tool counts, and step summaries."""
        rec = self._resolve_record(session_id)
        steps_to_render = rec.steps[:step_limit] if step_limit is not None else rec.steps

        step_summaries: list[TrajectoryStepSummary] = []
        for fallback_idx, step in enumerate(steps_to_render):
            idx = int(step.get("step_index", fallback_idx))
            source = str(step.get("source") or "UNKNOWN")
            step_type = str(step.get("type") or "UNKNOWN")
            created_at = _format_timestamp(step.get("created_at"))
            tools_used = [
                str(tc.get("name"))
                for tc in (step.get("tool_calls") or [])
                if isinstance(tc, dict) and tc.get("name")
            ]

            raw_content = str(step.get("content") or "")
            if step_type == "USER_INPUT":
                preview_text = _extract_user_prompt(raw_content)
            else:
                preview_text = " ".join(raw_content.split())

            if not preview_text and tools_used:
                preview_text = f"Called tools: {', '.join(tools_used)}"
            elif not preview_text:
                thinking = " ".join(str(step.get("thinking") or "").split())
                preview_text = thinking[:140] if thinking else "-"

            step_summaries.append(
                TrajectoryStepSummary(
                    step_index=idx,
                    source=source,
                    step_type=step_type,
                    created_at=created_at,
                    preview=preview_text[:160],
                    tools_used=tools_used,
                )
            )

        tool_counts = [
            ToolUsageCount(tool_name=name, count=count)
            for name, count in rec.tool_counts.most_common()
        ]
        return SessionTrajectoryDetail(
            summary=rec.summary,
            workspace_path=rec.summary.workspace_path,
            transcript_path=str(rec.transcript_path),
            models_used=rec.models_used,
            tool_counts=tool_counts,
            steps=step_summaries,
        )

    def inspect_step(self, session_id: str, step_index: int) -> TrajectoryStepDetail:
        """Return full step content, thinking, tool call args, and step output file if present."""
        rec = self._resolve_record(session_id)
        target_step: dict[str, Any] | None = None
        for fallback_idx, step in enumerate(rec.steps):
            if int(step.get("step_index", fallback_idx)) == step_index:
                target_step = step
                break
        if target_step is None:
            raise ValueError(f"Step {step_index} not found in session '{rec.session_id}'.")

        output_path = rec.session_dir / ".system_generated" / "steps" / str(step_index) / "output.txt"
        step_output: str | None = None
        if output_path.is_file():
            try:
                step_output = output_path.read_text(encoding="utf-8", errors="replace")[:8000]
            except OSError:
                step_output = None

        raw_calls = target_step.get("tool_calls") or []
        tool_calls = [tc for tc in raw_calls if isinstance(tc, dict)]

        return TrajectoryStepDetail(
            step_index=step_index,
            source=str(target_step.get("source") or "UNKNOWN"),
            step_type=str(target_step.get("type") or "UNKNOWN"),
            status=str(target_step["status"]) if target_step.get("status") else None,
            created_at=_format_timestamp(target_step.get("created_at")),
            content=str(target_step.get("content") or ""),
            thinking=str(target_step.get("thinking") or ""),
            tool_calls=tool_calls,
            step_output=step_output,
        )

    def search_sessions(
        self,
        query: str,
        project: str | None = None,
        limit: int = 20,
    ) -> SessionListResult:
        """Search across session prompts, step content, tool calls, and Skill Activations."""
        clean_query = query.strip().lower()
        if not clean_query:
            raise ValueError("'query' must not be empty.")
        if limit < 1:
            raise ValueError(f"'limit' must be at least 1, got {limit}")

        project_q = project.strip().lower() if project else None
        matches: list[SessionTrajectorySummary] = []

        for rec in self._iter_records():
            summary = rec.summary
            if project_q:
                proj_match = project_q in summary.project.lower()
                ws_match = bool(summary.workspace_path and project_q in summary.workspace_path.lower())
                if not (proj_match or ws_match):
                    continue

            haystack_hit = any(clean_query in act.skill_name.lower() for act in summary.skill_activations)
            if not haystack_hit:
                for step in rec.steps:
                    content = str(step.get("content") or "").lower()
                    if clean_query in content:
                        haystack_hit = True
                        break
                    tool_blob = json.dumps(step.get("tool_calls") or []).lower()
                    if clean_query in tool_blob:
                        haystack_hit = True
                        break

            if haystack_hit:
                matches.append(summary)
                if len(matches) >= limit:
                    break

        return SessionListResult(sessions=matches)

    def compare_sessions(self, session_a: str, session_b: str) -> SessionComparisonResult:
        """Compare two session trajectories deterministically by metrics and Skill Activations."""
        rec_a = self._resolve_record(session_a)
        rec_b = self._resolve_record(session_b)
        if rec_a.session_id == rec_b.session_id:
            raise ValueError(f"Cannot compare a session with itself: '{rec_a.session_id}'.")

        skills_a = {a.skill_name for a in rec_a.summary.skill_activations}
        skills_b = {b.skill_name for b in rec_b.summary.skill_activations}
        only_a = sorted(skills_a - skills_b)
        only_b = sorted(skills_b - skills_a)
        shared = sorted(skills_a & skills_b)

        differences: list[str] = [
            f"Steps: {rec_a.session_id[:8]} has {rec_a.summary.step_count} vs {rec_b.session_id[:8]} has {rec_b.summary.step_count}.",
            f"Duration: {rec_a.summary.duration or 'unknown'} vs {rec_b.summary.duration or 'unknown'}.",
            f"Total tool calls: {sum(rec_a.tool_counts.values())} vs {sum(rec_b.tool_counts.values())}.",
        ]
        if only_a:
            differences.append(f"Skills only in {rec_a.session_id[:8]}: {', '.join(only_a)}")
        if only_b:
            differences.append(f"Skills only in {rec_b.session_id[:8]}: {', '.join(only_b)}")
        if shared:
            differences.append(f"Shared skills: {', '.join(shared)}")

        summary_text = (
            f"Session {rec_a.session_id[:8]} ({rec_a.summary.project}, {rec_a.summary.step_count} steps) "
            f"compared with {rec_b.session_id[:8]} ({rec_b.summary.project}, {rec_b.summary.step_count} steps)."
        )
        return SessionComparisonResult(
            session_a=rec_a.summary,
            session_b=rec_b.summary,
            key_differences=differences,
            summary_comparison=summary_text,
        )
