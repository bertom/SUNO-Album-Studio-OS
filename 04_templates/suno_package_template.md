# SUNO Package Template

Use for `/suno`. Deliver **only** the blocks below when the user wants copy-paste output — no commentary inside fields.

Reference: `00_system/suno_song_preparation_guide_v2.md`

---

## Metadata (file header only — not copied to SUNO)

```markdown
<!-- track:  | prompt: v1 | date: YYYY-MM-DD | hypothesis:  -->
```

---

## Required Output Structure

### Lyrics

```text
[Verse 1]


[Chorus]


[Verse 2]


[Chorus]


[Bridge]


[Final Chorus]


[Outro]

```

**Rules:** Section tags only. No production notes. Short singable lines. Parentheses for call-response.

---

### Styles

```text

```

**Rules:** One compact paragraph. Concrete genre, rhythm, instruments, vocal, production, emotional tone, energy arc. Positive language only. No artist names. **No studio/album/song references or internal shorthand** (e.g. "studio warmth shorthand," "Family-like") — SUNO has no repo context; translate to musical terms. See guide § "Avoid References SUNO Cannot Know."

---

### More options

(Section header only — fields follow)

---

### Exclude styles

```text
EDM, trap, heavy autotune, metal, harsh synths, cinematic trailer music, musical theatre, glossy modern pop, comedy novelty
```

**Rules:** Concise comma-separated list. Customize per song/album.

---

### Vocal Gender

M

(or F)

---

### Weirdness %

15%

**Document rationale in file header.** Typical ranges: 10–25% precision songs, 35–60% joyful collective, 15–30% album-consistent roots.

---

### Style influence %

65%

**Document rationale in file header.** Typical: 55% balanced, 60–70% album consistency, 65–75% specific goals.

---

## Pre-Flight Checklist

- [ ] Lyrics fenced in `text` block
- [ ] Styles fenced — no negative instructions; **no artist, album, or studio-only references**
- [ ] Exclude styles fenced — concise
- [ ] Song Title fenced
- [ ] Field order exact: Lyrics → Styles → More options → Exclude → Vocal → Weirdness → Style influence → Title
- [ ] One rhythmic center
- [ ] One emotional center
- [ ] At least two artist DNA markers identifiable in Styles — expressed as **concrete musical terms**, not project names
- [ ] Saved as `suno/suno_prompt_vN.md`

---

## Example Minimal Package

### Lyrics

```text
[Verse 1]
I wake up slow
The light is on the floor

[Chorus]
Het komt goed
Het komt goed
Adem in
Adem door

[Outro]
Het komt goed
```

### Styles

```text
warm acoustic folk with gentle reggae sway, soft bass pulse, light hand percussion, intimate sincere Dutch female vocal, organic room sound, calm and reassuring, space between phrases, gradual warmth in chorus
```

### More options

### Exclude styles

```text
EDM, trap, heavy autotune, metal, cinematic trailer music, musical theatre, glossy pop, aggressive rock
```

### Vocal Gender

F

### Weirdness %

15%

### Style influence %

62%

### Song Title

```text
Het komt goed
```
