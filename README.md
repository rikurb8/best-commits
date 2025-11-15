# Best Commits

Installable command-line scripts to make working with git easier.

## Available Scripts

### `review`

AI-powered code review for uncommitted changes. Analyzes your code and provides feedback before you commit.

**Features:**

- Reviews both staged and unstaged changes
- Provides summary of changes, potential issues, and improvement suggestions
- Filters out noise (lock files, etc.) for cleaner reviews
- Interactive prompt to proceed with commit
- Chains directly to `commit` command for seamless workflow
- Beautiful terminal output with markdown formatting

### `commit`

AI-powered commit message generator using Claude API. Automatically analyzes your git changes and creates well-formatted, conventional commit messages.

**Features:**

- Analyzes staged and unstaged changes
- Generates conventional commit messages (feat:, fix:, docs:, etc.)
- Follows best practices (imperative mood, 50-char summary)
- Beautiful terminal output

## Installation

**Prerequisites:**

- [uv](https://docs.astral.sh/uv/) - Fast Python package installer
- API key for your chosen AI model (default: [Anthropic API key](https://console.anthropic.com))

### Quick Install

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/best-commits.git
cd best-commits

# Run the installer (installs both commit and review)
./scripts/install-tool.sh

# Or install individual tools
./scripts/install-tool.sh commit
./scripts/install-tool.sh review
```

The installer creates symlinks in `~/.local/bin/` pointing to the tools. Make sure this directory is in your PATH:

```bash
# Add to ~/.bashrc, ~/.zshrc, or equivalent
export PATH="$HOME/.local/bin:$PATH"
```

### Configure API Key

Set your API key (add to your shell's rc file for persistence):

```bash
# For Anthropic Claude (default):
export ANTHROPIC_API_KEY=your_anthropic_api_key

# OR use legacy variable name:
export GIT_API_KEY=your_anthropic_api_key

# For other models, see "API Key Configuration" section below
```

### Usage

Once installed, use the tools from any git repository:

```bash
cd ~/any-git-repo

# Review changes and optionally commit
review

# Or directly commit without review
commit
```

### Uninstall

To remove installed tools:

```bash
cd best-commits

# Uninstall all tools
./scripts/install-tool.sh uninstall

# Or uninstall individual tools
./scripts/install-tool.sh uninstall commit
./scripts/install-tool.sh uninstall review
```

## Adding New Scripts

To add a new script to this repo:

1. **Create executable Python script** with uv-compatible shebang:

   ```python
   #!/usr/bin/env python3
   # /// script
   # dependencies = [
   #   "package-name>=version",
   # ]
   # ///
   ```

2. **Make it executable:**

   ```bash
   chmod +x your-script.py
   ```

3. **Test with uv:**

   ```bash
   uv run your-script.py
   ```

4. **Add installation instructions** to this README

**Requirements:**

- Must be runnable with `uv run`
- Must include PEP 723 inline script metadata for dependencies
- Should be a single-file executable
- Should have clear, focused purpose

## API Usage

Both `review` and `commit` scripts support multiple AI models via LiteLLM:

### Default Model

- **Model:** `claude-haiku-4-5-20251001` (Claude Haiku 4.5)
- **Token limits:** 1024 for commit messages, 2048 for reviews

### Choosing a Different Model

Set the `BETTER_COMMIT_MODEL` environment variable to use a different model. Model names follow the LiteLLM format:

```bash
# Use OpenAI GPT-4
export BETTER_COMMIT_MODEL=gpt-4
export OPENAI_API_KEY=your_openai_key

# Use Anthropic Claude Opus
export BETTER_COMMIT_MODEL=claude-opus-4-20250514
export ANTHROPIC_API_KEY=your_anthropic_key

# Use xAI Grok (note: requires xai/ prefix)
export BETTER_COMMIT_MODEL=xai/grok-beta
export XAI_API_KEY=your_xai_key

# Use Google Gemini
export BETTER_COMMIT_MODEL=gemini/gemini-pro
export GEMINI_API_KEY=your_gemini_key

# Then use the commands as normal
review
commit
```

**Note:** Some providers require a prefix in the model name (e.g., `xai/`, `gemini/`, `cohere/`). Check the [LiteLLM providers documentation](https://docs.litellm.ai/docs/providers) for the correct format.

### API Key Configuration

Different model providers require different API key environment variables:

| Provider  | Model Format              | Example                     | Environment Variable                          |
| --------- | ------------------------- | --------------------------- | --------------------------------------------- |
| Anthropic | `claude-*`                | `claude-haiku-4-5-20251001` | `ANTHROPIC_API_KEY` or `GIT_API_KEY` (legacy) |
| OpenAI    | `gpt-*`, `o1-*`           | `gpt-4`, `gpt-4o`           | `OPENAI_API_KEY`                              |
| xAI       | `xai/*`                   | `xai/grok-beta`             | `XAI_API_KEY`                                 |
| Google    | `gemini/*`                | `gemini/gemini-pro`         | `GEMINI_API_KEY`                              |
| Cohere    | `cohere/*` or `command-*` | `cohere/command-r`          | `COHERE_API_KEY`                              |
| Mistral   | `mistral/*`               | `mistral/mistral-large`     | `MISTRAL_API_KEY`                             |

**Important:** Some providers (xAI, Google, Cohere, Mistral) require a provider prefix in the model name (e.g., `xai/grok-beta` not just `grok-beta`). Anthropic and OpenAI models can be used without a prefix.

For a complete list of supported models and providers, see [LiteLLM documentation](https://docs.litellm.ai/docs/providers).

**Note:** For backwards compatibility, `GIT_API_KEY` is still supported for Anthropic models.

## Future Plans

- Support for more AI models
  - [x] Setup LiteLLM
  - [x] use BETTER_COMMIT_MODEL env variable to specify model, document how to use it
  - [x] Document how to configure credentials for different models ("OPENAI_API_KEY", "XAI_API_KEY", etc)

- Improve commit message quality
  - More specific on what to include in commit messages
  - Should there be more context than just the uncommited changes?

- Enhance review functionality
  - Add context from recent relevant commits
  - Support for custom review rules/checklist
  - Integration with linters and test frameworks
- Claude Code Integration
  - [ ] Add support for Claude Code integration
  - [ ] Document how to configure Claude Code credentials
- Repository util
  - Create new /utils/repo_utils/
  - Initially connect with
  - Supported commands:
    - [ ] List PRs
    - [ ] Fetch PR details (diff, comments)
    - [ ] Add PR comment
    - [ ] List Issues

## License

MIT
