---
name: pixverse:character-design
description: Create, import, and reuse persistent character references across images and videos, storing cloud image IDs in a project or session registry.
---

# Character Design

Use the [persistent asset protocol](../references/persistent-assets.md) for create/import/list/show/use/migrate, persistence, naming, and recovery. These are agent actions, not shell subcommands. Character-specific choices follow here; [item-design](item-design.md) covers props.

## Fields and reference layout

`name` and `short_description` are required for a new generated character. Optional fields: `age`, `gender`, `species` (human unless indicated otherwise), `appearance`, `outfit`, `accessories`, `personality`, and `style_tags`. Importing a reference needs only a name and input; supplied metadata remains optional. Render age descriptors naturally (for example, “middle-aged”), without blindly appending “year-old”.

Default sheet: `16:9`, `1440p` with a supported image model. Build a description from supplied fields, omitting empty clauses, then append:

```text
Three-view character sheet: front, side, and back full-body views aligned
in a row; enlarged neutral head-and-face detail on the left; clothing and
accessory details below. Solid white background across panels and gutters,
with only subtle shadows beneath the feet. Keep one consistent character
identity across all views and a clear, balanced layout.
```

A supplied image can be adopted directly; do not regenerate it into a sheet unless requested. Treat this layout as the default for creating reusable design references, not an override of a user's chosen format.

## Reuse for images

Load the registry ID, then use I2I with a brief identity anchor from known fields and the requested scene. Use [create-and-edit-image](create-and-edit-image.md) for the selected model's limits and region compatibility.

```bash
pixverse create image --image <character_image_id> \
  --model gpt-image-2.0 --quality 1440p --aspect-ratio 16:9 \
  --prompt "Same character as the reference: <known distinctive traits>. <requested scene>." \
  --json
```

The example model/ratio are defaults for a compatible region; preserve requested output settings. A previous I2I failure is not a permanent prohibition on Gemini or another model.

## Reuse for video

A sheet is a design reference, not the video's opening frame. Do not directly animate a multi-panel sheet with `create video --image`.

- For models that accept subject reference images, use `create reference --images <id...>` with the requested scene. Resolve multiple names in their input order; limits belong to [create-video](create-video.md).
- For Seedance, prefer an existing single-view reference or generate a clean scene still from the sheet first, then animate that still. This avoids passing the multi-view layout to a consumer that may reproduce multiple character views. Do not require the user to manually split the sheet.
- The still-first route is also useful for precise pose, framing, or product placement. Check image generation completion before passing its ID to video generation; use the requested output ratio and supported duration consistently.

```bash
# Generate a clean scene from the persistent reference; capture the completed image_id.
pixverse create image --image <character_image_id> \
  --prompt "Same character as the reference. <requested scene and pose>." --json

# Animate that completed scene image, not the reference sheet.
pixverse create video --image <scene_image_id> --model <video_model> \
  --prompt "<requested motion>" --json
```

Use [seedance-prompt-optimize](seedance-prompt-optimize.md) for reference-binding syntax when prompt engineering is requested. Ordinary scene generation does not automatically trigger a rewrite.

## Scope

Character creation and reuse do not orchestrate a full story. Do not fuzzy-match names hidden in arbitrary prompts or silently regenerate an existing character; resolve explicit names and create a new version for a requested redesign. Scene stills may feed [storyboard-to-video](../workflows/storyboard-to-video.md), but this capability does not run that workflow automatically.

For characters holding persistent props, use [item-design](item-design.md#composing-with-characters). Use [create-voice](create-voice.md) and the relevant video capability when sound is requested; do not assume external voiceover replaces supported model-native speech.
