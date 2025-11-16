---
title: FAQ
description: Frequently asked questions about Best Commits
---

## General Questions

### What is Best Commits?

Best Commits is a collection of AI-powered command-line tools that enhance your Git workflow by automatically generating commit messages and providing code reviews.

### Do I need to be online to use it?

Yes, currently the tools require internet access to communicate with AI model providers (Anthropic, OpenAI, etc.). Local model support is planned for the future.

### Is it free?

The tools themselves are free and open source (MIT license). However, you'll need an API key from an AI provider, which may have associated costs:

- **Anthropic Claude Haiku**: ~$1 per million input tokens
- **OpenAI GPT-3.5 Turbo**: ~$0.50 per million input tokens
- **Google Gemini Flash**: Free tier available

Typical cost per commit: **< $0.001** (less than a tenth of a cent)

### Which programming languages are supported?

All programming languages! The tools work with git diffs, which are language-agnostic. The AI models understand most programming languages including Python, JavaScript, TypeScript, Go, Rust, Java, C++, and more.

### Can I use this for private repositories?

Yes, but be aware that your code diffs are sent to the AI provider's API. Review your provider's privacy policy. For sensitive codebases, consider:
- Using a provider with strong privacy guarantees
- Waiting for local model support (coming soon)
- Using enterprise API plans with data residency options

## Installation & Setup

### Do I need Python installed?

No! The `uv` package manager handles Python automatically. You just need:
1. `uv` installed
2. Git
3. An API key from your chosen provider

### Where are the tools installed?

The installer creates symlinks in `~/.local/bin/` that point to the source code in your cloned repository. This means:
- Updates via `git pull` work immediately
- You can edit prompts and see changes instantly
- The repository must stay on your machine

### Can I install without cloning the repo?

Not currently. The symlink-based installation requires the repository to remain on disk. This is intentional to enable easy updates and prompt customization.

### Why isn't `commit` working after installation?

Most common cause: `~/.local/bin` is not in your PATH.

**Fix**:
```bash
# Check PATH
echo $PATH | grep -q "$HOME/.local/bin" && echo "OK" || echo "Missing"

# Add to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

See [Troubleshooting](/troubleshooting) for more solutions.

## Usage Questions

### How do I use a different AI model?

Set the `BETTER_COMMIT_MODEL` environment variable:

```bash
# Use GPT-4
export BETTER_COMMIT_MODEL=gpt-4o
export OPENAI_API_KEY=sk-...

# Use Gemini
export BETTER_COMMIT_MODEL=gemini/gemini-pro
export GEMINI_API_KEY=...
```

See [API Providers](/reference/api-providers) for all options.

### Can I customize the commit message format?

Yes! Edit the prompt file:

```bash
# Edit commit prompt
vim tools/commit_changes/PROMPT.md

# Changes take effect immediately
commit
```

### Can I use this with pre-commit hooks?

Yes, but be careful:

```bash
# .git/hooks/pre-commit
#!/bin/bash
review || exit 1
```

**Warning**: This requires manual approval for every commit, which may slow down your workflow.

### How do I disable the review tool's interactive prompt?

Currently not supported. The review tool always asks for confirmation before committing. If you want to skip the review, use the `commit` tool directly.

### Can I commit without staging?

Yes! The `commit` tool automatically stages all changes before committing (`git add -A`). The `review` tool shows both staged and unstaged changes.

### What if I want to review only staged changes?

Currently both tools review all uncommitted changes (staged and unstaged). Selective reviewing is not yet supported.

## API & Models

### Which model should I use?

**For commit messages** (speed matters):
- `claude-haiku-4-5-20251001` (default, recommended)
- `gpt-3.5-turbo` (fast, cheap)
- `gemini/gemini-flash` (very cheap)

**For code reviews** (quality matters):
- `claude-sonnet-4-5-20250514` (balanced)
- `gpt-4o` (excellent)
- `claude-opus-4-20250514` (best but slower/expensive)

See [API Providers](/reference/api-providers) for detailed comparison.

### How much does it cost?

Typical costs per operation:

| Operation | Model | Input Tokens | Output Tokens | Cost |
|-----------|-------|--------------|---------------|------|
| Commit | Haiku | 500 | 50 | $0.0006 |
| Review | Haiku | 1000 | 300 | $0.002 |
| Commit | GPT-3.5 | 500 | 50 | $0.0003 |
| Review | Sonnet | 1000 | 300 | $0.005 |

**Monthly cost** (50 commits + 20 reviews):
- Haiku only: ~$0.07
- GPT-3.5 + Sonnet mix: ~$0.13

### Can I use free AI models?

Some providers offer free tiers:
- **Google Gemini**: Free tier with rate limits
- **OpenAI**: Free trial credits for new accounts

However, most sustained usage requires a paid plan.

### What if I hit rate limits?

1. **Wait a moment** and try again
2. **Upgrade your API plan** for higher limits
3. **Switch to a different model** temporarily:
   ```bash
   BETTER_COMMIT_MODEL=gpt-3.5-turbo commit
   ```

### Why do I get "Model not found" errors?

Common causes:
1. **Wrong model name** - Check [API Providers](/reference/api-providers) for correct format
2. **Missing provider prefix** - Some need prefixes (e.g., `xai/grok-beta`)
3. **API key doesn't have access** - Check your account permissions
4. **Wrong API key** - Ensure key matches the provider

## Features & Functionality

### Does it understand my project's context?

Currently, no. The tools only see:
- The current git diff
- The prompt template you provide

**Future plans**:
- Access to recent commits
- Project documentation
- Issue tracker integration
- Custom project rules

### Can it run tests or verify my code?

No. The tools only provide AI-generated feedback based on the code diff. They cannot:
- Execute code
- Run tests
- Access external resources
- Verify functionality

You should still run tests manually.

### Will it catch all bugs?

No! The AI review is helpful but not perfect. It can miss:
- Subtle logic errors
- Complex race conditions
- Performance issues requiring benchmarks
- Integration issues

**Always**:
- Run tests
- Use linters
- Do manual code review for critical changes

### Can it write code for me?

No. These tools only:
- Generate commit messages (`commit`)
- Review existing code (`review`)

For code generation, use tools like GitHub Copilot, ChatGPT, or Claude.

### Does it support monorepos?

Yes! The tools work in any git repository structure, including monorepos. They analyze whatever changes you've made in the current repository.

### Can I use it with Git worktrees?

Yes, the tools use standard git commands and should work with worktrees.

### Does it work with GitHub, GitLab, Bitbucket?

Yes! The tools work with any git repository, regardless of remote hosting provider. They only interact with your local git repository.

## Customization

### Can I change the commit message format?

Yes! Edit `tools/commit_changes/PROMPT.md` to specify your preferred format. The default is conventional commits, but you can change it to anything.

### Can I add project-specific guidelines?

Yes! Edit the prompt files to include:
- Project-specific rules
- Coding conventions
- Required checklist items
- Team preferences

Example:
```markdown
# In tools/review_changes/PROMPT.md

## Project-Specific Rules
- All API endpoints must have rate limiting
- Database queries must use prepared statements
- All user input must be validated with Zod schemas
```

### Can I create my own tool?

Yes! See the [Contributing Guide](/development/contributing#adding-a-new-tool) for a step-by-step guide to creating new tools.

### Can I have different configurations for different projects?

Yes! Use `direnv`:

```bash
# Install direnv
brew install direnv  # macOS
apt-get install direnv  # Linux

# Set up for your shell
eval "$(direnv hook bash)"  # Add to ~/.bashrc

# Create project-specific config
cd /path/to/project
echo 'export BETTER_COMMIT_MODEL=gpt-4o' > .envrc
direnv allow
```

## Troubleshooting

### It's generating bad commit messages. Why?

Possible causes:
1. **Changes are too vague** - Make focused, single-purpose commits
2. **Model is too cheap** - Try a better model:
   ```bash
   export BETTER_COMMIT_MODEL=claude-sonnet-4-5-20250514
   ```
3. **Prompt needs tuning** - Edit `tools/commit_changes/PROMPT.md`
4. **No context in code** - Add comments explaining your changes

### The review tool says everything looks good but there are obvious issues

AI models can miss things. Possible causes:
1. **Model not powerful enough** - Try Opus or GPT-4o
2. **Issue not visible in diff** - Problem might be in unchanged code
3. **Complex logic** - AI struggles with intricate algorithms
4. **Domain-specific** - May not understand your specific domain

**Always use judgment** and don't rely solely on AI review.

### It's too slow. How can I speed it up?

1. **Use faster models**:
   ```bash
   export BETTER_COMMIT_MODEL=gpt-3.5-turbo
   ```

2. **Make smaller commits** - Less diff = faster processing

3. **Check internet speed** - API calls require good connectivity

4. **Try different provider** - Some have faster response times

### My API key isn't working

See [Troubleshooting - API Key Errors](/troubleshooting#api-key-errors) for detailed solutions.

## Privacy & Security

### Is my code sent to AI providers?

Yes. Git diffs are sent to the AI provider's API for analysis. Ensure you:
- Review your provider's privacy policy
- Don't commit secrets or sensitive data
- Use enterprise plans for sensitive work
- Consider local models (coming soon) for very sensitive code

### Will my code be used to train AI models?

Depends on the provider:
- **Anthropic**: Enterprise/API data not used for training (per their policy)
- **OpenAI**: API data not used for training by default (can opt in)
- **Others**: Check their specific policies

### Should I use this for work projects?

Consult your organization's policies on:
- Using third-party AI services
- Sharing code with external services
- Data residency requirements

Many enterprises have approved AI providers and acceptable use policies.

### How do I keep my API key secure?

Best practices:
1. **Never commit API keys** to git
2. **Use environment variables** (not config files)
3. **Rotate keys regularly**
4. **Use separate keys** for work vs personal
5. **Revoke immediately** if compromised

See [Configuration - Security](/configuration#security-best-practices).

## Future Features

### Will there be a GUI?

It's being considered! The current focus is on CLI tools, but a web interface for teams is in the roadmap.

### Can you add support for {feature}?

Maybe! Please:
1. Check existing issues on GitHub
2. Create a feature request if not found
3. Explain your use case and motivation

Popular requests get prioritized.

### When will local model support be added?

It's a high priority feature. Planned support for:
- Ollama
- LlamaCPP
- Local API endpoints

No ETA yet, but contributions are welcome!

### Will it integrate with {tool}?

Possible integrations being considered:
- Linters (ESLint, Pylint, etc.)
- Test frameworks (pytest, Jest, etc.)
- CI/CD platforms (GitHub Actions, etc.)
- Issue trackers (GitHub, Jira, etc.)

Create an issue to request specific integrations.

## Getting More Help

### Where can I ask questions?

1. **Check documentation** - Most questions answered here
2. **Search issues** - Someone may have asked before
3. **GitHub Discussions** - For open-ended questions
4. **Create issue** - For bugs or feature requests

### How do I report a bug?

See [Contributing - Report Bugs](/development/contributing#-report-bugs).

### How can I contribute?

See the [Contributing Guide](/development/contributing).

### Is there a community?

The project is hosted on GitHub. Community interactions happen through:
- GitHub Issues (bugs, features)
- GitHub Discussions (questions, ideas)
- Pull Requests (contributions)

## Still Have Questions?

If your question isn't answered here:
1. Search the [documentation](/index)
2. Check [GitHub Issues](https://github.com/yourusername/best-commits/issues)
3. Ask in [GitHub Discussions](https://github.com/yourusername/best-commits/discussions)
4. Create a new issue if you found a bug
