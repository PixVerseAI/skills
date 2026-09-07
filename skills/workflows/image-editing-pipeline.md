---
name: pixverse:image-editing-pipeline
description: Refine an existing or generated image through iterative I2I edits
---

Read [execution contract](../references/execution-contract.md) for result handling, retries, and defaults.

Use [create-and-edit-image](../capabilities/create-and-edit-image.md) to generate a starting image, or begin with the user's existing image.

1. Inspect the image; identify a concrete edit, including spatial location when relevant.
2. Create an image with `--image <current-image-url-or-path>` and that edit prompt. Respect user choices of model, quality, framing, and features to preserve.
3. Validate success and retain the new `image_id` and `image_url` directly from the result. Inspect it before deciding whether another edit is needed.
4. Stop when the requested changes are satisfied; download the final ID with `--type image`.

Do not query `asset info` solely to retrieve a URL already returned by creation. Additional iterations consume credits; avoid an unbounded refinement loop.
