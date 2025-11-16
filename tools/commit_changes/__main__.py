#!/usr/bin/env python3
"""
Automated Git Commit Generator using AI

Entry point for the commit command. This script delegates to the main
implementation in tools.commit_changes.main module.

The package must be installed to use this command. Install with:
  uv tool install .
  # or
  uv tool install git+https://github.com/rikurb8/best-commits.git

For development without installation, use:
  uvx --from . commit
  # or
  uv run -m tools.commit_changes
"""

from tools.commit_changes import main

if __name__ == "__main__":
    main()
