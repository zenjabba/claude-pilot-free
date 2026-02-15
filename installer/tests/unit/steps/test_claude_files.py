"""Tests for pilot files installation step."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import patch


class TestPatchClaudePaths:
    """Test the patch_claude_paths function."""

    def test_patch_claude_paths_leaves_plugin_path_unchanged(self):
        """patch_claude_paths does NOT expand ~/.claude/pilot (hooks use ${CLAUDE_PLUGIN_ROOT})."""
        from installer.steps.claude_files import patch_claude_paths

        content = '{"command": "~/.claude/pilot/scripts/worker.cjs"}'
        result = patch_claude_paths(content)

        assert content == result

    def test_patch_claude_paths_expands_tilde_bin_path(self):
        """patch_claude_paths expands ~/.pilot/bin/ to absolute path."""
        from pathlib import Path as P

        from installer.steps.claude_files import patch_claude_paths

        content = '{"command": "~/.pilot/bin/pilot statusline"}'
        result = patch_claude_paths(content)

        expected_bin = str(P.home() / ".pilot" / "bin") + "/"
        assert '"~/.pilot/bin/' not in result
        assert expected_bin in result

    def test_patch_claude_paths_only_expands_bin_path(self):
        """patch_claude_paths only expands ~/.pilot/bin/, not ~/.claude/pilot."""
        from pathlib import Path as P

        from installer.steps.claude_files import patch_claude_paths

        content = """{
            "command": "~/.claude/pilot/scripts/worker.cjs",
            "statusLine": {"command": "~/.pilot/bin/pilot statusline"}
        }"""
        result = patch_claude_paths(content)

        expected_bin = str(P.home() / ".pilot" / "bin") + "/"
        assert expected_bin in result
        assert "~/.claude/pilot" in result

    def test_patch_claude_paths_preserves_non_tilde_paths(self):
        """patch_claude_paths leaves non-tilde paths unchanged."""
        from installer.steps.claude_files import patch_claude_paths

        content = '{"path": "/usr/local/bin/something"}'
        result = patch_claude_paths(content)

        assert result == content


class TestProcessSettings:
    """Test the process_settings function."""

    def test_process_settings_round_trips_json(self):
        """process_settings parses and re-serializes JSON with consistent formatting."""
        from installer.steps.claude_files import process_settings

        settings = {"hooks": {"PostToolUse": [{"matcher": "Write", "hooks": []}]}, "model": "opus"}
        result = process_settings(json.dumps(settings))
        parsed = json.loads(result)

        assert parsed == settings
        assert result.endswith("\n")

    def test_process_settings_preserves_all_hooks(self):
        """process_settings preserves all language hooks without filtering."""
        from installer.steps.claude_files import process_settings

        python_hook = "uv run python ~/.claude/pilot/hooks/file_checker_python.py"
        ts_hook = "uv run python ~/.claude/pilot/hooks/file_checker_ts.py"
        go_hook = "uv run python ~/.claude/pilot/hooks/file_checker_go.py"
        settings = {
            "hooks": {
                "PostToolUse": [
                    {
                        "matcher": "Write|Edit|MultiEdit",
                        "hooks": [
                            {"type": "command", "command": python_hook},
                            {"type": "command", "command": ts_hook},
                            {"type": "command", "command": go_hook},
                        ],
                    }
                ]
            }
        }

        result = process_settings(json.dumps(settings))
        parsed = json.loads(result)

        hooks = parsed["hooks"]["PostToolUse"][0]["hooks"]
        assert len(hooks) == 3


class TestClaudeFilesStep:
    """Test ClaudeFilesStep class."""

    def test_claude_files_step_has_correct_name(self):
        """ClaudeFilesStep has name 'claude_files'."""
        from installer.steps.claude_files import ClaudeFilesStep

        step = ClaudeFilesStep()
        assert step.name == "claude_files"

    def test_claude_files_check_returns_false_when_empty(self):
        """ClaudeFilesStep.check returns False when no files installed."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            ctx = InstallContext(
                project_dir=Path(tmpdir),
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=Path(tmpdir),
            )
            assert step.check(ctx) is False

    def test_claude_files_run_installs_files(self):
        """ClaudeFilesStep.run installs pilot files."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            home_dir = Path(tmpdir) / "home"
            home_dir.mkdir()

            source_pilot = Path(tmpdir) / "source" / "pilot"
            source_pilot.mkdir(parents=True)
            (source_pilot / "test.md").write_text("test content")
            (source_pilot / "rules").mkdir()
            (source_pilot / "rules" / "rule.md").write_text("rule content")

            dest_dir = Path(tmpdir) / "dest"
            dest_dir.mkdir()

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=Path(tmpdir) / "source",
            )

            with patch("installer.steps.claude_files.Path.home", return_value=home_dir):
                step.run(ctx)

            assert (home_dir / ".claude" / "rules" / "rule.md").exists()

    def test_claude_files_installs_settings(self):
        """ClaudeFilesStep installs settings.json to ~/.claude/."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            home_dir = Path(tmpdir) / "home"
            home_dir.mkdir()

            source_pilot = Path(tmpdir) / "source" / "pilot"
            source_pilot.mkdir(parents=True)
            (source_pilot / "settings.json").write_text('{"hooks": {}}')

            dest_dir = Path(tmpdir) / "dest"
            dest_dir.mkdir()

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=Path(tmpdir) / "source",
            )

            with patch("installer.steps.claude_files.Path.home", return_value=home_dir):
                step.run(ctx)

            assert (home_dir / ".claude" / "settings.json").exists()


class TestClaudeFilesCustomRulesPreservation:
    """Test that standard rules from repo are installed and project rules preserved."""

    def test_standard_rules_installed_and_project_rules_preserved(self):
        """ClaudeFilesStep installs repo standard rules to ~/.claude and preserves project rules."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            home_dir = Path(tmpdir) / "home"
            home_dir.mkdir()

            source_pilot = Path(tmpdir) / "source" / "pilot"
            source_rules = source_pilot / "rules"
            source_rules.mkdir(parents=True)

            (source_rules / "python-rules.md").write_text("python rules from repo")
            (source_rules / "standard-rule.md").write_text("standard rule")

            dest_dir = Path(tmpdir) / "dest"
            dest_claude = dest_dir / ".claude"
            dest_rules = dest_claude / "rules"
            dest_rules.mkdir(parents=True)
            (dest_rules / "my-project-rules.md").write_text("USER PROJECT RULES - PRESERVED")

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=Path(tmpdir) / "source",
            )

            with patch("installer.steps.claude_files.Path.home", return_value=home_dir):
                step.run(ctx)

            assert (dest_rules / "my-project-rules.md").exists()
            assert (dest_rules / "my-project-rules.md").read_text() == "USER PROJECT RULES - PRESERVED"

            global_rules = home_dir / ".claude" / "rules"
            assert (global_rules / "python-rules.md").exists()
            assert (global_rules / "python-rules.md").read_text() == "python rules from repo"
            assert (global_rules / "standard-rule.md").exists()

    def test_pycache_files_not_copied(self):
        """ClaudeFilesStep skips __pycache__ directories and .pyc files."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            home_dir = Path(tmpdir) / "home"
            home_dir.mkdir()

            source_pilot = Path(tmpdir) / "source" / "pilot"
            source_rules = source_pilot / "rules"
            source_pycache = source_rules / "__pycache__"
            source_pycache.mkdir(parents=True)
            (source_rules / "test-rule.md").write_text("# rule")
            (source_pycache / "something.cpython-312.pyc").write_text("bytecode")

            dest_dir = Path(tmpdir) / "dest"
            dest_dir.mkdir()

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=Path(tmpdir) / "source",
            )

            with patch("installer.steps.claude_files.Path.home", return_value=home_dir):
                step.run(ctx)

            global_rules = home_dir / ".claude" / "rules"
            assert (global_rules / "test-rule.md").exists()
            assert not (global_rules / "__pycache__").exists()


class TestDirectoryClearing:
    """Test directory clearing behavior in local and normal mode."""

    def test_clears_directories_in_normal_local_mode(self):
        """Global rules directory is cleared when source != destination in local mode."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            home_dir = Path(tmpdir) / "home"
            home_dir.mkdir()

            old_global_rules = home_dir / ".claude" / "rules"
            old_global_rules.mkdir(parents=True)
            (old_global_rules / "old-rule.md").write_text("old rule to be removed")

            source_dir = Path(tmpdir) / "source"
            source_pilot = source_dir / "pilot"
            source_rules = source_pilot / "rules"
            source_rules.mkdir(parents=True)
            (source_rules / "new-rule.md").write_text("new rule content")

            dest_dir = Path(tmpdir) / "dest"
            dest_dir.mkdir()

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=source_dir,
            )

            with patch("installer.steps.claude_files.Path.home", return_value=home_dir):
                step.run(ctx)

            global_rules = home_dir / ".claude" / "rules"
            assert (global_rules / "new-rule.md").exists()
            assert (global_rules / "new-rule.md").read_text() == "new rule content"
            assert not (global_rules / "old-rule.md").exists()

    def test_skips_clearing_when_source_equals_destination(self):
        """Directories are NOT cleared when source == destination (same dir)."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            home_dir = Path(tmpdir) / "home"
            home_dir.mkdir()

            pilot_dir = Path(tmpdir) / "pilot"
            rules_dir = pilot_dir / "rules"
            rules_dir.mkdir(parents=True)
            (rules_dir / "existing-rule.md").write_text("existing rule content")

            ctx = InstallContext(
                project_dir=Path(tmpdir),
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=Path(tmpdir),
            )

            with patch("installer.steps.claude_files.Path.home", return_value=home_dir):
                step.run(ctx)

            assert (home_dir / ".claude" / "rules" / "existing-rule.md").exists()

    def test_project_rules_never_cleared(self):
        """Project rules directory is NEVER cleared, only global standard rules."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            home_dir = Path(tmpdir) / "home"
            home_dir.mkdir()

            source_dir = Path(tmpdir) / "source"
            source_pilot = source_dir / "pilot"
            source_rules = source_pilot / "rules"
            source_rules.mkdir(parents=True)
            (source_rules / "new-rule.md").write_text("new standard rule")

            dest_dir = Path(tmpdir) / "dest"
            dest_claude = dest_dir / ".claude"
            dest_project_rules = dest_claude / "rules"
            dest_project_rules.mkdir(parents=True)
            (dest_project_rules / "my-project.md").write_text("USER PROJECT RULE")

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=source_dir,
            )

            with patch("installer.steps.claude_files.Path.home", return_value=home_dir):
                step.run(ctx)

            assert (dest_project_rules / "my-project.md").exists()
            assert (dest_project_rules / "my-project.md").read_text() == "USER PROJECT RULE"

            global_rules = home_dir / ".claude" / "rules"
            assert (global_rules / "new-rule.md").exists()

    def test_standard_commands_are_cleared(self):
        """Global commands directory is cleared and replaced with new commands."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            home_dir = Path(tmpdir) / "home"
            home_dir.mkdir()

            old_global_commands = home_dir / ".claude" / "commands"
            old_global_commands.mkdir(parents=True)
            (old_global_commands / "spec.md").write_text("old spec command")
            (old_global_commands / "plan.md").write_text("old plan command")

            source_dir = Path(tmpdir) / "source"
            source_pilot = source_dir / "pilot"
            source_commands = source_pilot / "commands"
            source_commands.mkdir(parents=True)
            (source_commands / "spec.md").write_text("new spec command")

            dest_dir = Path(tmpdir) / "dest"
            dest_dir.mkdir()

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=source_dir,
            )

            with patch("installer.steps.claude_files.Path.home", return_value=home_dir):
                step.run(ctx)

            global_commands = home_dir / ".claude" / "commands"
            assert (global_commands / "spec.md").exists()
            assert (global_commands / "spec.md").read_text() == "new spec command"

    def test_pilot_plugin_folder_is_installed(self):
        """ClaudeFilesStep installs pilot plugin folder to ~/.claude/pilot/ (global)."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            home_dir = Path(tmpdir) / "home"
            home_dir.mkdir()

            source_dir = Path(tmpdir) / "source"
            source_pilot = source_dir / "pilot"
            source_pilot.mkdir(parents=True)
            (source_pilot / "package.json").write_text('{"name": "pilot"}')
            (source_pilot / "plugin.json").write_text('{"version": "1.0"}')
            (source_pilot / ".mcp.json").write_text('{"servers": []}')
            (source_pilot / ".lsp.json").write_text('{"python": {}}')
            (source_pilot / "scripts").mkdir()
            (source_pilot / "scripts" / "mcp-server.cjs").write_text("// mcp server")
            (source_pilot / "hooks").mkdir()
            (source_pilot / "hooks" / "hook.py").write_text("# hook")

            dest_dir = Path(tmpdir) / "dest"
            dest_dir.mkdir()

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=source_dir,
            )

            with patch("installer.steps.claude_files.Path.home", return_value=home_dir):
                step.run(ctx)

            global_pilot = home_dir / ".claude" / "pilot"
            assert (global_pilot / "package.json").exists()
            assert (global_pilot / "plugin.json").exists()
            assert (global_pilot / ".mcp.json").exists()
            assert (global_pilot / ".lsp.json").exists()
            assert (global_pilot / "scripts" / "mcp-server.cjs").exists()
            assert (global_pilot / "hooks" / "hook.py").exists()

    def test_old_plugin_directory_is_removed(self):
        """ClaudeFilesStep removes old .claude/plugin directory (now renamed to pilot)."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            home_dir = Path(tmpdir) / "home"
            home_dir.mkdir()

            source_dir = Path(tmpdir) / "source"
            source_pilot = source_dir / "pilot"
            source_pilot.mkdir(parents=True)
            (source_pilot / "package.json").write_text('{"name": "pilot"}')

            dest_dir = Path(tmpdir) / "dest"
            dest_claude = dest_dir / ".claude"
            old_plugin = dest_claude / "plugin"
            old_plugin.mkdir(parents=True)
            (old_plugin / "package.json").write_text('{"name": "old-plugin"}')
            (old_plugin / "scripts").mkdir()
            (old_plugin / "scripts" / "worker.cjs").write_text("// old worker")

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=source_dir,
            )

            with patch("installer.steps.claude_files.Path.home", return_value=home_dir):
                step.run(ctx)

            assert not old_plugin.exists()
            assert not (old_plugin / "package.json").exists()
            assert not (old_plugin / "scripts").exists()


class TestUserFoldersPreservation:
    """Tests ensuring user-owned folders are never deleted."""

    def test_skills_folder_is_preserved(self):
        """ClaudeFilesStep NEVER deletes project .claude/skills folder."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            home_dir = Path(tmpdir) / "home"
            home_dir.mkdir()

            source_dir = Path(tmpdir) / "source"
            source_pilot = source_dir / "pilot"
            source_pilot.mkdir(parents=True)
            (source_pilot / "package.json").write_text('{"name": "pilot"}')

            dest_dir = Path(tmpdir) / "dest"
            dest_claude = dest_dir / ".claude"
            dest_skills = dest_claude / "skills"
            dest_skills.mkdir(parents=True)
            (dest_skills / "my-custom-skill.md").write_text("# My Custom Skill")

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=source_dir,
            )

            with patch("installer.steps.claude_files.Path.home", return_value=home_dir):
                step.run(ctx)

            assert dest_skills.exists(), ".claude/skills folder was deleted!"
            assert (dest_skills / "my-custom-skill.md").exists(), "User skill file was deleted!"
            assert (dest_skills / "my-custom-skill.md").read_text() == "# My Custom Skill"

    def test_rules_custom_empty_folder_is_removed(self):
        """ClaudeFilesStep removes empty .claude/rules/custom folder."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            home_dir = Path(tmpdir) / "home"
            home_dir.mkdir()

            source_dir = Path(tmpdir) / "source"
            source_pilot = source_dir / "pilot"
            source_pilot.mkdir(parents=True)
            (source_pilot / "package.json").write_text('{"name": "pilot"}')

            dest_dir = Path(tmpdir) / "dest"
            dest_claude = dest_dir / ".claude"
            old_custom = dest_claude / "rules" / "custom"
            old_custom.mkdir(parents=True)
            (old_custom / ".gitkeep").write_text("")

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=source_dir,
            )

            with patch("installer.steps.claude_files.Path.home", return_value=home_dir):
                step.run(ctx)

            assert not old_custom.exists(), ".claude/rules/custom folder was not removed"

    def test_rules_custom_with_user_files_is_preserved(self):
        """ClaudeFilesStep preserves .claude/rules/custom if it has user files."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            home_dir = Path(tmpdir) / "home"
            home_dir.mkdir()

            source_dir = Path(tmpdir) / "source"
            source_pilot = source_dir / "pilot"
            source_pilot.mkdir(parents=True)
            (source_pilot / "package.json").write_text('{"name": "pilot"}')

            dest_dir = Path(tmpdir) / "dest"
            dest_claude = dest_dir / ".claude"
            old_custom = dest_claude / "rules" / "custom"
            old_custom.mkdir(parents=True)
            (old_custom / "my-rule.md").write_text("# My Rule")

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=source_dir,
            )

            with patch("installer.steps.claude_files.Path.home", return_value=home_dir):
                step.run(ctx)

            assert old_custom.exists(), ".claude/rules/custom was deleted but had user files!"
            assert (old_custom / "my-rule.md").exists()


class TestResolveRepoUrl:
    """Tests for _resolve_repo_url method."""

    def test_resolve_repo_url_returns_correct_url(self):
        """_resolve_repo_url returns the repository URL."""
        from installer.steps.claude_files import ClaudeFilesStep

        step = ClaudeFilesStep()
        result = step._resolve_repo_url("v5.0.0")

        assert result == "https://github.com/zenjabba/claude-pilot-free"
