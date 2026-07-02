# SUNO Album Studio OS — Workflow

The creative cycle for every album. Phases are sequential in intent, but you may loop within phases — especially **SUNO Run Cycle** and **Song Development**.

---

## Orchestrated Draft (Optional)

For a new album with raw material in `input/`, `/orchestrate album` runs phases 1–6 plus draft assembly and `/album check` — stopping at `suno_prompt_v1.md` per track (no audio). The user reviews lyrics and styles, then generates tracks one at a time. Full spec: `00_system/album_orchestrator.md`.

---

## Overview

```text
1. Album Seed
2. Album World
3. Brainstorm Capture
4. Brainstorm Distillation
5. Song Pool
6. Song Development
7. SUNO Run Cycle
8. Final Selection
9. Album Assembly
10. Archive & Learn
11. Release Preparation
12. Catalog Review
```

---

## Phase 1 — Album Seed

**Purpose:** Start from life, not from a concept factory.

**Inputs:** A lived moment, question, season, audience, or creative hunger.

**Activities:**
- Name the seed in one paragraph
- Note why now
- Identify emotional temperature (not genre yet)

**Outputs:**
- `album.md` — working title, status, seed paragraph
- Optional first brainstorm file

**Command:** `/album seed`

**Guardrails:** Do not lock genre yet. Do not build a 14-track list yet.

---

## Phase 2 — Album World

**Purpose:** Build the album's own identity without breaking artist DNA.

**Activities:**
- Define who this album is for and what it refuses to be
- Sketch emotional arc
- Draft sonic palette (clothes, not body)
- Draft visual direction
- Note rejected directions early

**Outputs:**
- `album_identity.md`
- `album_arc.md`
- `sonic_palette.md`
- `visual_direction.md`
- `rejected_directions.md` (album level)

**Command:** `/album world`

**Guardrails:** Album world must allow variation. Check against `01_artist/artist_dna.md`.

---

## Phase 3 — Brainstorm Capture

**Purpose:** Think openly without premature structure.

**Activities:**
- Dump ideas: song titles, images, phrases, conflicts, grooves, fears
- Capture contradictions and wild options
- No filtering during capture

**Outputs:**
- `brainstorms/YYYY-MM-DD_<topic>.md` (one file per session)

**Command:** `/brainstorm`

**Guardrails:** Do not distill during capture. Do not write SUNO prompts yet.

---

## Phase 4 — Brainstorm Distillation

**Purpose:** Turn raw brainstorm into usable creative decisions.

**Activities:**
- Extract what stays, what goes, what's still open
- Name album direction decisions explicitly
- Separate essay ideas from song ideas

**Outputs:**
- `conclusions/album_direction_decisions.md`
- `conclusions/open_questions.md`
- `conclusions/rejected_directions.md`

**Command:** `/distill brainstorm`

**Guardrails:** Apply the single-vs-album learning — not every truth wants to become a song.

---

## Phase 5 — Song Pool

**Purpose:** List candidate songs before deep development.

**Activities:**
- Propose working titles and one-line roles
- Assign provisional energy and album function
- Mark must-haves vs experiments
- Do not fully develop lyrics yet

**Outputs:**
- `track_map.md` (pool version)
- Optional entries in `tracks/<slug>/track.md` as stubs

**Command:** `/song pool`

**Guardrails:** A pool is not a final tracklist. Leave room to cut or merge.

---

## Phase 6 — Song Development

**Purpose:** Develop one song deeply before moving to the next.

**Per song:**
1. Song role on the album
2. Emotional center
3. Life source
4. Hook / mantra
5. What it is / what it is not
6. Lyrics draft
7. Style direction (not final SUNO yet)

**Outputs:**
- `tracks/<slug>/song_brief.md`
- `tracks/<slug>/lyrics/lyrics_v1.md`
- `tracks/<slug>/suno/style_directions.md`

**Commands:** `/song brief`, `/lyrics`, `/style directions`

**Guardrails:** One clear emotional center per song. If it tries to become the whole album, narrow it.

---

## Phase 7 — SUNO Run Cycle

**Purpose:** Generate, listen, learn, retry — one song at a time.

**Pre-flight:** `/suno validate` (or `./studio-suno validate`) before every run or copy-paste.

**Mandatory reads:** `00_system/mandatory_reads.md` — `/suno`, `/listen`, `/retry` sections.

**Activities:**
1. Build SUNO package from brief + lyrics + style directions
2. Generate via Suno UI (copy-paste) **or** optional API CLI (`06_integrations/suno/`)
3. Save audio with run ID naming
4. Write listening notes
5. Adjust prompt and retry as needed

**Outputs:**
- `tracks/<slug>/suno/suno_prompt_vN.md`
- `tracks/<slug>/suno/suno_runs.md`
- `tracks/<slug>/suno/runs/run_NNN.json` (when using API)
- `tracks/<slug>/analysis/listening_notes.md`
- Audio in `tracks/<slug>/audio/`

**Commands:** `/suno`, `/suno run`, `/suno status`, `/suno wav`, `/listen`, `/retry`

**Guardrails:**
- Follow 8-field SUNO structure exactly
- Log every meaningful run
- Weirdness and Style influence must be intentional
- Download WAV for publishing before sunoapi.org 15-day file expiry

---

## Phase 8 — Final Selection

**Purpose:** Choose the winning version and know why.

**Activities:**
- Compare shortlisted runs
- Check album fit and artist identity fit
- Document selection rationale
- Freeze final SUNO fields

**Outputs:**
- `analysis/final_selection_reason.md`
- `analysis/comparison_notes.md`
- `suno/final_suno_fields.md`
- `metadata/final_style.md`

**Command:** `/select final`

**Guardrails:** Life beats concept. Alive but imperfect may beat polished but dead.

---

## Phase 9 — Album Assembly

**Purpose:** Ensure the album works as a whole.

**Activities:**
- Update final track order
- Check variation map: energy, rhythm, vocal, palette
- Verify each track has a distinct role
- Run cohesion check without sameness

**Outputs:**
- `track_map.md` (final)
- `variation_map.md`
- `masters/full_album_sequence.md`

**Commands:** `/update track map`, `/album check`

**Guardrails:** Same energy ≠ same style. Protect listener journey.

---

## Phase 10 — Archive & Learn

**Purpose:** Make the work retrievable and improve future albums.

**Activities:**
- Archive final WAV, lyrics, styles
- Update track metadata
- Extract learnings to album and global files
- Update album dossier

**Outputs:**
- `metadata/track_metadata.md`
- `lyrics/lyrics_final.md`
- `learnings/*`
- `03_global_learnings/*` (when pattern is reusable)

**Commands:** `/archive track`, `/extract learning`, `/update album dossier`

**Guardrails:** Link audio to prompt version and selection reason.

---

## Phase 11 — Release Preparation

**Purpose:** Move from studio complete to world ready.

**Activities:**
- Distribution metadata
- Spotify pitch
- Cover art finalization
- Social campaign notes
- Release checklist

**Outputs:**
- `release/*`
- `album_art/cover_notes.md`
- `release_notes.md`

**Command:** `/release prep`

---

## Phase 12 — Catalog Review

**Purpose:** Maintain discography truth and reusable assets.

**Activities:**
- Update released / unreleased lists
- Index strong style phrases
- Note best SUNO outputs for reference
- Cross-link albums

**Outputs:**
- `05_catalog/*`

**Command:** `/catalog review`

---

## Typical Loop Patterns

```text
Song Development → SUNO Run Cycle → Listen → Retry → (repeat)
Final Selection → Archive & Learn → (next song)
Album Assembly → Album Check → (back to Song Development if weak link found)
```

---

## Phase Checklist (Per Album)

| Phase | Done when |
|-------|-----------|
| Album Seed | `album.md` has a clear life-based seed |
| Album World | identity, arc, palette, visual drafted |
| Brainstorm | at least one brainstorm captured |
| Distillation | direction decisions written |
| Song Pool | track_map has candidates with roles |
| Song Dev | each track has song_brief before SUNO |
| SUNO Cycle | runs logged with listening notes |
| Final Selection | winner chosen with rationale |
| Album Assembly | variation_map reviewed |
| Archive | finals + metadata complete |
| Release | release folder populated |
| Catalog | discography updated |

---

## When to Pause an Album

Pause or narrow scope when:

- songs feel essay-driven, not inevitable
- every track sounds like the same SUNO default
- concept is stronger than musical life
- user says "it tries to become the whole album" repeatedly

Single-track projects taught: some truths arrive as singles. That is success, not failure.
