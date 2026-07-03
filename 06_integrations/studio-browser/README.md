# Studio Browser

A **local web page** for reviewing your albums — lyrics, SUNO prompts, MP3 takes, listening notes — without opening dozens of Markdown files.

Markdown stays the source of truth. The browser reads and writes the **same files** agents use. You can still edit files directly anytime.

> **Optional.** You do not need this to use SUNO Album Studio. Copy-paste to [suno.com](https://suno.com) and slash commands in Cursor work without it.

---

## Who this is for

- You have at least one album folder under `02_albums/` (not just `_album_template`)
- You want to **listen, compare takes, and mark favorites** in one place
- You are comfortable opening **Terminal** once to start the app (step-by-step below)

You do **not** need to know Python or coding.

---

## What you can do

- Browse albums and tracks
- Read song briefs, lyrics, style directions, SUNO 8-field packages (copy per field)
- Play MP3/WAV takes and compare A/B
- Mark **favorite**, **shortlist**, or **pass** — updates `suno_runs.md` and `review_state.yaml`
- Write listening notes
- Validate prompts (no API call)
- Generate via API, request WAV, select final, archive track *(only if you set up `SUNO_API_KEY` — see below)*

**Keyboard shortcuts** (album view): `j` / `k` = next/previous track · `1`–`6` = switch tabs

---

## One-time setup

Do this once on your computer.

### 1. You need albums to show

Copy the template if you have not started an album yet:

```text
02_albums/_album_template/  →  02_albums/my-album/
```

Fill it via **`/orchestrate album`** or manual workflow. Folders whose names start with `_` (like `_album_template`) **do not appear** in the browser.

### 2. Install the SUNO CLI environment *(recommended)*

Studio Browser reuses the same Python setup as the optional SUNO CLI.

1. At the **repo root**, copy the env file if you have not already:
   ```bash
   cp .env.example .env
   ```
   *(Only needed if you want **Generate** / **WAV** buttons in the browser. Reading lyrics and playing local MP3s works without it.)*

2. Install CLI dependencies *(from repo root in Terminal)*:
   ```bash
   cd 06_integrations/suno
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

   **Windows:** use `.venv\Scripts\activate` instead of `source .venv/bin/activate`.

The first time you run `./studio serve`, it will create its own small environment if the SUNO one is missing — but using the SUNO venv above is simpler.

---

## Every time you use it

### 1. Open Terminal

In **Cursor**: menu **Terminal → New Terminal** (or `` Ctrl+` `` / `` Cmd+` ``).

### 2. Go to the studio-browser folder

Paste this *(change the path if your repo lives somewhere else)*:

```bash
cd "06_integrations/studio-browser"
```

Run it from the **repo root** — the folder that contains `02_albums/`, `01_artist/`, etc.

### 3. Start the browser

```bash
./studio serve
```

You should see something like:

```text
Studio Browser → http://127.0.0.1:8787
```

### 4. Open the page

Click the link in Terminal, or paste **http://127.0.0.1:8787** into Chrome, Safari, or Firefox.

### 5. When you are done

Click in the Terminal window and press **Ctrl+C** to stop the server.

---

## Empty album list?

| Situation | What to do |
|-----------|------------|
| No albums shown | Create `02_albums/my-album/` from `_album_template/` and run **`/orchestrate album`** |
| Only `_album_template` exists | That folder is intentionally hidden — copy it to a real album name |
| Album shows but no tracks | Add tracks under `tracks/<slug>/` and update `track_map.md` |

---

## Generate / WAV in the browser *(optional)*

These buttons call the same API as `./studio-suno`. You need:

1. A [sunoapi.org](https://sunoapi.org) account and API key *(third-party — not the same as suno.com)*
2. `SUNO_API_KEY=...` in the **repo root** `.env` file

See [../suno/README.md](../suno/README.md) for CLI setup and troubleshooting.

Without an API key you can still: read all text, play downloaded MP3s, write notes, and copy prompts into the **suno.com** UI.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `permission denied: ./studio` | Run `chmod +x studio` once, then try again |
| `python3: command not found` | Install Python 3.10+ from [python.org](https://www.python.org/downloads/) |
| Page will not load | Check Terminal still shows the server running; URL must be `http://127.0.0.1:8787` |
| Album missing | Folder must be under `02_albums/` and **not** start with `_` |
| Generate fails | Set `SUNO_API_KEY` in repo root `.env`; see [suno README](../suno/README.md) |
| No audio plays | MP3s must be in `tracks/<slug>/audio/` (from SUNO UI download or `./studio-suno generate`) |

---

## For developers

REST API at `/api/*` — see `server/main.py`.

```bash
./studio test    # run tests
./studio build   # optional frontend build (requires npm in web/)
```

Tests use fixture albums under `tests/fixtures/02_albums/`, not your live workspace.
