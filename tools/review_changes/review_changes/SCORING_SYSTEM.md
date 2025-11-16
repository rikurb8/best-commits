# Gerrit Code-Review Scoring Guide for LLMs

## Score Definitions

| Score  | Label                                           | Meaning                                 | When to Use                                                                                                            |
| ------ | ----------------------------------------------- | --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **+2** | Looks good to me, approved                      | Strong approval, code is ready to merge | Code is well-written, tested, follows standards, and solves the problem correctly. No issues found.                    |
| **+1** | Looks good to me, but someone else must approve | Conditional approval                    | Code looks good but you're not the final authority, or minor concerns exist that don't block merging.                  |
| **0**  | No score                                        | Neutral/comments only                   | Providing feedback, asking questions, or suggesting improvements without blocking.                                     |
| **-1** | I would prefer this is not merged as is         | Request for changes                     | Issues found that should be addressed: bugs, code quality problems, missing tests, unclear logic, or style violations. |
| **-2** | This shall not be merged                        | Strong veto                             | Critical issues: security vulnerabilities, breaking changes, fundamental design flaws, or violates project principles. |

## Review Criteria

When reviewing, consider:

- **Correctness**: Does the code work as intended?
- **Tests**: Are there adequate tests? Do they pass?
- **Code Quality**: Is it readable, maintainable, and follows project conventions?
- **Security**: Are there any security concerns?
- **Performance**: Any performance regressions?
- **Documentation**: Is the change properly documented?
- **Scope**: Does the PR do one thing well, or is it too broad?

## Notes

- **+2** typically requires committer/maintainer status
- Multiple **+1** scores may be required before merge
- A single **-2** blocks merging until resolved or rescinded
