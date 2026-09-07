---
name: pixverse:seedance-prompt-optimize
description: Rewrite Seedance 2.0/2.5 prompts for precise reference binding, shot sequences, and video editing when optimization is requested. Diagnose ambiguous asset roles before generation.
---

# Seedance Prompt Optimizer

Apply the [prompt editing contract](../references/prompt-contract.md). Use for Seedance engineering intent; use [seedance-vibe-creating](seedance-vibe-creating.md) for emotional or atmospheric rewriting. Other models route to [prompting-guide](prompting-guide.md), or [prompt-enhance](prompt-enhance.md) for V6.

An explicit rewrite request is sufficient authorization. During generation-only requests, repair command/asset mapping as necessary but offer wording changes as advice. Do not automatically expand a clean prompt.

## Asset binding

Bind references in the order actually passed to the CLI, numbering each modality independently:

- `--image` / `--images` → `@image1`, `@image2`, …
- `--videos` → `@video1`, `@video2`, …
- `--audios` → `@audio1`, `@audio2`, …

Raw file paths, URLs, and IDs belong in command inputs, not as substitutes for visual identity in the action description. For pasted JSON/content arrays, map each media item to its actual CLI input before rewriting its text references. Do not invent an attachment merely by declaring an ID inside the prompt.

For repeated subjects, use `<subject1>@image1`, or define a stable alias once: `The woman in @image1 is <subject1>`. Then reuse that alias consistently. Prefer noun/alias references over constructions such as `@image1 runs`; this makes the subject-role relationship explicit without relying on speculative tokenizer behavior. One subject may draw face and outfit references from different images.

Ask when asset roles actually matter and are unresolved: which image is an opening frame, who is represented by which image, or which video is the edit target. Multiple people do not automatically need a left/right assignment.

For character grids or multi-view sheets, prefer an existing single-view or clean scene still when available. If extracting or generating a suitable reference is needed, use [character-design](character-design.md) and preserve its registry. Do not demand that the user manually split images when available tools can do the authorized preparation.

Reference limits, accepted media, region support, duration, and `--task-type` are owned by [create-video](create-video.md). In particular, Seedance video input uses `create reference --videos`; the separate `create extend` command does not support Seedance. Seedance 2.5 can declare reference/edit/extend intent through `--task-type`; do not apply that flag to 2.0.

## Choose the operation and structure

| Intent | Prompt pattern |
|---|---|
| Reference | `Use <subject1> from @image1; use the camera movement in @video1. [Requested scene/action].` |
| Add | `In @video1, add [element] at [requested place/time]; preserve [unchanged content].` |
| Modify | `Strictly edit @video1, replacing [old feature] with [new feature]; preserve the requested action and camera.` |
| Delete | `Remove [element] from @video1; keep the remaining content unchanged.` |
| Extend | `Continue @video1 with [requested continuation].` Specify forward/backward only when intended; continuation normally follows the clip. |
| Stitch | `@video1, [requested transition], then @video2.` |
| Combined | Name the edit target and the distinct reference role separately. |

For edit/extend, identify the target directly; calling it merely a “reference” can obscure the operation. Preserve explicit user intent rather than asking them to approve a syntax correction.

A single continuous scene or local edit needs one paragraph. For a sequence, use:

1. **Setup:** supplied scene/style and reusable subject/asset definitions.
2. **Shots:** ordered beats containing camera intent, action, relevant spatial relationship, and sound. Keep one clear primary camera intention per shot; preserve intentional coordinated movement. Preserve explicit timing, while explaining uncertainty if exact synchronization is essential.
3. **Constraints, only when useful:** identity continuity, requested text, or a specific observed failure to avoid. Do not add generic quality pads, slow all motion, prohibit logos, or prohibit matching clothes/intentional twins.

Audit subject, action, scene, lighting, camera, style, fidelity, and continuity as a checklist of relevant information, not eight required fields. Infer from attached references when appropriate; omit missing decorative elements. Ask about an abstract brief only when no usable visual subject/action can be determined.

## Audio and displayed text

These prompt delimiters distinguish channels:

| Channel | Markup |
|---|---|
| Music | `(requested background music)` |
| Sound effect | `<requested sound effect>` |
| Dialogue | `{Exact spoken words}` |
| Subtitle/title | `[Exact displayed text]` |

Preserve exact dialogue and text. Tag the requested language when helpful. Audio-reference timbre can be described as `Use the timbre in @audio1`; media eligibility still comes from create-video. Do not silently replace difficult words with homophones or remove multilingual dialogue. If pronunciation is wrong in an observed result, propose a correction. Exact subtitle/audio synchronization may need post-production; do not promise it from wording alone.

## Example: reference-bound edit

```bash
pixverse create reference --model seedance-2.0-fast \
  --videos 987654 \
  --prompt "Continue @video1: the truck falls and the driver jumps out." \
  --json
```

This preserves the requested continuation without inventing a direction, extra actions, or a reference asset that was not passed.

Return the optimized prompt and a short explanation of material edits or unresolved requirements. Do not attach a fixed list of internal principle names.
