#!/usr/bin/env -S uvx --quiet --with anthropic --with rich
# /// script
# dependencies = [
#   "anthropic>=0.40.0",
#   "rich>=13.0.0",
# ]
# ///

"""
AI-Powered Git Changes Review using Claude API

This script:
1. Analyzes current uncommitted git changes
2. Sends the diff to Claude API (Haiku 4.5) for code review
3. Displays summary, potential issues, and improvement suggestions
4. Optionally proceeds to commit with message generation

Prerequisites:
- Git repository with changes
- GIT_API_KEY environment variable set with Anthropic API key

Usage:
  ./review-changes.py
  # or with env var inline:
  GIT_API_KEY=your_key ./review-changes.py
  # or with uvx:
  uvx review-changes.py
"""

import os
import subprocess
import sys
from typing import Dict

from anthropic import Anthropic
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()


def run_git_command(*args: str) -> str:
    """Run a git command and return its output."""
    try:
        result = subprocess.run(
            ["git"] + list(args), capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Git command failed: {e.stderr}[/red]")
        raise


def has_uncommitted_changes() -> bool:
    """Check if there are uncommitted changes."""
    status = run_git_command("status", "--porcelain")
    return len(status.strip()) > 0


def get_git_changes() -> Dict[str, str]:
    """Get git diff and status information."""
    status = run_git_command("status", "--short")
    diff = run_git_command("diff")
    staged_diff = run_git_command("diff", "--staged")

    return {"status": status, "diff": diff, "staged_diff": staged_diff}


def should_ignore_file(filename: str) -> bool:
    """Determine if a file should be ignored in the review."""
    ignore_patterns = [
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        "poetry.lock",
        "Cargo.lock",
        "Gemfile.lock",
        ".lock",
    ]
    return any(pattern in filename for pattern in ignore_patterns)


def filter_diff_content(diff: str) -> str:
    """Filter out changes from files that should be ignored."""
    if not diff:
        return diff

    lines = diff.split("\n")
    filtered_lines = []
    skip_current_file = False

    for line in lines:
        # Check for new file diff header
        if line.startswith("diff --git"):
            # Extract filename from the diff header
            parts = line.split(" ")
            if len(parts) >= 4:
                filename = parts[-1].replace("b/", "")
                skip_current_file = should_ignore_file(filename)

        if not skip_current_file:
            filtered_lines.append(line)

    return "\n".join(filtered_lines)


def review_changes(changes: Dict[str, str]) -> str:
    """Call Claude API to review code changes."""
    api_key = os.getenv("GIT_API_KEY")

    if not api_key:
        raise ValueError("GIT_API_KEY environment variable is not set")

    # Filter out lock files and other unnecessary changes
    filtered_staged = filter_diff_content(changes["staged_diff"])
    filtered_unstaged = filter_diff_content(changes["diff"])

    prompt = f"""You are an expert code reviewer. Analyze the following git changes and provide constructive feedback.

Git Status:
{changes["status"]}

Staged Changes:
{filtered_staged or "(no staged changes)"}

Unstaged Changes:
{filtered_unstaged or "(no unstaged changes)"}

Please provide a code review with the following sections:

1. **Summary**: Brief overview of what changed (1-2 sentences)
2. **Potential Issues**: Any bugs, security concerns, or problems you notice
3. **Suggestions**: Code quality improvements, missing tests, refactoring opportunities
4. **Breaking Changes**: Any changes that might break existing functionality

Be concise but thorough. Focus on actionable feedback. If everything looks good, say so!

Format your response in markdown."""

    client = Anthropic(api_key=api_key)

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    if response.content and len(response.content) > 0:
        return response.content[0].text.strip()
    else:
        raise ValueError("No content in Claude API response")


def prompt_user_to_commit() -> bool:
    """Ask user if they want to proceed with commit."""
    console.print()
    response = (
        console.input("[cyan]Proceed with commit? (y/n): [/cyan]").strip().lower()
    )
    return response in ["y", "yes"]


def run_commit_script() -> None:
    """Run the commit-changes.py script."""
    console.print("\n[cyan]🚀 Running commit script...[/cyan]\n")

    # Check if 'commit' command exists in PATH
    commit_path = subprocess.run(
        ["which", "commit"], capture_output=True, text=True
    ).returncode

    if commit_path != 0:
        console.print(
            "[red]❌ Error: 'commit' command not found in PATH.[/red]\n"
            "[yellow]Please ensure the commit script is installed and available in your PATH.[/yellow]\n"
            "[yellow]You may need to install it or add its location to your PATH environment variable.[/yellow]"
        )
        sys.exit(1)

    try:
        subprocess.run(["commit"], check=True)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Commit script failed with exit code {e.returncode}[/red]")
        sys.exit(e.returncode)


def main() -> None:
    """Main execution function."""
    try:
        console.print("[cyan]🔍 Checking for uncommitted changes...[/cyan]\n")

        if not has_uncommitted_changes():
            console.print(
                "[yellow]No uncommitted changes found. Nothing to review.[/yellow]"
            )
            sys.exit(0)

        changes = get_git_changes()

        console.print("[cyan]📊 Current changes:[/cyan]")
        console.print(Panel(changes["status"], title="Git Status", border_style="cyan"))
        console.print()

        console.print("[cyan]🤖 Analyzing changes with Claude API...[/cyan]\n")

        review_feedback = review_changes(changes)

        console.print(
            Panel(
                Markdown(review_feedback),
                title="📋 Code Review",
                border_style="blue",
                padding=(1, 2),
            )
        )

        # Ask if user wants to proceed with commit
        if prompt_user_to_commit():
            run_commit_script()
        else:
            console.print(
                "\n[yellow]Commit cancelled. Review your changes and run again when ready.[/yellow]"
            )
            sys.exit(0)

    except ValueError as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        sys.exit(1)
    except subprocess.CalledProcessError:
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Review cancelled by user.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]❌ Unexpected error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
