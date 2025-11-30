---
description: Run tests and fix issues end-to-end with Claude CodePro
model: opus
---
# VERIFY MODE: Verification and Quality Assurance Process with Code Review

## The Process

Tests → Program execution → Call chain analysis → Coverage → Quality checks → Code review → E2E → Final verification

Active verification with comprehensive code review that immediately fixes issues as discovered, ensuring all tests pass, code quality is high, and system works end-to-end.

### Step 1: Run & Fix Unit Tests

Run unit tests and fix any failures immediately.

**If failures:** Identify → Read test → Fix implementation → Re-run → Continue until all pass

### Step 2: Run & Fix Integration Tests

Run integration tests and fix any failures immediately.

**Common issues:** Database connections, mock configuration, missing test data

### Step 3: Execute the Actual Program (MANDATORY)

**⚠️ CRITICAL: Tests passing ≠ Program works**

Run the actual program and verify real output.

**If serious bugs (NOT simple fixes):**
1. Store findings in Cipher
2. Update plan with bug fixes
3. Tell user: "Found [N] bugs. Run `/clear` → `/implement [plan]`"
4. STOP

**If simple fixes:** Fix directly, re-run, continue

### Step 4: Call Chain Analysis

**Perform deep impact analysis for all changes:**

1. **Trace Upwards (Callers):**
   - Identify all code that calls modified functions
   - Verify they handle new return values/exceptions
   - Check for breaking changes in interfaces

2. **Trace Downwards (Callees):**
   - Identify all dependencies of modified code
   - Verify correct parameter passing
   - Check error handling from callees

3. **Side Effect Analysis:**
   - Database state changes
   - Cache invalidation needs
   - External system impacts
   - Global state modifications

### Step 5: Check Coverage

Verify test coverage meets requirements.

**If insufficient:** Identify uncovered lines → Write tests for critical paths → Verify improvement

### Step 6: Run Quality Checks

Run automated quality tools and fix any issues found.

### Step 7: Code Review Simulation

**Perform self-review using code review checklist:**

- [ ] **Logic Correctness:** Edge cases handled, algorithms correct
- [ ] **Architecture & Design:** SOLID principles, no unnecessary coupling
- [ ] **Performance:** No N+1 queries, efficient algorithms, no memory leaks
- [ ] **Security:** No SQL injection, XSS, proper auth/authz
- [ ] **Readability:** Clear naming, complex logic documented
- [ ] **Error Handling:** Graceful error handling, adequate logging
- [ ] **Convention Compliance:** Follows project standards

**If issues found:** Document and fix immediately

### Step 8: E2E Verification (if applicable)

Run end-to-end tests as appropriate for the application type.

#### For APIs: Newman/Postman Collection Testing

**When applicable:** REST APIs, GraphQL APIs, authentication systems, microservices

**Check for Postman collections:**
- Look in `postman/collections/`, `tests/postman/`, or similar directories
- Common files: `api-tests.json`, `*.postman_collection.json`

**If collections exist, run Newman:**
```bash
newman run postman/collections/api-tests.json \
  -e postman/environments/dev.json \
  --reporters cli,json
```

**Verify:**
- All requests succeed with expected status codes
- Response times are acceptable
- Authentication flows work correctly
- CRUD operations complete successfully
- Error scenarios return proper error codes
- Chained requests (using saved variables) work

**If failures:** Analyze failure → Check API endpoint → Fix implementation → Re-run → Continue until all pass

**If no collections exist but API endpoints were added:**
- Consider creating basic Postman collection for new endpoints
- At minimum: test health check, main CRUD operations
- Document endpoint testing approach in PR/commit

### Step 9: Final Verification

**Run everything one more time:**
- All tests
- Program execution
- Diagnostics
- Call chain validation

**Success criteria:**
- All tests passing
- No diagnostics errors
- Program executes successfully with correct output
- Coverage ≥ 80%
- All Definition of Done criteria met
- Code review checklist complete
- No breaking changes in call chains

### Step 10: Update Plan Status

**When all verification passes:**

1. **MANDATORY: Update plan status to VERIFIED**
   ```
   Edit the plan file and change the Status line:
   Status: REVIEWED  →  Status: VERIFIED
   ```
2. Inform user: "✅ Verification complete. Plan status updated to VERIFIED."

**Fix immediately | Test after each fix | No "should work" - verify it works | Keep fixing until green**
