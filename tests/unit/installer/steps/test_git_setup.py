"""Tests for git setup step."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest


class TestGitSetupStep:
    """Test GitSetupStep class."""

    def test_git_setup_step_has_correct_name(self):
        """GitSetupStep has name 'git_setup'."""
        from installer.steps.git_setup import GitSetupStep

        step = GitSetupStep()
        assert step.name == "git_setup"

    def test_check_returns_true_when_git_configured(self):
        """check() returns True when git is properly configured."""
        from installer.context import InstallContext
        from installer.steps.git_setup import GitSetupStep
        from installer.ui import Console

        step = GitSetupStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)

            # Initialize git and configure
            subprocess.run(["git", "init"], cwd=project_dir, capture_output=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=project_dir, capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=project_dir, capture_output=True)
            # Disable commit signing for test environments
            subprocess.run(["git", "config", "commit.gpgsign", "false"], cwd=project_dir, capture_output=True)

            # Create a commit
            (project_dir / ".gitignore").write_text("*.tmp\n")
            subprocess.run(["git", "add", "."], cwd=project_dir, capture_output=True)
            subprocess.run(["git", "commit", "-m", "Initial"], cwd=project_dir, capture_output=True)

            ctx = InstallContext(
                project_dir=project_dir,
                ui=Console(non_interactive=True),
            )

            assert step.check(ctx) is True

    def test_check_returns_false_when_no_git(self):
        """check() returns False when no git repository."""
        from installer.context import InstallContext
        from installer.steps.git_setup import GitSetupStep
        from installer.ui import Console

        step = GitSetupStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            ctx = InstallContext(
                project_dir=project_dir,
                ui=Console(non_interactive=True),
            )

            assert step.check(ctx) is False


class TestGitHelpers:
    """Test git helper functions."""

    def test_is_git_initialized(self):
        """is_git_initialized returns True when .git exists."""
        from installer.steps.git_setup import is_git_initialized

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            assert is_git_initialized(project_dir) is False

            subprocess.run(["git", "init"], cwd=project_dir, capture_output=True)
            assert is_git_initialized(project_dir) is True

    def test_get_git_config(self):
        """get_git_config retrieves config values."""
        from installer.steps.git_setup import get_git_config

        # This tests the global config lookup
        result = get_git_config("core.pager")
        # Result can be None or string depending on system config
        assert result is None or isinstance(result, str)

    def test_has_commits_returns_false_for_empty_repo(self):
        """has_commits returns False for empty repository."""
        from installer.steps.git_setup import has_commits

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            subprocess.run(["git", "init"], cwd=project_dir, capture_output=True)
            assert has_commits(project_dir) is False

    def test_has_commits_returns_true_with_commit(self):
        """has_commits returns True when repository has commits."""
        from installer.steps.git_setup import has_commits

        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            subprocess.run(["git", "init"], cwd=project_dir, capture_output=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=project_dir, capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=project_dir, capture_output=True)
            # Disable commit signing for test environments
            subprocess.run(["git", "config", "commit.gpgsign", "false"], cwd=project_dir, capture_output=True)
            (project_dir / "test.txt").write_text("test")
            subprocess.run(["git", "add", "."], cwd=project_dir, capture_output=True)
            subprocess.run(["git", "commit", "-m", "Initial"], cwd=project_dir, capture_output=True)
            assert has_commits(project_dir) is True


class TestGitSetupRun:
    """Test GitSetupStep.run()."""

    def test_run_initializes_git_if_needed(self):
        """run() initializes git repository if not present."""
        from installer.context import InstallContext
        from installer.steps.git_setup import GitSetupStep
        from installer.ui import Console

        step = GitSetupStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            ctx = InstallContext(
                project_dir=project_dir,
                non_interactive=True,
                ui=Console(non_interactive=True),
            )

            # Mock environment variables for non-interactive
            with patch.dict("os.environ", {"GIT_USER_NAME": "CI User", "GIT_USER_EMAIL": "ci@test.com"}):
                step.run(ctx)

            # Git should be initialized
            assert (project_dir / ".git").is_dir()

    def test_run_skips_when_already_configured(self):
        """run() skips when git is already configured."""
        from installer.context import InstallContext
        from installer.steps.git_setup import GitSetupStep
        from installer.ui import Console

        step = GitSetupStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)

            # Pre-configure git
            subprocess.run(["git", "init"], cwd=project_dir, capture_output=True)
            subprocess.run(["git", "config", "user.name", "Existing"], cwd=project_dir, capture_output=True)
            subprocess.run(["git", "config", "user.email", "existing@test.com"], cwd=project_dir, capture_output=True)
            # Disable commit signing for test environments
            subprocess.run(["git", "config", "commit.gpgsign", "false"], cwd=project_dir, capture_output=True)
            (project_dir / ".gitignore").write_text("*.tmp\n")
            subprocess.run(["git", "add", "."], cwd=project_dir, capture_output=True)
            subprocess.run(["git", "commit", "-m", "Initial"], cwd=project_dir, capture_output=True)

            ctx = InstallContext(
                project_dir=project_dir,
                non_interactive=True,
                ui=Console(non_interactive=True),
            )

            # Should complete without error
            step.run(ctx)
