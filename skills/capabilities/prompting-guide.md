---
name: pixverse:prompting-guide
description: Diagnose unclear or inconsistent video/image prompts and suggest focused improvements. Use for prompt advice; model-specific rewriting belongs to the V6 or Seedance optimizer.
---

# Prompting Guide

Follow the [prompt editing contract](../references/prompt-contract.md). This is an advisory capability: identify meaningful weaknesses, propose a revision, and explain the change. Advice alongside a generation request does not delay generation with the original wording.

## Checks

| Signal | Useful suggestion |
|---|---|
| Repetition or buried main action | Put subject, action, and setting first; trim repeated description. There is no universal word limit. |
| Vague style or quality adjectives | Name a concrete visual treatment when the user supplied one; otherwise offer a style choice without inventing it. |
| Conflicting camera instructions | Clarify genuinely incompatible directions. Preserve intentional coordinated moves. |
| Long lists of defects to avoid | Prefer a short positive description of the desired result where it preserves meaning. Do not claim all models lack negative conditioning. |
| Too many actions for the intended clip | Clarify the main beat or propose ordered shots; preserve explicitly requested speed and timing. |
| I2V prompt repeats the entire reference | Focus on requested motion and camera, retaining identity or appearance constraints needed for this task. |

Flag only meaningful issues, once. If no change is needed, proceed with the original; do not manufacture a critique.

For requested rewriting, use [prompt-enhance](prompt-enhance.md) for V6, [seedance-prompt-optimize](seedance-prompt-optimize.md) for precise Seedance control, or [seedance-vibe-creating](seedance-vibe-creating.md) for Seedance emotional/atmospheric shaping. For other models, provide model-agnostic advice without importing V6-specific flags.
