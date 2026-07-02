# Input

Drop raw material here for the album orchestrator. This folder is **read-only** for agents — files stay as you wrote them.

## What belongs here

Anything readable that might become an album:

- Life seeds, diary fragments, voice-note transcripts
- Rough tracklist ideas or song titles
- Poem scraps, mantras, phrases you don't want to lose
- Audience notes ("for kids who feel too much")
- Mood references, season, place, memory
- Rejected ideas from other projects
- Pasted conversations or emails (redact private details if needed)

## Format

- `.md`, `.txt`, or any plain readable text
- **No required structure** — messy is fine
- Multiple files welcome; name them whatever helps you find them

## What happens next

Run `/orchestrate album` (or point an agent at `00_system/album_orchestrator.md`).

The orchestrator reads everything here, then builds the album through the normal studio workflow — brainstorms, conclusions, track pool, song briefs, lyrics, style directions, and SUNO prompt packages — in `02_albums/<album>/` outside this folder.

**Default language:** English unless you specify otherwise in input or when starting the run.

**Audio is not generated** during orchestration. You review lyrics and styles first, then generate tracks one at a time.

## Tips

- More life detail beats clever concepts
- Contradictions in your notes are useful — don't clean them up before dropping them here
- A working title in a filename is optional; the title often emerges during album world
