"""Archive track — mirror /archive track command."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import yaml

from server.config import ALBUMS_DIR
from server.parsers.album_md import parse_album_md


def archive_track(
    album_slug: str,
    track_slug: str,
    *,
    final_audio: str,
    track_number: int = 0,
    album_title: str = "",
) -> dict:
    track_dir = ALBUMS_DIR / album_slug / "tracks" / track_slug
    album_dir = ALBUMS_DIR / album_slug
    track_md = track_dir / "track.md"
    meta_path = track_dir / "metadata" / "track_metadata.md"

    title = track_slug.replace("-", " ").title()
    if track_md.exists():
        m = re.search(r"##\s+Title\s*\n\s*(.+)", track_md.read_text(encoding="utf-8"))
        if m:
            title = m.group(1).strip()

    if not album_title and (album_dir / "album.md").exists():
        album_meta = parse_album_md(album_dir / "album.md", album_slug)
        album_title = album_meta.title

    artist = parse_album_md(album_dir / "album.md", album_slug).artist if (album_dir / "album.md").exists() else ""
    if not artist:
        artist = "Unknown Artist"

    meta_path.parent.mkdir(parents=True, exist_ok=True)

    yaml_block = {
        "title": title,
        "artist": artist,
        "album": album_title or album_slug.replace("-", " ").title(),
        "track_number": track_number or None,
        "status": "final",
        "final_audio": f"audio/{final_audio}",
        "final_lyrics": "lyrics/lyrics_final.md",
        "final_suno_prompt": "suno/final_suno_fields.md",
        "archived": date.today().isoformat(),
    }

    content = f"""# Track Metadata

## Readable Summary

| Field | Value |
|-------|-------|
| Title | {title} |
| Artist | {artist} |
| Album | {yaml_block['album']} |
| Track # | {track_number or ''} |
| Status | final |
| Final audio | audio/{final_audio} |

---

## YAML (optional — for future automation)

```yaml
{yaml.dump(yaml_block, default_flow_style=False, allow_unicode=True).strip()}
```

Update on `/archive track`.
"""
    meta_path.write_text(content, encoding="utf-8")

    return {
        "archived": True,
        "changed_files": [str(meta_path.relative_to(ALBUMS_DIR.parent))],
    }
