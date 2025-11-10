---
description: Use when creating or planning anything - starts with discovery and clarification like design phase, then creates focused implementation plan with exact file paths, clear objectives, and verification steps (max 10-12 tasks)
model: opus
---

# Creating Focused Implementation Plans

## Overview

Transform ideas into actionable implementation plans through structured discovery, questioning, and focused task breakdown. This combines design exploration with concrete but concise implementation planning.

**Core principles:**
- Understand deeply, explore alternatives, plan focused and actionable
- **Zero-context assumption:** Assume implementer knows nothing about the codebase or domain
- Write plans that are self-contained and executable by a skilled developer with no prior context

**CRITICAL CONSTRAINT:** Plans MUST have 10-12 tasks maximum. If a feature needs more, split into multiple specifications.

**Workflow Position:** Step 1 of 3 in spec-driven development
- **This command (/plan):** Idea → Design → Implementation Plan
- **Next command (/implement):** Implementation Plan → Working Code
- **Final command (/verify):** Working Code → Verified Implementation

**Output location:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## Usage Modes

### Mode 1: Create New Plan (Default)
Use when starting fresh with a new feature or implementation.

### Mode 2: Extend Existing Plan
Use when adding tasks to an existing plan. User can provide:
- Path to existing plan: `/plan docs/plans/2024-11-04-auth-system.md`
- Or explicit instruction: "Add task to existing plan for user profile feature"

**When extending a plan:**
1. Load and parse the existing plan
2. Identify completed vs pending tasks
3. Add new tasks while preserving structure
4. Update total task count and progress tracking
5. Maintain original architecture decisions

## MCP Tools and Skills Available

### MCP Servers for Discovery & Planning

**Use these MCP servers during planning:**

1. **Cipher (START HERE)** - Query for past implementations, similar patterns, lessons learned
   ```
   mcp__cipher__ask_cipher("Have we implemented something similar to <feature>? What patterns worked?")
   mcp__cipher__ask_cipher("Store this implementation plan for <feature>")
   ```

2. **Claude Context** - Search codebase for existing patterns and exact file paths
   ```
   mcp__claude-context__search_code(path="/workspaces/...", query="authentication patterns")
   mcp__claude-context__index_codebase(path="/workspaces/...") # If not indexed
   mcp__claude-context__get_indexing_status(path="/workspaces/...")
   ```

3. **Ref/Context7** - Research documentation for design decisions and API details
   ```
   mcp__Ref__ref_search_documentation(query="pytest fixtures documentation")
   mcp__Ref__ref_read_url(url="https://...") # Read specific doc page
   mcp__context7__resolve-library-id(libraryName="react")
   mcp__context7__get-library-docs(context7CompatibleLibraryID="/facebook/react", topic="hooks")
   ```

4. **Database (if planning DB changes)** - Check current schema
   ```
   mcp__dbhub-postgres__execute_sql("SELECT column_name FROM information_schema.columns WHERE table_name='users'")
   ```

5. **Firecrawl (when additional information from web needed)** - External research for best practices
   ```
   mcp__firecrawl-mcp__firecrawl_search(query="best practices", sources=[{"type": "web"}])
   mcp__firecrawl-mcp__firecrawl_scrape(url="https://...", formats=["markdown"])
   ```

6. **MCP Funnel (for tool discovery)** - Find and use additional tools if needed
   ```
   mcp__mcp-funnel__discover_tools_by_words(words="example_words", enable=true)
   mcp__mcp-funnel__get_tool_schema(tool="tool_name")
   mcp__mcp-funnel__bridge_tool_request(tool="tool_name", arguments={})
   ```

**NOT needed during planning:** IDE diagnostics (no code yet)

### Available Skills for Implementation

These skills will be automatically activated during `/implement` when referenced in your plan:

#### Testing Skills (Use in Implementation Tasks)
- **@testing-test-driven-development** - MANDATORY for all code tasks (enforces RED-GREEN-REFACTOR cycle)
- **@testing-test-writing** - For creating test files and test case structure
- **@testing-anti-patterns** - When using mocks, test doubles, or complex test setup
- **@testing-debugging** - For systematic debugging and troubleshooting
- **@testing-final-verification** - For final verification before marking complete
- **@testing-code-reviewer** - After completing significant features

#### Global Skills (Apply to All Code)
- **@global-coding-style** - Clean code, naming conventions, DRY principles
- **@global-commenting** - Minimal, self-documenting code approach
- **@global-conventions** - Project structure, dependency management
- **@global-error-handling** - Error handling, try-catch, exceptions
- **@global-validation** - Input validation, data sanitization

#### Backend Skills (Server-Side Tasks)
- **@backend-api** - REST/GraphQL endpoints, route handlers
- **@backend-models** - Database models, ORMs, entity definitions
- **@backend-queries** - Database queries, repository patterns
- **@backend-migrations** - Database schema changes, migration files

#### Frontend Skills (Client-Side Tasks)
**@frontend-components** - UI components (React/Vue/Svelte)
**@frontend-css** - Styling, CSS/SCSS/Tailwind
**@frontend-accessibility** - ARIA attributes, keyboard navigation
**@frontend-responsive** - Responsive layouts, mobile-first design

## The Process

**New Plan Checklist:**
```
- [ ] Phase 0: Research (Cipher, codebase, documentation)
- [ ] Phase 1: Understanding (purpose, constraints, criteria)
- [ ] Phase 2: Exploration (2-3 approaches proposed)
- [ ] Phase 3: Design Validation (confirmed in sections)
- [ ] Phase 4: Implementation Planning (detailed tasks)
- [ ] Phase 5: Documentation (save to docs/plans/)
- [ ] Phase 6: Implementation Handoff
```

**Extending Plan Checklist:**
```
- [ ] Phase 0: Load and analyze existing plan
- [ ] Phase 1: Review completed vs pending tasks
- [ ] Phase 2: Research new requirements
- [ ] Phase 3: Understand new feature scope
- [ ] Phase 4: Design integration with existing
- [ ] Phase 5: Create new tasks maintaining consistency
- [ ] Phase 6: Update plan with new tasks/counts
- [ ] Phase 7: Save updated plan
```

### Phase 0: Research and Discovery

**Always start with:**
1. Query Cipher: `ask_cipher("What do we know about <feature>? Past implementations?")`
2. Search codebase: `search_code(path="/workspaces/...", query="related features")`
3. Check CLAUDE.md for project conventions
4. Query relevant MCP servers for external systems

**Additional for extending plans:**
1. Load existing plan: `Read(file_path="docs/plans/YYYY-MM-DD-<feature>.md")`
2. Parse structure (architecture, progress tracking, task status)
3. Check git status for partially completed work
4. Query Cipher for implementation learnings

### Phase 1: Understanding

- Ask ONE question at a time to refine requirements
- Use **AskUserQuestion tool** for structured choices
- Gather: Purpose, constraints, success criteria, integration points
- **For extending:** Verify compatibility with original architecture

**Example AskUserQuestion:**
```
Question: "Where should data be stored?"
Options: ["Session storage" (secure), "Local storage" (persistent), "Cookies" (SSR-compatible)]
```

### Phase 2: Exploration

- Propose 2-3 architectural approaches with trade-offs
- Use **AskUserQuestion tool** to present options
- **For extending:** Consider impact on existing components

### Phase 3: Design Validation

- Present design in 200-300 word sections
- Cover: Architecture, components, data flow, error handling, testing
- Ask: "Does this approach work for your needs?"
- Adjust based on feedback

### Phase 4: Implementation Planning

**CRITICAL: Task Count Limit**
- **Maximum: 10-12 tasks per plan**
- If initial breakdown exceeds 12 tasks, STOP and ask user to split into multiple features
- Example: "This feature requires 18 tasks. Should we split into: (A) Core CRUD + DB (8 tasks) and (B) Frontend + CDK (10 tasks)?"

**Required Plan Header:**
```markdown
# [Feature Name] Implementation Plan

> **IMPORTANT:** Start with fresh context. Run `/clear` before `/implement`.
> If context limits reached: `/remember` → `/clear` → `/implement` again

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

**Context for Implementer:**
- [Key codebase convention or pattern]
- [Domain knowledge needed]
- [Integration points or dependencies]

## Progress Tracking
- [ ] Task 1: [Brief summary]
- [ ] Task 2: [Brief summary]
- [ ] Task N: [Brief summary]

**Total Tasks:** [Number] (Max: 12)
```

**For Extending Plans:**
1. Preserve original header/architecture
2. Mark new tasks with `[NEW]` prefix
3. Check total: If original + new > 12 tasks, suggest splitting
4. Update total count: `Total Tasks: X (Originally: Y)`
5. Add extension history: `> Extended [Date]: Tasks X-Y for [feature]`
6. Insert tasks in logical order (after related, before dependent)

## Task Structure

**Keep tasks focused but complete. Include code examples ONLY for critical/complex patterns.**

```markdown
### Task N: [Component Name]

**Objective:** [1-2 sentences describing what to build]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py`
- Test: `tests/exact/path/to/test.py`

**Implementation Steps:**

1. **Write failing test** - Define expected behavior
   - Test command: `uv run pytest tests/path/test.py::test_name -v`
   - Expected: Test FAILS (function/class not defined)

2. **Implement minimal code** - Make test pass
   - Key pattern: [Brief description of approach]
   - Critical logic: [Include code example ONLY if complex/non-obvious]

3. **Verify tests pass** - Confirm test passes
   - Test command: `uv run pytest tests/path/test.py::test_name -v`
   - Expected: Test PASSES

4. **RUN ACTUAL PROGRAM** (MANDATORY if applicable) - Verify real-world behavior
   - ⚠️ Tests passing ≠ Program works! Must verify actual execution
   - Expected: [Specific logs/output/DB records/API responses]
   - Show actual output - never claim "should work"
   - Skip only if no runnable code (e.g., pure model/config changes)

**Skills:** @skill-name @another-skill

**Code Example (if complex):**
```python
# Include ONLY if pattern is complex or non-obvious
def critical_function():
    # Key implementation detail
    pass
```
```

**Example Task:**
```markdown
### Task 3: Data Access Layer

**Objective:** Create repository pattern for database operations with proper error handling.

**Files:**
- Create: `src/repositories/entity_repository.py`
- Test: `tests/repositories/test_entity_repository.py`

**Implementation Steps:**

1. **Write failing test** - Define expected repository behavior
   - Test command: `uv run pytest tests/repositories/test_entity_repository.py::test_get_by_id -v`
   - Expected: Test FAILS (EntityRepository not defined)

2. **Implement minimal code** - Create repository with CRUD methods
   - Key pattern: Repository pattern with parameterized queries
   - Critical logic: Use connection pooling, handle None cases

3. **Verify implementation** - Confirm test passes
   - Test command: `uv run pytest tests/repositories/test_entity_repository.py::test_get_by_id -v`
   - Expected: Test PASSES

4. **Execute actual code** - Verify database operations work
   - Run command: `uv run python -m src.repositories.entity_repository`
   - Expected: Successful connection, CRUD operations complete

**Skills:** @backend-queries @backend-models @testing-test-driven-development
```

## Skills to Reference in Tasks

**Mandatory:** `@testing-test-driven-development` for all code tasks

**Context-specific:**
`@backend-api` (endpoints), `@backend-models` (database), `@backend-queries` (SQL),
`@backend-migrations` (schema changes), `@global-error-handling`, `@global-validation`,
`@frontend-components` (UI), `@frontend-css` (styling), `@testing-final-verification` (last task)

## Coding Standards

✅ **Zero-context clarity** - Assume implementer knows nothing about codebase or domain
✅ **TDD Mandatory** - Test first (fail), implement, verify (pass), execute actual code
✅ **DRY/YAGNI** - No repetition or speculative features
✅ **Exact paths** - Complete file paths, no ambiguity
✅ **Bite-sized steps** - Break each task into 4 clear steps (test, implement, verify, execute)
✅ **Selective code examples** - Include code ONLY for complex/non-obvious patterns
✅ **Focused scope** - 10-12 tasks maximum, split if larger

### Phase 5: Plan Documentation

**New Plans:** Save to `docs/plans/YYYY-MM-DD-<feature-name>.md` with:
- Complete header with context management
- All tasks following concise structure (10-12 max)
- Referenced skills using @ syntax
- Clear file paths and objectives

**Extended Plans:** Update existing file with:
- Preserved completed work [x] checkboxes
- New tasks marked with `[NEW]`
- Extension metadata: `> Extended [Date]: Tasks X-Y for [feature]`
- Updated counts and Cipher storage of decisions
- Check: Total tasks must not exceed 12 (suggest split if needed)

### Phase 6: Implementation Handoff

1. Announce: "Plan saved to `docs/plans/YYYY-MM-DD-<feature-name>.md`"
2. Guide: "Has [N] tasks. To implement: `/clear` → `/implement [plan-path]`"
3. If context limits: "`/remember` → `/clear` → `/implement` again"
4. Ask: "Ready to clear context and start implementation?"

## Extension Examples

**Pattern 1: Insert Related Tasks**
```markdown
- [x] Task 1: Auth service setup
- [x] Task 2: JWT generation
- [ ] Task 3: [NEW] Error handler
- [ ] Task 4: [NEW] Rate limiting
- [ ] Task 5: User profile (was Task 3)
Total: 5 (Originally: 3)
```

**Pattern 2: Add Tests to Existing**
```markdown
- [x] Task 1: Payment gateway
- [ ] Task 2: [NEW] Unit tests for gateway
- [x] Task 3: Transaction model
- [ ] Task 4: [NEW] Unit tests for model
Total: 4 (Originally: 2)
```

**Pattern 3: Enhancement Section**
```markdown
### Original (Complete)
- [x] Tasks 1-5: Core feature
### Enhancement
- [ ] Task 6-8: [NEW] Additional feature
Total: 8 (Originally: 5, Completed: 5)
```

## When to Revisit Earlier Phases

Go backward when: New constraints revealed, validation gaps found, approach questioned, critical patterns discovered. Don't force forward progress.

## Key Principles

| Principle                | Application                                   |
| ------------------------ | --------------------------------------------- |
| **Research first**       | Always Cipher + codebase before planning      |
| **One question/time**    | Single question per message                   |
| **Structured choices**   | AskUserQuestion for 2-4 options               |
| **YAGNI/DRY**            | No speculation or repetition                  |
| **Explore alternatives** | Always 2-3 approaches                         |
| **Task limit**           | Maximum 10-12 tasks (split if more)           |
| **Zero-context**         | Assume implementer knows nothing              |
| **Bite-sized steps**     | 4-step flow: test, implement, verify, execute |
| **Selective code**       | Examples only for complex patterns            |
| **Fresh context**        | Start with /clear                             |

**For Extensions:** Preserve history, mark [NEW], group logically, update metadata, store in Cipher

## Remember

**All plans:** Research → Question → Explore → Validate → Task → Document → Handoff

**New:** Save to `docs/plans/YYYY-MM-DD-<feature>.md` (10-12 tasks max)
**Extend:** Update existing file, preserve completed work, mark additions [NEW], check task count

**Always include:**
- Exact file paths for all creates/modifies/tests
- 4-step flow: (1) test fail, (2) implement, (3) test pass, (4) **RUN ACTUAL PROGRAM**
- Step 4 is MANDATORY - tests alone don't prove program works
- Clear expected outputs: logs, DB records, API responses, file contents
- Code examples ONLY for complex/non-obvious patterns
- @ skill references for automatic enforcement
- E2E tests (Postman/Newman) for APIs

**Task count enforcement:**
- If breakdown > 12 tasks: STOP and suggest splitting
- Example split: "Backend Core (8 tasks) + Frontend (10 tasks)" rather than "Full Stack (18 tasks)"

**Zero-context principle:**
- Write as if implementer has never seen the codebase
- Include all context needed to understand the task
- Reference documentation if domain knowledge required
