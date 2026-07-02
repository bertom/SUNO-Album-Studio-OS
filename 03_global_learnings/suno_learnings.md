# SUNO Learnings

Cross-album SUNO behavior — mechanics that apply to any musician.

Add project-specific notes via **`/extract learning`**.

---

## Call-response in parentheses

SUNO reads `(yeah)`, `(oh)`, `(come on now)` in lyrics as backing vocals. Prefer parentheses over `[Backing vocals]` tags.

**Action:** Use sparingly for lift; don't stack too many in one section.

---

## Exclude lists matter

Concise exclude lists dramatically help consistent sound.

**Baseline (append to most packages):**
```text
EDM, trap, electronic dance, synth pop, heavy autotune, cinematic trailer, musical theatre, glossy modern pop, comedy novelty
```

---

## Positive Styles only

Never put exclusions in Styles (`no dub`, `without trap`). Use **Exclude styles** field.

**Pre-flight:** `/suno validate` or `./studio-suno validate`

---

## Sensitive words

| Word | Issue | Use instead |
|------|-------|-------------|
| `skank` | SUNO filter | offbeat rhythm guitar chop, skanking guitar pattern *(in agent notes only — prefer descriptive production terms in Styles)* |

---

## Weirdness % and Style influence %

| Brief type | Weirdness | Style influence |
|------------|-----------|-----------------|
| Precision / intimate | 15–35% | 65–75% |
| Standard album track | 35–50% | 70–78% |
| Joyful collective | 45–60% | 74–82% |
| Confrontation peak | 55–65% | 80–85% |

Outliers vs `song_brief.md` role → `/suno validate` warns.

---

## Mantra / outro extensions

SUNO sometimes extends mantra lines in outros — can be a feature if the line is strong.

**Action:** Listen for drift; retry with tighter lyrics or lower weirdness if it morphs words.

---

## Settings Quick Reference

See `03_global_learnings/style_decision_matrix.md` for role-based starting points.

Log your proven W/SI pairs in `05_catalog/best_suno_outputs.md`.
