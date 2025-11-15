#!/usr/bin/env -S uvx --quiet --with litellm --with rich
# /// script
# dependencies = [
#   "litellm>=1.0.0",
#   "rich>=13.0.0",
# ]
# ///

"""
Automated Git Commit Generator using AI

This script:
1. Analyzes current uncommitted git changes
2. Sends the diff to an AI model (default: Claude Haiku 4.5)
3. Generates an informative commit message
4. Creates the git commit

Prerequisites:
- Git repository with changes
- API key for your chosen model (see documentation for provider-specific keys)
- Optional: BETTER_COMMIT_MODEL environment variable to specify model

Usage:
  ./commit-changes.py
  # or with custom model:
  BETTER_COMMIT_MODEL=gpt-4 OPENAI_API_KEY=your_key ./commit-changes.py
  # or with uvx:
  uvx commit-changes.py
"""

import os
import sys
import subprocess
from typing import Dict, Optional
from litellm import completion
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def get_model_name() -> str:
    """Get the AI model to use from environment variable or default."""
    return os.getenv("BETTER_COMMIT_MODEL", "claude-haiku-4-5-20251001")


def setup_api_keys() -> None:
    """Setup API keys for backward compatibility with GIT_API_KEY."""
    # For backwards compatibility, if GIT_API_KEY is set and ANTHROPIC_API_KEY is not,
    # use GIT_API_KEY as ANTHROPIC_API_KEY
    if os.getenv("GIT_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        os.environ["ANTHROPIC_API_KEY"] = os.environ["GIT_API_KEY"]


def run_git_command(*args: str) -> str:
    """Run a git command and return its output."""
    try:
        result = subprocess.run(
            ["git"] + list(args),
            capture_output=True,
            text=True,
            check=True
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

    return {
        "status": status,
        "diff": diff,
        "staged_diff": staged_diff
    }


def generate_commit_message(changes: Dict[str, str]) -> str:
    """Call AI API to generate commit message."""
    model = get_model_name()

    prompt = f"""You are a git commit message generator. Analyze the following git changes and create a clear, informative commit message.

Git Status:
{changes['status']}

Staged Changes:
{changes['staged_diff'] or '(no staged changes)'}

Unstaged Changes:
{changes['diff'] or '(no unstaged changes)'}

Rules for the commit message:
1. First line: Brief summary (50 chars or less) in imperative mood (e.g., "Add feature" not "Added feature")
2. If needed, add a blank line then a detailed description
3. Focus on WHAT changed and WHY, not HOW
4. Be concise but informative
5. Use conventional commit prefixes if appropriate (feat:, fix:, docs:, refactor:, test:, chore:)

Return ONLY the commit message text, nothing else. Do not include any explanations or markdown formatting."""

    try:
        response = completion(
            model=model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        if response.choices and len(response.choices) > 0:
            message = response.choices[0].message.content.strip()

            # Strip markdown code fences if present
            import re
            message = re.sub(r'^```[a-z]*\n?', '', message, flags=re.IGNORECASE)
            message = re.sub(r'\n?```$', '', message, flags=re.IGNORECASE)

            return message.strip()
        else:
            raise ValueError("No content in AI API response")
    except Exception as e:
        # Provide helpful error message for missing API keys
        error_msg = str(e)
        if "api key" in error_msg.lower() or "authentication" in error_msg.lower():
            console.print(f"[red]API authentication failed for model '{model}'[/red]")
            console.print("[yellow]Make sure you have set the appropriate API key environment variable.[/yellow]")
            console.print("[yellow]See documentation for required credentials for your model.[/yellow]")
        raise


def stage_all_changes() -> None:
    """Stage all changes."""
    console.print("[yellow]Staging all changes...[/yellow]")
    run_git_command("add", "-A")


def create_commit(message: str) -> None:
    """Create git commit with the generated message."""
    run_git_command("commit", "-m", message)
    console.print("\n[green]✓ Commit created successfully![/green]")


def main() -> None:
    """Main execution function."""
    try:
        # Setup API keys for backwards compatibility
        setup_api_keys()

        console.print("[cyan]🔍 Checking for uncommitted changes...[/cyan]\n")

        if not has_uncommitted_changes():
            console.print("[yellow]No uncommitted changes found. Nothing to commit.[/yellow]")
            sys.exit(0)

        changes = get_git_changes()

        console.print("[cyan]📊 Current changes:[/cyan]")
        console.print(Panel(changes["status"], title="Git Status", border_style="cyan"))
        console.print()

        # Stage all changes if there are unstaged or untracked files
        if changes["diff"].strip() or changes["status"].strip():
            stage_all_changes()
            # Get updated changes after staging
            staged_diff = run_git_command("diff", "--staged")
            changes["staged_diff"] = staged_diff
            changes["diff"] = ""

        model = get_model_name()
        console.print(f"[cyan]🤖 Generating commit message with {model}...[/cyan]\n")

        commit_message = generate_commit_message(changes)

        console.print("[cyan]📝 Generated commit message:[/cyan]")
        console.print(Panel(
            Text(commit_message, style="white"),
            title="Commit Message",
            border_style="green"
        ))
        console.print()

        console.print("[cyan]💾 Creating commit...[/cyan]")
        create_commit(commit_message)

    except ValueError as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        sys.exit(1)
    except subprocess.CalledProcessError:
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]❌ Unexpected error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
