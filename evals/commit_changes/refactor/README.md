# Refactor Test Case

Tests commit message generation for code refactoring.

## Scenario
Extracting database logic into a separate service class.

## Expected Elements
- Prefix: `refactor:`
- Summary mentions what was refactored
- Summary ≤50 characters
- Optional body clarifies no functional changes
- Imperative mood ("Extract" not "Extracted")

## Scoring Rubric
- **90-100**: Clear refactor description, notes no behavior change
- **75-89**: Good but could clarify scope of refactoring
- **60-74**: Acceptable but unclear what was refactored
- **Below 60**: Wrong prefix or suggests functional changes
