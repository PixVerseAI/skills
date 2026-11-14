---
name: pixverse:template
description: Browse and apply PixVerse effect templates — including viral AI effects like AI Hug, AI Kiss, and more — to create videos or images from your photos
---

# Template

Discover and use PixVerse effect templates to create videos or images. Templates are pre-configured effects that take your image (or video) as input and apply a specific transformation. Results, polling and recovery follow the [execution contract](../references/execution-contract.md) unless noted for schema-driven templates below.

## Discover

| Command | Output |
|:---|:---|
| `template categories --json` | `{"categories": [{"id", "category_name"}]}` |
| `template list [--category <id>] [--limit 20] [--page 1] --json` | `{"items", "total", "page", "limit"}`; items carry `template_id`, `display_name`, `template_type` (1 video, 2 image), `effect_type`, `supported_features` |
| `template search "<keyword>" --json` | `{"items", "total"}` |
| `template info <id> --json` | Full detail; always inspect it before choosing inputs |

Useful `template info` fields: `template_type`, `effect_type`, `supported_features` (contains `1000` when video input is accepted; may be a scalar or an array), `duration`, `display_prompt` (presentation text, not a request for user input), `template_model`, `template_paid`, `video_base_cost`, `web_thumbnail_video_url`.

`template info` also returns normalized `input_requirements`: `images.required` / `optional`, `video_alternative`, `prompt.mode` and ordered `slots`. `complete: false` means some requirements are unknown; inspect the current detail rather than guessing. Slot descriptions and `example_url` explain the inputs. View an example before describing its contents, and never treat it as the user's own reference.

## Classic effects

Classic effects declare their input through `effect_type`. Templates that declare ordered `input_fields` are [schema-driven](#schema-driven-templates) instead.

| `effect_type` | Input |
|:---|:---|
| `0` | Text only; no image or video |
| `1` | 1 image, or 1 video if `supported_features` contains `1000` |
| `N > 1` | N required images; declared optional references may follow |

| Flag | Notes |
|:---|:---|
| `--template-id <id>` | Required |
| `--image <paths...>` | Required images first, then up to `input_requirements.images.optional` extra images for ordinary video effects. Image-output and text-only effects take no optional images |
| `--video <pathOrId>` | Only when the template supports a video alternative; replaces the required image and cannot be combined with images |
| `-q, --quality` | Default `720p`, model-dependent |
| `-d, --duration` | Template default unless overridden |
| `--aspect-ratio` | Optional override; image templates validate it against their model |
| `--prompt` | Follow `input_requirements.prompt.mode`: `disabled` rejects explicit prompts; editable text is optional |
| `--seed` | Image templates generate a random seed when omitted |
| `--count 1-4`, `--off-peak`, `--idempotency-key`, `--no-wait`, `--timeout 300` | As in the execution contract |

```bash
pixverse template info 12345 --json
pixverse create template --template-id 12345 --image ./photo.jpg --json
pixverse create template --template-id 12345 --video 987654 --json
```

The template decides the output type: `video_id` / `video_url` or `image_id` / `image_url`. Pass the matching `--type` to task and asset commands, and do not assume every template returns `video_id`.

## Schema-driven templates

The same `create template --template-id <id>` command supports templates whose detail declares ordered `input_fields`. Do not derive their inputs from `effect_type` or force their output into a single video/image ID.

- Match each field's `content_type` (`image`, `video`, `text`), normalized `required`, `max_size` (bytes), and video `min_duration` / `max_duration` (seconds).
- Supply images with `--image` in slot order, one video with `--video`, and one editable text value with `--prompt`. Image and video can coexist when the schema includes both. More than one video or text slot is unsupported, and there is no audio input flag.
- Image values fill required slots first, then optional slots from left to right. Ambiguous selections fail with exit 6 before uploads. Do not invent named slot flags.
- Omitted or blank text uses the slot default. Required text without a nonblank default must be supplied. A template without a text slot rejects `--prompt`. The CLI truncates text to 5000 Unicode code points; keep within that limit or get an authorized rewrite first.
- Output settings belong to the template: `--quality`, `--duration`, `--aspect-ratio`, `--seed`, `--count`, `--off-peak` and `--idempotency-key` are rejected. `--no-wait`, `--timeout` and `--json` work.

```bash
pixverse create template --template-id "$TEMPLATE_ID" --image ./subject.png --video ./motion.mp4 --prompt "Requested direction" --no-wait --json
```

Accepted JSON includes `template_id`, optional `set_id`, and `outputs: [{media_id, media_type}]`. When waiting, ordered `results` are appended, each with its output identity and either `detail` or `error`. Preserve every output and resume with `task wait <media_id> --type <media_type> --json`; never rerun generation to recover results.

Partial polling failures keep all IDs and completed details. Timeout exits 2 and generation failure exits 5. Missing or malformed accepted outputs exit 1 and print recovery data (`response`, `valid_outputs`, template ID, trace) to stderr. Inspect it before any retry, because tasks may already exist.

## Related

- [task-management](task-management.md) and [asset-management](asset-management.md)
- [create-video](create-video.md): videos without templates
