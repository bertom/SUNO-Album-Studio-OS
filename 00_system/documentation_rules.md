# Documentation Rules

How to write and maintain files in SUNO Album Studio OS so humans and AI agents can work together without chaos.

---

## Principles

1. **Markdown first** — no database required for v1.
2. **One source of truth per fact** — final lyrics live in `lyrics_final.md`; don't duplicate full lyrics in five places.
3. **Version, don't overwrite** — `lyrics_v1.md`, `suno_prompt_v2.md`; finals get `_final` or `final_*` names.
4. **Link, don't orphan** — audio files reference prompt version and run ID in listening notes and metadata.
5. **Warm but structured** — write like a creative partner, not a compliance manual.

---

## File Naming

| Type | Convention | Example |
|------|------------|---------|
| Album folder | lowercase slug | `my-album`, `summer-songs` |
| Track folder | lowercase slug | `opening-track`, `track-slug` |
| Brainstorm | `YYYY-MM-DD_topic.md` | `2026-06-28_opening-tracks.md` |
| Lyrics draft | `lyrics_vN.md` | `lyrics_v3.md` |
| SUNO prompt | `suno_prompt_vN.md` | `suno_prompt_v1.md` |
| Audio | `runNNN_short_desc.wav` | `run003_more_percussion.wav` |

Use hyphens in slugs, not spaces.

---

## Album Folder Requirements

Every active album should maintain at minimum:

- `album.md` — status and summary always current
- `track_map.md` — updated when pool or order changes
- `conclusions/album_direction_decisions.md` — after first distillation

Every **final** track should have:

- `song_brief.md`
- `lyrics/lyrics_final.md`
- `suno/final_suno_fields.md`
- `metadata/final_style.md`
- `metadata/track_metadata.md`
- `analysis/final_selection_reason.md`
- Final audio in `audio/`

---

## Status Vocabulary

Use consistent status values in `track.md` and `track_map.md`:

- `idea` — named only
- `pool` — in song pool
- `briefed` — song brief complete
- `lyrics` — lyrics in progress
- `suno` — in run cycle
- `shortlist` — candidates for final
- `final` — selected and archived
- `cut` — removed from album
- `hold` — paused, may return

**Album-level** (`album.md` status): `ideation` | `drafting` | `draft-ready` | `in_progress` | `released`

- `drafting` — orchestrator or team actively building draft docs
- `draft-ready` — all tracks have `suno_prompt_v1.md`; awaiting user's review before SUNO runs

---

## SUNO Documentation

When saving a SUNO package to a file:

1. Use the exact 8-field order from SUNO Guide v2.0
2. Fence Lyrics, Styles, Exclude styles, and Song Title
3. Add a header comment block **outside** the SUNO fields:

```markdown
<!-- prompt version: v2 | date: 2026-06-28 | hypothesis: more hand percussion -->
```

Never put HTML comments inside copy-paste SUNO fields.

---

## Learning Entries

Every learning should include:

- **Context** — album, track, prompt version if relevant
- **Observation** — what happened
- **Action** — what to do next time
- **Scope** — track / album / global
- **Type** — worked / failed / pattern

Use `04_templates/learning_entry_template.md`.

---

## YAML Metadata Blocks

Optional YAML in `track_metadata.md` must:

- Use consistent keys (see track template)
- Match actual finals — not intentions
- Stay minimal — no duplicate prose

Update YAML when archiving; treat it as machine-readable truth for future automation.

---

## What Not to Do

- Don't create `notes.md`, `notes2.md`, `final_final.md` — version properly
- Don't paste full album dossiers into track files — link to `album.md`
- Don't store secrets (API keys) in this repo
- Don't delete listening notes for failed runs — failures teach
- Don't rewrite history in `final_selection_reason.md` after release

---

## Reference vs Studio Files

| Location | Purpose |
|----------|---------|
| `01_artist/` | Stable artist identity and full style reference |
| `00_system/` | Workflow, commands, SUNO preparation guide |
| `02_albums/` | Living workspace — released albums include dossiers and masters |
| `03_global_learnings/` | Distilled cross-album patterns |

Released albums keep authoritative documentation in `album_dossier.md` (or `project_documentation.md`) within their album folder. Active albums use the full track workspace under `tracks/`.

---

## Agent Update Checklist

After a meaningful session, the agent should verify:

- [ ] Status fields updated
- [ ] New versions numbered, not overwritten
- [ ] Listening notes linked to audio filename
- [ ] Learnings extracted if pattern is reusable
- [ ] No artist names added to SUNO prompts
- [ ] `track_map.md` reflects reality

---

## Tone Guide

**Good:** "Run 4 finally had the body — hand claps and bass movement landed. Vocal still slightly theatrical; try lower weirdness on retry."

**Bad:** "The audio asset demonstrates suboptimal vocal performance metrics relative to KPI."

Write for future-you at 2am after a listening session.
