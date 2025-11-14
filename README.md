# Best Commits

Installable command-line scripts to make working with git easier.

## Available Scripts

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
- [Anthropic API key](https://console.anthropic.com) - Set as `GIT_API_KEY` env variable

**Install globally:**

```bash
# Clone and navigate to repo
git clone https://github.com/YOUR_USERNAME/best-commits.git
cd best-commits

# Create global command
mkdir -p ~/.local/bin && cat > ~/.local/bin/commit << EOF
#!/bin/bash
uv run "$PWD/commit-changes.py" "\$@"
EOF
chmod +x ~/.local/bin/commit

# Set API key (add to ~/.bashrc or ~/.zshrc for persistence)
export GIT_API_KEY=your_anthropic_api_key
```

**Usage:**

```bash
cd ~/any-git-repo
commit
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

The `commit` script uses Claude Haiku 4.5:
- **Model:** `claude-haiku-4-5-20251001`

## Future Plans

- Support for more AI models
  - [ ] Setup LiteLLM 
  - [ ] use BETTER_COMMIT_MODEL env variable to specify model, document how to use it
  - [ ] Document how to configure credentials for different models (""OPENAI_API_KEY", "XAI_API_KEY", etc)

- Improve commit message quality
  - More specific on what to include in commit messages
  - Should there be more context than just the uncommited changes?
  
- Review work functionality (Draft spec: docs/01-review-functionality.md)
  - [ ] Add "review" command which analyzes unchanged commits, gives small summary and suggestions for improvements or go ahead for making commit
    - Should it have more context, like "recent relevant commits"

## License

MIT
