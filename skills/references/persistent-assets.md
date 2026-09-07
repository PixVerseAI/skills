# Persistent character and item assets

Shared registry protocol for [character-design](../capabilities/character-design.md) and [item-design](../capabilities/item-design.md). Read for registry create/import/use/migration; the caller owns fields, reference layout, and scene composition. These actions are agent procedures, not installed `character-design` or `item-design` shell commands.

## Storage and identity

Use `.pixverse/characters.json` or `.pixverse/items.json` in the project root. The cloud `image_id` is the reusable reference; local PNGs are optional previews. Resolve names by exact slug, then case-insensitive display name; report ambiguity rather than guessing.

```json
{
  "version": 2,
  "characters": {
    "aria": {
      "name": "Aria",
      "image_id": 398830212288488,
      "image_url": "https://example.com/reference.png",
      "origin": "generated",
      "region": "global",
      "workspace_id": 0,
      "fields": {"short_description": "A cheerful apprentice wizard"},
      "source_prompt": "The actual generation prompt",
      "generation": {"model": "gpt-image-2.0", "quality": "1440p", "aspect_ratio": "16:9"},
      "cache": {"local_path": "./characters/aria/reference.png"},
      "created_at": "2026-04-22T13:14:29Z"
    }
  }
}
```

Items use top-level `items` and cache `./items/<slug>/reference.png`. Record actual generation parameters, never sample defaults. Imported entries have `source_prompt` and `generation` set to null. `origin` is `generated`, `uploaded` (file/URL), or `imported` (existing image ID). Keep metadata unknowns null or omitted; do not invent them. Preserve existing schema fields on updates. Record the effective `region` and `workspace_id` with each new entry. For older entries without this context, verify the image in the intended account/workspace before reuse; never infer global/CN provenance from the numeric ID. Do not silently switch accounts or regions to make an ID resolve.

If the root is unwritable, use session memory and explain once that persistence requires saving the registry. After a mutation, print the affected registry JSON for rehydration; do not print unrelated unchanged registries. Validate `version: 2` and each entry's image ID when rehydrating. Session state cannot promise durability across new conversations.

## Actions

- **Create:** collect name and short description; use supplied optional fields without interviewing for every field. Load the registry, choose an unused slug (`name`, `name-2`, …), generate the caller's layout, then register the completed image ID/URL and actual parameters. Preserve existing entries. Cache when possible, then persist; cache failure does not invalidate the cloud asset.
- **Import:** existing local file → `pixverse asset upload <path> --json`; HTTPS URL → the same upload command; numeric image ID → verify through `pixverse asset info <id> --type image --json` without uploading. Capture the fields returned by [asset-management](../capabilities/asset-management.md), register under a free slug, and optionally cache. Keep the image as the canonical reference.
- **List/show:** read the registry only; list slug, name, ID, origin (and item category when useful), or show one entry and preview URL. No generation or cache download is necessary.
- **Use:** resolve requested names to IDs and pass IDs directly to the caller's downstream command. A generated scene still is not a new persistent character/item entry unless requested.
- **Migrate:** for legacy `characters/<slug>/reference.png` + `meta.json`, or item reference + metadata folders without an image ID, upload the actual reference path once and merge the metadata into the v2 registry. Skip already migrated entries; optionally update legacy metadata. Do not overwrite a colliding unrelated entry.

Prefer atomic registry replacement after reading the latest contents. If multiple agents mutate the same registry, serialize that write or coordinate ownership; do not lose other entries through stale read-modify-write.

## Generation and recovery

Use [create-and-edit-image](../capabilities/create-and-edit-image.md) for current models, reference limits, qualities, and region support, and [execution-contract](execution-contract.md) for task completion, retries, and outputs.

For generated reference sheets, prefer `gpt-image-2.0` at `1440p` when available. If a fallback is warranted, candidates are `gemini-3.1-flash`, `gemini-3.0`, and `seedream-5.0-lite`; filter candidates by selected region and supported parameters before submitting. In CN, prefer `seedream-5.0-lite`; if using `qwen-image`, lower quality to its supported `1080p`. Respect explicit model requirements rather than silently changing them.

A successful task supplies the image ID; confirm completed status, not merely presence of a URL. A temporary preview/HEAD failure is not evidence that image generation failed: inspect/download the existing asset before creating a replacement. Separate parameter errors, authentication/credit failures, moderation, and transient task failures. Do not retry all models for every failure. After a fallback also fails, report the cause instead of exhausting a costly chain. Retain task IDs so interrupted work can resume.

Do not silently change named brands, requested actions, or other creative content to get past a failed generation. Explain the observed failure and propose a compatible revision where appropriate; past failures are not universal model restrictions.
