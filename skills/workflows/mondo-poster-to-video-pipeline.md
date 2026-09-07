---
name: pixverse:mondo-poster-to-video-pipeline
description: Generate a Mondo-style poster and animate a cinematic reveal
---

Read [execution contract](../references/execution-contract.md) for result handling, retries, and defaults.

Compose the poster with [mondo-poster-pipeline](mondo-poster-pipeline.md), then follow the image-to-video steps of [text-to-image-to-video](text-to-image-to-video.md) using that result; do not generate the poster a second time.

Preserve the composition with subtle animation. Choose an effect appropriate to the design:

| Effect | Motion prompt fragment |
|:---|:---|
| Reveal | Camera slowly pulls back revealing the full poster |
| Noir / horror | Shadows sweep slowly across the design; light flickers |
| Vintage / western | Dust drifts gently; warm light shifts |
| Sci-fi | Neon accents pulse subtly; atmospheric haze drifts |
| Fantasy | Fine glowing particles drift upward |
| Print process | Screen-print colors appear one layer at a time |

Use a single-shot setting where supported when the goal is one continuous reveal. Add sound only when requested, using supported native audio or [video-production](video-production.md). Download both the poster and final video when delivering the complete pipeline.
