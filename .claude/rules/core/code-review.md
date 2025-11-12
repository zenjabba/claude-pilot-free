## Automated Code Review with CodeRabbit

**Standards:** AI-powered analysis | Fix critical/high only | Iterative improvement

### What CodeRabbit Detects

- Race conditions and concurrency issues
- Memory leaks and resource cleanup
- Security vulnerabilities (SQL injection, XSS, etc.)
- Best practice violations
- Performance issues
- Error handling gaps
- Code complexity issues

**Why use it:**
- Catches complex issues standard linters miss
- Provides context-aware suggestions
- Identifies security vulnerabilities
- Analyzes code flow and logic

### Running CodeRabbit

```bash
# Review uncommitted changes
coderabbit --prompt-only --type uncommitted

# Review in background
coderabbit --prompt-only --type uncommitted &
CR_PID=$!

# Wait for completion
wait $CR_PID
```

**Note:** Check if CodeRabbit supports filtering by severity (e.g., `--severity critical,high`) to focus output.

### Rate Limits (Free Tier)

- 3 back-to-back reviews
- Then 2 reviews per hour
- 200 files per hour max
- 100 files per PR max

**If rate limited:** Wait ~8 minutes or proceed with other checks

### Processing Findings

**Focus on critical and high severity issues only.**

**Systematic approach:**
1. Create TodoWrite list for critical and high issues only
2. Prioritize: Critical first, then High
3. For each critical/high finding:
   - Read affected files
   - Understand issue context
   - Search similar patterns with `mcp__claude-context__search_code()`
   - Apply fix
   - Verify tests still pass
4. Store learnings in Cipher
5. Re-run CodeRabbit to verify
6. Repeat until no critical/high issues

**Medium/low severity:** Document but don't necessarily fix. Only fix if trivial or blocking.

### Common Critical/High Findings

**Race Conditions:** Add proper locking/synchronization
**Memory Leaks:** Ensure resource cleanup, close connections
**Security Vulnerabilities:** Sanitize inputs, use parameterized queries
**Error Handling Gaps:** Add try-catch, validate inputs
**Performance Issues:** Optimize algorithms, add caching (if critical)
**Best Practice Violations:** Follow framework conventions (if high severity)

### Integration Workflow

1. **Start early** - Run in background at beginning
2. **Continue working** - Run tests, check diagnostics
3. **Process when complete** - Review output, filter for critical/high
4. **Fix systematically** - One issue at a time, test after each
5. **Re-run to verify** - Ensure critical/high issues resolved
6. **Document remaining** - Note any unfixed medium/low issues

### When to Skip

**Skip for:** Documentation only, test fixtures only, configuration only, trivial formatting

**Always run for:** New features, bug fixes, refactoring, security-sensitive code, performance-critical code

### Success Criteria

**Required (blocking):**
- No critical severity findings
- No high severity findings
- All tests still passing
- No new diagnostics errors

**Optional (non-blocking):**
- Medium/low documented or fixed if trivial
- Can proceed with medium/low issues if documented
