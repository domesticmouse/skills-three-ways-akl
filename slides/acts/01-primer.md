---
class: text-center
---

<!-- S1-01 -->
<div class="h-full flex flex-col items-center justify-center">
  <h1 class="text-5xl font-extrabold tracking-tight text-white mb-3">
    Skills Three Ways
  </h1>
  <p class="text-2xl text-gray-300 font-light max-w-2xl">
    Ecosystem, Community, and Bespoke Agent Skills in Action
  </p>
  <div class="mt-4 text-sm font-mono text-cyan-300">
    90-Minute Self-Paced Codelab &amp; Walkthrough
  </div>
  <div class="mt-8 text-gray-400 text-base">
    <span class="font-semibold text-gray-200">Brett Morgan</span> &middot; Developer Relations Engineer, Google Cloud
  </div>
  <div class="mt-10 text-xs text-gray-500">
    Press <kbd>Space</kbd> or <kbd>&rarr;</kbd> to advance
  </div>
</div>

<!--
Welcome! Today we are running a 90-minute self-paced codelab exploring three ways of working with AI Agent Skills—from official ecosystem plugins, to community workflow skills, to bespoke skills authored right inside your project—by building and inspecting Brain Explorer, a Python and Textual TUI powered by the Google Antigravity SDK.
-->

---
layout: default
---

<!-- S1-01b -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">About Me: Brett Morgan</h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white">16 Years in Developer Relations at Google</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Crossed the ditch from Sydney to join you here in Auckland for DevFest.</li>
      <li>Supported <strong>Blogger</strong>, <strong>Google+</strong>, <strong>Google Maps</strong>, <strong>Flutter</strong>, and now <strong>Google Antigravity</strong></li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Down the Synthesiser &amp; Electronics Rabbit Hole</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Picked up electronics as a hobby a couple of years ago after watching videos on Eurorack synthesisers</li>
      <li>It quickly snowballed from building modules into reverse-engineering hardware</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">How Agents Re-Shape User Interfaces</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Exploring how LLMs and Antigravity re-shape the definition of &mdash; and requirement for &mdash; user interfaces</li>
    </ul>
  </li>
</ol>

<!--
Before we jump in, a quick bit about me. I'm Brett Morgan, and I've been a Developer Relations Engineer at Google for 16 years. I crossed the ditch from Sydney to be here with you in Auckland for DevFest! Over my time at Google I've supported Blogger, Google+, Google Maps, Flutter, and now Antigravity.

Outside of work, I picked up electronics as a hobby a couple of years ago after falling down a YouTube rabbit hole on Eurorack synthesisers, which somehow snowballed into building modules and reverse-engineering hardware.

And coming from Flutter to Antigravity, I'm deeply interested in how LLMs and agents re-shape the definition of—and even the requirement for—user interfaces.
-->

---
layout: default
---

<!-- S1-01c -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Quote of the Day</h2>
</div>


<div class="h-80 flex flex-col items-center justify-center text-center px-8">
  <blockquote class="text-3xl font-semibold text-white tracking-tight leading-snug max-w-3xl">
    &ldquo;Don&rsquo;t ask &lsquo;How do we add AI to this?&rsquo;<br/>
    Ask &lsquo;What is the agent-first version of this?&rsquo;&rdquo;
  </blockquote>
  <p class="mt-6 text-sm text-gray-400">
    &mdash; From PostHog's post <a href="https://posthog.com/newsletter/building-ai-products" target="_blank" class="text-cyan-300 underline">38 things we've learned about building AI products</a>
  </p>
</div>

<!--
There's a great line from the folks at PostHog that captures how I think about this shift: "Don't ask 'how do we add AI to this?' Ask 'what is the agent-first version of this?'"

Today, we're going to ask what the agent-first version of software architecture, developer tooling, and inspecting our own agent sessions looks like.
-->

---
layout: default
---

<!-- S1-01d -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Today&rsquo;s Itinerary</h2>
</div>

<ol class="space-y-3.5 text-sm text-gray-200 list-decimal pl-6 mt-4 leading-relaxed">
  <li>
    <strong class="text-white">Lab 0 &middot; Setup &amp; Agent Skills Primer (~10 min)</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Monolithic system prompts &rarr; 3-tier progressive disclosure</li>
      <li>Clone <code>codelab/start</code> and ask Antigravity directly how skills work</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Lab 1 &middot; Way 1 Ecosystem &amp; Plugin Skills (~10 min)</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Enable <code>google-antigravity-sdk</code> and <strong>EGM</strong> specialist review subagents via <code>/plugin</code></li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Labs 2–3 &middot; Way 2 Community Workflow Skills &amp; EGM Build (~40 min)</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Search and lock <code>wshobson/agents</code> with <code>find-skills</code>, spot the Textual TUI gap, and run two-pass <strong>EGM</strong> reviews</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Labs 4–5 &middot; Way 3 Bespoke Skills &amp; Brain Explorer Payoff (~30 min)</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Synthesise exploratory friction with <code>/agy-customizations</code> and inspect your own <code>~/.gemini</code> Session Trajectories</li>
    </ul>
  </li>
</ol>

<!--
Here's our itinerary across the next 90 minutes. Work through the self-paced codelab at your own speed while I walk through the ideas on screen:

First, in Lab 0, we clone the clean starter branch and ask Antigravity why stuffing every manual into a monolithic system prompt fails, and how 3-tier progressive disclosure keeps context clean.

Then we build Brain Explorer across Skills Three Ways:
- In Lab 1 (Way 1), we enable official plugins pairing the Google Antigravity SDK with EGM specialist review subagents.
- In Labs 2 and 3 (Way 2), we use `find-skills` to evaluate community Python skills, spot the coverage gap around Textual TUIs, and let EGM push and pull on our architecture.
- Finally, in Labs 4 and 5 (Way 3), we turn the friction we hit into a custom skill with `/agy-customizations`—and close the loop by opening Brain Explorer against your own `~/.gemini` Session Trajectories.
-->

---
layout: default
---

<!-- S1-01e -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Open the Codelab &mdash; Follow Along at Your Own Pace</h2>
</div>

<div class="grid grid-cols-12 gap-6 mt-5 items-center">
  <div class="col-span-5 flex flex-col items-center justify-center p-5 rounded-xl bg-[#1a1b22] border border-gray-800">
    <QrBadge size="lg" caption="Scan to open the 90-minute codelab" />
  </div>
  <div class="col-span-7 space-y-4">
    <div class="p-4 rounded-xl bg-gray-900/80 border border-gray-800 space-y-2">
      <div class="text-xs font-mono uppercase tracking-wider text-cyan-300">Prerequisites</div>
      <div class="flex flex-wrap gap-2 text-xs font-mono">
        <span class="px-2.5 py-1 rounded bg-gray-800 border border-gray-700 text-gray-200">agy (CLI + auth)</span>
        <span class="px-2.5 py-1 rounded bg-gray-800 border border-gray-700 text-gray-200">uv</span>
        <span class="px-2.5 py-1 rounded bg-gray-800 border border-gray-700 text-gray-200">Python 3.12+</span>
        <span class="px-2.5 py-1 rounded bg-gray-800 border border-gray-700 text-gray-200">Node 18+ (npx)</span>
        <span class="px-2.5 py-1 rounded bg-gray-800 border border-gray-700 text-gray-200">git</span>
      </div>
      <p class="text-xs text-gray-400 m-0 pt-1">
        Every prompt, recovery checkpoint branch, and troubleshooting foldout lives in the web codelab so you never have to squint at the projector.
      </p>
    </div>
    <PromptCard
      kind="command"
      way="0"
      label="Clone &amp; Start Lab"
      text="git clone https://github.com/domesticmouse/skills-three-ways-akl.git && cd skills-three-ways-akl && git checkout -b my-lab codelab/start"
    />
  </div>
</div>

<!--
Scan this QR code or open `domesticmouse.github.io/skills-three-ways-akl/` on your laptop right now. Everything you need—one-click copy buttons for every prompt, collapsible troubleshooting tips, and git checkpoint branches in case you ever want to skip ahead—lives in that codelab. Go ahead and get `codelab/start` cloned while we frame the skills primer.
-->

---
layout: center
class: text-center
---

<!-- S1-02 -->
<div class="space-y-4">
  <h1 class="text-4xl font-extrabold text-white">
    What Are Agent Skills?
  </h1>
  <p class="text-lg text-gray-400 max-w-xl mx-auto">
    Why on-demand procedural runbooks beat stuffing everything into your system prompt
  </p>
</div>

<!--
Before we dive into our build story, let's do a quick primer on what Agent Skills actually are and why they exist.
-->

---
layout: default
---

<!-- S1-03 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">The Context Window Trap</h2>
</div>

<div class="grid grid-cols-2 gap-6 mt-6">
  <div class="p-5 rounded-xl bg-red-950/15 border border-red-500/30 space-y-3">
    <div class="text-xs font-mono text-red-400 uppercase">Anti-Pattern: Monolithic AGENTS.md</div>
    <h3 class="text-lg font-bold text-white">Stuffing Every Manual into Always-On Rules</h3>
    <ul class="text-xs text-gray-300 space-y-2 list-disc pl-4">
      <li>Dozens of MCP servers with hundreds of functions</li>
      <li>Massive monolithic <code>AGENTS.md</code> files</li>
      <li>Pasted PDF manuals and sprawling documentation</li>
      <li>Increased token consumption and competing instructions</li>
      <li><strong>Result:</strong> Degraded reasoning and lost focus.</li>
    </ul>
  </div>
  <div class="p-5 rounded-xl bg-emerald-950/15 border border-emerald-500/30 space-y-3">
    <div class="text-xs font-mono text-emerald-400 uppercase">The Solution: Progressive Disclosure</div>
    <h3 class="text-lg font-bold text-white">Modular, Self-Contained Skill Packages</h3>
    <ul class="text-xs text-gray-300 space-y-2 list-disc pl-4">
      <li>Keep <code>AGENTS.md</code> tiny—only universal project conventions</li>
      <li>Package domain-specific workflows into Agent Skills</li>
      <li>Agent sees only an invitation to invoke a capability</li>
      <li>Cheatsheets, runbooks, and scripts load <strong>when required</strong></li>
    </ul>
  </div>
</div>

<!--
Why not just load dozens of MCP servers, paste in PDF manuals, or stuff everything into AGENTS.md? Because always-on rules consume context on every single turn and dilute attention. Skills give us progressive disclosure.
-->

---
layout: default
---

<!-- S1-04 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">What Are Agent Skills?</h2>
</div>

<div class="h-80 flex flex-col items-center justify-center text-center">
  <p class="text-4xl font-semibold text-white tracking-tight">
    "I know, let's ask Antigravity!"
  </p>
</div>

<!--
Jump into Lab 0 in your terminal and ask Antigravity directly: "What are agent skills?"
-->

---
layout: lab-step
step: "Lab 0"
way: 0
duration: "~10 min"
title: "Setup &amp; Warm-Up: Ask Antigravity"
codelabAnchor: "#step-0"
checkpoint: "codelab/start"
---

<!-- S1-05 -->

<PromptCard
  kind="command"
  way="0"
  label="Clone starter branch &amp; launch agy"
  text="git clone https://github.com/domesticmouse/skills-three-ways-akl.git && cd skills-three-ways-akl && git checkout -b my-lab codelab/start && agy"
/>

<PromptCard
  kind="prompt"
  way="0"
  label="Warm-up prompt inside agy"
  text="What are agent skills?"
/>

::verify::

<ul class="list-disc pl-4 space-y-1.5">
  <li><code>agy</code>, <code>uv</code>, <code>python3 &gt;= 3.12</code>, <code>node</code>, and <code>git</code> respond cleanly.</li>
  <li>You are on branch <code>my-lab</code> off <code>codelab/start</code> (empty <code>src/</code>).</li>
  <li><code>agy</code> inspects its customisation skill and explains <code>SKILL.md</code> plus 3-tier progressive disclosure.</li>
</ul>

<!--
Take a few minutes to work through Lab 0 in the codelab. Clone the starter branch `codelab/start` so your workspace has zero finished `src/` code for the agent to peek at, launch `agy`, and ask it "What are agent skills?". Notice how it immediately consults its built-in customisation skill and lays out the directory anatomy and 3-tier loading model.
-->


---
layout: default
---

<!-- S1-06 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Directory Anatomy of an Agent Skill</h2>
</div>

<div class="grid grid-cols-12 gap-6 mt-5 items-center">
  <div class="col-span-6">

```text
.agents/skills/code-reviewer/
├── SKILL.md          # Required: YAML frontmatter + core runbook
├── scripts/          # Optional: Helper scripts & CLI utilities
│   └── run_linter.py
├── references/       # Optional: In-depth documentation & API specs
│   └── style_guide.md
└── resources/        # Optional: Drop-in templates & sample assets
    └── report_template.md
```

  </div>

  <div class="col-span-6 space-y-3 text-xs">
    <div class="p-3 rounded-lg bg-gray-900 border border-gray-800">
      <div class="font-mono font-bold text-cyan-300">SKILL.md (Required)</div>
      <p class="text-gray-400 mt-1">Single entry point kept concise (&lt;500 lines). Contains activation metadata and primary procedural workflow.</p>
    </div>
    <div class="p-3 rounded-lg bg-gray-900 border border-gray-800">
      <div class="font-mono font-bold text-amber-300">scripts/ (Executable Utilities)</div>
      <p class="text-gray-400 mt-1">Deterministic tools so the agent runs tested commands instead of ad hoc on-the-fly solutions.</p>
    </div>
    <div class="p-3 rounded-lg bg-gray-900 border border-gray-800">
      <div class="font-mono font-bold text-emerald-300">references/ &amp; resources/ (Deep Context)</div>
      <p class="text-gray-400 mt-1">In-depth API specs, reference manuals, and template assets loaded on-demand only when a sub-step requires them.</p>
    </div>
  </div>
</div>

<!--
As Antigravity just explained in your terminal, a skill isn't just a loose markdown file—it is a self-contained directory package. SKILL.md acts as the primary runbook, while optional directories hold executable scripts, in-depth documentation, and reusable templates.
-->

---
layout: default
---

<!-- S1-07 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Inside SKILL.md Part 1: YAML Frontmatter</h2>
</div>

<div class="mt-4">

```yaml
---
name: code-reviewer
description: >-
  Reviews code changes for bugs, security vulnerabilities, and style violations.
  Use when reviewing pull requests or checking code quality.
---
```

</div>

<div class="grid grid-cols-2 gap-4 mt-5 text-xs">
  <div class="p-4 rounded-xl bg-gray-900 border border-gray-800">
    <div class="font-mono font-bold text-white mb-1"><code>name</code> (Identifier Constraint)</div>
    <p class="text-gray-400 leading-relaxed">
      A unique, lowercase, hyphenated identifier that <strong>must match the parent directory name</strong>.
    </p>
  </div>
  <div class="p-4 rounded-xl bg-gray-900 border border-gray-800">
    <div class="font-mono font-bold text-cyan-300 mb-1"><code>description</code> (The Routing Trigger)</div>
    <p class="text-gray-400 leading-relaxed">
      The <strong>primary activation trigger</strong> loaded at startup. The agent matches user prompts against this text to decide whether to load the full skill.
    </p>
  </div>
</div>

<!--
The YAML frontmatter provides the skill's identity and activation trigger. Because only name and description are loaded into context at session startup, the description must clearly specify domain keywords and explicit "Use when..." conditions.
-->

---
layout: default
---

<!-- S1-08 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Inside SKILL.md Part 2: The Important Stuff</h2>
</div>

<div class="grid grid-cols-2 gap-5 mt-6">
  <div class="p-5 rounded-xl bg-gray-900 border border-gray-800 space-y-3">
    <div class="text-xs font-mono text-cyan-300 uppercase">1. Runbook Procedures</div>
    <p class="text-xs text-gray-300 leading-relaxed">
      Step-by-step operational workflows, domain rules, and verification criteria the agent follows from start to finish:
    </p>

```markdown
## Review Workflow
1. Run the static analysis script on changed files.
2. Check changes against the project style guide.
3. Summarise findings using the report template.
```

  </div>

  <div class="p-5 rounded-xl bg-gray-900 border border-gray-800 space-y-3">
    <div class="text-xs font-mono text-emerald-300 uppercase">2. Pointers to Scripts &amp; References</div>
    <p class="text-xs text-gray-300 leading-relaxed">
      Relative links to executable utilities and deep reference documentation housed inside the skill directory:
    </p>

```markdown
## Bundled Resources
* Linter script:
  [`scripts/run_linter.py`](scripts/run_linter.py)
* Style guide:
  [`references/style_guide.md`](references/style_guide.md)
```

  </div>
</div>

<!--
Once triggered, the markdown body of SKILL.md acts as the agent's operational runbook. It contains the key step-by-step procedures for the task alongside direct relative pointers to additional resources housed within the skill—like helper scripts in `scripts/` and deep documentation in `references/`.
-->

---
layout: default
---

<!-- S1-09 -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">The 3-Tier Progressive Disclosure Model</h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white">Tier 1 &middot; Discovery (~100 Tokens, Always Loaded)</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>At session start, only <code>name</code> and <code>description</code> from each skill's YAML frontmatter are injected</li>
      <li>Acts as a lightweight semantic index without consuming working memory</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Tier 2 &middot; Activation (&lt; 5,000 Tokens, Loaded When Relevant)</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>When the user's task matches a skill's description, the agent reads <code>SKILL.md</code> into working memory</li>
      <li>Provides the primary procedural workflow, negative constraints, and relative links</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Tier 3 &middot; Execution (On-Demand Files, Loaded Per Sub-Task)</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>The agent selectively reads <code>references/*.md</code>, uses templates in <code>resources/</code>, or executes <code>scripts/*.py</code></li>
      <li>Executable code runs in the terminal rather than bloating the prompt context</li>
    </ul>
  </li>
</ol>

<!--
This 3-tier progressive disclosure model is why we can have 40+ skills installed in a workspace without blowing up the context window: 100 tokens at Tier 1, SKILL.md at Tier 2, and deep reference files or scripts at Tier 3.
-->

---
layout: default
---

<!-- S1-10 -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Authoring Skills with Agent Skills</h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white">Phase 1 &middot; Exploration &amp; Problem Solving</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Solve an unfamiliar task, research an API, or debug a tricky workflow interactively in the workspace</li>
      <li>Iterate until commands, scripts, and edge-case fixes are thoroughly tested and proven</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Phase 2 &middot; Synthesis with Built-In Customisation Skill</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Prompt the agent: <code>"/agy-customize Please convert this into an agent skill"</code></li>
      <li>The agent structures <code>SKILL.md</code>, formats YAML frontmatter, and isolates deep context into <code>scripts/</code> or <code>references/</code></li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Phase 3 &middot; Test in a Clean Session</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Start a brand-new conversation with an empty context window to simulate a real user prompt</li>
      <li>Verify that semantic routing activates Tier 1 and the agent executes Tier 2 and 3 without human intervention</li>
    </ul>
  </li>
</ol>

<div class="mt-6 p-3.5 rounded-lg bg-gray-900/40 border border-gray-800/80 text-center text-sm text-gray-300">
  You don't need to write the skill <strong>by hand</strong>!
</div>

<!--
Best of all, you don't have to hand-author every line of SKILL.md. We use Antigravity's built-in `agy-customizations` skill—invoked via `/agy-customize`—which knows the standard directory anatomy, YAML frontmatter rules, and discovery roots out of the box. The workflow is simple: first, solve the problem interactively in the terminal; second, tell the agent `/agy-customize Please convert this into an agent skill`; third, verify it in a brand-new conversation to prove it works from cold storage. Now let's look at Way 1: Ecosystem and Plugin Skills!
-->
