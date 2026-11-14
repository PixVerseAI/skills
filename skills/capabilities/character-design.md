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
  --model gpt-image-2.5-flare --quality 1440p --aspect-ratio 16:9 \
  --prompt "Same character as the reference: <known distinctive traits>. <requested scene>." \
  --json
```

Check region compatibility and preserve requested output settings. A previous I2I failure is not a permanent prohibition on Gemini or another model.

## Reuse for video

Follow [reuse in video](../references/persistent-assets.md#reuse-in-video): a multi-panel sheet is a design reference, not an opening frame. Use [seedance-prompt-optimize](seedance-prompt-optimize.md) for reference-binding syntax only when prompt engineering is requested.

## Scope

Character creation and reuse do not orchestrate a full story. Do not fuzzy-match names hidden in arbitrary prompts or silently regenerate an existing character; resolve explicit names and create a new version for a requested redesign. Scene stills may feed [storyboard-to-video](../workflows/storyboard-to-video.md), but this capability does not run that workflow automatically.

For characters holding persistent props, use [item-design](item-design.md#composing-with-characters). Use [create-voice](create-voice.md) and the relevant video capability when sound is requested; do not assume external voiceover replaces supported model-native speech.
