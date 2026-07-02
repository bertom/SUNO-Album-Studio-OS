# Catalog

Your discography memory — winners, style index, unreleased inventory.

## Empty vs populated

| State | What you have | What to do |
|-------|---------------|------------|
| **Empty** (day one) | Template rows, no real tracks | Finish first album; run **`/backfill catalog`** or **`/archive track`** per winner |
| **Growing** | Some rows in `best_suno_outputs.md` | Agents use your winners during **`/style directions`** — not generic examples |
| **Mature** | Multiple albums, style index filled | Run **`/catalog review`** between projects |

## Files in this folder

| File | Purpose |
|------|---------|
| `best_suno_outputs.md` | SUNO winners — style pull hints for agents |
| `discography.md` | Released albums and tracks |
| `released_tracks.md` | Track-level release log |
| `unreleased_tracks.md` | Shelved or in-progress inventory |
| `style_index.md` | Cross-album style family index |

## Backfill existing SUNO work

If you have albums before this studio:

1. Create `02_albums/<album-slug>/` (copy from `_album_template/`).
2. Drop masters in `tracks/<slug>/audio/`, lyrics in `lyrics/`, style notes in `suno/`.
3. Run **`/backfill catalog`** — mines winners into `best_suno_outputs.md`.

Future **`/style directions`** reads **your** catalog — not placeholder examples.
