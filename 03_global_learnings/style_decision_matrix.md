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
| Opener / invitation | low–mid | _[Family A — e.g. sparse / intimate]_ | 10–25% | 55–70% | _[your winner when logged]_ |
| Boundary / decision | mid, firm | _[Family B — e.g. live band / punch]_ | 15–35% | 60–75% | _[your winner]_ |
| Hook / chant track | mid | _[Family B or C]_ | 25–45% | 65–78% | _[your winner]_ |
| Stillness / weight | low–mid | _[Family A]_ | 30–45% | 70–78% | _[your winner]_ |
| Joy / movement / dance | mid–high | _[Family C — e.g. groove / collective]_ | 45–60% | 74–82% | _[your winner]_ |
| Quiet landing / integration | low | _[Family A or E — e.g. soft / sparse]_ | 35–50% | 72–80% | _[your winner]_ |
| Mirror / confrontation | mid–high, sharp | _[Family D — e.g. raw / aggressive]_ | 55–65% | 80–85% | _[your winner]_ |
| Peak / closer | high | _[Family C or D]_ | 55–65% | 78–84% | _[your winner]_ |
| Gentle / child-safe | low | _[Family E — e.g. soft / minimal]_ | 10–20% | 55–70% | _[your winner]_ |

Replace family placeholders with yours from `01_artist/style_reference_summary.md`. Album roles are examples — name roles that fit *your* albums.

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
