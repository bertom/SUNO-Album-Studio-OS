# SUNO Album Studio OS

**A Markdown workspace that turns life into albums — and albums into a learning system.**

SUNO gives you songs. It doesn't give you a *body of work*, a recognizable identity, or memory of what actually worked. This repo is a creative operating system: structured phases, slash commands, AI agent rules, winner catalog, and an optional API CLI — all in plain Markdown you own.

> Albums may change clothes; the body must remain recognizable.

---

## The problem

Most SUNO creators accumulate prompts and MP3s in folders with no arc, no learnings loop, and no consistent vocal or groove identity. Singles happen by accident. Albums never cohere.

## The solution

**SUNO Album Studio OS** gives you:

- A **12-phase workflow** from life seed to catalog review
- **Slash commands** (`/orchestrate album`, `/suno validate`, `/onboard artist`, …) agents understand
- An **`01_artist/` identity layer** so every album stays *you*
- A **catalog of winners** that feeds future style decisions
- **Templates** for briefs, lyrics, SUNO packages, cover prompts, release prep
- Optional **`studio-suno` CLI** for sunoapi.org — copy-paste still works
- Optional **Studio Browser** — local page to review lyrics, prompts, and MP3 takes

## Why it's different

| | Typical SUNO workflow | Album Studio OS |
|---|----------------------|-----------------|
| Data | Scattered chats | Markdown in your repo |
| Identity | Per-prompt guessing | `01_artist/` DNA + feedback dictionary |
| Albums | Track lists | Story arc, variation map, orchestration from any writing |
| Learning | Forgotten | `03_global_learnings/` + catalog |
| AI | Generic | Mandatory reads + command specs |

---

## Features

- **Album orchestration** — drop any writing in `input/`, get a story-driven draft album through SUNO-ready prompts ([how it works](#album-orchestration))
- **Validate pre-flight** — `/suno validate` and `./studio-suno validate` before every run
- **Studio Browser** — optional local UI to review tracks, compare takes, write notes ([setup](06_integrations/studio-browser/README.md))
- **Catalog backfill** — import existing SUNO albums into your winner index
- **Cover prompts** — family templates + `/cover prompt` command
- **Release prep** — metadata, checklists, distribution scaffolds
- **Variation map / album check** — cohesion before you call it done
- **One song at a time** — no batch-slop generation

---

## Album orchestration

Turn **any writing** into an album that tells **one story** — not a random track list.

Diary fragments, poems, voice-memo transcripts, half-finished lyrics, themes, audience notes, rejected ideas: if it is readable text, it belongs in `02_albums/<album>/input/`. Run **`/orchestrate album`** and a single agent runs the full studio workflow for you, stopping when every track has a review-ready SUNO package. **No audio is generated** during orchestration — you read lyrics and styles first, then generate songs one at a time.

### What the agent does

One conversation, **specialized studio roles** that hand off to each other ([agent_roles.md](00_system/agent_roles.md)):

| Role | Phase | Job |
|------|-------|-----|
| **Album Architect** | Seed → world → track pool → assembly | Theme, emotional arc, track roles, variation map |
| **Brainstorm Distiller** | Brainstorm → distill | Capture everything from `input/`, then decide what becomes songs |
| **Song Producer** | Song brief | One emotional center per track; how it fits the arc |
| **Lyric Sculptor** | Lyrics | Singable `lyrics_v1.md` from each brief |
| **Style Alchemist** | Style directions | Groove and production options that fit the album palette |
| **SUNO Engineer** | SUNO package | Copy-paste-ready `suno_prompt_v1.md` (8 fields, validated) |
| **Identity Guardian** | Every handoff | artist DNA stays recognizable — albums change clothes, body stays |

The agent states each role switch explicitly (e.g. *Switching to Lyric Sculptor — drafting lyrics v1 for `track-slug`*).

### What you get

```text
input/  (your raw writing — read only, never overwritten)
   ↓
album world (identity, arc, sonic palette, visual direction)
   ↓
brainstorms + conclusions (traceable decisions)
   ↓
track pool (each song has a unique role on the journey)
   ↓
per track: brief → lyrics → style directions → suno_prompt_v1
   ↓
orchestrator_report.md + album status draft-ready
```

After orchestration: review texts, give feedback, then **`/suno run`** or copy-paste into [suno.com](https://suno.com) — **one track at a time**.

Full spec: [album_orchestrator.md](00_system/album_orchestrator.md)

---

## Quick start

1. **Clone** and open in [Cursor](https://cursor.com) (or any editor + AI).
2. **Paste** [ONBOARDING.md](ONBOARDING.md) into agent chat → **`/onboard artist`**.
3. **First album:** copy `02_albums/_album_template/` → drop any writing in `input/` → **`/orchestrate album`** (or run `/album seed` first if you prefer a slower manual path).

Full manual: **[USER_GUIDE.md](USER_GUIDE.md)**

---

## Repository map

```text
00_system/          Workflow, commands, SUNO guide, orchestrator
01_artist/          Your identity (fill via onboarding)
02_albums/          One folder per album — start from _album_template/
03_global_learnings/  Patterns, recipes, failures
04_templates/       Reusable scaffolds
05_catalog/         Winners and discography
06_integrations/    Optional studio-suno CLI + Studio Browser
AGENTS.md             Agent entry point
ONBOARDING.md         First-run copy-paste prompt
```

---

## Workflow at a glance

```text
  ONBOARD          ALBUM SEED         SONG DEV           SUNO RUN
  artist DNA   →   world + pool   →   brief/lyrics   →   validate → generate
       │                │                  │                    │
       └────────────────┴──────────────────┴────────────────────┘
                                    │
                            listen → final → catalog
                                    │
                            next album (smarter)
```

---

## Requirements

- **Cursor** recommended — or any AI assistant + text editor (for the Markdown studio workflow)
- **To generate audio**, use one path — they are **not** the same service or linked accounts:
  - **Default:** [suno.com](https://suno.com) — copy-paste prompts from your track files into the Suno UI
  - **Optional:** [sunoapi.org](https://sunoapi.org) account + API key — for the `studio-suno` CLI and Studio Browser generate/WAV actions (third-party API, not Suno's official app)
  - **Optional:** Studio Browser — no extra account; local review only ([instructions](06_integrations/studio-browser/README.md))

You do not need both. Most users only need suno.com.

---

## License

MIT — see [LICENSE](LICENSE). You own what you write in `01_artist/` and `02_albums/`.

---

## Contributing

Issues and PRs welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Credits

Built from Inner Light Tales Studio OS; whitelabeled for distribution.

**Changelog:** [CHANGELOG.md](CHANGELOG.md)
