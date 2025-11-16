---
title: Contributing
description: Guide for contributing to Best Commits
---

Thank you for your interest in contributing to Best Commits! This guide will help you get started.

## Quick Start

```bash
# 1. Fork and clone
git clone https://github.com/yourusername/best-commits.git
cd best-commits

# 2. Install dependencies (via uv)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Run tools locally
uv run tools/commit_changes/__main__.py
uv run tools/review_changes/__main__.py

# 4. Make changes and test
# Edit files...
uv run tools/commit_changes/__main__.py  # Test your changes

# 5. Use the review tool on your own changes!
uv run tools/review_changes/__main__.py

# 6. Commit (using the commit tool)
uv run tools/commit_changes/__main__.py
```

## Ways to Contribute

### 🐛 Report Bugs

Found a bug? Please create an issue with:

- **Clear title**: Describe the problem concisely
- **Steps to reproduce**: Exact commands and context
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**:
  - OS and version
  - Python version (`python3 --version`)
  - uv version (`uv --version`)
  - Git version (`git --version`)
- **Error messages**: Full output (use code blocks)

**Example**:
```markdown
## Bug: Commit tool fails with large diffs

### Steps to Reproduce
1. Create repository with 1000+ file changes
2. Run `commit`

### Expected
Generate commit message

### Actual
Error: "Token limit exceeded"

### Environment
- macOS 14.0
- Python 3.11.5
- uv 0.1.44
```

### 💡 Suggest Features

Have an idea? Create an issue with:

- **Use case**: Why is this needed?
- **Proposed solution**: How should it work?
- **Alternatives**: Other approaches considered
- **Additional context**: Examples, mockups, etc.

### 📝 Improve Documentation

Documentation improvements are always welcome:

- Fix typos and grammar
- Add examples
- Clarify confusing sections
- Add missing documentation
- Improve organization

**Process**:
1. Edit files in `/docs/src/content/docs/`
2. Test locally: `cd docs && npm run dev`
3. Submit PR

### 🔧 Submit Code Changes

See the [Development Workflow](#development-workflow) below.

## Development Workflow

### 1. Set Up Development Environment

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/yourusername/best-commits.git
cd best-commits

# Add upstream remote
git remote add upstream https://github.com/originalowner/best-commits.git

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Set up API key for testing
export ANTHROPIC_API_KEY=sk-ant-...
```

### 2. Create a Feature Branch

```bash
# Update main
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feat/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### 3. Make Changes

**For tool changes**:
```bash
# Edit implementation
vim tools/commit_changes/main.py

# Edit prompts
vim tools/commit_changes/PROMPT.md

# Test your changes
cd /tmp && git init test-repo && cd test-repo
echo "test change" > README.md
uv run /path/to/best-commits/tools/commit_changes/__main__.py
```

**For documentation changes**:
```bash
# Edit documentation
vim docs/src/content/docs/installation.md

# Test locally
cd docs
npm install  # First time only
npm run dev  # Starts dev server at http://localhost:4321
```

### 4. Test Your Changes

**Manual testing**:
```bash
# Create a test repository
cd /tmp
git init test-repo
cd test-repo

# Initialize git user
git config user.name "Test User"
git config user.email "test@example.com"

# Make test changes
echo "feature implementation" > src/feature.py
echo "test for feature" > tests/test_feature.py

# Test commit tool
uv run /path/to/best-commits/tools/commit_changes/__main__.py

# Make more changes
echo "another change" > README.md

# Test review tool
uv run /path/to/best-commits/tools/review_changes/__main__.py
```

**Run evaluations**:
```bash
# Test commit tool
uv run evals/commit_changes/run_eval.py

# Test review tool
uv run evals/review_changes/run_eval.py

# Test specific case
uv run evals/commit_changes/run_eval.py --case basic_feature

# View results
uv run evals/commit_changes/run_eval.py --summary
```

### 5. Follow Code Style

**Python style**:
- Follow PEP 8
- Use type hints where helpful
- Add docstrings for functions
- Keep functions focused and small

**Example**:
```python
def get_git_diff(staged: bool = False) -> str:
    """
    Get git diff output.

    Args:
        staged: If True, get staged changes. Otherwise unstaged.

    Returns:
        Diff output as string.

    Raises:
        subprocess.CalledProcessError: If git command fails.
    """
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

**Commit message style**:
- Use conventional commits format
- Imperative mood ("Add feature" not "Added feature")
- First line ≤50 characters
- Optional body for details

**Examples**:
```
feat: add support for GPT-4 model

fix: handle empty git diff correctly

docs: update installation instructions

refactor: extract prompt loading logic

test: add eval case for bugfix commits

chore: update dependencies
```

### 6. Commit Your Changes

**Use the tool itself!**
```bash
# Stage your changes
git add -A

# Use the review tool
uv run tools/review_changes/__main__.py

# Use the commit tool
uv run tools/commit_changes/__main__.py

# Or manually if needed
git commit -m "feat: add new feature"
```

### 7. Push and Create PR

```bash
# Push to your fork
git push origin feat/your-feature-name

# Create PR on GitHub
# - Title: Clear, descriptive
# - Description: Explain changes and motivation
# - Link related issues
```

**PR template**:
```markdown
## Description
Brief description of changes

## Motivation
Why is this change needed?

## Changes
- Added X
- Modified Y
- Fixed Z

## Testing
- [ ] Tested manually in test repository
- [ ] Ran evaluations
- [ ] Updated documentation

## Related Issues
Fixes #123
```

## Code Review Process

### What to Expect

1. **Automated checks**: CI runs (if configured)
2. **Maintainer review**: Usually within 1-3 days
3. **Feedback**: Suggestions for improvements
4. **Iteration**: Make requested changes
5. **Approval**: PR is approved and merged

### Responding to Feedback

```bash
# Make requested changes
vim tools/commit_changes/main.py

# Commit changes
git add -A
git commit -m "refactor: address review feedback"

# Push updates
git push origin feat/your-feature-name

# PR automatically updates
```

## Development Areas

### High Priority

- **Model support**: Add new providers
- **Error handling**: Improve error messages
- **Performance**: Optimize API calls
- **Testing**: Add unit tests
- **Documentation**: Expand examples

### Medium Priority

- **Features**: Context-aware commits
- **Integration**: CI/CD examples
- **UI/UX**: Improve terminal output
- **Evaluation**: More test cases

### Future Considerations

- **Local models**: Ollama, LlamaCPP support
- **Plugins**: Custom rules system
- **Web interface**: Team collaboration
- **Analytics**: Usage tracking

## Adding a New Tool

Want to create a new tool?

### 1. Create Module Structure

```bash
mkdir -p tools/new_tool
touch tools/new_tool/__init__.py
touch tools/new_tool/__main__.py
touch tools/new_tool/main.py
touch tools/new_tool/PROMPT.md
```

### 2. Implement `__main__.py`

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

### 3. Implement `main.py`

```python
import os
import sys
import subprocess
from rich.console import Console
from litellm import completion

console = Console()

def load_prompt():
    """Load prompt from PROMPT.md"""
    tool_dir = os.path.dirname(__file__)
    with open(os.path.join(tool_dir, "PROMPT.md")) as f:
        return f.read()

def main():
    """Main entry point"""
    try:
        # Your tool logic here
        console.print("[green]Success![/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)
```

### 4. Create `__init__.py`

```python
from .main import main

__all__ = ["main"]
```

### 5. Write Prompt

Create `PROMPT.md` with your AI prompt.

### 6. Update Installer

```bash
# scripts/install-tool.sh
# Add your tool to the TOOLS array
```

### 7. Test

```bash
# Test with uv
uv run tools/new_tool/__main__.py

# Make executable
chmod +x tools/new_tool/__main__.py

# Install globally
./scripts/install-tool.sh new-tool
```

## Adding Evaluation Cases

### 1. Create Test Case Directory

```bash
mkdir -p evals/commit_changes/my_test_case
```

### 2. Create Test Files

**README.md**:
```markdown
# My Test Case

Description of what this tests.

## Expected Elements
- Element 1
- Element 2
```

**diff.txt**:
```diff
diff --git a/file.py b/file.py
index abc123..def456 100644
--- a/file.py
+++ b/file.py
@@ -1,3 +1,5 @@
+# New feature
+
 def hello():
     print("Hello")
```

**expected_elements.json**:
```json
{
  "must_include": [
    "Conventional commit prefix (feat:, fix:, etc.)",
    "Descriptive summary"
  ],
  "must_not_include": [
    "Markdown code blocks"
  ]
}
```

### 3. Run Evaluation

```bash
uv run evals/commit_changes/run_eval.py --case my_test_case
```

## Improving Prompts

Prompt improvements are highly valuable!

### 1. Edit Prompt File

```bash
vim tools/commit_changes/PROMPT.md
```

### 2. Test Extensively

```bash
# Test with various change types
# - New features
# - Bug fixes
# - Refactoring
# - Documentation
# - Tests

# Use evaluation system
uv run evals/commit_changes/run_eval.py
```

### 3. Document Changes

```bash
# Explain reasoning in commit message
git commit -m "docs: improve commit prompt with better examples

The previous prompt sometimes generated vague messages.
Added concrete examples and clearer guidelines for:
- Feature additions (what and why)
- Bug fixes (root cause)
- Refactoring (motivation)

Tested on 20+ real-world commits."
```

## Release Process

(For maintainers)

### 1. Version Bump

```bash
# Update version in pyproject.toml
vim pyproject.toml

# Update CHANGELOG.md
vim CHANGELOG.md
```

### 2. Tag Release

```bash
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0
```

### 3. Create GitHub Release

- Use tag
- Add release notes
- Highlight breaking changes

## Getting Help

### Stuck on Something?

1. **Check documentation**: Most questions answered here
2. **Search issues**: Someone may have asked before
3. **Ask in discussion**: GitHub Discussions for questions
4. **Create issue**: If you found a bug or have a feature request

### Communication Channels

- **GitHub Issues**: Bugs, features, questions
- **GitHub Discussions**: General discussion, ideas
- **Pull Requests**: Code review, collaboration

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone.

### Our Standards

**Positive behavior**:
- Using welcoming language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community

**Unacceptable behavior**:
- Trolling or insulting comments
- Public or private harassment
- Publishing others' private information
- Other unethical or unprofessional conduct

### Enforcement

Instances of unacceptable behavior may be reported by creating an issue.

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in relevant commits

## Thank You!

Every contribution makes Best Commits better. Whether it's:
- Reporting a bug
- Suggesting a feature
- Improving documentation
- Submitting code
- Helping others

**Your contribution matters!** 🎉

## Quick Reference

```bash
# Development workflow
git clone https://github.com/yourusername/best-commits.git
cd best-commits
git checkout -b feat/my-feature

# Make changes
vim tools/commit_changes/main.py

# Test
uv run tools/commit_changes/__main__.py

# Evaluate
uv run evals/commit_changes/run_eval.py

# Commit (use the tool!)
uv run tools/review_changes/__main__.py
uv run tools/commit_changes/__main__.py

# Push
git push origin feat/my-feature

# Create PR on GitHub
```

## Further Reading

- [Architecture Guide](/development/architecture) - System design
- [Claude Code Guide](/development/claude) - AI development tips
- [Prompt Engineering](/development/prompt-improvements) - Prompt design
