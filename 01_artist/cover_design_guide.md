# Cover Design Guide

Generic principles for album art. Each release gets its own identity — don't clone one layout onto another.

## Core principles

1. **One visual anchor** — sun, horizon, figure, object — something the eye returns to.
2. **Album-specific identity** — read `visual_direction.md` per project; families are starting points, not copies.
3. **Text in post when possible** — generate image without typography; add title and artist name in design tool.
4. **Warm, human, not stock** — avoid wellness clichés, religious iconography, glossy pop aesthetic, neon cyber.

## Cover prompt families

Templates in `04_templates/`:

| Family | Template | Best for |
|--------|----------|----------|
| Nature / trust | `cover_prompt_nature_trust.md` | Gentle, hopeful, child-safe, oneness |
| Single photo | `cover_prompt_single_photo.md` | Singles, live moment, documentary feel |
| Custom | `cover_prompt_template.md` | Build from scratch |

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
