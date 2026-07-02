"""Run logging — suno_runs.md and JSON sidecars."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any

RUN_HEADER = re.compile(r"^##\s+Run\s+(\d+)", re.MULTILINE | re.IGNORECASE)


def next_run_number(track_dir: Path) -> str:
    numbers: list[int] = []

    runs_md = track_dir / "suno" / "suno_runs.md"
    if runs_md.exists():
        numbers.extend(int(m.group(1)) for m in RUN_HEADER.finditer(runs_md.read_text(encoding="utf-8")))

    runs_json_dir = track_dir / "suno" / "runs"
    if runs_json_dir.exists():
        for path in runs_json_dir.glob("run_*.json"):
            match = re.search(r"run_(\d+)\.json", path.name)
            if match:
                numbers.append(int(match.group(1)))

    n = max(numbers, default=0) + 1
    return f"{n:03d}"


def write_run_sidecar(track_dir: Path, run_number: str, data: dict[str, Any]) -> Path:
    path = track_dir / "suno" / "runs" / f"run_{run_number}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path


def load_run_sidecar(track_dir: Path, run_number: str) -> dict[str, Any]:
    path = track_dir / "suno" / "runs" / f"run_{run_number}.json"
    if not path.exists():
        raise SystemExit(f"Run sidecar not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def append_run_log(
    track_dir: Path,
    *,
    run_number: str,
    prompt_version: str,
    task_id: str,
    model: str,
    vocal_gender: str,
    weirdness_pct: float,
    style_influence_pct: float,
    takes: list[dict[str, Any]],
    status: str = "complete",
    error: str | None = None,
) -> None:
    runs_md = track_dir / "suno" / "suno_runs.md"
    if not runs_md.exists():
        runs_md.write_text("# SUNO Run Log\n\n", encoding="utf-8")

    today = date.today().isoformat()
    lines = [
        f"\n## Run {run_number} — {today}\n",
        f"- **Status:** {status}",
        f"- **Prompt version:** `{prompt_version}`",
        f"- **Task ID:** `{task_id}`",
        f"- **Model:** {model}",
        f"- **Vocal gender:** {vocal_gender}",
        f"- **Weirdness:** {weirdness_pct:g}%",
        f"- **Style influence:** {style_influence_pct:g}%",
    ]

    if error:
        lines.append(f"- **Error:** {error}")

    output_files: list[str] = []
    for take in takes:
        label = take.get("take", "?")
        lines.append(f"- **Take {label} audio ID:** `{take.get('audio_id', '')}`")
        if take.get("stream_url"):
            lines.append(f"- **Take {label} stream URL:** {take['stream_url']}")
        if take.get("mp3"):
            rel = _relative(track_dir, take["mp3"])
            lines.append(f"- **Take {label} MP3:** `{rel}`")
            output_files.append(rel)
        if take.get("wav"):
            rel = _relative(track_dir, take["wav"])
            lines.append(f"- **Take {label} WAV:** `{rel}`")
            output_files.append(rel)

    if output_files:
        lines.append(f"- **Output files:** {', '.join(f'`{f}`' for f in output_files)}")

    lines.extend(
        [
            "- **Quick verdict:** ",
            f"- **Listening notes:** `analysis/listening_notes.md` (section Run {run_number})",
            "",
        ]
    )

    with runs_md.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def update_sidecar_wav(track_dir: Path, run_number: str, take: str, wav_path: Path) -> None:
    sidecar = load_run_sidecar(track_dir, run_number)
    for item in sidecar.get("takes", []):
        if item.get("take") == take:
            item["wav"] = _relative(track_dir, wav_path)
            break
    write_run_sidecar(track_dir, run_number, sidecar)


def _relative(track_dir: Path, path: str | Path) -> str:
    p = Path(path)
    if p.is_absolute():
        try:
            return str(p.relative_to(track_dir))
        except ValueError:
            return str(p)
    return str(p)
