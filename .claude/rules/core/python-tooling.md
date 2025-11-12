## Python Tooling Standards

**Python:** `uv` not pip | One-line docstrings | No inline comments | Edit > Create

### Package Management - uv Only

**ALWAYS use `uv` for Python package operations. NEVER use `pip` directly.**

```bash
uv pip install package-name
uv pip install -r requirements.txt
uv pip list
uv pip show package-name
```

**Why uv:** Faster resolution, better dependency management, project standard, consistent across environments

### Testing with pytest

```bash
uv run pytest                              # All tests
uv run pytest -m unit                      # Unit tests only
uv run pytest -m integration               # Integration tests only
uv run pytest tests/unit/test_module.py   # Specific file
uv run pytest --cov=src --cov-report=term-missing  # With coverage
```

### Code Quality Tools

**Ruff (Linting & Formatting):**
```bash
uv run ruff check . --fix      # Auto-fix issues
uv run ruff format .           # Format all code
```

**Mypy (Type Checking):**
```bash
uv run mypy src --strict       # Strict type checking
```

### Docstring Style

**Use one-line docstrings for functions and methods.**

Keep them concise - just describe what the function does, not how.

Multi-line docstrings acceptable for complex functions, but prefer one-liners.

### Comments

**Write self-documenting code. Avoid inline comments.**

Use clear variable and function names instead of comments.

Use comments only for:
- Complex algorithms requiring explanation
- Non-obvious business logic
- Workarounds for external library bugs

### File Operations

**Prefer editing existing files over creating new ones.**

Before creating a new file, ask:
- Can this fit in an existing module?
- Is there a related file to extend?
- Does this need to be separate?

Benefits: Reduces bloat, maintains coherent structure, easier navigation.

### Import Organization

**Order:** Standard library → Third-party → Local imports

Separate each group with a blank line.

Tools like `ruff` automatically organize imports.
