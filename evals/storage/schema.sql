-- Evaluation runs table
CREATE TABLE IF NOT EXISTS eval_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_name TEXT NOT NULL,
    case_name TEXT NOT NULL,
    model TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    score INTEGER NOT NULL,
    metadata_json TEXT,
    output TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_eval_runs_tool ON eval_runs(tool_name);
CREATE INDEX IF NOT EXISTS idx_eval_runs_case ON eval_runs(case_name);
CREATE INDEX IF NOT EXISTS idx_eval_runs_model ON eval_runs(model);
CREATE INDEX IF NOT EXISTS idx_eval_runs_timestamp ON eval_runs(timestamp);

-- Evaluation metrics table
CREATE TABLE IF NOT EXISTS eval_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    metric_name TEXT NOT NULL,
    value REAL NOT NULL,
    details_json TEXT,
    FOREIGN KEY (run_id) REFERENCES eval_runs(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_eval_metrics_run ON eval_metrics(run_id);
CREATE INDEX IF NOT EXISTS idx_eval_metrics_name ON eval_metrics(metric_name);
