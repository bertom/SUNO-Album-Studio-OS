"""Append listening notes sections."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from server.config import ALBUMS_DIR


def append_listening_notes(
    album_slug: str,
    track_slug: str,
    *,
    run_number: str,
    take: str,
    prompt_version: str,
    audio_file: str,
    first_feeling: str = "",
    what_worked: str = "",
    what_failed: str = "",
    decision: str = "keep exploring",
    next_move: str = "",
    quick_tags: list[str] | None = None,
) -> Path:
    track_dir = ALBUMS_DIR / album_slug / "tracks" / track_slug
    analysis_dir = track_dir / "analysis"
    analysis_dir.mkdir(parents=True, exist_ok=True)
    path = analysis_dir / "listening_notes.md"

    if not path.exists():
        path.write_text(
            "# Listening Notes\n\n"
            "Append one section per run. Template: `04_templates/listening_notes_template.md`\n\n---\n",
            encoding="utf-8",
        )

    today = date.today().isoformat()
    tags_line = ""
    if quick_tags:
        tags_line = f"\n**Quick tags:** {', '.join(quick_tags)}\n"

    section = f"""
### Run {run_number.lstrip('0') or run_number} — {today} (take {take.upper()})

**Prompt version:** {prompt_version}  
**Audio:** {audio_file}

**First feeling:** {first_feeling or '(not recorded)'}

**What worked:** {what_worked or '(not recorded)'}

**What failed:** {what_failed or '(not recorded)'}
{tags_line}
**Decision:** {decision}

**Next prompt move:** {next_move or '(none yet)'}

---
"""

    with path.open("a", encoding="utf-8") as fh:
        fh.write(section)

    return path
