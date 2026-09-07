---
name: pixverse:text-to-video-pipeline
description: Generate a video from a text prompt and download it
---

Read [execution contract](../references/execution-contract.md) for result handling, retries, and defaults.

Use [create-video](../capabilities/create-video.md) for model selection and generation. Create with `--json`; default mode already waits. Validate success, extract `video_id`, then `pixverse asset download <video_id> --type video --json`.

For an asynchronous request, retain the submitted ID and wait once before downloading. To extend, upscale, or add audio, continue with [video-production](video-production.md).
