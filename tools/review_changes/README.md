# best-commits-review

AI-powered code review tool for Git. Analyzes uncommitted changes and provides feedback before you commit.

## Features

- Reviews both staged and unstaged changes
- Provides summary of changes, potential issues, and improvement suggestions
- Filters out noise (lock files, etc.) for cleaner reviews
- Interactive prompt to proceed with commit
- Chains directly to `commit` command for seamless workflow
- Supports multiple AI models via LiteLLM
- Beautiful terminal output with Rich markdown formatting

## Installation

### From PyPI (future)
```bash
uv tool install best-commits-review
```

### From GitHub
```bash
# Install from subdirectory
uv tool install git+https://github.com/rikurb8/best-commits.git#subdirectory=tools/review_changes
```

### From Local Clone
```bash
git clone https://github.com/rikurb8/best-commits.git
cd best-commits/tools/review_changes
uv tool install .
```

## Usage

Once installed, use the `review` command from any git repository:

```bash
cd your-project
review
```

The tool will:
1. Analyze your uncommitted changes
2. Show a detailed code review
3. Ask if you want to proceed with commit
4. If yes, call the `commit` command (must be installed separately)

## Configuration

### Model Selection

Set the `BETTER_COMMIT_MODEL` environment variable to choose a model (default: `claude-haiku-4-5-20251001`):

```bash
export BETTER_COMMIT_MODEL=gpt-4
export OPENAI_API_KEY=your_key
review
```

### API Keys

Different providers require different API keys:

| Provider  | Model Format            | Environment Variable  |
|-----------|-------------------------|-----------------------|
| Anthropic | `claude-*`              | `ANTHROPIC_API_KEY` or `GIT_API_KEY` |
| OpenAI    | `gpt-*`, `o1-*`         | `OPENAI_API_KEY`      |
| xAI       | `xai/*`                 | `XAI_API_KEY`         |
| Google    | `gemini/*`              | `GEMINI_API_KEY`      |
| Cohere    | `cohere/*`              | `COHERE_API_KEY`      |
| Mistral   | `mistral/*`             | `MISTRAL_API_KEY`     |

See [LiteLLM documentation](https://docs.litellm.ai/docs/providers) for all supported models.

## Integration with Commit Tool

For the best workflow, install both tools:

```bash
uv tool install git+https://github.com/rikurb8/best-commits.git#subdirectory=tools/review_changes
uv tool install git+https://github.com/rikurb8/best-commits.git#subdirectory=tools/commit_changes
```

Then use `review` which will automatically offer to run `commit` after reviewing your changes.

## Development

```bash
# Install in editable mode
uv tool install --editable .

# Run without installation
uvx --from . review

# Run as module
uv run -m review_changes
```

## License

MIT
