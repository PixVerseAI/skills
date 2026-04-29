---
name: pixverse:character-design
description: Create and reuse persistent characters for stories and series. Generates a three-view character sheet (front/side/back + head detail + accessories) and saves it locally so subsequent image or video generations can reuse the same character via reference-image workflows.
---

# Character Design

Design a fixed, reusable character for a project — generate a high-quality three-view character sheet once, save it locally, and reuse it as a reference image for every later scene. Keeps characters visually consistent across a story, series, or campaign.

## When to Use

- The user wants to **create a persistent character** that will appear in multiple later generations.
- The user is starting a **story / series / campaign** and needs one or more anchor characters before generating scenes.
- A later request **cues** a previously-saved character (by name) and needs the reference image piped into a new image or video generation.

This skill **does not** orchestrate full stories — it only creates and serves character references. Downstream generation happens through the standard `pixverse create image` / `pixverse create reference` commands, with this skill resolving the character name to a reference image path.

---

## Decision Tree

```
Need a character?
├── Does the project already track characters?
│   ├── No   → ask user for a characters directory path, initialize .pixverse/characters.json
│   └── Yes  → read .pixverse/characters.json → resolve characters_dir
├── Creating a new character?                    → action: create
├── Listing existing characters?                  → action: list
├── Inspecting one character?                     → action: show <name>
└── Reusing a character in a new generation?     → action: use <name> --for image|video "<scene prompt>"
```

---

## Sub-Actions

| Action | Purpose |
|:---|:---|
| `create` | Collect character fields, generate the three-view sheet, save locally |
| `list` | Print all saved characters in the project |
| `show <name>` | Print metadata and file paths for one character |
| `use <name> --for image "<prompt>"` | Run I2I using `reference.png` as the reference |
| `use <a>,<b>[,<c>…] --for video "<prompt>"` | Run multi-subject video via `pixverse create reference` |

---

## Storage Layout

### Pointer config (per project)

`./.pixverse/characters.json` at the project root:

```json
{
  "version": 1,
  "characters_dir": "./characters"
}
```

- Created on first `create` when the file is missing. Ask the user to confirm or override the default `./characters` path.
- `characters_dir` may point outside the repo (e.g., `~/Creative/project-x/characters`) — always store the value as the user typed it; resolve to an absolute path at read time.
- Commit `.pixverse/characters.json` so teammates cloning the project inherit the same pointer.

### Per-character folder

```
<characters_dir>/
└── <slug>/
    ├── reference.png   # full three-view character sheet (NEVER sent directly to I2V)
    └── meta.json       # structured metadata
```

`meta.json` schema:

```json
{
  "slug": "alice",
  "name": "Alice",
  "created_at": "2026-04-22T12:00:00Z",
  "fields": {
    "short_description": "A cheerful apprentice wizard",
    "age": 17,
    "gender": "female",
    "species": "human",
    "appearance": "silver shoulder-length hair, violet eyes, slim build",
    "outfit": "navy wizard robe with silver trim",
    "accessories": "leather-bound spellbook, small owl familiar",
    "personality": "curious and mischievous",
    "style_tags": "Studio Ghibli"
  },
  "source_prompt": "Ultra-high-detail Studio Ghibli style. A cheerful apprentice wizard. …",
  "generation": {
    "model": "gemini-3.1-flash",
    "quality": "1440p",
    "aspect_ratio": "16:9",
    "image_id": 398819693367838,
    "image_url": "https://media.pixverse.ai/…"
  }
}
```

---

## Character Fields (Hybrid)

| Field | Required | Notes |
|:---|:---|:---|
| `name` | yes | Display name; slugified for the folder name |
| `short_description` | yes | One-line anchor, e.g. `"A cheerful apprentice wizard"` |
| `age` | no | Integer or descriptor, e.g. `17` or `"middle-aged"` |
| `gender` | no | `female` / `male` / `non-binary` / free-form |
| `species` | no | Defaults to `human` if omitted |
| `appearance` | no | Hair, eyes, build, distinguishing features |
| `outfit` | no | Primary clothing description |
| `accessories` | no | Items, familiars, props |
| `personality` | no | Personality descriptor / vibe |
| `style_tags` | no | Art style, e.g. `"Studio Ghibli"`, `"cyberpunk"`, `"photoreal"` |

Collect required fields first, then offer optional fields one at a time (or in a single summary prompt for batch/agent use). Skip any field the user leaves blank — do not insert placeholders.

---

## Prompt Template

`{DESCRIPTION}` is assembled by joining the provided fields in this order, skipping any that are empty:

```
Ultra-high-detail {style_tags}. {short_description}.
{age}-year-old {gender} {species}.
{appearance}. Wearing {outfit}. {accessories}. {personality}.
```

Then wrapped in the fixed layout instruction:

```
{DESCRIPTION}

Three-view character sheet layout: front full-body view, side full-body view,
and back full-body view aligned in a row; enlarged head-and-face detail on
the far left; clothing details and accessories showcase strip displayed below
the character views. Neutral light-gray studio background. Overall composition
is neat, balanced, symmetrical, and professional.
```

### Example (all fields filled)

```
Ultra-high-detail Studio Ghibli style. A cheerful apprentice wizard.
17-year-old female human.
Silver shoulder-length hair, violet eyes, slim build. Wearing a navy wizard
robe with silver trim. Carrying a leather-bound spellbook and accompanied by
a small owl familiar. Curious and mischievous vibe.

Three-view character sheet layout: front full-body view, side full-body view,
and back full-body view aligned in a row; enlarged head-and-face detail on
the far left; clothing details and accessories showcase strip displayed below
the character views. Neutral light-gray studio background. Overall composition
is neat, balanced, symmetrical, and professional.
```

---

## Create Flow

1. **Resolve config.** Read `./.pixverse/characters.json`. If missing, ask the user for a `characters_dir` (default `./characters`), then write both the config and the directory.
2. **Collect fields.** Prompt for the two required fields; walk through optional fields. Accept flag-based input for agent/headless use.
3. **Compute slug.** `slugify(name)` (lowercase, hyphenated). If `<characters_dir>/<slug>/` already exists, auto-version: `<slug>-2`, `<slug>-3`, …
4. **Assemble prompt** using the template above.
5. **Generate the sheet:**
   ```bash
   pixverse create image \
     --prompt "<assembled prompt>" \
     --model gemini-3.1-flash \
     --quality 1440p \
     --aspect-ratio 16:9 \
     --json
   ```
6. **Download & save:**
   - Create `<characters_dir>/<slug>/`.
   - Download `image_url` to `<characters_dir>/<slug>/reference.png`.
   - Write `meta.json` with all field values, the assembled `source_prompt`, and the `generation` block from the CLI response.
7. **Report** the resolved slug, local paths, and the `image_id` for future reference.

### Defaults (locked)

| Parameter | Value | Rationale |
|:---|:---|:---|
| Model | `gemini-3.1-flash` | Best layout adherence for multi-panel character sheets (same model used by `storyboard-to-video`) |
| Quality | `1440p` (2K) | Enough resolution for each panel to serve as a usable reference later |
| Aspect ratio | `16:9` | Three full-body views plus a head column fit a wide frame |

Override knobs should be exposed as flags for power users, but defaults should not be changed without a reason.

---

## Use Flow

> **Core rule:** the saved `reference.png` is a *reference image* only. It must **never** be passed directly to an I2V (image-to-video) command, because an I2V call would animate the character-sheet layout itself. Always route through I2I or `create reference`.

### `use <name> --for image "<scene prompt>"`

Produce a new scene image featuring the character:

```bash
pixverse create image \
  --image "<characters_dir>/<slug>/reference.png" \
  --model gemini-3.0 \
  --quality 1440p \
  --aspect-ratio 16:9 \
  --prompt "Same character from the reference sheet. <scene prompt>" \
  --json
```

**Model note:** I2I with `gemini-3.1-flash` is currently rejected by the API for this reference-image workflow; use `gemini-3.0` (Nano Banana Pro) for the I2I step. The three-view sheet (T2I) still uses `gemini-3.1-flash`.

**Prompt construction:** Always prefix the user's scene prompt with a short anchor line that names the most visually distinctive traits from `meta.json.fields` (e.g., `"Same character from the reference sheet — silver shoulder-length hair, violet eyes, navy wizard robe with silver trim. <scene prompt>"`). This preserves character fidelity across scenes.

### `use <name1>[,<name2>,…] --for video "<scene prompt>"`

Generate a multi-subject video with character fusion:

```bash
pixverse create reference \
  --images "<characters_dir>/<slug1>/reference.png" "<characters_dir>/<slug2>/reference.png" \
  --prompt "<scene prompt>" \
  --json
```

`pixverse create reference` requires **two or more** images. For a single character in a video, generate a scene still first with `use --for image`, then feed that still into `pixverse create video --image <still>`.

---

## List / Show

- **`list`**: scan `<characters_dir>/*/meta.json` and print `slug | name | short_description | created_at` rows.
- **`show <name>`**: print the full `meta.json` plus absolute paths to `reference.png` and `meta.json`. Resolve `<name>` by exact slug match first, then by case-insensitive name match; error on ambiguity.

---

## Collision Handling

If a user runs `create` with a name that slugifies to an existing folder:

- Auto-version: save as `<slug>-2`, `<slug>-3`, etc.
- The new `meta.json` should reference the same `name` but a unique `slug`.
- `list` and `show` treat each version as an independent character.

---

## Error Recovery

| Step | Failure | Recovery |
|:---|:---|:---|
| Config | `.pixverse/characters.json` points to a missing directory | Ask user to confirm or update `characters_dir` |
| Step 5 | Image generation fails (exit 5) | Offer to retry; suggest simplifying `short_description` or dropping conflicting `style_tags` |
| Step 6 | Download fails | Retry once; if still failing, keep the `image_url` in `meta.json` so the user can download manually |
| `use --for image` | I2I returns `invalid param` (400017) | Confirm `--model gemini-3.0` is set and the reference file exists; retry |
| `use --for video` | Only one character provided | Error clearly: suggest adding a second character or using `--for image` then I2V on the result |

---

## Out of Scope (v1)

- Auto-splitting the three-view sheet into front/side/back/head crops.
- Auto-detecting character names in free-form prompts (recall by fuzzy match).
- Editing or regenerating an existing character without collision-bumping the slug.
- Integration into `pixverse:storyboard-to-video` — that workflow stays untouched; users manually invoke `use --for image` to pre-generate scene stills before storyboarding.

---

## Related Skills

- `pixverse:create-and-edit-image` — underlying T2I / I2I command reference
- `pixverse:create-video` — how to animate a scene still produced by `use --for image`
- `pixverse:motion-control` — apply a motion reference to a character-anchored scene still
- `pixverse:prompt-enhance` — refine scene prompts before passing to `use`
