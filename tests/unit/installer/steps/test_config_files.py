"""Tests for config files step."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path


class TestConfigFilesStep:
    """Test ConfigFilesStep class."""

    def test_config_files_step_has_correct_name(self):
        """ConfigFilesStep has name 'config_files'."""
        from installer.steps.config_files import ConfigFilesStep

        step = ConfigFilesStep()
        assert step.name == "config_files"


class TestDirectoryInstallation:
    """Test .qlty directory installation."""

    def test_install_qlty_directory(self):
        """ConfigFilesStep installs .qlty directory."""
        from unittest.mock import patch

        from installer.context import InstallContext
        from installer.steps.config_files import ConfigFilesStep
        from installer.ui import Console

        step = ConfigFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            claude_dir = project_dir / ".claude"
            claude_dir.mkdir()

            template = {"setting": "value"}
            (claude_dir / "settings.local.template.json").write_text(json.dumps(template))

            ctx = InstallContext(
                project_dir=project_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=Path("/fake"),
            )

            with patch("installer.steps.config_files.download_directory") as mock_download:
                mock_download.return_value = 2
                step.run(ctx)

                calls = mock_download.call_args_list
                qlty_calls = [c for c in calls if ".qlty" in str(c)]
                assert len(qlty_calls) >= 1, "Should install .qlty directory"

    def test_skips_existing_directories(self):
        """ConfigFilesStep skips directories that already exist."""
        from unittest.mock import patch

        from installer.context import InstallContext
        from installer.steps.config_files import ConfigFilesStep
        from installer.ui import Console

        step = ConfigFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            claude_dir = project_dir / ".claude"
            claude_dir.mkdir()

            template = {"setting": "value"}
            (claude_dir / "settings.local.template.json").write_text(json.dumps(template))

            (project_dir / ".qlty").mkdir()

            ctx = InstallContext(
                project_dir=project_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=Path("/fake"),
            )

            with patch("installer.steps.config_files.download_directory") as mock_download:
                mock_download.return_value = 0
                step.run(ctx)

                calls = mock_download.call_args_list
                qlty_calls = [c for c in calls if ".qlty" in str(c)]
                assert len(qlty_calls) == 0, "Should skip existing .qlty"
