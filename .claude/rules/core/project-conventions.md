## Project Conventions and Standards

**Standards:** Clear structure | Up-to-date docs | Environment config | Dependency management

### Project Structure

Organize files in a predictable, logical structure:
- Source code in `src/`
- Tests mirror `src/` structure in `tests/`
- Documentation in `docs/`
- Configuration at project root

Use consistent naming across directories.

### Documentation Standards

**README.md must include:**
- Project overview and purpose
- Setup instructions (prerequisites, installation)
- Basic usage examples
- Development workflow
- Testing instructions
- Contributing guidelines

**Keep current:** Update README when setup changes, document breaking changes immediately, remove outdated information.

### Version Control Practices

**Commit messages:**
- Clear, descriptive messages
- Present tense ("Add feature" not "Added feature")
- Reference issue numbers when applicable
- First line: concise summary (50 chars)

**Pull requests:**
- Clear title describing the change
- Description explaining why and what
- Link to related issues
- List testing performed

**Branches:**
- Use feature branches
- Keep branches short-lived
- Meaningful names (feature/, fix/, refactor/)

### Environment Configuration

**Use .env files for local configuration:**
- Never commit secrets or API keys
- Provide `.env.example` with all required variables
- Document all environment variables

### Dependency Management

**Keep dependencies minimal:**
- Only add when necessary
- Regularly review and remove unused packages
- Keep dependencies updated for security

**Document major dependencies:**
- Why each was chosen
- Alternatives considered
- Known issues or limitations

### Code Review Standards

**For reviewers:**
- Check code quality and standards
- Verify tests are present and passing
- Look for security issues
- Suggest improvements, don't demand perfection

**For authors:**
- Self-review before requesting review
- Keep PRs focused and reasonably sized
- Respond to all comments
- Resolve conversations when addressed

### Testing Requirements

**Before merging:**
- All tests must pass
- Code coverage should not decrease
- New features require tests
- Bug fixes include regression tests

### Feature Flags

Use feature flags for incomplete features to avoid long-lived branches.

Benefits: Merge code before complete, control rollout, easy rollback, A/B testing.

### Changelog Maintenance

Keep a changelog to track significant changes:
- When adding new features
- When making breaking changes
- When fixing significant bugs
- When removing functionality
