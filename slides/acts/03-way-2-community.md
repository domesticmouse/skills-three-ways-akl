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
layout: lab-step
step: "Lab 2"
way: 2
duration: "~10 min"
title: "Searching &amp; Installing Community Skills"
codelabAnchor: "#step-2"
checkpoint: "codelab/checkpoint-2-skills"
---

<!-- S3-03 -->

<PromptCard
  kind="prompt"
  way="2"
  label="1. Search Python &amp; Textual skills via find-skills"
  text="We want to build Brain Explorer—a Python CLI and Textual TUI powered by the Google Antigravity SDK to inspect our ~/.gemini session trajectories. Use find-skills to search for Python and Textual TUI skills."
/>

<PromptCard
  kind="prompt"
  way="2"
  label="2. Install wshobson/agents Python skills"
  text="Let's install the Python development skills from wshobson/agents into this repo so our agents follow uv, strict typing, async, and testing conventions."
/>

::verify::

<ul class="list-disc pl-4 space-y-1.5">
  <li><code>npx skills find python</code> surfaces <code>wshobson/agents</code> with install &amp; trust signals.</li>
  <li><code>npx skills find textual</code> returns zero mature skills for Textual + A2UI v1.0.</li>
  <li><code>.agents/skills/</code> and <code>skills-lock.json</code> are populated cleanly on disk.</li>
</ul>

<!--
Start Lab 2 now. First, tell Antigravity you want to build Brain Explorer and ask it to search `find-skills` for Python and Textual skills. Notice what comes back: rich Python coverage from `wshobson/agents`, and zero dedicated skills for Textual TUIs with A2UI v1.0. Then paste the second prompt to install the Python suite into `.agents/skills/` and lock their hashes in `skills-lock.json`.
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
Here is the workspace snapshot once Lab 2 finishes. On the top, 17 battle-tested Python skills from `wshobson/agents` live in `.agents/skills/` and are pinned in `skills-lock.json`—covering `uv-package-manager`, `python-project-structure`, `python-type-safety`, `async-python-patterns`, `python-testing-patterns`, and more. On the bottom is the gap `find-skills` exposed: zero community skills for wiring A2UI v1.0 generative surfaces into Textual 8+. Knowing that gap exists before we start coding tells us right where to point our EGM review subagents in Lab 3.
-->

---
layout: default
---

<!-- S3-05 -->
<div class="flex items-center gap-3 mb-4">
  <h2 class="text-2xl font-bold m-0">Reference Pattern &middot; EGM Cycle 1: Naive vs. Hybrid Architecture</h2>
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
In Lab 3 Part A, you are going to ask Antigravity to design Brain Explorer and run an EGM review pass before writing code. Keep an eye out for a classic agent-first anti-pattern that `egm-design` and `egm-zoom-out` caught right away in our reference run. The naive design on the left wanted to route every TUI interaction through the in-process LLM agent—even listing `~/.gemini` directories and counting Skill Activations. That adds multi-second latency on every keystroke and writes new session trajectories straight back into `~/.gemini`, polluting the very dataset you are inspecting! On the right is the hybrid architecture EGM Cycle 1 pushed us into: a fast, deterministic local `TrajectoryStore` paired with an isolated, read-only `AgentService` that redirects `app_data_dir` outside `~/.gemini`.
-->

---
layout: lab-step
step: "Lab 3"
way: 2
duration: "~30 min"
title: "Two-Pass EGM Architecture &amp; Build Cycle"
codelabAnchor: "#step-3"
checkpoint: "codelab/checkpoint-3-brain-explorer"
---

<!-- S3-06 -->

<PromptCard
  kind="prompt"
  way="2"
  label="Part A (~10 min) · Cycle 1 design &amp; EGM audit"
  text="Using google-antigravity-sdk, agy-brain-explorer, and our Python skills, design a Brain Explorer Python CLI and Textual TUI that inspects ~/.gemini session trajectories and skill activations, then run an EGM review cycle (egm-design, egm-zoom-out, egm-codebase-details, egm-implementation-readiness) on the design."
/>

<PromptCard
  kind="prompt"
  way="2"
  label="Part B Path 1 (~20 min) · Cycle 2 implement, audit &amp; verify"
  text="Implement the hybrid TrajectoryStore, isolated AgentService, and Textual A2UI v1.0 renderer, then run a second EGM review pass and verify with ruff, mypy, and pytest."
/>

<div class="p-3 rounded-xl bg-gray-900/70 border border-gray-800 text-xs text-gray-300">
  <strong class="text-amber-300">Short on time or API quota for Part B?</strong> Follow <strong>Path 2 (Fast Track)</strong> in the codelab: check out <code>codelab/checkpoint-3-brain-explorer</code>, run <code>uv sync &amp;&amp; uv run pytest -v</code>, and ask <code>egm-codebase-details</code> to audit the reference traps.
</div>

::verify::

<ul class="list-disc pl-4 space-y-1.5">
  <li>Cycle 1 produces the Hybrid split (deterministic <code>TrajectoryStore</code> + isolated <code>AgentService</code>).</li>
  <li>Part B completes either via Path 1 (Full Build) or Path 2 (Fast Track checkpoint).</li>
  <li><code>uv run ruff check src tests</code>, <code>uv run mypy src</code>, and <code>uv run pytest -v</code> all pass.</li>
</ul>

<!--
Lab 3 is the big 30-minute build block, split into two parts. Everyone runs Part A (~10 minutes): paste the Cycle 1 prompt and watch the four EGM subagents fan out and critique your initial architecture. For Part B (~20 minutes), choose your own adventure in the codelab: either run the full Cycle 2 implementation prompt live, or take Path 2 (Fast Track) by checking out `codelab/checkpoint-3-brain-explorer` and running `egm-codebase-details` across the finished reference files so you stay on schedule for Labs 4 and 5.
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
Compare what your agent surfaced in Cycle 2 with the protocol traps our Exploratory Run hit—because this is right where that missing Textual and A2UI v1.0 skill bit us. First, A2UI v1.0 changed `DataBinding` syntax from `"path"` to `"@path"`, except inside `TemplateChildList`, which still keys the collection path under `"path"`. Second, under v1.0 `STRICT_VALIDATION`, `Text.variant` only permits `"body"` and `"caption"`—using `"h1"` through `"h5"` crashes validation. And third, if you feed raw agent messages straight into your live `MessageProcessor`, a single malformed turn wipes out the existing surface or triggers `A2uiIntegrityError` on duplicate `createSurface` IDs. Creating a throwaway staging `MessageProcessor` first keeps the live UI rock-solid.
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
The second half of the Cycle 2 findings lived at the seam between A2UI, Textual 8+, and the in-process Antigravity SDK. Textual 8 replaced `Select.BLANK` with `Select.NULL`, while A2UI's `ChoicePicker` expects a `list[str]` rather than a scalar string. Even subtler: if you call `data_context.resolve_action(...)` while building the `Button` widget, you freeze the initial form state and ignore everything the user types into inputs or dropdowns afterwards—you have to store the `DataContext` on the button and resolve the action inside `on_button_pressed`. Finally, the in-process SDK attaches console `StreamHandler` loggers to `google.antigravity` and `absl` that write straight to `stderr` and corrupt Textual's alternate screen buffer unless you strip non-file stream handlers before launch. Fixing all ten of these traps took real detective work—which sets up our big question for Lab 4: how do we make sure no agent in our repo ever hits those traps again?
-->
