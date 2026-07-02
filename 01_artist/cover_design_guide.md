# Cover Design Guide

Generic principles for album art. Each release gets its own identity — don't clone one layout onto another.

## Core principles

1. **One visual anchor** — sun, horizon, figure, object — something the eye returns to.
2. **Album-specific identity** — read `visual_direction.md` per project; families are starting points, not copies.
3. **Text in post when possible** — generate image without typography; add title and artist name in design tool.
4. **Warm, human, not stock** — avoid wellness clichés, religious iconography, glossy pop aesthetic, neon cyber.

## Cover prompt families *(examples — not a fixed menu)*

The templates in `04_templates/` are **starter scaffolds**, not rules. Every artist's visual taste differs.

**You can:**
- Use a preset as-is, then fill from `visual_direction.md`
- **Edit** a preset file to match your recurring look (e.g. always typographic, always illustrated)
- **Add** your own family — e.g. `04_templates/cover_prompt_brutalist_type.md` — and reference it from this guide
- Skip families entirely and use `cover_prompt_template.md` per album

Document your go-to families in **Your visual preferences** below so agents stop guessing.

| Family *(example)* | Template | Starting point for |
|--------------------|----------|-------------------|
| Gentle landscape | `cover_prompt_gentle_landscape.md` | Calm, open, hopeful |
| Documentary photo | `cover_prompt_documentary_photo.md` | Singles, live moment, real photo |
| Custom | `cover_prompt_template.md` | One-off or new family from scratch |

## Workflow

1. Read album `visual_direction.md` and `album_art/cover_notes.md`.
2. Run **`/cover prompt`** — outputs `cover_prompt_vN.md`.
3. Generate image; save final as `album_art/cover.png`.
4. Document why this cover in `cover_notes.md`.

## Avoid on all covers

Religious iconography, stock wellness clichés, glossy pop, neon/cyber, random concept art that doesn't match the album's story.

## Your visual preferences

<!-- Add after onboarding -->

- _[e.g. prefer natural light over illustrated]_
- _[e.g. muted earth tones]_
