---
name: pixverse:text-to-image-to-video
description: Generate an image from text, then animate it into a video
---

Read [execution contract](../references/execution-contract.md) for result handling, retries, and defaults.

1. Generate an image using [create-and-edit-image](../capabilities/create-and-edit-image.md), choosing framing for the intended final video.
2. Validate success and retain `image_id` and `image_url` from the completed result; no separate image wait or info query is needed.
3. Inspect the image when visual approval or refinement is part of the task. For edits, use [image-editing-pipeline](image-editing-pipeline.md).
4. Generate a video using [create-video](../capabilities/create-video.md), `--image <image_id>`, and a motion prompt. Choose a supported model/quality/duration combination.
5. Validate success and download the completed `video_id` with `--type video`. Download the source image with `--type image` if requested. Optional extension, upscale, and audio: [video-production](video-production.md).
