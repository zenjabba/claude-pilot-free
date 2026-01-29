<div align="center">

<img src="docs/img/logo.png" alt="Claude Pilot" width="400">

### Pilot Takes Control of Claude Code

Quality on autopilot. Context optimized. Testing enforced.</br>
All systems go. Pilot engaged. Ready for takeoff.

[![Version](https://img.shields.io/github/v/release/maxritter/claude-pilot?label=Version&color=orange)](https://github.com/maxritter/claude-pilot/releases)
[![Stars](https://img.shields.io/github/stars/maxritter/claude-pilot?style=flat&color=yellow)](https://github.com/maxritter/claude-pilot/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/maxritter/claude-pilot?color=blue)](https://github.com/maxritter/claude-pilot/commits/main)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/maxritter/claude-pilot/pulls)

#### ⭐ [Star this repository](https://github.com/maxritter/claude-pilot) · 🌐 [Visit the website](https://claude-pilot.com) · 🔔 [Follow for updates](https://www.linkedin.com/in/rittermax/)

</div>

---

## ⚡ TL;DR

```bash
curl -fsSL https://raw.githubusercontent.com/maxritter/claude-pilot/v5.4.12/install.sh | bash
```

Inside Claude Code, type `/sync` to sync rules and skills. Use `/spec` for Spec-Driven Development or Quick Mode for fast fixes.

---

## 📑 Table of Contents

- [Getting Started](#-getting-started)
- [What's Inside](#-whats-inside)
- [Why Claude Pilot?](#-why-claude-pilot)
- [Usage](#-usage)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Getting Started

### ✅ Prerequisites

Choose your installation method:

**Option A: 🍺 Local Installation**

Install directly on your system using Homebrew. Works on macOS, Linux, and Windows (WSL2).

**Option B: 🐳 Dev Container (Any OS)**

Pre-configured, isolated environment with all tools ready. No system conflicts, consistent across machines.
### 🔧 Installation

Run the following command in your **project folder root**:

```bash
curl -fsSL https://raw.githubusercontent.com/maxritter/claude-pilot/v5.4.12/install.sh | bash
```

You'll be asked to choose between **Dev Container** or **Local Installation**.

---

## 📦 What's Inside

### ♾️ Endless Mode

- **Seamless Continuity** - Work on complex features across multiple sessions without losing progress
- **Automatic Handoffs** - Context Monitor detects limits and continues seamlessly in new sessions
- **Persistent Memory** - Relevant observations automatically carry across all sessions
- **Works Everywhere** - Both `/spec` workflow and Quick Mode benefit from session continuity

### 📋 Spec-Driven Development

- **Planning** - Creates a detailed implementation plan for your review as markdown in `docs/plans/`
- **Approval** - You review, edit if needed, and approve the plan before implementation
- **Implementation** - Executes the plan with TDD enforcement and context management
- **Verification** - Runs tests, quality checks, and validates completion based on the plan

### 📚 Modular Rules, Commands & Skills

- **Rules** - Best practices for TDD, debugging, context management, and more
- **Commands** - `/spec` for SDD, `/sync` for updating rules, `/learn` for online learning
- **Skills** - Coding standards for Python, TypeScript, Go, testing, and components
- **Customizable** - Add your own rules, commands, and skills that survive updates

### 🧠 Enhanced Context Capabilities

- **Persistent Memory** - Cross-session memory system that automatically ingests context
- **Semantic Search** - Local vector store based semantic code search for token-efficient retrieval
- **External Context** - Library docs via Context7, web search and scraping via MCP tools
- **Browser Automation** - E2E UI testing with headless browser for frontend verification

### ✅ Quality Automation

- **TDD Enforcer** - Pre-edit hook that warns when modifying code without failing tests first
- **Quality Hooks** - Language-specific hooks for Python, TypeScript and Go that auto-fix issues
- **LSP Integration** - Language servers installed for real-time diagnostics and go-to-definitions
- **Status Line** - Live display of context usage, memory status, usage limits, and license info

### 🛠️ One-Command Installer

- **Automated Container Setup** - Isolated Linux environment with pre-configured tools and extensions
- **Extended Language Support** - Optionally install extended support for Python, TypeScript & Go
- **Automated Updater** - Updates Pilot to the latest version when launched over the binary
- **Shell Integration** - Auto-configures bash, fish and zsh with `pilot` alias

---

## 🔄 Why Claude Pilot?

Same task. Different results.

| Ad-hoc Prompting                 | With Claude Pilot                                   |
| -------------------------------- | ----------------------------------------------------- |
| ❌ Writes code without tests     | ✅ TDD enforced — tests first, then implementation    |
| ❌ No quality checks             | ✅ Auto-formatted, linted, type-checked on every edit |
| ❌ Inconsistent workflow         | ✅ Structured Plan → Implement → Verify cycle         |
| ❌ Context lost between sessions | ✅ Persistent memory carries observations forward     |
| ❌ No codebase awareness         | ✅ Semantic search understands your code              |
| ❌ Hope it works                 | ✅ Verified before marked complete                    |

**The result:** Production-grade code you can ship with confidence. Systematic. Tested. Verified.

---

## ⚡ Usage

### 🔄 Sync Rules & Skills

Run `/sync` to sync custom rules and skills with your codebase. Run it once initially, then anytime after major changes:

```bash
pilot
> /sync
```

### 📋 Spec-Driven Mode

Best for complex features, refactoring, or when you want to review a plan before implementation:

```bash
pilot
> /spec "Add user authentication with OAuth and JWT tokens"
```

**How it works:**

```
📋 Plan  →  ✅ Approve  →  🔨 Implement  →  🔍 Verify
                                ↑              ↓
                                └── 🔄 Loop ───┘
```

1. **📋 Plan** — Explores codebase, asks clarifying questions, writes spec to `docs/plans/`
2. **✅ Approve** — You review and edit the plan, then approve
3. **🔨 Implement** — Executes each task with TDD and quality hooks
4. **🔍 Verify** — Runs tests and checks; loops back if issues found

### 💬 Quick Mode

Just chat. No plan file, no approval gate. All quality hooks and TDD enforcement still apply.

Best for bug fixes, small improvements, and exploratory work:

```bash
pilot
> Fix the null pointer bug in user.py
```

### 🧠 Online Learning

Capture non-obvious discoveries as reusable skills. Automatically prompted by the context monitor, or invoke manually:

```bash
pilot
> /learn "Extract the debugging workflow we used for the race condition"
```

### 📐 Rules, Commands & Skills

Claude Pilot automatically installs best-practice rules, commands, and coding standard skills when you run the installer.

Create your own in your project's `.claude/` folder:

| Type         | Loaded                            | Best for                                |
| ------------ | --------------------------------- | --------------------------------------- |
| **Rules**    | Every session (always in context) | Guidelines Claude should always follow  |
| **Commands** | On demand via `/command`          | Specific workflows or multi-step tasks  |
| **Skills**   | Dynamically when relevant         | Specialized knowledge for specific tasks |

### 🔌 Custom MCP Servers

Add your own MCP servers in two locations:

| Config File | How It Works | Best For |
|-------------|--------------|----------|
| `.mcp.json` | Instructions load into context when triggered | Lightweight servers (few tools) |
| `mcp_servers.json` | Called via mcp-cli; instructions never enter context | Heavy servers (many tools) |

Run `/sync` after adding servers to generate documentation.

---

## 🤝 Contributing

**Pull Requests** - New features, improvements, and bug fixes are welcome. Fun fact: Pilot is built with Pilot — a self-improving loop where your contributions make the tool that makes contributions better. 🔄

**Issues** - Found a bug or have a feature request? [Open an issue](https://github.com/maxritter/claude-pilot/issues).

---

## 📄 License

> **Try free for 7 days** — No signup, no credit card. Just install and go.

**Why subscribe?** Claude Pilot is actively developed with daily usage in production environments. Your subscription gives you instant access to the latest best practices, workflows, and learnings — a shortcut to state-of-the-art Claude Code development without spending weeks figuring it out yourself.

After your trial, choose the tier that fits your needs [here](https://license.claude-pilot.com):

| Tier | Includes |
|:-----|:---------|
| **Standard** | All features, continuous updates with latest learnings, GitHub support |
| **Enterprise** | Standard + dedicated email support and priority feature requests |

See the [LICENSE](LICENSE) file for full terms.
