"""Resolve track paths within the Studio OS repo."""

from __future__ import annotations

import re
from pathlib import Path

from .config import REPO_ROOT

PROMPT_PATTERN = re.compile(r"suno_prompt_v(\d+)\.md$")


def resolve_track_path(track_arg: str) -> Path:
    """Resolve a track path from slug, album/track, or full path."""
    raw = Path(track_arg)
    if raw.is_absolute() and raw.exists():
        return _ensure_track(raw)

    candidates: list[Path] = []
    parts = raw.parts

    if len(parts) == 2:
        album, slug = parts
        candidates.append(REPO_ROOT / "02_albums" / album / "tracks" / slug)

    if len(parts) >= 2:
        candidates.append(REPO_ROOT / "02_albums" / raw)

    if len(parts) == 1:
        slug = parts[0]
        for album_dir in sorted((REPO_ROOT / "02_albums").iterdir()):
            if album_dir.is_dir() and not album_dir.name.startswith("_"):
                candidates.append(album_dir / "tracks" / slug)
        # Template track for validation / testing
        candidates.append(REPO_ROOT / "02_albums" / "_album_template" / "tracks" / slug)

    seen: set[Path] = set()
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if resolved.exists() and (resolved / "suno").is_dir():
            return _ensure_track(resolved)

    raise SystemExit(f"Track not found: {track_arg}")


def _ensure_track(path: Path) -> Path:
    if not (path / "suno").is_dir():
        raise SystemExit(f"Not a track folder (missing suno/): {path}")
    return path.resolve()


def find_prompt_file(track_dir: Path, prompt_version: str | None = None) -> Path:
    suno_dir = track_dir / "suno"
    if prompt_version:
        name = prompt_version if prompt_version.endswith(".md") else f"suno_prompt_{prompt_version}.md"
        path = suno_dir / name
        if not path.exists():
            raise SystemExit(f"Prompt file not found: {path}")
        return path

    prompts = sorted(
        suno_dir.glob("suno_prompt_v*.md"),
        key=lambda p: int(PROMPT_PATTERN.search(p.name).group(1)) if PROMPT_PATTERN.search(p.name) else 0,
    )
    if not prompts:
        raise SystemExit(f"No suno_prompt_vN.md files in {suno_dir}")
    return prompts[-1]


def audio_dir(track_dir: Path) -> Path:
    path = track_dir / "audio"
    path.mkdir(parents=True, exist_ok=True)
    return path


def runs_dir(track_dir: Path) -> Path:
    path = track_dir / "suno" / "runs"
    path.mkdir(parents=True, exist_ok=True)
    return path


def album_config_path(track_dir: Path) -> Path | None:
    album_dir = track_dir.parent.parent
    candidate = album_dir / "suno_config.yaml"
    return candidate if candidate.exists() else None
