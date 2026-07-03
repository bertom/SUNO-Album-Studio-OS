"""Paths and configuration."""

from __future__ import annotations

from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent.parent
INTEGRATIONS_DIR = PACKAGE_DIR.parent
REPO_ROOT = INTEGRATIONS_DIR.parent
ALBUMS_DIR = REPO_ROOT / "02_albums"
SUNO_DIR = INTEGRATIONS_DIR / "suno"
WEB_DIST = PACKAGE_DIR / "web" / "dist"
WEB_DEV = PACKAGE_DIR / "web"
