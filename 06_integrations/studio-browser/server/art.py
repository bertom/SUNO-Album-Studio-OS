"""Find and resolve album cover art."""

from __future__ import annotations

from pathlib import Path

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
COVER_CANDIDATES = ("cover.png", "cover.jpg", "cover.jpeg", "cover.webp")


def find_album_cover(album_dir: Path) -> dict[str, str] | None:
    """Return cover metadata if an image exists under album_art/."""
    art_dir = album_dir / "album_art"
    if not art_dir.is_dir():
        return None

    for name in COVER_CANDIDATES:
        path = art_dir / name
        if path.is_file():
            return _cover_info(album_dir, path)

    images = sorted(
        (p for p in art_dir.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS),
        key=lambda p: (not p.stem.lower().startswith("cover"), p.name.lower()),
    )
    if images:
        return _cover_info(album_dir, images[0])

    return None


def _cover_info(album_dir: Path, path: Path) -> dict[str, str]:
    rel = path.relative_to(album_dir)
    return {
        "path": str(rel),
        "filename": path.name,
        "url": f"/api/art/{album_dir.name}/{path.name}",
    }
