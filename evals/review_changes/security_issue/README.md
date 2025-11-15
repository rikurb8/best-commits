# Security Issue Test Case

Tests code review for security vulnerability (SQL injection).

## Scenario
Code that builds SQL queries using string concatenation instead of parameterized queries.

## Expected Elements
- Gerrit score: -1 or -2
- Issues section mentions "SQL injection" or "security"
- Severity: "critical" or "high"
- Suggests using parameterized queries
- No approval in summary

## Scoring Rubric
- **90-100**: Correctly identifies security risk, appropriate negative score, clear remediation
- **75-89**: Identifies issue but score/severity could be stronger
- **60-74**: Mentions security concern but lacks specificity
- **Below 60**: Misses security vulnerability or gives positive score
