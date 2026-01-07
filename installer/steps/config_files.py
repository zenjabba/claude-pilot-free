"""Config files step - installs config files."""

from __future__ import annotations

from typing import TYPE_CHECKING

from installer.downloads import DownloadConfig, download_directory
from installer.steps.base import BaseStep

if TYPE_CHECKING:
    from installer.context import InstallContext


class ConfigFilesStep(BaseStep):
    """Step that installs config files."""

    name = "config_files"

    def check(self, ctx: InstallContext) -> bool:
        """Always returns False - config files should always be updated."""
        return False

    def run(self, ctx: InstallContext) -> None:
        """Install config files."""
        ui = ctx.ui

        config = DownloadConfig(
            repo_url="https://github.com/maxritter/claude-codepro",
            repo_branch="main",
            local_mode=ctx.local_mode,
            local_repo_dir=ctx.local_repo_dir,
        )

        nvmrc_file = ctx.project_dir / ".nvmrc"
        nvmrc_file.write_text("22\n")
        if ui:
            ui.success("Created .nvmrc for Node.js 22")

        qlty_dir = ctx.project_dir / ".qlty"
        if not qlty_dir.exists():
            if ui:
                with ui.spinner("Installing .qlty configuration..."):
                    count = download_directory(".qlty", qlty_dir, config)
                ui.success(f"Installed .qlty directory ({count} files)")
            else:
                download_directory(".qlty", qlty_dir, config)

    def rollback(self, ctx: InstallContext) -> None:
        """Remove generated config files."""
        pass
