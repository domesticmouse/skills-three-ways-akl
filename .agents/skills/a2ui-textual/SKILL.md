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

Operational runbook for wiring `a2ui-agent-sdk` and `a2ui-core` (`ProtocolVersion.V1_0`) to a Python Textualize (`Textual`) viewport driven by an in-process `google-antigravity` SDK `Agent`.

Consult [`references/a2ui-v1-textual-gotchas.md`](references/a2ui-v1-textual-gotchas.md) whenever you hit `A2uiError` / `A2uiIntegrityError`, blank template `List` components, `Select.BLANK` / `MarkupError` crashes, frozen button action contexts, or corrupted Textual terminal output.

---

## 1. Emit & Strictly Validate A2UI v1.0 Payloads (`a2ui-core` + `a2ui-agent-sdk`)

1. **Configure the v1.0 catalog and request processor**:
   ```python
   from a2ui.core.basic_catalog import BasicCatalog
   from a2ui.core.processing import MessageProcessor
   from a2ui.core.processing.message_processor import MessageProcessorOptions
   from a2ui.core.schema import ProtocolVersion
   from a2ui.core.validation import STRICT_VALIDATION
   from a2ui.inference_formats.direct_json import DirectJsonFormatFactory
   from a2ui.parser.messages import to_message_dicts
   from a2ui.parser.response_part import A2uiPart, TextPart
   from a2ui.processor import A2uiRequestProcessor

   catalog = BasicCatalog(ProtocolVersion.V1_0)
   request_processor = A2uiRequestProcessor(
       catalogs=[catalog],
       format_factory=DirectJsonFormatFactory(),
   )
   ```
2. **Instruct the agent using v1.0 semantics**:
   Append `request_processor.prompt_snippet` to `system_instructions` alongside explicit v1.0 rules:
   - Include `"version": "1.0"` on every envelope and `"catalogId": catalog.catalog_id` on `createSurface`.
   - Use `"@path"` for every `DataBinding` (v0.9 `"path"` is treated as a literal dictionary in v1.0).
   - Restrict `Text.variant` to `"body"` or `"caption"` (`h1`–`h5` variants fail `STRICT_VALIDATION`; use Markdown headings inside `text` instead).
   - Bind `ChoicePicker.value` to a `DynamicStringList` (`list[str]`), never a scalar string.
3. **Parse and stage-validate atomically**:
   - Parse model responses with `request_processor.parse_response(raw_text)` and serialise `A2uiPart.a2ui` via `to_message_dicts(part.a2ui)` (avoid manual `.model_dump()` calls).
   - Run `raw_messages` through a throwaway staging `MessageProcessor([catalog], options=MessageProcessorOptions(validation_config=STRICT_VALIDATION))` first so invalid agent turns never wipe the live surface.
   - Before applying a validated payload containing `createSurface` to the live `MessageProcessor`, delete existing surfaces via `processor.model.delete_surface(surface_id)` to avoid `A2uiIntegrityError`.

*Completion Criterion*: The staging `MessageProcessor(..., validation_config=STRICT_VALIDATION)` accepts every parsed message without raising `A2uiError`, and the live `MessageProcessor` contains the updated `SurfaceModel`.

---

## 2. Map A2UI v1.0 `BasicCatalog` Components onto Textual Widgets

1. **Resolve dynamic values and template lists**:
   - Evaluate component properties through `data_ctx.resolve_dynamic_value(raw)`.
   - Extract two-way binding paths from `raw.get("@path") or raw.get("path")`.
   - For template-driven `List`, `Column`, or `Row` children (`{"componentId": ..., "path": ...}`), `TemplateChildList` still keys the array path under `"path"`. Wrap it as `{"@path": template_path}` when `data_ctx.at_least_v10` before resolving, then spawn per-item `DataContext(surface, path=f"{abs_base}/{idx}", index=idx, parent=data_ctx)`.
2. **Map widgets safely to Textual 8+**:
   - **`Tabs`**: Construct `TabPane(title, child)` items and attach them via `tabbed.compose_add_child(pane)` before mounting (do not call `add_pane()` on an unmounted `TabbedContent`).
   - **`Text`**: Render `"caption"` with `Static(text, markup=False)` and `"body"` (or Markdown headings) with `Markdown(text)`.
   - **`ChoicePicker`**: Use `Select.NULL` (not `Select.BLANK`) for empty selection, and write `[]` or `[str(event.value)]` (`list[str]`) back via `data_context.set(...)`.
   - **`Button`**: Store `raw_action` and the item `DataContext` on the button widget and evaluate `button.data_context.resolve_action(button.raw_action)` at click time inside `on_button_pressed`—never during render—so edits in `Input`, `Checkbox`, and `Select` reach the action payload.
   - **Markup and focus hygiene**: Pass `markup=False` to every `Static` and `Label` displaying JSON, exceptions, or `[bracketed]` text, and set `AUTO_FOCUS = None` on the `App` so global bindings remain active on launch.

*Completion Criterion*: Mounting `A2UISurfaceWidget` inside a headless `App.run_test()` pilot renders resolved `@path` text, template cards, and `TabbedContent`, and editing bound controls updates the payload emitted on button press.

---

## 3. Isolate In-Process `google-antigravity` SDK Agents Inside a Textual TUI

1. **Redirect SDK logging before Textual claims the terminal**:
   Strip non-file `logging.StreamHandler` instances on `"google.antigravity"` and `"absl"` while preserving existing `logging.FileHandler` instances (`isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)`), attach a dedicated `FileHandler`, and set `propagate = False`.
2. **Isolate artifact storage and enforce least-privilege policies**:
   - Pass explicit absolute `app_data_dir` and `save_dir` paths outside `~/.gemini` to `LocalAgentConfig` so live TUI queries never pollute developer session trajectories.
   - Lock down tools with `[policy.deny_all(), policy.allow("finish"), *(policy.allow(fn.__name__) for fn in tools)]`, set `enable_subagents=False`, and enforce a `types.BudgetConfig`.
   - When loading local skills via `skills_paths`, keep built-in `view_file` (`BuiltinTools.VIEW_FILE`) allowed alongside `policy.allow("view_file")` if the agent needs to read `SKILL.md` or `references/` files on disk.
3. **Handle missing blocks and `StopReason` bounds cleanly**:
   Retry once with a targeted v1.0 repair prompt when `<a2ui-json>` is missing or fails staging validation, only if `response.stop_reason == types.StopReason.UNSPECIFIED`.

*Completion Criterion*: Running an in-process `Agent` turn from Textual leaves terminal rendering uncorrupted, creates zero sessions under `~/.gemini`, and surfaces clear `StopReason` errors when budgets trip.

---

## Verification Checklist

Run static checks and headless TUI tests after every renderer or agent service change:

```bash
uv run ruff check src tests
uv run mypy src
uv run pytest -v
```
