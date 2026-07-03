"""Index 02_albums/ and build API-ready structures."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml

from studio_suno.parser import parse_prompt_file, validate_prompt_extended
from studio_suno.config import load_config

from server.config import ALBUMS_DIR
from server.art import find_album_cover
from server.parsers.album_md import parse_album_md
from server.parsers.suno_runs import parse_suno_runs
from server.parsers.track_map import parse_track_map
from server.parsers.track_md import parse_track_md

PROMPT_PATTERN = re.compile(r"suno_prompt_v(\d+)\.md$")
LYRICS_PATTERN = re.compile(r"lyrics_v(\d+)\.md$")


@dataclass
class AlbumProgress:
    total: int = 0
    with_lyrics: int = 0
    with_prompt: int = 0
    with_audio: int = 0
    shortlist: int = 0
    final: int = 0


@dataclass
class AlbumSummary:
    slug: str
    title: str
    status: str
    track_count: int
    progress: AlbumProgress
    has_tracks_workspace: bool = True


def list_albums() -> list[AlbumSummary]:
    albums: list[AlbumSummary] = []
    if not ALBUMS_DIR.exists():
        return albums

    for album_dir in sorted(ALBUMS_DIR.iterdir()):
        if not album_dir.is_dir() or album_dir.name.startswith("_"):
            continue
        summary = scan_album(album_dir.name)
        if summary:
            albums.append(summary)

    # Pin draft-ready / in_progress to top
    priority = {"draft-ready": 0, "in_progress": 1, "drafting": 2}
    albums.sort(key=lambda a: (priority.get(a.status, 99), a.slug))
    return albums


def scan_album(slug: str) -> AlbumSummary | None:
    album_dir = ALBUMS_DIR / slug
    if not album_dir.is_dir():
        return None

    meta = parse_album_md(album_dir / "album.md", slug)
    track_map = parse_track_map(album_dir / "track_map.md")
    tracks_dir = album_dir / "tracks"
    has_workspace = tracks_dir.is_dir()

    progress = AlbumProgress()
    if track_map.tracks:
        progress.total = len(track_map.tracks)

    if track_map.layout == "released":
        for entry in track_map.tracks:
            if entry.lyrics_path and (album_dir / entry.lyrics_path).exists():
                progress.with_lyrics += 1
            if entry.suno_style_path and (album_dir / entry.suno_style_path).exists():
                progress.with_prompt += 1
            if entry.master and (album_dir / "masters" / Path(entry.master).name).exists():
                progress.with_audio += 1
            elif entry.master and (album_dir / "masters" / entry.master).exists():
                progress.with_audio += 1
            if entry.status == "final":
                progress.final += 1
    elif has_workspace:
        for entry in track_map.tracks:
            track_dir = tracks_dir / entry.slug
            if not track_dir.is_dir():
                continue
            if _has_lyrics(track_dir):
                progress.with_lyrics += 1
            if _has_prompt(track_dir):
                progress.with_prompt += 1
            if _has_audio(track_dir):
                progress.with_audio += 1
            if entry.status == "shortlist":
                progress.shortlist += 1
            if entry.status == "final":
                progress.final += 1

    return AlbumSummary(
        slug=slug,
        title=meta.title or slug.replace("-", " ").title(),
        status=meta.status,
        track_count=progress.total,
        progress=progress,
        has_tracks_workspace=has_workspace,
    )


def album_cover(slug: str) -> dict[str, str] | None:
    album_dir = ALBUMS_DIR / slug
    if not album_dir.is_dir():
        return None
    return find_album_cover(album_dir)


def get_album_detail(slug: str) -> dict[str, Any]:
    album_dir = ALBUMS_DIR / slug
    if not album_dir.is_dir():
        raise FileNotFoundError(f"Album not found: {slug}")

    meta = parse_album_md(album_dir / "album.md", slug)
    track_map = parse_track_map(album_dir / "track_map.md")
    tracks_dir = album_dir / "tracks"

    tracks: list[dict[str, Any]] = []
    for entry in track_map.tracks:
        if track_map.layout == "released":
            lyrics_ok = bool(entry.lyrics_path and (album_dir / entry.lyrics_path).exists())
            style_ok = bool(entry.suno_style_path and (album_dir / entry.suno_style_path).exists())
            master_path = _resolve_master_path(album_dir, entry.master)
            audio_ok = master_path is not None and master_path.exists()
            tracks.append(
                {
                    "number": entry.number,
                    "slug": entry.slug,
                    "title": entry.title,
                    "role": "",
                    "energy": "",
                    "groove": "",
                    "status": entry.status,
                    "track_md_status": entry.status,
                    "status_mismatch": False,
                    "has_lyrics": lyrics_ok,
                    "has_prompt": style_ok,
                    "has_audio": audio_ok,
                    "has_listening_notes": False,
                    "exists": True,
                    "layout": "released",
                }
            )
            continue

        track_dir = tracks_dir / entry.slug if tracks_dir.is_dir() else None
        track_md_path = (track_dir / "track.md") if track_dir and track_dir.is_dir() else Path()
        track_meta = parse_track_md(track_md_path, entry.slug)

        status = entry.status
        track_status = track_meta.status
        status_mismatch = status != track_status and track_status != "unknown"

        tracks.append(
            {
                "number": entry.number,
                "slug": entry.slug,
                "title": entry.title or track_meta.title,
                "role": entry.role,
                "energy": entry.energy,
                "groove": entry.groove,
                "status": status,
                "track_md_status": track_status,
                "status_mismatch": status_mismatch,
                "has_lyrics": _has_lyrics(track_dir) if track_dir else False,
                "has_prompt": _has_prompt(track_dir) if track_dir else False,
                "has_audio": _has_audio(track_dir) if track_dir else False,
                "has_listening_notes": _has_listening_notes(track_dir) if track_dir else False,
                "exists": track_dir.is_dir() if track_dir else False,
                "layout": "active",
            }
        )

    orchestrator = album_dir / "orchestrator_report.md"
    cover = find_album_cover(album_dir)
    return {
        "slug": slug,
        "title": meta.title,
        "status": meta.status,
        "seed": meta.seed,
        "language": meta.language,
        "path": str(album_dir),
        "cover": cover,
        "has_orchestrator_report": orchestrator.exists(),
        "layout": track_map.layout,
        "tracks": tracks,
        "cut_hold": [asdict(c) for c in track_map.cut_hold],
        "dashboard": _build_dashboard(tracks),
    }


def get_track_detail(album_slug: str, track_slug: str) -> dict[str, Any]:
    album_dir = ALBUMS_DIR / album_slug
    track_map = parse_track_map(album_dir / "track_map.md")
    map_entry = _find_track_entry(track_map, track_slug)

    if track_map.layout == "released":
        if not map_entry:
            raise FileNotFoundError(f"Track not found: {album_slug}/{track_slug}")
        return _get_released_track_detail(album_slug, album_dir, map_entry)

    track_dir = _resolve_track_dir(album_slug, track_slug)
    map_entry = map_entry or next((t for t in track_map.tracks if t.slug == track_slug), None)

    track_meta = parse_track_md(track_dir / "track.md", track_slug)
    review_state = _load_review_state(track_dir)

    lyrics_files = _list_lyrics(track_dir)
    prompt_file = _find_latest_prompt(track_dir)
    prompt_data: dict[str, Any] | None = None
    validation: dict[str, Any] | None = None

    if prompt_file:
        try:
            prompt = parse_prompt_file(prompt_file)
            config = load_config()
            errors, warnings = validate_prompt_extended(prompt, config["limits"])
            prompt_data = {
                "file": prompt_file.name,
                "path": str(prompt_file.relative_to(track_dir)),
                "fields": {
                    "lyrics": prompt.lyrics,
                    "styles": prompt.styles,
                    "exclude_styles": prompt.exclude_styles,
                    "vocal_gender": prompt.vocal_gender,
                    "weirdness_pct": prompt.weirdness_pct,
                    "style_influence_pct": prompt.style_influence_pct,
                    "title": prompt.title,
                },
            }
            validation = {"ok": len(errors) == 0, "errors": errors, "warnings": warnings + prompt.warnings}
        except Exception as exc:
            validation = {"ok": False, "errors": [str(exc)], "warnings": []}

    style_directions = _read_md_file(track_dir / "suno" / "style_directions.md")
    final_suno = _read_md_file(track_dir / "suno" / "final_suno_fields.md")
    song_brief = _read_md_file(track_dir / "song_brief.md")
    listening_notes = _read_md_file(track_dir / "analysis" / "listening_notes.md")
    suno_runs = parse_suno_runs(track_dir / "suno" / "suno_runs.md")

    runs = _load_runs(track_dir)
    audio_files = _list_audio(track_dir)

    status = map_entry.status if map_entry else track_meta.status
    status_mismatch = map_entry and map_entry.status != track_meta.status and track_meta.status != "unknown"

    return {
        "album": album_slug,
        "slug": track_slug,
        "title": track_meta.title or (map_entry.title if map_entry else track_slug.replace("-", " ").title()),
        "status": status,
        "track_md_status": track_meta.status,
        "status_mismatch": bool(status_mismatch),
        "album_role": track_meta.album_role or (map_entry.role if map_entry else ""),
        "energy": track_meta.energy or (map_entry.energy if map_entry else ""),
        "current_focus": track_meta.current_focus,
        "number": map_entry.number if map_entry else 0,
        "path": str(track_dir),
        "song_brief": song_brief,
        "lyrics_files": lyrics_files,
        "style_directions": style_directions,
        "final_suno_fields": final_suno,
        "prompt": prompt_data,
        "validation": validation,
        "runs": runs,
        "suno_runs": [asdict(r) for r in suno_runs.runs],
        "audio_files": audio_files,
        "listening_notes": listening_notes,
        "review_state": review_state,
        "layout": "active",
        "read_only": False,
    }


def _find_track_entry(track_map, track_slug: str):
    slug_lower = track_slug.lower()
    for entry in track_map.tracks:
        if entry.slug == track_slug or entry.slug.lower() == slug_lower:
            return entry
    return None


def _get_released_track_detail(album_slug: str, album_dir: Path, entry) -> dict[str, Any]:
    lyrics_files: list[dict[str, str]] = []
    if entry.lyrics_path:
        lyrics_path = album_dir / entry.lyrics_path
        if lyrics_path.exists():
            lyrics_files.append(
                {
                    "name": lyrics_path.name,
                    "path": entry.lyrics_path,
                    "content": lyrics_path.read_text(encoding="utf-8"),
                }
            )

    style_content = None
    prompt_data = None
    if entry.suno_style_path:
        style_path = album_dir / entry.suno_style_path
        if style_path.exists():
            style_content = style_path.read_text(encoding="utf-8")
            prompt_data = _parse_released_style(style_path, style_content, entry.title)

    audio_files: list[dict[str, str]] = []
    master_path = _resolve_master_path(album_dir, entry.master)
    if master_path and master_path.exists():
        audio_files.append(
            {
                "name": master_path.name,
                "path": f"masters/{master_path.name}",
                "type": master_path.suffix[1:],
            }
        )

    return {
        "album": album_slug,
        "slug": entry.slug,
        "title": entry.title,
        "status": entry.status,
        "track_md_status": entry.status,
        "status_mismatch": False,
        "album_role": "",
        "energy": "",
        "current_focus": "",
        "number": entry.number,
        "path": str(album_dir),
        "song_brief": None,
        "lyrics_files": lyrics_files,
        "style_directions": style_content,
        "final_suno_fields": style_content,
        "prompt": prompt_data,
        "validation": None,
        "runs": [],
        "suno_runs": [],
        "audio_files": audio_files,
        "listening_notes": None,
        "review_state": {},
        "layout": "released",
        "read_only": True,
    }


def _resolve_master_path(album_dir: Path, master: str) -> Path | None:
    if not master:
        return None
    name = Path(master).name
    candidates = [
        album_dir / "masters" / name,
        album_dir / "masters" / master.strip("`"),
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def _parse_released_style(path: Path, text: str, title: str) -> dict[str, Any]:
    """Extract style fields from released album style archive markdown."""
    import re

    def fenced(section: str) -> str:
        pattern = re.compile(
            rf"###\s+{re.escape(section)}\s*\n.*?```(?:text)?\n(.*?)```",
            re.DOTALL | re.IGNORECASE,
        )
        match = pattern.search(text)
        return match.group(1).strip() if match else ""

    weirdness = re.search(r"\*\*Weirdness:\*\*\s*(\d+)%?", text)
    style_inf = re.search(r"\*\*Style influence:\*\*\s*(\d+)%?", text)

    return {
        "file": path.name,
        "path": str(path.relative_to(path.parent.parent)),
        "fields": {
            "lyrics": "(see lyrics tab — released archive)",
            "styles": fenced("Styles"),
            "exclude_styles": fenced("Exclude styles"),
            "vocal_gender": "—",
            "weirdness_pct": float(weirdness.group(1)) if weirdness else 0,
            "style_influence_pct": float(style_inf.group(1)) if style_inf else 0,
            "title": title,
        },
    }


def _resolve_track_dir(album_slug: str, track_slug: str) -> Path:
    track_dir = ALBUMS_DIR / album_slug / "tracks" / track_slug
    if not track_dir.is_dir():
        raise FileNotFoundError(f"Track not found: {album_slug}/{track_slug}")
    return track_dir


def _has_lyrics(track_dir: Path) -> bool:
    lyrics_dir = track_dir / "lyrics"
    if not lyrics_dir.is_dir():
        return False
    return any(lyrics_dir.glob("lyrics*.md"))


def _has_prompt(track_dir: Path) -> bool:
    suno_dir = track_dir / "suno"
    return suno_dir.is_dir() and bool(list(suno_dir.glob("suno_prompt_v*.md")))


def _has_audio(track_dir: Path) -> bool:
    audio_dir = track_dir / "audio"
    if not audio_dir.is_dir():
        return False
    return bool(list(audio_dir.glob("run*_take_*.*")))


def _has_listening_notes(track_dir: Path) -> bool:
    path = track_dir / "analysis" / "listening_notes.md"
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    return "Run " in text and "Pending" not in text


def _list_lyrics(track_dir: Path) -> list[dict[str, str]]:
    lyrics_dir = track_dir / "lyrics"
    if not lyrics_dir.is_dir():
        return []

    files: list[tuple[int, Path]] = []
    final_path = lyrics_dir / "lyrics_final.md"
    if final_path.exists():
        files.append((9999, final_path))

    for path in lyrics_dir.glob("lyrics_v*.md"):
        match = LYRICS_PATTERN.search(path.name)
        ver = int(match.group(1)) if match else 0
        files.append((ver, path))

    files.sort(key=lambda x: x[0], reverse=True)
    return [{"name": p.name, "path": str(p.relative_to(track_dir)), "content": p.read_text(encoding="utf-8")} for _, p in files]


def _find_latest_prompt(track_dir: Path) -> Path | None:
    suno_dir = track_dir / "suno"
    if not suno_dir.is_dir():
        return None
    prompts = sorted(
        suno_dir.glob("suno_prompt_v*.md"),
        key=lambda p: int(PROMPT_PATTERN.search(p.name).group(1)) if PROMPT_PATTERN.search(p.name) else 0,
    )
    return prompts[-1] if prompts else None


def _load_runs(track_dir: Path) -> list[dict[str, Any]]:
    runs_dir = track_dir / "suno" / "runs"
    runs: list[dict[str, Any]] = []
    if not runs_dir.is_dir():
        return runs

    for path in sorted(runs_dir.glob("run_*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            runs.append(data)
        except (json.JSONDecodeError, OSError):
            continue

    runs.sort(key=lambda r: r.get("run", ""), reverse=True)
    return runs


def _list_audio(track_dir: Path) -> list[dict[str, str]]:
    audio_dir = track_dir / "audio"
    if not audio_dir.is_dir():
        return []

    files: list[dict[str, str]] = []
    for path in sorted(audio_dir.iterdir()):
        if path.suffix.lower() in (".mp3", ".wav") and path.is_file():
            files.append({"name": path.name, "path": str(path.relative_to(track_dir)), "type": path.suffix[1:]})
    return files


def _read_md_file(path: Path) -> str | None:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return None


def _load_review_state(track_dir: Path) -> dict[str, Any]:
    path = track_dir / "metadata" / "review_state.yaml"
    if not path.exists():
        return {}
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return {}


def _build_dashboard(tracks: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "total": len(tracks),
        "with_lyrics": sum(1 for t in tracks if t.get("has_lyrics")),
        "with_prompt": sum(1 for t in tracks if t.get("has_prompt")),
        "with_audio": sum(1 for t in tracks if t.get("has_audio")),
        "shortlist": sum(1 for t in tracks if t.get("status") == "shortlist"),
        "final": sum(1 for t in tracks if t.get("status") == "final"),
        "needs_review": sum(
            1
            for t in tracks
            if t.get("status") in ("suno", "shortlist") and not t.get("has_listening_notes")
        ),
        "status_mismatches": sum(1 for t in tracks if t.get("status_mismatch")),
    }
