# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a collection of Python tools for Git workflow automation, organized as modules under the `tools/` directory. Each tool can be run as a Python module and uses `uv` for dependency management via PEP 723 inline script metadata. Tools are designed to be installed globally and run from any git repository.

**Current Tools:**
- `tools.commit_changes`: AI-powered commit message generator (default: Claude Haiku 4.5, supports multiple models via LiteLLM)
- `tools.review_changes`: AI-powered code review for uncommitted changes, with optional commit flow (supports multiple models via LiteLLM)

**Legacy Scripts (deprecated):**
- `commit-changes.py`: Standalone version (use `tools.commit_changes` instead)
- `review-changes.py`: Standalone version (use `tools.review_changes` instead)

## Architecture

### Module Structure
Each tool is organized as a Python module under `tools/`:
```
tools/
├── __init__.py
├── commit_changes/
│   ├── __init__.py          # Exports main() function
│   ├── __main__.py          # Module entry point with PEP 723 metadata
│   └── main.py              # Core implementation
└── review_changes/
    ├── __init__.py          # Exports main() function
    ├── __main__.py          # Module entry point with PEP 723 metadata
    └── main.py              # Core implementation
```

### Module Pattern
Each tool module follows this structure:
- **`__main__.py`**: Entry point with shebang and PEP 723 metadata block for `uvx` compatibility
- **`main.py`**: Core implementation with helper functions and main() entry point
- **`__init__.py`**: Exports main() function for module imports
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

## Installation

**Prerequisites**: Only `uv` needs to be installed. All Python dependencies are managed automatically via PEP 723 inline script metadata.

### Global Installation (Recommended)

Install tools globally so you can run `commit` and `review` from any git repository:

```bash
# Clone the repository
git clone https://github.com/yourusername/best-commits.git
cd best-commits

# Install all tools (commit and review)
./scripts/install-tool.sh

# Or install individual tools
./scripts/install-tool.sh commit
./scripts/install-tool.sh review
```

This creates symlinks in `~/.local/bin/` pointing to the tool scripts. Make sure `~/.local/bin` is in your PATH:

```bash
# Add to ~/.bashrc, ~/.zshrc, or equivalent
export PATH="$HOME/.local/bin:$PATH"
```

After installation, you can use the tools from any git repository:
```bash
cd /path/to/your/project
commit    # Generate AI-powered commit message
review    # Get AI code review feedback
```

## Development Commands

### Running Tools (Without Installation)
```bash
# Run the __main__.py scripts with uv (recommended)
uv run tools/commit_changes/__main__.py
uv run tools/review_changes/__main__.py

# Or make them executable and run directly
chmod +x tools/commit_changes/__main__.py tools/review_changes/__main__.py
./tools/commit_changes/__main__.py
./tools/review_changes/__main__.py

# Legacy standalone scripts (still work, but deprecated)
uv run commit-changes.py
uv run review-changes.py
```

### Running from Another Git Repository
```bash
# Run from any git repository using absolute path
cd /path/to/your/project
uv run /path/to/best-commits/tools/commit_changes/__main__.py
uv run /path/to/best-commits/tools/review_changes/__main__.py

# Or if made executable
/path/to/best-commits/tools/commit_changes/__main__.py
/path/to/best-commits/tools/review_changes/__main__.py
```

### Adding Dependencies
Update the PEP 723 metadata block in the tool's `__main__.py` file:
```python
# /// script
# dependencies = [
#   "litellm>=1.0.0",
#   "rich>=13.0.0",
# ]
# ///
```

No separate `pip install` needed - `uv` handles dependency resolution at runtime.

### Creating New Tools
1. Create a new directory under `tools/` (e.g., `tools/new_tool/`)
2. Add `__init__.py` that exports `main()`
3. Add `__main__.py` with PEP 723 metadata, shebang (`#!/usr/bin/env -S uv run --script`), and inline implementation
4. Optionally add `main.py` for shared code if the tool is complex
5. Test with: `uv run tools/new_tool/__main__.py`
6. Make executable: `chmod +x tools/new_tool/__main__.py`

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

For best results, use the review tool before committing:
1. Make your changes
2. Run `uv run tools/review_changes/__main__.py` to get AI feedback
3. Address any issues or suggestions
4. Proceed with commit when prompted (or run `uv run tools/commit_changes/__main__.py` separately)
