"""Parse track.md fields."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TrackMeta:
    slug: str
    title: str = ""
    status: str = "unknown"
    album_role: str = ""
    energy: str = ""
    current_focus: str = ""
    path: Path = field(default_factory=Path)


SECTION = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


def parse_track_md(path: Path, slug: str) -> TrackMeta:
    meta = TrackMeta(slug=slug, path=path.parent if path.name else Path())
    if not path.is_file():
        meta.title = slug.replace("-", " ").title()
        return meta

    text = path.read_text(encoding="utf-8")
    sections = _split_sections(text)

    meta.title = _clean(sections.get("Title", meta.title or slug.replace("-", " ").title()))
    meta.status = _extract_status(sections.get("Status", ""))
    meta.album_role = sections.get("Album Role", "").strip()
    meta.energy = sections.get("Energy", "").strip()
    meta.current_focus = sections.get("Current Focus", "").strip()
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
    return cleaned or "unknown"
