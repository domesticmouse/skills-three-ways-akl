# Skills Three Ways (DevFest Auckland 2026)

Domain vocabulary for the **Skills Three Ways** 90-minute self-paced codelab, its matching presentation deck, and its companion **Brain Explorer** application.

## Language

**Skills Three Ways**:
The three-tier classification of AI agent skills used as the spine of the codelab and deck: Ecosystem & Plugin Skills (Way 1), Community Workflow Skills (Way 2), and Bespoke In-Project Skills (Way 3).
_Avoid_: Skill categories, skill levels

**Brain Explorer**:
The companion Python CLI and Textualize (`Textual`) TUI application built during the codelab to discover, inspect, and compare Antigravity session trajectories, rendering A2UI v1.0 generative surfaces composed by the SDK agent alongside fast local trajectory views.
_Avoid_: Demo app, trajectory viewer, admin dashboard

**Session Trajectory**:
A single recorded Antigravity conversation stored under `~/.gemini/**/brain/<session-id>/` (`transcript.jsonl` and `transcript_full.jsonl`), comprising user prompts, model thinking steps, tool calls, and skill activations.
_Avoid_: Chat log, conversation history, trace file

**Skill Activation**:
An invocation of an agent skill within a Session Trajectory, evidenced either by an explicit `<SKILL>` slash-command payload in user input or by the agent reading a `SKILL.md` file during execution.
_Avoid_: Skill call, plugin trigger, tool invocation

**Exploratory Run**:
The unscripted first-pass build of **Brain Explorer** used to test the stack, surface the bespoke skill needed for Way 3, and establish the reference patterns and traps documented across the codelab.
_Avoid_: Dry run, spike, draft build

**Codelab Checkpoint**:
One of the four versioned git branch snapshots (`codelab/start`, `codelab/checkpoint-2-skills`, `codelab/checkpoint-3-brain-explorer`, `codelab/checkpoint-4-bespoke-skill`) providing a clean entry point and recovery rails for learners working through the 90-minute self-paced codelab.
_Avoid_: Live demo branch, backup commit, recording branch
