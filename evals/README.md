# Evals

Automated evaluation system for AI-powered Git tools.

## Quick Start

```bash
# Evaluate commit message generation
uv run evals/commit_changes/run_eval.py

# Evaluate code review generation
uv run evals/review_changes/run_eval.py

# View results summary
uv run evals/commit_changes/run_eval.py --summary
uv run evals/review_changes/run_eval.py --summary
```

## Structure

```
evals/
├── storage/              # SQLite-based results storage
│   ├── database.py       # Storage API
│   ├── schema.sql        # Database schema
│   └── README.md         # API documentation
├── commit_changes/       # Commit message evals
│   ├── basic_feature/    # Test: feature addition
│   ├── bugfix/           # Test: bug fix
│   ├── refactor/         # Test: refactoring
│   └── run_eval.py       # Eval runner
└── review_changes/       # Code review evals
    ├── security_issue/   # Test: security vulnerability
    ├── code_quality/     # Test: quality improvements
    ├── breaking_change/  # Test: API breaking changes
    └── run_eval.py       # Eval runner
```

## Usage Examples

### Run All Test Cases
```bash
uv run evals/commit_changes/run_eval.py
uv run evals/review_changes/run_eval.py
```

### Run Specific Test Case
```bash
uv run evals/commit_changes/run_eval.py --case basic_feature
uv run evals/review_changes/run_eval.py --case security_issue
```

### Test Different Models
```bash
uv run evals/commit_changes/run_eval.py --model gpt-4o
uv run evals/commit_changes/run_eval.py --model claude-sonnet-4-5-20250514
```

### View Results Summary
```bash
uv run evals/commit_changes/run_eval.py --summary
uv run evals/review_changes/run_eval.py --summary
```

## How It Works

1. **Test Cases**: Each case contains a sample git diff and expected elements
2. **Tool Execution**: The actual tool (`commit_changes` or `review_changes`) runs on the diff
3. **Judge Evaluation**: Claude Sonnet 4.5 scores the output 1-100 based on criteria
4. **Storage**: Results saved to SQLite database for historical tracking
5. **Comparison**: New results compared against previous runs

## Evaluation Criteria

### Commit Messages (1-100 points)
- **Conventional format** (20 pts): Correct prefix, ≤50 char summary
- **Clarity** (30 pts): Clear, understandable message
- **Conciseness** (20 pts): No redundant information
- **Informativeness** (30 pts): Captures what and why

### Code Reviews (1-100 points)
- **Score accuracy** (25 pts): Gerrit score matches severity
- **Completeness** (25 pts): Covers all aspects
- **Actionability** (25 pts): Clear, specific feedback
- **Tone** (25 pts): Professional, constructive

## Adding New Test Cases

1. Create directory: `evals/{tool_name}/{case_name}/`
2. Add `README.md` (description, expected elements)
3. Add `diff.txt` (sample git diff)
4. Add `expected_elements.json` (evaluation checklist)
5. Run eval: `uv run evals/{tool_name}/run_eval.py --case {case_name}`
