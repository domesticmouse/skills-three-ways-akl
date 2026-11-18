---
layout: center
class: text-center
---

<!-- S3-01 -->
<div class="space-y-4">
  <h1 class="text-4xl font-extrabold text-white">
    Way 2 &middot; Community Workflow Skills
  </h1>
  <p class="text-xl font-mono text-cyan-300">
    find-skills &middot; wshobson/agents &middot; egm-review-cycles
  </p>
  <p class="text-base text-gray-400 max-w-xl mx-auto">
    Discovering, vetting, and pairing community Python skills with EGM review passes to architect Brain Explorer
  </p>
</div>

<!--
That brings us to Way 2: Community Workflow Skills. Once you have your core platform plugins enabled, you don't need to reinvent standard language or framework conventions from scratch. The open-source skills ecosystem already has hundreds of community packages—provided you know how to discover them, evaluate their quality, and spot where the community still has gaps.
-->

---
layout: default
---

<!-- S3-02 -->
<div class="flex items-center gap-3 mb-6">
  <h2 class="text-2xl font-bold m-0">Evaluating Community Skills with <code>find-skills</code></h2>
</div>

<ol class="space-y-4 text-sm text-gray-200 list-decimal pl-6 mt-5 leading-relaxed">
  <li>
    <strong class="text-white">Discovery via <code>npx skills find</code></strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Search the open skills registry directly from the terminal or through <code>agy</code> using domain keywords (<code>python</code>, <code>textual</code>)</li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Trust &amp; Quality Signals Before Installing</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>Inspect install counts, GitHub stars, repository provenance, and security scan signals rather than blindly pulling arbitrary prompts into <code>.agents/skills/</code></li>
    </ul>
  </li>
  <li>
    <strong class="text-white">Spotting Ecosystem Coverage Gaps</strong>
    <ul class="list-disc pl-5 mt-1 space-y-1 text-gray-300">
      <li>High-adoption packs like <code>wshobson/agents</code> cover core Python engineering (<code>uv</code>, <code>mypy</code>, <code>asyncio</code>, <code>pytest</code>)</li>
      <li>Niche combinations like Textual TUI + A2UI v1.0 have zero mature community skills</li>
    </ul>
  </li>
</ol>

<!--
Remember how we installed `find-skills` in Act 2? Because `find-skills` is itself a skill, we can simply ask Antigravity to search the community registry for Python and Textual TUI skills. When evaluating community skills, we look at three things: first, searching by stack keywords with `npx skills find`; second, checking install counts, GitHub stars, and security scan results on `skills.sh` before anything touches our repository; and third, paying close attention to what isn't there—because an empty search result tells you ahead of time where your agent is going to rely on raw training weights and where you will likely need a bespoke Way 3 skill.
-->

---
layout: cast-full
title: "Searching Python & Textual Skills and Installing wshobson/agents"
cast: /casts/way-2-find-skills.cast
autoPlay: false
speed: 2.0
idleTimeLimit: 2.0
fit: both
---

<!-- S3-03 -->
<div class="w-full max-w-4xl mx-auto p-5 rounded-xl bg-[#1a1b26] border border-amber-500/30 shadow-2xl space-y-4">
  <div class="flex items-start justify-between gap-4 pb-3 border-b border-gray-800">
    <div>
      <div class="text-xs font-mono text-amber-400 uppercase tracking-wider">Trajectory 2 &middot; Way 2 Skill Evaluation</div>
      <h3 class="text-lg font-bold text-white mt-0.5 m-0">Searching Python &amp; Textual Skills and Installing wshobson/agents</h3>
      <div class="text-xs font-mono text-gray-400 mt-1">Target cast: <code>/casts/way-2-find-skills.cast</code></div>
    </div>
    <span class="shrink-0 px-2.5 py-1 rounded-full text-xs font-mono border border-amber-500/40 bg-amber-500/10 text-amber-300">
      CAST Placeholder &middot; 4 Stop Points (m1&ndash;m4)
    </span>
  </div>
  <div class="space-y-3 text-xs font-mono">
    <div class="p-3.5 rounded-lg bg-[#121317] border border-gray-800/80 space-y-1.5">
      <div class="text-amber-300 font-semibold">m1 &rarr; m2 &middot; Before / After: Search Python &amp; Textual skills prompt</div>
      <div class="text-gray-400">m1: <code>agy</code> prompt box empty</div>
      <div class="text-gray-200 leading-relaxed">m2: <code>We want to build Brain Explorer&mdash;a Python CLI and Textual TUI powered by the Google Antigravity SDK to inspect our ~/.gemini session trajectories. Use find-skills to search for Python and Textual TUI skills.</code></div>
    </div>
    <div class="p-3.5 rounded-lg bg-[#121317] border border-gray-800/80 space-y-1.5">
      <div class="text-amber-300 font-semibold">m3 &rarr; m4 &middot; Before / After: Install wshobson/agents Python skills prompt</div>
      <div class="text-gray-400">m3: <code>npx skills find python</code> and <code>npx skills find textual</code> evaluation complete; prompt box ready</div>
      <div class="text-gray-200 leading-relaxed">m4: <code>Let's install the Python development skills from wshobson/agents into this repo so our agents follow uv, strict typing, async, and testing conventions.</code></div>
    </div>
  </div>
  <div class="text-[11px] font-mono text-gray-500 pt-1">
    Awaiting <code>recordings/final/way-2-find-skills.cast</code> &mdash; switches automatically to <code>asciinema-player</code> once synced.
  </div>
</div>

<!--
Let's watch this play out in `way-2-find-skills.cast`. At our first prompt stop point, we tell Antigravity we want to build Brain Explorer—a Python CLI and Textual TUI powered by the Google Antigravity SDK—and ask it to use `find-skills` to search for Python and Textual skills. It runs `npx skills find python` and `npx skills find textual`, surfaces the `wshobson/agents` Python development suite along with its install counts and repository metrics, and flags that there are no dedicated skills covering Textual TUIs with A2UI v1.0. At our second prompt stop point, we ask Antigravity to install the Python skills from `wshobson/agents` into the repo, populating `.agents/skills/` and locking their hashes in `skills-lock.json`.
-->

---
layout: skill-breakdown
way: 2
title: "What We Installed vs. The Gap We Found"
---

<!-- S3-04 -->
<div class="space-y-4">

```text
.agents/skills/ (17 wshobson/agents Python skills locked in skills-lock.json)
├── uv-package-manager          ├── python-type-safety          ├── async-python-patterns
├── python-project-structure    ├── python-design-patterns      ├── python-code-style
├── python-error-handling       ├── python-testing-patterns     └── ... (9 more Python skills)

Coverage Gap Surfaced by `npx skills find textual`:
└── 0 skills for Textualize (Textual 8+) widget lifecycle + A2UI v1.0 generative surfaces
```

  <div class="grid grid-cols-2 gap-4 text-xs pt-2">
    <div class="p-3 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-amber-300 font-semibold">Strong Python Foundation:</span> Every agent turn now follows <code>uv run</code>, strict <code>mypy</code>, <code>ruff</code>, <code>pytest</code>, and clean separation of concerns automatically.
    </div>
    <div class="p-3 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-amber-300 font-semibold">Known Frontier Risk:</span> Because no community skill covers Textual 8+ with A2UI v1.0, we lean on our Way 1 <strong>EGM</strong> reviewers to catch integration traps during the build.
    </div>
  </div>
</div>

<!--
Here is the snapshot of our workspace after that command finishes. On the top, we have 17 battle-tested Python skills from `wshobson/agents` wired into `.agents/skills/` and pinned in `skills-lock.json`—covering `uv-package-manager`, `python-project-structure`, `python-type-safety`, `async-python-patterns`, `python-testing-patterns`, and more. On the bottom is the gap `find-skills` exposed: zero community skills for wiring A2UI v1.0 generative surfaces into Textual 8+. Knowing that gap exists before we start coding is gold, because it tells us exactly where to point our EGM review subagents.
-->

---
layout: default
---

<!-- S3-05 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">EGM Cycle 1: Naive Full-Delegation vs. Hybrid Architecture</h2>
</div>

<div class="grid grid-cols-2 gap-6 mt-6">
  <div class="p-5 rounded-xl bg-red-950/15 border border-red-500/30 space-y-3">
    <div class="text-xs font-mono text-red-400 uppercase">Anti-Pattern: Naive First Draft</div>
    <h3 class="text-lg font-bold text-white">Delegating Every TUI Action to an In-Process LLM Agent</h3>
    <ul class="text-xs text-gray-300 space-y-2 list-disc pl-4">
      <li>Spawns an LLM agent turn just to list <code>~/.gemini/**/brain/</code> directories or count Skill Activations</li>
      <li>Seconds of latency and token burn on every keypress inside the TUI</li>
      <li>Unbounded tool policy risks mutating or polluting the developer's own <code>~/.gemini</code> trajectories</li>
      <li><strong>Result:</strong> Sluggish TUI that contaminates the very dataset it inspects.</li>
    </ul>
  </div>
  <div class="p-5 rounded-xl bg-emerald-950/15 border border-emerald-500/30 space-y-3">
    <div class="text-xs font-mono text-emerald-400 uppercase">The Solution: EGM Cycle 1 Hybrid Architecture</div>
    <h3 class="text-lg font-bold text-white">Deterministic Local TrajectoryStore + Isolated Read-Only AgentService</h3>
    <ul class="text-xs text-gray-300 space-y-2 list-disc pl-4">
      <li><code>TrajectoryStore</code> parses <code>transcript.jsonl</code> &amp; <code>transcript_full.jsonl</code> locally in milliseconds</li>
      <li>Classifies Skill Activations (<code>way_1_plugin</code>, <code>way_2_community</code>, <code>way_3_bespoke</code>) deterministically</li>
      <li>In-process <code>AgentService</code> invoked only on explicit <code>/</code> user prompts to compose A2UI v1.0 comparison surfaces</li>
      <li><strong>Result:</strong> Instant local TUI navigation paired with isolated, read-only generative UI synthesis.</li>
    </ul>
  </div>
</div>

<!--
When we asked Antigravity to draft the initial architecture for Brain Explorer and immediately ran our first EGM review pass, `egm-design` and `egm-zoom-out` caught a classic agent-first anti-pattern right away. The naive design on the left wanted to route every TUI interaction through the in-process LLM agent—even listing `~/.gemini` directories and counting Skill Activations. That would mean multi-second latency on every keystroke and, worse, each inspection query would write a new session trajectory back into `~/.gemini`, polluting the dataset we were trying to inspect! On the right is the hybrid architecture EGM Cycle 1 forced us into: a fast, deterministic local `TrajectoryStore` that parses `transcript.jsonl` and classifies Skill Activations in milliseconds, paired with an isolated, read-only `AgentService` that redirects its `app_data_dir` outside `~/.gemini` and only runs when you press `/` to ask for a generative A2UI v1.0 surface.
-->

---
layout: cast-full
title: "Two-Pass EGM Architecture & Implementation Review"
cast: /casts/way-2-egm-cycle.cast
autoPlay: false
speed: 2.0
idleTimeLimit: 2.0
fit: both
---

<!-- S3-06 -->
<div class="w-full max-w-4xl mx-auto p-5 rounded-xl bg-[#1a1b26] border border-purple-500/30 shadow-2xl space-y-4">
  <div class="flex items-start justify-between gap-4 pb-3 border-b border-gray-800">
    <div>
      <div class="text-xs font-mono text-purple-400 uppercase tracking-wider">Trajectory 3 &middot; Two-Pass EGM Build Cycle (+ 8 EGM Subagents)</div>
      <h3 class="text-lg font-bold text-white mt-0.5 m-0">Two-Pass EGM Architecture &amp; Implementation Review</h3>
      <div class="text-xs font-mono text-gray-400 mt-1">Target cast: <code>/casts/way-2-egm-cycle.cast</code></div>
    </div>
    <span class="shrink-0 px-2.5 py-1 rounded-full text-xs font-mono border border-amber-500/40 bg-amber-500/10 text-amber-300">
      CAST Placeholder &middot; 4 Stop Points (m1&ndash;m4)
    </span>
  </div>
  <div class="space-y-3 text-xs font-mono">
    <div class="p-3.5 rounded-lg bg-[#121317] border border-gray-800/80 space-y-1.5">
      <div class="text-purple-300 font-semibold">m1 &rarr; m2 &middot; Before / After: Cycle 1 design &amp; EGM audit prompt</div>
      <div class="text-gray-400">m1: <code>agy</code> prompt box empty</div>
      <div class="text-gray-200 leading-relaxed">m2: <code>Using google-antigravity-sdk, agy-brain-explorer, and our Python skills, design a Brain Explorer Python CLI and Textual TUI that inspects ~/.gemini session trajectories and skill activations, then run an EGM review cycle (egm-design, egm-zoom-out, egm-codebase-details, egm-implementation-readiness) on the design.</code></div>
    </div>
    <div class="p-3.5 rounded-lg bg-[#121317] border border-gray-800/80 space-y-1.5">
      <div class="text-purple-300 font-semibold">m3 &rarr; m4 &middot; Before / After: Cycle 2 implement &amp; EGM audit prompt</div>
      <div class="text-gray-400">m3: Cycle 1 resolution summary rendered; prompt box ready</div>
      <div class="text-gray-200 leading-relaxed">m4: <code>Implement the hybrid TrajectoryStore, isolated AgentService, and Textual A2UI v1.0 renderer, then run a second EGM review pass and verify with ruff, mypy, and pytest.</code></div>
    </div>
  </div>
  <div class="text-[11px] font-mono text-gray-500 pt-1">
    Awaiting <code>recordings/final/way-2-egm-cycle.cast</code> &mdash; switches automatically to <code>asciinema-player</code> once synced.
  </div>
</div>

<!--
Let's watch both EGM cycles in `way-2-egm-cycle.cast`. At our first prompt stop point, we ask Antigravity to design Brain Explorer using `google-antigravity-sdk`, `agy-brain-explorer`, and our `wshobson/agents` Python skills, and then run an EGM review pass before writing implementation code. You can see the four EGM subagents fan out and converge on the hybrid `TrajectoryStore` plus isolated `AgentService` split. At our second prompt stop point, we tell Antigravity to implement the hybrid store, the isolated SDK agent, and the Textual A2UI v1.0 renderer, and then run a second EGM review pass verified with `ruff`, `mypy`, and `pytest`. Watch how Cycle 2 surfaces ten concrete A2UI v1.0 and Textual 8+ integration bugs—and resolves every single one until the test suite turns green.
-->

---
layout: skill-breakdown
way: mashup
title: "EGM Cycle 2 Part 1: A2UI v1.0 Protocol &amp; Schema Traps"
---

<!-- S3-07 -->
<div class="space-y-4">

```python
# Trap 1: v1.0 DataBinding requires "@path", EXCEPT TemplateChildList which still uses "path"
if data_ctx.at_least_v10 and "path" in template_spec:
    resolved_list = data_ctx.resolve_dynamic_value({"@path": template_spec["path"]})

# Trap 2: v1.0 STRICT_VALIDATION only allows Text.variant in {"body", "caption"}
# ("h1".."h5" fail validation -> use Markdown headings inside "text" instead)

# Trap 3: Stage-validate on a throwaway MessageProcessor before touching the live surface
staging = MessageProcessor([catalog], options=MessageProcessorOptions(validation_config=STRICT_VALIDATION))
staging.process_messages(raw_messages)  # Raises A2uiError without wiping active UI
```

  <div class="grid grid-cols-2 gap-4 text-xs pt-2">
    <div class="p-3 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-purple-300 font-semibold">v0.9 vs v1.0 Drift:</span> Without a skill, the LLM mixes v0.9 <code>"path"</code> and <code>h1</code>&ndash;<code>h5</code> variants into v1.0 payloads, failing <code>STRICT_VALIDATION</code>.
    </div>
    <div class="p-3 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-purple-300 font-semibold">Atomic Staging Processor:</span> Validating on a throwaway <code>MessageProcessor</code> prevents a malformed agent turn from blanking the user's live TUI surface.
    </div>
  </div>
</div>

<!--
Let's unpack what those EGM Cycle 2 reviewers and our `pytest` suite actually caught—because this is where the missing Textual and A2UI v1.0 skill bit us during the Exploratory Run. First, A2UI v1.0 changed `DataBinding` syntax from `"path"` to `"@path"`, except inside `TemplateChildList`, which still keys the collection path under `"path"`. Second, under v1.0 `STRICT_VALIDATION`, `Text.variant` only permits `"body"` and `"caption"`—using `"h1"` through `"h5"` crashes validation. And third, if you feed raw agent messages straight into your live `MessageProcessor`, a single malformed turn wipes out the existing surface or triggers `A2uiIntegrityError` on duplicate `createSurface` IDs. Creating a throwaway staging `MessageProcessor` first keeps the live UI rock-solid.
-->

---
layout: skill-breakdown
way: mashup
title: "EGM Cycle 2 Part 2: Textual Widget &amp; Runtime Isolation Traps"
---

<!-- S3-08 -->
<div class="space-y-4">

```python
# Trap 4: Textual 8+ Select uses Select.NULL (not Select.BLANK) & ChoicePicker binds list[str]
select_val = current[0] if current else Select.NULL

# Trap 5: Resolve Button action bindings at click time, NEVER at render time
def on_button_pressed(self, event: Button.Pressed) -> None:
    payload = event.button.data_context.resolve_action(event.button.raw_action)

# Trap 6: Strip SDK StreamHandlers (preserving FileHandlers) so stderr never corrupts Textual
for h in list(logger.handlers):
    if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler):
        logger.removeHandler(h)
```

  <div class="grid grid-cols-2 gap-4 text-xs pt-2">
    <div class="p-3 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-purple-300 font-semibold">Live Two-Way Binding:</span> Resolving <code>resolve_action</code> inside <code>on_button_pressed</code> ensures user edits in <code>Input</code>, <code>Checkbox</code>, and <code>Select</code> flow into action payloads.
    </div>
    <div class="p-3 rounded-lg bg-gray-900/80 border border-gray-800">
      <span class="text-purple-300 font-semibold">Terminal Buffer Hygiene:</span> Passing <code>Static(..., markup=False)</code> and stripping console <code>StreamHandler</code> instances stops JSON brackets and SDK logs from tearing the TUI.
    </div>
  </div>
</div>

<!--
The second half of the Cycle 2 findings lived at the seam between A2UI, Textual 8+, and the in-process Antigravity SDK. Textual 8 replaced `Select.BLANK` with `Select.NULL`, while A2UI's `ChoicePicker` expects a `list[str]` rather than a scalar string. Even subtler: if you call `data_context.resolve_action(...)` while building the `Button` widget, you freeze the initial form state and ignore everything the user types into inputs or dropdowns afterwards—you have to store the `DataContext` on the button and resolve the action inside `on_button_pressed`. Finally, the in-process SDK attaches console `StreamHandler` loggers to `google.antigravity` and `absl` that write straight to `stderr` and corrupt Textual's alternate screen buffer unless you strip non-file stream handlers before launch. Fixing all ten of these traps took real detective work—which sets up our big question for Act 4: how do we make sure no agent in our repo ever hits those ten traps again?
-->
