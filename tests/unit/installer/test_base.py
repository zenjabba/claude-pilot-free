"""Tests for installer base classes and Step protocol."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from installer.context import InstallContext


class TestStepProtocol:
    """Test Step protocol interface requirements."""

    def test_step_protocol_has_required_methods(self):
        """Step protocol must define check, run, rollback methods."""
        from installer.steps.base import Step

        # Check protocol defines required methods (compatible with Python 3.10+)
        # Use annotations or __dict__ to check for method definitions
        protocol_methods = set(Step.__annotations__.keys()) | set(
            k for k in dir(Step) if not k.startswith("_") and callable(getattr(Step, k, None))
        )
        assert "check" in protocol_methods
        assert "run" in protocol_methods
        assert "rollback" in protocol_methods

    def test_base_step_is_instance_of_step_protocol(self):
        """BaseStep instance must satisfy Step protocol."""
        from installer.steps.base import BaseStep, Step

        class TestStep(BaseStep):
            name = "test"

            def check(self, ctx) -> bool:
                return False

            def run(self, ctx) -> None:
                pass

        step = TestStep()
        assert isinstance(step, Step)

    def test_base_step_has_name_property(self):
        """BaseStep subclass must have name property."""
        from installer.steps.base import BaseStep

        class TestStep(BaseStep):
            name = "test"

            def check(self, ctx: InstallContext) -> bool:
                return False

            def run(self, ctx: InstallContext) -> None:
                pass

        step = TestStep()
        assert step.name == "test"

    def test_base_step_default_rollback_is_noop(self):
        """BaseStep default rollback should do nothing (no-op)."""
        from installer.steps.base import BaseStep

        class TestStep(BaseStep):
            name = "test"

            def check(self, ctx: InstallContext) -> bool:
                return False

            def run(self, ctx: InstallContext) -> None:
                pass

        step = TestStep()
        step.rollback(None)  # type: ignore - Should not raise

    def test_step_registry_exists(self):
        """Step registry should be available for step lookup."""
        from installer.steps import STEP_REGISTRY

        assert isinstance(STEP_REGISTRY, dict)


class TestInstallerPackage:
    """Test installer package structure."""

    def test_installer_has_build(self):
        """Installer package must have __build__ for CI timestamp."""
        import installer

        assert hasattr(installer, "__build__")
        assert isinstance(installer.__build__, str)
        # Build should contain date-like format or "dev"
        assert len(installer.__build__) > 0
