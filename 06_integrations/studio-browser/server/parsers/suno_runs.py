"""Parse suno_runs.md verdicts."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class RunVerdict:
    run: str
    date: str = ""
    status: str = ""
    prompt_version: str = ""
    quick_verdict: str = ""
    task_id: str = ""


@dataclass
class SunoRunsLog:
    runs: list[RunVerdict] = field(default_factory=list)


RUN_HEADER = re.compile(r"^##\s+Run\s+(\d+)\s*(?:—\s*(.+))?\s*$", re.MULTILINE | re.IGNORECASE)


def parse_suno_runs(path: Path) -> SunoRunsLog:
    log = SunoRunsLog()
    if not path.exists():
        return log

    text = path.read_text(encoding="utf-8")
    headers = list(RUN_HEADER.finditer(text))

    for i, match in enumerate(headers):
        run_num = match.group(1).zfill(3)
        date = (match.group(2) or "").strip()
        start = match.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        block = text[start:end]

        verdict = RunVerdict(run=run_num, date=date)
        status_m = re.search(r"\*\*Status:\*\*\s*(.+)", block)
        if status_m:
            verdict.status = status_m.group(1).strip()
        prompt_m = re.search(r"\*\*Prompt version:\*\*\s*`([^`]+)`", block)
        if prompt_m:
            verdict.prompt_version = prompt_m.group(1)
        task_m = re.search(r"\*\*Task ID:\*\*\s*`([^`]+)`", block)
        if task_m:
            verdict.task_id = task_m.group(1)
        verdict_m = re.search(r"\*\*Quick verdict:\*\*\s*(.+)", block)
        if verdict_m:
            verdict.quick_verdict = verdict_m.group(1).strip()

        log.runs.append(verdict)

    return log


def update_quick_verdict(path: Path, run_number: str, verdict_text: str) -> None:
    """Update Quick verdict line for a run in suno_runs.md."""
    if not path.exists():
        return

    text = path.read_text(encoding="utf-8")
    run_num = run_number.lstrip("0") or "0"
    pattern = re.compile(
        rf"(##\s+Run\s+{run_num.lstrip('0') or '0'}\b.*?-\s*\*\*Quick verdict:\*\*\s*)(.*)",
        re.DOTALL | re.IGNORECASE,
    )
    alt_pattern = re.compile(
        rf"(##\s+Run\s+{run_number}\s*.*?-\s*\*\*Quick verdict:\*\*\s*)(.*)",
        re.DOTALL | re.IGNORECASE,
    )

    for pat in (pattern, alt_pattern):
        if pat.search(text):
            text = pat.sub(rf"\g<1>{verdict_text}", text, count=1)
            path.write_text(text, encoding="utf-8")
            return

    # Try zero-padded run number
    padded = run_number.zfill(3)
    padded_pattern = re.compile(
        rf"(##\s+Run\s+{padded}\s*.*?-\s*\*\*Quick verdict:\*\*\s*)(.*)",
        re.DOTALL | re.IGNORECASE,
    )
    if padded_pattern.search(text):
        text = padded_pattern.sub(rf"\g<1>{verdict_text}", text, count=1)
        path.write_text(text, encoding="utf-8")
