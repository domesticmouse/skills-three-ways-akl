---
id: step-1
step: 1
title: Way 1 · Ecosystem & Plugin Skills
way: 1
duration: "~10 min"
slide: "S2-03"
slidePath: "./slides/#/17"
checkpoint: "codelab/start"
summary: "Bootstrap find-skills, enable official Google Antigravity SDK and EGM review plugins, and verify their skills and subagent personas."
---

When you start a fresh project with a fast-moving SDK, the fastest way to keep an agent grounded is **Way 1: Ecosystem & Plugin Skills**. Official plugins pair up-to-date API runbooks with specialist subagents, bundled as a single installable unit via `/plugin`.

## 1. Install `find-skills` Globally

First, exit `agy` if it is still open (`Ctrl+D` twice) and install Vercel Labs' `find-skills` skill globally so it is ready when we move into Way 2 in Lab 2:

```bash label="Lab 1 · Install find-skills globally"
npx skills add vercel-labs/skills@find-skills -g -y
```

Now launch `agy` again from your project root:

```bash label="Lab 1 · Launch agy for plugin setup"
agy
```

## 2. Enable the Two Core Way 1 Plugins

Inside `agy`, run the interactive plugin manager:

```prompt label="Lab 1 · Open plugin manager"
/plugin
```

In the `/plugin` menu, enable these two official plugins for this workspace:

1. **Google Antigravity SDK** (`google-antigravity-sdk` — catalog ID `antigravity-plugins-official/plugin/google-antigravity-sdk`): Ships current Python SDK patterns (`Agent`, `LocalAgentConfig`, `skills_paths`, `policy`, `BudgetConfig`) so the coding agent does not hallucinate deprecated APIs.
2. **Elephant-Goldfish Model** (`egm` — catalog ID `antigravity-plugins-official/plugin/egm`): Ships isolated specialist review subagents (`egm-design`, `egm-zoom-out`, `egm-codebase-details`, `egm-implementation-readiness`).

:::callout tip Optional Bonus Plugins (Skip If Short on Time)
When building web UIs or deploying to Google Cloud in your own projects, you can also explore `chrome-devtools-plugin`, `google-developer-knowledge`, `modern-web-guidance-plugin`, and `google-cloud-developer`. For this 90-minute codelab, **only `google-antigravity-sdk` and `egm` are required**—keeping setup fast and your Tier 1 discovery list lean.
:::

Close the `/plugin` menu and wait until `agy` finishes reloading plugins and settles back at the empty `>` prompt (`? for shortcuts`).

## 3. Verify What Way 1 Just Added

Paste this prompt into `agy` to confirm both plugins are active and inspect what capabilities they expose:

```prompt label="Lab 1 · Verify Way 1 plugins and subagents"
Please check that the Google Antigravity SDK plugin (google-antigravity-sdk) and the EGM review subagents are enabled for this workspace, and show me what skills and specialist agents they provide.
```

### What to Notice While `agy` Responds

- **`LocalAgentConfig` & `skills_paths`**: Instead of shelling out to a CLI subprocess, our Python app can embed an `Agent` directly in-process and mount the exact same `.agents/skills` directory.
- **Least-privilege policies**: Look for `policy.deny_all()`, explicit `policy.allow(...)`, and `types.BudgetConfig`—crucial for a read-only TUI agent.
- **Independent critic personas**: Coding agents are famously optimistic about their own designs. The four **EGM** subagents run in fresh context windows without inheriting the author's confirmation bias.

:::details Troubleshooting Lab 1 Plugins
- **Plugins do not appear immediately after enabling**: Wait a few seconds for plugin reload, or exit `agy` (`Ctrl+D` twice) and start a fresh `agy` session so Tier 1 discovery refreshes.
- **Network error during `npx skills add`**: Accept any sandbox network prompt if running inside an agent harness, or run the `npx` command directly in your regular shell.
:::

## Lab 1 Checklist

:::checklist
- [ ] `npx skills add vercel-labs/skills@find-skills -g -y` succeeded.
- [ ] `google-antigravity-sdk` and `egm` enabled via `/plugin`.
- [ ] `agy` verified the SDK primitives and listed the four `egm-*` specialist subagents.
:::
