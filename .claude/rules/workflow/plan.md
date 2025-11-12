## Six-Phase Planning Discovery Process

### Phase 0: Research and Discovery

**Always start with:**
1. Query Cipher: `mcp__cipher__ask_cipher("What do we know about <feature>? Past implementations?")`
2. Search codebase: `mcp__claude-context__search_code(path="/workspaces/...", query="related features")`
3. Query relevant MCP servers for external systems

**Goals:**
- Understand existing patterns
- Find similar implementations
- Identify reusable components
- Learn from past decisions

### Phase 1: Understanding

**Ask clarifying questions ONE at a time:**
- Use **AskUserQuestion tool** for structured choices
- Gather: Purpose, constraints, success criteria, integration points
- Don't assume - verify requirements explicitly

**Example structured question:**
```
Question: "Where should data be stored?"
Options:
  - "Session storage" (Secure, cleared on logout)
  - "Local storage" (Persistent across sessions)
  - "Cookies" (SSR-compatible, HTTP accessible)
```

**What to understand:**
- What problem does this solve?
- Who will use this feature?
- What are the constraints? (performance, security, compatibility)
- What defines success?
- How does it integrate with existing systems?

### Phase 2: Exploration

**Propose 2-3 architectural approaches:**
- Use **AskUserQuestion tool** to present options
- Each approach should have:
  - Brief description (2-3 sentences)
  - Key benefits
  - Trade-offs or limitations

**Example:**
```
Option A: Client-side filtering (Fast, no server load, limited scalability)
Option B: Server-side filtering (Scalable, secure, requires API changes)
Option C: Hybrid approach (Best of both, more complex)
```

Let the user choose the direction based on their priorities.

### Phase 3: Design Validation

**Present the chosen design in sections:**
- Keep each section 200-300 words
- Cover:
  - Architecture overview
  - Component breakdown
  - Data flow
  - Error handling strategy
  - Testing approach

**After each section:** Ask "Does this approach work for your needs?"
- Adjust based on feedback
- Don't proceed until design is validated

### Phase 4: Implementation Planning

**CRITICAL: Task Count Limit**
- **Maximum: 10-12 tasks per plan**
- If initial breakdown exceeds 12 tasks, STOP
- Ask user to split into multiple features

**Example split suggestion:**
```
"This feature requires 18 tasks. Should we split into:
(A) Core CRUD + Database (8 tasks)
(B) Frontend + Infrastructure (10 tasks)"
```

**Task Structure:**
```markdown
### Task N: [Component Name]

**Objective:** [1-2 sentences describing what to build]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py`
- Test: `tests/exact/path/to/test.py`

**Implementation Steps:**
1. Write failing test - Define expected behavior
2. Implement minimal code - Make test pass
3. Verify execution - Run actual program
4. Integration test - Test with other components
```

**Zero-context assumption:**
- Assume implementer knows nothing about codebase
- Provide exact file paths
- Explain domain concepts
- List integration points
- Reference similar patterns in codebase

### Phase 5: Documentation

**Save plan to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

**Required plan header:**
```markdown
# [Feature Name] Implementation Plan

> **IMPORTANT:** Start with fresh context. Run `/clear` before `/implement`.

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

**Total Tasks:** [Number] (Max: 12)
```

### Phase 6: Implementation Handoff

**After saving plan:**
1. Store in Cipher: `mcp__cipher__ask_cipher("Store this implementation plan for <feature>")`
2. Inform user: "✅ Plan saved to docs/plans/YYYY-MM-DD-<feature>.md"
3. Provide next steps: "Ready for implementation. Run `/clear` then `/implement <plan-path>`"

## Extending Existing Plans

**When adding tasks to existing plan:**

1. Load existing plan: `Read(file_path="docs/plans/...")`
2. Parse structure (architecture, completed tasks, pending tasks)
3. Check git status for partially completed work
4. Verify new tasks are compatible with existing architecture
5. Check total: If original + new > 12 tasks, suggest splitting
6. Mark new tasks with `[NEW]` prefix
7. Update total count: `Total Tasks: X (Originally: Y)`
8. Add extension history: `> Extended [Date]: Tasks X-Y for [feature]`
