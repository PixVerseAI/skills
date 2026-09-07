---
name: pixverse:motion-control-pipeline
description: Animate a character image with reference motion, then optionally post-process
---

Read [execution contract](../references/execution-contract.md) for result handling, retries, and defaults.

Use [motion-control](../capabilities/motion-control.md) with `--image <character-image>` and `--video <reference-video-id|local-path>`. Choose a clear half-body or full-body character image suitable for motion transfer; local inputs upload for processing.

Validate the completed `video_id`, then download with `--type video` or continue with [video-production](video-production.md). For multiple variations, use the bounded submission and recovery procedure in [batch-creation](batch-creation.md), applying `--count` to motion-control instead of video.
