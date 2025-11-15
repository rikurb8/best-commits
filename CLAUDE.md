# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a collection of standalone Python scripts for Git workflow automation. Each script is a single-file executable that uses `uv` for dependency management via PEP 723 inline script metadata. Scripts are designed to be installed globally and run from any git repository.

**Current Scripts:**
- `commit-changes.py`: AI-powered commit message generator (default: Claude Haiku 4.5, supports multiple models via LiteLLM)
- `review-changes.py`: AI-powered code review for uncommitted changes, with optional commit flow (supports multiple models via LiteLLM)

## Architecture

### Single-File Script Pattern
All scripts follow this structure:
- **Shebang**: `#!/usr/bin/env -S uvx --quiet --with <deps>` for direct execution
- **PEP 723 metadata block**: Inline dependency declarations between `# /// script` markers
- **Imports**: Standard library + dependencies listed in metadata
- **Helper functions**: Git operations, API calls, model selection, etc.
- **main()**: Entry point with error handling and Rich console output

### Key Patterns
- **Git operations**: Use `subprocess.run(["git", ...], capture_output=True, text=True, check=True)`
- **Terminal UI**: Use `rich.console.Console` for colored output, panels, and formatting
- **AI model integration**:
  - Uses LiteLLM for unified API access across multiple providers
  - Model selection via `BETTER_COMMIT_MODEL` environment variable (defaults to `claude-haiku-4-5-20251001`)
  - API keys read from provider-specific environment variables (e.g., `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `XAI_API_KEY`)
  - Backwards compatibility: `GIT_API_KEY` still supported for Anthropic models
- **Error handling**: Catch `subprocess.CalledProcessError` and `ValueError`, print user-friendly messages via Rich console

### Commit Script Flow
1. Setup API keys for backwards compatibility
2. Check for uncommitted changes (`git status --porcelain`)
3. Collect diff data (status, unstaged diff, staged diff)
4. Stage all changes with `git add -A`
5. Get model name from `BETTER_COMMIT_MODEL` or use default
6. Send diffs to AI model via LiteLLM with commit message generation prompt
7. Strip any markdown formatting from response
8. Create commit with `git commit -m <message>`

### Review Script Flow
1. Setup API keys for backwards compatibility
2. Check for uncommitted changes (`git status --porcelain`)
3. Collect diff data (status, unstaged diff, staged diff)
4. Filter out lock files and other noise (package-lock.json, etc.)
5. Get model name from `BETTER_COMMIT_MODEL` or use default
6. Send diffs to AI model via LiteLLM with code review prompt
7. Display review feedback with summary, issues, suggestions, and breaking changes
8. Prompt user to proceed with commit (y/n)
9. If yes, chain to `commit-changes.py` for message generation and commit

## Development Commands

### Testing Scripts
```bash
# Run scripts directly with uv
uv run commit-changes.py
uv run review-changes.py

# Test from another git repository
cd /path/to/test/repo
uv run /Users/riku/projects/best-commits/commit-changes.py
uv run /Users/riku/projects/best-commits/review-changes.py
```

### Adding Dependencies
Update the PEP 723 metadata block in the script file:
```python
# /// script
# dependencies = [
#   "litellm>=1.0.0",
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

### Model Selection
- `BETTER_COMMIT_MODEL`: Specifies which AI model to use (defaults to `claude-haiku-4-5-20251001`)

### API Keys
Different providers require different API key environment variables:
- `ANTHROPIC_API_KEY`: For Anthropic Claude models
- `OPENAI_API_KEY`: For OpenAI GPT models
- `XAI_API_KEY`: For xAI Grok models
- `GEMINI_API_KEY`: For Google Gemini models
- `COHERE_API_KEY`: For Cohere models
- `MISTRAL_API_KEY`: For Mistral models
- `GIT_API_KEY`: Legacy variable for Anthropic models (still supported for backwards compatibility)

See README.md for complete list of supported providers and their configuration.

## Code Style

- Use conventional commit prefixes (feat:, fix:, docs:, refactor:, test:, chore:)
- Follow imperative mood in commit messages ("Add feature" not "Added feature")
- Keep first line of commits ≤50 characters
- Use Rich console for all user-facing output with appropriate color coding:
  - cyan: informational/progress messages
  - yellow: warnings
  - green: success
  - red: errors

## Workflow Recommendations

For best results, use the review script before committing:
1. Make your changes
2. Run `uv run review-changes.py` to get AI feedback
3. Address any issues or suggestions
4. Proceed with commit when prompted (or run `commit-changes.py` separately)
