# Research: A2UI (`a2ui-project/a2ui`) and Python Libraries

Primary-source investigation of [`a2ui-project/a2ui`](https://github.com/a2ui-project/a2ui), focusing on its Python packages, architecture, agent skills, and implications for a Python + Textualize (`Textual`) TUI.

## 1. Overview & Core Architecture

**A2UI (Agent-to-User Interface)** is an Apache-2.0 open-source generative UI framework and protocol (`v1.0` current; `v0.8` deprecated) where an AI agent streams structured UI layout descriptions and data models, and the client renders them with its own trusted native UI components rather than executing untrusted code ([README.md](https://github.com/a2ui-project/a2ui/blob/main/README.md), [skills/a2ui/SKILL.md](https://github.com/a2ui-project/a2ui/blob/main/skills/a2ui/SKILL.md)).

The repository is structured as a multi-language monorepo using `uv` workspaces for Python (`requires-python = ">=3.10"`) alongside TypeScript, Dart/Flutter, Swift, and Kotlin packages ([pyproject.toml](https://github.com/a2ui-project/a2ui/blob/main/pyproject.toml)).

Its stack spans three layers ([README.md](https://github.com/a2ui-project/a2ui/blob/main/README.md)):

1. **Inference**: An agent instructed by an A2UI skill generates UI + data using an inference format such as Direct JSON or A2UI Express.
2. **Transport**: An A2UI Agent SDK parses and validates the model output, expands macros, and emits wire-stable A2UI protocol messages (`CreateSurface`, `UpdateComponents`, `UpdateDataModel`, `DeleteSurface`).
3. **Rendering**: A client combines an **A2UI Core** library (`MessageProcessor`, state model, expressions) with a native UI framework adapter and an explicit component catalog.

---

## 2. Official Python Packages in `a2ui-project/a2ui`

The [`python/`](https://github.com/a2ui-project/a2ui/tree/main/python) directory publishes four official packages to PyPI ([README.md](https://github.com/a2ui-project/a2ui/blob/main/README.md#python), [python/README.md](https://github.com/a2ui-project/a2ui/blob/main/python/README.md)):

| Package | Repo Path | PyPI | Role |
| --- | --- | --- | --- |
| `a2ui-core` | [`python/a2ui_core/`](https://github.com/a2ui-project/a2ui/tree/main/python/a2ui_core) | [`a2ui-core`](https://pypi.org/project/a2ui-core/) | Protocol messages, reactive surface state, data binding, expression evaluation, and catalog validation |
| `a2ui-agent-sdk` | [`python/a2ui_agent/`](https://github.com/a2ui-project/a2ui/tree/main/python/a2ui_agent) | [`a2ui-agent-sdk`](https://pypi.org/project/a2ui-agent-sdk/) | Framework-agnostic Agent SDK: catalog negotiation, prompt/skill generation, builders, macros, and streaming parsers |
| `a2ui-adk` | [`python/a2ui_adk/`](https://github.com/a2ui-project/a2ui/tree/main/python/a2ui_adk) | [`a2ui-adk`](https://pypi.org/project/a2ui-adk/) | Integration with Google's Agent Development Kit (`google-adk>=1.28.1`) |
| `a2ui-a2a` | [`python/a2ui_a2a/`](https://github.com/a2ui-project/a2ui/tree/main/python/a2ui_a2a) | [`a2ui-a2a`](https://pypi.org/project/a2ui-a2a/) | Extension for the Agent-to-Agent (`a2a-sdk`) protocol |

### 2.1 `a2ui-core` (`python/a2ui_core/`)

A framework-agnostic Python core library (`fallback-version = "0.7.0"` in [`python/a2ui_core/pyproject.toml`](https://github.com/a2ui-project/a2ui/blob/main/python/a2ui_core/pyproject.toml)) built on Pydantic v2 (`>=2.10.0`) and JSON Schema Draft 2020-12 (`jsonschema>=4.26.0`, `referencing>=0.37.0`). It targets A2UI **v0.9 and onwards** (no legacy v0.8 support) and mirrors the client-side `@a2ui/web_core` architecture ([python/a2ui_core/README.md](https://github.com/a2ui-project/a2ui/blob/main/python/a2ui_core/README.md)):

- **State Layer (`src/a2ui/core/state`)**: Reactive `Signal`, `DataModel` (JSON pointer path observer with wildcard queries), `SurfaceComponentsModel`, `SurfaceModel`, and `SurfaceGroupModel`.
- **Resolution Engine (`src/a2ui/core/resolution`)**: `DataContext`, `GenericBinder`, and `ComponentContext` for dynamic path resolution and expression evaluation.
- **Message Processing (`src/a2ui/core/processing`)**: `MessageProcessor` translates incoming A2UI envelopes (`CreateSurface`, `UpdateComponents`, `UpdateDataModel`, `DeleteSurface`) into reactive `SurfaceGroupModel` mutations ([message_processor.py](https://github.com/a2ui-project/a2ui/blob/main/python/a2ui_core/src/a2ui/core/processing/message_processor.py)).
- **Catalogs & Validation (`src/a2ui/core/catalog`, `src/a2ui/core/validation`)**: `JsonCatalog`, `ModelCatalog`, `Catalog.derive`, cyclic layout detection, reachability analysis, and orphan component tracking.
- **Basic Catalog (`src/a2ui/core/basic_catalog/v1_0/components.py`)**: Standard Pydantic component models:
  - Display & layout: `TextComponent`, `ImageComponent`, `IconComponent`, `VideoComponent`, `AudioPlayerComponent`, `RowComponent`, `ColumnComponent`, `ListComponent`, `CardComponent`, `TabsComponent`, `ModalComponent`, `DividerComponent`
  - Interactive inputs: `ButtonComponent`, `TextFieldComponent`, `CheckBoxComponent`, `ChoicePickerComponent`, `SliderComponent`, `DateTimeInputComponent`

### 2.2 `a2ui-agent-sdk` (`python/a2ui_agent/`)

The agent-side Python SDK (`fallback-version = "0.12.0"` in [`python/a2ui_agent/pyproject.toml`](https://github.com/a2ui-project/a2ui/blob/main/python/a2ui_agent/pyproject.toml)) depends on `a2ui-core>=0.7.0,<0.8.0`, `pydantic>=2.11.0`, `antlr4-python3-runtime`, `jsonschema`, and `pyyaml`. Crucially, it is explicitly **framework-agnostic**—`tests/test_framework_agnostic.py` enforces zero imports of A2A, ADK, or model SDKs—so it can be paired directly with `google-antigravity` or any custom Python agent ([python/a2ui_agent/README.md](https://github.com/a2ui-project/a2ui/blob/main/python/a2ui_agent/README.md)):

- **Processor & Catalog Configuration (`src/a2ui/processor`)**: `A2uiGenerator`, `A2uiRequestProcessor`, `CatalogConfig`, `CatalogProvider` (`FileSystemCatalogProvider`, `InMemoryCatalogProvider`), plus pruning transformers (`ComponentPruningTransformer`, `FunctionPruningTransformer`).
- **Typesafe Builders (`src/a2ui/builder`)**: Pydantic builders for `v0_9` and `v1_0` (`flatten_component_tree`) to construct component trees in Python without raw JSON dictionaries.
- **Macro Transformers (`src/a2ui/transformers/macros`)**: `@macro` and `MacroExpander` synthesise catalog schemas from Python builder functions and lower custom macro components into primitive subtrees.
- **Streaming Parsers & Inference Formats (`src/a2ui/parser`, `src/a2ui/inference_formats`)**:
  - `DirectJsonParser`: `open_stream` heals partial JSON chunks during streaming.
  - `ExpressParser`: ANTLR4-based parser for A2UI Express syntax (`Express.g4`).
  - `RendererState` & `validate_payload`: Mirrors client surface state on the agent side to catch invalid surfaces before transmission.
- **Renderer RPC (`src/a2ui/rpc`)**: `RendererToAgentMessageProcessor` and `RendererFunctionCalls` for bidirectional v1.0 `callAgentFunction` / `callRendererFunction` exchanges.

### 2.3 `a2ui-adk` (`python/a2ui_adk/`) and `a2ui-a2a` (`python/a2ui_a2a/`)

- **`a2ui-adk`** (`fallback-version = "0.3.0"`, [`python/a2ui_adk/README.md`](https://github.com/a2ui-project/a2ui/blob/main/python/a2ui_adk/README.md)): Connects `a2ui-agent-sdk` to `google-adk>=1.28.1` via `SendA2uiToClientToolset`, `A2uiInstruction`, `A2uiProcessorStore`, `A2uiRendererCallsStore`, and optional `[a2a]` helpers (`A2uiEventConverter`, `a2ui_rpc_callback`, `A2uiSubagentMap`).
- **`a2ui-a2a`** (`fallback-version = "0.4.0"`, [`python/a2ui_a2a/README.md`](https://github.com/a2ui-project/a2ui/blob/main/python/a2ui_a2a/README.md)): Connects `a2ui-agent-sdk` to `a2a-sdk>=0.3.0,<0.4.0` via `get_a2ui_agent_extension`, `create_a2ui_part`, `stream_response_to_parts`, and `get_a2ui_messages`.
- **Workspace extras** ([`pyproject.toml`](https://github.com/a2ui-project/a2ui/blob/main/pyproject.toml)): `python/catalogs/mcp` (MCP catalog helpers) and `tools/build_catalog` (catalog build tooling).

---

## 3. Agent Skills Inside `a2ui-project/a2ui`

- **User-facing skill**: [`skills/a2ui/SKILL.md`](https://github.com/a2ui-project/a2ui/blob/main/skills/a2ui/SKILL.md) instructs agents on when to choose A2UI, protocol version rules (`v1.0` current), and official package names across React, Angular, Lit, Flutter, SwiftUI, Jetpack Compose, Python (`pip install a2ui-agent-sdk`), and TypeScript.
- **Contributor skills**: [`.agents/skills/`](https://github.com/a2ui-project/a2ui/tree/main/.agents/skills) contains 16 internal workflow skills including `a2ui-generate-pydantic-models`, `a2ui-implement-new-sdks-for-client-language`, `a2ui-audit`, and `a2ui-release-python`.

---

## 4. Client Renderers & Relevance to a Python Textual TUI

Official client renderers in `a2ui-project/a2ui` target graphical web and mobile frameworks ([README.md](https://github.com/a2ui-project/a2ui/blob/main/README.md), [skills/a2ui/SKILL.md](https://github.com/a2ui-project/a2ui/blob/main/skills/a2ui/SKILL.md)):

- **Web**: `@a2ui/react`, `@a2ui/angular`, `@a2ui/lit` (backed by `@a2ui/web_core`)
- **Mobile / Multi-platform**: `a2ui_flutter` (backed by Dart `a2ui_core`), `A2UISwiftUI` (alpha), and Jetpack Compose (`kotlin/`, alpha)

There is **no official Python terminal/Textual renderer** in `a2ui-project/a2ui`. However, because `a2ui-core` already implements the complete client-side protocol state engine in Python (`MessageProcessor` -> `SurfaceGroupModel` -> `SurfaceModel` -> `DataModel` + `BasicCatalog` component models), building a lightweight Textual adapter only requires mapping the `BasicCatalog` components (`Column`, `Row`, `Card`, `Text`, `Tabs`, `List`, `Button`, `TextField`, `Divider`, `ChoicePicker`) onto Textual widgets—while `a2ui-agent-sdk` handles prompt generation, catalog pruning, and streaming JSON validation on the `google-antigravity` agent side.
