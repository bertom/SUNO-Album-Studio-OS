"""Update track.md and track_map.md status."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import yaml

from server.config import ALBUMS_DIR
from server.parsers.suno_runs import update_quick_verdict


def set_track_status(album_slug: str, track_slug: str, status: str) -> list[str]:
    """Update track.md and track_map.md. Returns list of changed files."""
    changed: list[str] = []
    track_dir = ALBUMS_DIR / album_slug / "tracks" / track_slug
    track_md = track_dir / "track.md"
    track_map = ALBUMS_DIR / album_slug / "track_map.md"

    if track_md.exists():
        text = track_md.read_text(encoding="utf-8")
        new_text = re.sub(
            r"(##\s+Status\s*\n\s*)`?[^`\n]+`?",
            rf"\g<1>`{status}`",
            text,
            count=1,
            flags=re.IGNORECASE,
        )
        if new_text != text:
            track_md.write_text(new_text, encoding="utf-8")
            changed.append(str(track_md.relative_to(ALBUMS_DIR.parent)))

    if track_map.exists():
        text = track_map.read_text(encoding="utf-8")
        pattern = re.compile(
            rf"^(\|\s*\d+\s*\|\s*`?{re.escape(track_slug)}`?\s*\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|\s*)[^|]+(\s*\|)",
            re.MULTILINE,
        )
        new_text = pattern.sub(rf"\g<1>{status}\2", text)
        if new_text != text:
            track_map.write_text(new_text, encoding="utf-8")
            changed.append(str(track_map.relative_to(ALBUMS_DIR.parent)))

    return changed


def save_review_state(
    album_slug: str,
    track_slug: str,
    *,
    favorite_take: dict[str, str] | None = None,
    shortlist: bool | None = None,
    quick_tags: list[str] | None = None,
    verdict: str | None = None,
    run_number: str | None = None,
) -> Path:
    track_dir = ALBUMS_DIR / album_slug / "tracks" / track_slug
    meta_dir = track_dir / "metadata"
    meta_dir.mkdir(parents=True, exist_ok=True)
    path = meta_dir / "review_state.yaml"

    state: dict = {}
    if path.exists():
        try:
            state = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            state = {}

    state["last_reviewed"] = date.today().isoformat()
    if favorite_take is not None:
        state["favorite_take"] = favorite_take
    if shortlist is not None:
        state["shortlist"] = shortlist
    if quick_tags is not None:
        state["quick_tags"] = quick_tags

    path.write_text(yaml.dump(state, default_flow_style=False, allow_unicode=True), encoding="utf-8")

    if verdict and run_number:
        runs_md = track_dir / "suno" / "suno_runs.md"
        update_quick_verdict(runs_md, run_number, verdict)

    return path


def apply_verdict(
    album_slug: str,
    track_slug: str,
    verdict_type: str,
    run_number: str,
    take: str,
) -> dict:
    """Apply shortlist, favorite, or pass verdict."""
    verdict_map = {
        "shortlist": ("shortlist", f"**Take {take} shortlist**"),
        "favorite": ("shortlist", f"**Take {take} loved**"),
        "pass": (None, f"Pass — take {take}"),
    }
    if verdict_type not in verdict_map:
        raise ValueError(f"Unknown verdict: {verdict_type}")

    new_status, verdict_text = verdict_map[verdict_type]
    changed: list[str] = []

    if new_status:
        changed.extend(set_track_status(album_slug, track_slug, new_status))

    save_review_state(
        album_slug,
        track_slug,
        favorite_take={"run": run_number, "take": take},
        shortlist=verdict_type in ("shortlist", "favorite"),
        verdict=verdict_text,
        run_number=run_number,
    )
    changed.append(f"02_albums/{album_slug}/tracks/{track_slug}/metadata/review_state.yaml")

    return {"verdict": verdict_text, "status": new_status, "changed_files": changed}
