---
name: pixverse:item-design
description: Create, import, and reuse persistent props or objects through a four-view reference and cloud image-ID registry; compose them with persistent characters.
---

# Item Design

Use the [persistent asset protocol](../references/persistent-assets.md) for create/import/list/show/use/migrate, storage, naming, and recovery. Items live in `.pixverse/items.json`, independently of character names. Actions are agent procedures, not installed `item-design` shell commands.

## Fields and layout

New generated items require `name` and `short_description`. Optional fields: `category`, `material`, `color_palette`, `size_scale`, `era_style`, `distinctive_features`, `condition`, and `style_tags`. Imported images are canonical references; metadata is optional.

Default generated sheet: `1:1`, `1440p` on a compatible model. Describe supplied fields without empty clauses, then append:

```text
Four-panel orthographic 2x2 grid: front view top-left, left side top-right,
top-down bottom-left, right side bottom-right. Show the same item in every
panel. Even quadrants with thin gutters; no labels or annotations. Solid
white background across the canvas and gutters, soft product lighting and
subtle shadows beneath each item. Clear reference layout rather than an ad.
```

Keep equal panels for roughly cubic/spherical items. When an item's shape would waste most of a quadrant, allow panel sizes to vary while retaining the reading order:

| Shape | Useful adaptation |
|---|---|
| Tall sword/staff | Taller front/side panels, smaller top-down view |
| Long vehicle | Wider side views |
| Flat book/plate/phone | Larger main surface view, thin side strips |

Use the description and actual shape, not category alone. Maintain a neutral background; honor a user's different requested reference format. Record the actual ratio in registry generation metadata.

## Reuse

For a scene still, pass the saved ID through I2I. Keep a short anchor naming known material, shape, and distinctive details.

```bash
pixverse create image --image <item_image_id> \
  --prompt "Same item as the reference: <known distinctive traits>. <requested scene>." \
  --json
```

For video, normally generate a clean scene still first, then animate its completed image ID using `create video --image`. A multi-panel sheet must not be used as an opening frame. Preserve the requested aspect ratio between stages and validate duration/model settings with [create-video](create-video.md).

Direct `create reference --images` is an alternative when the chosen model and task suit reference fusion. Do not turn this into a categorical ban: use the still-first route for controlled placement, or when direct reference results reproduce the grid.

## Composing with characters

Resolve the character and item names from their respective registries, then pass all IDs in a single I2I request:

```bash
pixverse create image --images <character_image_id> <item_image_id> \
  --prompt "<known character description> holding <known item description>. <requested scene>." \
  --json
```

For sword + shield or other combinations, add the necessary IDs within the selected model's actual limit; use [create-and-edit-image](create-and-edit-image.md), not a fixed cross-model reference cap. Do not drop a required item merely to fit a limit. Choose a compatible model or explain the constraint.

Coordinate shared registry mutations through the persistent protocol. Character and item slugs may match because their registries are separate. This capability does not automatically orchestrate stories or infer item names by fuzzy matching arbitrary prompt text.

## Related

- [character-design](character-design.md) — persistent characters
- [asset-management](asset-management.md) — upload, inspect, and download assets
- [create-and-edit-image](create-and-edit-image.md) — supported image settings and I2I inputs
- [create-video](create-video.md) — animate the composed still or use references
