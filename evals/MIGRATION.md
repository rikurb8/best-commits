# Migration Guide: Custom Eval System to DeepEval

This guide explains the migration from the custom evaluation system to DeepEval.

## What Changed

### Before (Custom System)
- Custom `run_eval.py` scripts for each tool
- Manual LLM judge implementation with custom prompts
- Custom SQLite storage layer
- Results stored in database with comparison tools
- Run via: `uv run evals/commit_changes/run_eval.py`

### After (DeepEval)
- DeepEval-based test suite with `test_*.py` files
- DeepEval's GEval metric for standardized evaluation
- Built-in reporting with optional cloud dashboards
- Standard test framework with pass/fail assertions
- Run via: `deepeval test run` (recommended) or `pytest`

## Key Benefits

1. **Standardization**: Uses industry-standard LLM evaluation framework (DeepEval)
2. **Better Tooling**: DeepEval CLI with parallel execution and cloud reporting
3. **Clearer Results**: Pass/fail based on thresholds instead of just scores
4. **Easier Extension**: Simple to add new metrics and test cases
5. **CI/CD Integration**: Native support in most CI/CD platforms
6. **Parallel Execution**: Run tests faster with `-n` flag
7. **Cloud Dashboards**: Optional integration with Confident AI platform

## Migration Steps

### For Users

1. **Install new dependencies**:
   ```bash
   cd evals
   uv pip install -e .
   ```

2. **Run tests instead of scripts**:
   ```bash
   # Old way
   uv run evals/commit_changes/run_eval.py --case basic_feature

   # New way (recommended)
   deepeval test run commit_changes/test_commit_eval.py::test_commit_message_generation[basic_feature]

   # Or with pytest (also works)
   pytest commit_changes/test_commit_eval.py::test_commit_message_generation[basic_feature] -v
   ```

3. **View results**:
   ```bash
   # Old way
   uv run evals/commit_changes/run_eval.py --summary

   # New way (recommended)
   deepeval test run  # Shows pass/fail with DeepEval reporting

   # Optional: cloud dashboard
   deepeval login  # One-time setup
   deepeval test run  # Automatically syncs to cloud

   # Or with pytest
   pytest commit_changes/ -v
   ```

### For Developers

1. **Test case structure remains the same**:
   - Still use `diff.txt` and `expected_elements.json`
   - Test cases are automatically discovered
   - No changes needed to existing test case directories

2. **Adding new test cases**:
   ```bash
   # Old way: Create files, then run script
   mkdir evals/commit_changes/new_case
   # Add files...
   uv run evals/commit_changes/run_eval.py --case new_case

   # New way: Create files, DeepEval auto-discovers
   mkdir evals/commit_changes/new_case
   # Add files...
   deepeval test run commit_changes/test_commit_eval.py  # Automatically finds and runs new case
   ```

3. **Customizing evaluation**:
   ```python
   # Old way: Modify JUDGE_PROMPT in run_eval.py
   JUDGE_PROMPT = """Your custom prompt..."""

   # New way: Modify GEval metric in test file
   commit_message_metric = GEval(
       name="commit_message_quality",
       criteria="Your custom criteria...",
       threshold=0.7,
   )
   ```

## Backwards Compatibility

The old `run_eval.py` scripts are **deprecated but still functional**. They are kept for backwards compatibility and will be removed in a future version.

If you need the old behavior:
```bash
uv run evals/commit_changes/run_eval.py  # Still works
```

However, we recommend migrating to the new DeepEval-based system.

## Database Storage

The old SQLite storage system (`evals/storage/`) is deprecated. DeepEval provides better result storage and reporting:

- **Test results**: `deepeval test run` automatically tracks results
- **Cloud dashboards**: `deepeval login` + `deepeval test run` syncs to Confident AI
- **Historical tracking**: Use CI/CD pipeline artifacts or Confident AI platform
- **Comparison**: Built-in comparison in cloud dashboards

If you need to access old results:
```python
from evals.storage import EvalStorage
storage = EvalStorage()
results = storage.get_results(tool_name="commit_changes", limit=10)
```

## Environment Variables

No changes - the same environment variables work:

- `BETTER_COMMIT_MODEL`: Model to evaluate
- `ANTHROPIC_API_KEY`: Anthropic API key
- `OPENAI_API_KEY`: OpenAI API key
- `JUDGE_MODEL`: Judge model (new, defaults to `gpt-4o`)

## Common Issues

### "No module named 'deepeval'"
```bash
cd evals && uv pip install -e .
```

### "No tests collected"
Make sure you're in the `evals` directory and test files are named `test_*.py`.

### "API key not found"
Set required API keys:
```bash
export ANTHROPIC_API_KEY=your-key
export OPENAI_API_KEY=your-key  # Required for judge model
```

## Need Help?

- DeepEval Documentation: https://docs.confident-ai.com/
- Pytest Documentation: https://docs.pytest.org/
- Open an issue: https://github.com/rikurb8/best-commits/issues
