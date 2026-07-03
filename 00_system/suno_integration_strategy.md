# SUNO Integration Strategy

How SUNO Album Studio OS relates to SUNO — manual UI, optional API.

---

## V1 Philosophy: Copy-Paste Optimized

The default path assumes:

- You generate music **manually in SUNO's UI**
- Prompts are prepared in structured Markdown, then copied field by field
- Audio is downloaded and stored locally in track `audio/` folders
- Runs are logged in `suno_runs.md` and listening notes

This remains valid. Reliability and creative control beat forced automation.

---

## V2: sunoapi.org CLI (opt-in)

A thin Python CLI lives at `06_integrations/suno/`. It reads existing `suno_prompt_vN.md` files and talks to [sunoapi.org](https://docs.sunoapi.org) — a **third-party** API provider, not Suno's official UI.

**When to use:** Skip copy-paste when you have an API key and want MP3 previews + WAV downloads into track folders automatically.

**When not to use:** API down, no credits, or you prefer the Suno UI. Manual workflow unchanged.

Setup: `06_integrations/suno/README.md`  
Field mapping: `06_integrations/suno/request_schema.md`  
**Default model:** `V5_5` (latest on sunoapi.org) — override in `config.yaml`, album `suno_config.yaml`, or `--model`.

### What the CLI auto-syncs

| Action | Updates |
|--------|---------|
| `generate` | `suno_runs.md`, `suno/runs/run_NNN.json`, `audio/runNNN_take_*.mp3` |
| `wav` | Sidecar WAV path, `audio/*.wav` |
| `download` | Re-fetch MP3s from existing task |

### What stays manual

- Listening, `/retry`, `/select final`, `/archive track`
- Creative phases 1–6 (brief, lyrics, style directions)
- Human verdict in `listening_notes.md`

### Retention warning

Generated files on sunoapi.org are retained for **15 days**. Download MP3s after runs and WAVs before publishing.

---

## API-Ready Structure

The repo structure supports both manual and API paths without restructuring the creative workflow.

### What is already API-ready

| Asset | Location | Use |
|-------|----------|-----|
| Versioned prompts | `suno/suno_prompt_vN.md` | Request payload source |
| Structured settings | Weirdness %, Style influence %, Vocal Gender | Request parameters |
| Run log | `suno/suno_runs.md` | Human-readable audit trail |
| Run sidecar | `suno/runs/run_NNN.json` | Task IDs, audio IDs, URLs |
| YAML metadata | `metadata/track_metadata.md` | Catalog sync |
| Audio + rationale | `audio/` + `final_selection_reason.md` | What worked |

---

## Manual Run Tracking

Each meaningful SUNO generation should be logged in `suno_runs.md`:

```markdown
## Run 003 — 2026-06-28

- **Prompt version:** suno_prompt_v2.md
- **Task ID:** `abc123` (API runs)
- **Weirdness:** 25%
- **Style influence:** 68%
- **Output files:** run003_take_a.mp3, run003_take_b.mp3
- **Quick verdict:** groove right, vocal too polished
- **Listening notes:** analysis/listening_notes.md#run-003
```

The CLI appends these entries automatically. Manual runs: copy the template from `04_templates/suno_run_template.md`.

---

## Integration Layer

```text
06_integrations/suno/
  README.md
  request_schema.md     — map studio fields → API fields
  studio_suno/            — Python CLI
  config.example.yaml
```

### Request mapping

See `06_integrations/suno/request_schema.md` for authoritative field mapping.

Studio field → API equivalent:

1. Lyrics → `prompt`
2. Styles → `style`
3. Exclude styles → `negativeTags`
4. Vocal Gender → `vocalGender`
5. Weirdness % → `weirdnessConstraint`
6. Style influence % → `styleWeight`
7. Song Title → `title`

### Response metadata captured

- task ID / audio ID
- timestamp
- model version
- duration
- stream URL, MP3 URL, WAV URL
- local file paths

Stored in JSON sidecars alongside Markdown logs — human listening notes still win.

---

## Audio Archiving

Final and shortlisted audio should:

1. Live in `tracks/<slug>/audio/`
2. Be named with run ID for traceability
3. Be referenced in `track_metadata.md` → `final_audio`
4. Link back to `suno_prompt_vN.md` and `final_selection_reason.md`

For album masters, use `masters/` with sequence notes in `full_album_sequence.md`.

Binary files may be gitignored later; paths in Markdown remain truth.

---

## Prompt ↔ Audio ↔ Learning Chain

```text
song_brief.md
    ↓
suno_prompt_vN.md ──→ SUNO (UI or API) ──→ audio/runNNN.*
    ↓                                        ↓
style_directions.md                    listening_notes.md
    ↓                                        ↓
final_suno_fields.md ←── select final ── final_selection_reason.md
    ↓
track_metadata.md + global learnings
```

Any automation should preserve this chain. Never generate audio without a stored prompt version.

---

## Settings Intentionality

Weirdness % and Style influence % are creative decisions, not defaults.

Document rationale in:

- `suno_prompt_vN.md` header comment
- `suno_runs.md`
- `metadata/final_style.md` for finals

See `01_artist/style_reference_summary.md` and `03_global_learnings/style_decision_matrix.md` for family and settings ranges.

---

## Exclude Styles Strategy

- Keep excludes concise
- Album-level common excludes may live in `sonic_palette.md`
- Track-specific excludes go in each prompt
- When a exclude pattern repeats 3+ times, add to `03_global_learnings/failed_patterns.md`

---

## Versioning SUNO Guide Compliance

All agents preparing SUNO output must follow:

`00_system/suno_song_preparation_guide_v2.md`

If SUNO's UI changes field names, update the guide in `00_system/` and note the date in this file.

---

## Summary

| Manual UI | API CLI (opt-in) |
|-----------|------------------|
| Copy-paste fields | `./studio-suno generate` |
| Hand-written run logs | Auto-append + JSON sidecar |
| Download from UI | MP3 + WAV via CLI |
| Human listening | Human listening still wins |

The studio OS serves **creative memory and workflow**, not the SUNO product itself.

Updated: 2026-07-02 — V2 sunoapi.org CLI added at `06_integrations/suno/`. Default model `V5_5` (2026-07-02).
