"""
Shell Configuration Functions - Aliases and shell environment setup

Manages shell RC files and aliases across bash, zsh, and fish
"""

from __future__ import annotations

import re
from pathlib import Path

from . import ui


def add_shell_alias(
    shell_file: Path,
    alias_cmd: str,
    shell_name: str,
    alias_name: str,
) -> None:
    """Add or update alias in a shell configuration file."""
    if not shell_file.exists():
        return

    content = shell_file.read_text()
    marker = "# Claude CodePro alias"
    alias_pattern = re.compile(rf"^alias {alias_name}=", re.MULTILINE)

    old_marker_pattern = re.compile(r"# Claude CodePro alias - .*\n")
    content = old_marker_pattern.sub("", content)

    if marker in content:
        lines = content.split("\n")
        new_lines = []
        skip_next_alias = False

        for line in lines:
            if line == marker:
                skip_next_alias = True
                new_lines.append(marker)
                new_lines.append(alias_cmd)
            elif skip_next_alias and alias_pattern.match(line):
                skip_next_alias = False
                continue
            else:
                new_lines.append(line)

        shell_file.write_text("\n".join(new_lines))
        ui.print_success(f"Updated alias '{alias_name}' in {shell_name}")

    elif alias_pattern.search(content):
        lines = content.split("\n")
        new_lines = []

        for line in lines:
            if alias_pattern.match(line):
                new_lines.append(marker)
                new_lines.append(alias_cmd)
            else:
                new_lines.append(line)

        shell_file.write_text("\n".join(new_lines))
        ui.print_success(f"Updated existing alias '{alias_name}' in {shell_name}")

    else:
        with open(shell_file, "a") as f:
            f.write(f"\n{marker}\n{alias_cmd}\n")
        ui.print_success(f"Added alias '{alias_name}' to {shell_name}")


def add_cc_alias() -> None:
    """
    Add 'ccp' alias to all detected shells.

    Creates an alias that:
    1. If current dir is CCP project → use it
    2. If in devcontainer (/workspaces exists) → find CCP project there
    3. Otherwise → show error
    """
    alias_name = "ccp"
    ui.print_status(f"Configuring shell for NVM and '{alias_name}' alias...")
    home = Path.home()

    bash_alias = (
        f"alias {alias_name}='"
        "if [ -f .claude/rules/build.py ]; then "
        "nvm use 22 && python3 .claude/rules/build.py &>/dev/null && clear && dotenvx run claude; "
        "elif [ -d /workspaces ]; then "
        'ccp_dir=""; for d in /workspaces/*/; do [ -f "$d.claude/rules/build.py" ] && ccp_dir="$d" && break; done; '
        'if [ -n "$ccp_dir" ]; then cd "$ccp_dir" && nvm use 22 && python3 .claude/rules/build.py &>/dev/null && clear && dotenvx run claude; '
        'else echo "Error: No CCP project found in /workspaces"; fi; '
        "else "
        'echo "Error: Not a Claude CodePro project. Please cd to a CCP-enabled project first."; '
        "fi'"
    )

    add_shell_alias(home / ".bashrc", bash_alias, ".bashrc", alias_name)
    add_shell_alias(home / ".zshrc", bash_alias, ".zshrc", alias_name)

    fish_config = home / ".config" / "fish" / "config.fish"
    fish_alias = (
        f"alias {alias_name}='"
        "if test -f .claude/rules/build.py; "
        "nvm use 22; and python3 .claude/rules/build.py &>/dev/null; and clear; and dotenvx run claude; "
        "else if test -d /workspaces; "
        'set ccp_dir ""; for d in /workspaces/*/; test -f "$d.claude/rules/build.py"; and set ccp_dir "$d"; and break; end; '
        'if test -n "$ccp_dir"; cd "$ccp_dir"; and nvm use 22; and python3 .claude/rules/build.py &>/dev/null; and clear; and dotenvx run claude; '
        'else; echo "Error: No CCP project found in /workspaces"; end; '
        "else; "
        'echo "Error: Not a Claude CodePro project. Please cd to a CCP-enabled project first."; '
        "end'"
    )

    add_shell_alias(fish_config, fish_alias, "config.fish", alias_name)

    print("")
    ui.print_success(f"Alias '{alias_name}' configured!")
    print(f"   Run '{alias_name}' from any CCP project or devcontainer")
