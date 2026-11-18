"""Typer CLI entrypoint for Brain Explorer."""

from __future__ import annotations

import asyncio
import json
from typing import Annotated

import typer
from a2ui.core.basic_catalog import BasicCatalog
from a2ui.core.processing import MessageProcessor
from a2ui.core.schema import ProtocolVersion
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from brain_explorer.agent_service import BrainExplorerAgentService
from brain_explorer.models import (
    ProjectListResult,
    SessionComparisonResult,
    SessionListResult,
    SessionTrajectoryDetail,
)
from brain_explorer.trajectory_store import TrajectoryStore
from brain_explorer.tui import BrainExplorerApp, VariantKey

app = typer.Typer(
    name="brain-explorer",
    help="Explore Antigravity Session Trajectories and Skill Activations via local index, A2UI v1.0, and Textual.",
)
console = Console()


def _render_projects(result: ProjectListResult) -> None:
    if not result.projects:
        console.print("[yellow]No projects discovered under ~/.gemini.[/yellow]")
        return

    table = Table(title="Antigravity Brain Projects")
    table.add_column("Project", style="bold cyan")
    table.add_column("Sessions", justify="right")
    table.add_column("Latest Active")
    table.add_column("Workspace Path", style="dim")

    for project in result.projects:
        table.add_row(
            project.name,
            str(project.session_count),
            project.latest_active or "-",
            project.workspace_path or "-",
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
            session.session_id[:8],
            session.project,
            session.created_at or "-",
            session.duration or "-",
            str(session.step_count),
            skills,
            (session.initial_prompt or "-")[:80],
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
        f"[bold]Session:[/bold] {summary.session_id}\n"
        f"[bold]Project:[/bold] {summary.project} ({detail.workspace_path or 'unknown workspace'})\n"
        f"[bold]Created:[/bold] {summary.created_at or '-'} | [bold]Duration:[/bold] {summary.duration or '-'}\n"
        f"[bold]Models:[/bold] {models}\n"
        f"[bold]Skill Activations:[/bold] {skills}\n"
        f"[bold]Tool Counts:[/bold] {tools_summary}\n"
        f"[bold]Transcript:[/bold] {detail.transcript_path or '-'}"
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
            str(step.step_index),
            step.source,
            step.step_type,
            ", ".join(step.tools_used) or "-",
            step.preview,
        )
    console.print(steps_table)


def _render_comparison(result: SessionComparisonResult) -> None:
    table = Table(title="Session Trajectory Comparison")
    table.add_column("Metric", style="bold")
    table.add_column(f"A: {result.session_a.session_id[:8]}", style="cyan")
    table.add_column(f"B: {result.session_b.session_id[:8]}", style="magenta")

    table.add_row("Project", result.session_a.project, result.session_b.project)
    table.add_row("Created", result.session_a.created_at or "-", result.session_b.created_at or "-")
    table.add_row("Duration", result.session_a.duration or "-", result.session_b.duration or "-")
    table.add_row("Steps", str(result.session_a.step_count), str(result.session_b.step_count))
    table.add_row(
        "Skill Activations",
        ", ".join(s.skill_name for s in result.session_a.skill_activations) or "-",
        ", ".join(s.skill_name for s in result.session_b.skill_activations) or "-",
    )
    console.print(table)

    differences = "\n".join(f"- {diff}" for diff in result.key_differences) or "- None listed"
    console.print(
        Panel(
            f"{result.summary_comparison}\n\n[bold]Key Differences:[/bold]\n{differences}",
            title="Comparison Summary",
            border_style="green",
        )
    )


def _run_tui(variant: VariantKey = "A") -> None:
    store = TrajectoryStore()
    service = BrainExplorerAgentService(store=store)
    tui_app = BrainExplorerApp(store=store, agent_service=service, initial_variant=variant)
    tui_app.run()


@app.callback(invoke_without_command=True)
def default_entrypoint(ctx: typer.Context) -> None:
    """Launch the Brain Explorer Textual TUI when invoked without a subcommand."""
    if ctx.invoked_subcommand is None:
        _run_tui()


@app.command()
def tui(
    variant: Annotated[VariantKey, typer.Option("--variant", "-v", help="Initial prototype layout variant (A, B, or C).")] = "A",
) -> None:
    """Launch the interactive Brain Explorer Textual TUI."""
    _run_tui(variant=variant)


@app.command()
def projects(
    agent: Annotated[bool, typer.Option("--agent", help="Also ask the Antigravity SDK Agent for a synthesis.")] = False,
) -> None:
    """List projects discovered in ~/.gemini brain directories."""
    store = TrajectoryStore()
    result = store.list_projects()
    _render_projects(result)
    if agent:
        narrative = asyncio.run(
            BrainExplorerAgentService(store=store).ask_narrative(
                "List our Antigravity projects and briefly summarise where recent activity is concentrated."
            )
        )
        console.print(Panel(narrative, title="Agent Synthesis", border_style="green"))


@app.command()
def sessions(
    project: Annotated[str | None, typer.Option("--project", "-p", help="Filter by project name or path.")] = None,
    skill: Annotated[str | None, typer.Option("--skill", "-s", help="Filter by activated skill name.")] = None,
    brain: Annotated[str | None, typer.Option("--brain", "-b", help="Filter by brain root (e.g. antigravity).")] = None,
    limit: Annotated[int, typer.Option("--limit", "-n", min=1, help="Maximum sessions to return.")] = 10,
    agent: Annotated[bool, typer.Option("--agent", help="Also ask the Antigravity SDK Agent for a synthesis.")] = False,
) -> None:
    """List recent Antigravity Session Trajectories."""
    store = TrajectoryStore()
    result = store.list_sessions(project=project, limit=limit, skill_filter=skill, brain_root=brain)
    _render_sessions(result)
    if agent:
        narrative = asyncio.run(
            BrainExplorerAgentService(store=store).ask_narrative(
                f"Summarise recent sessions (project={project!r}, skill={skill!r}, limit={limit}) and their Skill Activations."
            )
        )
        console.print(Panel(narrative, title="Agent Synthesis", border_style="green"))


@app.command()
def inspect(
    session_id: Annotated[str, typer.Argument(help="Session UUID or unambiguous prefix.")],
    limit: Annotated[int | None, typer.Option("--limit", "-n", min=1, help="Maximum steps to display.")] = 40,
    agent: Annotated[bool, typer.Option("--agent", help="Also ask the Antigravity SDK Agent for an audit.")] = False,
) -> None:
    """Inspect a single Antigravity Session Trajectory and its Skill Activations."""
    store = TrajectoryStore()
    try:
        detail = store.inspect_session(session_id, step_limit=limit)
    except (FileNotFoundError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc

    _render_session_detail(detail)
    if agent:
        narrative = asyncio.run(
            BrainExplorerAgentService(store=store).ask_narrative(
                f"Inspect session '{detail.summary.session_id}' and explain its workflow, tool usage, and Skill Activations."
            )
        )
        console.print(Panel(narrative, title="Agent Audit", border_style="green"))


@app.command()
def compare(
    session_a: Annotated[str, typer.Argument(help="First session UUID or prefix.")],
    session_b: Annotated[str, typer.Argument(help="Second session UUID or prefix.")],
    agent: Annotated[bool, typer.Option("--agent", help="Also ask the Antigravity SDK Agent for a narrative comparison.")] = False,
) -> None:
    """Compare two Antigravity Session Trajectories side-by-side."""
    store = TrajectoryStore()
    try:
        comparison = store.compare_sessions(session_a, session_b)
    except (FileNotFoundError, ValueError) as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc

    _render_comparison(comparison)
    if agent:
        narrative = asyncio.run(
            BrainExplorerAgentService(store=store).ask_narrative(
                f"Compare sessions '{comparison.session_a.session_id}' and '{comparison.session_b.session_id}', focusing on Skill Activations and outcomes."
            )
        )
        console.print(Panel(narrative, title="Agent Comparison", border_style="green"))


@app.command()
def query(
    prompt: Annotated[str, typer.Argument(help="Open-ended question for the Antigravity SDK Agent to render via A2UI v1.0.")],
) -> None:
    """Ask an open-ended question and print the validated A2UI v1.0 surface generated by the SDK Agent."""
    store = TrajectoryStore()
    service = BrainExplorerAgentService(store=store)
    processor = MessageProcessor([BasicCatalog(ProtocolVersion.V1_0)])
    try:
        reply_text = asyncio.run(service.generate_a2ui(prompt, processor))
    except Exception as exc:
        console.print(f"[red]Failed to generate A2UI response: {exc}[/red]")
        raise typer.Exit(code=1) from exc

    console.print(Panel(reply_text, title="Agent Response", border_style="cyan"))
    console.print(
        Panel(
            json.dumps(service.last_messages, indent=2, default=str),
            title=f"Validated A2UI v1.0 Messages ({len(service.last_messages)} message(s))",
            border_style="green",
        )
    )


if __name__ == "__main__":
    app()
