---
name: pixverse:mondo-poster-design
description: Design Mondo-inspired posters, book covers, and album covers using a curated artist-style library, genre templates, and composition patterns with PixVerse image generation.
---

# Mondo Poster Design

Create symbolic, illustrated poster art with deliberate palette, composition, and print texture. Start from the user's format and creative intent; use a restrained screen-print look by default, while honoring painterly, portrait, maximalist, or contemporary styles when selected.

> Based on [qiaomu-mondo-poster-design](https://github.com/joeseesun/qiaomu-mondo-poster-design) by [@vista8](https://x.com/vista8). The original artist library, compositions, and genre templates are his work; this adaptation uses PixVerse generation and optional video animation.

## Build the prompt

```text
[artist/style treatment] + [subject or symbolic concept] + [composition] +
[palette] + [medium/texture] + [format and requested text]
```

Read only the relevant reference sections:

- [Artist styles](../references/mondo-poster/artist-styles.md): choose by name or use its genre index; keep one dominant treatment, optionally borrowing one complementary technique.
- [Composition patterns](../references/mondo-poster/composition-patterns.md): choose layout, negative space, silhouette, framing, or typography as the subject requires.
- [Genre templates](../references/mondo-poster/genre-templates.md): use the matching film/book/album section as a starting point, not an extra mandatory prompt appended verbatim.

Use concrete palette names and purposeful symbols. Two to four colors and halftone/paper texture suit screen-print work, but are preferences, not restrictions on all styles. Match the requested artist/era rather than forcing every design into the 1960s–1980s. Preserve supplied title and author text; do not invent credits or substitute a silhouette when a portrait is requested.

## Generate

Use [create-and-edit-image](create-and-edit-image.md) for current models, qualities, regions, and reference limits. For a poster, prefer a model supporting the requested ratio and detail level; `gemini-3.1-flash` is one option for detailed line work, `seedream-5.0-lite` for an illustrated treatment, and `qwen-image` for a lower-resolution draft. Filter by region before calling. Draft-then-final is optional, not an automatic second paid generation.

Common formats: movie/book cover `2:3`, album cover `1:1`, social post `4:5` or `1:1`, horizontal art `3:2` or `16:9`. Match exact print dimensions when requested; 12×36 inches is 1:3, not 9:16. If a model lacks the target ratio, generate an appropriate source and explain the required crop/layout preparation.

```bash
pixverse create image \
  --prompt "Saul Bass-inspired noir poster, detective silhouette in fedora, centered single figure, three-color screen print: deep blue, cream, red accent; geometric negative space and halftone texture; 1940s noir atmosphere" \
  --model gemini-3.1-flash --quality 2160p --aspect-ratio 2:3 --json
```

For transforming existing art, supply `--image <input>` and state the requested style changes while preserving required content. For multiple requested variations, use supported `--count` and vary the creative dimension deliberately; do not promise different seeds unless set or observed.

Follow [execution-contract](../references/execution-contract.md) for completion, retries, and delivering assets. Use [asset-management](asset-management.md) for download; do not duplicate generic error tables here.

## Workflows

- [mondo-poster-pipeline](../workflows/mondo-poster-pipeline.md): full poster creation when a workflow is needed.
- [mondo-poster-to-video-pipeline](../workflows/mondo-poster-to-video-pipeline.md): animate a poster when requested.
- [image-editing-pipeline](../workflows/image-editing-pipeline.md): iterative I2I refinement.
