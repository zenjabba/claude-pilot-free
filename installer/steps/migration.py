"""Migration step - migrates CodePro installations to Pilot."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from installer.context import InstallContext
from installer.steps.base import BaseStep


def _detect_codepro_installation(project_dir: Path) -> bool:
    """Detect if old CodePro installation exists in project directory."""
    old_ccp_dir = project_dir / ".claude" / "ccp"
    old_config = project_dir / ".claude" / "config" / "ccp-config.json"
    return old_ccp_dir.exists() or old_config.exists()


def _detect_global_codepro() -> bool:
    """Detect if old global CodePro config exists."""
    old_global_config = Path.home() / ".claude" / "config" / "ccp-config.json"
    return old_global_config.exists()


def _migrate_global_config() -> dict | None:
    """Migrate global ccp-config.json to ~/.pilot/config.json.

    Returns the migrated config dict if migration occurred, None otherwise.
    """
    old_config_path = Path.home() / ".claude" / "config" / "ccp-config.json"
    new_config_dir = Path.home() / ".pilot"
    new_config_path = new_config_dir / "config.json"

    if not old_config_path.exists():
        return None

    try:
        config = json.loads(old_config_path.read_text())

        new_config_dir.mkdir(parents=True, exist_ok=True)

        if new_config_path.exists():
            existing = json.loads(new_config_path.read_text())
            existing.update(config)
            config = existing

        new_config_path.write_text(json.dumps(config, indent=2) + "\n")

        old_config_path.unlink()
        config_dir = old_config_path.parent
        if config_dir.exists() and not any(config_dir.iterdir()):
            config_dir.rmdir()

        return config
    except (json.JSONDecodeError, OSError, IOError):
        return None


def _migrate_project_config(project_dir: Path) -> dict | None:
    """Migrate project ccp-config.json to ~/.pilot/config.json.

    Returns the migrated config dict if migration occurred, None otherwise.
    """
    old_config_path = project_dir / ".claude" / "config" / "ccp-config.json"
    new_config_dir = Path.home() / ".pilot"
    new_config_path = new_config_dir / "config.json"

    if not old_config_path.exists():
        return None

    try:
        config = json.loads(old_config_path.read_text())

        new_config_dir.mkdir(parents=True, exist_ok=True)

        if new_config_path.exists():
            existing = json.loads(new_config_path.read_text())
            for key, value in config.items():
                if key not in existing:
                    existing[key] = value
            config = existing

        new_config_path.write_text(json.dumps(config, indent=2) + "\n")

        old_config_path.unlink()
        config_dir = old_config_path.parent
        if config_dir.exists() and not any(config_dir.iterdir()):
            config_dir.rmdir()

        return config
    except (json.JSONDecodeError, OSError, IOError):
        return None


def _cleanup_old_folders(project_dir: Path) -> list[str]:
    """Remove old CodePro folders from project directory.

    Returns list of removed folder names.
    """
    removed: list[str] = []

    folders_to_remove = [
        project_dir / ".claude" / "ccp",
        project_dir / ".claude" / "bin",
        project_dir / ".claude" / "installer",
        project_dir / ".claude" / "rules" / "standard",
    ]

    for folder in folders_to_remove:
        if folder.exists():
            try:
                shutil.rmtree(folder)
                removed.append(str(folder.relative_to(project_dir)))
            except (OSError, IOError):
                pass

    old_settings = project_dir / ".claude" / "settings.local.json"
    if old_settings.exists():
        try:
            old_settings.unlink()
            removed.append(str(old_settings.relative_to(project_dir)))
        except (OSError, IOError):
            pass

    return removed


def _cleanup_global_old_folders() -> list[str]:
    """Remove old global CodePro folders.

    Returns list of removed folder paths.
    """
    removed: list[str] = []

    folders_to_remove = [
        Path.home() / ".claude" / "bin",
        Path.home() / ".claude" / "config",
    ]

    for folder in folders_to_remove:
        if folder.exists():
            try:
                shutil.rmtree(folder)
                removed.append(str(folder))
            except (OSError, IOError):
                pass

    return removed


def _preserve_custom_rules(project_dir: Path) -> int:
    """Move custom rules from old location to keep them in project.

    Custom rules stay in .claude/rules/custom/ (unchanged location).
    Returns count of preserved rules.
    """
    custom_rules_dir = project_dir / ".claude" / "rules" / "custom"
    if not custom_rules_dir.exists():
        return 0

    return len(list(custom_rules_dir.glob("*.md")))


class MigrationStep(BaseStep):
    """Step that migrates CodePro installations to Pilot."""

    name = "migration"

    def check(self, ctx: InstallContext) -> bool:
        """Check if migration is needed.

        Returns True if no migration needed (already migrated or fresh install).
        """
        has_project_codepro = _detect_codepro_installation(ctx.project_dir)
        has_global_codepro = _detect_global_codepro()
        return not has_project_codepro and not has_global_codepro

    def run(self, ctx: InstallContext) -> None:
        """Run migration from CodePro to Pilot."""
        ui = ctx.ui

        has_project_codepro = _detect_codepro_installation(ctx.project_dir)
        has_global_codepro = _detect_global_codepro()

        if not has_project_codepro and not has_global_codepro:
            return

        if ui:
            ui.status("Migrating from CodePro to Pilot...")

        migrated_config = False
        removed_folders: list[str] = []
        preserved_rules = 0

        if has_global_codepro:
            if _migrate_global_config():
                migrated_config = True
            removed_folders.extend(_cleanup_global_old_folders())

        if has_project_codepro:
            if _migrate_project_config(ctx.project_dir):
                migrated_config = True
            preserved_rules = _preserve_custom_rules(ctx.project_dir)
            removed_folders.extend(_cleanup_old_folders(ctx.project_dir))

        if ui:
            if migrated_config:
                ui.success("Config migrated to ~/.pilot/config.json")
            if preserved_rules > 0:
                ui.success(f"Preserved {preserved_rules} custom rules")
            if removed_folders:
                ui.success(f"Cleaned up {len(removed_folders)} old CodePro folders")
            ui.success("Migration complete")

        ctx.config["migration"] = {
            "config_migrated": migrated_config,
            "preserved_rules": preserved_rules,
            "removed_folders": removed_folders,
        }
