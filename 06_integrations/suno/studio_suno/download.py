"""Download audio files from URLs."""

from __future__ import annotations

from pathlib import Path

import requests


def download_file(url: str, dest: Path) -> Path:
    if not url:
        raise ValueError("Empty download URL")

    dest.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, timeout=300, stream=True)
    response.raise_for_status()

    with dest.open("wb") as fh:
        for chunk in response.iter_content(chunk_size=65536):
            if chunk:
                fh.write(chunk)

    return dest
