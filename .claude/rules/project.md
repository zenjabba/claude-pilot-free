# Project: Claude Pilot

**Last Updated:** 2026-01-27

## Overview

A professional development environment for Claude Code (CC). Provides Endless Mode for unlimited context, spec-driven development workflow, TDD enforcement, semantic search, persistent memory, quality hooks, online learning system, and a modular rules system.

## Technology Stack

- **Language:** Python 3.12+
- **Package Manager:** uv
- **Testing:** pytest, pytest-cov, pytest-asyncio
- **Linting:** ruff
- **Type Checking:** basedpyright
- **Website:** TypeScript, React, Vite, Tailwind CSS

## Directory Structure

```
claude-pilot/
├── launcher/               # Pilot binary source package
│   ├── cli.py         # Pilot CLI (typer-based)
│   ├── wrapper.py     # Claude session wrapper + Endless Mode
│   ├── auth.py        # License verification
│   ├── banner.py      # Welcome banner display
│   ├── build.py       # Cython build for binary
│   ├── statusline/    # Status bar providers and widgets
│   └── tests/         # Pilot-specific tests
├── installer/         # Step-based installer package
│   ├── cli.py         # Typer CLI with subcommands
│   ├── context.py     # InstallContext dataclass
│   ├── ui.py          # Rich UI abstraction
│   └── steps/         # 10 installation step modules
├── docs/              # Documentation and website
│   ├── plans/         # Spec-driven development plans
│   └── site/          # React/Vite marketing site
└── .claude/           # Claude Code configuration
    ├── commands/      # Slash commands (/spec, /sync)
    ├── skills/        # Skill directories (plan/, implement/, verify/, standards-*/)
    ├── hooks/         # Quality and context hooks
    ├── bin/           # Compiled Pilot binary (.so)
    └── rules/         # Modular rules system (standard/, custom/)
```

## Key Files

- **Pilot Entry:** `launcher/__main__.py` or `.claude/bin/pilot`
- **Installer Entry:** `installer/__main__.py` or `python -m installer`
- **Commands:** `.claude/commands/spec.md`, `.claude/commands/sync.md`, `.claude/commands/learn.md`
- **Compiled Binary:** `.claude/bin/pilot.cpython-312-*.so`

## Development Commands

| Task | Command |
|------|---------|
| Install deps | `uv sync` |
| Run tests | `uv run pytest -q` |
| Pilot tests | `uv run pytest launcher/tests -q` |
| Installer tests | `uv run pytest installer/tests -q` |
| Coverage | `uv run pytest --cov=launcher --cov=installer` |
| Format | `ruff format .` |
| Lint | `ruff check . --fix` |
| Type check | `basedpyright launcher installer` |
| Build Pilot | `uv run python -m launcher.build` |
| Run installer | `python -m installer install --local` |

## Architecture Notes

- **Pilot Binary:** Cython-compiled wrapper with license verification and Endless Mode
- **Installer:** Step-based architecture (10 steps) with Rich UI
- **Steps:** Each step is idempotent with check(), run(), and rollback() methods
- **Workflow:** Spec-Driven (`/spec`) orchestrates plan → implement → verify
- **Endless Mode:** Automatic session handoffs at 90% context via send-clear
- **Online Learning:** `/learn` extracts reusable knowledge into skills after significant tasks
