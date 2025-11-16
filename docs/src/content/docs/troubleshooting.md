---
title: Troubleshooting
description: Common issues and solutions for Best Commits tools
---

This guide covers common issues you might encounter and how to resolve them.

## Installation Issues

### Command not found: `commit` or `review`

**Problem**: After installation, running `commit` or `review` shows "command not found"

**Solutions**:

1. **Check if `~/.local/bin` is in your PATH**:
   ```bash
   echo $PATH | grep -q "$HOME/.local/bin" && echo "In PATH" || echo "Not in PATH"
   ```

2. **Add to PATH** (if not present):
   ```bash
   # For bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc

   # For zsh
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc

   # For fish
   fish_add_path ~/.local/bin
   ```

3. **Verify symlinks exist**:
   ```bash
   ls -la ~/.local/bin/commit
   ls -la ~/.local/bin/review
   ```

4. **Reinstall if needed**:
   ```bash
   cd best-commits
   ./scripts/install-tool.sh uninstall
   ./scripts/install-tool.sh
   ```

### Permission denied when running installer

**Problem**: `./scripts/install-tool.sh` fails with permission denied

**Solution**:
```bash
chmod +x scripts/install-tool.sh
./scripts/install-tool.sh
```

### `uv` command not found

**Problem**: Installation script fails because `uv` is not installed

**Solution**:
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Reload shell
source ~/.bashrc  # or ~/.zshrc

# Verify installation
uv --version
```

## Runtime Issues

### API Key Errors

#### Error: "No API key found"

**Problem**: Tool can't find your API key

**Solutions**:

1. **Set the appropriate environment variable**:
   ```bash
   # For Anthropic (default)
   export ANTHROPIC_API_KEY=sk-ant-...

   # Or legacy variable
   export GIT_API_KEY=sk-ant-...
   ```

2. **Make it persistent** (add to shell rc file):
   ```bash
   # For bash
   echo 'export ANTHROPIC_API_KEY=sk-ant-...' >> ~/.bashrc

   # For zsh
   echo 'export ANTHROPIC_API_KEY=sk-ant-...' >> ~/.zshrc
   ```

3. **Verify it's set**:
   ```bash
   echo $ANTHROPIC_API_KEY
   ```

#### Error: "Invalid API key"

**Problem**: API key is malformed or incorrect

**Solutions**:

1. **Check for extra spaces or quotes**:
   ```bash
   # Wrong
   export ANTHROPIC_API_KEY=" sk-ant-... "

   # Correct
   export ANTHROPIC_API_KEY=sk-ant-...
   ```

2. **Get a new key** from your provider:
   - Anthropic: https://console.anthropic.com
   - OpenAI: https://platform.openai.com/api-keys
   - xAI: https://console.x.ai/

3. **Check the key format**:
   - Anthropic: starts with `sk-ant-`
   - OpenAI: starts with `sk-`
   - xAI: starts with `xai-`

### Model-Related Errors

#### Error: "Model not found" or "Invalid model"

**Problem**: The specified model doesn't exist or isn't accessible

**Solutions**:

1. **Check model name format**:
   ```bash
   # Some providers require prefixes
   export BETTER_COMMIT_MODEL=xai/grok-beta  # xAI requires xai/ prefix
   export BETTER_COMMIT_MODEL=gemini/gemini-pro  # Google requires gemini/
   ```

2. **Verify model availability**:
   - Check [LiteLLM providers docs](https://docs.litellm.ai/docs/providers)
   - Ensure your API key has access to the model
   - Some models require special access or billing setup

3. **Test with default model**:
   ```bash
   # Unset custom model to use default
   unset BETTER_COMMIT_MODEL
   ```

#### Error: Rate limit exceeded

**Problem**: Too many API requests in a short time

**Solutions**:

1. **Wait a few moments** and try again
2. **Check your API plan** - you may need to upgrade
3. **Use a different model** with higher rate limits:
   ```bash
   export BETTER_COMMIT_MODEL=claude-haiku-4-5-20251001  # Default, high limits
   ```

### Git-Related Errors

#### Error: "Not a git repository"

**Problem**: Running the command outside a git repository

**Solution**:
```bash
# Initialize git if needed
git init

# Or navigate to a git repository
cd /path/to/your/git/repo
```

#### Error: "No changes to commit"

**Problem**: No uncommitted changes found

**Solution**:
```bash
# Make some changes first
echo "test" >> README.md

# Verify changes exist
git status
```

#### Error: "Git command failed"

**Problem**: Underlying git operation failed

**Solutions**:

1. **Check git is installed**:
   ```bash
   git --version
   ```

2. **Check git configuration**:
   ```bash
   git config --global user.name
   git config --global user.email

   # Set if missing
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```

3. **Check repository health**:
   ```bash
   git status
   git fsck
   ```

### Network Errors

#### Error: "Connection timeout" or "Network error"

**Problem**: Can't reach API endpoint

**Solutions**:

1. **Check internet connection**:
   ```bash
   ping api.anthropic.com
   ```

2. **Check for proxy settings**:
   ```bash
   echo $HTTP_PROXY
   echo $HTTPS_PROXY
   ```

3. **Try a different network** (e.g., disable VPN)

4. **Check API status pages**:
   - Anthropic: https://status.anthropic.com
   - OpenAI: https://status.openai.com

## Debug Mode

### Enable verbose output

For more detailed error information:

```bash
# Run with Python's verbose mode
python3 -v $(which commit)

# Or directly with uv
uv run --verbose tools/commit_changes/__main__.py
```

### Check Python dependencies

```bash
# List installed dependencies
uv pip list

# Reinstall dependencies
uv pip install --force-reinstall litellm rich
```

## Common Workflow Issues

### Review tool doesn't show expected issues

**Problem**: Code review misses obvious problems

**Causes**:
- Lock files not filtered (working as designed)
- Model limitations
- Diff too large

**Solutions**:
1. **Check what's being reviewed**:
   ```bash
   git diff
   git diff --staged
   ```

2. **Try a more powerful model**:
   ```bash
   export BETTER_COMMIT_MODEL=claude-sonnet-4-5-20250514
   ```

3. **Review smaller changesets** - break up large changes

### Commit messages are generic

**Problem**: Generated commit messages lack detail

**Solutions**:

1. **Make focused changes** - one logical change per commit
2. **Add descriptive code comments** before committing
3. **Use review tool first** to get context
4. **Try a different model**:
   ```bash
   export BETTER_COMMIT_MODEL=gpt-4o
   ```

## Getting Help

If you're still stuck:

1. **Check existing docs**:
   - [Configuration](/configuration)
   - [API Providers](/reference/api-providers)
   - [FAQ](/reference/faq)

2. **Search for similar issues**:
   - GitHub Issues: https://github.com/yourusername/best-commits/issues

3. **Create a new issue** with:
   - Your OS and version
   - Python version (`python3 --version`)
   - uv version (`uv --version`)
   - Error message (full output)
   - Steps to reproduce

4. **Check logs** (if available):
   ```bash
   # Check recent shell history
   history | grep commit
   history | grep review
   ```
