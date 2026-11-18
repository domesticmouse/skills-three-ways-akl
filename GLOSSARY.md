# Skills Three Ways (DevFest Auckland 2026)

Domain vocabulary for the **Skills Three Ways** presentation and its companion **Brain Explorer** application.

## Language

**Skills Three Ways**:
The three-tier classification of AI agent skills used as the spine of the talk: Ecosystem & Plugin Skills (Way 1), Community Workflow Skills (Way 2), and Bespoke In-Project Skills (Way 3).
_Avoid_: Skill categories, skill levels

**Brain Explorer**:
The companion application built during the talk to discover, inspect, and compare Antigravity session trajectories.
_Avoid_: Demo app, trajectory viewer, admin dashboard

**Session Trajectory**:
A single recorded Antigravity conversation stored under `~/.gemini/**/brain/<session-id>/` (`transcript.jsonl` and `transcript_full.jsonl`), comprising user prompts, model thinking steps, tool calls, and skill activations.
_Avoid_: Chat log, conversation history, trace file

**Wayfinder Map**:
The canonical GitHub issue labelled `wayfinder:map` that indexes resolved decisions, child decision tickets on the frontier, and the fog of war (`Not yet specified`) on the route to the destination.
_Avoid_: Epic, project board, backlog

**Skill Activation**:
An invocation of an agent skill within a Session Trajectory, evidenced either by an explicit `<SKILL>` slash-command payload in user input or by the agent reading a `SKILL.md` file during execution.
_Avoid_: Skill call, plugin trigger, tool invocation
