# Style Decision Matrix

Lightweight routing: **album role + energy → starting family → settings hint → catalog winners**.

Use during `/style directions`, orchestrator phase 6c, and `/suno validate` (settings sanity). Starting point only — always adapt to `song_brief.md`.

Full families: `01_artist/style_reference_summary.md`  
Proven blocks: `03_global_learnings/reusable_style_recipes.md`  
Winners with W/SI: `05_catalog/best_suno_outputs.md`

---

## Matrix

| Album role | Energy | Starting family | Weirdness | Style influence | Catalog anchor(s) |
|------------|--------|-----------------|-----------|-----------------|-------------------|
| Opener / invitation | low–mid | Intimate Acoustic *(example — replace)* | 10–25% | 55–70% | _[your winner when logged]_ |
| Boundary / decision | mid, firm | Live Band Pulse *(example)* | 15–35% | 60–75% | _[your winner]_ |
| Mantra / consciousness | mid | Live Band Pulse *(example)* | 25–45% | 65–78% | _[your winner]_ |
| Prophetic / still | low–mid | Intimate Acoustic *(example)* | 30–45% | 70–78% | _[your winner]_ |
| Joy / movement / dance | mid–high | Collective Groove *(example)* | 45–60% | 74–82% | _[your winner]_ |
| Soft healing / integration | low | Intimate Acoustic *(example)* | 35–50% | 72–80% | _[your winner]_ |
| Mirror / confrontation | mid–high, sharp | Raw Live *(example)* | 55–65% | 80–85% | _[your winner]_ |
| Ecstatic peak / closer | high | Collective Groove *(example)* | 55–65% | 78–84% | _[your winner]_ |
| Gentle / child-safe | low | Acoustic / Soft *(example)* | 10–20% | 55–70% | _[your winner]_ |

Replace example family names with yours from `01_artist/style_reference_summary.md`.

---

## Energy curve template (album design)

Sketch before locking the song pool — map tracks to slots, not just titles:

```text
enter (low) → build → peak → mirror → release → land
```

`variation_map.md` should reflect this arc. Orchestrator runs `/album check` before `draft-ready`.

---

## Global exclude baseline

Add to every option's exclude list; extend per album in `style_reference_summary.md`:

```text
EDM, trap, electronic dance, synth pop, heavy autotune, cinematic trailer, musical theatre, glossy modern pop, comedy novelty
```

### Per-album excludes *(example — customize per project)*

| Album type | Also exclude |
|------------|--------------|
| Acoustic-forward | heavy metal, dubstep, club beats |
| Live band | tropical house, hyperpop, trailer orchestral |
| Raw / confrontational | theatrical rage, comedy novelty, glossy studio pop |

Document album-specific excludes in `album_identity.md` or track `style_directions.md`.

---

## Validation flags (for `/suno validate`)

| Flag | When |
|------|------|
| Weirdness > 60% on precision/mirror brief | Warn — check brief; exception: intentional confrontation peak |
| Weirdness < 25% on joyful collective brief | Warn — may sound flat |
| Style influence < 60% | Warn — album drift risk |
| No exclude block | Warn — EDM/trap bleed likely |
| Negative words in Styles (`no dub`, `without`) | Error — use Exclude styles |
| Studio shorthand in Styles (`Family-like`, project name) | Error — translate to concrete terms |

Settings reference: `03_global_learnings/suno_learnings.md` § Settings Quick Reference.
