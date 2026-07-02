# SUNO API Request Schema — Studio OS → sunoapi.org

Authoritative mapping from SUNO Album Studio 8-field SUNO packages to [sunoapi.org](https://docs.sunoapi.org) API payloads.

Source format: `00_system/suno_song_preparation_guide_v2.md`, `04_templates/suno_package_template.md`.

---

## Field mapping

| # | Studio field | API field | Transform |
|---|--------------|-----------|-----------|
| 1 | Lyrics (fenced block) | `prompt` | Raw text; required when `instrumental: false` |
| 2 | Styles (fenced block) | `style` | Raw text — **concrete musical language only**; no artist, album, or studio shorthand (see SUNO guide § "Avoid References SUNO Cannot Know") |
| 3 | More options | — | Not sent (UI-only section header) |
| 4 | Exclude styles (fenced block) | `negativeTags` | Raw comma-separated text |
| 5 | Vocal Gender M/F | `vocalGender` | `M` → `m`, `F` → `f` |
| 6 | Weirdness % | `weirdnessConstraint` | Strip `%`, divide by 100 (22% → 0.22) |
| 7 | Style influence % | `styleWeight` | Strip `%`, divide by 100 (68% → 0.68) |
| 8 | Song Title (fenced block) | `title` | Raw text |

## Fixed parameters (Studio OS custom mode)

| API field | Value | Notes |
|-----------|-------|-------|
| `customMode` | `true` | Studio always uses custom mode |
| `instrumental` | `false` | Override with `--instrumental` for instrumental tracks |
| `model` | `V5_5` | Default (latest on sunoapi.org); override via `config.yaml`, album `suno_config.yaml`, or `--model` |
| `callBackUrl` | `https://localhost/noop` | Required by API; CLI polls instead of webhooks |

## Character limits (V4_5 / V5 family)

| Field | Max chars |
|-------|-----------|
| `prompt` | 5000 |
| `style` | 1000 |
| `title` | 100 |

V4 model uses lower limits — see sunoapi.org docs if switching models.

---

## Example payload

From `memory-of-the-stars/suno/suno_prompt_v1.md`:

```json
{
  "customMode": true,
  "instrumental": false,
  "model": "V4_5ALL",
  "prompt": "[Verse 1]\nFeet on the dust\n...",
  "style": "West African night ceremony, authentic tribal roots, ...",
  "title": "Po Tolo",
  "negativeTags": "meditation drone, ambient new age, ...",
  "vocalGender": "m",
  "weirdnessConstraint": 0.22,
  "styleWeight": 0.68,
  "callBackUrl": "https://localhost/noop"
}
```

---

## Response metadata (stored in `suno/runs/run_NNN.json`)

| API response | Sidecar field |
|--------------|---------------|
| `taskId` | `task_id` |
| `sunoData[].id` | `takes[].audio_id` |
| `sunoData[].audioUrl` | `takes[].audio_url` |
| `sunoData[].streamAudioUrl` | `takes[].stream_url` |
| Local path | `takes[].mp3` / `takes[].wav` |

---

## WAV conversion

`POST /api/v1/wav/generate`:

```json
{
  "taskId": "<generation task_id>",
  "audioId": "<take audio_id>",
  "callBackUrl": "https://localhost/noop"
}
```

Poll `GET /api/v1/wav/record-info?taskId=<wav_task_id>` until `successFlag: SUCCESS`, then download `response.audioWavUrl`.

---

## Retention

Generated files on sunoapi.org are retained for **15 days**. Download MP3s after generation and WAVs before publishing.
