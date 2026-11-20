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
    <strong class="text-white"><code>slidev-deck</code> &amp; <code>bjm-voice</code> (Presentation &amp; Editorial Hygiene on <code>main</code>)</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Pre-seeded <code>agy-brain-explorer</code> came along in <code>codelab/start</code>; meanwhile <code>slidev-deck</code> and <code>bjm-voice</code> shaped these slides and Australian English voice (<code>realise</code>, <code>colour</code>, <code>labelled</code>, <code>organisation</code>)</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">The Missing Piece &mdash; Our A2UI + Textual Skill</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Every time a fresh session touches our Textual + A2UI v1.0 renderer without a skill, it risks repeating the ten Cycle 2 traps</li>
    </ul>
  </li>
</ol>

<!--
Before we extract our new skill in Lab 4, notice that bespoke project skills are already quietly doing heavy lifting here. `agy-brain-explorer` came along in `codelab/start` so your agent—and Brain Explorer's embedded SDK agent—knew how `~/.gemini` brain directories work on disk. Meanwhile on `main`, `slidev-deck` and `bjm-voice` built the slides you are looking at right now and kept my spelling firmly in Australian English. What we are still missing in your lab workspace is a bespoke skill for our A2UI v1.0 Textual renderer so fresh sessions never stumble into those ten Cycle 2 traps again.
-->

---
layout: lab-step
step: "Lab 4"
way: 3
duration: "~15 min"
title: "Synthesise &amp; Cold-Verify Your Bespoke Skill"
codelabAnchor: "#step-4"
checkpoint: "codelab/checkpoint-4-bespoke-skill"
---

<!-- S4-03 -->

<PromptCard
  kind="prompt"
  way="3"
  label="Phase 2 · Synthesise bespoke skill with /agy-customizations"
  text="/agy-customizations Please turn what we learned building and reviewing our A2UI v1.0 Textual renderer and Antigravity SDK integration into a reusable workspace skill"
/>

<PromptCard
  kind="prompt"
  way="3"
  label="Phase 3 · Exit agy (Ctrl+D x2), reopen cold, &amp; test routing"
  text="Build an A2UI v1.0 surface for our Python Textual TUI that compares Skill Activations across Way 1 plugins, Way 2 community skills, and Way 3 bespoke skills with interactive tabs and a tier filter."
/>

::verify::

<ul class="list-disc pl-4 space-y-1.5">
  <li><code>.agents/skills/&lt;your-skill&gt;/SKILL.md</code> and <code>references/</code> exist on disk.</li>
  <li><strong>Exit <code>agy</code> completely</strong> (<code>Ctrl+D</code> twice) before Phase 3 so context is empty.</li>
  <li>Cold session auto-triggers your skill without naming it and passes <code>STRICT_VALIDATION</code>.</li>
</ul>

<!--
Remember our promise in Act 1: "You don't write the skill by hand—Antigravity writes it for you"? Put that to work in Lab 4 right now. First, run `/agy-customizations` in the same session where you built or audited the renderer so it distils your runbook into `SKILL.md` and splits the edge cases into `references/`. Then—this is the crucial test—exit `agy` completely with `Ctrl+D` twice, open a cold session, and paste the Phase 3 prompt. Notice the prompt never names your new skill; watch Tier 1 semantic routing pull it in automatically!
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
Compare the skill you just synthesised with the two files `/agy-customizations` generated in our reference run under `.agents/skills/a2ui-textual/`. First is `SKILL.md`, which handles Tiers 1 and 2. The YAML `description` packs the exact domain keywords—A2UI v1.0, `Textual`, `a2ui-core`, `MessageProcessor`, `BasicCatalog`, and `LocalAgentConfig`—into around 60 tokens so Tier 1 routing fires reliably in a cold session. The Markdown body stays under 100 lines, giving the agent the golden-path runbook and an explicit pointer to `references/a2ui-v1-textual-gotchas.md`.
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
layout: lab-step
step: "Lab 5"
way: "mashup"
duration: "~15 min"
title: "Brain Explorer Payoff: Inspect Your Own Sessions"
codelabAnchor: "#step-5"
checkpoint: "codelab/checkpoint-4-bespoke-skill"
---

<!-- S4-06 -->

<PromptCard
  kind="command"
  way="mashup"
  label="1. Inspect your Session Trajectories &amp; launch Brain Explorer TUI"
  text='uv run brain-explorer sessions --project "$(basename "$PWD")" --limit 20 && uv run brain-explorer'
/>

<PromptCard
  kind="prompt"
  way="mashup"
  label="2. Press / inside the TUI for an A2UI v1.0 comparison"
  text="Compare how Way 1 plugin skills, Way 2 community skills, and Way 3 bespoke skills were activated across our Brain Explorer build sessions, and group them into an interactive A2UI v1.0 tabbed breakdown."
/>

::verify::

<ul class="list-disc pl-4 space-y-1.5">
  <li>CLI &amp; <code>Ctrl+B</code> sidebar show your <strong>own</strong> Labs 0–4 trajectories and skill tiers.</li>
  <li>Pressing <code>/</code> renders interactive A2UI v1.0 tabs cleanly without stderr corruption.</li>
  <li>Press <code>Ctrl+I</code> to inspect the validated <code>"version": "1.0"</code> envelope &amp; <code>DataModel</code>.</li>
</ul>

<!--
Here is the payoff in Lab 5: exit `agy` completely (`Ctrl+D` twice) and inspect the real `~/.gemini` Session Trajectories you created over the last 75 minutes. First, `uv run brain-explorer sessions` prints a fast deterministic table of your build sessions—zero LLM calls needed. Next, launch the TUI with `uv run brain-explorer`, browse the `Ctrl+B` sidebar, press `/` to focus the prompt bar, and ask the embedded Antigravity SDK agent to compare your Way 1, Way 2, and Way 3 Skill Activations inside interactive A2UI v1.0 tabs. Press `Ctrl+I` to inspect the validated JSON envelope underneath.
-->

---
layout: skill-breakdown
way: mashup
title: "What Brain Explorer Reveals: Three Ways Working in Concert"
---

<!-- S4-07 -->
<div class="space-y-4">

```text
Trajectory 1 · Way 1 Plugin Discovery        -> plugin, google-antigravity-sdk              [way_1_plugin]
Trajectory 2 · Way 2 Skill Evaluation        -> find-skills                                 [way_2_community]
Trajectory 3 · Two-Pass EGM Build Cycle      -> google-antigravity-sdk + 4x EGM subagents   [way_1_plugin]
   (+ Cycle 1 & Cycle 2 EGM trajectories)       uv-package-manager + Python skills          [way_2_community]
                                                agy-brain-explorer                          [way_3_bespoke]
Trajectory 4 · Way 3 Synthesis & Cold Test   -> agy-customizations                          [way_1_plugin]
                                                writing-for-agents                          [way_2_community]
                                                your bespoke skill (SKILL.md + references/) [way_3_bespoke]
```

  <div class="grid grid-cols-2 gap-4 text-xs pt-2">
    <div class="p-3 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-purple-300 font-semibold">Dynamic Tier Classification:</span> <code>TrajectoryStore</code> detects <code>&lt;SKILL&gt;</code> slash commands and <code>SKILL.md</code> reads, classifying workspace skills absent from <code>skills-lock.json</code> as <code>way_3_bespoke</code>.
    </div>
    <div class="p-3 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-purple-300 font-semibold">The Three Ways in Concert:</span> Every build stage combined platform plugins, community conventions, and repo-specific bespoke skills.
    </div>
  </div>
</div>

<!--
Looking at your own breakdown inside Brain Explorer makes something crystal clear: the Three Ways aren't isolated silos you graduate out of—they layer together in the same workflow. Across Labs 3 and 4, a single session combines Way 1 platform plugins (`google-antigravity-sdk`, `agy-customizations`, and EGM subagents), Way 2 community workflow skills (`wshobson/agents` and `writing-for-agents`), and Way 3 bespoke project skills (`agy-brain-explorer` plus whatever bespoke skill `/agy-customizations` generated for you). And because `TrajectoryStore` checks `skills-lock.json` dynamically, your newly minted skill shows up right under `way_3_bespoke`.
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
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Links &amp; Resources</h2>
</div>

<div class="grid grid-cols-12 gap-5 mt-4 items-center">
  <div class="col-span-8 space-y-3">
    <div class="p-4 rounded-xl bg-gray-900 border border-gray-800">
      <div class="flex items-center justify-between">
        <div class="text-xs font-mono text-cyan-400 uppercase tracking-wide">90-Minute Codelab, Slidev Deck &amp; Brain Explorer Source</div>
        <span class="text-xs font-mono text-gray-500">github.com</span>
      </div>
      <div class="text-sm font-bold font-mono mt-1">
        <a href="https://github.com/domesticmouse/skills-three-ways-akl" target="_blank" class="text-cyan-300 hover:underline">github.com/domesticmouse/skills-three-ways-akl</a>
      </div>
      <p class="text-xs text-gray-400 mt-1 m-0">
        Interactive codelab (<code>codelab/</code>), Slidev deck (<code>slides/</code>), checkpoint branches (<code>codelab/*</code>), Brain Explorer TUI, and <code>.agents/skills/a2ui-textual/</code>.
      </p>
    </div>
    <div class="p-4 rounded-xl bg-gray-900 border border-gray-800">
      <div class="flex items-center justify-between">
        <div class="text-xs font-mono text-amber-400 uppercase tracking-wide">Open Agent Skills Ecosystem &amp; CLI</div>
        <span class="text-xs font-mono text-gray-500">skills.sh &middot; npx skills find</span>
      </div>
      <div class="text-sm font-bold font-mono mt-1">
        <a href="https://skills.sh" target="_blank" class="text-amber-300 hover:underline">skills.sh</a>
      </div>
      <p class="text-xs text-gray-400 mt-1 m-0">
        Discover, evaluate, and lock community workflow skills (<code>vercel-labs/skills@find-skills</code>, <code>wshobson/agents</code>).
      </p>
    </div>
    <div class="p-4 rounded-xl bg-gray-900 border border-gray-800">
      <div class="flex items-center justify-between">
        <div class="text-xs font-mono text-emerald-400 uppercase tracking-wide">Google Antigravity &amp; Python SDK</div>
        <span class="text-xs font-mono text-gray-500">antigravity.google</span>
      </div>
      <div class="text-sm font-bold font-mono mt-1">
        <a href="https://antigravity.google" target="_blank" class="text-emerald-300 hover:underline">antigravity.google</a>
      </div>
      <p class="text-xs text-gray-400 mt-1 m-0">
        In-process <code>google-antigravity</code> Python SDK (<code>LocalAgentConfig</code>, <code>skills_paths</code>), <code>/plugin</code>, and <code>/agy-customizations</code>.
      </p>
    </div>
  </div>
  <div class="col-span-4 flex flex-col items-center justify-center p-5 rounded-xl bg-[#1a1b22] border border-gray-800">
    <QrBadge size="lg" caption="Scan for the self-paced codelab" />
  </div>
</div>

<!--
Everything we walked through today—the 90-minute self-paced codelab, this Slidev presentation deck, the `codelab/*` recovery checkpoint branches, the Brain Explorer Python Textual TUI, and the `a2ui-textual` reference skill—is up on GitHub at `github.com/domesticmouse/skills-three-ways-akl`. Keep experimenting at your own pace, and feel free to grab me with any questions!
-->
