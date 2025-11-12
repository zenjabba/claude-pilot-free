## Coding Standards and Best Practices

**Standards:** DRY/YAGNI | Clean imports | Check diagnostics before/after

### DRY (Don't Repeat Yourself)

Extract duplicated logic into reusable functions or classes.

Identify common patterns and abstract them. If you're copying code, extract it into a shared function instead.

### YAGNI (You Aren't Gonna Need It)

Don't add features, abstractions, or complexity until they're actually needed.

Build the simplest thing that works. Add abstractions when you have concrete evidence they're needed, not because they might be useful someday.

### Small, Focused Functions

Keep functions small and focused on a single responsibility.

Each function should do one thing well. If a function has "and" in its description, it probably does too much.

### Meaningful Names

Use clear, descriptive names that reveal intent.

**Good names:** `calculate_discount`, `validate_email`, `fetch_active_users`
**Bad names:** `process`, `handle`, `data`, `temp`, `x`

Avoid abbreviations except for widely understood ones. Use domain terminology.

### Clean Imports

Organize imports logically and remove unused ones.

**Order:** Standard library → Third-party → Local application

Remove unused imports immediately. They add noise and confusion.

### Remove Dead Code

Delete unused code, commented-out blocks, and unused imports.

Don't leave commented code "just in case". Use version control to recover old code if needed.

### Check Diagnostics

Run diagnostics before and after changes to catch issues early.

Use `mcp__ide__getDiagnostics()` at start and end of every task. Fix errors immediately.

### Consistent Formatting

Use automated formatters to maintain consistent code style.

Configure your formatter once, then let it handle indentation, line breaks, and spacing.

### Backward Compatibility

Only add backward compatibility logic when explicitly required.

Don't assume you need to support old versions unless specifically instructed.

### Best Practices

**DO:**
- Extract duplicate code into functions
- Build the simplest solution first
- Use descriptive names
- Keep functions small and focused
- Remove dead code immediately
- Run diagnostics before and after
- Use automated formatting

**DON'T:**
- Copy-paste code
- Over-engineer solutions
- Use vague names like "process" or "handle"
- Leave functions doing multiple things
- Keep commented-out code
- Skip diagnostic checks
- Manually format code
