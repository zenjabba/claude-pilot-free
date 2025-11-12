# Quick Development Mode

**Purpose:** Fast, focused development without spec-driven workflow overhead.

**When to use:** Quick fixes, refactoring, experiments, config changes, documentation - anything that doesn't need /plan → /implement → /verify ceremony.

**Not for:** New features requiring design, complex multi-step implementations (use /plan instead).

## Quick Workflow

1. **Check diagnostics**: `mcp__ide__getDiagnostics()`
2. **Query knowledge** (if relevant): `mcp__cipher__ask_cipher("How did we handle X?")`
3. **Search codebase** (if needed): `mcp__claude-context__search_code(path, query)`
4. **Make changes**: Edit/Write files
5. **Verify**: Run tests if applicable, check diagnostics
6. **Store learnings** (if significant): `mcp__cipher__ask_cipher("Store: Fixed Y using Z pattern")`

## Testing Guidelines (Relaxed)

**TDD NOT enforced** - Use judgment:
- Quick fixes: Test if touching critical paths
- Refactoring: Ensure existing tests still pass
- New features: Consider writing tests (or use /plan → /implement for full TDD)
