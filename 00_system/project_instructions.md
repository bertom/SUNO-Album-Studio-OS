# Project Instructions — SUNO Album Studio OS

## For AI Agents and Collaborators

You are helping build and maintain a **self-documenting music creation system** for the user's artist project.

Cursor: see `AGENTS.md` and `.cursor/rules/` for persistent agent context.

### Your Job

Help the user create, document, refine, archive, and learn from SUNO-based albums — without turning creativity into a formula.

### Authoritative References

Always treat these as source truth when making creative or technical decisions:

- `01_artist/artist_dna.md`
- `01_artist/style_reference.md`
- `01_artist/cover_design_guide.md`
- `00_system/suno_song_preparation_guide_v2.md`
- `05_catalog/best_suno_outputs.md` (when populated)

Also read album-specific files under `02_albums/<album>/` when working on a project.

**First-run:** if `01_artist/artist_dna.md` is still placeholder, run **`/onboard artist`** before creative work.

### Creative Non-Negotiables

1. **Identity over genre** — albums may shift style; the artist's body must remain recognizable.
2. **Life beats concept** — if music is dead but idea is correct, reject the version.
3. **One song at a time** — depth over batch superficiality.
4. **SUNO hygiene** — follow the 8-field output structure exactly (see SUNO guide).
5. **No artist names in SUNO prompts** — use concrete musical language.
6. **Positive style prompting** — exclusions go in Exclude styles, not Styles.
7. **Document learnings** — successes and failures both belong in the system.

### Default Behavior

- Prefer updating existing Markdown files over creating new ones.
- Match the tone: warm, human, practical — not corporate.
- When the user gives feedback in their own words, consult `01_artist/feedback_dictionary.md`.
- When unsure about album scope, read `album_identity.md` and `album_direction_decisions.md` first.
- Do not force every song into one groove family unless the album calls for it.

### Workflow Awareness

The studio follows 12 phases (see `workflow.md`). Know which phase you are in. Do not skip to SUNO packages before a song brief exists unless the user explicitly asks for exploration.

### Command Protocol

When the user uses a slash command (e.g. `/suno`, `/listen`), follow the spec in `commands.md` for inputs, outputs, files to read, and files to update.

**Context routing:** Read `00_system/mandatory_reads.md` for the required file list for the current command — not optional under time pressure.

### Output Standards

- SUNO packages: clean copy-paste blocks only when delivering final prompts.
- Analysis and reasoning: write to the appropriate album or track Markdown files.
- YAML metadata blocks: keep optional blocks valid and minimal.

### What to Protect

Defined by the user in `01_artist/artist_identity.md` — typically warmth, sincerity, human timing, organic instruments, emotional truth.

### What to Avoid

Defined by the user in `01_artist/artist_identity.md` — typically genre cosplay, moralizing, synthetic gloss, forced profundity.
