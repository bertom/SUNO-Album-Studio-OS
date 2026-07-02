"""Load config and environment."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

PACKAGE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = PACKAGE_DIR.parent.parent

DEFAULT_CONFIG: dict[str, Any] = {
    "api_base_url": "https://api.sunoapi.org",
    "callback_url": "https://localhost/noop",
    "default_model": "V5_5",
    "poll_interval_seconds": 20,
    "poll_timeout_seconds": 600,
    "credit_warning_threshold": 10,
    "limits": {
        "prompt_max": 5000,
        "style_max": 1000,
        "title_max": 100,
    },
}


def load_config() -> dict[str, Any]:
    load_dotenv(REPO_ROOT / ".env")
    config = dict(DEFAULT_CONFIG)
    config_path = PACKAGE_DIR / "config.yaml"
    if config_path.exists():
        with config_path.open(encoding="utf-8") as fh:
            user = yaml.safe_load(fh) or {}
        config.update(user)
        if "limits" in user:
            config["limits"] = {**DEFAULT_CONFIG["limits"], **user["limits"]}
    return config


def get_api_key() -> str:
    load_dotenv(REPO_ROOT / ".env")
    key = os.environ.get("SUNO_API_KEY", "").strip()
    if not key:
        raise SystemExit(
            "SUNO_API_KEY not set. Copy .env.example to repo root .env and add your key."
        )
    return key
