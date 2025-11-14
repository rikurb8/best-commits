# Review work functionality

## What & Why

A `review` command that analyzes uncommitted changes before creating a commit. Provides a quick summary of what changed and suggests improvements (code quality, missing tests, breaking changes, etc.), helping developers catch issues before they commit.

Unlike `commit` which generates the message, `review` focuses on evaluating the changes themselves.

## High-Level Implementation

### 1. Change Analysis
- Collect git diff (staged + unstaged changes, similar to `commit` script)
- Send to Claude with a prompt focused on code review rather than message generation
- Request: summary of changes, potential issues, improvement suggestions

### 2. Interactive Output
- Display AI-generated summary and feedback in terminal
- Present simple prompt: "Proceed with commit? (y/n)"
- If yes, chain directly to `commit` command for message generation
- If no, exit gracefully

### 3. Script Structure
- New `review-changes.py` file following same pattern as `commit-changes.py`
- Different system prompt optimized for code review feedback
- Ignore package-lock.json changes and other unnecessary files that clutter the review process
