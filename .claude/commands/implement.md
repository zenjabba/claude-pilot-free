---
description: Use when partner provides a complete implementation plan to execute - loads plan, reviews critically, executes tasks in batches, reports for review between batches
model: sonnet
---

# Implementing Specification Plans

## Overview

Load plan, review critically, execute tasks in batches, report for review between batches.

**Core principle:** Batch execution with checkpoints for architect review.

**Workflow Position:** Step 2 of 3 in spec-driven development
- **Previous command (/plan):** Idea → Design → Implementation Plan
- **This command (/implement):** Implementation Plan → Working Code
- **Next command (/verify):** Working Code → Verified Implementation

**Input location:** `docs/plans/YYYY-MM-DD-<feature-name>.md`
**Output:** Working, tested code

## Session Context Awareness

**Session states:** Fresh start | After `/remember`+`/clear` | Ongoing session

**ALWAYS read plan first**, then:
- Check git status/diff for progress
- Query Cipher for stored learnings
- Search codebase with Claude Context
- Determine completed tasks from evidence
- Continue from next pending task

**After `/remember`+`/clear` preserved:** ✅ Plan, Code, Tests, Cipher, Codebase | ❌ Conversation

## MCP Tools for Implementation

### Always Available (Direct Access)

1. **IDE Diagnostics** (FIRST & LAST)
   ```
   mcp__ide__getDiagnostics() # Check errors/warnings before and after
   mcp__ide__executeCode(code="...") # Run Python in Jupyter kernel (notebooks only)
   ```

2. **Cipher** - Query patterns, store discoveries
   ```
   mcp__cipher__ask_cipher("How did we implement X? What patterns worked?")
   mcp__cipher__ask_cipher("Store: Fixed issue Y using pattern Z")
   ```

3. **Claude Context** - Search codebase semantically
   ```
   mcp__claude-context__search_code(path="/workspaces/...", query="similar patterns")
   mcp__claude-context__index_codebase(path="/workspaces/...") # If search fails
   ```

4. **Database** - Check schema, run queries
   ```
   mcp__dbhub-postgres__execute_sql("SELECT * FROM table WHERE...")
   ```

5. **Ref/Context7** - Documentation research
   ```
   mcp__Ref__ref_search_documentation(query="pytest fixtures")
   mcp__Ref__ref_read_url(url="https://...")
   mcp__context7__resolve-library-id(libraryName="library")
   mcp__context7__get-library-docs(context7CompatibleLibraryID="/org/lib")
   ```

6. **Firecrawl** - Web scraping/search
   ```
   mcp__firecrawl-mcp__firecrawl_search(query="...", sources=[{"type": "web"}])
   mcp__firecrawl-mcp__firecrawl_scrape(url="https://...", formats=["markdown"])
   ```

### Tool Discovery (When Needed)

7. **MCP Funnel** - Discover and bridge additional tools
   ```
   mcp__mcp-funnel__discover_tools_by_words(words="tool keywords", enable=true)
   mcp__mcp-funnel__get_tool_schema(tool="discovered_tool_name")
   mcp__mcp-funnel__bridge_tool_request(tool="tool_name", arguments={...})
   ```

## Standard Task Flow (EVERY Task)

1. **Diagnostics**: `mcp__ide__getDiagnostics()`
2. **Knowledge**: Query Cipher for patterns - `mcp__cipher__ask_cipher("...")`
3. **Search**: Claude Context for similar code - `mcp__claude-context__search_code(...)`
4. **Research**: Ref/Context7 if needed - `mcp__Ref__ref_search_documentation(...)`
5. **Test**: Write failing test FIRST (MANDATORY)
6. **Implement**: Minimal code to pass
7. **Verify**: Diagnostics + run tests
8. **Execute**: Run actual code and verify output (MANDATORY)
9. **E2E** (APIs): Newman/Postman tests
10. **Store**: Save discoveries in Cipher - `mcp__cipher__ask_cipher("Store: ...")`

**CRITICAL - Execute Actual Code:** After tests pass, run the actual program/function to verify it works:
- ETL: `uv run python src/main.py` → Check logs/DB records
- API: `curl localhost:8000/endpoint` → Check response
- CLI: `uv run python src/cli.py --flag` → Check output
- Show actual output, don't claim "should work"

## API E2E Testing (Newman)

**For APIs:** Create Postman collection in `postman/collections/` with tests:
```json
{"info": {"name": "API Tests"},
 "item": [{
   "request": {"method": "POST", "url": "{{base_url}}/api/endpoint"},
   "event": [{"listen": "test", "script": {
     "exec": ["pm.test('Status 200', () => pm.response.to.have.status(200));"]
   }}]
 }]}
```
Run: `newman run postman/collections/feature.json -e postman/environments/dev.json`

## TDD Enforcement (NON-NEGOTIABLE)

**NO PRODUCTION CODE WITHOUT FAILING TEST FIRST**

**RED-GREEN-REFACTOR:** Write test → Verify fail → Minimal code → Verify pass → Refactor → Repeat

**Code before test = DELETE and restart with test**

## The Process

### Step 1: Load Plan and Assess Context

**FIRST:** Read plan file (from argument or ask for path)

**Determine session state:**
- Check git: `git status --short` and `git diff --name-only`
- If changes exist: Continuation - read files, query Cipher, search codebase
- Check plan file for `[x]` completed tasks - SKIP these, resume from first `[ ]` task
- If no changes: Fresh start from Task 1

**Prepare:**
1. Count total tasks
2. Review critically, raise concerns
3. Create TodoWrite (mark completed if continuation)
4. Run `mcp__ide__getDiagnostics()` for clean state
5. Search codebase for relevant patterns using `mcp__claude-context__search_code(...)`

### Step 2: Execute Tasks Autonomously

**Execute ALL tasks continuously. NO stopping unless context > 75%.**

**⚠️ CRITICAL - NEVER SKIP TASKS:**
- **EVERY task in the plan MUST be fully implemented**
- **NO exceptions** - not for "MVP scope", "complexity", "environment constraints", or ANY other reason
- **If a task cannot be completed:** STOP and inform the user with specific blockers
- **NEVER mark a task complete without doing the actual work**
- **Skipping tasks violates the entire spec-driven workflow and is unprofessional**

**Per task (CRITICAL - follow exactly):**
1. Mark task as `in_progress` in TodoWrite
2. Run `mcp__ide__getDiagnostics()` to check for pre-existing errors
3. Execute Standard Task Flow (see above)
4. Write failing test FIRST (TDD mandatory - NO exceptions)
5. Implement minimal code to pass test
6. Run `mcp__ide__getDiagnostics()` again to verify no errors
7. **RUN ACTUAL PROGRAM** (if applicable - MANDATORY):
   - ETL: `uv run python src/main.py` → Verify logs show extraction/loading, check DB records
   - API: `curl localhost:8000/endpoint` → Verify response data is correct
   - CLI: `uv run python src/cli.py` → Verify output matches expected behavior
   - **Show actual output - never claim "should work"**
   - Skip only if task has no runnable code (e.g., model-only changes)
8. Mark task as `completed` in TodoWrite ONLY if tests pass AND program runs successfully
9. **UPDATE PLAN FILE:** Change `[ ]` to `[x]` for this task ONLY after completing ALL work
10. Check context usage (see below)

**⚠️ BEFORE MARKING COMPLETE - VERIFY:**
- [ ] Test written and initially FAILED (RED phase)
- [ ] Implementation code written
- [ ] Test now PASSES (GREEN phase)
- [ ] Program executed and output verified (if applicable)
- [ ] No diagnostics errors
- [ ] Task fully complete - no shortcuts taken

**Context Check After EVERY Task (CRITICAL):**
```
IMPORTANT: System warnings only show MESSAGE tokens, NOT total context!
Total context = MESSAGE tokens + OVERHEAD (~35-40k for system + tools + memory)

To check ACTUAL context usage:
1. Look for LATEST <system_warning> containing "Token usage: X/200000"
2. Add 35k overhead: TOTAL = X + 35000
3. Calculate percentage: (TOTAL / 200000) * 100
4. Alternative: Ask user to run /context command for exact total

If ≥ 80% (160k total tokens):
  - Run `/remember` immediately to store learnings
  - STOP execution - NO new features above 80%
  - Tell user: "Context at 80% (Xk/200k). Running /remember to preserve learnings. Please run /clear then /implement <plan> to continue."
If < 80%: Continue to next task without asking
```

**Flow:** Task → Check → Continue (if <80%) | Remember+Stop (if ≥80%)

**Why 80% limit:** Above 80%, overhead and new tool calls can quickly consume remaining space, causing context overflow mid-task.

**Standards:** TDD | `uv` not pip | One-line docstrings | No inline comments | Imports at top | DRY/YAGNI | Check diagnostics | Edit > Create

**Active Skills:**

**Testing (EVERY task):** @testing-test-driven-development (MANDATORY), @testing-test-writing, @testing-anti-patterns, @testing-debugging, @testing-final-verification, @testing-code-reviewer

**Global (all code):** @global-coding-style, @global-commenting, @global-conventions, @global-error-handling, @global-validation

**Backend:** @backend-api, @backend-models, @backend-queries, @backend-migrations

**Frontend:** @frontend-accessibility, @frontend-components, @frontend-css, @frontend-responsive

### Step 3: Automatic Context Management

**After EVERY task:** Check context usage (MESSAGE tokens + 35k overhead)

**If ≥ 80% (160k total):** `/remember` → STOP → Tell user to `/clear` then continue
**If < 80%:** Continue immediately

**CRITICAL**: System warnings show MESSAGE tokens only. Add ~35k for system/tools/memory overhead to get TOTAL context usage.

**Preserved after /clear:** ✅ Plan, Code, Tests, Cipher, Codebase | ❌ Conversation
**On restart:** Read plan → Check git → Query Cipher → Resume from pending task

### Step 4: Complete Development

**When ALL tasks are `[x]` complete:**
1. Run quick verification: `mcp__ide__getDiagnostics()` and `uv run pytest`
2. Store learnings: `mcp__cipher__ask_cipher("Store: Completed <feature>. Key learnings: <insights>")`
3. **INFORM USER:** "✅ All tasks complete. Run `/verify` for comprehensive verification"
4. DO NOT run /verify yourself - let user initiate

**Evidence required:** Test output, diagnostics clean

**NO completion claims without showing actual test output.**

## When to Stop

**STOP when:** Blocker hit | Plan has gaps | Instruction unclear | Verification fails repeatedly
**Ask, don't guess.**

**⚠️ NEVER SKIP TASKS:**
- If you cannot complete a task due to technical limitations, environment issues, or complexity:
  - STOP immediately
  - Report the specific blocker to the user
  - DO NOT mark the task as complete
  - DO NOT justify skipping with "MVP scope" or similar reasoning
- The plan is the contract - every task must be completed or explicitly discussed with the user

## Git Operations - READ ONLY

✅ **Allowed:** `git status`, `git diff`, `git log`, `git show`, `git branch`
❌ **FORBIDDEN:** `git add`, `git commit`, `git push`, `git pull`, `git merge`, `git rebase`, `git checkout`, `git reset`, `git stash`

## Remember

- Review plan critically → Raise concerns
- Standard Task Flow → TDD always
- Check diagnostics before/after
- Work autonomously until 80% context
- Auto /remember at 80%
- Stop when blocked
- Evidence required for completion
- **NEVER SKIP TASKS - Complete every task or stop and report blockers**
