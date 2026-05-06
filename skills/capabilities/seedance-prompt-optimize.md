---
name: pixverse:seedance-prompt-optimize
description: Optimize user prompts for Seedance 2.0 (`seedance-2.0-standard`, `seedance-2.0-fast`) video generation. Invoke when (a) the user is targeting a Seedance model — e.g. `--model seedance-2.0-standard` / `--model seedance-2.0-fast`, or any model identifier containing "seedance" — AND (b) a quick triage check shows the prompt has meaningful optimization headroom (missing core elements, ambiguous multi-asset references, raw asset IDs, camera-move conflicts, vague verbs). If the user's prompt already cleanly expresses their intent, do NOT optimize — go straight to generation. The user can also explicitly request optimization to force-trigger.
---

# Seedance 2.0 Prompt Optimizer

Optimize a user's video generation prompt for **Seedance 2.0** (`seedance-2.0-standard` / `seedance-2.0-fast`). Seedance 2.0 natively supports multi-modal references (image / video) and end-to-end video editing — its prompt engineering surface is significantly richer than V6's. This skill rewrites loose, adjective-heavy prompts into engineered, three-section prompts grounded in the eight core elements and Seedance's multi-modal reference syntax.

> **PixVerse pipeline note:** PixVerse's current Seedance 2.0 integration does **not** accept audio as an input reference. Do not direct users to attach audio assets, and do not write audio cues into the prompt body. Reference assets are limited to **images** and **videos**.

For non-Seedance video models, use `pixverse:prompt-enhance` instead.

## When to Use

**Model-gated, with smart auto-detection.** Both conditions must hold:

1. **Target model is Seedance** — the user has specified `--model seedance-2.0-standard`, `--model seedance-2.0-fast`, or any future model identifier containing `seedance`.
2. **Optimization is actually warranted** — either the user explicitly asks for it, OR a quick triage of the prompt finds meaningful headroom for improvement. If the prompt already cleanly expresses the user's intent, **skip this skill** and go straight to generation.

### Triage Check (mandatory before invoking)

Before applying the full optimization workflow, run a fast triage on the user's prompt + attached assets. Count how many of these red flags are present:

- **Missing core elements** — fewer than three of {subject, action, scene} are present
- **Raw paths / URLs / video IDs in body** — local file paths (`./img.jpg`, `/Users/...`), HTTPS URLs, or generated-asset video IDs (e.g. `123456`) appear inside the action description instead of being bound to a positional `@imageN` / `@videoN` label in the setup
- **Ambiguous multi-asset roles** — multiple inputs passed via `--images` / `--image` / source video but no left/right, first-frame/last-frame, or subject/reference assignment
- **Camera-move conflict** — two simultaneous moves like "dolly in *and* pan left", "zoom in while pulling back"
- **Vague verbs only** — the action is carried by generic verbs ("moves", "goes", "does something") with no physical specifics
- **Tokenizer-disambiguation violations** — `@imageN` / `@videoN` references followed directly by a verb, preposition, or numeric word
- **Hollow filler dominates** — more than half the prompt is non-actionable filler ("cinematic 4K", "masterpiece", "octane render", "highly detailed") with no concrete subject / action
- **High-action scene with multiple characters but no position lock** — multi-character dynamic action where face-swap / clipping is likely

**Decision rules:**

| Trigger | What to do |
|:---|:---|
| User explicitly asked to optimize | Always invoke (skip triage; respect explicit ask) |
| ≥ 2 red flags | Invoke; brief one-line note that optimization headroom was detected |
| 1 red flag | Invoke only if the flag is one of: raw asset IDs, camera-move conflict, ambiguous multi-asset roles (these block generation quality regardless of the rest) |
| 0 red flags | **Do not invoke.** The prompt is good enough — go straight to `create video` |

When the triage says "skip", do not announce it as a decision — silently move on to generation. Only mention this skill when you actually run it.

When invoked (whether auto-triggered or explicit), **state explicitly** in your response that you are applying the Seedance 2.0 Prompt Optimizer, and briefly cite which red flag(s) drove the decision.

## Scope

- **Seedance 2.0 only** — engineering rules below are tuned to Seedance's prompt parser and its multi-modal reference handling.
- **Prompt text only** — this skill rewrites the `--prompt` value; it does not select model variant, quality, duration, or other CLI flags.
- **All Seedance scene types** — text-to-video (T2V), image-to-video (I2V), reference-to-video (R2V), video-to-video (V2V), and video editing (add / delete / modify / extend / stitch).
- **No workflows or pipelines** — do not propose multi-step processes.

## Core Workflow

When the user supplies a rough prompt, multi-modal assets (images / videos), or only a high-level brief (e.g. "make a cyberpunk dance video"), follow these steps in order.

### Step 0 — Brief Expansion (only when the user gave no concrete prompt)

If the user only provided a high-level idea ("I want a cyberpunk video", "generate a girl dancing"), enter **guided mode** before optimizing. Ask focused questions tied to the eight core elements (see Step 3) — never invent details silently.

Example:

> A few quick questions to ground the prompt: (1) What does the girl look like — age, outfit, hair? (2) Where is she dancing — neon street, classical stage, rooftop? (3) Do you have a reference image (e.g. `@image1`) to attach?

When the user replies with enough detail, proceed to Step 1.

### Step 1 — Intent & Scene Classification

Classify the request along two axes:

1. **Generation type** — fresh generation (T2V / I2V / R2V) vs. video editing (add / delete / modify / extend / stitch).
2. **Scene dynamics** — *dialogue / quiet scene* (needs micro-direction: facial expression, subtle motion) vs. *high-action scene* (preserve large motion, lean on motion / camera reference assets).

This shapes how aggressively you should describe motion vs. nuance.

### Step 2 — Asset Parsing & Mapping (multi-modal auto-mapping)

1. **CLI flag mapping.** Determine how the assets will reach Seedance 2.0 via the PixVerse CLI:
   - Single image (I2V) → `--image <pathOrUrl>` (or `--asset-image <ossPath>` for an already-uploaded asset). Bind it to `@image1`.
   - Multi-image fusion (R2V) → `pixverse create reference --images <p1> <p2> ...`. Bind them in flag order: 1st → `@image1`, 2nd → `@image2`, …  (Seedance supports up to 7 images.)
   - Source video (V2V / video edit) → bind to `@video1`, `@video2`, … in the order the user introduces them. Up to 3 input videos, total ≤ 15 s.
   - Generated assets the user references by `video_id` (e.g. `123456`) → bind them up front (`@video1 is video_id 123456 — [description]`) before using them in the body.
   - **Audio assets are not supported** by PixVerse's Seedance 2.0 — if any are present, drop them and inform the user.
2. **Long-text / JSON parsing.** If the user pasted a payload containing a `"content"` array or any structure with attached image / video items, scan it the same way: number items in the order they appear (audio items dropped), and in the `text` portion replace any inline raw paths / URLs / `video_id` numbers with the corresponding `@imageN` / `@videoN` label.
3. **Long-image / grid check.** Ask the user whether any uploaded asset is a long image or N-up grid. If so, instruct them to split it into separate single-frame images first.
4. **Mapping confirmation.** When multiple images / videos exist but their roles are ambiguous (who is on the left, who is the first frame vs. the last frame, which is reference vs. subject), explicitly ask the user before rewriting.

### Step 3 — Element Audit & Multi-Select Confirmation

Audit the user's prompt against the **eight core elements**:

1. **Precise subject** — who / what is in frame (appearance, defining features)
2. **Action detail** — what they are doing, with physical specifics
3. **Scene / environment** — where it takes place
4. **Light & color** — lighting source, color temperature, mood
5. **Camera & motion** — framing, lens, single coherent camera move
6. **Visual style** — render style, art direction, era
7. **Quality parameters** — resolution / fidelity cues
8. **Constraints** — anti-failure guards (face stability, no clipping, etc.)

Also check for **camera-move conflicts** (e.g. "dolly in *and* pan left simultaneously" — Seedance enforces one camera move per time slice).

**Reject silent fixes.** When something is missing or conflicting, surface concrete suggestions to the user as a multi-select list, then wait for their picks.

Multi-select template:

> I reviewed your prompt. A few suggestions — please pick the ones to apply:
> 1. **Clarify positions** — `@image1` and `@image2` need a left/right assignment.
> 2. **Add action detail** — how are they running (chasing, side by side)?
> 3. **Resolve camera conflict** — current prompt has both "dolly in" and "pan left". Pick one.
>
> ☐ Apply (1) — `@image1` on the left, `@image2` on the right
> ☐ Apply (2) — chasing run
> ☐ Apply (3) — keep "dolly in" only
> ☐ Other (please describe)

### Step 4 — Structured Rewrite

Once the user has resolved the multi-select (or the prompt was already complete), produce the final output in the three-section structure below. The structure is mandatory.

## Output Format

When optimizing a prompt, return three labeled sections.

### 1. Optimized Prompt

A **three-section** prompt body:

#### Section A — Global Setup
Lock the cast, environment, and core assets up front.

- **MANDATORY: bind every input asset to a positional `@imageN` / `@videoN` label and a named role.** The position must match the order the asset is passed to the CLI (`--images` flag order, or the order the user introduces source videos). Examples:
  > `@image1` (1st image in `--images`) is **Li Wu**, a young man in a black coat.
  > `@image2` (2nd image in `--images`) is **Su You**, a woman in a red dress.
  > `@video1` (source clip, `video_id` 123456) is a 5 s shot of a fire truck on a tilting street.
- **Never** drop a bare path, URL, or numeric `video_id` into the action description — bind it to a positional label in this section first, then refer to the label only.
- **First/last-frame control.** If the user wants a specific opening or closing frame, declare it here:
  > `@image1` as the first-frame anchor, `@image2` as the last-frame anchor.

#### Section B — Time-Sliced Shot Script
Drive the temporal layer. Slice the timeline dynamically based on action density (e.g. `0–3s`, `3–7s`, `7–10s`). Each slice contains one primary action and **one** camera move.

- **Disambiguation rule (critical for Seedance's tokenizer).** Whenever you reference `@imageN` or `@videoN`, you MUST follow it with a parenthetical alias or a clear noun phrase so the parser does not glue the digit to whatever follows.
  - ✅ **Correct:** `@image1 (Li Wu) walks toward @image3 (Su You)`
  - ✅ **Correct:** `the girl in @image2 is on the left side of the frame`
  - ❌ **Wrong:** `@image2 stands at the door` (parser may read "image 2 stands" as "image2stands" or count "2" as a quantity)
  - ❌ **Wrong:** `@image1 runs toward the gate` (no alias buffer)
- **Single camera move per slice.** Never combine push, pull, pan, tilt in the same slice.

#### Section C — Edit Instructions (video editing only)
Only include this section when the user is doing add / delete / modify / extend / stitch.

- **Add element:** `In @video1, between Ns–Ms in the [position], add [element]. Other content unchanged.`
- **Delete element:** `Remove [element] from @video1. Other content unchanged.`
- **Modify element:** `Replace [old element] in @video1 with [new element]; preserve original action and camera.`
- **Extend video (forward / backward):** `Extend @video1 forward/backward — [continuation description].` (Seedance auto-trims the seam; do not re-describe the existing footage.)
- **Stitch / track-fill:** `@video1, [transition description], cut to @video2.` (Up to 3 input videos, total ≤ 15s.)
- **On-screen text:** `Bottom of frame: subtitle "..." appears at Ns–Ms` (specify content, timing, position, appearance style; prefer common characters; avoid rare glyphs and special symbols).

#### Section D — Quality, Style & Constraint Pad
Always append a quality + safety pad:

> Style: [style cue from user, or "natural lighting, photoreal"]. 4K, rich detail. Faces stable and unwarped, five-sense features clear, no clipping, no extra limbs.

### 2. Issues Found

Itemize the concrete defects in the original prompt (e.g. "missing camera direction", "raw file path / URL / `video_id` inlined as a subject", "simultaneous push and pan", "ambiguous left/right between two characters", "rare glyphs in subtitle text").

### 3. Principles Applied

For each issue, name the Seedance prompt-engineering rule used to fix it. Use the canonical names below so users learn the vocabulary:

- **Positional Reference Binding** — bind every input asset (image path, URL, OSS path, or `video_id`) to a positional `@imageN` / `@videoN` label in Section A; only the label may appear in the action description.
- **Tokenizer Disambiguation** — every `@imageN` / `@videoN` is followed by a parenthetical or noun phrase to prevent digit-glue parse errors.
- **Single-Camera-Move-Per-Slice** — at most one camera operation (push / pull / pan / tilt / orbit) per time slice.
- **Three-Section Structure** — Setup → Shot Script → Constraints; edit instructions slot before constraints when applicable.
- **Verb Precision Over Adjective Stacking** — replace vague verbs with physical, specific ones.
- **Eight-Element Coverage** — audit subject / action / scene / light / camera / style / quality / constraints.
- **First-Last-Frame Anchoring** — when the user wants a specific opening or closing frame, declare anchors in Section A.
- **Common-Glyph Rule** — for on-screen text, prefer common characters; avoid rare glyphs and special symbols.

## Hard Constraints

- **No silent fixes.** Never auto-fill missing elements or auto-resolve camera conflicts without confirming with the user.
- **Mandatory safety pad.** Every final prompt MUST include the quality + anti-failure constraint pad.
- **Multi-character action scenes.** When two or more characters share the frame in dynamic action, lock positions explicitly ("left character wears a slate-blue jumpsuit", "right character is bareheaded") and prefer a fixed camera to prevent face-swapping or clipping.
- **Positional reference binding.** Raw paths, URLs, OSS paths, or `video_id` numbers must never appear in the action description. Bind each to a positional `@imageN` / `@videoN` label in Section A (matching the CLI flag order), then refer to the label only.
- **Tokenizer disambiguation.** No `@imageN` or `@videoN` may be immediately followed by a verb, preposition, or numeric word. Always insert an alias or noun.

## Examples

### Example 1 — Vague brief, no assets

**User prompt:** "Generate a Seedance video of a girl dancing"
**Model:** `seedance-2.0-standard`

**Response:** Enter Step 0 guided mode.

> Before I optimize, a few details: (1) What does the girl look like — outfit, hair, age? (2) Where is she dancing — neon street, classical stage, rooftop? (3) Style — photoreal, anime, oil painting? (4) Do you have a reference image to attach?

(Optimization waits until the user replies.)

---

### Example 2 — Multi-asset prompt with mapping ambiguity

**Planned CLI invocation:**
```
pixverse create reference --model seedance-2.0-standard \
  --images ./adrian.jpg ./mira.jpg \
  --prompt "..."
```

**User prompt text:** *"./adrian.jpg and ./mira.jpg walk together in the rain, dolly in and pan left, cinematic 4K"*

**Issues found:**
- Raw file paths (`./adrian.jpg`, `./mira.jpg`) inlined as subjects (Positional Reference Binding violation).
- No left/right position assignment between the two characters.
- Camera conflict: simultaneous dolly-in and pan-left (Single-Camera-Move-Per-Slice violation).
- "Cinematic 4K" is filler unless paired with concrete style + constraint pad.
- No light / color cue.

**Multi-select check sent to user:**
> ☐ Apply position: `@image1 (man)` on the left, `@image2 (woman)` on the right
> ☐ Resolve camera: keep dolly-in only
> ☐ Add lighting: cool rainy-night neon
> ☐ Other

**After user picks all three, Optimized Prompt:**

```
Section A — Setup
@image1 (1st in --images, ./adrian.jpg) is Adrian, a man in a black coat.
@image2 (2nd in --images, ./mira.jpg) is Mira, a woman in a red dress.
Scene: a rain-soaked downtown street at night, cool blue neon reflecting on wet asphalt.

Section B — Shot Script
0–4s: Medium shot. @image1 (Adrian) on the left and @image2 (Mira) on the right walk
side by side, shoulders almost touching, raindrops streaking through the streetlight.
Camera dollies in slowly.
4–8s: Close-up. @image2 (Mira) glances at @image1 (Adrian) and smiles faintly; he
returns the look without breaking stride. Camera holds.

Section D — Constraints
Style: photoreal, cool neon-noir lighting. 4K, rich detail. Faces stable and unwarped,
five-sense features clear, no clipping, no extra limbs.
```

**Principles applied:** Positional Reference Binding, Tokenizer Disambiguation, Single-Camera-Move-Per-Slice, Three-Section Structure, Eight-Element Coverage.

---

### Example 3 — Video editing (extend)

**Planned CLI invocation:** `pixverse create extend --model seedance-2.0-fast --video-id 987654 --prompt "..."`

**User prompt text:** *"extend video 987654, the truck falls and the driver jumps out"*

**Optimized Prompt:**

```
Section A — Setup
@video1 (source clip, video_id 987654) — a 5 s shot of a fire truck halted on a
tilting street, dust drifting up from the cracked asphalt.

Section C — Edit Instructions
Extend @video1 backward (forward in time). The continuation:
0–3s after seam: The rear axle of @video1 (the fire truck) drops over the crumbling
road edge; the truck pivots violently. The driver from @video1 (the firefighter at
the wheel) kicks the door open, jumps onto the tilting street, rolls once, grabs a
curb edge as the truck slides past him and drops into the void. Single tracking shot
following the driver.

Section D — Constraints
Style preserved from @video1. 4K, rich detail. Driver face stable and unwarped,
five-sense features clear, no clipping, no extra limbs.
```

**Principles applied:** Positional Reference Binding (the bare `987654` is bound to `@video1` in Section A; only the label is used in the body), Tokenizer Disambiguation, Verb Precision Over Adjective Stacking ("falls" → "drops over the edge, pivots"; "jumps out" → "kicks the door open, jumps, rolls, grabs"), Three-Section Structure with Edit Instructions.

## What This Skill Does NOT Do

- Select model variant (`seedance-2.0-standard` vs `seedance-2.0-fast`), quality, aspect ratio, or duration — see `pixverse:create-video`.
- Suggest multi-step workflows or pipelines.
- Auto-trigger during normal Seedance video generation.
- Add creative elements the user did not mention or confirm.
- Optimize prompts for non-Seedance models — use `pixverse:prompt-enhance` for V6.
