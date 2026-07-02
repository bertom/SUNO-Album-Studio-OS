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

## Why it's different

| | Typical SUNO workflow | Album Studio OS |
|---|----------------------|-----------------|
| Data | Scattered chats | Markdown in your repo |
| Identity | Per-prompt guessing | `01_artist/` DNA + feedback dictionary |
| Albums | Track lists | Arc, variation map, orchestrator |
| Learning | Forgotten | `03_global_learnings/` + catalog |
| AI | Generic | Mandatory reads + command specs |

---

## Features

- **Orchestrator** — drop notes in `input/`, get draft album through SUNO-ready prompts
- **Validate pre-flight** — `/suno validate` and `./studio-suno validate` before every run
- **Catalog backfill** — import existing SUNO albums into your winner index
- **Cover prompts** — family templates + `/cover prompt` command
- **Release prep** — metadata, checklists, distribution scaffolds
- **Variation map / album check** — cohesion before you call it done
- **One song at a time** — no batch-slop generation

---

## Quick start

1. **Clone** and open in [Cursor](https://cursor.com) (or any editor + AI).
2. **Paste** [ONBOARDING.md](ONBOARDING.md) into agent chat → **`/onboard artist`**.
3. **First album:** `/album seed` or copy `02_albums/_album_template/` → add `input/` notes → **`/orchestrate album`**.

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
06_integrations/    Optional studio-suno CLI
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

Add screenshots: [docs/SCREENSHOTS.md](docs/SCREENSHOTS.md) · `docs/images/`

---

## Requirements

- **SUNO account** (suno.com)
- **Cursor** recommended — or any AI assistant + text editor
- **Optional:** [sunoapi.org](https://sunoapi.org) API key for `studio-suno` CLI

---

## License

MIT — see [LICENSE](LICENSE). You own what you write in `01_artist/` and `02_albums/`.

---

## Contributing

Issues and PRs welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Credits

Built from SUNO Album Studio OS; whitelabeled for distribution.

**Changelog:** [CHANGELOG.md](CHANGELOG.md)
