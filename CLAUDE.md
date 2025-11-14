# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a collection of standalone Python scripts for Git workflow automation. Each script is a single-file executable that uses `uv` for dependency management via PEP 723 inline script metadata. Scripts are designed to be installed globally and run from any git repository.

**Current Scripts:**
- `commit-changes.py`: AI-powered commit message generator using Claude Haiku 4.5

## Architecture

### Single-File Script Pattern
All scripts follow this structure:
- **Shebang**: `#!/usr/bin/env -S uvx --quiet --with <deps>` for direct execution
- **PEP 723 metadata block**: Inline dependency declarations between `# /// script` markers
- **Imports**: Standard library + dependencies listed in metadata
- **Helper functions**: Git operations, API calls, etc.
- **main()**: Entry point with error handling and Rich console output

### Key Patterns
- **Git operations**: Use `subprocess.run(["git", ...], capture_output=True, text=True, check=True)`
- **Terminal UI**: Use `rich.console.Console` for colored output, panels, and formatting
- **API integration**: Scripts that use AI models read API keys from environment variables (e.g., `GIT_API_KEY` for Anthropic)
- **Error handling**: Catch `subprocess.CalledProcessError` and `ValueError`, print user-friendly messages via Rich console

### Commit Script Flow
1. Check for uncommitted changes (`git status --porcelain`)
2. Collect diff data (status, unstaged diff, staged diff)
3. Stage all changes with `git add -A`
4. Send diffs to Claude API with commit message generation prompt
5. Strip any markdown formatting from response
6. Create commit with `git commit -m <message>`

## Development Commands

### Testing Scripts
```bash
# Run script directly with uv
uv run commit-changes.py

# Test from another git repository
cd /path/to/test/repo
uv run /Users/riku/projects/best-commits/commit-changes.py
```

### Adding Dependencies
Update the PEP 723 metadata block in the script file:
```python
# /// script
# dependencies = [
#   "anthropic>=0.40.0",
#   "rich>=13.0.0",
# ]
# ///
```

No separate `pip install` needed - `uv` handles dependency resolution at runtime.

### Making Scripts Executable
```bash
chmod +x your-script.py
```

## Environment Variables

- `GIT_API_KEY`: Anthropic API key for Claude access (required for commit script)
- `BETTER_COMMIT_MODEL`: (Planned) Allow specifying alternative AI models via LiteLLM

## Code Style

- Use conventional commit prefixes (feat:, fix:, docs:, refactor:, test:, chore:)
- Follow imperative mood in commit messages ("Add feature" not "Added feature")
- Keep first line of commits ≤50 characters
- Use Rich console for all user-facing output with appropriate color coding:
  - cyan: informational/progress messages
  - yellow: warnings
  - green: success
  - red: errors

## Future Development

See `specs/01-review-functionality.md` for planned `review` command which will analyze uncommitted changes and provide feedback before committing.
