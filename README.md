<div align="center">

<img src="docs/img/logo.png" alt="Claude Pilot" width="400">

### Claude Pilot — License-Free Fork

All the power of Claude Pilot with no license checks, no trial timers, no tier restrictions.

[![Stars](https://img.shields.io/github/stars/zenjabba/claude-pilot-free?style=flat&color=F59E0B)](https://github.com/zenjabba/claude-pilot-free/stargazers)

<br>

```bash
curl -fsSL https://raw.githubusercontent.com/zenjabba/claude-pilot-free/main/install.sh | bash
```

**Works on macOS, Linux, and Windows (WSL2).**

</div>

---

## What Is This?

This is a fork of [maxritter/claude-pilot](https://github.com/maxritter/claude-pilot) with all licensing and tier-checking code removed. Claude Pilot enhances Claude Code with enforced quality hooks, TDD, persistent memory, spec-driven development, and endless mode — but the original requires a paid license after a 7-day trial.

This fork removes that requirement entirely. Everything runs without license verification.

---

## What Was Changed

The following modifications were made to remove license gating:

### Worker Service (`console/src/services/worker-service.ts`)
- `verifyLicense()` always returns `true` — no more startup blocking
- Removed the `UNLICENSED` error that prevented the worker from starting
- Removed unused `execSync` and `homedir` imports

### License API Routes (`console/src/services/worker/http/routes/LicenseRoutes.ts`)
- `getLicenseInfo()` always returns `{ valid: true, tier: "enterprise" }`
- `activateLicense()` always returns success
- Removed all `spawnSync` calls to the pilot binary

### Installer (`installer/cli.py`)
- `_handle_license_flow()` always returns `None` (continue) — no trial checks, no license key prompts, no expired trial gates

### Installer UI (`installer/ui.py`)
- Removed trial countdown, expired warnings, and promo code display from the install banner

### Install Script (`install.sh`)
- Added `patch_pilot_wrapper()` that rewrites the downloaded `pilot` wrapper script after install to intercept:
  - `pilot verify` — always exits 0
  - `pilot status --json` — returns enterprise tier with no expiration
  - `pilot trial --check/--start` — reports no trial needed
  - `pilot statusline` — strips the `Tier: Trial (Xd)` line from the status bar

### UI (`console/src/ui/viewer/layouts/Topbar/index.tsx`)
- Removed `LicenseBadge`, `ActivationModal`, and `useLicense` imports
- Removed trial/expired prompts, activate button, and promo codes from the top bar

### Built Artifacts
- `pilot/scripts/worker-service.cjs` — rebuilt without license gate
- `pilot/ui/viewer-bundle.js` — rebuilt without license UI

### Tests
- Updated `console/tests/worker/license-routes.test.ts` to match always-valid behavior
- Updated `installer/tests/unit/test_cli.py` to match disabled license flow

---

## Updating an Existing Installation

If you already have Claude Pilot installed and want to remove the license checks:

1. **Re-run the installer from this fork:**
   ```bash
   curl -fsSL https://raw.githubusercontent.com/zenjabba/claude-pilot-free/main/install.sh | bash
   ```

2. **Or manually patch your existing install:**
   ```bash
   # Clone this repo
   git clone https://github.com/zenjabba/claude-pilot-free.git
   cd claude-pilot-free

   # Copy the patched built files
   cp pilot/scripts/worker-service.cjs ~/.claude/pilot/scripts/
   cp pilot/ui/viewer-bundle.js ~/.claude/pilot/ui/

   # Restart the worker
   bun ~/.claude/pilot/scripts/worker-service.cjs restart
   ```

   Then edit `~/.pilot/bin/pilot` to add the license bypass interceptors (see `install.sh` `patch_pilot_wrapper()` for the exact content).

---

## Features (from upstream)

Everything from Claude Pilot works — no features removed, only license checks:

- **Endless Mode** — Seamless continuity across sessions with automatic handoffs
- **Spec-Driven Development** (`/spec`) — Plan, approve, implement with TDD, verify with sub-agents
- **Quality Hooks** — Auto-lint, format, type-check on every file edit (Python, TypeScript, Go)
- **TDD Enforcement** — Mandatory RED/GREEN/REFACTOR cycle
- **Persistent Memory** — Context preserved across sessions via Pilot Console
- **Semantic Search** — Vexor-powered codebase exploration
- **Rules & Skills** — Best practices loaded automatically, fully customizable
- **Team Vault** — Share rules, commands, and skills via Git
- **MCP Servers** — Context7, mem-search, web-search, grep-mcp, web-fetch
- **Language Servers** — basedpyright, vtsls, gopls with auto-restart
- **Worktree Isolation** — Safe experimentation on dedicated branches

---

## Credits

All credit for Claude Pilot goes to [Max Ritter](https://maxritter.net) and the original project at [maxritter/claude-pilot](https://github.com/maxritter/claude-pilot). This fork only removes the licensing requirement.

---

## Prerequisites

**Claude Subscription:** You still need an Anthropic Claude subscription ([Max 5x or 20x](https://claude.com/pricing)) or API key. Pilot enhances Claude Code — it doesn't replace it.
