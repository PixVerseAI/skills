# Prompt editing contract

Read this when diagnosing or rewriting generation prompts. Model syntax belongs in the relevant capability; command execution follows [execution-contract.md](execution-contract.md).

- A generation-only request uses the supplied prompt unchanged. You may offer a material improvement once without blocking authorized generation. Do not turn silence into acceptance of a rewrite.
- An explicit request to improve, optimize, or shape the prompt authorizes that rewrite. “Optimize and generate” authorizes using the result in the requested generation; do not ask for the same approval again. If only advice was requested, return advice without generating.
- Preserve named subjects, actions, scene, style, dialogue, timing, reference roles, and explicit technical requirements. Sharpen wording without adding unrequested objects, plot, emotional changes, or lighting. Missing decorative detail is not a reason to ask questions.
- Ask only for an ambiguity that prevents the requested result: unresolved asset identity/role, incompatible explicit requirements, or an abstract idea with no usable visual subject or action. A coordinated camera move is not inherently contradictory (for example, a dolly zoom); distinguish intentional combinations from incompatible movement requirements.
- Generic quality words and negative phrasing are not universal model failures. Remove repetition when rewriting, prefer concrete visual instructions, and use model-specific guidance only within its scope. Never add mandatory quality, logo, subtitle, twin, or motion pads. A constraint must suit the scene and preserve user intent, including intentional twins, uniforms, logos, or text.
- Return the result and a brief explanation of material changes when useful. Show original/suggested comparison for advice or when requested; do not repeat the entire original by default. Preserve exact spoken or displayed text unless the user asks to edit it.
