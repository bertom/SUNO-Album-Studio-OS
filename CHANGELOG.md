# Changelog

## v1.0.0 — 2026-07-02

**Whitelabel release — SUNO Album Studio OS**

First public distribution of the Markdown-first album studio formerly built as a private artist workspace.

### Added

- Generic `01_artist/` scaffold with **`/onboard artist`** first-run command
- `USER_GUIDE.md`, `ONBOARDING.md`, `05_catalog/README.md`, `01_artist/README.md`
- `docs/SCREENSHOTS.md` placeholder for marketing assets
- `.env.example` for optional SUNO API CLI
- MIT `LICENSE`

### Changed

- Product branding: **SUNO Album Studio OS** (identity-over-genre, any musician)
- CLI renamed: `ilt-suno` → **`studio-suno`** (`studio_suno` Python package)
- Cover prompt families genericized (removed album-specific preset names)
- `03_global_learnings/` and catalog files → empty templates with example rows
- All agent rules, mandatory reads, and commands updated for generic paths

### Removed

- Artist-specific albums, masters, personal archive, and session history
- ILT-specific DNA, feedback dictionary, and style reference files

### Provenance

Built from SUNO Album Studio OS; whitelabeled for distribution.

### Migration note

If you forked an older private copy: run fresh `git init` for a clean public history. Old `./studio-suno` invocations → `./studio-suno`.
