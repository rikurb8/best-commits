# best-commits-commit

AI-powered Git commit message generator using LiteLLM. Automatically analyzes your git changes and creates well-formatted, conventional commit messages.

## Features

- Analyzes staged and unstaged changes
- Generates conventional commit messages (feat:, fix:, docs:, etc.)
- Follows best practices (imperative mood, 50-char summary)
- Supports multiple AI models via LiteLLM
- Beautiful terminal output with Rich

## Installation

### From PyPI (future)
```bash
uv tool install best-commits-commit
```

### From GitHub
```bash
# Install from subdirectory
uv tool install git+https://github.com/rikurb8/best-commits.git#subdirectory=tools/commit_changes
```

### From Local Clone
```bash
git clone https://github.com/rikurb8/best-commits.git
cd best-commits/tools/commit_changes
uv tool install .
```

## Usage

Once installed, use the `commit` command from any git repository:

```bash
cd your-project
commit
```

## Configuration

### Model Selection

Set the `BETTER_COMMIT_MODEL` environment variable to choose a model (default: `claude-haiku-4-5-20251001`):

```bash
export BETTER_COMMIT_MODEL=gpt-4
export OPENAI_API_KEY=your_key
commit
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

## Development

```bash
# Install in editable mode
uv tool install --editable .

# Run without installation
uvx --from . commit

# Run as module
uv run -m commit_changes
```

## License

MIT
