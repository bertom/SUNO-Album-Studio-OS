# Cover Prompt — Documentary Photo Family

Real moment, real light — performance, portrait, session, or street; not illustrated concept art.

**Use when:** the cover *is* a photograph (or should feel like one): singles, live energy, or “this happened.”

Guide: `01_artist/cover_design_guide.md`

---

## Before you generate

| Field | Your release (fill in) |
|-------|------------------------|
| Subject | _[performer, hands on instrument, crowd slice, portrait — from visual_direction.md]_ |
| Setting | _[venue, studio, street, home — specific]_ |
| Light | _[tungsten stage, window daylight, flash — one source]_ |
| Mood | _[present, raw, celebratory, intimate]_ |

**Prefer:** a real photo you own → `album_art/cover.png`. Use generation only as fallback.

---

## Composition defaults

| Field | Starting point |
|-------|----------------|
| Framing | Subject off-center or mid-action; space for title in post |
| Texture | Natural grain, motion blur OK if honest |
| Palette | What the moment gives — light grade in post, not neon polish |
| Typography | Title in post; artist name in metadata for singles |

---

## Image prompt skeleton

Describe **this** moment — not a generic stock concert:

```text
documentary photography, [subject and action], [setting],
[light description], shallow depth of field, authentic room and skin texture,
no text, no watermark, photorealistic
```

### Example *(replace entirely)*

```text
documentary photography, musician mid-song at small club, warm tungsten stage light,
crowd silhouettes soft in background, shallow depth of field, motion in hands,
no text, no watermark, photorealistic
```

## Negative prompt

```text
text, logo, watermark, stock photo smile, glossy pop aesthetic, religious symbols,
neon cyberpunk, illustrated cartoon, oversized lens flare, AI glamour portrait
```

---

## Workflow

1. Real photo first — generation is fallback.
2. Final → `album_art/cover.png`.
3. Why this image → `cover_notes.md`.

Version files: `album_art/cover_prompt_vN.md`
