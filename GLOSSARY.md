# Skills Three Ways (DevFest Auckland 2026)

Domain vocabulary for the **Skills Three Ways** presentation and its companion **Brain Explorer** application.

## Language

**Skills Three Ways**:
The three-tier classification of AI agent skills used as the spine of the talk: Ecosystem & Plugin Skills (Way 1), Community Workflow Skills (Way 2), and Bespoke In-Project Skills (Way 3).
_Avoid_: Skill categories, skill levels

**Brain Explorer**:
The companion Python CLI and Textualize (`Textual`) TUI application built during the talk to discover, inspect, and compare Antigravity session trajectories.
_Avoid_: Demo app, trajectory viewer, admin dashboard

**Session Trajectory**:
A single recorded Antigravity conversation stored under `~/.gemini/**/brain/<session-id>/` (`transcript.jsonl` and `transcript_full.jsonl`), comprising user prompts, model thinking steps, tool calls, and skill activations.
_Avoid_: Chat log, conversation history, trace file

**Skill Activation**:
An invocation of an agent skill within a Session Trajectory, evidenced either by an explicit `<SKILL>` slash-command payload in user input or by the agent reading a `SKILL.md` file during execution.
_Avoid_: Skill call, plugin trigger, tool invocation

**Exploratory Run**:
The unscripted first-pass build of **Brain Explorer** used to test the stack, surface the bespoke skill needed for Way 3, and harvest real `~/.gemini` Session Trajectories before scripting the talk's prompts.
_Avoid_: Dry run, spike, draft build

**Recording Run**:
The scripted second-pass execution of the prompts discovered during the Exploratory Run, captured under `asciinema` into `.cast` files for deterministic playback across the entire Slidev deck.
_Avoid_: Live demo, screen recording, final take
