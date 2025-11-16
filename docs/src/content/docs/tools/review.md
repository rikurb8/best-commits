---
title: Review Tool
description: AI-powered code review before committing
---

The `review` tool analyzes your uncommitted changes and provides detailed feedback before you commit.

## Quick Start

```bash
# Make some changes
vim src/app.py

# Get AI review
review

# Review feedback appears
# Prompt: "Proceed with commit? (y/n)"
```

## How It Works

```
1. Check for uncommitted changes
   ↓
2. Collect diffs (staged + unstaged)
   ↓
3. Filter noise (lock files, etc.)
   ↓
4. Send to AI model with review prompt
   ↓
5. Receive structured feedback
   ↓
6. Display review with formatting
   ↓
7. Ask: "Proceed with commit? (y/n)"
   ↓
8. If yes → Call commit tool
   ↓
9. If no → Exit
```

## Features

### Structured Review Format

The review includes:

1. **Executive Summary** - High-level overview of changes
2. **Gerrit Score** - Overall assessment (-2 to +2)
3. **Detailed Analysis**:
   - Correctness issues
   - Security concerns
   - Performance problems
   - Code quality notes
   - Error handling gaps
   - Best practices violations
4. **Breaking Changes** - API/behavior changes
5. **Improvement Suggestions** - Actionable recommendations
6. **Next Steps** - What to do with the feedback

### Gerrit Scoring System

| Score | Meaning | Description |
|-------|---------|-------------|
| **+2** | Looks good, approved | No issues found, ready to submit |
| **+1** | Looks good but minor issues | Acceptable with small improvements |
| **0** | Neutral | Needs work before submission |
| **-1** | I would prefer changes | Concerns that should be addressed |
| **-2** | Do not submit | Serious issues, blocking submission |

See [Scoring System](/tools/scoring) for detailed criteria.

### Intelligent Filtering

Automatically filters out:
- Lock files (`package-lock.json`, `yarn.lock`, `Gemfile.lock`)
- Generated code
- Binary files
- Very large minified files
- Build artifacts

### Example Output

```
$ review

🔍 Reviewing changes...

╭─ Code Review ─────────────────────────╮
│ Score: +1 (Looks good but minor      │
│            issues)                    │
╰───────────────────────────────────────╯

## Summary
Adds user authentication with JWT tokens.
Well-structured implementation with clear
separation of concerns.

## Issues Found

### Security
⚠️  No rate limiting on login endpoint
   - Could be vulnerable to brute force
   - Add rate limiting middleware

### Error Handling
⚠️  Missing try/catch in token verification
   - Could crash on malformed tokens
   - Wrap in try/catch block

## Suggestions
💡 Consider adding refresh token rotation
💡 Add password strength validation
💡 Log failed authentication attempts

## Breaking Changes
None

## Next Steps
1. Address security concerns
2. Add error handling
3. Consider suggestions
4. Run tests

🚀 Proceed with commit? (y/n):
```

## Usage

### Basic Usage

```bash
# In any git repository with changes
cd /path/to/your/repo
review
```

### With Specific Model

```bash
# Use Claude Opus for thorough review
BETTER_COMMIT_MODEL=claude-opus-4-20250514 review

# Use GPT-4o
BETTER_COMMIT_MODEL=gpt-4o review
```

### Review Without Committing

Press 'n' when prompted:

```bash
review
# ... review output ...
🚀 Proceed with commit? (y/n): n
```

### In Shell Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc
alias gr='review'
alias check='review'
alias deep-review='BETTER_COMMIT_MODEL=claude-opus-4-20250514 review'
```

## What It Analyzes

### Review Criteria

The AI evaluates your changes across 7 dimensions:

1. **Correctness**
   - Logic errors
   - Edge cases
   - Potential bugs

2. **Security**
   - Injection vulnerabilities
   - Authentication/authorization issues
   - Data exposure risks

3. **Performance**
   - Inefficient algorithms
   - N+1 queries
   - Memory leaks

4. **Code Quality**
   - Readability
   - Maintainability
   - Naming conventions

5. **Error Handling**
   - Missing error checks
   - Uncaught exceptions
   - Error recovery

6. **Best Practices**
   - Language idioms
   - Design patterns
   - Framework conventions

7. **Testing**
   - Test coverage
   - Test quality
   - Edge case tests

### Input Data

The tool sends:

1. **Git status**: Changed files
2. **Full diff**: All uncommitted changes (filtered)
3. **Review prompt**: Guidelines and criteria
4. **Scoring system**: Gerrit scale explanation

## Customization

### Edit the Prompt

```bash
# Navigate to best-commits repository
cd /path/to/best-commits

# Edit review prompt
vim tools/review_changes/PROMPT.md

# Edit scoring system
vim tools/review_changes/SCORING_SYSTEM.md

# Changes take effect immediately
review
```

**What you can customize**:
- Review criteria
- Focus areas
- Scoring thresholds
- Output format
- Tone and style
- Project-specific rules

See [Review Prompt](/tools/review-prompt) for the current prompt.

### Add Project-Specific Rules

```markdown
# In tools/review_changes/PROMPT.md

## Project-Specific Requirements

### This Project
- All API endpoints must have rate limiting
- Database queries must use prepared statements
- All user input must be validated
- Error messages must not expose internal details
- All mutations must have tests
```

## Model Recommendations

### For Standard Reviews

Balanced models work well:

```bash
export BETTER_COMMIT_MODEL=claude-sonnet-4-5-20250514  # Recommended
# or
export BETTER_COMMIT_MODEL=gpt-4o
```

**Cost**: ~$0.002-0.005 per review

### For Thorough Reviews

Use the most capable models for important code:

```bash
export BETTER_COMMIT_MODEL=claude-opus-4-20250514  # Best
# or
export BETTER_COMMIT_MODEL=o1-preview  # OpenAI reasoning model
```

**Cost**: ~$0.01-0.03 per review

### For Quick Checks

Fast models for simple changes:

```bash
export BETTER_COMMIT_MODEL=claude-haiku-4-5-20251001
# or
export BETTER_COMMIT_MODEL=gpt-3.5-turbo
```

**Cost**: ~$0.001-0.002 per review

## Best Practices

### When to Use Review

**Recommended**:
- New features
- Bug fixes
- Refactoring
- Security-sensitive code
- Public API changes
- Database migrations

**Optional**:
- Documentation updates
- Configuration changes
- Minor typos
- Generated code

### Workflow Patterns

**Pattern 1: Review → Fix → Commit**
```bash
# Make changes
vim src/feature.py

# Get review
review
# Press 'n' to skip commit

# Address issues
vim src/feature.py

# Review again
review
# Press 'y' to proceed with commit
```

**Pattern 2: Review → Commit in One**
```bash
# Make changes
vim src/feature.py

# Review and commit if approved
review
# Press 'y' to commit immediately
```

**Pattern 3: Quick Commits**
```bash
# For trivial changes, skip review
vim README.md
commit  # Skip review, direct commit
```

### Interpreting Reviews

**Score +2** (Approved):
- Safe to commit
- High quality code
- No issues found

**Score +1** (Minor issues):
- Generally good
- Consider suggestions
- Safe to commit if time-sensitive

**Score 0** (Neutral):
- Needs improvement
- Address issues before committing
- May need refactoring

**Score -1** (Prefer changes):
- Significant concerns
- Should address before committing
- Review again after fixes

**Score -2** (Do not submit):
- Critical issues
- Security vulnerabilities
- Must fix before committing

### Acting on Feedback

1. **Read the entire review** before reacting
2. **Prioritize security issues** - Always address
3. **Consider performance concerns** - May impact users
4. **Evaluate suggestions** - Not all are required
5. **Re-review after fixes** - Ensure issues resolved
6. **Use judgment** - AI can be wrong

## Limitations

### What It Cannot Do

- **Run tests** - Cannot verify functionality
- **Execute code** - Cannot check runtime behavior
- **Access external resources** - No API calls, databases
- **Understand full context** - Only sees the diff
- **Catch all bugs** - AI is helpful but not perfect
- **Make decisions** - Final call is yours

### Known Limitations

| Limitation | Impact | Workaround |
|-----------|--------|------------|
| Large diffs | May exceed token limit | Break into smaller commits |
| Complex logic | May miss subtle bugs | Manual review + tests |
| No execution | Can't verify behavior | Run tests |
| Limited context | Misses broader issues | Add comments |
| Language limits | Better for popular languages | Use with caution |

### False Positives

The AI may flag:
- Intentional code patterns
- Domain-specific conventions
- Optimization trade-offs
- Framework-specific patterns

**Use your judgment** to filter false positives.

### False Negatives

The AI may miss:
- Subtle race conditions
- Performance at scale
- Integration issues
- Business logic errors

**Don't skip manual review** for critical code.

## Workflow Integration

### With Git Hooks

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Require review approval before commit
uv run /path/to/best-commits/tools/review_changes/__main__.py

# Exit status is 0 if user approves, 1 if declines
exit $?
```

**Note**: Makes all commits interactive.

### In Code Review Process

1. **Local review** with the tool
2. **Address issues** found
3. **Commit** changes
4. **Create PR** for human review
5. **CI checks** run
6. **Human reviewers** approve

The AI review complements (doesn't replace) human review.

### In CI/CD

Run review in CI for PRs:

```yaml
# .github/workflows/ai-review.yml
name: AI Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Run AI review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          git clone https://github.com/yourusername/best-commits.git
          uv run best-commits/tools/review_changes/__main__.py
```

## Troubleshooting

### "No changes to review"

**Problem**: No uncommitted changes found

**Solution**:
```bash
# Check git status
git status

# Make sure you have changes
echo "test" >> README.md
review
```

### Review is too generic

**Problem**: AI doesn't provide specific feedback

**Solutions**:
1. **Use better model**:
   ```bash
   export BETTER_COMMIT_MODEL=claude-opus-4-20250514
   ```

2. **Make smaller, focused changes**
3. **Add code comments** explaining intent
4. **Customize prompt** with specific criteria

### Review misses obvious issues

**Possible causes**:
- Model not powerful enough
- Issue not visible in diff
- Complex domain-specific logic
- AI limitation

**Solutions**:
- Use more capable model
- Add context in comments
- Run linters and tests
- Manual review for critical code

### Lock files in review

**Problem**: Review includes package-lock.json

**Solution**: Should be automatically filtered. If not, check tool version or file issue.

## Advanced Usage

### Custom Scoring Thresholds

Edit the scoring system to match your standards:

```bash
vim tools/review_changes/SCORING_SYSTEM.md
```

### Multiple Review Passes

```bash
# First pass: Quick review
BETTER_COMMIT_MODEL=gpt-3.5-turbo review

# Second pass: Deep review
BETTER_COMMIT_MODEL=claude-opus-4-20250514 review
```

### Focused Reviews

Customize prompt for specific focus:

```markdown
# Temporary focus on security
For this review, focus exclusively on:
- SQL injection risks
- XSS vulnerabilities
- Authentication/authorization
- Data validation
```

## Examples

### Security Review

**Changes**: Login endpoint

**Review Output**:
```
Score: -1 (I would prefer changes)

## Issues Found

### Security (Critical)
❌ No rate limiting - brute force vulnerability
❌ Passwords logged in plaintext
❌ No HTTPS enforcement

### Recommendations
1. Add rate limiting (5 attempts/minute)
2. Remove password from logs
3. Enforce HTTPS in production
```

### Performance Review

**Changes**: Database query

**Review Output**:
```
Score: 0 (Needs work)

## Issues Found

### Performance
⚠️  N+1 query problem in user.posts loop
⚠️  Missing database index on email field

### Suggestions
- Use eager loading: User.includes(:posts)
- Add index: add_index :users, :email
```

### Quality Review

**Changes**: Refactoring

**Review Output**:
```
Score: +2 (Looks good)

## Summary
Excellent refactoring! Code is more readable
and maintainable.

## Positives
✓ Clear function names
✓ Good error handling
✓ Well-documented
✓ Tests updated

No issues found.
```

## Related Documentation

- [Tools Overview](/tools/) - All available tools
- [Commit Tool](/tools/commit) - Generate commit messages
- [Review Prompt](/tools/review-prompt) - View/edit AI prompt
- [Scoring System](/tools/scoring) - Gerrit scoring details
- [API Providers](/reference/api-providers) - Model selection
- [Configuration](/configuration) - Customize behavior

## See Also

- [Gerrit Code Review](https://www.gerritcodereview.com/) - Scoring system origin
- [Google Engineering Practices](https://google.github.io/eng-practices/review/) - Code review guide
