---
title: Installation
description: Complete installation guide for Best Commits tools
---

Best Commits provides AI-powered Git workflow automation through two main tools: `commit` for generating commit messages and `review` for code reviews.

## Prerequisites

Before installing, ensure you have:

1. **uv** - Fast Python package installer and manager
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Windows (PowerShell)
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Git** - Version control system (usually pre-installed)
   ```bash
   git --version
   ```

3. **API Key** - From your chosen AI provider (see [API Providers](/reference/api-providers))

## Quick Install

### Clone the Repository

```bash
git clone https://github.com/yourusername/best-commits.git
cd best-commits
```

### Run the Installer

Install both tools globally:

```bash
./scripts/install-tool.sh
```

Or install individual tools:

```bash
# Install only the commit tool
./scripts/install-tool.sh commit

# Install only the review tool
./scripts/install-tool.sh review
```

### Add to PATH

The installer creates symlinks in `~/.local/bin/`. Ensure this directory is in your PATH:

```bash
# Check if already in PATH
echo $PATH | grep -q "$HOME/.local/bin" && echo "Already in PATH" || echo "Not in PATH"

# Add to PATH (add to ~/.bashrc, ~/.zshrc, or equivalent)
export PATH="$HOME/.local/bin:$PATH"

# Reload shell configuration
source ~/.bashrc  # or ~/.zshrc
```

### Configure API Key

Set your API key for the default provider (Anthropic):

```bash
export ANTHROPIC_API_KEY=your_api_key_here

# Or use the legacy variable
export GIT_API_KEY=your_api_key_here
```

For other providers, see the [API Providers guide](/reference/api-providers).

## Verify Installation

```bash
# Check that commands are available
which commit
which review

# Try running in a git repository
cd /path/to/your/git/repo
commit --help  # Should show usage info
```

## Installation Locations

The installer creates these files:

- **Symlinks**: `~/.local/bin/commit` → `<repo>/tools/commit_changes/__main__.py`
- **Symlinks**: `~/.local/bin/review` → `<repo>/tools/review_changes/__main__.py`
- **Source**: Original files remain in the cloned repository

This means you can:
- Update tools with `git pull` in the repository
- Modify prompts in `tools/*/PROMPT.md` and changes take effect immediately
- Uninstall by removing symlinks

## Updating

To update to the latest version:

```bash
cd best-commits
git pull origin main
# Symlinks automatically point to updated files
```

## Uninstalling

To remove the installed tools:

```bash
cd best-commits

# Remove all tools
./scripts/install-tool.sh uninstall

# Or remove individual tools
./scripts/install-tool.sh uninstall commit
./scripts/install-tool.sh uninstall review
```

## Alternative: Direct Usage (Without Installation)

You can use the tools without installing globally:

```bash
# From the best-commits directory
uv run tools/commit_changes/__main__.py
uv run tools/review_changes/__main__.py

# From any directory (use absolute path)
uv run /path/to/best-commits/tools/commit_changes/__main__.py
```

This is useful for:
- Testing before installing
- Running specific versions
- CI/CD environments

## Next Steps

- [Configure environment variables](/configuration)
- [Set up API providers](/reference/api-providers)
- [Troubleshoot common issues](/troubleshooting)
- [Learn about the tools](/tools/commit)
