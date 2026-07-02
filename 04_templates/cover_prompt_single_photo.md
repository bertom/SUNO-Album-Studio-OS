# Cover Prompt — Single Photo Family

Concert moment, documentary feel, real photography energy.

Used for: **singles** and releases where a captured live moment *is* the cover.

Guide: `01_artist/cover_design_guide.md`

---

## Family defaults

| Field | Default |
|-------|---------|
| Source | Real photo preferred over generation |
| Composition | Performer or crowd moment; space for title in post |
| Texture | Natural grain, stage light, motion blur acceptable |
| Palette | Whatever the moment gives — avoid over-grading |
| Typography | Minimal; artist name in metadata only for singles |
| Mood | Present, alive, unposed |

---

## When generation is fallback

If no usable photo exists, describe the **moment** not the artist:

```text
documentary concert photography, singer on small stage, warm tungsten light,
crowd silhouettes, shallow depth of field, motion in hands, authentic sweat and room,
no text, no watermark, photorealistic
```

## Negative prompt

```text
text, logo, watermark, stock photo smile, glossy pop aesthetic, religious symbols,
neon cyberpunk, illustrated cartoon, oversized lens flare
```

---

## Workflow

1. Try real photo first — generation is fallback.
2. Final cover → `album_art/cover.png`.
3. Document choice in `cover_notes.md`.

Version files: `album_art/cover_prompt_vN.md`
