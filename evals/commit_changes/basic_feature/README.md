# Basic Feature Test Case

Tests commit message generation for a simple feature addition.

## Scenario
Adding a new user authentication module with JWT token support.

## Expected Elements
- Prefix: `feat:`
- Summary mentions "authentication" or "auth"
- Summary ≤50 characters
- Optional body explains JWT implementation
- Imperative mood ("Add" not "Added")

## Scoring Rubric
- **90-100**: Perfect conventional commit, clear and concise
- **75-89**: Good message, minor issues with length or detail
- **60-74**: Acceptable but could be clearer or more concise
- **Below 60**: Missing key elements or poor quality
