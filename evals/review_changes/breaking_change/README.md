# Breaking Change Test Case

Tests code review detection of breaking API changes.

## Scenario
Function signature change that breaks existing API contract.

## Expected Elements
- Gerrit score: -1, 0, or +1 (depends on if it's justified)
- "Breaking Changes" section populated
- Mentions API compatibility concern
- Suggests migration path or versioning

## Scoring Rubric
- **90-100**: Clearly identifies breaking change, discusses impact, suggests mitigation
- **75-89**: Identifies breaking change but lacks migration guidance
- **60-74**: Mentions compatibility but doesn't highlight it properly
- **Below 60**: Misses the breaking change entirely
