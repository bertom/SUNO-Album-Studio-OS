# Cover Prompt Template

Master structure for album/single cover briefs. Use with **`/cover prompt`**.

Guide: `01_artist/cover_design_guide.md`

---

## Family presets

Pick one starting point from `04_templates/`:

| Family | Template | Best for |
|--------|----------|----------|
| Nature / trust | `cover_prompt_nature_trust.md` | Gentle, hopeful, child-safe |
| Single photo | `cover_prompt_single_photo.md` | Singles, live moment |
| Custom | This template | Build from album `visual_direction.md` |

---

## Brief structure (fill per version)

### Metadata

- **Album / single:**
- **Artist:** _[Your artist name]_
- **Cover family:**
- **Version:** vN

### Visual anchor (required — define per album)

Describe the recurring visual element for *this* release (horizon, figure, object, light source — album-specific).

### Composition

- Framing:
- Text zone (usually lower third — type in post):
- Key elements:

### Palette & mood

- Colors:
- Texture / medium (photo, illustration, mixed):
- Emotional tone:

### Image prompt (copy-paste)

```text

```

### Negative prompt

```text
text, letters, watermark, logo, religious symbols, neon, cyberpunk, stock wellness cliché,
oversaturated, harsh flash, random concept art
```

### Exclude baseline

Always include baseline excludes plus family-specific items from the preset.

---

## Guardrails

1. **Album-specific identity** — read `visual_direction.md`; don't clone another project's layout.
2. **Family fidelity** — use the matching family template; do not blend families unless the user asks.
3. **Typography** — usually post-production; omit readable text from image prompts unless exploring type-in-image.
4. Save as `album_art/cover_prompt_vN.md` — never overwrite prior versions.
