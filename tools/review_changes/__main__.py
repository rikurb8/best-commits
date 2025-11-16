#!/usr/bin/env python3
"""
AI-Powered Git Changes Review

Entry point for the review command. This script delegates to the main
implementation in tools.review_changes.main module.

The package must be installed to use this command. Install with:
  uv tool install .
  # or
  uv tool install git+https://github.com/rikurb8/best-commits.git

For development without installation, use:
  uvx --from . review
  # or
  uv run -m tools.review_changes
"""

from tools.review_changes import main

if __name__ == "__main__":
    main()
