---
title: Configuration
description: Configure Best Commits tools for your workflow
---

Best Commits tools are designed to work with minimal configuration, but offer customization options for advanced users.

## Quick Start

The minimal configuration needed:

```bash
# 1. Set API key
export ANTHROPIC_API_KEY=sk-ant-...

# 2. Run from any git repo
cd /path/to/your/project
commit
```

That's it! The tools use sensible defaults for everything else.

## Configuration Methods

Configuration is done entirely through environment variables. There are three ways to set them:

### 1. Session-Level (Temporary)

Set for the current terminal session only:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export BETTER_COMMIT_MODEL=claude-haiku-4-5-20251001
```

### 2. Persistent (Recommended)

Add to your shell configuration file:

```bash
# For bash
echo 'export ANTHROPIC_API_KEY=sk-ant-...' >> ~/.bashrc
source ~/.bashrc

# For zsh
echo 'export ANTHROPIC_API_KEY=sk-ant-...' >> ~/.zshrc
source ~/.zshrc

# For fish
set -Ux ANTHROPIC_API_KEY sk-ant-...
```

### 3. Per-Command (One-Time)

Set for a single command execution:

```bash
BETTER_COMMIT_MODEL=gpt-4o commit
BETTER_COMMIT_MODEL=claude-opus-4-20250514 review
```

## Core Settings

### API Authentication

**Required**: One of these API key variables based on your chosen provider:

```bash
# Anthropic (default)
export ANTHROPIC_API_KEY=sk-ant-...

# OpenAI
export OPENAI_API_KEY=sk-...

# xAI
export XAI_API_KEY=xai-...

# Google Gemini
export GEMINI_API_KEY=...

# Cohere
export COHERE_API_KEY=...

# Mistral
export MISTRAL_API_KEY=...

# Legacy (Anthropic only)
export GIT_API_KEY=sk-ant-...
```

See [API Providers](/reference/api-providers) for detailed setup.

### Model Selection

**Optional**: Specify which AI model to use (defaults to `claude-haiku-4-5-20251001`):

```bash
export BETTER_COMMIT_MODEL=claude-haiku-4-5-20251001  # Default
export BETTER_COMMIT_MODEL=gpt-4o                      # OpenAI
export BETTER_COMMIT_MODEL=xai/grok-beta              # xAI
export BETTER_COMMIT_MODEL=gemini/gemini-pro          # Google
```

**Note**: Some providers require a prefix (e.g., `xai/`, `gemini/`).

## Advanced Configuration

### Prompt Customization

You can modify the AI prompts used by the tools:

**Location**:
- Commit tool: `tools/commit_changes/PROMPT.md`
- Review tool: `tools/review_changes/PROMPT.md`
- Scoring system: `tools/review_changes/SCORING_SYSTEM.md`

**To customize**:

```bash
# 1. Navigate to the best-commits repository
cd /path/to/best-commits

# 2. Edit the prompt file
nano tools/commit_changes/PROMPT.md

# 3. Changes take effect immediately (prompts are loaded at runtime)
commit  # Will use your modified prompt
```

**Tips for customization**:
- Keep the overall structure intact
- Modify examples and guidelines
- Add project-specific requirements
- Test thoroughly with different change types

### Multiple Configurations

Use shell aliases to maintain different configurations:

```bash
# Add to ~/.bashrc or ~/.zshrc

# Work projects (company API key, strict reviews)
alias work-commit='ANTHROPIC_API_KEY=$WORK_API_KEY commit'
alias work-review='ANTHROPIC_API_KEY=$WORK_API_KEY BETTER_COMMIT_MODEL=claude-opus-4-20250514 review'

# Personal projects (personal API key, fast commits)
alias personal-commit='ANTHROPIC_API_KEY=$PERSONAL_API_KEY commit'
alias personal-review='ANTHROPIC_API_KEY=$PERSONAL_API_KEY review'

# Quick commits (cheap model)
alias quick-commit='BETTER_COMMIT_MODEL=gpt-3.5-turbo commit'

# Thorough review (powerful model)
alias deep-review='BETTER_COMMIT_MODEL=claude-opus-4-20250514 review'
```

## Project-Specific Configuration

### Directory-Level Settings

Use `direnv` for project-specific environment variables:

```bash
# 1. Install direnv
# macOS: brew install direnv
# Linux: apt-get install direnv

# 2. Add to shell rc file
eval "$(direnv hook bash)"  # or zsh

# 3. Create .envrc in project root
cd /path/to/project
cat > .envrc <<EOF
export BETTER_COMMIT_MODEL=gpt-4o
export OPENAI_API_KEY=\$PERSONAL_OPENAI_KEY
EOF

# 4. Allow the directory
direnv allow

# 5. Settings auto-apply when entering the directory
cd /path/to/project  # Settings activated
cd ~                 # Settings deactivated
```

### Git Hooks Integration

Optionally integrate with git hooks:

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Run review before allowing commit
review || exit 1
```

**Note**: This requires manual intervention for each commit.

## Environment-Specific Settings

### Development vs Production

```bash
# Development: Use fast, cheap model
export DEV_MODEL=claude-haiku-4-5-20251001

# Production: Use quality model for release commits
export PROD_MODEL=claude-opus-4-20250514

# Aliases
alias dev-commit='BETTER_COMMIT_MODEL=$DEV_MODEL commit'
alias prod-commit='BETTER_COMMIT_MODEL=$PROD_MODEL commit'
```

### CI/CD Configuration

For use in CI/CD pipelines:

```yaml
# Example: GitHub Actions
name: AI Commit Check
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Review changes
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          BETTER_COMMIT_MODEL: claude-haiku-4-5-20251001
        run: |
          git clone https://github.com/yourusername/best-commits.git
          uv run best-commits/tools/review_changes/__main__.py
```

## Token Limits

The tools use these default token limits:

| Tool   | Max Tokens | Purpose                 |
|--------|-----------|-------------------------|
| commit | 1024      | Generate commit message |
| review | 2048      | Detailed code review    |

These are hardcoded but can be modified by editing the source code:

```python
# In tools/commit_changes/main.py or tools/review_changes/main.py
response = completion(
    model=model_name,
    messages=[...],
    max_tokens=1024,  # Modify this value
)
```

## Performance Tuning

### Response Speed

Faster models for quick commits:

```bash
export BETTER_COMMIT_MODEL=gpt-3.5-turbo      # Fastest
export BETTER_COMMIT_MODEL=claude-haiku-4-5-20251001  # Fast
export BETTER_COMMIT_MODEL=gemini/gemini-flash # Fast
```

### Response Quality

Higher quality for important reviews:

```bash
export BETTER_COMMIT_MODEL=claude-opus-4-20250514  # Best
export BETTER_COMMIT_MODEL=gpt-4o              # Excellent
export BETTER_COMMIT_MODEL=claude-sonnet-4-5-20250514  # Great
```

### Cost Optimization

See [API Providers - Cost Optimization](/reference/api-providers#cost-optimization) for strategies.

## Configuration Validation

### Check Your Setup

```bash
# Verify environment variables are set
env | grep -E "(API_KEY|BETTER_COMMIT)"

# Expected output (example):
# ANTHROPIC_API_KEY=sk-ant-...
# BETTER_COMMIT_MODEL=claude-haiku-4-5-20251001

# Test in a git repository
cd /tmp
git init test-repo
cd test-repo
echo "test" > README.md
git add .
commit  # Should work without errors
```

### Common Configuration Mistakes

1. **Wrong variable name**
   ```bash
   # Wrong
   export CLAUDE_API_KEY=sk-ant-...

   # Correct
   export ANTHROPIC_API_KEY=sk-ant-...
   ```

2. **Extra spaces or quotes**
   ```bash
   # Wrong
   export ANTHROPIC_API_KEY=" sk-ant-... "

   # Correct
   export ANTHROPIC_API_KEY=sk-ant-...
   ```

3. **Missing model prefix**
   ```bash
   # Wrong
   export BETTER_COMMIT_MODEL=grok-beta

   # Correct
   export BETTER_COMMIT_MODEL=xai/grok-beta
   ```

## Security Best Practices

### API Key Protection

1. **Never commit API keys** to version control
   ```bash
   # Add to .gitignore
   echo '.env' >> .gitignore
   echo '.envrc' >> .gitignore
   ```

2. **Use environment files**
   ```bash
   # Create .env (git-ignored)
   echo 'export ANTHROPIC_API_KEY=sk-ant-...' > .env

   # Source in shell
   source .env
   ```

3. **Rotate keys regularly**
   - Generate new keys monthly
   - Revoke old keys immediately if compromised

4. **Use different keys** for different contexts
   ```bash
   export WORK_API_KEY=sk-ant-work-...
   export PERSONAL_API_KEY=sk-ant-personal-...
   ```

### Sensitive Projects

For sensitive codebases:

1. **Use self-hosted models** (future feature)
2. **Review prompts carefully** to ensure no sensitive data leaks
3. **Consider local-only commit messages** without AI
4. **Audit API logs** for your provider

## Troubleshooting Configuration

See the [Troubleshooting Guide](/troubleshooting) for common configuration issues.

## Next Steps

- [API Providers Guide](/reference/api-providers) - Detailed provider setup
- [Environment Variables Reference](/reference/environment) - Complete variable list
- [Tools Documentation](/tools/commit) - Learn about the tools
- [FAQ](/reference/faq) - Common questions
