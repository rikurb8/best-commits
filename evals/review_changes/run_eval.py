#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "litellm>=1.0.0",
#   "rich>=13.0.0",
# ]
# ///

"""Evaluation runner for review_changes tool."""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from evals.storage import EvalStorage
from litellm import completion
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

console = Console()

JUDGE_MODEL = "claude-sonnet-4-20250514"  # Claude Sonnet 4 for judging
JUDGE_PROMPT = """You are evaluating the quality of an AI-generated code review.

**Original Git Diff:**
{diff}

**Expected Elements:**
{expected}

**Generated Review:**
{output}

**Evaluation Criteria (100 points total):**
- Score accuracy (25 pts): Gerrit score (-2 to +2) matches severity of issues
- Completeness (25 pts): Covers correctness, quality, tests, documentation
- Actionability (25 pts): Clear, specific, actionable feedback
- Tone (25 pts): Professional, constructive, balanced

**Your Task:**
1. Score the review from 1-100
2. Provide brief reasoning
3. Check which expected elements are present
4. Extract the Gerrit score from the review (look for "Score:" or similar)

Respond in JSON format:
{{
  "score": <1-100>,
  "reasoning": "<2-3 sentence explanation>",
  "gerrit_score": <-2 to +2>,
  "elements_present": ["element1", "element2"],
  "elements_missing": ["element3"]
}}"""


def load_test_case(case_path: Path) -> Dict[str, Any]:
    """Load test case data."""
    diff_path = case_path / "diff.txt"
    expected_path = case_path / "expected_elements.json"

    if not diff_path.exists() or not expected_path.exists():
        raise FileNotFoundError(f"Missing required files in {case_path}")

    return {
        "diff": diff_path.read_text(),
        "expected": json.loads(expected_path.read_text()),
    }


def generate_review(diff: str, model: str) -> str:
    """Generate code review using the tool's logic."""
    # Import the actual tool
    from tools.review_changes.review_changes.main import review_changes as tool_review

    # Set the model via environment variable
    original_model = os.getenv("BETTER_COMMIT_MODEL")
    os.environ["BETTER_COMMIT_MODEL"] = model

    try:
        # Simulate the tool's input format
        changes = {
            "status": "A  file.py",
            "diff": diff,
            "staged_diff": diff,
        }

        return tool_review(changes)
    finally:
        # Restore original model
        if original_model:
            os.environ["BETTER_COMMIT_MODEL"] = original_model
        else:
            os.environ.pop("BETTER_COMMIT_MODEL", None)


def extract_gerrit_score(review: str) -> int:
    """Extract Gerrit score from review text."""
    # Look for patterns like "Score: +1" or "**Score:** -2"
    patterns = [
        r"Score:\s*([+-]?\d+)",
        r"\*\*Score:\*\*\s*([+-]?\d+)",
        r"Gerrit Score:\s*([+-]?\d+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, review, re.IGNORECASE)
        if match:
            return int(match.group(1))

    # Fallback: look for standalone +2, +1, 0, -1, -2 near beginning
    lines = review.split("\n")[:10]
    for line in lines:
        if re.match(r"^[+-]?[012]$", line.strip()):
            return int(line.strip())

    return 0  # Default if not found


def evaluate_output(diff: str, output: str, expected: Dict) -> Dict[str, Any]:
    """Use judge model to evaluate the output."""
    prompt = JUDGE_PROMPT.format(
        diff=diff,
        expected=json.dumps(expected, indent=2),
        output=output
    )

    try:
        response = completion(
            model=JUDGE_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )

        result = json.loads(response.choices[0].message.content)

        # Also extract Gerrit score from actual review
        actual_gerrit = extract_gerrit_score(output)
        result["actual_gerrit_score"] = actual_gerrit

        return result
    except Exception as e:
        console.print(f"[red]Judge evaluation failed: {e}[/red]")
        return {
            "score": 0,
            "reasoning": f"Evaluation error: {e}",
            "gerrit_score": 0,
        }


def run_case(case_name: str, model: str, storage: EvalStorage) -> Dict[str, Any]:
    """Run a single test case."""
    case_path = Path(__file__).parent / case_name

    console.print(f"\n[cyan]Running case: {case_name}[/cyan]")

    # Load test case
    test_data = load_test_case(case_path)

    # Generate review
    console.print("[dim]Generating code review...[/dim]")
    output = generate_review(test_data["diff"], model)

    # Display review (truncate if too long)
    display_output = output if len(output) < 2000 else output[:2000] + "\n\n[...truncated...]"
    console.print(Panel(Markdown(display_output), title="Generated Review", border_style="blue"))

    # Evaluate
    console.print("[dim]Evaluating with judge model...[/dim]")
    evaluation = evaluate_output(test_data["diff"], output, test_data["expected"])

    score = evaluation.get("score", 0)
    reasoning = evaluation.get("reasoning", "No reasoning provided")
    gerrit_score = evaluation.get("actual_gerrit_score", 0)

    console.print(f"[bold]Judge Score: {score}/100[/bold]")
    console.print(f"[bold]Gerrit Score: {gerrit_score:+d}[/bold]")
    console.print(f"[dim]{reasoning}[/dim]")

    # Store result
    run_id = storage.record_result(
        tool_name="review_changes",
        case_name=case_name,
        model=model,
        score=score,
        output=output,
        metadata={
            "judge_model": JUDGE_MODEL,
            "gerrit_score": gerrit_score,
            "evaluation": evaluation,
        }
    )

    return {
        "case": case_name,
        "score": score,
        "gerrit_score": gerrit_score,
        "output": output,
        "evaluation": evaluation,
        "run_id": run_id,
    }


def show_summary(storage: EvalStorage):
    """Show summary of all results."""
    console.print("\n[bold cyan]Results Summary[/bold cyan]\n")

    # Summary by model
    summary = storage.get_summary(tool_name="review_changes", group_by="model")

    if not summary:
        console.print("[yellow]No results found[/yellow]")
        return

    table = Table(title="Scores by Model")
    table.add_column("Model", style="cyan")
    table.add_column("Avg Score", justify="right", style="green")
    table.add_column("Min", justify="right")
    table.add_column("Max", justify="right")
    table.add_column("Count", justify="right")

    for row in summary:
        table.add_row(
            row["model"],
            f"{row['avg_score']:.1f}",
            str(row["min_score"]),
            str(row["max_score"]),
            str(row["count"]),
        )

    console.print(table)

    # Recent results
    console.print("\n[bold]Recent Results[/bold]")
    results = storage.get_results(tool_name="review_changes", limit=5)

    for result in results:
        metadata = result.get("metadata", {})
        gerrit = metadata.get("gerrit_score", "?")
        console.print(
            f"  [{result['timestamp']}] {result['case_name']} - "
            f"{result['model']}: {result['score']}/100 (Gerrit: {gerrit:+d})"
        )


def main():
    parser = argparse.ArgumentParser(description="Run review_changes evaluations")
    parser.add_argument("--case", help="Specific case to run (default: all)")
    parser.add_argument(
        "--model",
        default=os.getenv("BETTER_COMMIT_MODEL", "claude-haiku-4-5-20251001"),
        help="Model to evaluate",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show summary of results and exit",
    )

    args = parser.parse_args()

    storage = EvalStorage()

    if args.summary:
        show_summary(storage)
        return

    # Find cases to run
    cases_dir = Path(__file__).parent
    if args.case:
        cases = [args.case]
    else:
        cases = [
            d.name for d in cases_dir.iterdir()
            if d.is_dir() and (d / "diff.txt").exists()
        ]

    console.print(f"[bold]Evaluating model:[/bold] {args.model}")
    console.print(f"[bold]Test cases:[/bold] {', '.join(cases)}")

    # Run cases
    results = []
    for case in cases:
        try:
            result = run_case(case, args.model, storage)
            results.append(result)
        except Exception as e:
            console.print(f"[red]Error running {case}: {e}[/red]")
            import traceback
            traceback.print_exc()

    # Summary
    if results:
        avg_score = sum(r["score"] for r in results) / len(results)
        console.print(f"\n[bold green]Average Score: {avg_score:.1f}/100[/bold green]")

        # Show comparison with previous runs
        console.print("\n[bold]Comparison with Previous Results:[/bold]")
        for case in cases:
            comparison = storage.compare_models(
                tool_name="review_changes",
                case_name=case,
            )
            if len(comparison) > 1:
                console.print(f"\n  {case}:")
                for model, data in comparison.items():
                    console.print(f"    {model}: {data['score']}/100")


if __name__ == "__main__":
    main()
