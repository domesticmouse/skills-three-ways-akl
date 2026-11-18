"""Textualize (Textual) renderer and surface builders for A2UI v1.0."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Literal

from a2ui.core.basic_catalog import BasicCatalog
from a2ui.core.processing import MessageProcessor
from a2ui.core.processing.message_processor import MessageProcessorOptions
from a2ui.core.resolution import DataContext
from a2ui.core.schema import ProtocolVersion
from a2ui.core.state import ComponentModel, SurfaceModel
from a2ui.core.validation import STRICT_VALIDATION
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Button, Checkbox, Input, Markdown, Rule, Select, Static, TabbedContent, TabPane

from brain_explorer.models import ProjectSummary, SessionTrajectoryDetail, SessionTrajectorySummary
from brain_explorer.trajectory_store import TrajectoryStore

A2UI_BASIC_CATALOG_V1_0_ID = BasicCatalog(ProtocolVersion.V1_0).catalog_id


class A2UIActionDispatched(Message):
    """Textual message posted when a user triggers an A2UI component action."""

    def __init__(self, surface_id: str, action_name: str, context: dict[str, Any]) -> None:
        super().__init__()
        self.surface_id = surface_id
        self.action_name = action_name
        self.context = context


class A2UIButton(Button):
    """Textual Button carrying unresolved A2UI action metadata for click-time evaluation."""

    def __init__(
        self,
        label: str,
        *,
        component_id: str,
        surface_id: str,
        raw_action: dict[str, Any] | None,
        data_context: DataContext,
        variant: str = "default",
    ) -> None:
        textual_variant: Literal["default", "primary"] = "primary" if variant == "primary" else "default"
        super().__init__(label, variant=textual_variant, classes="a2ui-button")
        self.component_id = component_id
        self.surface_id = surface_id
        self.raw_action = raw_action
        self.data_context = data_context


class A2UITextField(Input):
    """Textual Input bound to an A2UI DataModel path."""

    def __init__(
        self,
        *,
        surface: SurfaceModel,
        data_context: DataContext,
        bound_path: str | None,
        value: str,
        placeholder: str,
    ) -> None:
        super().__init__(value=value, placeholder=placeholder, classes="a2ui-textfield")
        self.surface = surface
        self.data_context = data_context
        self.bound_path = bound_path


class A2UICheckBox(Checkbox):
    """Textual Checkbox bound to an A2UI DataModel path."""

    def __init__(
        self,
        label: str,
        *,
        value: bool,
        data_context: DataContext,
        bound_path: str | None,
    ) -> None:
        super().__init__(label, value=value, classes="a2ui-checkbox")
        self.data_context = data_context
        self.bound_path = bound_path


class A2UIChoicePicker(Select[str]):
    """Textual Select bound to an A2UI DataModel DynamicStringList path."""

    def __init__(
        self,
        options: list[tuple[str, str]],
        *,
        prompt: str,
        initial_value: str | None,
        data_context: DataContext,
        bound_path: str | None,
    ) -> None:
        kwargs: dict[str, Any] = {"prompt": prompt, "classes": "a2ui-choicepicker"}
        if initial_value is not None and any(val == initial_value for _, val in options):
            kwargs["value"] = initial_value
        super().__init__(options, **kwargs)
        self.data_context = data_context
        self.bound_path = bound_path


def _resolve_value(data_ctx: DataContext, raw: Any, default: Any = None) -> Any:
    if raw is None:
        return default
    try:
        resolved = data_ctx.resolve_dynamic_value(raw)
        return default if resolved is None else resolved
    except Exception:
        return default


def _resolve_str(data_ctx: DataContext, raw: Any, default: str = "") -> str:
    val = _resolve_value(data_ctx, raw, default)
    if val is None:
        return default
    return str(val)


def _extract_bound_path(raw: Any) -> str | None:
    if isinstance(raw, dict):
        bound = raw.get("@path") or raw.get("path")
        if isinstance(bound, str):
            return bound
    return None


def _resolve_button_label(
    surface: SurfaceModel,
    comp: ComponentModel,
    data_ctx: DataContext,
) -> str:
    child_id = comp.properties.get("child")
    if isinstance(child_id, str):
        child = surface.components_model.get(child_id)
        if child is not None and child.type == "Text":
            label = _resolve_str(data_ctx, child.properties.get("text"), "")
            if label:
                return label
    return comp.id


def _render_component(
    surface: SurfaceModel,
    component_id: str,
    data_ctx: DataContext,
    visited: frozenset[str] = frozenset(),
) -> Widget:
    if component_id in visited:
        return Static(f"[Cycle detected at {component_id}]", markup=False, classes="a2ui-error")

    comp = surface.components_model.get(component_id)
    if comp is None:
        return Static(f"[Missing component: {component_id}]", markup=False, classes="a2ui-missing")

    next_visited = visited | {component_id}
    props = comp.properties
    comp_type = comp.type

    if comp_type == "Text":
        text_val = _resolve_str(data_ctx, props.get("text"), "")
        variant = str(props.get("variant") or "body")
        if variant in ("h1", "h2", "h3", "h4", "h5"):
            level = int(variant[1])
            return Markdown(f"{'#' * level} {text_val}", classes=f"a2ui-text a2ui-{variant}")
        if variant == "caption":
            return Static(text_val, markup=False, classes="a2ui-text a2ui-caption")
        return Markdown(text_val, classes="a2ui-text a2ui-body")

    if comp_type == "Divider":
        axis = str(props.get("axis") or "horizontal")
        orientation: Literal["horizontal", "vertical"] = "vertical" if axis == "vertical" else "horizontal"
        return Rule(orientation=orientation, classes="a2ui-divider")

    if comp_type == "Button":
        label = _resolve_button_label(surface, comp, data_ctx)
        raw_action = props.get("action")
        action_dict = dict(raw_action) if isinstance(raw_action, dict) else None
        variant = str(props.get("variant") or "default")
        return A2UIButton(
            label,
            component_id=comp.id,
            surface_id=surface.id,
            raw_action=action_dict,
            data_context=data_ctx,
            variant=variant,
        )

    if comp_type == "TextField":
        bound_path = _extract_bound_path(props.get("value"))
        value = _resolve_str(data_ctx, props.get("value"), "")
        placeholder = _resolve_str(data_ctx, props.get("placeholder"), "")
        label = _resolve_str(data_ctx, props.get("label"), "")
        field_widget = A2UITextField(
            surface=surface,
            data_context=data_ctx,
            bound_path=bound_path,
            value=value,
            placeholder=placeholder or label,
        )
        if label:
            return Vertical(
                Static(label, markup=False, classes="a2ui-field-label"),
                field_widget,
                classes="a2ui-field-group",
            )
        return field_widget

    if comp_type == "CheckBox":
        bound_path = _extract_bound_path(props.get("value"))
        label = _resolve_str(data_ctx, props.get("label"), comp.id)
        checked = bool(_resolve_value(data_ctx, props.get("value"), False))
        return A2UICheckBox(label, value=checked, data_context=data_ctx, bound_path=bound_path)

    if comp_type == "ChoicePicker":
        bound_path = _extract_bound_path(props.get("value"))
        label = _resolve_str(data_ctx, props.get("label"), "Select option")
        raw_options = props.get("options") or []
        options: list[tuple[str, str]] = []
        for opt in raw_options:
            if isinstance(opt, dict):
                opt_label = _resolve_str(data_ctx, opt.get("label"), str(opt.get("value") or ""))
                opt_value = str(opt.get("value") or opt_label)
                options.append((opt_label, opt_value))
        resolved_val = _resolve_value(data_ctx, props.get("value"), None)
        initial_val: str | None = None
        if isinstance(resolved_val, list) and resolved_val:
            initial_val = str(resolved_val[0])
        elif isinstance(resolved_val, str):
            initial_val = resolved_val
        return A2UIChoicePicker(
            options,
            prompt=label,
            initial_value=initial_val,
            data_context=data_ctx,
            bound_path=bound_path,
        )

    if comp_type in ("Column", "Row"):
        children_raw = props.get("children")
        child_widgets = _render_children_spec(surface, children_raw, data_ctx, next_visited)
        if comp_type == "Row":
            return Horizontal(*child_widgets, classes="a2ui-row")
        return Vertical(*child_widgets, classes="a2ui-column")

    if comp_type == "List":
        children_raw = props.get("children")
        child_widgets = _render_children_spec(surface, children_raw, data_ctx, next_visited)
        direction = str(props.get("direction") or "vertical")
        if direction == "horizontal":
            return Horizontal(*child_widgets, classes="a2ui-list a2ui-list-horizontal")
        return Vertical(*child_widgets, classes="a2ui-list")

    if comp_type == "Card":
        child_id = props.get("child")
        children: list[Widget] = []
        if isinstance(child_id, str):
            children.append(_render_component(surface, child_id, data_ctx, next_visited))
        return Vertical(*children, classes="a2ui-card")

    if comp_type == "Modal":
        trigger_id = props.get("trigger")
        content_id = props.get("content")
        modal_children: list[Widget] = []
        if isinstance(trigger_id, str):
            modal_children.append(_render_component(surface, trigger_id, data_ctx, next_visited))
        if isinstance(content_id, str):
            modal_children.append(_render_component(surface, content_id, data_ctx, next_visited))
        return Vertical(*modal_children, classes="a2ui-modal")

    if comp_type == "Tabs":
        tabs_raw = props.get("tabs") or []
        tabbed = TabbedContent(classes="a2ui-tabs")
        for idx, tab in enumerate(tabs_raw):
            if not isinstance(tab, dict):
                continue
            title = _resolve_str(data_ctx, tab.get("title"), f"Tab {idx + 1}")
            child_id = tab.get("child")
            pane_child: Widget = (
                _render_component(surface, child_id, data_ctx, next_visited)
                if isinstance(child_id, str)
                else Static("(empty tab)", markup=False)
            )
            tabbed.compose_add_child(TabPane(title, pane_child))
        return tabbed

    if comp_type in ("Image", "Icon", "Video", "AudioPlayer"):
        label = _resolve_str(data_ctx, props.get("url") or props.get("name"), comp_type)
        return Static(f"[{comp_type}: {label}]", markup=False, classes="a2ui-media")

    return Static(f"[{comp_type} {comp.id}]", markup=False, classes="a2ui-unknown")


def _render_children_spec(
    surface: SurfaceModel,
    children_spec: Any,
    data_ctx: DataContext,
    visited: frozenset[str],
) -> list[Widget]:
    widgets: list[Widget] = []
    if isinstance(children_spec, list):
        for cid in children_spec:
            if isinstance(cid, str):
                widgets.append(_render_component(surface, cid, data_ctx, visited))
        return widgets

    if isinstance(children_spec, dict):
        template_id = children_spec.get("componentId")
        template_path = children_spec.get("path")
        if isinstance(template_id, str) and isinstance(template_path, str):
            path_binding = {"@path": template_path} if data_ctx.at_least_v10 else {"path": template_path}
            resolved_list = _resolve_value(data_ctx, path_binding, [])
            if isinstance(resolved_list, list):
                abs_base = data_ctx.resolve_path(template_path).rstrip("/")
                for idx, _ in enumerate(resolved_list):
                    item_path = f"{abs_base}/{idx}" if abs_base else f"/{idx}"
                    item_ctx = DataContext(surface, path=item_path, index=idx, parent=data_ctx)
                    widgets.append(_render_component(surface, template_id, item_ctx, visited))
    return widgets


def _resolve_button_action(button: A2UIButton) -> tuple[str, dict[str, Any]]:
    action_name = button.component_id
    action_context: dict[str, Any] = {}
    if not button.raw_action:
        return action_name, action_context

    resolved = button.data_context.resolve_action(button.raw_action)
    if isinstance(resolved, dict):
        if isinstance(resolved.get("event"), dict):
            ev = resolved["event"]
            action_name = str(ev.get("name") or button.component_id)
            ctx_obj = ev.get("context")
            if isinstance(ctx_obj, dict):
                action_context = dict(ctx_obj)
            if ev.get("userMessage") is not None:
                action_context.setdefault("userMessage", ev["userMessage"])
        elif "name" in resolved:
            action_name = str(resolved.get("name") or button.component_id)
            ctx_obj = resolved.get("context")
            if isinstance(ctx_obj, dict):
                action_context = dict(ctx_obj)
    return action_name, action_context


class A2UISurfaceWidget(VerticalScroll):
    """Textual viewport rendering active A2UI v1.0 surfaces from a MessageProcessor."""

    DEFAULT_CSS = """
    A2UISurfaceWidget {
        height: 1fr;
        padding: 1 2;
    }
    .a2ui-surface-frame {
        height: auto;
        margin-bottom: 1;
    }
    .a2ui-column, .a2ui-list {
        height: auto;
    }
    .a2ui-row {
        height: auto;
        align-vertical: middle;
        margin-bottom: 1;
    }
    .a2ui-card {
        height: auto;
        border: round $accent;
        padding: 1 2;
        margin-bottom: 1;
        background: $surface;
    }
    .a2ui-modal {
        height: auto;
        border: heavy $warning;
        padding: 1 2;
        margin-bottom: 1;
    }
    .a2ui-button {
        margin-right: 1;
    }
    .a2ui-caption {
        color: $text-muted;
        margin-bottom: 1;
    }
    .a2ui-tabs {
        height: auto;
        min-height: 12;
    }
    """

    def __init__(self, processor: MessageProcessor | None = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._processor = processor

    @property
    def processor(self) -> MessageProcessor | None:
        """Return the active MessageProcessor."""
        return self._processor

    async def on_mount(self) -> None:
        if self._processor is not None:
            await self.refresh_surfaces()

    async def set_processor(self, processor: MessageProcessor) -> None:
        """Bind a new MessageProcessor and render its active surfaces."""
        self._processor = processor
        await self.refresh_surfaces()

    async def refresh_surfaces(self) -> None:
        """Rebuild the Textual widget tree from the MessageProcessor's SurfaceGroupModel."""
        await self.remove_children()
        if self._processor is None or not self._processor.model.surfaces_map:
            await self.mount(
                Static(
                    "No active A2UI surfaces yet. Ask a question below.",
                    markup=False,
                    classes="a2ui-caption",
                )
            )
            return

        frames: list[Widget] = []
        for surface_id, surface in self._processor.model.surfaces_map.items():
            root_id = surface.root_id or "root"
            root_ctx = DataContext(surface, path="/")
            if surface.components_model.get(root_id) is None:
                frames.append(Static(f"Surface '{surface_id}' waiting for '{root_id}' component...", markup=False))
                continue
            rendered_root = _render_component(surface, root_id, root_ctx)
            frames.append(Vertical(rendered_root, classes="a2ui-surface-frame"))

        if frames:
            await self.mount(*frames)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if isinstance(event.button, A2UIButton):
            event.stop()
            action_name, action_context = _resolve_button_action(event.button)
            self.post_message(
                A2UIActionDispatched(
                    surface_id=event.button.surface_id,
                    action_name=action_name,
                    context=action_context,
                )
            )

    def on_input_changed(self, event: Input.Changed) -> None:
        if isinstance(event.input, A2UITextField) and event.input.bound_path:
            event.input.data_context.set(event.input.bound_path, event.value)

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        if isinstance(event.checkbox, A2UICheckBox) and event.checkbox.bound_path:
            event.checkbox.data_context.set(event.checkbox.bound_path, event.value)

    def on_select_changed(self, event: Select.Changed) -> None:
        if isinstance(event.select, A2UIChoicePicker) and event.select.bound_path:
            selected: list[str] = [] if event.value is Select.NULL else [str(event.value)]
            event.select.data_context.set(event.select.bound_path, selected)


def build_initial_overview_messages(
    store: TrajectoryStore,
    *,
    projects: Sequence[ProjectSummary] | None = None,
    sessions: Sequence[SessionTrajectorySummary] | None = None,
) -> list[dict[str, Any]]:
    """Build strict A2UI v1.0 messages for the initial Brain Explorer dashboard."""
    resolved_projects = list(projects) if projects is not None else store.list_projects().projects
    resolved_sessions = list(sessions) if sessions is not None else store.list_sessions(limit=12).sessions

    skill_counts: dict[str, int] = {}
    tier_counts: dict[str, int] = {"way_1_plugin": 0, "way_2_community": 0, "way_3_bespoke": 0, "unknown": 0}
    for sess in resolved_sessions:
        for act in sess.skill_activations:
            skill_counts[act.skill_name] = skill_counts.get(act.skill_name, 0) + 1
            tier_counts[act.tier] = tier_counts.get(act.tier, 0) + 1

    session_items = [
        {
            "session_id": s.session_id,
            "headline": f"### {s.session_id[:8]} · {s.project} · {s.step_count} steps · {s.duration or '-'}",
            "prompt": (s.initial_prompt or "(no initial prompt)")[:120],
            "skills": (
                "Skills: " + ", ".join(f"{a.skill_name} [{a.tier}]" for a in s.skill_activations)
                if s.skill_activations
                else "Skills: none detected"
            ),
        }
        for s in resolved_sessions
    ]
    project_items = [
        {
            "name": f"### {p.name}",
            "meta": f"{p.session_count} sessions · latest {p.latest_active or '-'}",
            "path": p.workspace_path or "(no workspace)",
        }
        for p in resolved_projects[:15]
    ]
    skill_items = [
        {"label": f"{name} — seen {count} time(s) across recent sessions"}
        for name, count in sorted(skill_counts.items(), key=lambda kv: (-kv[1], kv[0]))
    ]

    components: list[dict[str, Any]] = [
        {"id": "root", "component": "Column", "children": ["title", "subtitle", "actions_row", "tabs"]},
        {"id": "title", "component": "Text", "text": {"@path": "/header"}, "variant": "body"},
        {"id": "subtitle", "component": "Text", "text": {"@path": "/stats"}, "variant": "caption"},
        {
            "id": "actions_row",
            "component": "Row",
            "children": ["refresh_btn", "compare_btn"] if len(resolved_sessions) >= 2 else ["refresh_btn"],
        },
        {
            "id": "refresh_btn",
            "component": "Button",
            "child": "refresh_lbl",
            "variant": "primary",
            "action": {"event": {"name": "refresh_overview", "context": {}}},
        },
        {"id": "refresh_lbl", "component": "Text", "text": "Refresh Local Index"},
    ]

    if len(resolved_sessions) >= 2:
        components.extend(
            [
                {
                    "id": "compare_btn",
                    "component": "Button",
                    "child": "compare_lbl",
                    "action": {
                        "event": {
                            "name": "compare_sessions",
                            "context": {
                                "session_a": resolved_sessions[0].session_id,
                                "session_b": resolved_sessions[1].session_id,
                            },
                        }
                    },
                },
                {"id": "compare_lbl", "component": "Text", "text": "Ask Agent: Compare Top 2"},
            ]
        )

    components.append(
        {
            "id": "tabs",
            "component": "Tabs",
            "tabs": [
                {"title": f"Session Trajectories ({len(session_items)})", "child": "sessions_tab"},
                {"title": f"Projects ({len(resolved_projects)})", "child": "projects_tab"},
                {"title": f"Skill Activations ({len(skill_items)})", "child": "skills_tab"},
            ],
        }
    )

    if session_items:
        components.extend(
            [
                {
                    "id": "sessions_tab",
                    "component": "List",
                    "children": {"componentId": "session_card", "path": "/sessions"},
                },
                {"id": "session_card", "component": "Card", "child": "session_card_col"},
                {
                    "id": "session_card_col",
                    "component": "Column",
                    "children": ["sess_head", "sess_prompt", "sess_skills", "sess_btn"],
                },
                {"id": "sess_head", "component": "Text", "text": {"@path": "headline"}, "variant": "body"},
                {"id": "sess_prompt", "component": "Text", "text": {"@path": "prompt"}, "variant": "body"},
                {"id": "sess_skills", "component": "Text", "text": {"@path": "skills"}, "variant": "caption"},
                {
                    "id": "sess_btn",
                    "component": "Button",
                    "child": "sess_btn_lbl",
                    "action": {
                        "event": {
                            "name": "inspect_session",
                            "context": {"session_id": {"@path": "session_id"}},
                        }
                    },
                },
                {"id": "sess_btn_lbl", "component": "Text", "text": "Inspect with Agent"},
            ]
        )
    else:
        components.append(
            {
                "id": "sessions_tab",
                "component": "Text",
                "text": "No Antigravity session trajectories found under the configured Gemini directory.",
            }
        )

    if project_items:
        components.extend(
            [
                {
                    "id": "projects_tab",
                    "component": "List",
                    "children": {"componentId": "project_card", "path": "/projects"},
                },
                {"id": "project_card", "component": "Card", "child": "project_card_col"},
                {"id": "project_card_col", "component": "Column", "children": ["proj_name", "proj_meta", "proj_path"]},
                {"id": "proj_name", "component": "Text", "text": {"@path": "name"}, "variant": "body"},
                {"id": "proj_meta", "component": "Text", "text": {"@path": "meta"}, "variant": "body"},
                {"id": "proj_path", "component": "Text", "text": {"@path": "path"}, "variant": "caption"},
            ]
        )
    else:
        components.append({"id": "projects_tab", "component": "Text", "text": "No projects discovered yet."})

    if skill_items:
        components.extend(
            [
                {
                    "id": "skills_tab",
                    "component": "List",
                    "children": {"componentId": "skill_card", "path": "/skills"},
                },
                {"id": "skill_card", "component": "Card", "child": "skill_label"},
                {"id": "skill_label", "component": "Text", "text": {"@path": "label"}, "variant": "body"},
            ]
        )
    else:
        components.append({"id": "skills_tab", "component": "Text", "text": "No skill activations detected yet."})

    stats_line = (
        f"Indexed {len(resolved_projects)} projects and {len(resolved_sessions)} recent Session Trajectories · "
        f"Way 1 Plugin: {tier_counts['way_1_plugin']} · "
        f"Way 2 Community: {tier_counts['way_2_community']} · "
        f"Way 3 Bespoke: {tier_counts['way_3_bespoke']}"
    )

    return [
        {
            "version": "1.0",
            "createSurface": {"surfaceId": "brain_overview", "catalogId": A2UI_BASIC_CATALOG_V1_0_ID},
        },
        {
            "version": "1.0",
            "updateDataModel": {
                "surfaceId": "brain_overview",
                "path": "/",
                "value": {
                    "header": "# Brain Explorer — A2UI v1.0 Generative Surface",
                    "stats": stats_line,
                    "sessions": session_items,
                    "projects": project_items,
                    "skills": skill_items,
                },
            },
        },
        {
            "version": "1.0",
            "updateComponents": {"surfaceId": "brain_overview", "components": components},
        },
    ]


def build_local_session_detail_messages(detail: SessionTrajectoryDetail) -> list[dict[str, Any]]:
    """Build strict A2UI v1.0 messages for offline local Session Trajectory drill-down."""
    summary = detail.summary
    surface_id = f"session_{summary.session_id[:8]}"

    skill_items = [
        {
            "label": f"{act.skill_name} · {act.activation_kind} · {act.tier} · step {act.step_index}",
            "evidence": act.evidence or "-",
        }
        for act in summary.skill_activations
    ]
    step_items = [
        {
            "heading": f"**Step {step.step_index}** · {step.source} / {step.step_type}",
            "preview": step.preview or "-",
            "tools": "Tools: " + (", ".join(step.tools_used) if step.tools_used else "none"),
        }
        for step in detail.steps
    ]
    tool_items = [{"label": f"`{tc.tool_name}`: {tc.count}"} for tc in detail.tool_counts]

    components: list[dict[str, Any]] = [
        {"id": "root", "component": "Column", "children": ["detail_title", "detail_meta", "detail_actions", "detail_tabs"]},
        {"id": "detail_title", "component": "Text", "text": {"@path": "/title"}, "variant": "body"},
        {"id": "detail_meta", "component": "Text", "text": {"@path": "/meta"}, "variant": "caption"},
        {"id": "detail_actions", "component": "Row", "children": ["audit_btn", "back_btn"]},
        {
            "id": "audit_btn",
            "component": "Button",
            "child": "audit_lbl",
            "variant": "primary",
            "action": {
                "event": {
                    "name": "audit_session",
                    "context": {"session_id": summary.session_id},
                }
            },
        },
        {"id": "audit_lbl", "component": "Text", "text": "Ask Agent to Audit Session"},
        {
            "id": "back_btn",
            "component": "Button",
            "child": "back_lbl",
            "action": {"event": {"name": "refresh_overview", "context": {}}},
        },
        {"id": "back_lbl", "component": "Text", "text": "Back to Overview"},
        {
            "id": "detail_tabs",
            "component": "Tabs",
            "tabs": [
                {"title": f"Skill Activations ({len(skill_items)})", "child": "detail_skills_tab"},
                {"title": f"Steps ({len(step_items)})", "child": "detail_steps_tab"},
                {"title": f"Tools ({len(tool_items)})", "child": "detail_tools_tab"},
            ],
        },
    ]

    if skill_items:
        components.extend(
            [
                {
                    "id": "detail_skills_tab",
                    "component": "List",
                    "children": {"componentId": "detail_skill_card", "path": "/skills"},
                },
                {"id": "detail_skill_card", "component": "Card", "child": "detail_skill_col"},
                {
                    "id": "detail_skill_col",
                    "component": "Column",
                    "children": ["detail_skill_lbl", "detail_skill_ev"],
                },
                {"id": "detail_skill_lbl", "component": "Text", "text": {"@path": "label"}, "variant": "body"},
                {"id": "detail_skill_ev", "component": "Text", "text": {"@path": "evidence"}, "variant": "caption"},
            ]
        )
    else:
        components.append(
            {
                "id": "detail_skills_tab",
                "component": "Text",
                "text": "No Skill Activations detected in this Session Trajectory.",
            }
        )

    if step_items:
        components.extend(
            [
                {
                    "id": "detail_steps_tab",
                    "component": "List",
                    "children": {"componentId": "detail_step_card", "path": "/steps"},
                },
                {"id": "detail_step_card", "component": "Card", "child": "detail_step_col"},
                {
                    "id": "detail_step_col",
                    "component": "Column",
                    "children": ["detail_step_hdr", "detail_step_prev", "detail_step_tools"],
                },
                {"id": "detail_step_hdr", "component": "Text", "text": {"@path": "heading"}, "variant": "body"},
                {"id": "detail_step_prev", "component": "Text", "text": {"@path": "preview"}, "variant": "body"},
                {"id": "detail_step_tools", "component": "Text", "text": {"@path": "tools"}, "variant": "caption"},
            ]
        )
    else:
        components.append({"id": "detail_steps_tab", "component": "Text", "text": "No steps recorded."})

    if tool_items:
        components.extend(
            [
                {
                    "id": "detail_tools_tab",
                    "component": "List",
                    "children": {"componentId": "detail_tool_card", "path": "/tools"},
                },
                {"id": "detail_tool_card", "component": "Card", "child": "detail_tool_lbl"},
                {"id": "detail_tool_lbl", "component": "Text", "text": {"@path": "label"}, "variant": "body"},
            ]
        )
    else:
        components.append({"id": "detail_tools_tab", "component": "Text", "text": "No tool calls recorded."})

    models_text = ", ".join(detail.models_used) if detail.models_used else "unknown"
    meta_line = (
        f"Session {summary.session_id} · Created: {summary.created_at or '-'} · "
        f"Duration: {summary.duration or '-'} · Models: {models_text} · "
        f"Workspace: {detail.workspace_path or '-'}"
    )

    return [
        {
            "version": "1.0",
            "createSurface": {"surfaceId": surface_id, "catalogId": A2UI_BASIC_CATALOG_V1_0_ID},
        },
        {
            "version": "1.0",
            "updateDataModel": {
                "surfaceId": surface_id,
                "path": "/",
                "value": {
                    "title": f"# Session `{summary.session_id[:8]}` · {summary.project}",
                    "meta": meta_line,
                    "skills": skill_items,
                    "steps": step_items,
                    "tools": tool_items,
                },
            },
        },
        {
            "version": "1.0",
            "updateComponents": {"surfaceId": surface_id, "components": components},
        },
    ]


def create_strict_processor(messages: Sequence[dict[str, Any]]) -> MessageProcessor:
    """Create a strictly validated A2UI v1.0 MessageProcessor and apply ``messages``."""
    catalog = BasicCatalog(ProtocolVersion.V1_0)
    processor = MessageProcessor(
        [catalog],
        options=MessageProcessorOptions(validation_config=STRICT_VALIDATION),
    )
    processor.process_messages(list(messages))
    return processor


def create_overview_processor(
    store: TrajectoryStore,
    *,
    projects: Sequence[ProjectSummary] | None = None,
    sessions: Sequence[SessionTrajectorySummary] | None = None,
) -> MessageProcessor:
    """Create a strictly validated MessageProcessor populated with the Brain Explorer overview."""
    return create_strict_processor(
        build_initial_overview_messages(store, projects=projects, sessions=sessions)
    )


def extract_surface_snapshot(processor: MessageProcessor) -> list[dict[str, Any]]:
    """Extract a JSON-serializable snapshot of all active surfaces for debugging/inspector views."""
    snapshots: list[dict[str, Any]] = []
    for surface_id, surface in processor.model.surfaces_map.items():
        snapshots.append(
            {
                "surfaceId": surface_id,
                "rootId": surface.root_id,
                "dataModel": surface.data_model.get("/"),
                "components": [
                    {"id": cid, "component": comp.type, **comp.properties}
                    for cid, comp in surface.components_model.entries
                ],
            }
        )
    return snapshots
