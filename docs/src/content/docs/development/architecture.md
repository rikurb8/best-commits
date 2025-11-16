---
title: Architecture
description: Deep dive into Best Commits architecture and design decisions
---

This document provides a comprehensive overview of Best Commits' architecture, design decisions, and implementation patterns.

## Project Structure

```
best-commits/
├── tools/                      # Main Python modules (installable tools)
│   ├── __init__.py            # Package initialization
│   ├── commit_changes/        # Commit message generator
│   │   ├── __main__.py        # Entry point with PEP 723 metadata
│   │   ├── main.py            # Core implementation
│   │   ├── __init__.py        # Module exports
│   │   └── PROMPT.md          # AI prompt template
│   └── review_changes/        # Code review tool
│       ├── __main__.py        # Entry point with PEP 723 metadata
│       ├── main.py            # Core implementation
│       ├── __init__.py        # Module exports
│       ├── PROMPT.md          # AI prompt template
│       └── SCORING_SYSTEM.md  # Gerrit scoring reference
├── evals/                     # Automated evaluation system
│   ├── storage/               # SQLite-based results storage
│   ├── commit_changes/        # Commit tool evaluations
│   ├── review_changes/        # Review tool evaluations
│   └── README.md
├── scripts/                   # Installation and utilities
│   └── install-tool.sh        # Global installation script
├── specs/                     # Feature specifications
├── docs/                      # Starlight documentation (this site)
├── README.md                  # Project overview
├── CLAUDE.md                  # Claude Code integration guide
└── pyproject.toml             # Python project metadata
```

## Design Principles

### 1. Simplicity First

**Goal**: Make Git workflows easier, not more complex

**Implementation**:
- Zero configuration required (sensible defaults)
- Single command execution (`commit`, `review`)
- No config files, only environment variables
- Automatic dependency management via uv

### 2. Module-Based Architecture

**Goal**: Each tool is an independent, installable Python module

**Pattern**:
```
tools/{tool_name}/
├── __main__.py     # Entry point with inline script metadata
├── main.py         # Core implementation
└── __init__.py     # Exports main() function
```

**Benefits**:
- Can run with `python -m tools.commit_changes`
- Can run with `uv run tools/commit_changes/__main__.py`
- Can import programmatically: `from tools.commit_changes import main`
- Each tool is self-contained with PEP 723 dependencies

### 3. Runtime Prompt Loading

**Goal**: Allow prompt customization without code changes

**Implementation**:
- Prompts stored as markdown files
- Loaded at runtime from `PROMPT.md`
- Changes take effect immediately
- Easy to version control and review

**Example**:
```python
def load_prompt(tool_dir):
    prompt_path = os.path.join(tool_dir, "PROMPT.md")
    with open(prompt_path, "r") as f:
        return f.read()
```

### 4. Provider Agnostic

**Goal**: Support multiple AI providers seamlessly

**Implementation**:
- Uses LiteLLM for unified API
- Single `BETTER_COMMIT_MODEL` variable
- Provider auto-detected from model name
- API keys read from standard environment variables

## Core Components

### 1. Tool Entry Points (`__main__.py`)

**Responsibilities**:
- Define PEP 723 metadata for dependencies
- Provide shebang for direct execution
- Call main() from main.py

**Pattern**:
```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "litellm>=1.0.0",
#   "rich>=13.0.0",
# ]
# ///

from .main import main

if __name__ == "__main__":
    main()
```

**Key Features**:
- Executable with `uv run` or directly (`./tools/.../main__.py`)
- Dependencies automatically installed
- No separate requirements.txt needed

### 2. Core Implementation (`main.py`)

**Structure**:
```python
def setup_api_keys():
    """Handle backwards compatibility for API keys"""

def load_prompt():
    """Load prompt template from PROMPT.md"""

def get_model_name():
    """Get model from env or use default"""

def get_git_status():
    """Run git status --porcelain"""

def get_diff(staged=False):
    """Get git diff (staged or unstaged)"""

def generate_commit_message(diffs, model):
    """Call AI model to generate message"""

def main():
    """Main entry point with error handling"""
```

**Error Handling**:
```python
try:
    # Git operations
    result = subprocess.run(["git", ...], check=True)
except subprocess.CalledProcessError as e:
    console.print(f"[red]Git error: {e}[/red]")
    sys.exit(1)
except Exception as e:
    console.print(f"[red]Unexpected error: {e}[/red]")
    sys.exit(1)
```

### 3. Git Integration

**Operations**:
- `git status --porcelain` - Check for changes
- `git diff` - Get unstaged changes
- `git diff --staged` - Get staged changes
- `git add -A` - Stage all changes (commit tool only)
- `git commit -m "..."` - Create commit (commit tool only)

**Implementation Pattern**:
```python
def get_git_status():
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout

def get_diff(staged=False):
    cmd = ["git", "diff"]
    if staged:
        cmd.append("--staged")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout
```

### 4. AI Model Integration

**Library**: LiteLLM for unified API

**Pattern**:
```python
from litellm import completion

response = completion(
    model=model_name,  # e.g., "claude-haiku-4-5-20251001"
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": diff_content}
    ],
    max_tokens=1024,
)

message = response.choices[0].message.content
```

**Benefits**:
- Single API for all providers
- Automatic retry logic
- Error handling
- Token counting
- Streaming support (not currently used)

### 5. Terminal UI

**Library**: Rich for formatted console output

**Components**:
- **Console**: Main output interface
- **Panels**: Bordered content boxes
- **Markdown**: Formatted text rendering
- **Syntax**: Code highlighting

**Example**:
```python
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

# Success message
console.print("[green]✓[/green] Committed successfully!")

# Panel output
console.print(Panel(commit_message, title="Commit Message"))

# Markdown rendering
console.print(Markdown(review_output))
```

## Data Flow

### Commit Tool Flow

```
1. Check for changes (git status)
   ├─ If no changes → Exit with message
   └─ If changes → Continue

2. Collect diffs
   ├─ Get unstaged diff
   └─ Get staged diff

3. Stage all changes
   └─ Run: git add -A

4. Load prompt template
   └─ Read: tools/commit_changes/PROMPT.md

5. Call AI model
   ├─ Provider: Determined from model name
   ├─ Input: Prompt + diffs
   └─ Output: Commit message

6. Format message
   └─ Strip markdown code blocks

7. Create commit
   └─ Run: git commit -m "message"

8. Display success
   └─ Print confirmation with Rich
```

### Review Tool Flow

```
1. Check for changes (git status)
   ├─ If no changes → Exit with message
   └─ If changes → Continue

2. Collect diffs
   ├─ Get unstaged diff
   └─ Get staged diff

3. Filter diffs
   ├─ Remove lock files (package-lock.json, etc.)
   ├─ Remove large generated files
   └─ Keep relevant changes

4. Load prompt templates
   ├─ Read: tools/review_changes/PROMPT.md
   └─ Read: tools/review_changes/SCORING_SYSTEM.md

5. Call AI model
   ├─ Provider: Determined from model name
   ├─ Input: Prompt + filtered diffs
   └─ Output: Structured review

6. Parse review
   ├─ Extract: Summary
   ├─ Extract: Gerrit score
   ├─ Extract: Issues
   ├─ Extract: Suggestions
   └─ Extract: Breaking changes

7. Display review
   └─ Render with Rich (markdown)

8. Prompt user
   ├─ Ask: "Proceed with commit? (y/n)"
   ├─ If yes → Call commit tool
   └─ If no → Exit
```

## Design Decisions

### Why uv Instead of pip?

**Reasons**:
1. **Speed**: 10-100x faster than pip
2. **PEP 723 Support**: Inline script metadata
3. **Simplicity**: No virtualenv management needed
4. **Reproducibility**: Lockfile support (uv.lock)

**Trade-off**: Requires uv installation (one-time setup)

### Why LiteLLM Instead of Direct SDKs?

**Reasons**:
1. **Unified API**: Same code for all providers
2. **Easy Switching**: Change model with env var
3. **Built-in Retry**: Automatic retry logic
4. **Token Counting**: Consistent across providers
5. **Future-Proof**: New providers added regularly

**Trade-off**: Extra dependency, slight overhead

### Why Rich for Terminal UI?

**Reasons**:
1. **Beautiful Output**: Professional formatting
2. **Cross-Platform**: Works on all terminals
3. **Markdown Support**: Render AI output directly
4. **Developer Experience**: Easy to use API
5. **Features**: Panels, colors, progress bars, etc.

**Trade-off**: Additional dependency (~500KB)

### Why Runtime Prompt Loading?

**Reasons**:
1. **Flexibility**: Edit without code changes
2. **Version Control**: Track prompt changes in git
3. **Experimentation**: Test different prompts easily
4. **Documentation**: Prompts are self-documenting
5. **Sharing**: Easy to share and review prompts

**Trade-off**: File I/O on each run (negligible)

### Why Symlinks for Installation?

**Reasons**:
1. **Updates**: `git pull` automatically updates tools
2. **Development**: Edit prompts, see changes immediately
3. **Simplicity**: No build step, no copying files
4. **Transparency**: User can see where tools are

**Trade-off**: Requires keeping repo on disk

### Why Conventional Commits Format?

**Reasons**:
1. **Standard**: Widely adopted in open source
2. **Tooling**: Many tools parse conventional commits
3. **Semantic Versioning**: Enables automated releases
4. **Changelog**: Can auto-generate changelogs
5. **Clarity**: Type prefix adds context

**Examples**:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `refactor:` Code refactoring
- `test:` Add tests
- `chore:` Maintenance

### Why Gerrit Scoring for Reviews?

**Reasons**:
1. **Standard**: Used by major projects (Android, Chromium)
2. **Nuance**: -2 to +2 provides useful granularity
3. **Actionable**: Clear meaning for each score
4. **Familiar**: Many developers know Gerrit

**Scale**:
- **+2**: Looks good, approved
- **+1**: Looks good but minor issues
- **0**: Neutral (needs work)
- **-1**: I would prefer changes
- **-2**: Do not submit (serious issues)

## Evaluation System

### Architecture

```
evals/
├── storage/
│   ├── database.py         # SQLite abstraction
│   └── schema.sql          # Database schema
├── commit_changes/
│   ├── run_eval.py         # Evaluation runner
│   └── {test_case}/
│       ├── README.md       # Test description
│       ├── diff.txt        # Sample diff
│       └── expected_elements.json
└── review_changes/
    └── (similar structure)
```

### Evaluation Flow

```
1. Load test case
   ├─ Read: diff.txt
   └─ Read: expected_elements.json

2. Run actual tool
   └─ Execute with test diff

3. Get judge evaluation
   ├─ Model: claude-sonnet-4-5-20250514 (judge)
   ├─ Input: Tool output + expected elements
   └─ Output: Score (1-100) + reasoning

4. Store result
   ├─ Save to SQLite
   └─ Compare with previous runs

5. Display results
   ├─ Score
   ├─ Comparison with baseline
   └─ Judge reasoning
```

### Storage Schema

```sql
CREATE TABLE eval_runs (
    id INTEGER PRIMARY KEY,
    tool_name TEXT,
    test_case TEXT,
    model_name TEXT,
    score REAL,
    timestamp TEXT,
    output TEXT,
    judge_reasoning TEXT
);
```

## Extension Points

### Adding a New Tool

1. **Create module structure**:
   ```bash
   mkdir -p tools/new_tool
   touch tools/new_tool/{__init__.py,__main__.py,main.py,PROMPT.md}
   ```

2. **Add PEP 723 metadata** to `__main__.py`

3. **Implement main()** in `main.py`

4. **Create prompt** in `PROMPT.md`

5. **Update installer**:
   ```bash
   # scripts/install-tool.sh
   # Add new tool to TOOLS array
   ```

### Adding a New Evaluation

1. **Create test case directory**:
   ```bash
   mkdir evals/{tool_name}/{test_case}
   ```

2. **Add test files**:
   - `README.md` - Description
   - `diff.txt` - Sample diff
   - `expected_elements.json` - Evaluation criteria

3. **Run evaluation**:
   ```bash
   uv run evals/{tool_name}/run_eval.py --case {test_case}
   ```

### Custom Prompts

1. **Edit prompt file**:
   ```bash
   vim tools/commit_changes/PROMPT.md
   ```

2. **Test changes**:
   ```bash
   commit  # Uses new prompt immediately
   ```

3. **Version control**:
   ```bash
   git add tools/commit_changes/PROMPT.md
   git commit -m "docs: update commit prompt"
   ```

## Performance Considerations

### Token Usage

| Tool | Typical Input | Typical Output | Total Tokens | Cost (Haiku) |
|------|---------------|----------------|--------------|--------------|
| commit | 500 tokens | 50 tokens | 550 | ~$0.0006 |
| review | 1000 tokens | 300 tokens | 1300 | ~$0.002 |

**Optimization**:
- Use cheap models (Haiku, GPT-3.5) for simple tasks
- Filter diffs to reduce input tokens
- Set appropriate max_tokens limits

### Response Time

| Component | Typical Time |
|-----------|-------------|
| Git operations | <100ms |
| Prompt loading | <10ms |
| API call (Haiku) | 2-3 seconds |
| API call (Sonnet) | 4-6 seconds |
| Display formatting | <50ms |

**Bottleneck**: AI API call (majority of time)

### Scaling

**Current**: Single-user, local execution

**Future Considerations**:
- Batch operations for multiple commits
- Caching for similar diffs
- Parallel evaluation runs
- Web service deployment

## Security Considerations

### API Key Handling

**Current**:
- Read from environment variables
- Never logged or printed
- Not stored in files

**Best Practices**:
- Use separate keys for different contexts
- Rotate keys regularly
- Revoke compromised keys immediately

### Code Privacy

**Considerations**:
- Diffs sent to third-party AI APIs
- No explicit data retention guarantees (depends on provider)
- Sensitive code should use self-hosted models (future)

**Recommendations**:
- Review provider privacy policies
- Avoid committing secrets
- Use enterprise API plans for sensitive work

### Input Validation

**Current**:
- Git operations use subprocess with shell=False
- No direct user input to shell
- API responses stripped of markdown only

**Improvements**:
- Sanitize git command outputs
- Validate model responses
- Rate limiting for API calls

## Testing Strategy

### Manual Testing

**Tools**:
```bash
# Quick smoke test
cd /tmp && git init test && cd test
echo "test" > README.md
commit
```

### Automated Evaluation

**System**: Judge-based evaluation with Claude Sonnet

**Benefits**:
- Consistent scoring
- Historical tracking
- Model comparison
- Regression detection

### Future: Unit Tests

**Planned**:
```python
def test_commit_message_format():
    message = generate_commit("feat: ...", diff)
    assert message.startswith("feat:")
    assert len(message.split("\n")[0]) <= 50
```

## Future Architecture

### Planned Enhancements

1. **Local Model Support**
   - Run models locally (Ollama, LlamaCPP)
   - No API costs, better privacy

2. **Context Awareness**
   - Access recent commits
   - Read related files
   - Check issue tracker

3. **Interactive Mode**
   - Chat interface
   - Iterative refinement
   - Multi-turn conversations

4. **Plugin System**
   - Custom rules
   - Project-specific guidelines
   - Linter integration

5. **Web Interface**
   - Team collaboration
   - Shared configuration
   - Analytics dashboard

## Contributing

See the [Contributing Guide](/development/contributing) for how to contribute to the architecture.

## Further Reading

- [CLAUDE.md](/development/claude) - Claude Code integration
- [Prompt Engineering](/development/prompt-improvements) - Prompt design
- [Contributing Guide](/development/contributing) - Development workflow
