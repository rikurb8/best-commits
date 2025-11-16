---
title: API Providers
description: Complete guide to setting up AI model providers
---

Best Commits supports multiple AI providers through [LiteLLM](https://docs.litellm.ai/), giving you flexibility in choosing models based on cost, performance, and availability.

## Default Provider

**Anthropic Claude** is the default provider:
- **Model**: `claude-haiku-4-5-20251001` (Claude Haiku 4.5)
- **Why**: Fast, cost-effective, excellent for commit messages and code reviews
- **Pricing**: ~$1 per million tokens (input), ~$5 per million tokens (output)

## Supported Providers

### Anthropic (Claude)

**Models**: Claude Opus, Sonnet, Haiku

**Setup**:
```bash
# Get API key from https://console.anthropic.com
export ANTHROPIC_API_KEY=sk-ant-api03-...

# Optional: specify model
export BETTER_COMMIT_MODEL=claude-sonnet-4-5-20250514
```

**Available Models**:
- `claude-opus-4-20250514` - Most capable, slowest, most expensive
- `claude-sonnet-4-5-20250514` - Balanced performance
- `claude-haiku-4-5-20251001` - Fast, cheap, recommended (default)

**Pricing**: See [Anthropic pricing](https://www.anthropic.com/pricing)

**Legacy Support**: `GIT_API_KEY` environment variable still works for backwards compatibility.

---

### OpenAI (GPT)

**Models**: GPT-4, GPT-4o, GPT-3.5 Turbo

**Setup**:
```bash
# Get API key from https://platform.openai.com/api-keys
export OPENAI_API_KEY=sk-...

# Specify model
export BETTER_COMMIT_MODEL=gpt-4o
```

**Available Models**:
- `gpt-4o` - Latest, fast, multimodal
- `gpt-4-turbo` - Previous generation, capable
- `gpt-4` - Original GPT-4
- `gpt-3.5-turbo` - Fast and cheap
- `o1-preview` - Reasoning model (slower, more thoughtful)

**Pricing**: See [OpenAI pricing](https://openai.com/pricing)

**Notes**:
- OpenAI models are generally faster than Claude
- GPT-4o recommended for best balance
- o1 models use different token counting

---

### xAI (Grok)

**Models**: Grok Beta

**Setup**:
```bash
# Get API key from https://console.x.ai
export XAI_API_KEY=xai-...

# Specify model (note the xai/ prefix)
export BETTER_COMMIT_MODEL=xai/grok-beta
```

**Available Models**:
- `xai/grok-beta` - Latest Grok model

**Important**: xAI models **require** the `xai/` prefix in the model name.

**Pricing**: See [xAI pricing](https://x.ai/api)

---

### Google (Gemini)

**Models**: Gemini Pro, Gemini Flash

**Setup**:
```bash
# Get API key from https://makersuite.google.com/app/apikey
export GEMINI_API_KEY=...

# Specify model (note the gemini/ prefix)
export BETTER_COMMIT_MODEL=gemini/gemini-pro
```

**Available Models**:
- `gemini/gemini-pro` - Most capable Gemini model
- `gemini/gemini-flash` - Fast, lightweight version
- `gemini/gemini-1.5-pro` - Latest version with long context

**Important**: Gemini models **require** the `gemini/` prefix.

**Pricing**: See [Google AI pricing](https://ai.google.dev/pricing)

---

### Cohere (Command)

**Models**: Command R, Command R+

**Setup**:
```bash
# Get API key from https://dashboard.cohere.com/api-keys
export COHERE_API_KEY=...

# Specify model (prefix optional but recommended)
export BETTER_COMMIT_MODEL=cohere/command-r-plus
```

**Available Models**:
- `cohere/command-r-plus` - Most capable
- `cohere/command-r` - Balanced
- `command-light` - Fastest (prefix optional)

**Pricing**: See [Cohere pricing](https://cohere.com/pricing)

---

### Mistral AI

**Models**: Mistral Large, Medium, Small

**Setup**:
```bash
# Get API key from https://console.mistral.ai
export MISTRAL_API_KEY=...

# Specify model
export BETTER_COMMIT_MODEL=mistral/mistral-large-latest
```

**Available Models**:
- `mistral/mistral-large-latest` - Most capable
- `mistral/mistral-medium-latest` - Balanced
- `mistral/mistral-small-latest` - Fast and cheap

**Pricing**: See [Mistral pricing](https://mistral.ai/technology/#pricing)

---

## Provider Comparison

| Provider  | Speed    | Cost      | Quality   | Best For                |
|-----------|----------|-----------|-----------|-------------------------|
| Anthropic | Medium   | Medium    | Excellent | All-around, code review |
| OpenAI    | Fast     | Medium    | Excellent | Quick commits           |
| xAI       | Medium   | Medium    | Good      | Alternative to Claude   |
| Google    | Fast     | Low       | Good      | Budget-conscious        |
| Cohere    | Fast     | Low       | Good      | Simple tasks            |
| Mistral   | Fast     | Low       | Good      | European data residency |

## Choosing a Model

### For Commit Messages

**Recommended**: Fast, cheap models work great:
```bash
export BETTER_COMMIT_MODEL=claude-haiku-4-5-20251001  # Default
# or
export BETTER_COMMIT_MODEL=gpt-3.5-turbo
# or
export BETTER_COMMIT_MODEL=gemini/gemini-flash
```

### For Code Reviews

**Recommended**: More capable models for thorough analysis:
```bash
export BETTER_COMMIT_MODEL=claude-sonnet-4-5-20250514
# or
export BETTER_COMMIT_MODEL=gpt-4o
# or
export BETTER_COMMIT_MODEL=gemini/gemini-1.5-pro
```

### Cost Optimization

1. **Use cheaper models** for routine commits
2. **Reserve expensive models** for important reviews
3. **Switch based on context**:
   ```bash
   # In your shell rc file
   alias commit-quick='BETTER_COMMIT_MODEL=gpt-3.5-turbo commit'
   alias review-deep='BETTER_COMMIT_MODEL=claude-opus-4-20250514 review'
   ```

### Quality Optimization

**For best results**:
- Use Opus or GPT-4o for complex code reviews
- Use Sonnet or GPT-4 for standard reviews
- Use Haiku or GPT-3.5 for simple commits

## Environment Variable Reference

```bash
# Provider API Keys
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...
export XAI_API_KEY=xai-...
export GEMINI_API_KEY=...
export COHERE_API_KEY=...
export MISTRAL_API_KEY=...

# Model Selection
export BETTER_COMMIT_MODEL=claude-haiku-4-5-20251001

# Legacy (Anthropic only)
export GIT_API_KEY=sk-ant-...
```

## Testing Your Setup

```bash
# Verify environment variables
env | grep -E "(API_KEY|BETTER_COMMIT)"

# Test in a git repo
cd /path/to/test/repo
echo "test" >> README.md
commit  # Should generate a commit message
```

## Common Issues

### Wrong API Key Variable

**Problem**: Using `OPENAI_API_KEY` with Claude model

**Solution**: Match the key to your chosen model:
```bash
# If using Claude
export ANTHROPIC_API_KEY=sk-ant-...
export BETTER_COMMIT_MODEL=claude-haiku-4-5-20251001

# If using OpenAI
export OPENAI_API_KEY=sk-...
export BETTER_COMMIT_MODEL=gpt-4o
```

### Missing Model Prefix

**Problem**: `export BETTER_COMMIT_MODEL=grok-beta` fails

**Solution**: Add required prefix:
```bash
export BETTER_COMMIT_MODEL=xai/grok-beta  # ✓ Correct
export BETTER_COMMIT_MODEL=gemini/gemini-pro  # ✓ Correct
```

### Model Not Available

**Problem**: "Model not found" error

**Solutions**:
1. Check your API plan has access to the model
2. Verify model name is correct
3. Check [LiteLLM docs](https://docs.litellm.ai/docs/providers) for current model names
4. Some models require special access requests

## Advanced: Multiple Profiles

Create shell aliases for different use cases:

```bash
# Add to ~/.bashrc or ~/.zshrc

# Fast commits with cheap model
alias commit-fast='BETTER_COMMIT_MODEL=gpt-3.5-turbo commit'

# Thorough review with powerful model
alias review-thorough='BETTER_COMMIT_MODEL=claude-opus-4-20250514 review'

# Budget-friendly option
alias commit-free='BETTER_COMMIT_MODEL=gemini/gemini-flash commit'

# Work vs personal (different API keys)
alias commit-work='ANTHROPIC_API_KEY=$WORK_API_KEY commit'
alias commit-personal='ANTHROPIC_API_KEY=$PERSONAL_API_KEY commit'
```

## Further Reading

- [LiteLLM Providers Documentation](https://docs.litellm.ai/docs/providers)
- [Configuration Reference](/configuration)
- [Environment Variables](/reference/environment)
- [Troubleshooting API Issues](/troubleshooting#api-key-errors)
