"""Unit tests for unified CLI entry point."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

runner = CliRunner()


class TestCLIVersion:
    """Tests for version command."""

    def test_version_flag_shows_version(self) -> None:
        """--version shows the package version."""
        from ccp.cli import app

        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "Claude CodePro v" in result.stdout


class TestCLIActivate:
    """Tests for activate command."""

    def test_activate_with_valid_key(self, tmp_path: Path) -> None:
        """activate command activates a valid license key."""
        from ccp.cli import app

        mock_result = MagicMock()
        mock_result.success = True
        mock_result.seats_total = 5
        mock_result.seats_used = 1
        mock_result.tier = "commercial"

        with patch("ccp.cli.LicenseManager") as mock_manager_class:
            mock_manager = MagicMock()
            mock_manager.activate.return_value = mock_result
            mock_manager_class.return_value = mock_manager

            result = runner.invoke(app, ["activate", "TEST-KEY-1234"])

        assert result.exit_code == 0
        assert "activated" in result.stdout.lower() or "success" in result.stdout.lower()

    def test_activate_with_invalid_key(self, tmp_path: Path) -> None:
        """activate command fails with invalid license key."""
        from ccp.cli import app

        mock_result = MagicMock()
        mock_result.success = False
        mock_result.error = "Invalid license key"

        with patch("ccp.cli.LicenseManager") as mock_manager_class:
            mock_manager = MagicMock()
            mock_manager.activate.return_value = mock_result
            mock_manager_class.return_value = mock_manager

            result = runner.invoke(app, ["activate", "INVALID-KEY"])

        assert result.exit_code == 1

    def test_activate_json_output(self) -> None:
        """activate --json outputs JSON format."""
        from ccp.cli import app

        mock_result = MagicMock()
        mock_result.success = True
        mock_result.seats_total = 5
        mock_result.seats_used = 1
        mock_result.tier = "commercial"
        mock_result.error = ""

        with patch("ccp.cli.LicenseManager") as mock_manager_class:
            mock_manager = MagicMock()
            mock_manager.activate.return_value = mock_result
            mock_manager_class.return_value = mock_manager

            result = runner.invoke(app, ["activate", "TEST-KEY", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.stdout)
        assert data["success"] is True
        assert "seats_total" in data


class TestCLIStatus:
    """Tests for status command."""

    def test_status_shows_license_info(self) -> None:
        """status command shows license information."""
        from ccp.cli import app

        mock_license_info = {
            "tier": "commercial",
            "email": "test@example.com",
            "created_at": "2026-01-01T00:00:00+00:00",
            "expires_at": None,
            "days_remaining": None,
            "is_expired": False,
        }

        with patch("ccp.cli.LicenseManager") as mock_manager_class:
            mock_manager = MagicMock()
            mock_manager.get_license_info.return_value = mock_license_info
            mock_manager_class.return_value = mock_manager

            result = runner.invoke(app, ["status"])

        assert result.exit_code == 0

    def test_status_json_output(self) -> None:
        """status --json outputs JSON format with all fields."""
        from ccp.cli import app

        mock_license_info = {
            "tier": "commercial",
            "email": "test@example.com",
            "created_at": "2026-01-01T00:00:00+00:00",
            "expires_at": None,
            "days_remaining": None,
            "is_expired": False,
        }

        with patch("ccp.cli.LicenseManager") as mock_manager_class:
            mock_manager = MagicMock()
            mock_manager.get_license_info.return_value = mock_license_info
            mock_manager_class.return_value = mock_manager

            result = runner.invoke(app, ["status", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.stdout)
        assert "success" in data
        assert "tier" in data
        assert "email" in data
        assert "created_at" in data

    def test_status_not_registered(self) -> None:
        """status shows not registered when no license exists."""
        from ccp.cli import app

        with patch("ccp.cli.LicenseManager") as mock_manager_class:
            mock_manager = MagicMock()
            mock_manager.get_license_info.return_value = None
            mock_manager_class.return_value = mock_manager

            result = runner.invoke(app, ["status"])

        assert result.exit_code == 1
        assert "not registered" in result.stdout.lower()

    def test_status_trial_expired(self) -> None:
        """status shows trial expired when trial is expired."""
        from ccp.cli import app

        mock_license_info = {
            "tier": "trial",
            "email": "test@example.com",
            "created_at": "2026-01-01T00:00:00+00:00",
            "expires_at": "2026-01-08T00:00:00+00:00",
            "days_remaining": 0,
            "is_expired": True,
        }

        with patch("ccp.cli.LicenseManager") as mock_manager_class:
            mock_manager = MagicMock()
            mock_manager.get_license_info.return_value = mock_license_info
            mock_manager_class.return_value = mock_manager

            result = runner.invoke(app, ["status"])

        assert result.exit_code == 1
        assert "expired" in result.stdout.lower()


class TestCLICheckContext:
    """Tests for check-context command."""

    def test_check_context_returns_status(self) -> None:
        """check-context returns OK or CLEAR_NEEDED."""
        from ccp.cli import app

        with patch("ccp.cli.get_context_percentage", return_value=50.0):
            result = runner.invoke(app, ["check-context"])

        assert result.exit_code == 0
        assert "OK" in result.stdout

    def test_check_context_json_output(self) -> None:
        """check-context --json outputs JSON format."""
        from ccp.cli import app

        with patch("ccp.cli.get_context_percentage", return_value=50.0):
            result = runner.invoke(app, ["check-context", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.stdout)
        assert data["status"] == "OK"
        assert "percentage" in data


class TestCLISendClear:
    """Tests for send-clear command."""

    def test_send_clear_returns_success(self) -> None:
        """send-clear returns success when pipe available."""
        from ccp.cli import app

        with patch("ccp.cli.send_clear", return_value=True):
            result = runner.invoke(app, ["send-clear"])

        assert result.exit_code == 0

    def test_send_clear_with_plan_path(self) -> None:
        """send-clear with plan path sends clear-continue."""
        from ccp.cli import app

        with patch("ccp.cli.send_clear", return_value=True) as mock_send:
            result = runner.invoke(app, ["send-clear", "docs/plan.md"])

        mock_send.assert_called_once_with(plan_path="docs/plan.md", general=False)
        assert result.exit_code == 0

    def test_send_clear_general_flag(self) -> None:
        """send-clear --general sends general continuation."""
        from ccp.cli import app

        with patch("ccp.cli.send_clear", return_value=True) as mock_send:
            result = runner.invoke(app, ["send-clear", "--general"])

        mock_send.assert_called_once_with(plan_path=None, general=True)
        assert result.exit_code == 0


class TestCLIDeactivate:
    """Tests for deactivate command."""

    def test_deactivate_removes_license(self) -> None:
        """deactivate removes the license file."""
        from ccp.cli import app

        with patch("ccp.cli.LicenseManager") as mock_manager_class:
            mock_manager = MagicMock()
            mock_manager.deactivate.return_value = True
            mock_manager_class.return_value = mock_manager

            result = runner.invoke(app, ["deactivate"])

        assert result.exit_code == 0
        assert "deactivated" in result.stdout.lower()
