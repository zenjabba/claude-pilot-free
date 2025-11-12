"""
Rule Builder - Assembles slash commands and skills from markdown rules.

Reads rules from .claude/rules/ and generates:
- Slash commands in .claude/commands/
- Skills in .claude/skills/*/SKILL.md
"""

import logging
import sys
from pathlib import Path
from typing import Any

import yaml

logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stderr)


class RuleBuilder:
    """Builds commands and skills from markdown rules."""

    def __init__(self, claude_dir: Path):
        self.claude_dir = claude_dir
        self.rules_dir = claude_dir / "rules"
        self.commands_dir = claude_dir / "commands"
        self.skills_dir = claude_dir / "skills"
        self.rules: dict[str, str] = {}
        self.available_skills: list[dict[str, str]] = []
        self.logger = logging.getLogger(__name__)

    def load_rules(self) -> None:
        """Load all markdown rules from core/, workflow/, and extended/ directories."""
        self.logger.info("Loading rules...")

        for category in ["core", "workflow", "extended"]:
            category_dir = self.rules_dir / category
            if not category_dir.exists():
                continue

            for md_file in category_dir.glob("*.md"):
                rule_id = md_file.stem
                with open(md_file, encoding="utf-8") as f:
                    self.rules[rule_id] = f.read()
                    self.logger.info(f"  ✓ Loaded {category}/{md_file.name}")

        self.logger.info(f"  Total rules loaded: {len(self.rules)}")

    def discover_skills(self) -> None:
        """Discover available skills from extended/ directory."""
        self.logger.info("Discovering skills...")

        extended_dir = self.rules_dir / "extended"
        if not extended_dir.exists():
            return

        for md_file in sorted(extended_dir.glob("*.md")):
            skill_name = md_file.stem
            description = ""
            with open(md_file, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        description = line
                        break

            self.available_skills.append({"name": skill_name, "description": description or "No description"})
            self.logger.info(f"  ✓ Discovered @{skill_name}")

        self.logger.info(f"  Total skills discovered: {len(self.available_skills)}")

    def format_skills_section(self) -> str:
        """Format available skills as markdown section."""
        if not self.available_skills:
            return ""

        lines = ["## Available Skills", ""]

        categories: dict[str, list[str]] = {
            "Testing": [],
            "Global": [],
            "Backend": [],
            "Frontend": [],
        }

        for skill in self.available_skills:
            name = skill["name"]
            if name.startswith("testing-"):
                categories["Testing"].append(f"@{name}")
            elif name.startswith("global-"):
                categories["Global"].append(f"@{name}")
            elif name.startswith("backend-"):
                categories["Backend"].append(f"@{name}")
            elif name.startswith("frontend-"):
                categories["Frontend"].append(f"@{name}")

        for category, skills in categories.items():
            if skills:
                lines.append(f"**{category}:** {' | '.join(skills)}")

        lines.append("")
        return "\n".join(lines)

    def load_config(self) -> dict[str, Any]:
        """Load rule configuration."""
        config_file = self.rules_dir / "config.yaml"
        with open(config_file, encoding="utf-8") as f:
            return yaml.safe_load(f)

    def build_commands(self, config: dict[str, Any]) -> list[str]:
        """Build all command files from configuration."""
        self.logger.info("\nBuilding commands...")
        updated_files = []

        self.commands_dir.mkdir(parents=True, exist_ok=True)

        for command_name, command_config in config.get("commands", {}).items():
            description = command_config.get("description", "")
            model = command_config.get("model", "sonnet")
            inject_skills = command_config.get("inject_skills", False)

            rules_content = []
            for rule_id in command_config.get("rules", []):
                if rule_id in self.rules:
                    rules_content.append(self.rules[rule_id])
                else:
                    self.logger.warning(f"  ⚠️  Rule '{rule_id}' not found")

            output_parts = [
                "---",
                f"description: {description}",
                f"model: {model}",
                "---",
            ]

            for rule_content in rules_content:
                output_parts.append(rule_content)
                output_parts.append("")

            if inject_skills and self.available_skills:
                output_parts.append(self.format_skills_section())

            output = "\n".join(output_parts)

            command_file = self.commands_dir / f"{command_name}.md"
            with open(command_file, "w", encoding="utf-8") as f:
                f.write(output)

            updated_files.append(str(command_file))
            if inject_skills:
                self.logger.info(f"  ✓ Generated {command_file.name} (with skills)")
            else:
                self.logger.info(f"  ✓ Generated {command_file.name}")

        return updated_files

    def build_skills(self) -> list[str]:
        """Build all skill files from extended rules."""
        self.logger.info("\nBuilding skills...")
        updated_files: list[str] = []

        self.skills_dir.mkdir(parents=True, exist_ok=True)

        extended_dir = self.rules_dir / "extended"
        if not extended_dir.exists():
            return updated_files

        for md_file in extended_dir.glob("*.md"):
            rule_id = md_file.stem
            if rule_id not in self.rules:
                continue

            output = self.rules[rule_id]

            skill_dir = self.skills_dir / rule_id
            skill_dir.mkdir(parents=True, exist_ok=True)

            skill_file = skill_dir / "SKILL.md"
            with open(skill_file, "w", encoding="utf-8") as f:
                f.write(output)

            updated_files.append(str(skill_file))
            self.logger.info(f"  ✓ Generated {rule_id}/SKILL.md")

        return updated_files

    def build_all(self) -> None:
        """Build all commands and skills."""
        self.load_rules()
        self.discover_skills()
        config = self.load_config()

        command_files = self.build_commands(config)
        skill_files = self.build_skills()

        self.logger.info("\n✅ Claude CodePro Build Complete!")
        self.logger.info(f"   Commands: {len(command_files)} files")
        self.logger.info(f"   Skills: {len(skill_files)} files")
        self.logger.info(f"   Available skills: {len(self.available_skills)}")


def main():
    """Main entry point."""
    logger = logging.getLogger(__name__)
    script_dir = Path(__file__).parent
    claude_dir = script_dir.parent

    if claude_dir.name != ".claude":
        logger.error("Error: Script must be in .claude/rules/")
        sys.exit(1)

    builder = RuleBuilder(claude_dir)
    builder.build_all()


if __name__ == "__main__":
    main()
