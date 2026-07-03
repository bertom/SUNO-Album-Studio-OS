"""Parse track_map.md table — active and released album formats."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TrackMapEntry:
    number: int
    slug: str
    title: str
    role: str = ""
    energy: str = ""
    groove: str = ""
    status: str = "unknown"
    note: str = ""
    # Released album fields
    master: str = ""
    lyrics_path: str = ""
    suno_style_path: str = ""
    layout: str = "active"  # active | released


@dataclass
class TrackMap:
    tracks: list[TrackMapEntry] = field(default_factory=list)
    cut_hold: list[TrackMapEntry] = field(default_factory=list)
    layout: str = "active"


ACTIVE_ROW = re.compile(
    r"^\|\s*(\d+)\s*\|\s*`?([^|`]+?)`?\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|",
    re.MULTILINE,
)
RELEASED_ROW = re.compile(
    r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*`?([^|`]+?)`?\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|",
    re.MULTILINE,
)
CUT_ROW = re.compile(
    r"^\|\s*`?([^|`]+?)`?\s*\|\s*([^|]+?)\s*\|",
    re.MULTILINE,
)


def parse_track_map(path: Path) -> TrackMap:
    result = TrackMap()
    if not path.exists():
        return result

    text = path.read_text(encoding="utf-8")
    layout = _detect_layout(text)
    result.layout = layout

    if layout == "released":
        for match in RELEASED_ROW.finditer(text):
            slug = match.group(3).strip().strip("`")
            if slug.lower() in ("slug", "---"):
                continue
            result.tracks.append(
                TrackMapEntry(
                    number=int(match.group(1)),
                    title=match.group(2).strip(),
                    slug=slug,
                    master=_strip_backticks(match.group(4)),
                    lyrics_path=_strip_backticks(match.group(5)),
                    suno_style_path=_strip_backticks(match.group(6)),
                    status=match.group(7).strip().strip("`"),
                    layout="released",
                )
            )
    else:
        for match in ACTIVE_ROW.finditer(text):
            slug = match.group(2).strip().strip("`")
            if slug.lower() in ("slug", "---"):
                continue
            result.tracks.append(
                TrackMapEntry(
                    number=int(match.group(1)),
                    slug=slug,
                    title=match.group(3).strip(),
                    role=match.group(4).strip(),
                    energy=match.group(5).strip(),
                    groove=match.group(6).strip(),
                    status=match.group(7).strip().strip("`"),
                    layout="active",
                )
            )

    cut_section = re.search(r"##\s+Cut\s*/\s*Hold\s*\n(.*?)(?:\n##|\Z)", text, re.DOTALL | re.IGNORECASE)
    if cut_section:
        for match in CUT_ROW.finditer(cut_section.group(1)):
            slug = match.group(1).strip().strip("`")
            if slug.lower() in ("slug", "---"):
                continue
            result.cut_hold.append(
                TrackMapEntry(
                    number=0,
                    slug=slug,
                    title=slug.replace("-", " ").title(),
                    note=match.group(2).strip(),
                    status="cut",
                )
            )

    return result


def _detect_layout(text: str) -> str:
    """Detect active vs released track_map column order from header row."""
    header = re.search(r"^\|\s*#\s*\|(.+)\|$", text, re.MULTILINE)
    if not header:
        return "active"
    cols = [c.strip().lower() for c in header.group(1).split("|")]
    # Released: # | Title | Slug | Master | ...
    # Active:   # | Slug | Title | Role | ...
    if len(cols) >= 2 and cols[0] == "title" and cols[1] == "slug":
        return "released"
    if len(cols) >= 2 and cols[0] == "slug" and cols[1] == "title":
        return "active"
    # Fallback: look for "master" column
    if any("master" in c for c in cols):
        return "released"
    return "active"


def _strip_backticks(value: str) -> str:
    return value.strip().strip("`").strip()
