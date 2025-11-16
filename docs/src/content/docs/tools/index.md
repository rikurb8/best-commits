---
title: Tools Overview
description: Overview of Best Commits AI-powered Git tools
---

Best Commits provides two main tools that enhance your Git workflow with AI assistance.

## Available Tools

### `commit` - AI-Powered Commit Messages

Automatically generates well-formatted, conventional commit messages by analyzing your git changes.

**Key Features**:
- ✓ Analyzes staged and unstaged changes
- ✓ Generates conventional commit format (feat:, fix:, docs:, etc.)
- ✓ Follows best practices (imperative mood, 50-char summary)
- ✓ Beautiful terminal output with Rich formatting
- ✓ Creates actual git commits automatically

**Usage**:
```bash
cd /path/to/your/repo
# Make some changes
echo "new feature" >> src/app.py
# Generate commit message and commit
commit
```

[Learn more →](/tools/commit)

---

### `review` - AI-Powered Code Review

Reviews your uncommitted changes and provides detailed feedback before you commit.

**Key Features**:
- ✓ Reviews both staged and unstaged changes
- ✓ Provides structured feedback with summary, issues, and suggestions
- ✓ Uses Gerrit scoring system (-2 to +2)
- ✓ Filters out noise (lock files, generated code)
- ✓ Interactive prompt to proceed with commit
- ✓ Chains directly to `commit` command

**Usage**:
```bash
cd /path/to/your/repo
# Make some changes
vim src/app.py
# Get AI review feedback
review
# Optionally proceed to commit (y/n)
```

[Learn more →](/tools/review)

## Common Workflows

### Basic Workflow

```bash
# 1. Make changes to your code
vim src/app.py

# 2. Review changes
review

# 3. Address any issues
vim src/app.py

# 4. Review again or commit directly
commit
```

### Quick Commit Workflow

For small, straightforward changes:

```bash
# Make a quick fix
vim README.md

# Commit directly without review
commit
```

### Thorough Review Workflow

For important changes:

```bash
# Make significant changes
vim src/*.py

# Deep review with powerful model
BETTER_COMMIT_MODEL=claude-opus-4-20250514 review

# If approved, proceed with commit
```

## Tool Comparison

| Feature | `commit` | `review` |
|---------|----------|----------|
| **Purpose** | Generate commit messages | Analyze code quality |
| **Input** | Git diff | Git diff |
| **Output** | Commit message → Git commit | Structured review feedback |
| **Token Limit** | 1024 | 2048 |
| **Speed** | Fast (~2-5 seconds) | Medium (~5-10 seconds) |
| **Interactive** | No (auto-commits) | Yes (y/n prompt) |
| **Chaining** | Standalone | Can chain to `commit` |

## Model Recommendations

### For Commit Messages

Fast models work great:
```bash
# Default - good balance
claude-haiku-4-5-20251001

# Fastest and cheapest
gpt-3.5-turbo
gemini/gemini-flash
```

### For Code Reviews

Use more capable models:
```bash
# Recommended for thorough reviews
claude-sonnet-4-5-20250514
gpt-4o

# Best for complex reviews
claude-opus-4-20250514
```

## Advanced Features

### Prompt Customization

Both tools load prompts from markdown files that you can customize:

- **Commit**: `tools/commit_changes/PROMPT.md`
- **Review**: `tools/review_changes/PROMPT.md`
- **Scoring**: `tools/review_changes/SCORING_SYSTEM.md`

Changes take effect immediately since prompts are loaded at runtime.

[View commit prompt →](/tools/commit-prompt)
[View review prompt →](/tools/review-prompt)
[View scoring system →](/tools/scoring)

### Filtering

The review tool automatically filters:
- Lock files (`package-lock.json`, `yarn.lock`, etc.)
- Generated code
- Binary files
- Large minified files

### Output Formats

Both tools use Rich library for beautiful terminal output:

**commit** outputs:
- Progress indicators
- Colored git diffs
- Generated commit message in a panel
- Success confirmation

**review** outputs:
- Executive summary
- Gerrit score with color coding
- Categorized issues (security, performance, etc.)
- Improvement suggestions
- Breaking changes warnings
- Next steps

## Integration Patterns

### With Git Aliases

```bash
# Add to ~/.gitconfig
[alias]
    ai-commit = !commit
    ai-review = !review
    quick = !commit
    check = !review
```

### With Shell Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc
alias gc='commit'
alias gr='review'
alias grc='review'  # r for review, c for commit chain
```

### With Git Hooks

```bash
# .git/hooks/pre-commit
#!/bin/bash
review || exit 1
```

**Note**: Requires manual approval for each commit.

### In CI/CD

```yaml
# GitHub Actions example
- name: Review PR changes
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  run: |
    git clone https://github.com/yourusername/best-commits.git
    uv run best-commits/tools/review_changes/__main__.py
```

## Performance Tips

### Speed Optimization

1. **Use fast models** for routine commits:
   ```bash
   export BETTER_COMMIT_MODEL=gpt-3.5-turbo
   ```

2. **Create aliases** for different speeds:
   ```bash
   alias quick-commit='BETTER_COMMIT_MODEL=gpt-3.5-turbo commit'
   alias thorough-review='BETTER_COMMIT_MODEL=claude-opus-4-20250514 review'
   ```

3. **Skip review** for trivial changes:
   ```bash
   commit  # Skip review, directly commit
   ```

### Cost Optimization

1. **Use cheaper models** by default:
   ```bash
   export BETTER_COMMIT_MODEL=claude-haiku-4-5-20251001  # ~$1/M tokens
   ```

2. **Reserve expensive models** for important reviews:
   ```bash
   alias critical-review='BETTER_COMMIT_MODEL=claude-opus-4-20250514 review'
   ```

3. **Batch commits** when appropriate:
   ```bash
   # Make multiple small commits instead of one large review
   git add file1.py && commit
   git add file2.py && commit
   ```

## Limitations

### What the tools CAN'T do

- **Understand broader context** beyond the current diff
- **Access external resources** or APIs
- **Run tests** or verify functionality
- **Understand natural language** requests (no chat interface)
- **Modify code** automatically

### Current Constraints

- **Token limits**: 1024 (commit), 2048 (review)
- **Diff size**: Very large diffs may be truncated
- **Binary files**: Not analyzed
- **External context**: No access to issue trackers, docs, etc.

### Future Enhancements

See the [project roadmap](/#future-plans) for planned improvements.

## Tool Architecture

Both tools follow a similar architecture:

```
User runs command
    ↓
Check for uncommitted changes
    ↓
Collect git diff (staged + unstaged)
    ↓
Filter noise (review only)
    ↓
Load prompt from PROMPT.md
    ↓
Call AI model via LiteLLM
    ↓
Format and display output
    ↓
Execute action (commit or prompt)
```

[Learn more about architecture →](/development/architecture)

## Related Documentation

- [Installation Guide](/installation) - Install the tools
- [Configuration](/configuration) - Customize behavior
- [API Providers](/reference/api-providers) - Set up AI models
- [Troubleshooting](/troubleshooting) - Fix common issues
- [FAQ](/reference/faq) - Common questions

## Examples

### Example: Commit Output

```
$ commit

🔍 Analyzing changes...

📝 Generated commit message:
┌────────────────────────────────────────┐
│ feat: add user authentication module  │
│                                        │
│ Implements JWT-based authentication    │
│ with token refresh and secure storage │
└────────────────────────────────────────┘

✅ Committed successfully!
```

### Example: Review Output

```
$ review

🔍 Reviewing changes...

╭─ Code Review ─────────────────────────╮
│ Score: +1 (Looks good but has minor  │
│            issues)                    │
╰───────────────────────────────────────╯

📊 Summary:
Adds user authentication with JWT tokens.
Good structure but needs error handling.

⚠️  Issues:
1. [Security] No rate limiting on login
2. [Error Handling] Missing try/catch

💡 Suggestions:
- Add rate limiting middleware
- Implement proper error boundaries

🚀 Proceed with commit? (y/n):
```

## Getting Started

Ready to use these tools?

1. [Install Best Commits](/installation)
2. [Configure your API key](/configuration)
3. [Try the commit tool](/tools/commit)
4. [Try the review tool](/tools/review)
