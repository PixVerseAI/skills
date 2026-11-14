---
name: pixverse:capabilities
description: Discover the installed CLI's Create capabilities offline, and query live Canvas generation routes, models, and parameter constraints. Use before generating or patching Canvas so flags, models, enums, defaults, and media limits come from the current CLI and backend instead of a static table.
---

# Capability Discovery

Query what this installed CLI can do. Create capabilities are bundled and offline. Canvas capabilities are live and merged with the installed Create registry.

Do **not** invent Canvas `node_type` → CLI command mappings, and do **not** copy a Canvas runtime schema into notes or a skill file. Query the live commands below.

## Prerequisites

- PixVerse CLI 1.4.0 or later. On older releases, use `pixverse create <mode> --help` and the static model references; Canvas needs an upgrade.
- `capabilities` and `capabilities create` need **no login and no network**
- `capabilities canvas` requires authentication (ordinary login, access key, or a [paired session](../references/auth-pairing.md))

## Decision Tree

```text
Need current capabilities?
├── What can this CLI install do?     → pixverse capabilities --json
├── Which create modes exist?         → pixverse capabilities create --json
├── One create mode, all models?      → pixverse capabilities create <mode> --json
├── One create mode + one model?      → pixverse capabilities create <mode> --model <id> --json
├── Merged Canvas + CLI view?         → pixverse capabilities canvas [--node-type] [--selector] [--model] --json
├── Unmodified Canvas package?        → pixverse capabilities canvas --raw --json
└── One Canvas node schema?           → pixverse canvas node schema --node-type <type> --json
```

## capabilities (offline)

Prints the installed static capability bundle. `--json` is identical to the installed `capabilities.json`.

```bash
pixverse capabilities --json
```

No login, no workspace switch, no HTTP, no generation credits.

The bundled file uses a compact encoding (`capability_domains.create.encoding: "normalized"`). Prefer `capabilities create` when you need an expanded, query-ready structure. MiniApps are a separate product surface and are **not** in the Create mode list.

## capabilities create (offline)

Create modes that can be queried:

```text
video
image
transition
voice
music
extend
modify
upscale
reference
motion-control
template
seedance-final
```

### Mode index

```bash
pixverse capabilities create --json
```

```json
{
  "schema_version": "pixverse_create_capabilities.v1",
  "source": "bundled",
  "modes": [
    {
      "mode": "video",
      "capability_id": "create.video",
      "command": "pixverse create video",
      "description": "...",
      "default_model": "v6",
      "models": ["v6", "pixverse-c1"]
    }
  ]
}
```

The `models` array is this installed CLI, not a live catalog of future models.

### One mode, expanded

```bash
pixverse capabilities create video --json
pixverse capabilities create voice --json
```

JSON schema is `pixverse_create_capability_query.v1`. The result already expands shared parameters and model definitions.

### One mode + one model

```bash
pixverse capabilities create video --model v6 --json
pixverse capabilities create image --model qwen-image --json
```

Behavior:

- Applies mode parameters, model overrides, and matching model rules
- `capability.selected_model` is the chosen model
- `capability.models` keeps only that model
- `parameters.model.enum` narrows to that model
- Unsupported parameters keep `supported: false` and drop invalid defaults/enums/ranges
- If `capability.rules` contains conditions, apply matching rules before choosing dependent parameters. Do not invent rules absent from the installed query.
- Still offline — this is not a live backend catalog

For template creation, the offline registry describes shared flags, not a specific template’s accepted overrides. Read `template info <id> --json`; [schema-driven templates](template.md#schema-driven-templates) define their own inputs and fixed output settings.

`relax_mode` is declared with no boolean default and `on_invalid: backend` in six creation modes; this describes pass-through, not account eligibility. Image `background` is model-specific. See [Relax rules](../references/execution-contract.md#relax-mode) and [image options](create-and-edit-image.md#flags).

`supported: false` for `audio`, `multi_shot` or `off_peak` describes unavailable CLI control, not an assertion that the model cannot generate sound, multiple shots, or receive service-side scheduling. Do not promise silent output merely because an audio switch is unsupported.

`seedance-final` (CLI 1.4.19+) is a model-less action with inherited parameters. Draft Reference framing uses conditional rules for video presence and automatic/fixed duration; apply matching rules instead of relying only on the base enum. See [Draft/Final](../references/seedance-draft-final.md).

### Parameter fields

Each parameter uses a stable logical key plus the real CLI `flag`. Structured fields include:

| Field | Meaning |
|:---|:---|
| `type` | `string`, `integer`, `number`, `boolean`, `text`, `media`, `media_list`, `json` |
| `required` | Whether the flag must be supplied |
| `supported` | Whether the current mode/model accepts it |
| `default` | Normalized JSON default |
| `enum` | Allowed values |
| `min` / `max` | Numeric range |
| `unit` | Unit such as seconds |
| `min_count` / `max_count` | Media cardinality |
| `min_length` / `max_length` | Text length |
| `accepts` | Literal / file / stdin / media forms |
| `on_invalid` | `reject` (exit 6), `adjust` (CLI normalizes), or `backend` |
| `description` | English help text |

Types, defaults, and enums use normalized JSON values. Integers are numbers, not strings. Reference automatic duration is JSON integer `0`; the CLI flag remains `--duration auto` and is normalized before submit.

The registry declares no local length cap for voice text or music prompt/lyrics. Missing length metadata means there is no declared local cap, not that the provider accepts unlimited input; backend validation still applies.

### Validation errors (exit 6)

These fail before any request:

- unknown create mode
- model not in that mode
- `--model` without a mode

JSON errors go to stderr and may include `valid_modes` or `valid_models`.

## capabilities canvas (online)

Merges live Canvas node types, adapter routes, and field mappings with the **installed** CLI Create registry. Needs login. Does not create tasks, mutate projects, or charge generation credits. `capabilities canvas` and `canvas node schema` do not take a project ID; they discover node capabilities, not saved project positions. For a project layout use `canvas graph get <id>`, and to change that layout use `canvas arrange <id>`; see [Canvas](canvas.md).

```bash
# All nodes, merged
pixverse capabilities canvas --json

# One node type
pixverse capabilities canvas --node-type image_generate --json

# One adapter route (requires --node-type)
pixverse capabilities canvas --node-type image_generate --selector text_to_image --json

# One model on that node (requires --node-type)
pixverse capabilities canvas --node-type image_generate --model qwen-image --json

# Unmodified Canvas response (no merge; cannot combine with filters)
pixverse capabilities canvas --raw --json

# Bypass the 5-minute in-process cache
pixverse capabilities canvas --refresh --json
```

| Flag | Meaning |
|:---|:---|
| `--node-type <type>` | Return one Canvas node type |
| `--selector <value>` | Return one adapter route; requires `--node-type` |
| `-m, --model <id>` | Resolve CLI parameters for one model; requires `--node-type` |
| `--raw` | Original Canvas capabilities; cannot combine with node/route/model filters |
| `--refresh` | Force a full server fetch |
| `--json` | Pure JSON stdout |

Merged JSON schema is `pixverse_canvas_cli_capability_query.v1`. Each node keeps the original Canvas schema plus:

- `execution: "canvas"` — Canvas-only; empty `routes`; do not infer Create from the type name
- `execution: "canvas_cli"` — publishes adapter revision `canvas_cli_capability_adapter.v2`
- `routes[]` — selector, `capability_ref`, field mapping, Canvas conditions, expanded CLI capability
- `compatible` / `issues[]` — version, mapping, model, or current-region mismatches

Unknown adapter revisions, selectors, capability refs, mappings, or transforms **fail closed**. Do not guess a fallback. `capability_ref` is for discovery and validation only — it does **not** authorize calling `create.*` instead of Canvas Graph.

Region limits from the current `--region` / `PIXVERSE_REGION` are reflected in the merged result.

A single node schema is also available as:

```bash
pixverse canvas node schema --node-type image_generate --json
```

That command returns the unmodified Canvas node schema. Use `capabilities canvas --raw` for the full original package.

## Agent pattern

```bash
# Offline: confirm this CLI's video flags for a model
pixverse capabilities create video --model v6 --json

# Online: confirm a Canvas node can use that model before patching
pixverse capabilities canvas \
  --node-type image_generate \
  --selector text_to_image \
  --model qwen-image \
  --json
```

If `compatible` is false or `issues` is non-empty, fix the node type, selector, model, or region before `canvas patch`.

## Errors

Exit codes follow the [execution contract](../references/execution-contract.md#waiting-and-recovery). Offline queries fail only with exit 6 (unknown mode, model, node type or selector, or an illegal flag combination); `capabilities canvas` can also exit 1, 2 or 3 like any authenticated request.

## Related

- [canvas](canvas.md): build and run Canvas graphs using these results
- [create-video](create-video.md) / [create-and-edit-image](create-and-edit-image.md): static tables; prefer `capabilities create` when the installed CLI may be newer than this skill
