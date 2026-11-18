"""Typer CLI entrypoint for Brain Explorer."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Annotated

import typer
from a2ui.core.basic_catalog import BasicCatalog
from a2ui.core.processing import MessageProcessor
from a2ui.core.processing.message_processor import MessageProcessorOptions
from a2ui.core.schema import ProtocolVersion
from a2ui.core.validation import STRICT_VALIDATION
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from brain_explorer.agent_service import BrainExplorerAgentService
from brain_explorer.models import (
    ProjectListResult,
    SessionComparisonResult,
    SessionListResult,
    SessionTrajectoryDetail,
    TrajectoryStepDetail,
)
from brain_explorer.trajectory_store import TrajectoryStore
from brain_explorer.tui import BrainExplorerApp

app = typer.Typer(
    name="brain-explorer",
    help="Explore Antigravity Session Trajectories and Skill Activations via local index, A2UI v1.0, and Textual.",
)
console = Console()

GeminiDirOption = Annotated[
    Path | None,
    typer.Option("--gemini-dir", help="Root Gemini directory (defaults to ~/.gemini)."),
]


def _render_projects(result: ProjectListResult) -> None:
    if not result.projects:
        console.print("[yellow]No projects discovered under the configured Gemini directory.[/yellow]")
        return

    table = Table(title="Antigravity Brain Projects")
    table.add_column("Project", style="bold cyan")
    table.add_column("Sessions", justify="right")
    table.add_column("Latest Active")
    table.add_column("Workspace Path", style="dim")

    for project in result.projects:
        table.add_row(
            Text(project.name),
            Text(str(project.session_count)),
            Text(project.latest_active or "-"),
            Text(project.workspace_path or "-"),
        )
    console.print(table)


def _render_sessions(result: SessionListResult) -> None:
    if not result.sessions:
        console.print("[yellow]No Session Trajectories matched the requested filters.[/yellow]")
        return

    table = Table(title="Antigravity Session Trajectories")
    table.add_column("Session ID", style="bold cyan")
    table.add_column("Project")
    table.add_column("Created")
    table.add_column("Duration", justify="right")
    table.add_column("Steps", justify="right")
    table.add_column("Skill Activations")
    table.add_column("Prompt", overflow="fold")

    for session in result.sessions:
        skills = ", ".join(f"{item.skill_name} ({item.tier})" for item in session.skill_activations) or "-"
        table.add_row(
            Text(session.session_id[:8]),
            Text(session.project),
            Text(session.created_at or "-"),
            Text(session.duration or "-"),
            Text(str(session.step_count)),
            Text(skills),
            Text((session.initial_prompt or "-")[:80]),
        )
    console.print(table)


def _render_session_detail(detail: SessionTrajectoryDetail) -> None:
    summary = detail.summary
    skills = (
        ", ".join(
            f"{item.skill_name} ({item.activation_kind}, {item.tier}, step {item.step_index})"
            for item in summary.skill_activations
        )
        or "None detected"
    )
    models = ", ".join(detail.models_used) or "-"
    tools_summary = ", ".join(f"{tc.tool_name}: {tc.count}" for tc in detail.tool_counts) or "-"

    header = (
        f"[bold]Session:[/bold] {escape(summary.session_id)}\n"
        f"[bold]Project:[/bold] {escape(summary.project)} ({escape(detail.workspace_path or 'unknown workspace')})\n"
        f"[bold]Created:[/bold] {escape(summary.created_at or '-')} | "
        f"[bold]Duration:[/bold] {escape(summary.duration or '-')}\n"
        f"[bold]Models:[/bold] {escape(models)}\n"
        f"[bold]Skill Activations:[/bold] {escape(skills)}\n"
        f"[bold]Tool Counts:[/bold] {escape(tools_summary)}\n"
        f"[bold]Transcript:[/bold] {escape(detail.transcript_path or '-')}"
    )
    console.print(Panel(header, title="Session Trajectory Detail", border_style="cyan"))

    steps_table = Table(title=f"Steps ({len(detail.steps)} shown)")
    steps_table.add_column("#", justify="right", style="cyan")
    steps_table.add_column("Source")
    steps_table.add_column("Type")
    steps_table.add_column("Tools")
    steps_table.add_column("Preview", overflow="fold")

    for step in detail.steps:
        steps_table.add_row(
            Text(str(step.step_index)),
            Text(step.source),
            Text(step.step_type),
            Text(", ".join(step.tools_used) or "-"),
            Text(step.preview),
        )
    console.print(steps_table)


def _render_step_detail(step: TrajectoryStepDetail) -> None:
    header = (
        f"[bold]Step:[/bold] {step.step_index}\n"
        f"[bold]Source:[/bold] {escape(step.source)} | [bold]Type:[/bold] {escape(step.step_type)}\n"
        f"[bold]Status:[/bold] {escape(step.status or '-')} | [bold]Created:[/bold] {escape(step.created_at or '-')}"
    )
    console.print(Panel(header, title="Trajectory Step Detail", border_style="cyan"))
    if step.thinking:
        console.print(Panel(Text(step.thinking), title="Thinking", border_style="magenta"))
    if step.content:
        console.print(Panel(Text(step.content), title="Content", border_style="blue"))
    if step.tool_calls:
        console.print(Panel(Text(json.dumps(step.tool_calls, indent=2)), title="Tool Calls", border_style="yellow"))
    if step.step_output:
        console.print(Panel(Text(step.step_output), title="Step Output", border_style="green"))


def _render_comparison(result: SessionComparisonResult) -> None:
    table = Table(title="Session Trajectory Comparison")
    table.add_column("Metric", style="bold")
    table.add_column(f"A: {escape(result.session_a.session_id[:8])}", style="cyan")
    table.add_column(f"B: {escape(result.session_b.session_id[:8])}", style="magenta")

    table.add_row(Text("Project"), Text(result.session_a.project), Text(result.session_b.project))
    table.add_row(Text("Created"), Text(result.session_a.created_at or "-"), Text(result.session_b.created_at or "-"))
    table.add_row(Text("Duration"), Text(result.session_a.duration or "-"), Text(result.session_b.duration or "-"))
    table.add_row(Text("Steps"), Text(str(result.session_a.step_count)), Text(str(result.session_b.step_count)))
    table.add_row(
        Text("Skill Activations"),
        Text(", ".join(s.skill_name for s in result.session_a.skill_activations) or "-"),
        Text(", ".join(s.skill_name for s in result.session_b.skill_activations) or "-"),
    )
    console.print(table)

    differences = "\n".join(f"- {escape(diff)}" for diff in result.key_differences) or "- None listed"
    console.print(
        Panel(
            f"{escape(result.summary_comparison)}\n\n[bold]Key Differences:[/bold]\n{differences}",
            title="Comparison Summary",
            border_style="green",
        )
    )


def _run_tui(
    *,
    gemini_dir: Path | None = None,
    sidebar: bool = True,
    inspector: bool = False,
) -> None:
    store = TrajectoryStore(gemini_dir=gemini_dir)
    service = BrainExplorerAgentService(store=store)
    tui_app = BrainExplorerApp(
        store=store,
        agent_service=service,
        show_sidebar=sidebar,
        show_inspector=inspector,
    )
    tui_app.run()


@app.callback(invoke_without_command=True)
def default_entrypoint(ctx: typer.Context) -> None:
    """Launch the Brain Explorer Textual TUI when invoked without a subcommand."""
    if ctx.invoked_subcommand is None:
        _run_tui()


@app.command()
def tui(
    gemini_dir: GeminiDirOption = None,
    sidebar: Annotated[bool, typer.Option("--sidebar/--no-sidebar", help="Show local trajectory sidebar.")] = True,
    inspector: Annotated[bool, typer.Option("--inspector/--no-inspector", help="Show A2UI protocol inspector.")] = False,
) -> None:
    """Launch the interactive Brain Explorer Textual TUI."""
    _run_tui(gemini_dir=gemini_dir, sidebar=sidebar, inspector=inspector)


@app.command()
def projects(
    gemini_dir: GeminiDirOption = None,
    agent: Annotated[bool, typer.Option("--agent", help="Also ask the Antigravity SDK Agent for a synthesis.")] = False,
) -> None:
    """List projects discovered in ~/.gemini brain directories."""
    store = TrajectoryStore(gemini_dir=gemini_dir)
    result = store.list_projects()
    _render_projects(result)
    if agent:
        narrative = asyncio.run(
            BrainExplorerAgentService(store=store).ask_narrative(
                "List our Antigravity projects and briefly summarise where recent activity is concentrated."
            )
        )
        console.print(Panel(Text(narrative), title="Agent Synthesis", border_style="green"))


@app.command()
def sessions(
    project: Annotated[str | None, typer.Option("--project", "-p", help="Filter by project name or path.")] = None,
    skill: Annotated[str | None, typer.Option("--skill", "-s", help="Filter by activated skill name.")] = None,
    brain: Annotated[str | None, typer.Option("--brain", "-b", help="Filter by brain root (e.g. antigravity).")] = None,
    limit: Annotated[int, typer.Option("--limit", "-n", min=1, help="Maximum sessions to return.")] = 10,
    gemini_dir: GeminiDirOption = None,
    agent: Annotated[bool, typer.Option("--agent", help="Also ask the Antigravity SDK Agent for a synthesis.")] = False,
) -> None:
    """List recent Antigravity Session Trajectories."""
    store = TrajectoryStore(gemini_dir=gemini_dir)
    result = store.list_sessions(project=project, limit=limit, skill_filter=skill, brain_root=brain)
    _render_sessions(result)
    if agent:
        narrative = asyncio.run(
            BrainExplorerAgentService(store=store).ask_narrative(
                f"Summarise recent sessions (project={project!r}, skill={skill!r}, limit={limit}) and their Skill Activations."
            )
        )
        console.print(Panel(Text(narrative), title="Agent Synthesis", border_style="green"))


@app.command()
def search(
    query_text: Annotated[str, typer.Argument(help="Keyword to search across prompts, steps, thinking, and tools.")],
    project: Annotated[str | None, typer.Option("--project", "-p", help="Filter by project name or path.")] = None,
    limit: Annotated[int, typer.Option("--limit", "-n", min=1, help="Maximum matching sessions to return.")] = 10,
    gemini_dir: GeminiDirOption = None,
) -> None:
    """Search across Session Trajectories for prompts, step content, thinking, tools, or skills."""
    store = TrajectoryStore(gemini_dir=gemini_dir)
    try:
        result = store.search_sessions(query=query_text, project=project, limit=limit)
    except ValueError as exc:
        console.print(f"[red]{escape(str(exc))}[/red]")
        raise typer.Exit(code=1) from exc
    _render_sessions(result)


@app.command()
def inspect(
    session_id: Annotated[str, typer.Argument(help="Session UUID or unambiguous prefix.")],
    limit: Annotated[int | None, typer.Option("--limit", "-n", min=1, help="Maximum steps to display.")] = 40,
    gemini_dir: GeminiDirOption = None,
    agent: Annotated[bool, typer.Option("--agent", help="Also ask the Antigravity SDK Agent for an audit.")] = False,
) -> None:
    """Inspect a single Antigravity Session Trajectory and its Skill Activations."""
    store = TrajectoryStore(gemini_dir=gemini_dir)
    try:
        detail = store.inspect_session(session_id, step_limit=limit)
    except (FileNotFoundError, ValueError) as exc:
        console.print(f"[red]{escape(str(exc))}[/red]")
        raise typer.Exit(code=1) from exc

    _render_session_detail(detail)
    if agent:
        narrative = asyncio.run(
            BrainExplorerAgentService(store=store).ask_narrative(
                f"Inspect session '{detail.summary.session_id}' and explain its workflow, tool usage, and Skill Activations."
            )
        )
        console.print(Panel(Text(narrative), title="Agent Audit", border_style="green"))


@app.command()
def step(
    session_id: Annotated[str, typer.Argument(help="Session UUID or unambiguous prefix.")],
    step_index: Annotated[int, typer.Argument(help="Step index to inspect.")],
    gemini_dir: GeminiDirOption = None,
) -> None:
    """Inspect a specific step's full content, thinking, tool calls, and output."""
    store = TrajectoryStore(gemini_dir=gemini_dir)
    try:
        detail = store.inspect_step(session_id, step_index)
    except (FileNotFoundError, ValueError) as exc:
        console.print(f"[red]{escape(str(exc))}[/red]")
        raise typer.Exit(code=1) from exc
    _render_step_detail(detail)


@app.command()
def compare(
    session_a: Annotated[str, typer.Argument(help="First session UUID or prefix.")],
    session_b: Annotated[str, typer.Argument(help="Second session UUID or prefix.")],
    gemini_dir: GeminiDirOption = None,
    agent: Annotated[bool, typer.Option("--agent", help="Also ask the Antigravity SDK Agent for a narrative comparison.")] = False,
) -> None:
    """Compare two Antigravity Session Trajectories side-by-side."""
    store = TrajectoryStore(gemini_dir=gemini_dir)
    try:
        comparison = store.compare_sessions(session_a, session_b)
    except (FileNotFoundError, ValueError) as exc:
        console.print(f"[red]{escape(str(exc))}[/red]")
        raise typer.Exit(code=1) from exc

    _render_comparison(comparison)
    if agent:
        narrative = asyncio.run(
            BrainExplorerAgentService(store=store).ask_narrative(
                f"Compare sessions '{comparison.session_a.session_id}' and '{comparison.session_b.session_id}', focusing on Skill Activations and outcomes."
            )
        )
        console.print(Panel(Text(narrative), title="Agent Comparison", border_style="green"))


@app.command()
def query(
    prompt: Annotated[str, typer.Argument(help="Open-ended question for the Antigravity SDK Agent to render via A2UI v1.0.")],
    gemini_dir: GeminiDirOption = None,
) -> None:
    """Ask an open-ended question and print the validated A2UI v1.0 surface generated by the SDK Agent."""
    store = TrajectoryStore(gemini_dir=gemini_dir)
    service = BrainExplorerAgentService(store=store)
    processor = MessageProcessor(
        [BasicCatalog(ProtocolVersion.V1_0)],
        options=MessageProcessorOptions(validation_config=STRICT_VALIDATION),
    )
    try:
        reply_text = asyncio.run(service.generate_a2ui(prompt, processor))
    except Exception as exc:
        console.print(f"[red]Failed to generate A2UI response: {escape(str(exc))}[/red]")
        raise typer.Exit(code=1) from exc

    console.print(Panel(Text(reply_text), title="Agent Response", border_style="cyan"))
    console.print(
        Panel(
            Text(json.dumps(service.last_messages, indent=2, default=str)),
            title=f"Validated A2UI v1.0 Messages ({len(service.last_messages)} message(s))",
            border_style="green",
        )
    )


if __name__ == "__main__":
    app()
