---
name: pixverse:prompt-enhance
description: Rewrite prompts for PixVerse V6 when the user explicitly asks to enhance, improve, or optimize them. Covers text-to-video and image-to-video prompt text.
---

# V6 Prompt Enhance

Apply the [prompt editing contract](../references/prompt-contract.md). State briefly when applying this optimizer. Normal generation requests do not auto-trigger rewriting.

## Rewrite

1. Order supplied information as subject → action → scene → camera → lighting/style, omitting missing elements.
2. Remove repetition and generic boosters that add no intended style information. Preserve meaningful aesthetic terms: a requested render style is not automatically filler.
3. Make action wording precise without selecting a new action, prop, setting, or narrative. “A person walks steadily forward” can become “A person strides steadily forward”; “he escapes” does not authorize inventing a door or a pavement roll.
4. For I2V, let the image supply appearance and emphasize requested motion. Do not add a breeze or camera move to fill space.
5. If the user supplied distinct sequential beats, organize them into shots. Preserve requested timing; when timing was not given, shot order is sufficient. Avoid inventing transitions or additional beats.

Return the enhanced prompt and a brief note about meaningful changes. Prompt optimization does not select CLI flags. For model support, duration, audio, and multi-shot settings, use [create-video](create-video.md); a single-shot or silent request should not acquire `--multi-shot` or `--audio` because it was optimized.

## Examples

- Input: `cinematic 4K, a woman dancing in the rain, dancing in the rain, masterpiece`.
  Result: `A woman dancing in the rain, cinematic style.` Explain that repetition and resolution/quality labels were removed; retain the requested style unless the user wants it replaced.
- Input: `a boy and a girl at the beach, fighting, then close-up on the boy, the boy cries`.
  Result: `Shot 1: A boy and a girl fighting at the beach. Shot 2: Close-up of the boy as he cries.`

For Seedance, use [seedance-prompt-optimize](seedance-prompt-optimize.md). For other models, use [prompting-guide](prompting-guide.md) rather than applying V6 assumptions.
