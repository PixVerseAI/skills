# Seedance Draft and Final (CLI 1.4.19+)

Use `seedance-2.5-480draft` for a requested 480p sample in `create video`, `create reference`, or exactly-two-image `create transition`. It is not interchangeable with ordinary Seedance 2.5 at 480p. Draft is available in Global and CN; preserve the selected region and workspace.

Draft supports only `480p` (default; other qualities are adjusted), integer 4–30 second duration (default 5), and requires a prompt. Reference limits match Seedance 2.5: up to 30 images, 10 videos and 10 audios, 50 total; separate 30-second video/audio totals, with visual input required for audio. Use [reference constraints](video-reference.md#reference-media-matrix) for media details.

Framing depends on mode: T2V and text/image-only Reference accept six fixed ratios (`21:9`, `16:9`, `4:3`, `1:1`, `3:4`, `9:16`), default `16:9`. I2V uses automatic framing; Transition derives framing from its two images. With reference video, duration defaults to `auto` (JSON `0`) and locks framing to `auto`; explicit 4–30 seconds permits `auto` or fixed framing. `--task-type auto|reference|edit|extend` is available in Reference. Read matching installed capability rules instead of treating the base ratio enum as universal. Audio/multi-shot/off-peak controls remain unsupported.

```bash
pixverse create video --model seedance-2.5-480draft --prompt "$PROMPT" --quality 480p --duration 5 --json
```

## Inspect and create Final

`task status`, `task wait` and completed video creation output preserve optional `seedance_draft` metadata:

- Draft: `stage: "draft"`, `expires_at` (Unix seconds), `can_create_final`, and optional string `final_video_ids` / `latest_final_video_id`.
- Final: `stage: "final"`, `can_create_final: false`, and `source_draft_video_id`.

Inspect this metadata to explain eligibility and expiry, or recover an already-created Final. The current CLI submits directly and the service makes the final eligibility decision; do not claim a local eligibility precheck or treat stale metadata as permission to create.

Once Final creation is within the user's requested scope:

```bash
pixverse create seedance-final --video-id "$DRAFT_ID" --no-wait --json
```

The source ID must be a positive safe integer. Final inherits generation settings server-side and produces 1080p; it is not generic upscaling. It accepts only the source ID, optional Relax flags, `--no-wait`, `--timeout` (default 300 seconds), and JSON/pipe mode. No prompt/model/quality overrides or idempotency key are supported.

Every accepted Final submission creates a new paid task. Never automatically retry submission, including after a transport failure or an unsupported returned ID. Save `video_id`, `trace_id`, `cost_credits` and submitted `params` when returned. Recover with `task status` / `task wait --type video`, or inspect the Draft's linked Final IDs before considering another separately intended submission. Polling failure does not authorize creating another Final.

Final Relax is independent of the Draft: in Global, bare `--relax-mode` or `true` sends true; `false` / `--no-relax-mode` sends false; omission sends no field. CN always omits it, even when specified. Invalid boolean values fail locally in either region. Backend entitlement still applies.
