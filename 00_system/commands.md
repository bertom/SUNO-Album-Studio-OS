# Studio Commands

Slash-style commands for use with Cursor agents or any AI assistant — **type in chat** (e.g. `/suno validate on track X`). Not Cursor's native `/` command picker unless you add `.cursor/commands/` yourself. Each command should read listed files, produce stated outputs, and update documented files.

**Global rules for all commands:**
- Read `00_system/project_instructions.md` if context is missing
- Read `00_system/mandatory_reads.md` for the **required file list** for this command — mandatory reads are not optional
- Consult `01_artist/feedback_dictionary.md` when interpreting user's feedback
- Never put artist names or studio/album shorthand in SUNO fenced fields — translate to concrete musical language
- Preserve artist DNA without forcing a single genre
- Prefer updating existing files over creating duplicates

---

## `/onboard artist`

**Purpose:** First-run setup — interview the user and fill `01_artist/` scaffold.

**Input:** User answers (can be one messy paragraph or Q&A).

**Output:** Populated `artist_dna.md`, `artist_identity.md`, starter `style_reference_summary.md` (2–4 style families), starter `feedback_dictionary.md` (5–10 rows from their words), `sonic_palette.md` seeds.

**Read:** Empty templates in `01_artist/`, `01_artist/README.md`, `ONBOARDING.md`, `04_templates/` if helpful.

**Update:** `01_artist/artist_dna.md`, `artist_identity.md`, `style_reference_summary.md`, `style_reference.md` (starter families), `feedback_dictionary.md`, `sonic_palette.md`

**Process:** Ask or infer:
1. Artist / project name
2. What must every song feel like? (3–5 protect words)
3. What do you refuse? (3–5 avoid words)
4. Vocal identity (gender, tone, delivery)
5. 2–3 groove families (feel, not Spotify genres)
6. Reference moods (translate to instruments — no artist names in SUNO)
7. Optional: existing SUNO albums to backfill later?

**Guardrails:** No SUNO prompts yet. No album creation. Identity only.

---

## `/album seed`

**Purpose:** Start a new album from a life-based seed.

**Input:** Seed description (life moment, audience, question, season). Optional working title.

**Output:** Draft seed paragraph, working title options, first questions to explore.

**Read:** `01_artist/artist_dna.md`, relevant album folder in `02_albums/` if continuing a thread.

**Update:** `02_albums/<album>/album.md`

**Guardrails:** No final tracklist. No genre lock. No SUNO prompts.

---

## `/orchestrate album`

**Purpose:** Run the full draft-album pipeline from raw input through review-ready SUNO packages — one cohesive album, traceable process, no audio generation.

**Input:** Album path (e.g. `02_albums/my-album/`), or working title + permission to bootstrap from `_album_template/`. Optional language override (default English).

**Output:** Complete draft album at `draft-ready` status: album world docs, brainstorms, conclusions, track pool, per-track briefs, lyrics v1, style directions, `suno_prompt_v1.md`, filled `variation_map.md`, `orchestrator_report.md`.

**Read:** `00_system/mandatory_reads.md` (orchestrator section), `00_system/album_orchestrator.md` (master spec), all files in `input/`, `00_system/agent_roles.md`, `01_artist/artist_dna.md`, `01_artist/style_reference.md`, `03_global_learnings/style_decision_matrix.md`, `05_catalog/best_suno_outputs.md`, `00_system/suno_song_preparation_guide_v2.md`, `04_templates/*`, reference albums as needed.

**Update:** Full album scaffold per orchestrator spec — `album.md`, identity/arc/palette/visual, `brainstorms/`, `conclusions/`, `track_map.md`, `variation_map.md`, `learnings/album_learnings.md`, `masters/full_album_sequence.md`, every `tracks/<slug>/` through `suno/suno_prompt_v1.md`, `orchestrator_report.md`.

**Execute:** Follow `00_system/album_orchestrator.md` phase by phase. One agent, role-switching. Develop tracks one at a time.

**Guardrails:**
- Read `input/` only — do not copy input files elsewhere
- Stop before `/suno run` — user reviews lyrics and styles, then generates one track at a time
- Album must tell one story with variety — not a loose song collection; use `variation_map.md` and `/album check` equivalent before finishing
- Identity Guardian audits at album world, song pool, each track, and final assembly
- Usually 8–16 tracks; let the story decide count
- Empty `input/` → stop and ask the user for material
- End-to-end quality bar: every brief from life, every lyric singable, every SUNO package copy-paste ready

---

## `/album world`

**Purpose:** Define the album's identity, arc, sound clothes, and visual direction.

**Input:** Album slug or path. Optional brainstorm conclusions.

**Output:** Drafts for identity, arc, sonic palette, visual direction.

**Read:** `album.md`, `conclusions/album_direction_decisions.md`, `01_artist/*`, style reference.

**Update:** `album_identity.md`, `album_arc.md`, `sonic_palette.md`, `visual_direction.md`

**Guardrails:** Album may differ from past albums; DNA must remain. Document rejections.

---

## `/brainstorm`

**Purpose:** Open capture session — no filtering.

**Input:** Topic or "open". Raw ideas welcome.

**Output:** New brainstorm file with dated header and unstructured sections.

**Read:** `album.md`, `album_identity.md` (light context only).

**Update:** `brainstorms/YYYY-MM-DD_<topic>.md` (new file)

**Guardrails:** Do not distill, rank, or write SUNO prompts in this command.

---

## `/distill brainstorm`

**Purpose:** Extract decisions, rejections, and open questions from brainstorm(s).

**Input:** Brainstorm file path(s) or "latest".

**Output:** Structured distillation using brainstorm distillation template.

**Read:** `brainstorms/*.md`, `album_identity.md`

**Update:** `conclusions/album_direction_decisions.md`, `conclusions/open_questions.md`, `conclusions/rejected_directions.md`

**Guardrails:** Flag essay-vs-song ideas. Separate "interesting" from "actionable".

---

## `/song pool`

**Purpose:** Build or refresh the candidate song list with roles.

**Input:** Album direction, brainstorm conclusions, optional target track count.

**Output:** Proposed pool: title, role, energy, status (idea / candidate / developing).

**Read:** `track_map.md`, `conclusions/*`, `album_arc.md`

**Update:** `track_map.md`, optionally create stub `tracks/<slug>/track.md`

**Guardrails:** Pool ≠ final order. Allow duplicates to merge later.

---

## `/song brief`

**Purpose:** Create or refine the creative brief for one song.

**Input:** Track slug or title. Optional life source, role notes.

**Output:** Completed song brief from template.

**Read:** `04_templates/song_brief_template.md`, `album_identity.md`, `track_map.md`, `01_artist/artist_dna.md`

**Update:** `tracks/<slug>/song_brief.md`, `tracks/<slug>/track.md`

**Guardrails:** One emotional center. Clear "what this is not". Album contrast required.

---

## `/style directions`

**Purpose:** Explore style options before committing to a SUNO package.

**Input:** Track slug. Optional reference to a past groove family from the user's catalog.

**Output:** 2–3 style direction options with tradeoffs, exclude suggestions, setting ranges.

**Read:** `00_system/mandatory_reads.md` (`/style directions`), `song_brief.md`, `01_artist/sonic_palette.md`, `01_artist/style_reference_summary.md`, `03_global_learnings/style_decision_matrix.md`, `03_global_learnings/reusable_style_recipes.md`, `05_catalog/style_index.md`, `05_catalog/best_suno_outputs.md` (match 2–3 winners by role/energy)

**Update:** `tracks/<slug>/suno/style_directions.md`

**Guardrails:** Pick starting family from `style_decision_matrix.md`. Concrete musical language. No artist names. Note artist DNA preserved in each option.

---

## `/lyrics`

**Purpose:** Draft or refine lyrics for a track.

**Input:** Track slug. Optional seed lines, mantra, structural notes.

**Output:** SUNO-formatted lyrics with section tags.

**Read:** `song_brief.md`, `01_artist/lyric_principles.md`, existing `lyrics/*.md`

**Update:** `tracks/<slug>/lyrics/lyrics_vN.md` (increment version)

**Guardrails:** Short singable lines. Call-response in parentheses when needed. No production notes in lyrics.

---

## `/suno`

**Purpose:** Produce a copy-paste SUNO package for the current track.

**Input:** Track slug. Optional style direction choice (A/B/C).

**Output:** Full 8-field SUNO output per SUNO Guide v2.0.

**Read:** `00_system/mandatory_reads.md` (`/suno`), `song_brief.md`, `lyrics/lyrics_v*.md` (latest), `suno/style_directions.md`, `00_system/suno_song_preparation_guide_v2.md`, `03_global_learnings/suno_learnings.md`, `03_global_learnings/failed_patterns.md`

**Update:** `tracks/<slug>/suno/suno_prompt_vN.md` (new version file)

**Guardrails:**
- Exact field order: Lyrics, Styles, More options, Exclude styles, Vocal Gender, Weirdness %, Style influence %, Song Title
- Fenced blocks for Lyrics, Styles, Exclude styles, Song Title
- No negative instructions in Styles
- **No references SUNO cannot know** in fenced fields — translate studio/album shorthand to concrete musical language (guide § "Avoid References SUNO Cannot Know")
- Intentional Weirdness % and Style influence %
- Run `/suno validate` before delivering or before `/suno run`

---

## `/suno validate`

**Purpose:** Pre-flight a SUNO package before credits or copy-paste — catch hygiene failures early.

**Input:** Track slug or path to `suno_prompt_vN.md`. Optional prompt version.

**Output:** Pass/fail report: errors (must fix), warnings (review), settings sanity vs `song_brief.md` and `style_decision_matrix.md`.

**Read:** `00_system/mandatory_reads.md` (`/suno validate`), target prompt file, `song_brief.md`, `suno/style_directions.md`, `03_global_learnings/suno_learnings.md`, `03_global_learnings/style_decision_matrix.md`

**Execute (CLI — recommended):**

```bash
cd 06_integrations/suno && ./studio-suno validate <track> [--prompt v1]
```

**Checks:**
- 8-field structure and fenced blocks (Lyrics, Styles, Exclude styles, Song Title)
- No artist names or studio shorthand in Styles (`Family-like`, project names, etc.)
- No negative instructions in Styles (`no dub`, `without trap`, …)
- Sensitive terms (`skank` → use offbeat rhythm guitar chop)
- Lyrics length limits; `[Backing vocals]` → prefer parentheses call-response
- Empty exclude list warning
- Weirdness % / Style influence % in range; flag outliers vs brief role

**Update:** None — report only. Fix via `/suno` or `/retry`.

**Guardrails:** Validate does not change files unless the user asks to fix. Warnings ≠ blockers unless the user says so.

---

## `/suno run`

**Purpose:** Submit a SUNO package to sunoapi.org and download MP3 previews.

**Input:** Track slug or path. Optional prompt version (`v1`). Optional `--dry-run`, `--no-wait`, `--stream-only`.

**Output:** Task ID, downloaded MP3s in `audio/`, updated `suno_runs.md` and `suno/runs/run_NNN.json`.

**Read:** Latest or specified `suno/suno_prompt_vN.md`, `06_integrations/suno/request_schema.md`

**Update:** `suno/suno_runs.md`, `suno/runs/run_NNN.json`, `audio/runNNN_take_*.mp3`

**Execute:**

```bash
cd 06_integrations/suno && ./studio-suno generate <track> [--prompt v1] [--dry-run]
```

**Guardrails:** Require existing `suno_prompt_vN.md`. Run `--dry-run` first if validating. Check credits with `./studio-suno credits`. Human listening still required after.

---

## `/suno status`

**Purpose:** Poll a generation or WAV conversion task.

**Input:** Task ID, or track slug + run number.

**Output:** Status, stream URLs, audio IDs, download URLs if ready.

**Execute:**

```bash
cd 06_integrations/suno && ./studio-suno status TASK_ID
cd 06_integrations/suno && ./studio-suno status --track <track> --run 003
cd 06_integrations/suno && ./studio-suno status --track <track> --run 003 --wav
```

---

## `/suno wav`

**Purpose:** Convert a shortlisted take to WAV and download for publishing.

**Input:** Track slug, run number, take (`a` or `b`). Optional final filename.

**Output:** WAV in `audio/`, updated run sidecar.

**Read:** `suno/runs/run_NNN.json`

**Update:** `audio/runNNN_take_a.wav` or custom final name, sidecar `takes[].wav`

**Execute:**

```bash
cd 06_integrations/suno && ./studio-suno wav <track> --run 003 --take a
```

**Guardrails:** Use after `/select final` or when take is shortlisted. Files on sunoapi.org expire after 15 days — download promptly.

---

## `/listen`

**Purpose:** Structure listening notes for a SUNO run.

**Input:** Run ID, audio filename, prompt version, first impressions (user's words welcome).

**Output:** Completed listening notes.

**Read:** `04_templates/listening_notes_template.md`, `song_brief.md`, corresponding `suno_prompt_vN.md`

**Update:** `tracks/<slug>/analysis/listening_notes.md` (append or new dated section), `suno/suno_runs.md`

**Guardrails:** Map user's casual feedback through `feedback_dictionary.md`. Note SUNO artifacts explicitly.

---

## `/retry`

**Purpose:** Propose the next SUNO prompt adjustment after a failed or partial run.

**Input:** Track slug, run reference, what failed.

**Output:** Changed style/lyrics/settings with rationale; optional new `/suno` package.

**Read:** `00_system/mandatory_reads.md` (`/retry`), latest listening notes, style directions, prior prompts, `03_global_learnings/suno_learnings.md`, `03_global_learnings/failed_patterns.md`, relevant `05_catalog/best_suno_outputs.md` rows

**Update:** `suno/style_directions.md` (if direction shifts), new `suno_prompt_vN.md`, listening notes "Next Prompt Move"

**Guardrails:** Change one major variable at a time when possible. Log the hypothesis. **End output with a draft learning entry** for `/extract learning` (even if not saved).

---

## `/select final`

**Purpose:** Record the winning version and freeze creative decisions.

**Input:** Track slug, chosen run/audio, why it won.

**Output:** Final selection rationale, comparison summary, final SUNO fields draft.

**Read:** `analysis/listening_notes.md`, `analysis/comparison_notes.md`, shortlisted audio refs

**Update:** `analysis/final_selection_reason.md`, `suno/final_suno_fields.md`, `metadata/final_style.md`, `track.md` status → final

**Guardrails:** Must state album fit and artist identity fit, not only "sounds good".

---

## `/archive track`

**Purpose:** Finalize track documentation for long-term storage.

**Input:** Track slug, paths to final WAV, confirm final lyrics and prompt version.

**Output:** Complete metadata, credits stub, release metadata stub.

**Read:** All `final_*` files, `track_metadata` template fields

**Update:** `metadata/track_metadata.md`, `lyrics/lyrics_final.md`, `metadata/credits.md`, `track.md`, copy audio to `audio/`

**Guardrails:** YAML block must match actual finals. Link prompt version to audio filename.

---

## `/update track map`

**Purpose:** Sync track map with current development status.

**Input:** Album slug. Optional explicit order change.

**Output:** Updated track_map with status, roles, energy markers.

**Read:** All `tracks/*/track.md`, `album_arc.md`

**Update:** `track_map.md`

**Guardrails:** Distinguish pool order vs final sequence. Note cuts explicitly.

---

## `/update album dossier`

**Purpose:** Refresh the album-level narrative documentation.

**Input:** Album slug. What changed (tracks finalized, direction shift, etc.).

**Output:** Updated album.md, identity, arc, learnings summary.

**Read:** All track finals, `learnings/*`, `variation_map.md`

**Update:** `album.md`, `album_identity.md`, `album_arc.md`, `learnings/album_learnings.md`

**Guardrails:** Dossier should read human and complete — not bullet-only.

---

## `/extract learning`

**Purpose:** Move a insight from a track or album into reusable learnings.

**Input:** Learning text, scope (track / album / global), category.

**Output:** Formatted learning entry with context and reuse note.

**Read:** `04_templates/learning_entry_template.md`, source listening notes or album learnings

**Update:** `tracks/<slug>/learnings.md` and/or `learnings/*` and/or `03_global_learnings/*`

**Guardrails:** Tag as worked / failed / pattern. Link to song and prompt version when relevant.

---

## `/album check`

**Purpose:** Cohesion and variation audit before release or mid-production.

**Input:** Album slug.

**Output:** Report on track roles, energy spread, vocal variation, rhythm variation, palette drift, artist identity.

**Output:** Cohesion report with scoring rubric:

| Check | Pass? | Notes |
|-------|-------|-------|
| Adjacent tracks same energy? | | |
| Two tracks same role? | | |
| 3+ tracks same groove family? | | |
| artist DNA present on every track? | | |
| Story arc: clear enter + land? | | |

**Read:** `00_system/mandatory_reads.md` (`/album check`), `variation_map.md`, `track_map.md`, all `song_brief.md`, `metadata/final_style.md` (if exists), `album_arc.md`

**Update:** `variation_map.md` (gaps filled), optional notes in `learnings/album_learnings.md`

**Guardrails:** Flag sameness and outliers. Suggest fixes, not automatic rewrites.

---

## `/catalog review`

**Purpose:** Sync global catalog with album reality.

**Input:** Optional album just completed.

**Output:** Updated discography, released/unreleased, style index, best outputs.

**Read:** `05_catalog/*`, all album `track.md` statuses

**Update:** `05_catalog/discography.md`, `released_tracks.md`, `unreleased_tracks.md`, `style_index.md`, `best_suno_outputs.md`

**Guardrails:** Do not list unreleased as released. Link to album folders.

---

## `/backfill catalog`

**Purpose:** Mine released album material into the global catalog — winners, style phrases, settings.

**Input:** Album slug or path (e.g. `02_albums/my-album/`). Optional: single track slug.

**Output:** Proposed updates to `05_catalog/best_suno_outputs.md`, `style_index.md`, and optionally `reusable_style_recipes.md` — **show the user before writing** unless they say "write it".

**Read:** `00_system/mandatory_reads.md` (`/backfill catalog`), album `track_map.md`, `masters/` or `audio/` finals, `suno/*_style.md` or `final_suno_fields.md`, `lyrics/`, existing `05_catalog/*`

**Process:**
1. List tracks with final audio + archived style or prompt
2. For each: audio path, lyrics path, style archive path, W/SI if known, one-line *why it won*
3. Propose `style_index.md` rows for reusable phrases (proven only)
4. Flag gaps (missing W/SI, lyrics not master-verified, no style archive)
5. Write after user approves, or write directly if they invoked with full data inline

**Update:** `05_catalog/best_suno_outputs.md`, `05_catalog/style_index.md`, optionally `03_global_learnings/reusable_style_recipes.md`, album `track_map.md` style columns

**Guardrails:** Do not invent "why it won" — use the user's words or listening notes.

---

## `/cover prompt`

**Purpose:** Draft an image-generation or designer brief for album/single cover art.

**Input:** Album slug (or single track path), optional iteration notes.

**Output:** Filled brief in `album_art/cover_prompt_vN.md` + copy-paste **Image prompt** and **Negative prompt** blocks.

**Read:** `01_artist/cover_design_guide.md`, `visual_direction.md`, `album_art/visual_direction.md`, `04_templates/cover_prompt_template.md`, matching family preset (`cover_prompt_gentle_landscape.md` / `cover_prompt_documentary_photo.md`)

**Update:** `album_art/cover_prompt_vN.md` (new version file)

**Guardrails:** Define visual anchor from `visual_direction.md` — do not reuse another album's layout. Match cover family to album identity; singles often use documentary-photo unless the brief says otherwise. No religious iconography. Typography usually post-production — omit readable text from image prompts unless exploring type-in-image.

---

## `/release prep`

**Purpose:** Prepare release assets and checklist.

**Input:** Album slug, target release context (single / EP / album).

**Output:** Draft pitch, distribution fields, campaign notes, checklist status.

**Read:** `album_identity.md`, `release_notes.md`, `track_map.md`, `album_art/*`, `04_templates/release_checklist_template.md`

**Update:** `release/spotify_pitch.md`, `release/distribution_metadata.md`, `release/campaign_notes.md`, `release/social_posts.md`

**Guardrails:** Pitch must match actual sound, not aspirational genre.

---

## Command Quick Reference

| Command | Phase |
|---------|-------|
| `/onboard artist` | First run |
| `/orchestrate album` | 1–7 (draft, no audio) |
| `/album seed` | 1 |
| `/album world` | 2 |
| `/brainstorm` | 3 |
| `/distill brainstorm` | 4 |
| `/song pool` | 5 |
| `/song brief` | 6 |
| `/style directions` | 6 |
| `/lyrics` | 6 |
| `/suno` | 7 |
| `/suno validate` | 7 |
| `/suno run` | 7 |
| `/suno status` | 7 |
| `/suno wav` | 7 |
| `/listen` | 7 |
| `/retry` | 7 |
| `/select final` | 8 |
| `/archive track` | 10 |
| `/update track map` | 9 |
| `/update album dossier` | 10 |
| `/extract learning` | 10 |
| `/album check` | 9 |
| `/backfill catalog` | 12 |
| `/catalog review` | 12 |
| `/cover prompt` | 11 |
| `/release prep` | 11 |
