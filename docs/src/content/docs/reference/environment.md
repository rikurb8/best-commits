---
title: Environment Variables
description: Complete reference of all environment variables
---

This page documents all environment variables used by Best Commits tools.

## API Authentication

### Provider API Keys

| Variable | Provider | Format | Required |
|----------|----------|--------|----------|
| `ANTHROPIC_API_KEY` | Anthropic Claude | `sk-ant-api03-...` | For Claude models |
| `OPENAI_API_KEY` | OpenAI | `sk-...` | For GPT models |
| `XAI_API_KEY` | xAI Grok | `xai-...` | For Grok models |
| `GEMINI_API_KEY` | Google Gemini | varies | For Gemini models |
| `COHERE_API_KEY` | Cohere | varies | For Command models |
| `MISTRAL_API_KEY` | Mistral AI | varies | For Mistral models |
| `GIT_API_KEY` | Legacy Anthropic | `sk-ant-...` | Legacy support only |

**Notes**:
- Only one API key is required based on your chosen model
- `GIT_API_KEY` is deprecated but still works for backwards compatibility
- Multiple keys can be set for switching between providers

**Examples**:
```bash
# Anthropic (recommended)
export ANTHROPIC_API_KEY=sk-ant-api03-xxx

# OpenAI
export OPENAI_API_KEY=sk-xxx

# xAI
export XAI_API_KEY=xai-xxx
```

## Model Configuration

### BETTER_COMMIT_MODEL

Specifies which AI model to use for both `commit` and `review` tools.

**Default**: `claude-haiku-4-5-20251001`

**Format**: Depends on provider (some require prefixes)

**Examples**:
```bash
# Anthropic (no prefix needed)
export BETTER_COMMIT_MODEL=claude-haiku-4-5-20251001
export BETTER_COMMIT_MODEL=claude-sonnet-4-5-20250514
export BETTER_COMMIT_MODEL=claude-opus-4-20250514

# OpenAI (no prefix needed)
export BETTER_COMMIT_MODEL=gpt-4o
export BETTER_COMMIT_MODEL=gpt-4-turbo
export BETTER_COMMIT_MODEL=gpt-3.5-turbo

# xAI (requires xai/ prefix)
export BETTER_COMMIT_MODEL=xai/grok-beta

# Google (requires gemini/ prefix)
export BETTER_COMMIT_MODEL=gemini/gemini-pro
export BETTER_COMMIT_MODEL=gemini/gemini-flash

# Cohere (prefix recommended)
export BETTER_COMMIT_MODEL=cohere/command-r-plus

# Mistral (requires mistral/ prefix)
export BETTER_COMMIT_MODEL=mistral/mistral-large-latest
```

**Validation**:
- Model name must be recognized by LiteLLM
- Corresponding API key must be set
- Model must be accessible with your API plan

## Shell Configuration

### PATH

Best Commits installs to `~/.local/bin/`, which must be in your PATH.

**Check**:
```bash
echo $PATH | grep -q "$HOME/.local/bin" && echo "OK" || echo "Not in PATH"
```

**Add to PATH**:
```bash
# Bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# Zsh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc

# Fish
fish_add_path ~/.local/bin
```

## Optional: Development Variables

These are not used by the tools but may be helpful for development:

### ANTHROPIC_LOG

Enable debug logging for Anthropic API calls:

```bash
export ANTHROPIC_LOG=debug
```

### OPENAI_LOG

Enable debug logging for OpenAI API calls:

```bash
export OPENAI_LOG=debug
```

## Complete Configuration Example

**Minimal setup** (Anthropic):
```bash
export ANTHROPIC_API_KEY=sk-ant-api03-xxx
```

**Optimized setup** (multiple providers):
```bash
# API Keys
export ANTHROPIC_API_KEY=sk-ant-api03-xxx
export OPENAI_API_KEY=sk-xxx
export XAI_API_KEY=xai-xxx

# Default model
export BETTER_COMMIT_MODEL=claude-haiku-4-5-20251001

# PATH (if not already set)
export PATH="$HOME/.local/bin:$PATH"
```

**Advanced setup** (aliases for different use cases):
```bash
# API Keys
export ANTHROPIC_API_KEY=sk-ant-api03-xxx
export OPENAI_API_KEY=sk-xxx

# Aliases for different models
alias commit-fast='BETTER_COMMIT_MODEL=gpt-3.5-turbo commit'
alias commit-quality='BETTER_COMMIT_MODEL=claude-sonnet-4-5-20250514 commit'
alias review-deep='BETTER_COMMIT_MODEL=claude-opus-4-20250514 review'

# Work vs personal
alias work-commit='ANTHROPIC_API_KEY=$WORK_API_KEY commit'
alias personal-commit='ANTHROPIC_API_KEY=$PERSONAL_API_KEY commit'
```

## Precedence Rules

When multiple configuration sources are present:

1. **Per-command variables** (highest priority)
   ```bash
   BETTER_COMMIT_MODEL=gpt-4o commit
   ```

2. **Session exports**
   ```bash
   export BETTER_COMMIT_MODEL=claude-haiku-4-5-20251001
   ```

3. **Shell RC files**
   ```bash
   # ~/.bashrc or ~/.zshrc
   export BETTER_COMMIT_MODEL=claude-haiku-4-5-20251001
   ```

4. **Defaults** (lowest priority)
   - Model: `claude-haiku-4-5-20251001`

## Validation Commands

### Check All Variables

```bash
# Show all relevant environment variables
env | grep -E "(API_KEY|BETTER_COMMIT|PATH)" | grep -v "="

# Safer: Show variables without exposing keys
env | grep -E "(API_KEY|BETTER_COMMIT)" | sed 's/=.*/=***/'
```

### Test Configuration

```bash
# Quick test in a temporary repository
cd /tmp
git init test-config
cd test-config
echo "test" > README.md
git add .
commit  # Should generate commit message
```

## Security Considerations

### Protecting API Keys

1. **Never print API keys**:
   ```bash
   # Wrong - exposes key in shell history
   echo $ANTHROPIC_API_KEY

   # Better - mask the value
   env | grep ANTHROPIC_API_KEY | sed 's/=.*/=***/'
   ```

2. **Never commit to git**:
   ```bash
   # Add to .gitignore
   echo '.env' >> .gitignore
   echo '.envrc' >> .gitignore
   ```

3. **Use file permissions**:
   ```bash
   # Protect your shell RC file
   chmod 600 ~/.bashrc
   chmod 600 ~/.zshrc
   ```

4. **Rotate regularly**:
   - Generate new keys monthly
   - Revoke compromised keys immediately

### Environment File Pattern

**Create `.env` file** (git-ignored):
```bash
# .env
export ANTHROPIC_API_KEY=sk-ant-xxx
export BETTER_COMMIT_MODEL=claude-haiku-4-5-20251001
```

**Source it**:
```bash
# In ~/.bashrc or manually
source /path/to/.env
```

**Protect it**:
```bash
chmod 600 .env
echo '.env' >> .gitignore
```

## Platform-Specific Notes

### macOS

```bash
# Add to ~/.zshrc (default shell since Catalina)
export ANTHROPIC_API_KEY=sk-ant-xxx
```

### Linux

```bash
# Add to ~/.bashrc or ~/.zshrc depending on shell
export ANTHROPIC_API_KEY=sk-ant-xxx
```

### Windows (WSL)

```bash
# Add to ~/.bashrc
export ANTHROPIC_API_KEY=sk-ant-xxx

# Note: Windows environment variables don't transfer to WSL
```

### Windows (PowerShell)

```powershell
# Session-level
$env:ANTHROPIC_API_KEY = "sk-ant-xxx"

# Persistent (user-level)
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-xxx", "User")
```

## Troubleshooting

### Variable Not Set

**Symptom**: "No API key found" error

**Check**:
```bash
echo $ANTHROPIC_API_KEY
# Should show your key, not empty
```

**Fix**:
```bash
export ANTHROPIC_API_KEY=sk-ant-xxx
source ~/.bashrc  # or ~/.zshrc
```

### Wrong Model Name

**Symptom**: "Model not found" error

**Check**:
```bash
echo $BETTER_COMMIT_MODEL
```

**Fix**: Ensure model name matches provider format:
```bash
# xAI requires prefix
export BETTER_COMMIT_MODEL=xai/grok-beta

# Gemini requires prefix
export BETTER_COMMIT_MODEL=gemini/gemini-pro
```

### PATH Issues

**Symptom**: "command not found: commit"

**Check**:
```bash
echo $PATH | grep -q "$HOME/.local/bin" && echo "OK" || echo "Missing"
```

**Fix**:
```bash
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## See Also

- [Configuration Guide](/configuration) - Higher-level configuration guide
- [API Providers](/reference/api-providers) - Provider-specific setup
- [Troubleshooting](/troubleshooting) - Common issues and solutions
