---
layout: center
class: text-center
---

<!-- S2-01 -->
<div class="space-y-4">
  <h1 class="text-4xl font-extrabold text-white">
    Way 1 &middot; Ecosystem &amp; Plugin Skills
  </h1>
  <p class="text-xl font-mono text-cyan-300">
    google-antigravity-sdk &middot; egm-review-subagents
  </p>
  <p class="text-base text-gray-400 max-w-xl mx-auto">
    Starting from zero with curated official plugins that pair domain skills with specialist review subagents
  </p>
</div>

<!--
Now let's dive into Way 1: Ecosystem and Plugin Skills. When you start a brand-new project in Antigravity, the fastest way to get trustworthy domain knowledge and architectural guardrails into your workspace is through official plugins. They bundle curated skills together with specialist subagent personas so you don't start from a blank slate.
-->

---
layout: default
---

<!-- S2-02 -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">What Official Plugins Bring to the Table</h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white">Curated Domain Runbooks Out of the Box</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Official plugins like <code>google-antigravity-sdk</code> ship up-to-date API patterns (<code>Agent</code>, <code>LocalAgentConfig</code>, <code>skills_paths</code>, <code>policy</code>, <code>BudgetConfig</code>)</li>
      <li>Maintained alongside the SDK itself so agents avoid stale training assumptions</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Specialist Subagent Personas Paired with Skills</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>The <strong>EGM</strong> plugin provides dedicated critic personas (<code>egm-design</code>, <code>egm-zoom-out</code>, <code>egm-codebase-details</code>, <code>egm-implementation-readiness</code>)</li>
      <li>Each reviewer audits architecture and implementation in an isolated context window</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Single-Unit Lifecycle &amp; Discovery</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Installed and toggled as one unit via <code>/plugin</code></li>
      <li>Keeps Tier 1 discovery lightweight (~100 tokens per skill) until a task triggers Tier 2 activation</li>
    </ul>
  </li>
</ol>

<!--
Why start with plugins rather than immediately writing your own skills or scraping documentation? Three reasons. First, official plugins ship curated runbooks for fast-moving SDKs like the Google Antigravity Python SDK, so the agent uses current `LocalAgentConfig` patterns instead of guessing from stale training weights. Second, plugins can bundle specialist subagents alongside skills—like the EGM review suite, which gives us four distinct architectural critics. And third, plugins install and enable as a single unit while still obeying the same 3-tier progressive disclosure budget we saw in Act 1.
-->

---
layout: cast-full
title: "Bootstrapping find-skills & Verifying Way 1 Plugins in agy"
cast: /casts/way-1-plugins-setup.cast
autoPlay: false
speed: 2.0
idleTimeLimit: 2.0
fit: both
---

<!-- S2-03 -->
<div class="w-full max-w-4xl mx-auto p-5 rounded-xl bg-[#1a1b26] border border-cyan-500/30 shadow-2xl space-y-3.5">
  <div class="flex items-start justify-between gap-4 pb-3 border-b border-gray-800">
    <div>
      <div class="text-xs font-mono text-cyan-400 uppercase tracking-wider">Trajectory 1 &middot; Way 1 Plugin Discovery</div>
      <h3 class="text-lg font-bold text-white mt-0.5 m-0">Bootstrapping find-skills &amp; Verifying Way 1 Plugins in agy</h3>
      <div class="text-xs font-mono text-gray-400 mt-1">Target cast: <code>/casts/way-1-plugins-setup.cast</code></div>
    </div>
    <span class="shrink-0 px-2.5 py-1 rounded-full text-xs font-mono border border-amber-500/40 bg-amber-500/10 text-amber-300">
      CAST Placeholder &middot; 6 Stop Points (m1&ndash;m6)
    </span>
  </div>
  <div class="space-y-2 text-xs font-mono">
    <div class="p-3 rounded-lg bg-[#121317] border border-gray-800/80 space-y-1">
      <div class="text-cyan-300 font-semibold">m1 &rarr; m2 &middot; Before / After: Install find-skills</div>
      <div class="text-gray-400">m1: Clean <code>zsh</code> prompt ready</div>
      <div class="text-gray-200">m2: <code>npx skills add vercel-labs/skills@find-skills -g -y</code></div>
    </div>
    <div class="p-3 rounded-lg bg-[#121317] border border-gray-800/80 space-y-1">
      <div class="text-cyan-300 font-semibold">m3 &rarr; m4 &middot; Before / After: Launch agy</div>
      <div class="text-gray-400">m3: <code>find-skills</code> installation finished; <code>zsh</code> prompt ready</div>
      <div class="text-gray-200">m4: <code>agy</code></div>
    </div>
    <div class="p-3 rounded-lg bg-[#121317] border border-gray-800/80 space-y-1">
      <div class="text-cyan-300 font-semibold">m5 &rarr; m6 &middot; Before / After: Verify Way 1 plugins prompt</div>
      <div class="text-gray-400">m5: <code>agy</code> banner loaded and <code>&gt;</code> prompt box empty</div>
      <div class="text-gray-200 leading-relaxed">m6: <code>/plugin Please check that the Google Antigravity SDK plugin (google-antigravity-sdk) and the EGM review subagents are enabled for this workspace, and show me what skills and specialist agents they provide.</code></div>
    </div>
  </div>
  <div class="text-[11px] font-mono text-gray-500 pt-1">
    Awaiting <code>recordings/final/way-1-plugins-setup.cast</code> &mdash; switches automatically to <code>asciinema-player</code> once synced.
  </div>
</div>

<!--
Let's step through our first recording. At our first stop point in `zsh`, we install Vercel Labs' `find-skills` CLI globally with `npx skills add vercel-labs/skills@find-skills -g -y` so it is ready when we move into community skills in Act 3. Next, we launch `agy` right in the project root. Once the prompt box is ready, we run `/plugin` and ask Antigravity to verify that both the `google-antigravity-sdk` plugin and the EGM review subagents are enabled, and to summarise what capabilities they provide. Watch how it inspects the enabled plugins and reports back both the in-process Python SDK primitives and the four EGM reviewer roles.
-->

---
layout: skill-breakdown
way: 1
title: "Inside google-antigravity-sdk: In-Process Agent &amp; LocalAgentConfig"
---

<!-- S2-04 -->
<div class="space-y-4">

```python
from google.antigravity import Agent, LocalAgentConfig, types
from google.antigravity.hooks import policy

config = LocalAgentConfig(
    model="gemini-2.5-pro",
    skills_paths=[repo_root / ".agents" / "skills"],
    tools=[list_trajectories, get_trajectory_detail, get_skill_breakdown],
    policy=[
        policy.deny_all(),
        policy.allow("finish"),
        policy.allow("view_file"),
        policy.allow("list_trajectories"),
        policy.allow("get_trajectory_detail"),
        policy.allow("get_skill_breakdown"),
    ],
    enable_subagents=False,
    budget=types.BudgetConfig(max_iterations=8, max_tokens=24_000),
)
```

  <div class="grid grid-cols-2 gap-4 text-xs pt-2">
    <div class="p-3 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-cyan-300 font-semibold">skills_paths Mounting:</span> Injects workspace skills directly into the in-process SDK agent so our app can reuse the same skill packages as the CLI.
    </div>
    <div class="p-3 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-cyan-300 font-semibold">Least-Privilege Policy &amp; Budgets:</span> Locks the embedded agent down to read-only trajectory tools, <code>view_file</code>, and strict token/iteration budgets.
    </div>
  </div>
</div>

<!--
Let's zoom in on what the `google-antigravity-sdk` plugin teaches our coding agent. Instead of shelling out to a subprocess or spinning up an HTTP bridge, we can embed an Antigravity `Agent` directly in-process inside our Python application using `LocalAgentConfig`. Notice two things the skill emphasises: first, `skills_paths` lets our embedded Python agent mount the exact same `.agents/skills` directory that the CLI uses. Second, it enforces an explicit deny-by-default `policy` and `BudgetConfig`, so an embedded agent inside a TUI only ever runs read-only inspection tools within a bounded token budget.
-->

---
layout: skill-breakdown
way: 1
title: "Inside the EGM Plugin: Specialist Review Subagents"
---

<!-- S2-05 -->
<div class="space-y-4">

```text
egm-design                    -> Hostile Design Critic (boundaries, failure modes, runtime isolation)
egm-zoom-out                  -> Skeptical Architect (YAGNI, minimalism, stripping over-engineering)
egm-codebase-details          -> Pedantic Technical Auditor (API contracts, schema fidelity, library reuse)
egm-implementation-readiness  -> Pragmatic Tech Lead (actionable specs, zero ambiguous hand-offs)
```

  <div class="grid grid-cols-2 gap-4 text-xs pt-2">
    <div class="p-3 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-cyan-300 font-semibold">Fresh Context Windows:</span> Each reviewer runs as an independent subagent without inheriting the author agent's confirmation bias.
    </div>
    <div class="p-3 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-cyan-300 font-semibold">Productive Tension:</span> <code>egm-design</code> hunts for missing edge cases while <code>egm-zoom-out</code> pushes back against unnecessary complexity.
    </div>
  </div>
</div>

<!--
Alongside `google-antigravity-sdk`, we enabled the EGM review subagents. Anyone who has built with coding agents knows they are wonderfully optimistic—if you ask an agent whether its own design is ready, it will enthusiastically tell you everything is brilliant. The EGM plugin fixes that by giving us four opinionated reviewer subagents that run in fresh context windows: a Hostile Design Critic, a Skeptical Architect that enforces YAGNI, a Pedantic Technical Auditor that checks actual library signatures, and a Pragmatic Tech Lead that checks implementation readiness.
-->

---
layout: default
---

<!-- S2-06 -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Way 1 Takeaway: Guardrails Before We Write a Line of Python</h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white">SDK Correctness Solved</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li><code>google-antigravity-sdk</code> gives the agent authoritative in-process <code>Agent</code> and <code>LocalAgentConfig</code> patterns</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Architectural Critics Armed</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>The four <strong>EGM</strong> subagents are ready to stress-test our <strong>Brain Explorer</strong> design before and after implementation</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Next Question &mdash; What About Our Stack?</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>We are building a modern Python CLI and Textualize (<code>Textual</code>) TUI</li>
      <li>Can the broader open-source community fill in our Python and TUI engineering conventions?</li>
    </ul>
  </li>
</ol>

<!--
So before we have written a single line of Python for Brain Explorer, Way 1 plugins have solved two massive problems: how to embed the Antigravity SDK safely in-process, and how to review our architecture with independent specialist subagents. That naturally raises the next question: what about day-to-day Python engineering conventions—`uv`, strict `mypy` typing, `asyncio`, `pytest`, and building a Textual TUI? For that, we turn to Way 2: Community Workflow Skills.
-->
