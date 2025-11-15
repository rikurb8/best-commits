# Commit Message Evaluation

Evaluates the quality of AI-generated commit messages.

## Usage

```bash
# Run all test cases
uv run evals/commit_changes/run_eval.py

# Run specific case
uv run evals/commit_changes/run_eval.py --case basic_feature

# Test specific model
uv run evals/commit_changes/run_eval.py --model gpt-4o

# View results summary
uv run evals/commit_changes/run_eval.py --summary
```

## Test Cases

### basic_feature
Simple feature addition - expects "feat:" prefix, clear description.

### bugfix
Bug fix scenario - expects "fix:" prefix, mentions the issue being fixed.

### refactor
Code reorganization - expects "refactor:" prefix, clarifies no functional changes.

## Evaluation Criteria

Scored 1-100 by judge model (Claude Sonnet 4.5) based on:
- **Conventional format** (20 pts): Correct prefix, 50-char summary line
- **Clarity** (30 pts): Clear, understandable message
- **Conciseness** (20 pts): No redundant information
- **Informativeness** (30 pts): Captures what and why
