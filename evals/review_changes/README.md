# Code Review Evaluation

Evaluates the quality of AI-generated code reviews.

## Usage

```bash
# Run all test cases
uv run evals/review_changes/run_eval.py

# Run specific case
uv run evals/review_changes/run_eval.py --case security_issue

# Test specific model
uv run evals/review_changes/run_eval.py --model gpt-4o

# View results summary
uv run evals/review_changes/run_eval.py --summary
```

## Test Cases

### security_issue
Code with SQL injection vulnerability - expects negative Gerrit score, security warnings.

### code_quality
Good functionality with style/quality issues - expects neutral/positive score, constructive suggestions.

### breaking_change
API change that breaks compatibility - expects "Breaking Changes" section populated.

## Evaluation Criteria

Scored 1-100 by judge model (Claude Sonnet 4.5) based on:
- **Score accuracy** (25 pts): Gerrit score (-2 to +2) matches severity
- **Completeness** (25 pts): Covers all aspects (correctness, quality, tests, docs)
- **Actionability** (25 pts): Clear, specific, actionable feedback
- **Tone** (25 pts): Professional, constructive, balanced
