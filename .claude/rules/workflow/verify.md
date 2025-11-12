## Verification and Quality Assurance Process

**Process:** CodeRabbit → Tests → Run program → Coverage → Quality checks → E2E → Final verification

Active verification that immediately fixes issues as discovered, ensuring all tests pass and system works end-to-end.

### Step 1: Start CodeRabbit & Gather Context

**Start CodeRabbit analysis in background**

**While it runs:**
1. Check diagnostics: `mcp__ide__getDiagnostics()` - Fix any errors immediately
2. Read plan (if exists): `Glob("docs/plans/*.md")` then `Read(latest_plan)`
3. Check changes: `git status --short` and `git diff --stat`
4. Query Cipher: `mcp__cipher__ask_cipher("What was implemented? Any known issues?")`

### Step 2: Run & Fix Unit Tests

Run unit tests and fix any failures immediately.

**If failures:** Identify → Read test → Fix implementation → Re-run → Continue until all pass

### Step 3: Run & Fix Integration Tests

Run integration tests and fix any failures immediately.

**Common issues:** Database connections, mock configuration, missing test data

### Step 4: Execute the Actual Program (MANDATORY)

**⚠️ CRITICAL: Tests passing ≠ Program works**

Run the actual program and verify real output.

**If serious bugs (NOT simple fixes):**
1. Store findings in Cipher
2. Update plan with bug fixes
3. Tell user: "Found [N] bugs. Run `/clear` → `/implement [plan]`"
4. STOP

**If simple fixes:** Fix directly, re-run, continue

### Step 5: Check Coverage

Verify test coverage meets requirements.

**If insufficient:** Identify uncovered lines → Write tests for critical paths → Verify improvement

### Step 6: Review & Fix CodeRabbit Findings

Process CodeRabbit results and fix issues systematically.

**Quality gate:** No critical/high issues before proceeding

### Step 7: Run Quality Checks

Run automated quality tools and fix any issues found.

### Step 8: E2E Verification (if applicable)

Run end-to-end tests as appropriate for the application type.

### Step 9: Final Verification

**Run everything one more time:**
- All tests
- Program execution
- Diagnostics
- CodeRabbit

**Success criteria:**
- All tests passing
- No diagnostics errors
- No critical/high CodeRabbit issues
- Program executes successfully with correct output
- Coverage ≥ 80%

**Fix immediately | Test after each fix | No "should work" - verify it works | Keep fixing until green**
