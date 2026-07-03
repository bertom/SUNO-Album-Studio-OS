"""Select final — mirror /select final command outputs."""

from __future__ import annotations

import re
import shutil
from datetime import date
from pathlib import Path

from server.config import ALBUMS_DIR
from server.scanner import _find_latest_prompt
from server.writers.track_status import set_track_status


def select_final(
    album_slug: str,
    track_slug: str,
    *,
    run_number: str,
    take: str,
    reason: str,
    album_fit: str = "",
    artist_fit: str = "",
) -> dict:
    track_dir = ALBUMS_DIR / album_slug / "tracks" / track_slug
    prompt_file = _find_latest_prompt(track_dir)
    prompt_name = prompt_file.name if prompt_file else "suno_prompt_v1.md"

    audio_name = f"run{run_number.zfill(3)}_take_{take}.mp3"
    wav_name = f"run{run_number.zfill(3)}_take_{take}.wav"
    audio_path = track_dir / "audio" / audio_name
    if not audio_path.exists():
        wav_path = track_dir / "audio" / wav_name
        audio_name = wav_path.name if wav_path.exists() else audio_name

    changed: list[str] = []

    # final_selection_reason.md
    reason_path = track_dir / "analysis" / "final_selection_reason.md"
    reason_path.parent.mkdir(parents=True, exist_ok=True)
    reason_content = f"""# Final Selection — {track_slug.replace('-', ' ').title()}

## Selected Version

- **Run:** {run_number}
- **Take:** {take}
- **Audio:** `audio/{audio_name}`
- **Prompt:** `{prompt_name}`
- **Date:** {date.today().isoformat()}

## Why It Won

{reason}

## Album Fit

{album_fit or 'Fits album role and energy tier.'}

## Artist Fit

{artist_fit or 'Artist DNA markers from identity files — recognizable across genre clothes.'}

## Comparison Summary

Selected over other takes/runs based on listening notes and review session.
"""
    reason_path.write_text(reason_content, encoding="utf-8")
    changed.append(str(reason_path.relative_to(ALBUMS_DIR.parent)))

    # final_suno_fields.md — copy from latest prompt
    if prompt_file and prompt_file.exists():
        final_suno = track_dir / "suno" / "final_suno_fields.md"
        prompt_text = prompt_file.read_text(encoding="utf-8")
        header = f"<!-- Frozen from {prompt_name} on {date.today().isoformat()} -->\n\n"
        final_suno.write_text(header + prompt_text, encoding="utf-8")
        changed.append(str(final_suno.relative_to(ALBUMS_DIR.parent)))

    # final_style.md — extract styles from prompt
    if prompt_file:
        styles = _extract_fenced(prompt_file.read_text(encoding="utf-8"), "Styles")
        if styles:
            style_path = track_dir / "metadata" / "final_style.md"
            style_path.parent.mkdir(parents=True, exist_ok=True)
            style_path.write_text(
                f"# Final Style\n\nFrozen {date.today().isoformat()} from `{prompt_name}`\n\n```text\n{styles}\n```\n",
                encoding="utf-8",
            )
            changed.append(str(style_path.relative_to(ALBUMS_DIR.parent)))

    # Promote lyrics_final if only draft exists
    lyrics_final = track_dir / "lyrics" / "lyrics_final.md"
    if not lyrics_final.exists() or _is_placeholder(lyrics_final):
        latest_lyrics = _find_latest_lyrics(track_dir)
        if latest_lyrics:
            shutil.copy2(latest_lyrics, lyrics_final)
            changed.append(str(lyrics_final.relative_to(ALBUMS_DIR.parent)))

    changed.extend(set_track_status(album_slug, track_slug, "final"))

    return {
        "status": "final",
        "audio": audio_name,
        "changed_files": changed,
    }


def _extract_fenced(text: str, section_name: str) -> str:
    pattern = re.compile(
        rf"###\s+{re.escape(section_name)}\s*\n.*?```(?:text)?\n(.*?)```",
        re.DOTALL | re.IGNORECASE,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def _is_placeholder(path: Path) -> bool:
    text = path.read_text(encoding="utf-8").strip()
    return len(text) < 50 or "pending" in text.lower()


def _find_latest_lyrics(track_dir: Path) -> Path | None:
    lyrics_dir = track_dir / "lyrics"
    if not lyrics_dir.is_dir():
        return None
    drafts = sorted(lyrics_dir.glob("lyrics_v*.md"))
    return drafts[-1] if drafts else None
