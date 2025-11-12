## Task Execution and Batch Processing

**Execute ALL tasks continuously. NO stopping unless context manager says context is full.**

### Session Context Awareness

**ALWAYS read plan first**, then:
- Check git: `git status --short` and `git diff --name-only`
- If changes exist: Continuation - read files, query Cipher, search codebase
- Check plan file for `[x]` completed tasks - SKIP these, resume from first `[ ]` task
- If no changes: Fresh start from Task 1

### Per-Task Execution Flow

**For EVERY task, follow this exact sequence:**

1. **READ PLAN'S IMPLEMENTATION STEPS** - List all files to create/modify/delete
2. **Mark task as in_progress** in TodoWrite
3. **Check diagnostics** - `mcp__ide__getDiagnostics()`
4. **Execute Standard Task Flow** - TDD mandatory
5. **Verify tests pass** - `uv run pytest tests/path/to/test.py -v`
6. **Run actual program** - Show real output
7. **Check diagnostics again** - Must be zero errors
8. **Mark task completed** in TodoWrite
9. **Update plan file** - Change `[ ]` to `[x]`
10. **Check context usage** - See context-management.yaml

### Critical Task Rules

**⚠️ NEVER SKIP TASKS:**
- EVERY task MUST be fully implemented
- NO exceptions for "MVP scope" or complexity
- If blocked: STOP and report specific blockers
- NEVER mark complete without doing the work

### Verification Checklist

Before marking complete:
- [ ] Test written and FAILED (RED phase)
- [ ] Implementation written
- [ ] Test PASSES (GREEN phase)
- [ ] Program executed with verified output
- [ ] No diagnostics errors

### When All Tasks Complete

1. Quick verification: `mcp__ide__getDiagnostics()` and `uv run pytest`
2. Store learnings in Cipher
3. Inform user: "✅ All tasks complete. Run `/verify`"
4. DO NOT run /verify yourself
