---
description: Create a detailed implementation plan with exploration for Claude CodePro
model: opus
---
# PLAN MODE: Five-Phase Planning Process

> **WARNING: DO NOT use the built-in `ExitPlanMode` or `EnterPlanMode` tools.**
> This project has its own planning workflow using `/plan`, `/implement`, and `/verify` slash commands.
> The built-in Claude Code plan mode tools write to different paths and are incompatible.
> When planning is complete, simply inform the user and wait for confirmation - no special tool needed.

## MCP Servers - Use Throughout Planning

| Server | Purpose | When to Use |
|--------|---------|-------------|
| **Cipher** | Project memory | Query past decisions, store plan context |
| **Claude Context** | Semantic code search | Find patterns, similar implementations |
| **Exa** | Web search & code examples | Research libraries, find documentation |
| **MCP Funnel** | Tool discovery | Find specialized tools when needed |

**Start every planning session by querying Cipher for relevant history.**


## Using AskUserQuestion - Core Planning Tool

**The AskUserQuestion tool is essential for effective planning.** Questions are grouped into batches so users answer related questions together without interruption.

### Question Batching Strategy

Questions are consolidated into two batches for a smooth user experience:

| Batch | When | Purpose |
|-------|------|---------|
| **Batch 1** | Phase 0 (before exploration) | Clarify task, scope, priorities |
| **Batch 2** | Phase 2 (after exploration) | Architecture choices, design decisions |

**Don't scatter questions across phases** - gather them and present together.

### When to Use AskUserQuestion

| Situation | Example Question |
|-----------|------------------|
| **Unclear requirements** | "Should this feature support batch processing or single items only?" |
| **Multiple valid approaches** | Present 2-3 options with trade-offs for user to choose |
| **Ambiguous scope** | "Should we include error recovery, or fail fast?" |
| **Technology choices** | "Prefer async/await or callbacks for this integration?" |
| **Priority decisions** | "Performance or simplicity - which matters more here?" |
| **Missing domain knowledge** | "How does the existing auth flow work in production?" |

### How to Structure Questions

**Use the AskUserQuestion tool with clear options:**
```
Question: "Which authentication approach should we use?"
Options:
- Option A: JWT tokens (stateless, scalable, requires token refresh logic)
- Option B: Session-based (simpler, requires session storage)
- Option C: OAuth integration (most secure, more complex setup)
```

**Key principles:**
- Present options, not open-ended questions when possible
- Include trade-offs for each option
- **Batch related questions together** - don't interrupt user flow
- Don't proceed with assumptions - ASK


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


## Creating New Plans

### Phase 0: Task Understanding & Clarification

**First, clearly state your understanding of the task.**

Before any exploration:
1. Restate what the user is asking for in your own words
2. Identify the core problem being solved
3. List any assumptions you're making

**Then gather all clarifications needed (Question Batch 1):**

Use AskUserQuestion to ask everything upfront in a single interaction:

```
I want to confirm my understanding and clarify a few things:

Questions:
1. "Is my understanding correct?"
   - Yes, that's correct
   - Partially correct (please clarify)
   - No, let me explain

2. "What's the priority for this feature?"
   - Performance (fast, optimized)
   - Simplicity (easy to maintain)
   - Flexibility (extensible)

3. "Should error handling be comprehensive or minimal?"
   - Comprehensive (recovery, retries, detailed logging)
   - Basic (fail fast, simple error messages)
```

**Don't proceed to exploration until clarifications are complete.**

### Phase 1: Exploration

**Explore the codebase systematically.** Run explorations **one at a time** (sequentially, not in parallel).

**Exploration areas (in order):**

1. **Architecture** - Project structure, entry points, how components connect
2. **Similar Features** - Existing patterns that relate to the task, what can be reused
3. **Dependencies** - Imports, modules, what will be impacted
4. **Tests** - Test infrastructure, existing patterns, available fixtures

**For each area:**
- Use Task tool with `subagent_type='Explore'` OR search directly with Grep/Glob
- Document hypotheses (not conclusions)
- Note full file paths for relevant code
- Track questions that remain unanswered

**Also query memory and external sources:**
- Cipher: `mcp__cipher__ask_cipher("What do we know about <feature>?")`
- Codebase: `mcp__claude-context__search_code(path, "related features")`

**After explorations complete:**
1. Read each identified file to verify hypotheses
2. Build a complete mental model of current architecture
3. Identify integration points and potential risks
4. Note reusable patterns

### Phase 2: Design Decisions

**Present findings and gather all design decisions (Question Batch 2).**

Summarize what you found, then use AskUserQuestion with all decisions at once:

```
Based on my exploration, I found [summary of key findings].

I have some design questions:

Questions:
1. "Which architecture approach should we use?"
   - Option A: [description + trade-offs]
   - Option B: [description + trade-offs]
   - Option C: [description + trade-offs]

2. "How should we handle [specific concern found during exploration]?"
   - Option A: [approach]
   - Option B: [approach]

3. "The existing [component] uses [pattern]. Should we follow it or try something different?"
   - Follow existing pattern (consistency)
   - Use new approach (explain why)
```

**After user answers:**
- Summarize the chosen design approach
- Confirm: "Does this design work for your needs?"
- Don't proceed until design is validated

### Phase 3: Implementation Planning

**CRITICAL: Task Count Limit**
- **Maximum: 10-12 tasks per plan**
- If breakdown exceeds 12 tasks, use AskUserQuestion to ask user to split into multiple features

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

**Definition of Done:**
- [ ] All tests pass (unit, integration if applicable)
- [ ] No diagnostics errors (linting, type checking)
- [ ] Code functions correctly with real data
- [ ] Edge cases handled appropriately
- [ ] Error messages are clear and actionable
```

**Zero-context assumption:**
- Assume implementer knows nothing about codebase
- Provide exact file paths
- Explain domain concepts
- List integration points
- Reference similar patterns in codebase

### Phase 4: Documentation

**Save plan to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

**Required plan template:**

```markdown
# [Feature Name] Implementation Plan

> **IMPORTANT:** Start with fresh context. Run `/clear` before `/implement`.

Created: [Date]
Status: PENDING

> **Status Lifecycle:** PENDING → COMPLETE → VERIFIED
> - PENDING: Initial state, awaiting implementation
> - COMPLETE: All tasks implemented (set by /implement)
> - VERIFIED: Rules supervisor passed (set automatically)

## Summary
**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about chosen approach]

**Tech Stack:** [Key technologies/libraries]

## Scope

### In Scope
- [What WILL be changed/built]
- [Specific components affected]

### Out of Scope
- [What will NOT be changed]
- [Explicit boundaries]

## Prerequisites
- [Any requirements before starting]
- [Dependencies that must exist]
- [Environment setup needed]

## Context for Implementer
- [Key codebase convention or pattern]
- [Domain knowledge needed]
- [Integration points or dependencies]

## Progress Tracking

**MANDATORY: Update this checklist as tasks complete. Change `[ ]` to `[x]`.**

- [ ] Task 1: [Brief summary]
- [ ] Task 2: [Brief summary]
- [ ] ...

**Total Tasks:** [Number] | **Completed:** 0 | **Remaining:** [Number]

## Implementation Tasks

### Task 1: [Component Name]
[Full task structure from Phase 3]

### Task 2: [Component Name]
[Full task structure from Phase 3]

## Testing Strategy
- Unit tests: [What to test in isolation]
- Integration tests: [What to test together]
- Manual verification: [Steps to verify manually]

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Low/Med/High | Low/Med/High | [How to mitigate] |

## Open Questions
- [Any remaining questions for the user]
- [Decisions deferred to implementation]

---
**USER: Please review this plan. Edit any section directly, then confirm to proceed.**
```

### Phase 5: Implementation Handoff

**After saving plan:**

1. **Store in Cipher:** `mcp__cipher__ask_cipher("Store: implementation plan for <feature>")`
2. **Inform user:** "Plan saved to docs/plans/YYYY-MM-DD-<feature>.md"
3. **Request review:** Ask user to review and edit the plan
4. **Wait for explicit confirmation** before proceeding

**After user confirms:**

1. **Re-read the plan file completely** - User may have edited it
2. **Note any changes** the user made
3. **Acknowledge changes** before proceeding
4. Provide next steps: "Ready for implementation. Run `/clear` then `/implement <plan-path>`"

**DO NOT write or edit any implementation files until confirmed.**


## Critical Rules

These rules are non-negotiable:

1. **USE AskUserQuestion when uncertain** - Don't guess, ask the user
2. **Batch questions together** - Don't interrupt user with scattered questions
3. **Run explorations sequentially** - One at a time, never in parallel
4. **NEVER write implementation code during planning** - Planning and implementing are separate
5. **NEVER assume - verify by reading files** - Hypotheses must be confirmed
6. **ALWAYS get user confirmation before implementing** - User owns the decision
7. **ALWAYS re-read the plan after user confirms** - They may have edited it
8. **The plan must be detailed enough that another developer could follow it**
9. **NEVER use built-in ExitPlanMode or EnterPlanMode tools** - This project uses custom `/plan`, `/implement`, `/verify` slash commands. The built-in plan mode tools are incompatible with this workflow.
