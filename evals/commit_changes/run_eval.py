#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "litellm>=1.0.0",
#   "rich>=13.0.0",
# ]
# ///

"""Evaluation runner for commit_changes tool."""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from evals.storage import EvalStorage
from litellm import completion
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

JUDGE_MODEL = "claude-sonnet-4-20250514"  # Claude Sonnet 4 for judging
JUDGE_PROMPT = """You are evaluating the quality of an AI-generated commit message.

**Original Git Diff:**
{diff}

**Expected Elements:**
{expected}

**Generated Commit Message:**
{output}

**Evaluation Criteria (100 points total):**
- Conventional format (20 pts): Correct prefix (feat:/fix:/refactor:), summary ≤50 chars
- Clarity (30 pts): Clear, understandable, mentions key changes
- Conciseness (20 pts): No redundant information, focused
- Informativeness (30 pts): Captures what and why, matches diff content

**Your Task:**
1. Score the commit message from 1-100
2. Provide brief reasoning for the score
3. Check which expected elements are present

Respond in JSON format:
{{
  "score": <1-100>,
  "reasoning": "<2-3 sentence explanation>",
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


def generate_commit_message(diff: str, model: str) -> str:
    """Generate commit message using the tool's logic."""
    # Import the actual tool
    from tools.commit_changes.main import generate_commit_message as tool_generate

    # Set the model via environment variable
    original_model = os.getenv("BETTER_COMMIT_MODEL")
    os.environ["BETTER_COMMIT_MODEL"] = model

    try:
        # Simulate the tool's input format
        changes = {
            "status": "M  file1.py\nM  file2.py",
            "diff": diff,
            "staged_diff": diff,
        }

        return tool_generate(changes)
    finally:
        # Restore original model
        if original_model:
            os.environ["BETTER_COMMIT_MODEL"] = original_model
        else:
            os.environ.pop("BETTER_COMMIT_MODEL", None)


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
        return result
    except Exception as e:
        console.print(f"[red]Judge evaluation failed: {e}[/red]")
        return {"score": 0, "reasoning": f"Evaluation error: {e}"}


def run_case(case_name: str, model: str, storage: EvalStorage) -> Dict[str, Any]:
    """Run a single test case."""
    case_path = Path(__file__).parent / case_name

    console.print(f"\n[cyan]Running case: {case_name}[/cyan]")

    # Load test case
    test_data = load_test_case(case_path)

    # Generate commit message
    console.print("[dim]Generating commit message...[/dim]")
    output = generate_commit_message(test_data["diff"], model)

    console.print(Panel(output, title="Generated Commit Message", border_style="blue"))

    # Evaluate
    console.print("[dim]Evaluating with judge model...[/dim]")
    evaluation = evaluate_output(test_data["diff"], output, test_data["expected"])

    score = evaluation.get("score", 0)
    reasoning = evaluation.get("reasoning", "No reasoning provided")

    console.print(f"[bold]Score: {score}/100[/bold]")
    console.print(f"[dim]{reasoning}[/dim]")

    # Store result
    run_id = storage.record_result(
        tool_name="commit_changes",
        case_name=case_name,
        model=model,
        score=score,
        output=output,
        metadata={
            "judge_model": JUDGE_MODEL,
            "evaluation": evaluation,
        }
    )

    return {
        "case": case_name,
        "score": score,
        "output": output,
        "evaluation": evaluation,
        "run_id": run_id,
    }


def show_summary(storage: EvalStorage):
    """Show summary of all results."""
    console.print("\n[bold cyan]Results Summary[/bold cyan]\n")

    # Summary by model
    summary = storage.get_summary(tool_name="commit_changes", group_by="model")

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
    results = storage.get_results(tool_name="commit_changes", limit=5)

    for result in results:
        console.print(
            f"  [{result['timestamp']}] {result['case_name']} - "
            f"{result['model']}: {result['score']}/100"
        )


def main():
    parser = argparse.ArgumentParser(description="Run commit_changes evaluations")
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

    # Summary
    if results:
        avg_score = sum(r["score"] for r in results) / len(results)
        console.print(f"\n[bold green]Average Score: {avg_score:.1f}/100[/bold green]")

        # Show comparison with previous runs
        console.print("\n[bold]Comparison with Previous Results:[/bold]")
        for case in cases:
            comparison = storage.compare_models(
                tool_name="commit_changes",
                case_name=case,
            )
            if len(comparison) > 1:
                console.print(f"\n  {case}:")
                for model, data in comparison.items():
                    console.print(f"    {model}: {data['score']}/100")


if __name__ == "__main__":
    main()
