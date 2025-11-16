#!/usr/bin/env python3
"""
AI-Powered Git Changes Review

Entry point for the review command. This script delegates to the main
implementation in review_changes.main module.

The package must be installed to use this command. Install with:
  uv tool install ./tools/review_changes
  # or
  uv tool install git+https://github.com/rikurb8/best-commits.git#subdirectory=tools/review_changes

For development without installation, use:
  uvx --from ./tools/review_changes review
  # or
  uv run -m review_changes
"""

from review_changes import main

if __name__ == "__main__":
    main()
