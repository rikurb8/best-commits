"""Pytest configuration for DeepEval tests."""

import os
import sys
from pathlib import Path

import pytest

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def pytest_configure(config):
    """Configure pytest for DeepEval."""
    # Register custom markers
    config.addinivalue_line("markers", "commit: tests for commit message generation")
    config.addinivalue_line("markers", "review: tests for code review generation")


@pytest.fixture(autouse=True)
def setup_environment():
    """Ensure required environment variables are set."""
    # Check for API keys (either for model under test or judge model)
    api_keys = [
        "ANTHROPIC_API_KEY",
        "OPENAI_API_KEY",
        "GIT_API_KEY",  # Legacy support
    ]

    has_key = any(os.getenv(key) for key in api_keys)

    if not has_key:
        pytest.skip("No API key found. Set ANTHROPIC_API_KEY or OPENAI_API_KEY")
