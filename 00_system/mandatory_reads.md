# Mandatory Reads — Context Routing

Agents **must** read the files listed for their current task before producing output. Optional reads are helpful; mandatory reads are not negotiable under time pressure.

> Smarter = the right archive slice at the right moment — not reading everything every time.

---

## Always (any session)

| File | Why |
|------|-----|
| `00_system/project_instructions.md` | Role, non-negotiables, authoritative docs |
| `01_artist/artist_dna.md` | Artist body — identity over genre |

**First-run:** if DNA is still placeholder, run **`/onboard artist`** first.

---

## By command / phase

### `/onboard artist`

| Read |
|------|
| All templates in `01_artist/`, `01_artist/README.md`, `ONBOARDING.md` |

### `/orchestrate album` · Album Orchestrator

| When | Read |
|------|------|
| Start | This file, `00_system/album_orchestrator.md`, `00_system/agent_roles.md`, all `input/*` |
| Album world (phase 2) | `01_artist/style_reference.md`, `01_artist/artist_identity.md`, `03_global_learnings/album_learnings.md` |
| Song pool | `03_global_learnings/style_decision_matrix.md`, `album_arc.md` |
| Each track — style (6c) | `01_artist/style_reference_summary.md`, `03_global_learnings/reusable_style_recipes.md`, `05_catalog/style_index.md`, **2–3 rows from `05_catalog/best_suno_outputs.md`** matched by role/energy (if populated) |
| Each track — SUNO (6d) | `00_system/suno_song_preparation_guide_v2.md`, `03_global_learnings/suno_learnings.md`, `03_global_learnings/failed_patterns.md` |
| Final assembly (phase 7) | `variation_map.md`, all `song_brief.md`, run `/album check` rubric in `commands.md` |

### `/album seed` · `/album world` · `/song pool`

Same as orchestrator phases 1–5 above for the relevant step.

### `/song brief`

| Read |
|------|
| `04_templates/song_brief_template.md`, `album_identity.md`, `album_arc.md`, `track_map.md`, `01_artist/artist_dna.md` |

### `/style directions`

| Read |
|------|
| `song_brief.md`, `01_artist/sonic_palette.md`, `01_artist/style_reference_summary.md`, `03_global_learnings/style_decision_matrix.md`, `03_global_learnings/reusable_style_recipes.md`, `05_catalog/style_index.md`, `05_catalog/best_suno_outputs.md` (match 2–3 winners by role/energy when populated) |

**Action:** Pick a **starting family** from the matrix — then adapt. Do not invent from scratch when a proven row exists in the user's catalog.

### `/lyrics`

| Read |
|------|
| `song_brief.md`, `01_artist/lyric_principles.md`, latest `lyrics/*.md`, `03_global_learnings/lyric_learnings.md` |

### `/suno`

| Read |
|------|
| `song_brief.md`, latest `lyrics/lyrics_v*.md`, `suno/style_directions.md`, `00_system/suno_song_preparation_guide_v2.md`, `03_global_learnings/suno_learnings.md`, `03_global_learnings/failed_patterns.md` |

**After writing:** run `/suno validate` (or CLI — see below) before the user copies to SUNO or runs API.

### `/suno validate`

| Read |
|------|
| Target `suno_prompt_vN.md`, `song_brief.md`, `suno/style_directions.md`, `03_global_learnings/suno_learnings.md`, `03_global_learnings/style_decision_matrix.md` (settings sanity) |

### `/suno run`

| Read |
|------|
| Latest `suno/suno_prompt_vN.md`, `06_integrations/suno/request_schema.md` |

**Execute:** `./studio-suno validate <track>` first unless the user explicitly skips.

### `/listen` · `/retry`

| Read |
|------|
| `01_artist/feedback_dictionary.md`, `analysis/listening_notes.md`, `suno/style_directions.md`, prior `suno_prompt_v*.md` |

**`/retry` also:** `03_global_learnings/suno_learnings.md`, `03_global_learnings/failed_patterns.md`, relevant rows from `05_catalog/best_suno_outputs.md`

**`/retry` output:** end with a draft learning entry (even if not saved).

### `/select final` · `/archive track`

| Read |
|------|
| All `analysis/*`, `suno/final_suno_fields.md` draft, `metadata/final_style.md` |

### `/backfill catalog` · `/catalog review`

| Read |
|------|
| `05_catalog/*`, album `track_map.md`, `masters/` or `audio/` finals, `suno/*_style.md` or `final_suno_fields.md`, `lyrics/` |

### `/album check`

| Read |
|------|
| `variation_map.md`, `track_map.md`, all `song_brief.md`, `metadata/final_style.md` (if exists), `album_arc.md` |

---

## CLI pre-flight (optional but recommended)

From `06_integrations/suno/`:

```bash
./studio-suno validate <track> [--prompt v1]
```

Same checks as `/suno validate` field hygiene. Use before `generate` or before pasting into the SUNO UI.

---

## Matching winners to briefs

When `best_suno_outputs.md` has rows, use the **Style pull hints** table at the bottom — fill it as your catalog grows.

| Brief needs… | Start from |
|--------------|------------|
| _(empty until you log winners)_ | Run `/backfill catalog` or `/archive track` |

Adapt — never copy-paste a released prompt onto a different song.
