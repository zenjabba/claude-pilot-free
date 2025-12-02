"""Git setup step - ensures git is properly configured."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

from installer.steps.base import BaseStep

if TYPE_CHECKING:
    from installer.context import InstallContext


def is_git_initialized(project_dir: Path) -> bool:
    """Check if git repository is initialized."""
    return (project_dir / ".git").is_dir()


def get_git_config(key: str, project_dir: Path | None = None) -> str | None:
    """Get a git config value (checks local repo config first, then global)."""
    try:
        # If project_dir is provided, check local config first
        if project_dir is not None:
            result = subprocess.run(
                ["git", "config", key],
                capture_output=True,
                text=True,
                check=False,
                cwd=project_dir,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()

        # Fall back to global config
        result = subprocess.run(
            ["git", "config", "--global", key],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def set_git_config(key: str, value: str) -> bool:
    """Set a git config value."""
    try:
        subprocess.run(
            ["git", "config", "--global", key, value],
            check=True,
            capture_output=True,
        )
        return True
    except Exception:
        return False


def has_commits(project_dir: Path) -> bool:
    """Check if the repository has at least one commit."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
            cwd=project_dir,
        )
        return result.returncode == 0
    except Exception:
        return False


def create_initial_commit(project_dir: Path) -> bool:
    """Create an initial commit with any existing files."""
    try:
        subprocess.run(
            ["git", "add", "."],
            check=True,
            capture_output=True,
            cwd=project_dir,
        )

        subprocess.run(
            ["git", "commit", "-m", "Initial commit"],
            check=True,
            capture_output=True,
            cwd=project_dir,
        )
        return True
    except Exception:
        return False


class GitSetupStep(BaseStep):
    """Step that ensures git is properly configured."""

    name = "git_setup"

    def check(self, ctx: InstallContext) -> bool:
        """Check if git is properly configured."""
        # Check if git repo exists
        if not is_git_initialized(ctx.project_dir):
            return False

        # Check if user config exists (local or global)
        if not get_git_config("user.name", ctx.project_dir):
            return False
        if not get_git_config("user.email", ctx.project_dir):
            return False

        # Check if repo has commits
        if not has_commits(ctx.project_dir):
            return False

        return True

    def run(self, ctx: InstallContext) -> None:
        """Ensure git is properly set up for the project."""
        ui = ctx.ui

        if ui:
            ui.section("Git Configuration")

        # Check git is installed
        try:
            subprocess.run(["git", "--version"], capture_output=True, check=True)
        except Exception:
            if ui:
                ui.error("Git is not installed. Please install git first.")
            return

        # Initialize git if needed
        if not is_git_initialized(ctx.project_dir):
            if ui:
                ui.status("Initializing git repository...")
            try:
                subprocess.run(
                    ["git", "init"],
                    check=True,
                    capture_output=True,
                    cwd=ctx.project_dir,
                )
                if ui:
                    ui.success("Git repository initialized")
            except Exception as e:
                if ui:
                    ui.error(f"Failed to initialize git: {e}")
                return
        else:
            if ui:
                ui.success("Git repository already initialized")

        # Configure user.name
        user_name = get_git_config("user.name")
        if not user_name:
            if ctx.non_interactive:
                user_name = os.getenv("GIT_USER_NAME")
                if not user_name:
                    if ui:
                        ui.error("Git user.name not configured. Set GIT_USER_NAME environment variable.")
                    return
            else:
                if ui:
                    ui.print()
                    ui.status("Git user.name is not configured (required for commits).")
                user_name = ui.input("Enter your name for git commits") if ui else ""
                if not user_name:
                    if ui:
                        ui.error("Name cannot be empty")
                    return

            if set_git_config("user.name", user_name):
                if ui:
                    ui.success(f"Git user.name set to: {user_name}")
            else:
                if ui:
                    ui.error("Failed to set git user.name")
                return
        else:
            if ui:
                ui.success(f"Git user.name: {user_name}")

        # Configure user.email
        user_email = get_git_config("user.email")
        if not user_email:
            if ctx.non_interactive:
                user_email = os.getenv("GIT_USER_EMAIL")
                if not user_email:
                    if ui:
                        ui.error("Git user.email not configured. Set GIT_USER_EMAIL environment variable.")
                    return
            else:
                if ui:
                    ui.print()
                    ui.status("Git user.email is not configured (required for commits).")
                user_email = ui.input("Enter your email for git commits") if ui else ""
                if not user_email:
                    if ui:
                        ui.error("Email cannot be empty")
                    return

            if set_git_config("user.email", user_email):
                if ui:
                    ui.success(f"Git user.email set to: {user_email}")
            else:
                if ui:
                    ui.error("Failed to set git user.email")
                return
        else:
            if ui:
                ui.success(f"Git user.email: {user_email}")

        # Create initial commit if needed
        if not has_commits(ctx.project_dir):
            if ui:
                ui.status("Creating initial commit...")

            # Create .gitignore if it doesn't exist
            gitignore = ctx.project_dir / ".gitignore"
            if not gitignore.exists():
                gitignore.write_text(
                    """# Environment
.env
.env.local
.env.*.local

# Dependencies
node_modules/
__pycache__/
*.pyc
.venv/
venv/

# IDE
.idea/
*.swp
*.swo

# Build
dist/
build/
*.egg-info/

# Data
data/
*.db
"""
                )
                if ui:
                    ui.success("Created .gitignore")

            if create_initial_commit(ctx.project_dir):
                if ui:
                    ui.success("Initial commit created")
            else:
                if ui:
                    ui.warning("Could not create initial commit (repository may be empty)")
        else:
            if ui:
                ui.success("Repository has commits")

    def rollback(self, ctx: InstallContext) -> None:
        """Git setup is not rolled back (would be too disruptive)."""
        pass
