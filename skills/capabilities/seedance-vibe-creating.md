---
name: pixverse:seedance-vibe-creating
description: Shape emotional, atmospheric, memory-driven, or loosely expressed ideas into Seedance 2.0/2.5 prompts when the user wants creative rewriting. Preserve specified sound, scene progression, and technical constraints.
---

# Seedance Vibe Creating

Apply the [prompt editing contract](../references/prompt-contract.md). VC emphasizes the viewer's experience: imagery, emotion, rhythm, and continuity. For exact asset binding and engineered shot control, use [seedance-prompt-optimize](seedance-prompt-optimize.md). Parameter selection belongs to [create-video](create-video.md).

## Decide how much to change

| Input | Handling |
|---|---|
| A clear, mature emotional scene | Keep it or lightly clarify; do not rewrite merely to demonstrate activity. |
| Emotional idea with repetitive or mixed execution language | Rewrite only within the requested scope, preserving meaningful camera intent and supplied details. |
| Multi-shot sequence serving one feeling | Preserve beat order, scene relationships, dialogue, and requested structure. Numbering may be reformatted if the user did not require it. |
| Brand/character brief with some experiential content | Keep functional requirements; a more expressive version can be optional. |
| Abstract word without a visual anchor/action | Ask for the minimum missing direction, usually in one round. |
| Functional demo, execution shot list, or strict dialogue-synced drama | Keep the requested control; use precise prompt engineering where needed. |

Do not treat a supplied lens, camera move, or timing as disposable because the scene is emotional. Translate technical control only when the user requested that simplification, or provide an optional alternate version. Do not interrupt for missing decorative details when the scene already makes sense.

## Rewrite approaches

- **Narrative:** retain event order and emotional turns; use continuous prose or the supplied scene segments.
- **Emotion:** emphasize the supplied environment, rhythm, and texture without inventing a causal story.
- **Memory:** retain intentional gaps, recurring images, fading, or fragility; do not over-explain them.
- **Stream of consciousness:** preserve perceptible images and their internal relationship without forcing linear plot.
- **Multi-shot experience:** retain the visual motifs and progression across scenes; normally 1–3 sentences per beat suffice.
- **Hybrid cleanup:** remove repetition and explanations that do not belong in the generated scene; preserve useful structure and controls.

Keep length proportional to the input. Preserve dialogue, voiceover, music, sound effects, titles, and subtitles verbatim unless editing those is requested. Use the audio/text markup in [seedance-prompt-optimize](seedance-prompt-optimize.md#audio-and-displayed-text) when needed. Do not invent character relationships, props, plot twists, or emotional shifts.

## Output

Return the prompt, plus a short note if a meaningful transformation needs explanation. Do not expose classification labels or force Judgment/Action/Result sections. If the original already works, say so and retain it.

Example input: `A girl waits alone at a rainy bus stop at night; neon reflections; a long wait, lonely. Keep the slow dolly-in.`

Result: `Slow dolly-in on a girl waiting alone at a rainy bus stop at night. Neon reflections in the rain; the long wait feels lonely.`

For non-Seedance models, use [prompting-guide](prompting-guide.md), or [prompt-enhance](prompt-enhance.md) for V6.
