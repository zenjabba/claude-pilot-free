"""User configuration persistence for installer preferences."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CONFIG_DIR = ".claude/config"
CONFIG_FILE = "pilot-config.json"

VALID_CONFIG_KEYS = frozenset(
    {
        "auto_update",
        "declined_version",
        "install_mode",
        "enable_python",
        "enable_typescript",
        "enable_golang",
    }
)


def _filter_valid_keys(config: dict[str, Any]) -> dict[str, Any]:
    """Remove unknown keys from config."""
    return {k: v for k, v in config.items() if k in VALID_CONFIG_KEYS}


def get_config_path(project_dir: Path) -> Path:
    """Get the path to the config file."""
    return project_dir / CONFIG_DIR / CONFIG_FILE


def load_config(project_dir: Path) -> dict[str, Any]:
    """Load user configuration from .claude/config/pilot-config.json.

    Automatically removes any deprecated/unknown keys.
    """
    config_path = get_config_path(project_dir)
    if config_path.exists():
        try:
            raw_config = json.loads(config_path.read_text())
            return _filter_valid_keys(raw_config)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_config(project_dir: Path, config: dict[str, Any]) -> bool:
    """Save user configuration to .claude/config/pilot-config.json.

    Automatically removes any deprecated/unknown keys before saving.
    """
    config_path = get_config_path(project_dir)
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        filtered = _filter_valid_keys(config)
        config_path.write_text(json.dumps(filtered, indent=2) + "\n")
        return True
    except OSError:
        return False
