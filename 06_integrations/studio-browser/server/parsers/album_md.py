"""Parse album.md fields."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class AlbumMeta:
    slug: str
    title: str = ""
    artist: str = ""
    status: str = "unknown"
    seed: str = ""
    language: str = ""
    path: Path = field(default_factory=Path)


SECTION = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


def parse_album_md(path: Path, slug: str) -> AlbumMeta:
    meta = AlbumMeta(slug=slug, path=path.parent)
    if not path.exists():
        return meta

    text = path.read_text(encoding="utf-8")
    sections = _split_sections(text)

    meta.title = _clean(sections.get("Title", slug.replace("-", " ").title()))
    meta.artist = _clean(sections.get("Artist", meta.artist))
    meta.status = _extract_status(sections.get("Status", ""))
    meta.seed = sections.get("Seed", "").strip()
    meta.language = _clean(sections.get("Language", ""))
    return meta


def _split_sections(text: str) -> dict[str, str]:
    headers = list(SECTION.finditer(text))
    sections: dict[str, str] = {}
    for i, match in enumerate(headers):
        name = match.group(1).strip()
        start = match.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        sections[name] = text[start:end].strip()
    return sections


def _clean(value: str) -> str:
    return value.strip().strip("`").strip()


def _extract_status(value: str) -> str:
    cleaned = _clean(value)
    if cleaned.startswith("`") and cleaned.endswith("`"):
        cleaned = cleaned[1:-1]
    return cleaned or "unknown"
