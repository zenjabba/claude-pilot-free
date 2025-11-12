## Context Management (95% Rule)

### How to Calculate Context

**System warnings show MESSAGE tokens only, not total!**
```
System warning: "Token usage: X/200000"
Total = X + 35000 (system/tools overhead)
Percentage = (Total / 200000) * 100
```

**Example:** 155k message tokens + 35k overhead = 190k total = 95%

### Thresholds & Actions

**< 80% (< 160k total):**
- Continue freely
- Take on any size task

**80-85% (160-170k total):**
- Context aware mode
- Finish current work
- Avoid starting large tasks (big refactors, reading many files)
- Prefer small, focused changes

**85-90% (170-180k total):**
- Complete small fixes only
- No new feature implementation
- Focus on wrapping up

**≥ 90% (≥ 180k total):**
- HARD STOP - no exceptions
- Risk of context overflow with any operation

### At 90% - Mandatory Sequence

1. **Run `/remember` immediately** - Store learnings in Cipher
2. **STOP all work** - No "one more fix"
3. **Inform user:**
   ```
   Context at 90% (Xk/200k). Running /remember to preserve learnings.
   Please run: `/clear` then `/implement <plan>` to continue.
   ```

### What Gets Preserved After /clear

**✅ Kept:**
- All code and tests in repository
- Plan files in `docs/plans/`
- Cipher learnings (via /remember)
- Searchable codebase

**❌ Lost:**
- Conversation history
- Context about decisions (unless stored in Cipher)

### Resume Process After /clear

1. **Read plan** - Understand what's being built
2. **Check git status** - See what's done
3. **Query Cipher** - Retrieve stored learnings
4. **Continue from pending tasks** - Look for `[ ]` vs `[x]` in plan

### Why 90% Not Higher?

- Tool calls can consume 5-10k tokens
- File reads add significant context
- Error traces can be large
- Better safe than context overflow mid-task
- Provides buffer for completion and cleanup
