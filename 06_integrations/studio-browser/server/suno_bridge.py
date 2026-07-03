"""Wrap studio-suno CLI and API for Studio Browser."""

from __future__ import annotations

import subprocess
import sys
import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from studio_suno.cli import (
    cmd_credits,
    cmd_download,
    cmd_generate,
    cmd_status,
    cmd_validate,
    cmd_wav,
)
from studio_suno.config import load_config
from studio_suno.parser import parse_prompt_file, validate_prompt_extended
from studio_suno.paths import find_prompt_file, resolve_track_path

from server.config import SUNO_DIR


@dataclass
class Job:
    id: str
    kind: str
    track: str
    status: str = "pending"
    logs: list[str] = field(default_factory=list)
    result: dict[str, Any] | None = None
    error: str | None = None
    started_at: str = ""
    finished_at: str = ""


_jobs: dict[str, Job] = {}
_active_job_id: str | None = None
_lock = threading.Lock()


class LogCapture:
    def __init__(self, job: Job):
        self.job = job
        self._buffer = ""

    def write(self, text: str) -> None:
        self._buffer += text
        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            if line.strip():
                self.job.logs.append(line)

    def flush(self) -> None:
        if self._buffer.strip():
            self.job.logs.append(self._buffer.strip())
            self._buffer = ""


def get_job(job_id: str) -> Job | None:
    return _jobs.get(job_id)


def has_active_job() -> bool:
    with _lock:
        return _active_job_id is not None


def validate_track(album_slug: str, track_slug: str, prompt: str | None = None) -> dict[str, Any]:
    track_arg = f"{album_slug}/{track_slug}"
    track_dir = resolve_track_path(track_arg)
    prompt_path = find_prompt_file(track_dir, prompt)
    prompt_obj = parse_prompt_file(prompt_path)
    config = load_config()
    errors, warnings = validate_prompt_extended(prompt_obj, config["limits"])

    return {
        "ok": len(errors) == 0,
        "prompt": prompt_path.name,
        "errors": errors,
        "warnings": warnings + prompt_obj.warnings,
        "title": prompt_obj.title,
    }


def get_credits() -> dict[str, Any]:
    config = load_config()
    try:
        import io
        from contextlib import redirect_stdout

        buf = io.StringIO()
        with redirect_stdout(buf):
            code = cmd_credits(config)
        output = buf.getvalue().strip()
        credits = 0
        for line in output.splitlines():
            if "Remaining credits:" in line:
                try:
                    credits = int(line.split(":")[-1].strip())
                except ValueError:
                    pass
        return {"credits": credits, "output": output, "ok": code == 0}
    except SystemExit as exc:
        return {"credits": None, "error": str(exc), "ok": False}
    except Exception as exc:
        return {"credits": None, "error": str(exc), "ok": False}


def start_generate(album_slug: str, track_slug: str, prompt: str | None = None) -> Job:
    global _active_job_id

    with _lock:
        if _active_job_id:
            raise RuntimeError("Another generation job is already running")

        job = Job(
            id=str(uuid.uuid4())[:8],
            kind="generate",
            track=f"{album_slug}/{track_slug}",
            started_at=datetime.now().isoformat(),
        )
        _jobs[job.id] = job
        _active_job_id = job.id

    thread = threading.Thread(
        target=_run_generate,
        args=(job, album_slug, track_slug, prompt),
        daemon=True,
    )
    thread.start()
    return job


def _run_generate(job: Job, album_slug: str, track_slug: str, prompt: str | None) -> None:
    global _active_job_id

    job.status = "running"
    capture = LogCapture(job)
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    class Tee:
        def __init__(self, original, cap):
            self.original = original
            self.cap = cap

        def write(self, text):
            self.original.write(text)
            self.cap.write(text)

        def flush(self):
            self.original.flush()
            self.cap.flush()

    try:
        sys.stdout = Tee(old_stdout, capture)
        sys.stderr = Tee(old_stderr, capture)

        import argparse

        args = argparse.Namespace(
            track=f"{album_slug}/{track_slug}",
            prompt=prompt,
            model=None,
            instrumental=False,
            wait=True,
            stream_only=False,
            dry_run=False,
        )
        config = load_config()
        code = cmd_generate(args, config)
        capture.flush()

        job.status = "complete" if code == 0 else "failed"
        job.result = {"exit_code": code}
        if code != 0:
            job.error = "Generation failed — see logs"
    except Exception as exc:
        capture.flush()
        job.status = "failed"
        job.error = str(exc)
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        job.finished_at = datetime.now().isoformat()
        with _lock:
            if _active_job_id == job.id:
                _active_job_id = None


def run_download(album_slug: str, track_slug: str, run_number: str, take: str = "both") -> dict:
    import argparse

    args = argparse.Namespace(
        track=f"{album_slug}/{track_slug}",
        run=run_number,
        take=take,
    )
    config = load_config()
    code = cmd_download(args, config)
    return {"ok": code == 0, "exit_code": code}


def run_wav(
    album_slug: str,
    track_slug: str,
    run_number: str,
    take: str = "a",
    final_name: str | None = None,
) -> dict:
    import argparse

    args = argparse.Namespace(
        track=f"{album_slug}/{track_slug}",
        run=run_number,
        take=take,
        final_name=final_name,
    )
    config = load_config()
    try:
        code = cmd_wav(args, config)
        return {"ok": code == 0, "exit_code": code}
    except SystemExit as exc:
        return {"ok": False, "error": str(exc)}


def run_status(album_slug: str, track_slug: str, run_number: str) -> dict:
    import argparse
    import io
    from contextlib import redirect_stdout

    args = argparse.Namespace(
        task_id=None,
        track=f"{album_slug}/{track_slug}",
        run=run_number,
        wav=False,
    )
    config = load_config()
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = cmd_status(args, config)
    return {"ok": code == 0, "output": buf.getvalue()}


def run_validate_cli(album_slug: str, track_slug: str, prompt: str | None = None) -> dict:
    import argparse
    import io
    from contextlib import redirect_stdout

    args = argparse.Namespace(
        track=f"{album_slug}/{track_slug}",
        prompt=prompt,
    )
    config = load_config()
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = cmd_validate(args, config)
    return {"ok": code == 0, "output": buf.getvalue()}
