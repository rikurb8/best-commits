# Best Commits

AI-powered git commit message generator using Claude API. Automatically analyze your changes and create informative, well-formatted commit messages.

## Features

- Analyzes both staged and unstaged changes
- Generates conventional commit messages using Claude Haiku 4.5
- Follows best practices (imperative mood, 50-char summary, etc.)
- Beautiful terminal output with rich formatting
- Single-file executable with uvx (no installation required)
- Available in both Python and JavaScript/zx versions

## Prerequisites

- Git repository with changes to commit
- Anthropic API key (get one at https://console.anthropic.com)
- Python 3.8+ (for Python version) or Node.js (for JavaScript version)

## Quick Start

### Python Version (Recommended)

The Python version uses `uvx` for zero-installation execution:

```bash
# Set your API key
export GIT_API_KEY=your_anthropic_api_key

# Run directly with uvx (no installation needed!)
uvx commit-changes.py

# Or make it executable and run it
chmod +x commit-changes.py
./commit-changes.py
```

### JavaScript/zx Version

```bash
# Set your API key
export GIT_API_KEY=your_anthropic_api_key

# Run with npx zx
npx zx commit-changes.mjs
```

## Installation

### Python Version

No installation required! The script uses `uvx` which automatically handles dependencies.

If you want to install it system-wide:

```bash
# Copy to your local bin directory
cp commit-changes.py ~/.local/bin/best-commit
chmod +x ~/.local/bin/best-commit

# Now you can run it from anywhere
cd any-git-repo
best-commit
```

### JavaScript Version

```bash
# Install zx globally (optional)
npm install -g zx

# Install dependencies for the script
npm install @anthropic-ai/sdk zx
```

## Configuration

Set the `GIT_API_KEY` environment variable with your Anthropic API key:

```bash
# Temporary (current session only)
export GIT_API_KEY=your_anthropic_api_key

# Permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export GIT_API_KEY=your_anthropic_api_key' >> ~/.bashrc
```

## How It Works

1. **Detects Changes**: Checks for uncommitted changes in your git repository
2. **Stages Files**: Automatically stages all changes (`git add -A`)
3. **Analyzes Diff**: Collects git status and diff information
4. **Generates Message**: Sends changes to Claude API for analysis
5. **Creates Commit**: Uses the generated message to create a commit

## Commit Message Format

The generated messages follow conventional commit standards:

- **Format**: `type: brief summary (≤50 chars)`
- **Types**: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
- **Style**: Imperative mood ("Add feature" not "Added feature")
- **Content**: Focus on WHAT and WHY, not HOW
- **Details**: Optional detailed description after blank line

### Example Output

```
🔍 Checking for uncommitted changes...

┏━━━━━━━━━━━ Git Status ━━━━━━━━━━━┓
┃ M  commit-changes.py            ┃
┃ ?? README.md                    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

🤖 Generating commit message with Claude API...

┏━━━━━━━━ Commit Message ━━━━━━━━┓
┃ feat: Add Python version with  ┃
┃ rich formatting                 ┃
┃                                 ┃
┃ Create uvx-compatible Python   ┃
┃ script with beautiful terminal ┃
┃ output using rich library      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

💾 Creating commit...

✓ Commit created successfully!
```

## API Usage

The script uses Claude Haiku 4.5, which is fast and cost-effective:

- **Model**: `claude-haiku-4-5-20251001`
- **Cost**: ~$0.001 per commit message
- **Speed**: ~1-2 seconds per generation

## Troubleshooting

### "GIT_API_KEY environment variable is not set"

Make sure you've set your API key:
```bash
export GIT_API_KEY=your_key_here
```

### "No uncommitted changes found"

The repository is clean. Make some changes first:
```bash
echo "test" > test.txt
./commit-changes.py
```

### "Git command failed"

Ensure you're in a git repository:
```bash
git init  # if not already a repo
```

### Python version: "uvx: command not found"

Install uv:
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

## License

MIT

## Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## Acknowledgments

- Built with [Claude API](https://www.anthropic.com/api) by Anthropic
- Python version uses [rich](https://github.com/Textualize/rich) for beautiful terminal output
- JavaScript version uses [zx](https://github.com/google/zx) for scripting
- Inspired by best practices from [Conventional Commits](https://www.conventionalcommits.org/)
