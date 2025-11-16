"""Deepeval-based evaluation tests for commit_changes tool."""

import json
import os
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


def generate_commit_message(diff: str, model: str) -> str:
    """Generate commit message using the tool's logic."""
    from tools.commit_changes.commit_changes.main import generate_commit_message as tool_generate

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


# Discover all test cases
def get_test_cases():
    """Discover all test case directories."""
    cases_dir = Path(__file__).parent
    return [
        d.name
        for d in cases_dir.iterdir()
        if d.is_dir() and (d / "diff.txt").exists()
    ]


def get_commit_message_metric():
    """Create the evaluation metric (lazy initialization to avoid API key issues at import time)."""
    judge_model = os.getenv("JUDGE_MODEL", "gpt-4o")

    return GEval(
        name="commit_message_quality",
        criteria=(
            "Evaluate the quality of an AI-generated commit message based on: "
            "1. Conventional format (20%): Correct prefix (feat:/fix:/refactor:), summary ≤50 chars. "
            "2. Clarity (30%): Clear, understandable, mentions key changes. "
            "3. Conciseness (20%): No redundant information, focused. "
            "4. Informativeness (30%): Captures what and why, matches diff content."
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
@pytest.mark.commit
@pytest.mark.parametrize("case_name", get_test_cases())
def test_commit_message_generation(case_name: str):
    """Test commit message generation with deepeval."""
    # Get model from environment or use default
    model = os.getenv("BETTER_COMMIT_MODEL", "claude-haiku-4-5-20251001")

    # Load test case
    test_data = load_test_case(case_name)

    # Generate commit message
    actual_output = generate_commit_message(test_data["diff"], model)

    # Create deepeval test case
    test_case = LLMTestCase(
        input=test_data["diff"],
        actual_output=actual_output,
        expected_output=json.dumps(test_data["expected"], indent=2),
    )

    # Get metric (lazy initialization)
    commit_message_metric = get_commit_message_metric()

    # Assert using deepeval
    assert_test(test_case, [commit_message_metric])


if __name__ == "__main__":
    # Allow running as standalone script
    pytest.main([__file__, "-v", "--tb=short"])
