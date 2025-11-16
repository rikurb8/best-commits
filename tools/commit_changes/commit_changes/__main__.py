#!/usr/bin/env python3
"""
Automated Git Commit Generator using AI

Entry point for the commit command. This script delegates to the main
implementation in commit_changes.main module.

The package must be installed to use this command. Install with:
  uv tool install ./tools/commit_changes
  # or
  uv tool install git+https://github.com/rikurb8/best-commits.git#subdirectory=tools/commit_changes

For development without installation, use:
  uvx --from ./tools/commit_changes commit
  # or
  uv run -m commit_changes
"""

from commit_changes import main

if __name__ == "__main__":
    main()
