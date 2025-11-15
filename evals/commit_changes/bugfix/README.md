# Bugfix Test Case

Tests commit message generation for a bug fix.

## Scenario
Fixing a null pointer exception in user profile loading.

## Expected Elements
- Prefix: `fix:`
- Summary mentions the bug/issue being fixed
- Summary ≤50 characters
- Optional body explains root cause
- Imperative mood ("Fix" not "Fixed")

## Scoring Rubric
- **90-100**: Clear bug description, proper format
- **75-89**: Good but could be more specific about the bug
- **60-74**: Acceptable but vague about what was fixed
- **Below 60**: Missing fix prefix or unclear what bug was addressed
