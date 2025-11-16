# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python package providing Git workflow automation tools, organized as modules under the `tools/` directory. Dependencies are managed via `pyproject.toml` using the standard Python packaging system. Tools are designed to be installed globally via `uv tool install` and run from any git repository.

**Current Tools:**
- `commit`: AI-powered commit message generator (default: Claude Haiku 4.5, supports multiple models via LiteLLM)
- `review`: AI-powered code review for uncommitted changes, with optional commit flow (supports multiple models via LiteLLM)

**Package Name:** `best-commits`
**Version:** `0.2.0`
**Entry Points:** Defined in `pyproject.toml` under `[project.scripts]`

## Architecture

### Module Structure
Each tool is organized as a Python module under `tools/`:
```
tools/
├── __init__.py
├── commit_changes/
│   ├── __init__.py          # Exports main() function
│   ├── __main__.py          # Simple entry point (imports main)
│   ├── main.py              # Core implementation
│   └── PROMPT.md            # AI prompt template
└── review_changes/
    ├── __init__.py          # Exports main() function
    ├── __main__.py          # Simple entry point (imports main)
    ├── main.py              # Core implementation
    ├── PROMPT.md            # AI prompt template
    └── SCORING_SYSTEM.md    # Review scoring guide
```

### Module Pattern
Each tool module follows this structure:
- **`__main__.py`**: Minimal entry point that imports and calls `main()` from the module
- **`main.py`**: Core implementation with helper functions and main() entry point
- **`__init__.py`**: Exports main() function for module imports and entry points
- **Helper functions**: Git operations, API calls, model selection, prompt loading, etc.
- **main()**: Entry point with error handling and Rich console output
- **PROMPT.md**: External prompt templates loaded at runtime

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

**Prerequisites**: Only `uv` needs to be installed. All Python dependencies are managed via `pyproject.toml` and installed automatically in an isolated virtual environment.

### Global Installation (Recommended)

Install the package globally using `uv tool install`:

```bash
# From local repository (clone first)
git clone https://github.com/rikurb8/best-commits.git
cd best-commits
uv tool install .

# Or use the installer script
./scripts/install-tool.sh

# Or directly from GitHub (no cloning needed)
uv tool install git+https://github.com/rikurb8/best-commits.git
```

The `uv tool install` command:
- Creates an isolated virtual environment for the package
- Installs all dependencies automatically
- Adds the `commit` and `review` commands to your PATH
- No manual PATH configuration needed

### Development Installation

For development with editable install (changes reflect immediately):

```bash
cd best-commits
uv tool install --editable .

# Or use the installer script
./scripts/install-tool.sh --editable
```

After installation, use the tools from any git repository:
```bash
cd /path/to/your/project
commit    # Generate AI-powered commit message
review    # Get AI code review feedback
```

### Managing Installation

```bash
# List installed tools
uv tool list

# Upgrade to latest version
uv tool upgrade best-commits

# Uninstall
uv tool uninstall best-commits
```

## Development Commands

### Running Tools (Without Installation)

Use `uvx` to run tools without installing them:

```bash
# From local directory
cd best-commits
uvx --from . commit
uvx --from . review

# Or run as Python modules
uv run -m tools.commit_changes
uv run -m tools.review_changes

# Directly from GitHub (no cloning needed)
uvx --from git+https://github.com/rikurb8/best-commits.git commit
uvx --from git+https://github.com/rikurb8/best-commits.git review
```

### Using Makefile

The project includes a `Makefile` for common development tasks:

```bash
make help          # Show all available commands
make install       # Install normally
make install-dev   # Install in editable mode
make uninstall     # Uninstall the package
make run-commit    # Run commit without installation (uvx)
make run-review    # Run review without installation (uvx)
make clean         # Clean build artifacts
make format        # Format code with black
make lint          # Lint code with ruff
```

### Adding Dependencies

Update the `dependencies` list in `pyproject.toml`:

```toml
[project]
dependencies = [
    "litellm>=1.0.0",
    "rich>=13.0.0",
    "your-new-package>=version",
]
```

Dependencies are automatically installed when users install the package via `uv tool install`.

### Creating New Tools

1. **Create module directory** under `tools/`:
   ```bash
   mkdir -p tools/new_tool
   ```

2. **Create module files:**
   - `__init__.py` - Export the main() function
   - `__main__.py` - Simple entry point that imports and calls main()
   - `main.py` - Core implementation with all logic

3. **Add dependencies** to `pyproject.toml`:
   ```toml
   dependencies = [
       "your-dependency>=version",
   ]
   ```

4. **Add entry point** in `pyproject.toml`:
   ```toml
   [project.scripts]
   new-tool = "tools.new_tool:main"
   ```

5. **Test your tool:**
   ```bash
   # Test as module
   uv run -m tools.new_tool

   # Test with uvx (without installation)
   uvx --from . new-tool

   # Test installed version (editable mode)
   uv tool install --editable .
   new-tool
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

For best results, use the review tool before committing:
1. Make your changes
2. Run `review` to get AI feedback (or `uvx --from . review` if not installed)
3. Address any issues or suggestions
4. Proceed with commit when prompted (or run `commit` separately)

## Package Distribution

The package uses standard Python packaging with `pyproject.toml`:
- **Build system**: Hatchling
- **Dependencies**: Managed via `[project.dependencies]`
- **Entry points**: Defined in `[project.scripts]`
- **Build**: `make build` or `uv build`
- **Publish**: Can be published to PyPI when ready

This allows users to:
- Install from GitHub: `uv tool install git+https://github.com/...`
- Install from PyPI (future): `uv tool install best-commits`
- Install locally: `uv tool install .`
- Use without installing: `uvx --from . commit`
