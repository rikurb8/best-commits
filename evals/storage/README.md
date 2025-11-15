# Evaluation Storage

SQLite-based storage for evaluation results with a simple Python API.

## Quick Start

```python
from evals.storage import EvalStorage

storage = EvalStorage()  # Uses evals/storage/results.db

# Record a result
run_id = storage.record_result(
    tool_name="commit_changes",
    case_name="basic_feature",
    model="claude-haiku-4-5-20251001",
    score=85,
    output="feat: add user authentication\n\nImplement JWT-based auth...",
    metrics={"clarity": 90, "conciseness": 80},
    metadata={"judge_model": "claude-sonnet-4-5-20250514"}
)

# Get recent results
results = storage.get_results(tool_name="commit_changes", limit=5)

# Get summary by model
summary = storage.get_summary(tool_name="commit_changes", group_by="model")

# Compare models on a case
comparison = storage.compare_models(
    tool_name="commit_changes",
    case_name="basic_feature"
)
```

## Database Schema

### eval_runs
- `id`: Primary key
- `tool_name`: Tool being evaluated (e.g., "commit_changes")
- `case_name`: Test case name (e.g., "basic_feature")
- `model`: Model identifier
- `timestamp`: When the eval was run
- `score`: Overall score (1-100)
- `output`: Tool output that was evaluated
- `metadata_json`: Additional metadata as JSON

### eval_metrics
- `id`: Primary key
- `run_id`: Foreign key to eval_runs
- `metric_name`: Name of the metric
- `value`: Numeric value
- `details_json`: Optional details as JSON

## API Methods

### `record_result(tool_name, case_name, model, score, output, metrics=None, metadata=None)`
Record an evaluation result. Returns the run ID.

### `get_results(tool_name=None, case_name=None, model=None, limit=10)`
Get evaluation results with optional filtering. Returns list of result dicts.

### `get_summary(tool_name=None, group_by='model')`
Get summary statistics grouped by model or case_name. Returns list with avg/min/max scores.

### `compare_models(tool_name, case_name, models=None)`
Compare model performance on a specific case. Returns dict mapping model to latest result.
