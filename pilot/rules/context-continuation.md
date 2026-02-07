# Context Continuation - Endless Mode for All Sessions

**Rule:** When context reaches critical levels, save state and continue seamlessly in a new session.

## Quality Over Speed - CRITICAL

**NEVER rush or compromise quality due to context pressure.**

- You can ALWAYS continue in the next session - work is never lost
- A well-done task split across 2 sessions is better than a rushed task in 1 session
- **Quality is the #1 metric** - clean code, proper tests, thorough implementation
- Do NOT skip tests, compress explanations, or cut corners to "beat" context limits

**The context limit is not your enemy.** It's just a checkpoint. The plan file, Pilot Memory, and continuation files ensure seamless handoff. Trust the system.

### ⛔ But at 90%+, HANDOFF OVERRIDES EVERYTHING

**At 90% context, the handoff IS the quality action.** Failing to hand off means losing ALL work.

- **"Finish current task" means the single tool call in progress** - NOT "fix every remaining error"
- **Do NOT start new fix cycles** at 90%+ (running linters, fixing type errors, running tests)
- **Document remaining errors** in the continuation file for the next session
- The "fix ALL errors" rule is **suspended** at 90%+ - incomplete fixes are expected and acceptable
- The next session will continue exactly where you left off - nothing is lost

## Session Identity

Continuation files are stored under `~/.pilot/sessions/<session-id>/` where `<session-id>` comes from the `PILOT_SESSION_ID` environment variable (defaults to `"default"` if not set). This ensures parallel sessions don't interfere with each other's continuation state.

**⚠️ CRITICAL: The context monitor hook prints the EXACT absolute path to use.** Copy the path from the hook output — do NOT try to resolve `$PILOT_SESSION_ID` yourself. If you need the path before the hook fires, resolve it explicitly:

```bash
echo $PILOT_SESSION_ID
```

Then construct the path: `~/.pilot/sessions/<resolved-id>/continuation.md`

## How It Works

This enables "endless mode" for any development session, not just /spec workflows:

1. **Context Monitor** warns at 80% and 90% usage
2. **You save state** to Pilot Memory before clearing
3. **Pilot restarts** Claude with continuation prompt
4. **Pilot Memory injects** your saved state
5. **You continue** where you left off

## When Context Warning Appears

When you see the context warning (80% or 90%), take action:

### At 80% - Prepare for Continuation

- Wrap up current task if possible
- Avoid starting new complex work
- Consider saving progress observation

### At 90% - Mandatory Continuation Protocol

**⚠️ CRITICAL: Execute ALL steps below in a SINGLE turn. DO NOT stop, wait for user response, or output summary and then pause. Write file → Trigger clear → Done.**

**Step 1: VERIFY Before Writing (CRITICAL)**

Before writing the continuation file, you MUST run verification commands:
```bash
# Run the project's test suite (e.g., uv run pytest -q, bun test, npm test)
# Run the project's type checker (e.g., basedpyright src, tsc --noEmit)
```

**DO NOT claim work is complete without showing verification output in the continuation file.**

**Step 2: Check for Active Plan (MANDATORY)**

**⚠️ CRITICAL: You MUST check for an active plan before deciding which handoff command to use.**

```bash
# Check for non-VERIFIED plans (most recent first by filename)
ls -1 docs/plans/*.md 2>/dev/null | sort -r | head -5
```

Then check the Status field in the most recent plan file(s). An **active plan** is any plan with `Status: PENDING` or `Status: COMPLETE` (not `VERIFIED`).

**Decision Tree:**
| Situation | Command to Use |
|-----------|----------------|
| Active plan exists (PENDING/COMPLETE) | `~/.pilot/bin/pilot send-clear docs/plans/YYYY-MM-DD-name.md` |
| No active plan (all VERIFIED or none exist) | `~/.pilot/bin/pilot send-clear --general` |

**NEVER use `--general` when there's an active plan file. This loses the plan context!**

**Step 3: Write Session Summary to File (GUARANTEED BACKUP)**

Write the summary using the Write tool to the **exact path printed by the context monitor hook** (Step 1 in the hook output). The path is an absolute path like `/Users/you/.pilot/sessions/12345/continuation.md`. **Do NOT use `$PILOT_SESSION_ID` as a literal string in the file path — the Write tool cannot resolve shell variables.**

Include VERIFIED status with actual command output.

```markdown
# Session Continuation

**Task:** [Brief description of what you were working on]
**Active Plan:** [path/to/plan.md or "None"]

## VERIFIED STATUS (run just before handoff):
- Test suite → **X passed** or **X failed** (be honest!)
- Type checker → **X errors** or **0 errors**
- If tests fail or errors exist, document WHAT is broken

## Completed This Session:
- [x] [What was VERIFIED as finished]
- [ ] [What was started but NOT verified/complete]

## IN PROGRESS / INCOMPLETE:
- [Describe exactly what was being worked on]
- [What command was being run]
- [What error or issue was being fixed]

## Next Steps:
1. [IMMEDIATE: First thing to do - be SPECIFIC]
2. [Include exact file:line if fixing something]

## Files Changed:
- `path/to/file.py` - [what was changed]
```

**CRITICAL: If you were in the middle of fixing something, say EXACTLY what and where. The next agent cannot read your mind.**

**Step 4: Output Summary AND Trigger Clear (SAME TURN)**

Output brief summary then IMMEDIATELY trigger clear in the same response:

```
🔄 Session handoff - [brief task description]. Triggering restart...
```

Then execute the send-clear command (do NOT wait for user response):

**Use the correct command based on Step 2:**

```bash
# If active plan exists (PREFERRED - preserves plan context):
~/.pilot/bin/pilot send-clear docs/plans/YYYY-MM-DD-name.md

# ONLY if NO active plan exists:
~/.pilot/bin/pilot send-clear --general
```

This triggers session continuation in Endless Mode:
1. Waits 10s for Pilot Memory to capture the session
2. Waits 5s for graceful shutdown (SessionEnd hooks run)
3. Waits 5s for session hooks to complete
4. Waits 3s for Pilot Memory initialization
5. Restarts Claude with the continuation prompt

Or if no active session, inform user:
```
Context at 90%. Please run `/clear` and then tell me to continue where I left off.
```

**Step 4: After Restart**

The new session receives:
- Pilot Memory context injection (including your Session End Summary)
- A continuation prompt instructing you to resume

## ⛔ MANDATORY: Clean Up Stale Continuation Files at Session Start

**At the START of EVERY session (not just continuation sessions), delete any stale continuation file:**

```bash
rm -f ~/.pilot/sessions/$PILOT_SESSION_ID/continuation.md
```

**Why this is critical:** Stale continuation files from previous sessions cause the Write tool to fail (it requires reading before writing). If the stale file contains old context, it can corrupt the handoff. This cleanup MUST happen before any work begins — even in quick-mode sessions that aren't continuations.

**When to clean up:**
- At the very start of every new session
- Before writing a new continuation file (as a safety net)
- The `send-clear` command does NOT guarantee the file is deleted

## Resuming After Session Restart

When a new session starts with a continuation prompt:

1. **Resolve session ID and read continuation file:**
   ```bash
   # Resolve the actual session ID first
   echo $PILOT_SESSION_ID
   ```
   Then use the Read tool with the resolved absolute path (e.g., `~/.pilot/sessions/12345/continuation.md`). **Do NOT pass `$PILOT_SESSION_ID` to the Read tool — resolve it first.**

2. **Delete the continuation file after reading it:**
   ```bash
   rm -f ~/.pilot/sessions/$PILOT_SESSION_ID/continuation.md
   ```

3. **Also check Pilot Memory** for injected context about "Session Continuation"

4. **Acknowledge the continuation** - Tell user: "Continuing from previous session..."

5. **Resume the work** - Execute the "Next Steps" from the continuation file immediately

## Integration with /spec

If you're in a /spec workflow (plan file exists):
- Use the existing `/spec --continue <plan-path>` mechanism
- The plan file is your source of truth

If you're in general development (no plan file):
- Use this continuation protocol
- Pilot Memory observations are your source of truth

## Quick Reference

| Context Level | Action |
|---------------|--------|
| < 80% | Continue normally |
| 80-89% | Wrap up current work, avoid new features |
| ≥ 90% | **MANDATORY:** Save state → Clear session → Continue |

## Pilot Commands for Endless Mode

```bash
# Check context percentage
~/.pilot/bin/pilot check-context --json

# Trigger session continuation (no continuation prompt)
~/.pilot/bin/pilot send-clear

# Trigger continuation WITH plan (PREFERRED when plan exists):
~/.pilot/bin/pilot send-clear docs/plans/YYYY-MM-DD-name.md

# Trigger continuation WITHOUT plan (ONLY when no active plan):
~/.pilot/bin/pilot send-clear --general
```

**⚠️ ALWAYS check for active plans before using `--general`. See Step 2 above.**

## Important Notes

1. **Don't ignore 90% warnings** - Context will fail at 100%
2. **Save before clearing** - Lost context cannot be recovered
3. **Pilot Memory is essential** - It bridges sessions with observations
4. **Trust the injected context** - It's your previous session's state
