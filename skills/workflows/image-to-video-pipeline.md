---
name: pixverse:image-to-video-pipeline
description: Animate an existing image into a video and download it
---

Read [execution contract](../references/execution-contract.md) for result handling, retries, and defaults.

Use [create-video](../capabilities/create-video.md) with `--image <local-path|URL|image-id|media-path>` and a prompt describing motion. Local inputs upload for processing. Validate the completed result, then download its `video_id` with `--type video`.

If the image must first be generated, use [text-to-image-to-video](text-to-image-to-video.md). For character motion from a reference clip, use [motion-control-pipeline](motion-control-pipeline.md).
