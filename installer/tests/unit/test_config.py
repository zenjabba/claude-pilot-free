"""Tests for config module."""

import json
from pathlib import Path


class TestConfigKeyFiltering:
    """Test that config loading/saving filters out unknown keys."""

    def test_load_config_removes_unknown_keys(self, tmp_path: Path):
        """Unknown keys should be filtered out when loading config."""
        from installer.config import load_config

        config_dir = tmp_path / ".claude" / "config"
        config_dir.mkdir(parents=True)
        config_file = config_dir / "pilot-config.json"
        config_file.write_text(
            json.dumps(
                {
                    "enable_python": True,
                    "enable_agent_browser": True,
                    "old_deprecated_key": "value",
                }
            )
        )

        result = load_config(tmp_path)

        assert "enable_python" in result
        assert "enable_agent_browser" not in result
        assert "old_deprecated_key" not in result

    def test_save_config_removes_unknown_keys(self, tmp_path: Path):
        """Unknown keys should be filtered out when saving config."""
        from installer.config import save_config

        config = {
            "enable_python": True,
            "enable_agent_browser": True,
            "unknown_key": "value",
        }

        save_config(tmp_path, config)

        config_file = tmp_path / ".claude" / "config" / "pilot-config.json"
        saved = json.loads(config_file.read_text())

        assert "enable_python" in saved
        assert "enable_agent_browser" not in saved
        assert "unknown_key" not in saved

    def test_valid_keys_are_preserved(self, tmp_path: Path):
        """All valid keys should be preserved."""
        from installer.config import VALID_CONFIG_KEYS, load_config, save_config

        config = {key: True for key in VALID_CONFIG_KEYS}
        save_config(tmp_path, config)
        result = load_config(tmp_path)

        assert set(result.keys()) == VALID_CONFIG_KEYS
