"""Point album scanners and studio_suno at fixture data for tests."""

from __future__ import annotations

from pathlib import Path

import pytest

FIXTURES_ROOT = Path(__file__).parent / "fixtures"
FIXTURES_ALBUMS = FIXTURES_ROOT / "02_albums"

_ALBUMS_ATTRS = (
    "server.config",
    "server.scanner",
    "server.main",
    "server.writers.archive_track",
    "server.writers.listening_notes",
    "server.writers.select_final",
    "server.writers.track_status",
)


@pytest.fixture(autouse=True)
def albums_dir(monkeypatch):
    for module in _ALBUMS_ATTRS:
        monkeypatch.setattr(f"{module}.ALBUMS_DIR", FIXTURES_ALBUMS)
    monkeypatch.setattr("studio_suno.config.REPO_ROOT", FIXTURES_ROOT)
    monkeypatch.setattr("studio_suno.paths.REPO_ROOT", FIXTURES_ROOT)
