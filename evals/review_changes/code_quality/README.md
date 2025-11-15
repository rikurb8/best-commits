# Code Quality Test Case

Tests code review for quality and style improvements.

## Scenario
Functional code that works but has quality issues (long function, no error handling, magic numbers).

## Expected Elements
- Gerrit score: 0 or +1 (works but could be better)
- Issues section with medium/low severity items
- Suggestions for improvement (error handling, constants, etc.)
- Balanced tone (acknowledges it works)

## Scoring Rubric
- **90-100**: Balanced review, identifies quality issues, constructive suggestions
- **75-89**: Good feedback but tone could be more balanced
- **60-74**: Identifies issues but lacks constructive suggestions
- **Below 60**: Too harsh/lenient, misses key quality concerns
