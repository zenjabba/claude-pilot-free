"""Integration tests for license verification flow.

These tests verify the complete flow without mocking, using temporary directories.
They don't make real API calls - that requires actual license keys.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest


class TestLicenseStateFlow:
    """Test complete license state management flow."""

    def test_full_license_state_lifecycle(self, tmp_path: Path) -> None:
        """Test complete state lifecycle: create, get, deactivate."""
        from ccp.auth import LicenseManager, LicenseState

        config_dir = tmp_path / "config"
        config_dir.mkdir()

        manager = LicenseManager(config_dir=config_dir)

        # Initially no license
        state = manager.get_state()
        assert state is None

        # Manually create state (simulating successful activation)
        new_state = LicenseState(
            license_key="TEST-KEY",
            tier="commercial",
            email="test@example.com",
            created_at=datetime.now(timezone.utc),
        )
        manager._save_state(new_state)

        # Now get_state returns the state
        state = manager.get_state()
        assert state is not None
        assert state.tier == "commercial"
        assert state.email == "test@example.com"

        # Deactivate
        assert manager.deactivate() is True
        state = manager.get_state()
        assert state is None

    def test_trial_expiration_flow(self, tmp_path: Path) -> None:
        """Test trial license expiration."""
        from ccp.auth import LicenseManager, LicenseState

        config_dir = tmp_path / "config"
        config_dir.mkdir()

        manager = LicenseManager(config_dir=config_dir)

        # Create trial state that hasn't expired
        now = datetime.now(timezone.utc)
        state = LicenseState(
            license_key="TRIAL",
            tier="trial",
            email="trial@example.com",
            created_at=now,
            expires_at=now + timedelta(days=5),
        )
        manager._save_state(state)

        loaded = manager.get_state()
        assert loaded is not None
        assert loaded.is_trial_expired() is False
        # days_remaining() uses delta.days which truncates, so 5 days from now returns 4
        assert loaded.days_remaining() in (4, 5)

        # Create expired trial state
        expired_state = LicenseState(
            license_key="TRIAL",
            tier="trial",
            email="trial@example.com",
            created_at=now - timedelta(days=10),
            expires_at=now - timedelta(days=3),
        )
        manager._save_state(expired_state)

        loaded = manager.get_state()
        assert loaded is not None
        assert loaded.is_trial_expired() is True
        assert loaded.days_remaining() == 0

    def test_tamper_detection_flow(self, tmp_path: Path) -> None:
        """Test tampered state files are rejected."""
        from ccp.auth import LicenseManager

        config_dir = tmp_path / "config"
        config_dir.mkdir()

        manager = LicenseManager(config_dir=config_dir)

        # Write tampered state file with invalid signature
        license_file = config_dir / ".license"
        license_file.write_text(
            json.dumps(
                {
                    "state": {
                        "license_key": "TAMPERED",
                        "tier": "commercial",
                        "email": "fake@example.com",
                        "created_at": datetime.now(timezone.utc).isoformat(),
                    },
                    "signature": "invalid_signature_that_wont_match",
                }
            )
        )

        # get_state should raise TamperedStateError for tampered files
        from ccp.auth import TamperedStateError

        try:
            manager.get_state()
            pytest.fail("Expected TamperedStateError for tampered state")
        except TamperedStateError:
            pass  # Expected

    def test_free_tier_state(self, tmp_path: Path) -> None:
        """Test free tier state creation and retrieval."""
        from ccp.auth import LicenseManager, create_free_tier_state

        config_dir = tmp_path / "config"
        config_dir.mkdir()

        state = create_free_tier_state(config_dir=config_dir, email="free@example.com")
        assert state.tier == "free"
        assert state.email == "free@example.com"
        assert state.license_key == "FREE"
        assert state.is_trial_expired() is False  # Free tier never expires
        assert state.days_remaining() is None  # No expiration for free

        # Verify it was persisted
        manager = LicenseManager(config_dir=config_dir)
        loaded = manager.get_state()
        assert loaded is not None
        assert loaded.tier == "free"
        assert loaded.email == "free@example.com"

    def test_trial_tier_state(self, tmp_path: Path) -> None:
        """Test trial tier state creation and retrieval."""
        from ccp.auth import TRIAL_DAYS, LicenseManager, create_eval_state

        config_dir = tmp_path / "config"
        config_dir.mkdir()

        state = create_eval_state(config_dir=config_dir, email="trial@example.com")
        assert state.tier == "trial"
        assert state.email == "trial@example.com"
        assert state.license_key == "TRIAL"
        assert state.is_trial_expired() is False
        # days_remaining() uses delta.days which truncates, so TRIAL_DAYS returns TRIAL_DAYS-1
        assert state.days_remaining() in (TRIAL_DAYS - 1, TRIAL_DAYS)

        # Verify it was persisted
        manager = LicenseManager(config_dir=config_dir)
        loaded = manager.get_state()
        assert loaded is not None
        assert loaded.tier == "trial"
        assert loaded.expires_at is not None


class TestCLIIntegration:
    """Test CLI commands work as module invocation."""

    def test_cli_version_as_module(self) -> None:
        """CLI can be invoked as python -m ccp --version."""
        result = subprocess.run(
            [sys.executable, "-m", "ccp", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        assert "Claude CodePro v" in result.stdout

    def test_cli_help_as_module(self) -> None:
        """CLI shows help when invoked as module."""
        result = subprocess.run(
            [sys.executable, "-m", "ccp", "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        assert "Claude CodePro" in result.stdout or "ccp" in result.stdout.lower()

    def test_cli_check_context_json(self) -> None:
        """check-context --json returns valid JSON."""
        result = subprocess.run(
            [sys.executable, "-m", "ccp", "check-context", "--json"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "status" in data
        assert "percentage" in data

    def test_cli_status_not_registered(self) -> None:
        """status command shows not registered for new install."""
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as tmp_dir:
            env = os.environ.copy()
            env["HOME"] = tmp_dir

            result = subprocess.run(
                [sys.executable, "-m", "ccp", "status"],
                capture_output=True,
                text=True,
                timeout=10,
                env=env,
            )
            # Should exit with 1 and show "not registered"
            assert result.returncode == 1
            assert "not registered" in result.stdout.lower() or "no license" in result.stdout.lower()
