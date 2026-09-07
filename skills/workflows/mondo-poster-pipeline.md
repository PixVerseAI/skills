---
name: pixverse:mondo-poster-pipeline
description: Design and generate a Mondo-style poster, with optional refinement
---

Read [execution contract](../references/execution-contract.md) for result handling, retries, and defaults.

Use [mondo-poster-design](../capabilities/mondo-poster-design.md) to choose the visual style, genre, composition, and print treatment. Read only the relevant artist/genre references linked there.

Generate using [create-and-edit-image](../capabilities/create-and-edit-image.md), choosing a model supported in the active region and the requested poster framing. Inspect the result, and use [image-editing-pipeline](image-editing-pipeline.md) only for concrete refinements. Download the final `image_id` with `--type image`.

For style exploration, vary the design prompt using [batch-creation](batch-creation.md). A draft from a different model previews the prompt idea, not the exact final composition; pass the draft as an image reference when preservation matters.

For animation, continue with [mondo-poster-to-video-pipeline](mondo-poster-to-video-pipeline.md).
