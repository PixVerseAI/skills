---
name: pixverse:modify-video-pipeline
description: Edit video content, then optionally upscale and download
---

Read [execution contract](../references/execution-contract.md) for result handling, retries, and defaults.

Use [modify-video](../capabilities/modify-video.md) with `--video <generated-id|local-path>` and an edit prompt. Local clips upload for processing. `--keyframe-time` is in **milliseconds**; omit it for the first frame or use, for example, `2000` for two seconds.

Validate the completed result and retain its `video_id`. Download with `--type video`, or continue with the optional post-processing steps in [video-production](video-production.md). Default creation already waits; do not wait again.
