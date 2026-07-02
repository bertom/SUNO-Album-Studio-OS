# User Guide — SUNO Album Studio OS

Warm, practical manual for musicians who use SUNO and Cursor (or any AI assistant).

**Quick links:** [ONBOARDING.md](ONBOARDING.md) · [README.md](README.md) · [commands.md](00_system/commands.md) · [workflow.md](00_system/workflow.md)

---

## What this is

SUNO Album Studio OS is a **Markdown workspace** for making albums — not random singles. Your identity, lyrics, style decisions, SUNO prompts, listening notes, and learnings live in plain files you own. No cloud lock-in, no proprietary DAW.

It is **not a web app**. You work in folders, slash commands, and AI chat. SUNO still generates the audio — manually in the UI or optionally via the API CLI.

---

## Who it's for

- SUNO creators who want a **body of work**, not a folder of unrelated prompts
- Musicians who think in **albums and arcs**, not one-off experiments
- Anyone willing to spend one session onboarding their **artist identity** so every future song stays recognizable

You don't need to be a developer. You need SUNO, a text editor, and (recommended) Cursor.

---

## 5-minute start

1. **Clone** this repo and open it in Cursor.
2. **Paste** the prompt from [ONBOARDING.md](ONBOARDING.md) into a new agent chat.
3. Complete **`/onboard artist`** — fills `01_artist/` with your DNA.
4. **Start an album:** run **`/album seed`** *or* copy `02_albums/_album_template/` to `02_albums/my-album/`, drop notes in `input/`, run **`/orchestrate album`**.

Next: develop one track at a time → **`/suno validate`** → generate in SUNO → **`/listen`** → **`/select final`**.

---

## How it's organized

```text
00_system/          Workflow, commands, SUNO guide, orchestrator
01_artist/          Your identity — DNA, style, feedback dictionary
02_albums/          One folder per album (_album_template/ to copy)
03_global_learnings/  Cross-album patterns you discover
04_templates/       Document scaffolds (briefs, cover prompts, etc.)
05_catalog/         Winners, discography, style index
06_integrations/    Optional studio-suno CLI (sunoapi.org)
```

Deep map: [README.md](README.md#repository-map).

---

## The 12 phases (you are here)

| Phase | Plain language | Typical command |
|-------|----------------|-----------------|
| 1 Album Seed | Life moment → album question | `/album seed` |
| 2 Album World | Identity, arc, sound, visual | `/album world` |
| 3 Brainstorm | Capture everything, no filter | `/brainstorm` |
| 4 Distillation | Decide, reject, open questions | `/distill brainstorm` |
| 5 Song Pool | Candidates with roles | `/song pool` |
| 6 Song Development | One track: brief → lyrics → style | `/song brief`, `/lyrics`, `/style directions` |
| 7 SUNO Run Cycle | Generate, log, listen, retry | `/suno`, `/suno run`, `/listen`, `/retry` |
| 8 Final Selection | Pick the keeper | `/select final` |
| 9 Album Assembly | Cohesion, variation map | `/album check`, `/update track map` |
| 10 Archive & Learn | Finals + learnings | `/archive track`, learning entries |
| 11 Release Prep | Pitch, metadata, cover | `/cover prompt`, release templates |
| 12 Catalog Review | Discography, style index | `/catalog review`, `/backfill catalog` |

Full detail: [workflow.md](00_system/workflow.md).

**Rule of thumb:** Don't jump to phase 7 until phase 6 exists for that track (brief + lyrics + style direction).

---

## Slash commands cheat sheet

| Command | When to use | What you get |
|---------|-------------|--------------|
| `/onboard artist` | First run | Filled `01_artist/` scaffold |
| `/album seed` | New album from a life seed | Draft `album.md` |
| `/orchestrate album` | Raw notes in `input/` | Full draft album through SUNO prompts |
| `/album world` | Define album identity | identity, arc, palette, visual docs |
| `/song brief` | Start one track | `song_brief.md` |
| `/lyrics` | Write or revise lyrics | Versioned `lyrics_vN.md` |
| `/style directions` | Groove + production plan | `style_directions.md` |
| `/suno` | Build 8-field SUNO package | `suno_prompt_vN.md` |
| `/suno validate` | Before every SUNO run | Hygiene check (no API) |
| `/suno run` | API generation | MP3s via CLI |
| `/listen` | After a run | Structured listening notes |
| `/retry` | Fix a failed run | Adjusted prompt + learning draft |
| `/select final` | Choose keeper | Final docs + metadata |
| `/archive track` | Lock a winner | Catalog-ready archive |
| `/backfill catalog` | Import old SUNO work | Rows in `best_suno_outputs.md` |
| `/album check` | Before calling album done | Cohesion rubric |
| `/cover prompt` | Album art direction | `cover_prompt_vN.md` |
| `/catalog review` | Between projects | Updated discography |

Full specs: [commands.md](00_system/commands.md).

---

## Working with AI

1. Point the agent at **[AGENTS.md](AGENTS.md)** — entry point for cold sessions.
2. Use **slash commands** instead of vague requests ("run `/suno validate` on track X").
3. **One song at a time** — depth beats batch-generating an album in SUNO.
4. Agents must read **[mandatory_reads.md](00_system/mandatory_reads.md)** for your current command — not optional.

Cursor users: rules in `.cursor/rules/` apply automatically when relevant files are open.

---

## SUNO workflow

### Manual (default)

1. Agent writes `suno_prompt_vN.md` (8 fields).
2. Run **`/suno validate`** (or `./studio-suno validate <track>`).
3. Copy fields into SUNO UI.
4. Log run in `suno_runs.md`; listen with **`/listen`**.

### Optional API CLI

See [06_integrations/suno/README.md](06_integrations/suno/README.md).

```bash
cp .env.example .env   # add SUNO_API_KEY
cd 06_integrations/suno && pip install -r requirements.txt
./studio-suno validate my-album/track-slug
./studio-suno generate my-album/track-slug
```

Manual copy-paste remains fully supported.

---

## Pre-flight — always validate

Before every SUNO run:

- **`/suno validate`** — checks field order, positive Styles, no artist names, settings sanity
- Or: `./studio-suno validate <album>/<track>`

See [suno_song_preparation_guide_v2.md](00_system/suno_song_preparation_guide_v2.md) and [suno_learnings.md](03_global_learnings/suno_learnings.md).

---

## Building your catalog

Winners become future reference:

1. **`/select final`** + **`/archive track`** on each keeper.
2. Row lands in **[best_suno_outputs.md](05_catalog/best_suno_outputs.md)**.
3. Future **`/style directions`** matches 2–3 winners by role/energy.

**Existing SUNO history?** Create album folder, drop masters + lyrics + styles, run **`/backfill catalog`**. See [05_catalog/README.md](05_catalog/README.md).

---

## Orchestrated album

For a full draft from messy notes:

1. Copy `02_albums/_album_template/` → `02_albums/my-album/`.
2. Drop raw material in `input/` (lyrics fragments, voice memos transcribed, themes).
3. Run **`/orchestrate album`** on `02_albums/my-album/`.
4. Review lyrics and styles **before** generating audio — orchestrator stops at draft-ready.
5. Generate **one track at a time** in SUNO.

Spec: [album_orchestrator.md](00_system/album_orchestrator.md).

---

## FAQ

**Do I need the API?**  
No. Copy-paste to [suno.com](https://suno.com) is the default path.

**Are suno.com and sunoapi.org the same?**  
No. sunoapi.org is a **third-party** API used only by the optional `studio-suno` CLI. Separate signup, separate billing — not linked to your Suno app account.

**Can I use ChatGPT instead of Cursor?**  
Yes. Paste `AGENTS.md`, `commands.md`, and mandatory reads into context. Slash commands still work as instructions.

**Where do WAVs go?**  
`02_albums/<album>/tracks/<slug>/audio/` — never commit large masters if you publish the repo; `.gitignore` excludes `*.wav` and `*.mp3`.

**Can I use this for any genre?**  
Yes. Identity over genre — your `01_artist/` files define the body; albums change clothes.

**How many tracks per album?**  
Usually 8–16; let the story decide. Orchestrator default is flexible.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Empty `input/` for orchestrator | Add notes or run `/album seed` first |
| Agent skips reading files | Name the command explicitly; cite `mandatory_reads.md` |
| SUNO rejects lyrics | Check sensitive words — see `suno_learnings.md` |
| `skank` in styles breaks | Use concrete description in Styles; exclusions in Exclude styles |
| Negative words in Styles | Move to **Exclude styles** — SUNO guide forbids "no dub" in Styles |
| CLI `SUNO_API_KEY not set` | Copy `.env.example` → `.env` at repo root |
| Agent uses placeholder DNA | Run `/onboard artist` — empty templates aren't enough |

---

*Albums may change clothes; the body must remain recognizable.*
