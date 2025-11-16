# Evals

Automated evaluation system for AI-powered Git tools using [DeepEval](https://docs.confident-ai.com/).

## Quick Start

```bash
# Install dependencies
cd evals && uv pip install -e .

# Run all evaluations
pytest

# Run commit message evaluations only
pytest commit_changes/test_commit_eval.py -v

# Run code review evaluations only
pytest review_changes/test_review_eval.py -v

# Run a specific test case
pytest commit_changes/test_commit_eval.py::test_commit_message_generation[basic_feature] -v
```

## Structure

```
evals/
├── pyproject.toml        # Package config with deepeval dependency
├── conftest.py           # Pytest/deepeval configuration
├── storage/              # Legacy SQLite storage (deprecated)
│   ├── database.py       # Storage API
│   ├── schema.sql        # Database schema
│   └── README.md         # API documentation
├── commit_changes/       # Commit message evals
│   ├── basic_feature/    # Test: feature addition
│   ├── bugfix/           # Test: bug fix
│   ├── refactor/         # Test: refactoring
│   ├── test_commit_eval.py  # Deepeval test suite
│   └── run_eval.py       # Legacy eval runner (deprecated)
└── review_changes/       # Code review evals
    ├── security_issue/   # Test: security vulnerability
    ├── code_quality/     # Test: quality improvements
    ├── breaking_change/  # Test: API breaking changes
    ├── test_review_eval.py  # Deepeval test suite
    └── run_eval.py       # Legacy eval runner (deprecated)
```

## Migration to DeepEval

This evaluation suite has been migrated from a custom evaluation system to DeepEval, providing:

- **Standard Testing Framework**: Uses pytest for test discovery and execution
- **Built-in Metrics**: Leverages DeepEval's GEval metric for LLM-based evaluation
- **Better Reporting**: Integrated test results and detailed failure analysis
- **Easier Extension**: Simple to add new test cases and metrics

### Legacy Scripts

The old `run_eval.py` scripts and SQLite storage are deprecated but kept for backwards compatibility. Use the new pytest-based tests instead.

## Usage Examples

### Run All Tests
```bash
cd evals
pytest -v
```

### Run Specific Tool Tests
```bash
# Commit message tests
pytest commit_changes/ -v

# Code review tests
pytest review_changes/ -v
```

### Run Specific Test Case
```bash
pytest commit_changes/test_commit_eval.py::test_commit_message_generation[basic_feature] -v
pytest review_changes/test_review_eval.py::test_code_review_generation[security_issue] -v
```

### Test Different Models
```bash
# Set model via environment variable
BETTER_COMMIT_MODEL=gpt-4o pytest commit_changes/ -v
BETTER_COMMIT_MODEL=claude-sonnet-4-20250514 pytest commit_changes/ -v
```

### Generate Test Report
```bash
# Generate HTML report
pytest --html=report.html --self-contained-html

# Generate JSON report for CI/CD
pytest --json-report --json-report-file=report.json
```

## How It Works

1. **Test Cases**: Each case contains a sample git diff and expected elements
2. **Tool Execution**: The actual tool (`commit_changes` or `review_changes`) runs on the diff
3. **DeepEval Metrics**: GEval metric uses an LLM judge (GPT-4) to score outputs based on criteria
4. **Assertions**: Tests pass/fail based on configurable thresholds (default: 70%)
5. **Reporting**: Standard pytest output with detailed failure analysis

## Evaluation Criteria

### Commit Messages
DeepEval's GEval metric evaluates commit messages based on:

- **Conventional format** (20%): Correct prefix (feat:/fix:/refactor:), summary ≤50 chars
- **Clarity** (30%): Clear, understandable message
- **Conciseness** (20%): No redundant information
- **Informativeness** (30%): Captures what and why

Threshold: 70% (0.7) - Tests pass if the score is above this threshold.

### Code Reviews
DeepEval's GEval metric evaluates code reviews based on:

- **Score accuracy** (25%): Gerrit score (-2 to +2) matches severity of issues
- **Completeness** (25%): Covers correctness, quality, tests, documentation
- **Actionability** (25%): Clear, specific, actionable feedback
- **Tone** (25%): Professional, constructive, balanced

Threshold: 70% (0.7) - Tests pass if the score is above this threshold.

## Adding New Test Cases

1. Create directory: `evals/{tool_name}/{case_name}/`
2. Add `README.md` (description of the test case)
3. Add `diff.txt` (sample git diff to test)
4. Add `expected_elements.json` (evaluation checklist)
5. The test will be automatically discovered and run with: `pytest {tool_name}/ -v`

Example:
```bash
mkdir -p evals/commit_changes/new_case
echo "feat: add new feature" > evals/commit_changes/new_case/diff.txt
echo '{"elements": ["mentions feature", "uses feat: prefix"]}' > evals/commit_changes/new_case/expected_elements.json
pytest commit_changes/ -v
```

## Configuration

### Environment Variables

- `BETTER_COMMIT_MODEL`: Model to evaluate (default: `claude-haiku-4-5-20251001`)
- `JUDGE_MODEL`: Judge model for evaluation (default: `gpt-4o`)
- `ANTHROPIC_API_KEY`: Anthropic API key
- `OPENAI_API_KEY`: OpenAI API key (required for default judge model)

### Customizing Metrics

You can customize the evaluation criteria by modifying the GEval metric in the test files:

```python
commit_message_metric = GEval(
    name="commit_message_quality",
    criteria="Your custom criteria here...",
    threshold=0.7,  # Adjust threshold as needed
    model="gpt-4o",  # Change judge model if desired
)
```

## Integration with CI/CD

The evaluation suite can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run evaluations
  run: |
    cd evals
    uv pip install -e .
    pytest --json-report --json-report-file=results.json
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```
