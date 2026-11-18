---
layout: center
class: text-center
---

<!-- S4-01 -->
<div class="space-y-4">
  <h1 class="text-4xl font-extrabold text-white">
    Way 3 &middot; Bespoke In-Project Skills
  </h1>
  <p class="text-xl font-mono text-cyan-300">
    agy-customizations &middot; a2ui-textual &middot; brain-explorer
  </p>
  <p class="text-base text-gray-400 max-w-xl mx-auto">
    Turning exploratory friction into a bespoke workspace skill and inspecting the real Session Trajectories that built it
  </p>
</div>

<!--
Welcome to Act 4 and Way 3: Bespoke In-Project Skills. We saw in Act 3 that community skills gave us a rock-solid Python foundation, while our EGM reviewers helped us uncover and solve ten thorny integration traps at the seam of A2UI v1.0, Textual 8+, and the in-process Antigravity SDK. Now we close the loop on two levels: first, by turning that hard-won exploratory knowledge into a bespoke skill without writing it by hand; and second, by launching Brain Explorer to inspect the actual `~/.gemini` Session Trajectories and Skill Activations that built this project.
-->

---
layout: default
---

<!-- S4-02 -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Bespoke Skills Already Powering This Repo</h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white"><code>agy-brain-explorer</code> (Mounted via <code>LocalAgentConfig.skills_paths</code>)</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Teaches both our coding agent and the in-process <strong>Brain Explorer</strong> SDK agent how <code>~/.gemini/**/brain/</code> trajectories, <code>transcript.jsonl</code>, and Skill Activations are structured on disk</li>
    </ul>
  </li>
  <li>
    <strong class="text-white"><code>slidev-deck</code> &amp; <code>bjm-voice</code> (Presentation &amp; Editorial Hygiene)</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Encodes this Slidev deck's modular act architecture, <code>AsciinemaPlayer.vue</code> chapter markers, and Australian English storytelling voice (<code>realise</code>, <code>colour</code>, <code>labelled</code>, <code>organisation</code>)</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">The Missing Piece &mdash; <code>a2ui-textual</code></strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Every time a fresh session touches our Textual + A2UI v1.0 renderer without a skill, it risks repeating the ten Cycle 2 traps</li>
    </ul>
  </li>
</ol>

<!--
Before we extract our new skill, it's worth noting that three bespoke project skills are already quietly doing heavy lifting in this repository. First is `agy-brain-explorer`, which documents the on-disk schema of `~/.gemini` brain directories and is mounted straight into Brain Explorer's in-process SDK agent via `skills_paths`. Second are `slidev-deck` and `bjm-voice`, which built the very slides and chapter-marked `asciinema` players you're looking at right now—and keep my spelling firmly in Australian English. What we're still missing is a bespoke skill for our A2UI v1.0 Textual renderer so future sessions never stumble into those ten Cycle 2 traps again.
-->

---
layout: cast-full
title: "Turning Exploratory Friction into a2ui-textual with /agy-customizations"
cast: /casts/way-3-agy-customizations.cast
autoPlay: false
speed: 2.0
idleTimeLimit: 2.0
fit: both
---

<!-- S4-03 -->
<div class="w-full max-w-4xl mx-auto p-5 rounded-xl bg-[#1a1b26] border border-emerald-500/30 shadow-2xl space-y-4">
  <div class="flex items-start justify-between gap-4 pb-3 border-b border-gray-800">
    <div>
      <div class="text-xs font-mono text-emerald-400 uppercase tracking-wider">Trajectory 4 &middot; Way 3 Synthesis &amp; Cold Verification</div>
      <h3 class="text-lg font-bold text-white mt-0.5 m-0">Turning Exploratory Friction into <code>a2ui-textual</code> with <code>/agy-customizations</code></h3>
      <div class="text-xs font-mono text-gray-400 mt-1">Target cast: <code>/casts/way-3-agy-customizations.cast</code></div>
    </div>
    <span class="shrink-0 px-2.5 py-1 rounded-full text-xs font-mono border border-amber-500/40 bg-amber-500/10 text-amber-300">
      CAST Placeholder &middot; 4 Stop Points (m1&ndash;m4)
    </span>
  </div>

  <div class="space-y-3 text-xs font-mono">
    <div class="p-3.5 rounded-lg bg-[#121317] border border-gray-800/80 space-y-1.5">
      <div class="text-emerald-300 font-semibold">m1 &rarr; m2 &middot; Before / After: /agy-customizations synthesis prompt</div>
      <div class="text-gray-400">m1: <code>agy</code> prompt box empty</div>
      <div class="text-gray-200 leading-relaxed">m2: <code>/agy-customizations Please turn what we learned building and reviewing our A2UI v1.0 Textual renderer and Antigravity SDK integration into a reusable workspace skill</code></div>
    </div>

    <div class="p-3.5 rounded-lg bg-[#121317] border border-gray-800/80 space-y-1.5">
      <div class="text-emerald-300 font-semibold">m3 &rarr; m4 &middot; Before / After: Phase 3 cold-session verification prompt</div>
      <div class="text-gray-400">m3: <code>.agents/skills/a2ui-textual/</code> synthesised and registered; cold-session prompt box empty</div>
      <div class="text-gray-200 leading-relaxed">m4: <code>Build an A2UI v1.0 surface for our Python Textual TUI that compares Skill Activations across Way 1 plugins, Way 2 community skills, and Way 3 bespoke skills with interactive tabs and a tier filter.</code></div>
    </div>
  </div>

  <div class="text-[11px] font-mono text-gray-500 pt-1">
    Awaiting <code>recordings/final/way-3-agy-customizations.cast</code> &mdash; switches automatically to <code>asciinema-player</code> once synced.
  </div>
</div>

<!--
Remember our heel turn at the end of Act 1—"I don't write skills by hand; Antigravity writes them for me"? Here is that promise in action in `way-3-agy-customizations.cast`. At our first prompt stop point, right after solving the Cycle 2 bugs, we run `/agy-customizations` and ask Antigravity to turn what we learned building and reviewing our A2UI v1.0 Textual renderer and Antigravity SDK integration into a reusable workspace skill. It distils the core workflow into `.agents/skills/a2ui-textual/SKILL.md` and splits the ten deep integration traps into `references/a2ui-v1-textual-gotchas.md`. Then, at our second prompt stop point, we open a brand-new cold session and ask it to build an interactive A2UI v1.0 surface comparing Skill Activations across Way 1, Way 2, and Way 3. Watch the cold agent trigger Tier 1 discovery, read Tier 2 `SKILL.md`, pull Tier 3 `a2ui-v1-textual-gotchas.md`, and pass `STRICT_VALIDATION` on the first try.
-->

---
layout: skill-breakdown
way: 3
title: "Inside .agents/skills/a2ui-textual/SKILL.md (Tiers 1 &amp; 2)"
---

<!-- S4-04 -->
<div class="space-y-4">

```markdown
---
name: a2ui-textual
description: >-
  Build, validate, and debug A2UI v1.0 generative surfaces inside Python Textualize
  (Textual) TUIs powered by a2ui-core, a2ui-agent-sdk, MessageProcessor, BasicCatalog,
  and in-process google-antigravity SDK agents. Use when generating or parsing A2UI v1.0
  JSON envelopes, mapping BasicCatalog components to Textual widgets, or embedding
  LocalAgentConfig agents inside a Textual application.
---
# A2UI v1.0 for Python Textual TUIs
Consult [`references/a2ui-v1-textual-gotchas.md`](references/a2ui-v1-textual-gotchas.md) whenever you hit
`A2uiError` / `A2uiIntegrityError`, blank template `List` components, `Select.BLANK` / `MarkupError`
crashes, frozen button action contexts, or corrupted Textual terminal output.
```

  <div class="grid grid-cols-2 gap-4 text-xs pt-2">
    <div class="p-3 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-emerald-300 font-semibold">Tier 1 Routing Trigger (~60 Tokens):</span> Matches any prompt mentioning A2UI v1.0, <code>BasicCatalog</code>, Textual widgets, or embedded <code>LocalAgentConfig</code> agents.
    </div>
    <div class="p-3 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-emerald-300 font-semibold">Tier 2 Operational Runbook (94 Lines):</span> Covers v1.0 catalogue setup, atomic <code>STRICT_VALIDATION</code> staging, Textual 8+ widget mapping, and <code>ruff</code>/<code>mypy</code>/<code>pytest</code> verification.
    </div>
  </div>
</div>

<!--
Let's look at the two files `/agy-customizations` generated in `.agents/skills/a2ui-textual/`. First is `SKILL.md`, which handles Tiers 1 and 2. The YAML `description` packs the exact domain keywords—A2UI v1.0, `Textual`, `a2ui-core`, `MessageProcessor`, `BasicCatalog`, and `LocalAgentConfig`—into around 60 tokens so Tier 1 routing fires reliably in a cold session. The Markdown body stays under 100 lines, giving the agent the golden-path runbook and an explicit pointer to `references/a2ui-v1-textual-gotchas.md`.
-->

---
layout: skill-breakdown
way: 3
title: "Inside references/a2ui-v1-textual-gotchas.md (Tier 3 Deep Context)"
---

<!-- S4-05 -->
<div class="space-y-4">

```markdown
## 1. `@path` DataBindings vs v0.9 `path` (plus `TemplateChildList`)
- **Symptom**: `Text` labels render literal `"{'path': '/header'}"` and template `List` renders zero cards.
- **Fix**: Emit `{"@path": "/..."}` for bindings, and wrap `TemplateChildList` `"path"` as `{"@path": path}`.

## 5. Click-Time Action Context Evaluation (`DataContext.resolve_action`)
- **Symptom**: Clicking a `Button` after editing a `TextField` or `ChoicePicker` sends stale initial values.
- **Fix**: Store `raw_action` and `data_context` on the button and resolve inside `on_button_pressed`.

## 9. `logging.FileHandler` Is a Subclass of `logging.StreamHandler`
- **Fix**: Preserve `FileHandler` (`isinstance(h, StreamHandler) and not isinstance(h, FileHandler)`).
```

  <div class="grid grid-cols-2 gap-4 text-xs pt-2">
    <div class="p-3 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-emerald-300 font-semibold">Symptom &rarr; Root Cause &rarr; Fix:</span> Structured for fast agent diagnosis without polluting unrelated Python or Slidev turns.
    </div>
    <div class="p-3 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-emerald-300 font-semibold">Zero Hand-Authoring:</span> Distilled directly from our Exploratory Run diff and <strong>EGM</strong> Cycle 2 findings via <code>/agy-customizations</code>.
    </div>
  </div>
</div>

<!--
And here is Tier 3: `references/a2ui-v1-textual-gotchas.md`. Instead of bloating every session with 114 lines of edge-case troubleshooting, this file sits at Tier 3 and loads only when an agent is actively building or debugging A2UI v1.0 Textual surfaces. Each of the ten traps is formatted as `Symptom -> Root Cause -> Fix` with copy-pasteable code—from `@path` versus `TemplateChildList`, to click-time `resolve_action`, to `FileHandler` subclassing `StreamHandler`.
-->

---
layout: cast-full
title: "Closing the Loop: Inspecting Our Build Trajectories in Brain Explorer"
cast: /casts/way-3-brain-explorer-payoff.cast
autoPlay: false
speed: 2.0
idleTimeLimit: 2.0
fit: both
---

<!-- S4-06 -->
<div class="w-full max-w-4xl mx-auto p-5 rounded-xl bg-[#1a1b26] border border-emerald-500/30 shadow-2xl space-y-3.5">
  <div class="flex items-start justify-between gap-4 pb-3 border-b border-gray-800">
    <div>
      <div class="text-xs font-mono text-emerald-400 uppercase tracking-wider">Brain Explorer CLI &amp; TUI Payoff</div>
      <h3 class="text-lg font-bold text-white mt-0.5 m-0">Closing the Loop: Inspecting Our Build Trajectories in Brain Explorer</h3>
      <div class="text-xs font-mono text-gray-400 mt-1">Target cast: <code>/casts/way-3-brain-explorer-payoff.cast</code></div>
    </div>
    <span class="shrink-0 px-2.5 py-1 rounded-full text-xs font-mono border border-amber-500/40 bg-amber-500/10 text-amber-300">
      CAST Placeholder &middot; 6 Stop Points (m1&ndash;m6)
    </span>
  </div>

  <div class="space-y-2 text-xs font-mono">
    <div class="p-3 rounded-lg bg-[#121317] border border-gray-800/80 space-y-1">
      <div class="text-emerald-300 font-semibold">m1 &rarr; m2 &middot; Before / After: CLI sessions overview command</div>
      <div class="text-gray-400">m1: Clean <code>zsh</code> prompt ready</div>
      <div class="text-gray-200">m2: <code>uv run brain-explorer sessions --project skills-three-ways-akl</code></div>
    </div>

    <div class="p-3 rounded-lg bg-[#121317] border border-gray-800/80 space-y-1">
      <div class="text-emerald-300 font-semibold">m3 &rarr; m4 &middot; Before / After: Launch Brain Explorer TUI command</div>
      <div class="text-gray-400">m3: CLI sessions table rendered; <code>zsh</code> prompt ready</div>
      <div class="text-gray-200">m4: <code>uv run brain-explorer</code></div>
    </div>

    <div class="p-3 rounded-lg bg-[#121317] border border-gray-800/80 space-y-1">
      <div class="text-emerald-300 font-semibold">m5 &rarr; m6 &middot; Before / After: In-TUI A2UI v1.0 prompt</div>
      <div class="text-gray-400">m5: <strong>Brain Explorer</strong> TUI open (<code>Ctrl+B</code> sidebar browsed), <code>/</code> prompt input focused and empty</div>
      <div class="text-gray-200 leading-relaxed">m6: <code>Compare how Way 1 plugin skills, Way 2 community skills, and Way 3 bespoke skills were activated across our Brain Explorer build sessions, and group them into an interactive A2UI v1.0 tabbed breakdown.</code></div>
    </div>
  </div>

  <div class="text-[11px] font-mono text-gray-500 pt-1">
    Awaiting <code>recordings/final/way-3-brain-explorer-payoff.cast</code> &mdash; switches automatically to <code>asciinema-player</code> once synced.
  </div>
</div>

<!--
Now let's bring the whole story together in `way-3-brain-explorer-payoff.cast`. First, we run `uv run brain-explorer sessions --project skills-three-ways-akl` to see a fast CLI summary table of the four canonical Session Trajectories we recorded while building the app across Ways 1, 2, and 3. Next, we launch the interactive Textual TUI with `uv run brain-explorer`. In the left sidebar, the deterministic `TrajectoryStore` lets us step through each trajectory and its Skill Activations instantly. Then, at our final prompt stop point, we press `/` inside the TUI and ask the embedded Antigravity SDK agent to compare how Way 1 plugin skills, Way 2 community skills, and Way 3 bespoke skills were activated across our build sessions and group them into an interactive A2UI v1.0 tabbed breakdown. Watch the live A2UI v1.0 tabs render inside Textual—and when we press `Ctrl+I`, the protocol inspector reveals the validated `"version": "1.0"` envelope and `DataModel` driving the screen.
-->

---
layout: skill-breakdown
way: mashup
title: "What Brain Explorer Revealed: 4 Build Trajectories Across Three Ways"
---

<!-- S4-07 -->
<div class="space-y-4">

```text
Trajectory 1 · Way 1 Plugin Discovery        -> plugin, google-antigravity-sdk              [way_1_plugin]
Trajectory 2 · Way 2 Skill Evaluation        -> find-skills                                 [way_2_community]
Trajectory 3 · Two-Pass EGM Build Cycle      -> google-antigravity-sdk + 4x EGM subagents   [way_1_plugin]
   (+ 8 Cycle 1 & Cycle 2 EGM trajectories)     uv-package-manager + 7 Python skills        [way_2_community]
                                                agy-brain-explorer                          [way_3_bespoke]
Trajectory 4 · Way 3 Synthesis & Cold Test   -> agy-customizations                          [way_1_plugin]
                                                writing-for-agents                          [way_2_community]
                                                a2ui-textual (SKILL.md + Tier 3 gotchas)    [way_3_bespoke]
```

  <div class="grid grid-cols-2 gap-4 text-xs pt-2">
    <div class="p-3 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-purple-300 font-semibold">Dual Activation Evidence:</span> <code>TrajectoryStore</code> detects both explicit <code>&lt;SKILL&gt;</code> slash-command invocations and on-demand <code>SKILL.md</code> / <code>references/</code> file reads in <code>transcript.jsonl</code>.
    </div>
    <div class="p-3 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-purple-300 font-semibold">The Three Ways in Concert:</span> Every build stage combined platform plugins, community conventions, and repo-specific bespoke skills.
    </div>
  </div>
</div>

<!--
Looking at the breakdown inside Brain Explorer makes something really clear: the Three Ways aren't isolated silos you graduate out of—they layer together in the same workflow. Look at Trajectory 3 and Trajectory 4 on screen: in a single build session, the agent combines Way 1 platform plugins (`google-antigravity-sdk`, `agy-customizations`, and the EGM review subagents), Way 2 community workflow skills (`wshobson/agents` and `writing-for-agents`), and Way 3 bespoke project skills (`agy-brain-explorer` and our newly minted `a2ui-textual` skill). And because `TrajectoryStore` inspects both `<SKILL>` slash commands and `SKILL.md` file reads inside `~/.gemini`, you can see the exact moment Tier 2 and Tier 3 progressive disclosure kicked in.
-->

---
layout: default
---

<!-- S4-08 -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Skills Three Ways: Choosing the Right Tier for the Job</h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white">Way 1 &middot; Ecosystem &amp; Plugin Skills (Start Here)</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Enable official plugins (<code>google-antigravity-sdk</code>, <strong>EGM</strong>) first for authoritative platform SDKs and independent architectural review subagents</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Way 2 &middot; Community Workflow Skills (Adopt &amp; Vet)</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Use <code>find-skills</code> (<code>npx skills find</code>) to adopt high-trust language and workflow packs (<code>wshobson/agents</code>) while explicitly noting where ecosystem coverage stops</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Way 3 &middot; Bespoke In-Project Skills (Capture Exploratory Friction)</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Don't hand-write skills up front&mdash;solve the problem once in an Exploratory Run, let <code>/agy-customizations</code> synthesise the 3-tier skill into <code>.agents/skills/</code>, and verify it in a clean cold session</li>
    </ul>
  </li>
</ol>

<!--
So if you take one mental model back to your team tomorrow, here is Skills Three Ways on a single slide. First, reach for Way 1 Ecosystem and Plugin Skills whenever you're working with a vendor SDK or want specialist subagent reviewers like EGM watching your back. Second, use `find-skills` to pull in vetted Way 2 Community Workflow Skills for standard language hygiene—and treat empty search results as early radar for where your integration risks live. Third, when you hit real friction on your own architecture or internal stack, don't write a massive `AGENTS.md` or hand-craft a skill from scratch: solve the problem interactively, invoke `/agy-customizations` to distil it into a 3-tier bespoke skill, and test it in a fresh session.
-->

---
layout: default
---

<!-- S4-09 -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Links &amp; Resources</h2>
</div>

<div class="space-y-4 mt-6">
  <div class="p-4 rounded-xl bg-gray-900 border border-gray-800">
    <div class="flex items-center justify-between">
      <div class="text-xs font-mono text-cyan-400 uppercase tracking-wide">Presentation Deck, Recordings &amp; Brain Explorer Source</div>
      <span class="text-xs font-mono text-gray-500">github.com</span>
    </div>
    <div class="text-base font-bold font-mono mt-1">
      <a href="https://github.com/domesticmouse/skills-three-ways-akl" target="_blank" class="text-cyan-300 hover:underline">github.com/domesticmouse/skills-three-ways-akl</a>
    </div>
    <p class="text-xs text-gray-400 mt-1.5 m-0">
      Full Slidev deck (<code>slides/</code>), chapter-marked <code>asciinema</code> recordings (<code>recordings/final/</code>), Brain Explorer Textual TUI, and <code>.agents/skills/a2ui-textual/</code>.
    </p>
  </div>

  <div class="p-4 rounded-xl bg-gray-900 border border-gray-800">
    <div class="flex items-center justify-between">
      <div class="text-xs font-mono text-amber-400 uppercase tracking-wide">Open Agent Skills Ecosystem &amp; CLI</div>
      <span class="text-xs font-mono text-gray-500">skills.sh &middot; npx skills find</span>
    </div>
    <div class="text-base font-bold font-mono mt-1">
      <a href="https://skills.sh" target="_blank" class="text-amber-300 hover:underline">skills.sh</a>
    </div>
    <p class="text-xs text-gray-400 mt-1.5 m-0">
      Discover, evaluate, and lock community workflow skills (<code>vercel-labs/skills@find-skills</code>, <code>wshobson/agents</code>).
    </p>
  </div>

  <div class="p-4 rounded-xl bg-gray-900 border border-gray-800">
    <div class="flex items-center justify-between">
      <div class="text-xs font-mono text-emerald-400 uppercase tracking-wide">Google Antigravity &amp; Python SDK</div>
      <span class="text-xs font-mono text-gray-500">antigravity.google</span>
    </div>
    <div class="text-base font-bold font-mono mt-1">
      <a href="https://antigravity.google" target="_blank" class="text-emerald-300 hover:underline">antigravity.google</a>
    </div>
    <p class="text-xs text-gray-400 mt-1.5 m-0">
      In-process <code>google-antigravity</code> Python SDK (<code>LocalAgentConfig</code>, <code>skills_paths</code>), <code>/plugin</code>, and <code>/agy-customizations</code>.
    </p>
  </div>
</div>

<!--
Everything we walked through today—the Slidev presentation deck, the chapter-marked `asciinema` recordings, the Brain Explorer Python Textual TUI, and the `a2ui-textual` skill we extracted—is up on GitHub at `github.com/domesticmouse/skills-three-ways-akl`. Thank you so much, DevFest Auckland—I'd love to take your questions!
-->
