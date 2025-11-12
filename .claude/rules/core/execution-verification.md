## Execution Verification

**Standards:** Tests passing ≠ Program working | Always execute | Verify output

### Core Principle

**Tests passing ≠ Program working**

You MUST run the actual program and verify real output. Tests might mock incorrectly, miss runtime issues, or pass while the program fails.

### When to Execute

Execute in EVERY situation where:
- After refactoring code
- After tests pass
- When about to mark task complete
- After dependency changes
- When working with entry points
- After infrastructure changes
- When imports were modified

**If there's a runnable program, RUN IT. No exceptions.**

### What to Execute

**ETL Pipelines:** Run the actual ETL, verify logs, check database records, verify exports

**API Services:** Start server, test endpoints, verify responses, check database side effects

**CLI Tools:** Run commands, verify exit codes, check stdout/stderr, verify file changes

**Batch Jobs/Scripts:** Run script, verify files created, check database changes, verify logs

### Verification Checklist

After running, verify:
- No import errors
- No runtime errors
- Expected output in logs
- Side effects correct (database/files/APIs updated)
- Configuration loads correctly
- Dependencies available
- Performance acceptable

### What "Verification" Means

**BAD:**
- "The tests pass so it should work"
- "I'm confident the imports are correct"
- "It will probably work in production"

**GOOD:**
- "I ran the program and saw: [actual logs]"
- "Database now contains 150 records"
- "API returned 200 with payload: [show response]"

### Integration with TDD Flow

1. Write failing test (RED)
2. Write minimal code (GREEN)
3. Run tests - PASS ✓
4. **⚠️ RUN ACTUAL PROGRAM** ← Critical step
5. Verify real output
6. Refactor if needed
7. Mark task complete

**Never skip step 4.** Tests use mocks and fixtures. Real program uses real imports, config, and dependencies.

### Common Failures This Prevents

**Import Errors:** Tests mock imports, but real code has missing/wrong imports
**Configuration Issues:** Tests use mock settings, real program reads env vars that are missing
**Missing Dependencies:** Tests mock libraries, real program needs actual package installed
**Build Issues:** Tests use source directly, built package has missing files

### When Execution is Not Applicable

**ONLY skip execution if:**
- Pure refactoring of internal functions (no entry points)
- Documentation changes only
- Test-only changes
- Infrastructure-as-code (where "synth" is the execution)
- Configuration files

**If in doubt, execute.**

### Error Handling

When execution fails after tests pass:
1. Don't ignore it - this is a real bug
2. Fix the issue immediately
3. Run tests again
4. Execute again to verify
5. Update tests to catch this failure

### Final Rule

**Before marking ANY task complete:**

Ask yourself: "Did I run the actual program and verify output?"

**If no:** Stop. Run it. Verify. Then complete.
**If yes:** Show the output. Then complete.

Tests are necessary but not sufficient. Execution is mandatory.
