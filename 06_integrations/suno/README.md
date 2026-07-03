# Studio SUNO CLI

Thin Python CLI for [sunoapi.org](https://docs.sunoapi.org) — reads existing `suno_prompt_vN.md` files, submits generation, downloads MP3 previews and WAV masters, and updates `suno_runs.md`.

Manual copy-paste to the Suno UI still works. This is **opt-in**.

**Prefer a visual review UI?** See [Studio Browser](../studio-browser/README.md) — browse albums, play takes, and write notes in a local web page. Generate/WAV buttons use this same CLI under the hood.

> Generated files on sunoapi.org expire after **15 days**. Download MP3s after runs and WAVs before publishing.

---

## Setup

1. Get an API key from [sunoapi.org/api-key](https://sunoapi.org/api-key)
2. From repo root:
   ```bash
   cp .env.example .env
   # Edit .env — set SUNO_API_KEY
   ```
3. Install dependencies:
   ```bash
   cd 06_integrations/suno
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Optional: copy `config.example.yaml` → `config.yaml` for model/poll defaults

---

## Commands

Run from `06_integrations/suno` (with venv active) or use `./studio-suno`:

```bash
# Pre-flight — validate prompt hygiene (no API call)
./studio-suno validate my-album/track-slug

# Dry run — validate prompt, print API payload
./studio-suno generate my-album/track-slug --dry-run

# Generate and wait for MP3s (2 takes per request)
./studio-suno generate my-album/track-slug

# Specific prompt version
./studio-suno generate track-slug --prompt v1

# Submit without waiting
./studio-suno generate track-slug --no-wait

# Stream preview only (~30-40s)
./studio-suno generate track-slug --stream-only

# Check task status
./studio-suno status TASK_ID
./studio-suno status --track track-slug --run 001

# Re-download MP3s
./studio-suno download track-slug --run 001 --take a

# WAV for publishing
./studio-suno wav track-slug --run 001 --take a
./studio-suno wav track-slug --run 001 --take a --final-name track-slug_final

# Credits
./studio-suno credits
```

Track paths accept:

- Album slug + track: `my-album/track-slug`
- Track slug only (searches known albums): `track-slug`
- Full path under `02_albums/`

---

## What gets updated

| Output | Location |
|--------|----------|
| MP3 previews | `tracks/<slug>/audio/runNNN_take_a.mp3`, `runNNN_take_b.mp3` |
| WAV masters | `tracks/<slug>/audio/runNNN_take_a.wav` or custom name |
| Run log | `tracks/<slug>/suno/suno_runs.md` |
| Machine metadata | `tracks/<slug>/suno/runs/run_NNN.json` |

---

## Album defaults

Optional `02_albums/<album>/suno_config.yaml`:

```yaml
default_model: V5_5
```

---

## Field mapping

See [request_schema.md](request_schema.md) for Studio OS 8-field → API mapping.

---

## Troubleshooting

| Error | Action |
|-------|--------|
| `SUNO_API_KEY not set` | Create repo root `.env` from `.env.example` |
| `401` | Check API key |
| `429` | Top up credits |
| `413` | Shorten lyrics/styles for model limits |
| `SENSITIVE_WORD_ERROR` | Edit lyrics/styles, retry |
| Empty MP3 URL | Wait and run `studio-suno status` or `download` again |

---

## Cursor slash commands

Agents can wrap this CLI:

- `/suno run` — generate with `--wait`
- `/suno status` — poll task
- `/suno wav` — WAV conversion

See `00_system/commands.md`.
