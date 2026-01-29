"""Tests for .claude files installation step."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path


class TestPatchClaudePaths:
    """Test the patch_claude_paths function."""

    def test_patch_claude_paths_replaces_bin_source_repo_path(self):
        """patch_claude_paths replaces source repo bin path with global ~/.pilot/bin/."""
        from pathlib import Path as P

        from installer.steps.claude_files import patch_claude_paths

        content = '{"command": "/workspaces/claude-pilot/pilot/bin/pilot statusline"}'
        result = patch_claude_paths(content, Path("/home/user/myproject"))

        expected_bin = str(P.home() / ".pilot" / "bin") + "/"
        assert "/workspaces/claude-pilot/pilot/bin/" not in result
        assert expected_bin in result

    def test_patch_claude_paths_replaces_relative_bin_path(self):
        """patch_claude_paths replaces relative .pilot/bin/ paths with global ~/.pilot/bin/."""
        from pathlib import Path as P

        from installer.steps.claude_files import patch_claude_paths

        content = '{"command": ".pilot/bin/pilot statusline"}'
        result = patch_claude_paths(content, Path("/home/user/myproject"))

        expected_bin = str(P.home() / ".pilot" / "bin") + "/"
        assert '".pilot/bin/' not in result
        assert expected_bin in result

    def test_patch_claude_paths_replaces_plugin_source_repo_path(self):
        """patch_claude_paths replaces source repo plugin path with global ~/.pilot."""
        from pathlib import Path as P

        from installer.steps.claude_files import patch_claude_paths

        content = '{"command": "/workspaces/claude-pilot/pilot/scripts/worker.cjs"}'
        result = patch_claude_paths(content, Path("/home/user/myproject"))

        expected_plugin = str(P.home() / ".pilot")
        assert "/workspaces/claude-pilot/pilot" not in result
        assert expected_plugin in result

    def test_patch_claude_paths_replaces_relative_plugin_path(self):
        """patch_claude_paths replaces relative .pilot paths with global ~/.pilot."""
        from pathlib import Path as P

        from installer.steps.claude_files import patch_claude_paths

        content = '{"command": ".pilot/scripts/worker.cjs"}'
        result = patch_claude_paths(content, Path("/home/user/myproject"))

        expected_plugin = str(P.home() / ".pilot")
        assert '".pilot/' not in result
        assert expected_plugin in result

    def test_patch_claude_paths_handles_bin_and_plugin(self):
        """patch_claude_paths replaces both bin and plugin paths in same content."""
        from pathlib import Path as P

        from installer.steps.claude_files import patch_claude_paths

        content = """{
            "command": "/workspaces/claude-pilot/pilot/scripts/worker.cjs",
            "statusLine": {"command": "/workspaces/claude-pilot/pilot/bin/pilot statusline"}
        }"""
        result = patch_claude_paths(content, Path("/target"))

        expected_plugin = str(P.home() / ".pilot")
        expected_bin = str(P.home() / ".pilot" / "bin") + "/"
        assert expected_plugin in result
        assert expected_bin in result
        assert "/workspaces/claude-pilot" not in result


class TestProcessSettings:
    """Test the process_settings function."""

    def test_process_settings_preserves_python_hook_when_enabled(self):
        """process_settings keeps Python hook when enable_python=True."""
        from installer.steps.claude_files import process_settings

        python_hook = "uv run python /workspaces/claude-pilot/.claude/hooks/file_checker_python.py"
        settings = {
            "hooks": {
                "PostToolUse": [
                    {
                        "matcher": "Write|Edit|MultiEdit",
                        "hooks": [
                            {"type": "command", "command": python_hook},
                        ],
                    }
                ]
            }
        }

        result = process_settings(json.dumps(settings), enable_python=True, enable_typescript=True, enable_golang=True)
        parsed = json.loads(result)

        hooks = parsed["hooks"]["PostToolUse"][0]["hooks"]
        commands = [h["command"] for h in hooks]
        assert any("file_checker_python.py" in cmd for cmd in commands)
        assert len(hooks) == 1

    def test_process_settings_removes_python_hook_when_disabled(self):
        """process_settings removes Python hook when enable_python=False."""
        from installer.steps.claude_files import process_settings

        python_hook = "uv run python /workspaces/claude-pilot/.claude/hooks/file_checker_python.py"
        ts_hook = "uv run python /workspaces/claude-pilot/.claude/hooks/file_checker_ts.py"
        settings = {
            "hooks": {
                "PostToolUse": [
                    {
                        "matcher": "Write|Edit|MultiEdit",
                        "hooks": [
                            {"type": "command", "command": python_hook},
                            {"type": "command", "command": ts_hook},
                        ],
                    }
                ]
            }
        }

        result = process_settings(json.dumps(settings), enable_python=False, enable_typescript=True, enable_golang=True)
        parsed = json.loads(result)

        hooks = parsed["hooks"]["PostToolUse"][0]["hooks"]
        commands = [h["command"] for h in hooks]
        assert not any("file_checker_python.py" in cmd for cmd in commands)
        assert any("file_checker_ts.py" in cmd for cmd in commands)
        assert len(hooks) == 1

    def test_process_settings_handles_missing_hooks(self):
        """process_settings handles settings without hooks gracefully."""
        from installer.steps.claude_files import process_settings

        settings = {"model": "opus", "env": {"key": "value"}}

        result = process_settings(
            json.dumps(settings), enable_python=False, enable_typescript=False, enable_golang=True
        )
        parsed = json.loads(result)

        assert parsed["model"] == "opus"
        assert parsed["env"]["key"] == "value"

    def test_process_settings_preserves_other_settings(self):
        """process_settings preserves all other settings unchanged."""
        from installer.steps.claude_files import process_settings

        python_hook = "uv run python /workspaces/claude-pilot/.claude/hooks/file_checker_python.py"
        settings = {
            "model": "opus",
            "env": {"DISABLE_TELEMETRY": "true"},
            "permissions": {"allow": ["Read", "Write"]},
            "hooks": {
                "PostToolUse": [
                    {
                        "matcher": "Write|Edit|MultiEdit",
                        "hooks": [{"type": "command", "command": python_hook}],
                    }
                ]
            },
        }

        result = process_settings(json.dumps(settings), enable_python=False, enable_typescript=True, enable_golang=True)
        parsed = json.loads(result)

        assert parsed["model"] == "opus"
        assert parsed["env"]["DISABLE_TELEMETRY"] == "true"
        assert parsed["permissions"]["allow"] == ["Read", "Write"]

    def test_process_settings_handles_malformed_structure(self):
        """process_settings handles malformed settings gracefully without crashing."""
        from installer.steps.claude_files import process_settings

        malformed_cases = [
            {"hooks": {"PostToolUse": None}},
            {"hooks": {"PostToolUse": "not a list"}},
            {"hooks": {"PostToolUse": [{"hooks": None}]}},
            {"hooks": {"PostToolUse": [None, "string"]}},
            {"hooks": None},
            {"no_hooks": "at all"},
        ]

        for settings in malformed_cases:
            result = process_settings(
                json.dumps(settings), enable_python=False, enable_typescript=False, enable_golang=True
            )
            parsed = json.loads(result)
            assert parsed is not None

    def test_process_settings_removes_typescript_hook_when_disabled(self):
        """process_settings removes TypeScript hook when enable_typescript=False."""
        from installer.steps.claude_files import process_settings

        ts_hook = "uv run python /workspaces/claude-pilot/.claude/hooks/file_checker_ts.py"
        go_hook = "uv run python /workspaces/claude-pilot/.claude/hooks/file_checker_go.py"
        settings = {
            "hooks": {
                "PostToolUse": [
                    {
                        "matcher": "Write|Edit|MultiEdit",
                        "hooks": [
                            {"type": "command", "command": go_hook},
                            {"type": "command", "command": ts_hook},
                        ],
                    }
                ]
            }
        }

        result = process_settings(json.dumps(settings), enable_python=True, enable_typescript=False, enable_golang=True)
        parsed = json.loads(result)

        hooks = parsed["hooks"]["PostToolUse"][0]["hooks"]
        commands = [h["command"] for h in hooks]
        assert not any("file_checker_ts.py" in cmd for cmd in commands)
        assert any("file_checker_go.py" in cmd for cmd in commands)
        assert len(hooks) == 1

    def test_process_settings_removes_both_hooks_when_both_disabled(self):
        """process_settings removes both Python and TypeScript hooks when both disabled."""
        from installer.steps.claude_files import process_settings

        python_hook = "uv run python /workspaces/claude-pilot/.claude/hooks/file_checker_python.py"
        ts_hook = "uv run python /workspaces/claude-pilot/.claude/hooks/file_checker_ts.py"
        go_hook = "uv run python /workspaces/claude-pilot/.claude/hooks/file_checker_go.py"
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

        result = process_settings(
            json.dumps(settings), enable_python=False, enable_typescript=False, enable_golang=True
        )
        parsed = json.loads(result)

        hooks = parsed["hooks"]["PostToolUse"][0]["hooks"]
        commands = [h["command"] for h in hooks]
        assert not any("file_checker_python.py" in cmd for cmd in commands)
        assert not any("file_checker_ts.py" in cmd for cmd in commands)
        assert any("file_checker_go.py" in cmd for cmd in commands)
        assert len(hooks) == 1

    def test_process_settings_removes_golang_hook_when_disabled(self):
        """process_settings removes Go hook when enable_golang=False."""
        from installer.steps.claude_files import process_settings

        go_hook = "uv run python /workspaces/claude-pilot/.claude/hooks/file_checker_go.py"
        python_hook = "uv run python /workspaces/claude-pilot/.claude/hooks/file_checker_python.py"
        settings = {
            "hooks": {
                "PostToolUse": [
                    {
                        "matcher": "Write|Edit|MultiEdit",
                        "hooks": [
                            {"type": "command", "command": python_hook},
                            {"type": "command", "command": go_hook},
                        ],
                    }
                ]
            }
        }

        result = process_settings(json.dumps(settings), enable_python=True, enable_typescript=True, enable_golang=False)
        parsed = json.loads(result)

        hooks = parsed["hooks"]["PostToolUse"][0]["hooks"]
        commands = [h["command"] for h in hooks]
        assert not any("file_checker_go.py" in cmd for cmd in commands)
        assert any("file_checker_python.py" in cmd for cmd in commands)
        assert len(hooks) == 1

    def test_process_settings_preserves_golang_hook_when_enabled(self):
        """process_settings keeps Go hook when enable_golang=True."""
        from installer.steps.claude_files import process_settings

        go_hook = "uv run python /workspaces/claude-pilot/.claude/hooks/file_checker_go.py"
        python_hook = "uv run python /workspaces/claude-pilot/.claude/hooks/file_checker_python.py"
        settings = {
            "hooks": {
                "PostToolUse": [
                    {
                        "matcher": "Write|Edit|MultiEdit",
                        "hooks": [
                            {"type": "command", "command": python_hook},
                            {"type": "command", "command": go_hook},
                        ],
                    }
                ]
            }
        }

        result = process_settings(json.dumps(settings), enable_python=True, enable_typescript=True, enable_golang=True)
        parsed = json.loads(result)

        hooks = parsed["hooks"]["PostToolUse"][0]["hooks"]
        commands = [h["command"] for h in hooks]
        assert any("file_checker_go.py" in cmd for cmd in commands)
        assert len(hooks) == 2


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
        """ClaudeFilesStep.run installs .claude files."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            source_claude = Path(tmpdir) / "source" / ".claude"
            source_claude.mkdir(parents=True)
            (source_claude / "test.md").write_text("test content")
            (source_claude / "rules").mkdir()
            (source_claude / "rules" / "standard").mkdir()
            (source_claude / "rules" / "standard" / "rule.md").write_text("rule content")

            dest_dir = Path(tmpdir) / "dest"
            dest_dir.mkdir()

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=Path(tmpdir) / "source",
            )

            (dest_dir / ".claude").mkdir()

            step.run(ctx)

            assert (dest_dir / ".claude" / "test.md").exists()

    def test_claude_files_installs_settings_local(self):
        """ClaudeFilesStep installs settings.local.json."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            source_claude = Path(tmpdir) / "source" / ".claude"
            source_claude.mkdir(parents=True)
            (source_claude / "settings.local.json").write_text('{"hooks": {}}')

            dest_dir = Path(tmpdir) / "dest"
            dest_dir.mkdir()
            (dest_dir / ".claude").mkdir()

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=Path(tmpdir) / "source",
            )

            step.run(ctx)

            assert (dest_dir / ".claude" / "settings.local.json").exists()

    def test_claude_files_skips_python_when_disabled(self):
        """ClaudeFilesStep skips Python rules when enable_python=False."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            source_claude = Path(tmpdir) / "source" / ".claude"
            source_rules = source_claude / "rules" / "standard"
            source_rules.mkdir(parents=True)
            (source_rules / "python-rules.md").write_text("# python rules")
            (source_rules / "other-rules.md").write_text("# other rules")

            dest_dir = Path(tmpdir) / "dest"
            dest_dir.mkdir()
            (dest_dir / ".claude").mkdir()

            ctx = InstallContext(
                project_dir=dest_dir,
                enable_python=False,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=Path(tmpdir) / "source",
            )

            step.run(ctx)

            assert not (dest_dir / ".claude" / "rules" / "standard" / "python-rules.md").exists()
            assert (dest_dir / ".claude" / "rules" / "standard" / "other-rules.md").exists()

    def test_claude_files_skips_typescript_when_disabled(self):
        """ClaudeFilesStep skips TypeScript rules when enable_typescript=False."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            source_claude = Path(tmpdir) / "source" / ".claude"
            source_rules = source_claude / "rules" / "standard"
            source_rules.mkdir(parents=True)
            (source_rules / "typescript-rules.md").write_text("# typescript rules")
            (source_rules / "python-rules.md").write_text("# python rules")

            dest_dir = Path(tmpdir) / "dest"
            dest_dir.mkdir()
            (dest_dir / ".claude").mkdir()

            ctx = InstallContext(
                project_dir=dest_dir,
                enable_typescript=False,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=Path(tmpdir) / "source",
            )

            step.run(ctx)

            assert not (dest_dir / ".claude" / "rules" / "standard" / "typescript-rules.md").exists()
            assert (dest_dir / ".claude" / "rules" / "standard" / "python-rules.md").exists()

    def test_claude_files_skips_golang_when_disabled(self):
        """ClaudeFilesStep skips Go rules when enable_golang=False."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            source_claude = Path(tmpdir) / "source" / ".claude"
            source_rules = source_claude / "rules" / "standard"
            source_rules.mkdir(parents=True)
            (source_rules / "golang-rules.md").write_text("# golang rules")
            (source_rules / "python-rules.md").write_text("# python rules")

            dest_dir = Path(tmpdir) / "dest"
            dest_dir.mkdir()
            (dest_dir / ".claude").mkdir()

            ctx = InstallContext(
                project_dir=dest_dir,
                enable_golang=False,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=Path(tmpdir) / "source",
            )

            step.run(ctx)

            assert not (dest_dir / ".claude" / "rules" / "standard" / "golang-rules.md").exists()
            assert (dest_dir / ".claude" / "rules" / "standard" / "python-rules.md").exists()


class TestClaudeFilesCustomRulesPreservation:
    """Test that custom rules from repo are installed and user files preserved."""

    def test_custom_rules_installed_and_user_files_preserved(self):
        """ClaudeFilesStep installs repo standard rules and preserves user custom files."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            source_claude = Path(tmpdir) / "source" / ".claude"
            source_rules_standard = source_claude / "rules" / "standard"
            source_rules_standard.mkdir(parents=True)

            (source_rules_standard / "python-rules.md").write_text("python rules from repo")
            (source_rules_standard / "standard-rule.md").write_text("standard rule")

            dest_dir = Path(tmpdir) / "dest"
            dest_claude = dest_dir / ".claude"
            dest_rules_custom = dest_claude / "rules" / "custom"
            dest_rules_custom.mkdir(parents=True)
            (dest_rules_custom / "my-project-rules.md").write_text("USER PROJECT RULES - PRESERVED")

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=Path(tmpdir) / "source",
            )

            step.run(ctx)

            assert (dest_rules_custom / "my-project-rules.md").exists()
            assert (dest_rules_custom / "my-project-rules.md").read_text() == "USER PROJECT RULES - PRESERVED"

            assert (dest_claude / "rules" / "standard" / "python-rules.md").exists()
            assert (dest_claude / "rules" / "standard" / "python-rules.md").read_text() == "python rules from repo"

            assert (dest_claude / "rules" / "standard" / "standard-rule.md").exists()

    def test_pycache_files_not_copied(self):
        """ClaudeFilesStep skips __pycache__ directories and .pyc files."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            source_claude = Path(tmpdir) / "source" / ".claude"
            source_rules = source_claude / "rules" / "standard"
            source_pycache = source_rules / "__pycache__"
            source_pycache.mkdir(parents=True)
            (source_rules / "test-rule.md").write_text("# rule")
            (source_pycache / "something.cpython-312.pyc").write_text("bytecode")

            dest_dir = Path(tmpdir) / "dest"
            (dest_dir / ".claude").mkdir(parents=True)

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=Path(tmpdir) / "source",
            )

            step.run(ctx)

            assert (dest_dir / ".claude" / "rules" / "standard" / "test-rule.md").exists()

            assert not (dest_dir / ".claude" / "rules" / "standard" / "__pycache__").exists()


class TestDirectoryClearing:
    """Test directory clearing behavior in local and normal mode."""

    def test_clears_directories_in_normal_local_mode(self):
        """Standard rules directory is cleared when source != destination in local mode."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            source_dir = Path(tmpdir) / "source"
            source_claude = source_dir / ".claude"
            source_rules = source_claude / "rules" / "standard"
            source_rules.mkdir(parents=True)
            (source_rules / "new-rule.md").write_text("new rule content")

            dest_dir = Path(tmpdir) / "dest"
            dest_claude = dest_dir / ".claude"
            dest_rules = dest_claude / "rules" / "standard"
            dest_rules.mkdir(parents=True)
            (dest_rules / "old-rule.md").write_text("old rule to be removed")

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=source_dir,
            )

            step.run(ctx)

            assert (dest_rules / "new-rule.md").exists()
            assert (dest_rules / "new-rule.md").read_text() == "new rule content"
            assert not (dest_rules / "old-rule.md").exists()

    def test_skips_clearing_when_source_equals_destination(self):
        """Directories are NOT cleared when source == destination (same dir)."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            claude_dir = Path(tmpdir) / ".claude"
            rules_dir = claude_dir / "rules" / "standard"
            rules_dir.mkdir(parents=True)
            (rules_dir / "existing-rule.md").write_text("existing rule content")

            ctx = InstallContext(
                project_dir=Path(tmpdir),
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=Path(tmpdir),
            )

            step.run(ctx)

            assert (rules_dir / "existing-rule.md").exists()
            assert (rules_dir / "existing-rule.md").read_text() == "existing rule content"

    def test_custom_rules_never_cleared(self):
        """Custom rules directory is NEVER cleared, only standard rules."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            source_dir = Path(tmpdir) / "source"
            source_claude = source_dir / ".claude"
            source_standard = source_claude / "rules" / "standard"
            source_standard.mkdir(parents=True)
            (source_standard / "new-rule.md").write_text("new standard rule")

            dest_dir = Path(tmpdir) / "dest"
            dest_claude = dest_dir / ".claude"
            dest_custom = dest_claude / "rules" / "custom"
            dest_standard = dest_claude / "rules" / "standard"
            dest_custom.mkdir(parents=True)
            dest_standard.mkdir(parents=True)
            (dest_custom / "my-project.md").write_text("USER CUSTOM RULE")
            (dest_standard / "old-rule.md").write_text("old standard rule")

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=source_dir,
            )

            step.run(ctx)

            assert (dest_custom / "my-project.md").exists()
            assert (dest_custom / "my-project.md").read_text() == "USER CUSTOM RULE"

            assert not (dest_standard / "old-rule.md").exists()
            assert (dest_standard / "new-rule.md").exists()

    def test_standard_commands_are_cleared(self):
        """Standard commands (spec, sync, plan, implement, verify) are cleared and replaced."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            source_dir = Path(tmpdir) / "source"
            source_claude = source_dir / ".claude"
            source_commands = source_claude / "commands"
            source_commands.mkdir(parents=True)
            (source_commands / "spec.md").write_text("new spec command")

            dest_dir = Path(tmpdir) / "dest"
            dest_claude = dest_dir / ".claude"
            dest_commands = dest_claude / "commands"
            dest_commands.mkdir(parents=True)
            (dest_commands / "spec.md").write_text("old spec command")
            (dest_commands / "plan.md").write_text("old plan command")

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=source_dir,
            )

            step.run(ctx)

            assert (dest_commands / "spec.md").exists()
            assert (dest_commands / "spec.md").read_text() == "new spec command"

    def test_custom_commands_never_cleared(self):
        """Custom commands (non-standard names) are NEVER cleared."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            source_dir = Path(tmpdir) / "source"
            source_claude = source_dir / ".claude"
            source_commands = source_claude / "commands"
            source_commands.mkdir(parents=True)
            (source_commands / "spec.md").write_text("new spec command")

            dest_dir = Path(tmpdir) / "dest"
            dest_claude = dest_dir / ".claude"
            dest_commands = dest_claude / "commands"
            dest_commands.mkdir(parents=True)
            (dest_commands / "my-custom-workflow.md").write_text("USER CUSTOM COMMAND")
            (dest_commands / "spec.md").write_text("old spec command")

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=source_dir,
            )

            step.run(ctx)

            assert (dest_commands / "my-custom-workflow.md").exists()
            assert (dest_commands / "my-custom-workflow.md").read_text() == "USER CUSTOM COMMAND"

            assert (dest_commands / "spec.md").exists()
            assert (dest_commands / "spec.md").read_text() == "new spec command"

    def test_pilot_folder_is_installed(self):
        """ClaudeFilesStep installs pilot folder from repo."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            source_dir = Path(tmpdir) / "source"
            source_claude = source_dir / ".claude"
            source_pilot = source_claude / "pilot"
            source_pilot.mkdir(parents=True)
            (source_pilot / "package.json").write_text('{"name": "test"}')
            (source_pilot / "scripts").mkdir()
            (source_pilot / "scripts" / "mcp-server.cjs").write_text("// mcp server")
            (source_pilot / "hooks").mkdir()
            (source_pilot / "hooks" / "hook.py").write_text("# hook")

            dest_dir = Path(tmpdir) / "dest"
            dest_claude = dest_dir / ".claude"
            dest_claude.mkdir(parents=True)

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=source_dir,
            )

            step.run(ctx)

            assert (dest_claude / "pilot" / "package.json").exists()
            assert (dest_claude / "pilot" / "scripts" / "mcp-server.cjs").exists()
            assert (dest_claude / "pilot" / "hooks" / "hook.py").exists()

    def test_hooks_are_not_installed_from_repo(self):
        """ClaudeFilesStep does NOT install hooks from repo (hooks come from plugin)."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            source_dir = Path(tmpdir) / "source"
            source_claude = source_dir / ".claude"
            source_hooks = source_claude / "hooks"
            source_hooks.mkdir(parents=True)
            (source_hooks / "my_hook.py").write_text("# hook code")
            (source_hooks / "another_hook.sh").write_text("# shell hook")

            source_commands = source_claude / "commands"
            source_commands.mkdir(parents=True)
            (source_commands / "test.md").write_text("test command")

            source_rules = source_claude / "rules" / "standard"
            source_rules.mkdir(parents=True)
            (source_rules / "test-rule.md").write_text("test rule")

            dest_dir = Path(tmpdir) / "dest"
            dest_claude = dest_dir / ".claude"
            dest_claude.mkdir(parents=True)

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=source_dir,
            )

            step.run(ctx)

            assert not (dest_claude / "hooks" / "my_hook.py").exists()
            assert not (dest_claude / "hooks" / "another_hook.sh").exists()

            assert (dest_claude / "commands" / "test.md").exists()
            assert (dest_claude / "rules" / "standard" / "test-rule.md").exists()

    def test_skills_are_not_installed_from_repo(self):
        """ClaudeFilesStep does NOT install skills from repo (skills come from plugin)."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            source_dir = Path(tmpdir) / "source"
            source_claude = source_dir / ".claude"
            source_skills = source_claude / "skills" / "standards-testing"
            source_skills.mkdir(parents=True)
            (source_skills / "SKILL.md").write_text("# skill content")

            source_commands = source_claude / "commands"
            source_commands.mkdir(parents=True)
            (source_commands / "test.md").write_text("test command")

            dest_dir = Path(tmpdir) / "dest"
            dest_claude = dest_dir / ".claude"
            dest_claude.mkdir(parents=True)

            ctx = InstallContext(
                project_dir=dest_dir,
                ui=Console(non_interactive=True),
                local_mode=True,
                local_repo_dir=source_dir,
            )

            step.run(ctx)

            assert not (dest_claude / "skills" / "standards-testing" / "SKILL.md").exists()

            assert (dest_claude / "commands" / "test.md").exists()

    def test_old_plugin_directory_is_removed(self):
        """ClaudeFilesStep removes old .claude/plugin directory (now renamed to pilot)."""
        from installer.context import InstallContext
        from installer.steps.claude_files import ClaudeFilesStep
        from installer.ui import Console

        step = ClaudeFilesStep()
        with tempfile.TemporaryDirectory() as tmpdir:
            source_dir = Path(tmpdir) / "source"
            source_claude = source_dir / ".claude"
            source_pilot = source_claude / "pilot"
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

            step.run(ctx)

            assert not old_plugin.exists()
            assert not (old_plugin / "package.json").exists()
            assert not (old_plugin / "scripts").exists()
