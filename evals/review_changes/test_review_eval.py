"""Deepeval-based evaluation tests for review_changes tool."""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Any

import pytest
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def load_test_case(case_name: str) -> Dict[str, Any]:
    """Load test case data from directory."""
    case_path = Path(__file__).parent / case_name
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


# Discover all test cases
def get_test_cases():
    """Discover all test case directories."""
    cases_dir = Path(__file__).parent
    return [
        d.name
        for d in cases_dir.iterdir()
        if d.is_dir() and (d / "diff.txt").exists()
    ]


def get_code_review_metric():
    """Create the evaluation metric (lazy initialization to avoid API key issues at import time)."""
    judge_model = os.getenv("JUDGE_MODEL", "gpt-4o")

    return GEval(
        name="code_review_quality",
        criteria=(
            "Evaluate the quality of an AI-generated code review based on: "
            "1. Score accuracy (25%): Gerrit score (-2 to +2) matches severity of issues. "
            "2. Completeness (25%): Covers correctness, quality, tests, documentation. "
            "3. Actionability (25%): Clear, specific, actionable feedback. "
            "4. Tone (25%): Professional, constructive, balanced."
        ),
        evaluation_params=[
            LLMTestCaseParams.INPUT,
            LLMTestCaseParams.ACTUAL_OUTPUT,
            LLMTestCaseParams.EXPECTED_OUTPUT,
        ],
        threshold=0.7,  # 70% threshold for passing
        model=judge_model,  # Judge model
    )


# Parametrize tests for all cases
@pytest.mark.review
@pytest.mark.parametrize("case_name", get_test_cases())
def test_code_review_generation(case_name: str):
    """Test code review generation with deepeval."""
    # Get model from environment or use default
    model = os.getenv("BETTER_COMMIT_MODEL", "claude-haiku-4-5-20251001")

    # Load test case
    test_data = load_test_case(case_name)

    # Generate review
    actual_output = generate_review(test_data["diff"], model)

    # Extract Gerrit score for additional validation
    gerrit_score = extract_gerrit_score(actual_output)

    # Add Gerrit score info to expected output for evaluation
    expected_with_gerrit = test_data["expected"].copy()
    expected_with_gerrit["note"] = f"Review should provide a Gerrit score (-2 to +2)"

    # Create deepeval test case
    test_case = LLMTestCase(
        input=test_data["diff"],
        actual_output=actual_output,
        expected_output=json.dumps(expected_with_gerrit, indent=2),
    )

    # Get metric (lazy initialization)
    code_review_metric = get_code_review_metric()

    # Assert using deepeval
    assert_test(test_case, [code_review_metric])

    # Additional assertion for Gerrit score validity
    assert -2 <= gerrit_score <= 2, (
        f"Gerrit score {gerrit_score} out of valid range (-2 to +2)"
    )


if __name__ == "__main__":
    # Allow running as standalone script
    pytest.main([__file__, "-v", "--tb=short"])
