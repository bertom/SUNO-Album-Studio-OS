# Agents — SUNO Album Studio OS

This repo is a **Markdown creative studio**, not an application codebase. Agents help the user develop SUNO albums, document runs, and maintain the archive.

## Start here

1. `00_system/project_instructions.md` — role, non-negotiables, authoritative docs
2. `00_system/mandatory_reads.md` — **required context by command/phase**
3. `00_system/commands.md` — slash commands (`/onboard artist`, `/suno`, `/orchestrate album`, …)
4. `00_system/workflow.md` — 12-phase creative cycle
5. `00_system/album_orchestrator.md` — full-album draft from `input/`

Cursor: `.cursor/rules/` reinforce the above — core rule always on; SUNO/orchestrator rules when matching files are open. Slash commands are chat instructions in `commands.md` (type them explicitly). No `.cursor/skills/` in this repo.

**First-run users:** run **`/onboard artist`** before album work — see `ONBOARDING.md`.

## Authoritative docs

| Topic | Path |
|-------|------|
| Artist DNA | `01_artist/artist_dna.md` |
| Full style reference | `01_artist/style_reference.md` |
| Cover design | `01_artist/cover_design_guide.md` |
| SUNO preparation | `00_system/suno_song_preparation_guide_v2.md` |
| SUNO API CLI (optional) | `06_integrations/suno/README.md` |
| User feedback language | `01_artist/feedback_dictionary.md` |
| Context routing by command | `00_system/mandatory_reads.md` |
| Style role → family → settings | `03_global_learnings/style_decision_matrix.md` |
| Catalog winners | `05_catalog/best_suno_outputs.md` |
| Album orchestrator | `00_system/album_orchestrator.md` |
| Operator manual | `USER_GUIDE.md` |

## Default behavior

- Update existing files before creating new ones.
- One song at a time; know the workflow phase.
- No git commits unless the user asks.
- Artist identity over genre — albums change clothes, body stays recognizable.
