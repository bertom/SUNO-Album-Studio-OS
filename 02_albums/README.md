# Albums

One folder per album. Use `_album_template/` when starting a new project.

| Slug | Title | Status | Key files |
|------|-------|--------|-----------|
| `_album_template` | (template) | scaffold | Copy to start a new album |

**New album:** copy `_album_template/` → `02_albums/<album-slug>/`, drop notes in `input/`, run **`/orchestrate album`**.

Active albums develop tracks under `tracks/<slug>/`. Released albums may use `album_dossier.md` and `masters/` at album level.

**Review in browser (optional):** after you have MP3s in `tracks/<slug>/audio/`, run `./studio serve` from `06_integrations/studio-browser/` and open http://127.0.0.1:8787 — see [06_integrations/studio-browser/README.md](../06_integrations/studio-browser/README.md).
