## Git Operations - READ ONLY

**Git:** READ-ONLY - `git status/diff/log/show/branch` ✅ | `git add/commit/push` ❌

Claude Code operates in **read-only mode** for git operations. This ensures the user maintains full control over version control decisions.

### Allowed Operations (Read-Only)

✅ **Status & Inspection:**
- `git status` - Check working tree status
- `git status --short` - Compact status view
- `git diff` - View changes in working directory
- `git diff --staged` - View staged changes
- `git log` - View commit history
- `git log --oneline` - Compact commit history
- `git show` - Show commit details
- `git branch` - List branches
- `git branch -a` - List all branches including remote

### Forbidden Operations (Write)

❌ **NEVER execute these commands:**
- `git add` - Staging files
- `git commit` - Creating commits
- `git push` - Pushing to remote
- `git pull` - Pulling from remote
- `git merge` - Merging branches
- `git rebase` - Rebasing commits
- `git checkout` - Switching branches (unless explicitly requested)
- `git reset` - Resetting commits
- `git stash` - Stashing changes

Users should explicitly control:
- What gets committed and when
- Commit messages and structure
- Branch management
- Remote synchronization

Claude Code can suggest commit messages or git operations, but **execution remains with the user**.
