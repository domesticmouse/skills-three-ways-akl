# A2UI v1.0 + Textual + Antigravity SDK Gotchas

Reference catalogue of integration traps uncovered while building and reviewing **Brain Explorer** (`a2ui-core`, `a2ui-agent-sdk`, `textual`, and `google-antigravity`). Load this file when debugging validation errors, blank widgets, runtime exceptions, or terminal corruption.

---

## 1. `@path` DataBindings vs v0.9 `path` (plus `TemplateChildList`)

- **Symptom**: `Text` labels render literal strings like `"{'path': '/header'}"` and template `List` containers render zero child cards.
- **Root cause**: A2UI v1.0 changed `DataBinding` syntax from `{"path": "..."}` to `{"@path": "..."}`. Passing `{"path": "..."}` into `DataContext.resolve_dynamic_value()` returns the dictionary verbatim instead of resolving the `DataModel`. However, `TemplateChildList` (`children: {"componentId": "...", "path": "..."}`) still names its array field `"path"`.
- **Fix**:
  - Always emit `{"@path": "/..."}` for `Text`, `TextField`, `CheckBox`, `ChoicePicker`, and `Button.action.event.context` bindings.
  - Extract two-way input paths defensively via `raw.get("@path") or raw.get("path")`.
  - When expanding a template `children` dict, translate `template_path = children_spec.get("path")` into `{"@path": template_path}` if `data_ctx.at_least_v10`:
    ```python
    path_binding = {"@path": template_path} if data_ctx.at_least_v10 else {"path": template_path}
    resolved_list = _resolve_value(data_ctx, path_binding, [])
    ```

---

## 2. `TextComponent.variant` Rejects Heading Levels (`h1`–`h5`)

- **Symptom**: `STRICT_VALIDATION` rejects `Text` components carrying `"variant": "h1"` or `"h2"`.
- **Root cause**: In `a2ui-core` v1.0 `BasicCatalog`, `TextComponent.variant` only permits `"body"` or `"caption"`.
- **Fix**: Emit `"variant": "body"` or `"variant": "caption"` on every `Text` component, and express headings using Markdown prefixes (`"# Title"`, `"### Card Heading"`) inside `"text"` rendered via Textual's `Markdown` widget.

---

## 3. Silent Masking Without `STRICT_VALIDATION`

- **Symptom**: Invalid component trees, orphan references, or cyclic layouts appear to load silently and then fail or render blank widgets in Textual.
- **Root cause**: `MessageProcessor([catalog])` without `MessageProcessorOptions(validation_config=STRICT_VALIDATION)` skips strict catalog checks.
- **Fix**: Always stage and validate messages through a `STRICT_VALIDATION` processor before applying them to the active UI surface:
  ```python
  staging = MessageProcessor(
      [catalog],
      options=MessageProcessorOptions(validation_config=STRICT_VALIDATION),
  )
  staging.process_messages(raw_messages)
  ```

---

## 4. `A2uiIntegrityError` on Duplicate `createSurface`

- **Symptom**: Generating a second surface reusing an existing `surfaceId` raises `A2uiIntegrityError`.
- **Root cause**: `MessageProcessor` forbids re-creating an already registered `surfaceId`.
- **Fix**: After staging validation passes, delete existing surfaces whenever incoming messages include `createSurface`:
  ```python
  if any(isinstance(m.get("createSurface"), dict) for m in raw_messages):
      for existing_id in list(processor.model.surfaces_map):
          processor.model.delete_surface(existing_id)
  processor.process_messages(raw_messages)
  ```

---

## 5. Click-Time Action Context Evaluation (`DataContext.resolve_action`)

- **Symptom**: Clicking a `Button` after typing into a bound `TextField`, toggling a `CheckBox`, or picking a `ChoicePicker` option sends stale initial values to the agent.
- **Root cause**: Calling `data_ctx.resolve_action(raw_action)` while building widgets freezes values at render time.
- **Fix**: Store `raw_action` and `data_context` on the custom `Button` subclass and resolve `button.data_context.resolve_action(button.raw_action)` inside `on_button_pressed`.

---

## 6. `TabbedContent.compose_add_child` During Off-Mount Widget Assembly

- **Symptom**: Mounting `Tabs` raises lifecycle or mounting errors when panes are added before the `TabbedContent` widget is mounted.
- **Root cause**: `TabbedContent.add_pane()` expects a mounted widget tree.
- **Fix**: Build panes off-mount using `tabbed.compose_add_child(TabPane(title, pane_child))` and let Textual mount them cleanly with the parent container.

---

## 7. `Select.NULL` vs `Select.BLANK` & `DynamicStringList` (`list[str]`)

- **Symptom**: `AttributeError: type object 'Select' has no attribute 'BLANK'` or schema validation failures when updating `ChoicePicker.value`.
- **Root cause**: Textual 8+ uses `Select.NULL` for empty selections (not `Select.BLANK`), and A2UI v1.0 models `ChoicePickerComponent.value` as a `DynamicStringList` (`list[str]`), not a scalar string.
- **Fix**:
  ```python
  selected: list[str] = [] if event.value is Select.NULL else [str(event.value)]
  event.select.data_context.set(event.select.bound_path, selected)
  ```

---

## 8. `Static(markup=False)` & `AUTO_FOCUS = None` in Textual

- **Symptom**: Rendering raw JSON, `[way_3_bespoke]` tags, `[/SKILL]` strings, or Python exception messages crashes with `rich.errors.MarkupError`; global shortcuts like `/` or `Ctrl+B` are swallowed by an input widget on launch.
- **Root cause**: `Static` and `Label` default to `markup=True`, interpreting square brackets as Rich style tags, and Textual's default auto-focus targets the first focusable input.
- **Fix**: Pass `markup=False` to every `Static` and `Label` showing dynamic/raw text (and use `rich.markup.escape` in CLI tables), and declare `AUTO_FOCUS = None` on the `App` class.

---

## 9. `logging.FileHandler` Is a Subclass of `logging.StreamHandler`

- **Symptom**: Log redirection strips your own `FileHandler`, or calling `configure_sdk_logging()` twice duplicates log lines while failing to silence console output that corrupts Textual's alternate screen.
- **Root cause**: In Python's standard library, `issubclass(logging.FileHandler, logging.StreamHandler)` is `True`. Filtering out `isinstance(h, logging.StreamHandler)` removes `FileHandler` too.
- **Fix**: Explicitly preserve `FileHandler` instances and deduplicate by target path:
  ```python
  if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
      continue
  ```

---

## 10. `app_data_dir` / `save_dir` Isolation, Read-Only Policies, & `StopReason` Retries

- **Symptom**: Running an embedded `google-antigravity` `Agent` inside **Brain Explorer** creates spurious session folders inside `~/.gemini/`, exposes `view_file` or write tools unexpectedly, or wastes budget retrying after hitting `MAX_MODEL_CALLS_EXCEEDED`.
- **Root cause**: Default `LocalAgentConfig()` writes artifacts to `~/.gemini/antigravity/brain/`, enables all built-in tools except `run_command`, and omits budget/stop checks.
- **Fix**:
  - Pass explicit resolved absolute paths for `app_data_dir` and `save_dir` outside `~/.gemini`.
  - Pair `policy.deny_all()` with explicit `policy.allow(...)` entries and `capabilities=types.CapabilitiesConfig(enabled_tools=[types.BuiltinTools.FINISH], enable_subagents=False)` (plus `BuiltinTools.VIEW_FILE` when the agent must inspect local `SKILL.md` / `references/` files).
  - Use `to_message_dicts(part.a2ui)` when serialising parsed A2UI parts, and skip `<a2ui-json>` repair retries unless `response.stop_reason == types.StopReason.UNSPECIFIED`.
