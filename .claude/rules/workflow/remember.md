# Remember Session Learnings

**Purpose:** Preserve learnings in Cipher before `/clear`.

**Workflows:**
- **With plan:** `/remember` → `/clear` → `/implement [plan]` (continues with fresh context)
- **Without plan (/quick):** `/remember` → `/clear` → `/quick [task]` (continues quick work)

## The Process

### Step 1: Update Plan Progress (Only if using /plan → /implement workflow)

**CRITICAL:** Only mark tasks as complete if FULLY WORKING (tests pass + actual code executes successfully)

Check `git status --short` → Update plan's Progress Tracking:
- Mark completed: `- [ ]` → `- [x]` ONLY if tests pass AND code works
- Leave incomplete: `- [ ]` if tests fail OR code not executed OR broken functionality
- Add sub-tasks for incomplete work: Task 6.1, 6.2
- Update counts and percentages

**DO NOT mark tasks complete if:**
- Tests failing
- Code not executed
- Program crashes
- Outputs incorrect
- Only partially implemented

### Step 2: Identify Key Learnings

**Capture:** Technical discoveries | Design decisions | Implementation details | Problems solved | Gotchas
**Skip:** Trivial changes | Obvious implementations | Temporary debug steps

### Step 3: Store in Cipher

```
mcp__cipher__ask_cipher("Store: [Feature] - [Title]
Built: [What/how]
Decisions: [Choice]: [Why]
Patterns: [Pattern]: [Application]
Key files: [file:line] - [Significance]
Gotchas: [Problem] → [Solution]
Docs: [plan/design path]")
```

### Step 4: Confirm Storage

```
✅ Stored [N] learnings in Cipher
Next: `/clear` → `/implement [plan]` to continue
```

## Key Principles & What to Store

**Principles:** Run BEFORE `/clear` | Be specific (file:line) | Explain WHY | Update plan inline | Store gotchas

**✅ Store:** Architecture decisions | Working patterns | Problem solutions | Complex logic | Integration points | Gotchas

**❌ Skip:** Trivial changes | Obvious implementations | Debug steps | Vague progress statements
