"""SQLite storage layer for evaluation results."""

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class EvalStorage:
    """Manages storage of evaluation results in SQLite."""

    def __init__(self, db_path: Optional[Path] = None):
        """Initialize storage with database path.

        Args:
            db_path: Path to SQLite database file. Defaults to evals/storage/results.db
        """
        if db_path is None:
            db_path = Path(__file__).parent / "results.db"
        self.db_path = Path(db_path)
        self._ensure_schema()

    def _ensure_schema(self):
        """Create database schema if it doesn't exist."""
        schema_path = Path(__file__).parent / "schema.sql"
        with self._get_connection() as conn:
            conn.executescript(schema_path.read_text())
            conn.commit()

    @contextmanager
    def _get_connection(self):
        """Get database connection as context manager."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def record_result(
        self,
        tool_name: str,
        case_name: str,
        model: str,
        score: int,
        output: str,
        metrics: Optional[Dict[str, float]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> int:
        """Record an evaluation result.

        Args:
            tool_name: Name of the tool being evaluated (e.g., 'commit_changes')
            case_name: Name of the test case (e.g., 'basic_feature')
            model: Model identifier (e.g., 'claude-haiku-4-5-20251001')
            score: Overall score (1-100)
            output: Tool output that was evaluated
            metrics: Dict of metric name -> value pairs
            metadata: Additional metadata to store as JSON

        Returns:
            Run ID of the inserted record
        """
        metadata_json = json.dumps(metadata) if metadata else None

        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO eval_runs (tool_name, case_name, model, score, output, metadata_json)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (tool_name, case_name, model, score, output, metadata_json),
            )
            run_id = cursor.lastrowid

            # Insert metrics if provided
            if metrics:
                for metric_name, value in metrics.items():
                    conn.execute(
                        """
                        INSERT INTO eval_metrics (run_id, metric_name, value)
                        VALUES (?, ?, ?)
                        """,
                        (run_id, metric_name, value),
                    )

            conn.commit()
            return run_id

    def get_results(
        self,
        tool_name: Optional[str] = None,
        case_name: Optional[str] = None,
        model: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """Get evaluation results with optional filtering.

        Args:
            tool_name: Filter by tool name
            case_name: Filter by case name
            model: Filter by model
            limit: Maximum number of results to return

        Returns:
            List of result dictionaries
        """
        conditions = []
        params = []

        if tool_name:
            conditions.append("tool_name = ?")
            params.append(tool_name)
        if case_name:
            conditions.append("case_name = ?")
            params.append(case_name)
        if model:
            conditions.append("model = ?")
            params.append(model)

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        with self._get_connection() as conn:
            cursor = conn.execute(
                f"""
                SELECT id, tool_name, case_name, model, timestamp, score,
                       output, metadata_json
                FROM eval_runs
                {where_clause}
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                params + [limit],
            )

            results = []
            for row in cursor.fetchall():
                result = dict(row)
                if result["metadata_json"]:
                    result["metadata"] = json.loads(result["metadata_json"])
                    del result["metadata_json"]
                results.append(result)

            return results

    def get_summary(
        self,
        tool_name: Optional[str] = None,
        group_by: str = "model",
    ) -> List[Dict[str, Any]]:
        """Get summary statistics grouped by model or case.

        Args:
            tool_name: Filter by tool name
            group_by: Group by 'model' or 'case_name'

        Returns:
            List of summary dictionaries with avg_score, min_score, max_score, count
        """
        if group_by not in ["model", "case_name"]:
            raise ValueError("group_by must be 'model' or 'case_name'")

        where_clause = "WHERE tool_name = ?" if tool_name else ""
        params = [tool_name] if tool_name else []

        with self._get_connection() as conn:
            cursor = conn.execute(
                f"""
                SELECT
                    {group_by},
                    AVG(score) as avg_score,
                    MIN(score) as min_score,
                    MAX(score) as max_score,
                    COUNT(*) as count
                FROM eval_runs
                {where_clause}
                GROUP BY {group_by}
                ORDER BY avg_score DESC
                """,
                params,
            )

            return [dict(row) for row in cursor.fetchall()]

    def compare_models(
        self,
        tool_name: str,
        case_name: str,
        models: Optional[List[str]] = None,
    ) -> Dict[str, Dict[str, Any]]:
        """Compare model performance on a specific case.

        Args:
            tool_name: Tool name to compare
            case_name: Case name to compare
            models: List of models to compare (None = all models)

        Returns:
            Dict mapping model name to latest result
        """
        conditions = ["tool_name = ?", "case_name = ?"]
        params = [tool_name, case_name]

        if models:
            placeholders = ",".join("?" * len(models))
            conditions.append(f"model IN ({placeholders})")
            params.extend(models)

        where_clause = " AND ".join(conditions)

        with self._get_connection() as conn:
            # Get latest result for each model
            cursor = conn.execute(
                f"""
                SELECT model, score, timestamp, output
                FROM eval_runs
                WHERE {where_clause}
                  AND id IN (
                      SELECT MAX(id)
                      FROM eval_runs
                      WHERE {where_clause}
                      GROUP BY model
                  )
                ORDER BY score DESC
                """,
                params + params,  # WHERE clause appears twice
            )

            results = {}
            for row in cursor.fetchall():
                model = row["model"]
                results[model] = dict(row)

            return results
