---
description: Active verification and fix command - runs all tests, immediately fixes any issues found, ensures everything works end-to-end
model: sonnet
---

# Active Verification & Fix

**Purpose:** Hands-on verification that immediately fixes issues as they're discovered, ensuring all tests pass and the system works end-to-end.

**Workflow Position:** Step 3 of 3 in spec-driven development
- **Previous command (/plan):** Idea → Design → Implementation Plan
- **Previous command (/implement):** Implementation Plan → Working Code
- **This command (/verify):** Working Code → Fixed & Verified Implementation

**Process:** Run CodeRabbit analysis → Run tests → Fix failures immediately → Re-test → Run program → Fix CodeRabbit findings → Repeat until all green

## Tools for Verification

**Primary tools for verification and fixing:**
- **CodeRabbit CLI**: `coderabbit --prompt-only` - AI-powered code review (CENTRAL TOOL)
  - Identifies race conditions, memory leaks, security issues, best practice violations
  - Use `--type uncommitted` for uncommitted changes only
  - Use `--type committed` for committed changes only
  - Use `--base <branch>` to specify base branch (e.g., `--base develop`)
  - Run in background to keep workflow responsive
  - **Rate Limits (Free Tier)**: 3 back-to-back reviews, then 2/hour (summary only), 200 files/hour, 100 files/PR
  - **If rate limited**: Wait ~8 minutes or proceed with other verification steps (tests, build, diagnostics)
- **IDE Diagnostics**: `mcp__ide__getDiagnostics()` - Check errors/warnings
- **Cipher**: `mcp__cipher__ask_cipher(...)` - Query issues, store fixes
- **Claude Context**: `mcp__claude-context__search_code(...)` - Find similar code
- **Database**: `mcp__dbhub-postgres__execute_sql(...)` - Verify data
- **Firecrawl**: `mcp__firecrawl-mcp__firecrawl_search(...)` - Research solutions
- **Ref/Context7**: `mcp__Ref__ref_search_documentation(...)` - Check docs

## Process

### Step 1: Start CodeRabbit Analysis & Gather Context

**Launch automated code review while gathering context:**

```bash
# Start CodeRabbit analysis in background (critical first step)
coderabbit --prompt-only --type uncommitted &
CR_PID=$!
```

**While CodeRabbit runs, gather context and fix obvious problems:**
1. Check diagnostics: `mcp__ide__getDiagnostics()`
   - **If errors/warnings found:** Fix them immediately before proceeding
2. Read plan (if exists): `Glob("docs/plans/*.md")` then `Read(latest_plan)`
   - Extract requirements, success criteria, architecture decisions
   - If no plan found, continue without (standalone verification)
3. Check changes: `git status --short` and `git diff --stat` - Understand scope
4. Query Cipher: `mcp__cipher__ask_cipher("What was implemented? Any known issues?")`

**Check if CodeRabbit is complete:**
```bash
# Check if background job finished
jobs -l | grep $CR_PID
# If still running, continue with tests; check back after Step 2-3
```

### Step 2: Run & Fix Unit Tests

**Start with the fastest tests and fix failures immediately:**

```bash
# Run unit tests first
uv run pytest -m unit -v --tb=short
```

**If failures occur:**
1. Identify the failing test and error message
2. Read the test file to understand expected behavior
3. Fix the implementation code (not the test unless it's wrong)
4. Re-run the specific failing test: `uv run pytest path/to/test.py::test_function -v`
5. Once fixed, re-run all unit tests to ensure no regression
6. Continue until all unit tests pass

### Step 3: Run & Fix Integration Tests

**Test component interactions and fix issues:**

```bash
# Run integration tests
uv run pytest -m integration -v --tb=short
```

**If failures occur:**
1. Analyze the failure - often related to:
   - Database connection issues
   - External service mocks not properly configured
   - Missing test data setup
2. Fix the issue in the code or test setup
3. Re-run the failing test specifically
4. Continue until all integration tests pass

### Step 4: Execute & Fix the Actual Program (MANDATORY)

**⚠️ CRITICAL: Tests passing ≠ Program works. MUST run actual program and verify output.**

```bash
# ETL Pipeline - Run and verify logs + database
uv run python src/main.py
# MUST verify: 1) Logs show extraction/loading 2) Check DB records created 3) No errors in output

# API Server - Start and test endpoints
uv run python src/app.py &
curl -X GET localhost:8000/health && curl -X POST localhost:8000/api/endpoint -d '{}'
# MUST verify: 1) Server starts 2) Endpoints respond 3) Check response data

# CLI Tool - Run actual commands
uv run python src/cli.py command --flag
# MUST verify: Output matches expected behavior

# Background Job - Run and check processing
uv run python src/worker.py
# MUST verify: Tasks process correctly, check logs/queue
```

**Verification checklist:**
- [ ] Program executes without errors
- [ ] Logs show expected behavior (extraction, loading, processing)
- [ ] Output data is correct (check DB, files, API responses)
- [ ] No warnings or unexpected errors in logs

**If program reveals serious bugs (NOT simple fixes):**

**When to go back to implementation:**
- Multiple data validation errors
- Schema/table structure issues
- Business logic failures
- Complex bugs requiring TDD approach

**Process:**
1. Store current findings: `mcp__cipher__ask_cipher("Found [N] bugs: [list]. Returning to implementation.")`
2. Update plan: Add new task with bug details and fix steps
3. Check context (see Context Management section): If ≥80%, run `/remember` first
4. Tell user: "Found [N] bugs requiring implementation phase. Added Task X to plan. Run `/clear` → `/implement [plan]` to fix."
5. STOP - do not attempt complex fixes in verify mode

**If simple configuration/import fixes:**
1. Fix directly
2. Re-run program
3. Continue verification

### Step 5: Run & Fix Coverage Issues

**Check test coverage and add missing tests:**

```bash
# Run with coverage report
uv run pytest --cov=. --cov-report=term-missing --cov-fail-under=80
```

**If coverage < 80% or critical code uncovered:**
1. Identify uncovered lines from the report
2. Write tests for uncovered critical paths:
   - Create test file if it doesn't exist
   - Write test FIRST (TDD approach)
   - Verify test fails appropriately
   - Run again to confirm coverage improvement
3. Skip coverage for truly untestable code (e.g., if __name__ == "__main__")

### Step 6: Review & Fix CodeRabbit Findings

**Process CodeRabbit analysis results (CRITICAL QUALITY GATE):**

```bash
# Check if CodeRabbit analysis is complete
wait $CR_PID || coderabbit --prompt-only --type uncommitted
```

**CodeRabbit output provides AI-optimized findings with:**
- File locations and line numbers
- Issue severity (critical/high/medium/low)
- Suggested approaches for fixes
- Best practice violations

**Create systematic fix plan:**
1. Review all findings and create TodoWrite list for each issue
2. Prioritize: Critical → High → Medium → Low
3. For each finding:
   - Read the affected file(s)
   - Understand the issue context
   - Apply the fix (use `mcp__claude-context__search_code` to find similar patterns)
   - Verify fix doesn't break tests: `uv run pytest path/to/affected_test.py`
4. Store fixes in Cipher: `mcp__cipher__ask_cipher("Fixed CodeRabbit finding: [issue] in [file]. Solution: [description]")`

**Common CodeRabbit findings:**
- Race conditions → Add proper locking/synchronization
- Memory leaks → Fix resource cleanup, close connections
- Security vulnerabilities → Sanitize inputs, use secure functions
- Error handling gaps → Add try-catch, validate inputs
- Performance issues → Optimize algorithms, add caching
- Best practice violations → Follow framework conventions

**Re-run CodeRabbit after fixes to verify:**
```bash
coderabbit --prompt-only --type uncommitted
# Continue fixing until no critical/high issues remain
```

**If rate limit is hit:**
- Message: "Rate limit exceeded, please try after X minutes"
- **Option 1**: Wait the specified time (usually 8 minutes) then re-run
- **Option 2**: Proceed to Step 7-9 (code quality, tests, build) and verify those pass
- **Option 3**: If all other checks pass and you fixed all reported issues, consider verification complete
- **Note**: Free tier allows 3 back-to-back reviews, then 2/hour. Plan accordingly for large codebases.

### Step 7: Fix Code Quality Issues

**Run additional quality checks and fix all issues:**

```bash
# Linting - auto-fix what's possible
uv run ruff check . --fix
# If issues remain, manually fix them

# Format all files
uv run ruff format .
# No manual action needed - it auto-formats

# Type checking
uv run mypy src --strict
# If errors: Add type hints, fix type mismatches

# Security scan (if available)
uv run bandit -r src 2>/dev/null || echo "Bandit not installed"
# If issues: Fix security vulnerabilities immediately
```

**Common fixes:**
- Import errors → Reorder/remove unused imports
- Type errors → Add type hints or fix incorrect types
- Line too long → Break into multiple lines
- Undefined names → Import missing modules
- Security issues → Use secure functions/patterns

### Step 8: E2E Verification (if applicable)

**For API projects - test with real requests:**
```bash
# If Postman collection exists
if [ -d "postman/collections" ]; then
  newman run postman/collections/*.json -e postman/environments/dev.json
  # Fix any failing requests
fi

# Or test key endpoints manually
curl -X GET localhost:8000/api/health
curl -X POST localhost:8000/api/[endpoint] -H "Content-Type: application/json" -d '{}'
```

**For data pipelines - verify data flow:**
```sql
-- Check if data was loaded correctly
SELECT COUNT(*) FROM target_table WHERE created_at > NOW() - INTERVAL '1 hour';
-- If no data, debug the pipeline
```

### Step 9: Final Verification & Context Management

**Check context usage FIRST** (see Context Management section below for calculation)
- If ≥ 80%: `/remember` → STOP → Tell user to `/clear` and `/verify` again
- If < 80%: Continue with final verification

**Run everything one more time:**
```bash
uv run pytest -q  # Quick pass/fail
uv run python src/main.py  # Actual program execution
mcp__ide__getDiagnostics()  # Must be zero
coderabbit --prompt-only --type uncommitted  # Final check
```

**If anything fails:** Go back to specific step and fix

**Success criteria:**
- All tests passing
- No IDE diagnostics
- No critical/high CodeRabbit findings
- **Program executes successfully with correct output**
- Coverage ≥ 80%

## Context Management & Storage

**After EACH major step (tests, CodeRabbit, quality):** Check context
```
MESSAGE tokens from <system_warning>: X/200000
Add 35k overhead: TOTAL = X + 35000
Calculate: (TOTAL / 200000) * 100

If ≥ 80% (160k total): `/remember` → STOP → Tell user to `/clear` and `/verify` again
If < 80%: Continue to next step
```

**Store in Cipher after fixing:**
```
mcp__cipher__ask_cipher("Fixed [issue] in [file]. Solution: [description]")
```

**Store after completion:**
```
mcp__cipher__ask_cipher("Verification complete for [feature].
Tests: X passing, Coverage: Y%, Program execution: [verified/failed].
CodeRabbit: [findings resolved].
Key fixes: [list]")
```

**Preserved after /clear:** ✅ Code fixes, Cipher learnings, Plan updates | ❌ Conversation

## Key Principles

**Fix immediately** | **Test after each fix** | **No "should work" - verify it works** | **Keep fixing until green**

**Success = Everything works. No exceptions.**

## CodeRabbit Integration Workflow

**Recommended iterative cycle for feature implementation:**

1. Implement feature as requested
2. Run `coderabbit --prompt-only` in background
3. Continue with tests while CodeRabbit analyzes
4. Check CodeRabbit completion: "Is CodeRabbit finished running?"
5. Create TodoWrite list for each finding systematically
6. Fix issues iteratively until critical/high issues resolve
7. Re-run CodeRabbit to verify fixes
8. Repeat until quality gate passes

**Optimization tips:**
- Work on smaller feature branches to reduce analysis time
- Use `--type uncommitted` for work-in-progress changes
- Use `--type committed` for pre-merge final review
- Specify `--base <branch>` when working on feature branches
- Run in background to keep Claude responsive during analysis
- CodeRabbit catches complex issues (race conditions, memory leaks) that standard linters miss
