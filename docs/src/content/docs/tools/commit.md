---
title: Commit Tool
description: AI-powered commit message generation
---

The `commit` tool automatically generates well-formatted, conventional commit messages by analyzing your git changes.

## Quick Start

```bash
# Make some changes
echo "new feature" >> src/app.py

# Generate commit message and commit
commit
```

That's it! The tool:
1. Analyzes your changes
2. Generates a commit message
3. Creates the commit automatically

## How It Works

```
1. Check for uncommitted changes
   ↓
2. Collect diffs (staged + unstaged)
   ↓
3. Stage all changes (git add -A)
   ↓
4. Send to AI model with prompt
   ↓
5. Generate commit message
   ↓
6. Create git commit
   ↓
7. Display confirmation
```

## Features

### Conventional Commits Format

The tool generates commits following the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>: <description>

[optional body]
```

**Types**:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

### Best Practices

The tool follows commit message best practices:
- **Imperative mood**: "Add feature" not "Added feature"
- **Concise summary**: ≤50 characters
- **Clear description**: Explains what and why
- **Optional body**: Provides context when needed

### Example Output

```
$ commit

🔍 Analyzing changes...

📝 Generated commit message:
┌────────────────────────────────────────┐
│ feat: add user authentication module  │
│                                        │
│ Implements JWT-based authentication    │
│ with token refresh capability          │
└────────────────────────────────────────┘

✅ Committed successfully!
```

## Usage

### Basic Usage

```bash
# In any git repository with changes
cd /path/to/your/repo
commit
```

### With Specific Model

```bash
# Use GPT-4
BETTER_COMMIT_MODEL=gpt-4o commit

# Use Claude Opus
BETTER_COMMIT_MODEL=claude-opus-4-20250514 commit
```

### In a Shell Alias

```bash
# Add to ~/.bashrc or ~/.zshrc
alias gc='commit'
alias quick-commit='BETTER_COMMIT_MODEL=gpt-3.5-turbo commit'
```

## What It Analyzes

The tool sends these to the AI model:

1. **Git status**: List of changed files
   ```
   M  src/app.py
   A  src/auth.py
   D  src/old.py
   ```

2. **Unstaged diff**: What changed in unstaged files
   ```diff
   diff --git a/src/app.py b/src/app.py
   +def new_function():
   +    pass
   ```

3. **Staged diff**: What changed in staged files
   ```diff
   diff --git a/src/auth.py b/src/auth.py
   +class Auth:
   +    pass
   ```

## Customization

### Edit the Prompt

```bash
# Navigate to best-commits repository
cd /path/to/best-commits

# Edit prompt template
vim tools/commit_changes/PROMPT.md

# Changes take effect immediately
commit
```

**What you can customize**:
- Commit message format
- Type prefixes
- Examples
- Best practices
- Length requirements
- Tone and style

See [Commit Prompt](/tools/commit-prompt) for the current prompt.

### Change Default Model

```bash
# In ~/.bashrc or ~/.zshrc
export BETTER_COMMIT_MODEL=claude-sonnet-4-5-20250514

# Now all commits use this model
commit
```

## Model Recommendations

### For Speed

Fast and cheap models work great for commits:

```bash
export BETTER_COMMIT_MODEL=claude-haiku-4-5-20251001  # Default
# or
export BETTER_COMMIT_MODEL=gpt-3.5-turbo
# or
export BETTER_COMMIT_MODEL=gemini/gemini-flash
```

**Cost**: ~$0.0003-0.0006 per commit

### For Quality

Use better models for important commits:

```bash
export BETTER_COMMIT_MODEL=claude-sonnet-4-5-20250514
# or
export BETTER_COMMIT_MODEL=gpt-4o
```

**Cost**: ~$0.002-0.005 per commit

## Best Practices

### Make Focused Commits

**Good** (single purpose):
```bash
# Add one feature
vim src/auth.py
commit  # "feat: add JWT authentication"

# Fix one bug
vim src/api.py
commit  # "fix: handle null response in API call"
```

**Avoid** (mixed changes):
```bash
# Multiple unrelated changes
vim src/auth.py src/api.py README.md tests/test_*.py
commit  # Generates vague "chore: various updates"
```

### Review Before Committing

For important changes, use the review tool first:

```bash
review  # Get AI feedback
# Address issues
commit  # Generate commit message
```

### Add Descriptive Comments

The AI generates better messages when your code has good comments:

```python
# Good: Explains intent
def calculate_discount(price, user_level):
    """Calculate discount based on user membership level.

    Premium users get 20% off, regular users get 10% off.
    """
    if user_level == "premium":
        return price * 0.8
    return price * 0.9

# Poor: No context
def calc(p, u):
    if u == "premium":
        return p * 0.8
    return p * 0.9
```

### Commit Related Changes Together

```bash
# Good: Feature and its test together
vim src/auth.py tests/test_auth.py
commit  # "feat: add JWT authentication with tests"

# Also good: Separate if tests are extensive
vim src/auth.py
commit  # "feat: add JWT authentication"
vim tests/test_auth.py
commit  # "test: add comprehensive JWT auth tests"
```

## Limitations

### What It Cannot Do

- **Understand broader context** beyond the diff
- **Access issue trackers** or documentation
- **Verify functionality** or run tests
- **Follow project-specific conventions** (unless in prompt)
- **Generate perfect messages** every time

### Current Constraints

| Aspect | Limit | Workaround |
|--------|-------|------------|
| Diff size | ~4000 tokens | Make smaller commits |
| Token output | 1024 max | Adequate for messages |
| Context | Only current diff | Add code comments |
| Languages | All supported | N/A |

### When to Skip the Tool

Consider writing messages manually when:
- **Trivial changes**: "fix typo", "update version"
- **Generated code**: Lock files, build artifacts
- **Revert commits**: Use `git revert` directly
- **Merge commits**: Use git's default merge message
- **Very complex changes**: Multi-part features

## Workflow Integration

### With Git Aliases

```bash
# In ~/.gitconfig
[alias]
    ai = "!commit"
    smart = "!commit"
    auto = "!commit"
```

Then use:
```bash
git ai     # Instead of git commit
git smart  # Instead of git commit
```

### With Pre-Commit Hooks

You can run the review tool before committing:

```bash
# .git/hooks/pre-commit
#!/bin/bash
review || exit 1
```

**Note**: This makes `git commit` interactive.

### In CI/CD

Verify commit message format in CI:

```yaml
# .github/workflows/check-commits.yml
name: Check Commits
on: [pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check commit format
        run: |
          # Check conventional commits format
          git log --format=%s origin/main..HEAD | \
            grep -E '^(feat|fix|docs|style|refactor|perf|test|chore):'
```

## Troubleshooting

### "No changes to commit"

**Problem**: No uncommitted changes found

**Solution**:
```bash
# Check git status
git status

# Make sure you have changes
echo "test" >> README.md
commit
```

### "API key not found"

**Problem**: Missing or incorrect API key

**Solution**:
```bash
# Set API key
export ANTHROPIC_API_KEY=sk-ant-...

# Or for other providers
export OPENAI_API_KEY=sk-...
```

See [Troubleshooting - API Errors](/troubleshooting#api-key-errors).

### Commit messages are too vague

**Problem**: Generated messages lack detail

**Solutions**:
1. **Make focused commits** - one logical change
2. **Add code comments** explaining changes
3. **Use better model**:
   ```bash
   export BETTER_COMMIT_MODEL=claude-sonnet-4-5-20250514
   ```
4. **Customize prompt** with more specific guidelines

### Commit messages are too long

**Problem**: First line exceeds 50 characters

**Solution**: Edit prompt to emphasize brevity:
```markdown
# In tools/commit_changes/PROMPT.md
- First line MUST be ≤50 characters (STRICT)
- Be extremely concise
```

## Advanced Usage

### Batch Commits

For multiple independent changes:

```bash
# Commit each change separately
git add src/feature1.py
BETTER_COMMIT_MODEL=gpt-3.5-turbo commit

git add src/feature2.py
BETTER_COMMIT_MODEL=gpt-3.5-turbo commit
```

**Note**: This doesn't use `git add -A`, so adjust the tool or stage manually.

### Custom Prompt Per Project

```bash
# Use direnv for project-specific prompts
cd /path/to/project

cat > .envrc <<EOF
# Point to custom prompt
export COMMIT_PROMPT_PATH=/path/to/custom/PROMPT.md
EOF

direnv allow
```

**Note**: Requires modifying tool to support `COMMIT_PROMPT_PATH`.

### Generate Without Committing

Currently not supported. The tool always creates a commit. Future enhancement could add a `--dry-run` flag.

## Examples

### New Feature

**Changes**:
```python
# src/auth.py
def authenticate(username, password):
    """Verify user credentials."""
    return verify_password(username, password)
```

**Generated Message**:
```
feat: add user authentication function

Implements password verification for user login
```

### Bug Fix

**Changes**:
```python
# src/api.py
-return data.user
+return data.get('user', None)
```

**Generated Message**:
```
fix: handle missing user field in API response
```

### Refactoring

**Changes**:
```python
# src/utils.py
-def process(data):
-    result = []
-    for item in data:
-        result.append(transform(item))
-    return result
+def process(data):
+    return [transform(item) for item in data]
```

**Generated Message**:
```
refactor: simplify data processing with list comprehension
```

## Related Documentation

- [Tools Overview](/tools/) - All available tools
- [Review Tool](/tools/review) - Code review before commit
- [Commit Prompt](/tools/commit-prompt) - View/edit the AI prompt
- [API Providers](/reference/api-providers) - Model selection
- [Configuration](/configuration) - Customize behavior

## See Also

- [Conventional Commits](https://www.conventionalcommits.org/) - Commit format specification
- [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/) - Best practices guide
