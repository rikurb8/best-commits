# Prompt Improvements Summary

## Overview
The prompts have been extracted from the Python code into separate `PROMPT.md` files within each tool module. This separation provides better maintainability, version control, and collaboration opportunities.

## Changes Made

### 1. File Structure
```
tools/
├── commit_changes/
│   ├── PROMPT.md          # NEW: Commit message generation prompt
│   ├── __init__.py
│   ├── __main__.py
│   └── main.py            # UPDATED: Now loads prompt from PROMPT.md
└── review_changes/
    ├── PROMPT.md          # NEW: Code review prompt
    ├── __init__.py
    ├── __main__.py
    └── main.py            # UPDATED: Now loads prompt from PROMPT.md
```

### 2. Code Changes
Both `main.py` files now include:
- `load_prompt_template()` function to read PROMPT.md
- Fallback to embedded prompt if file not found (for backwards compatibility)
- Dynamic prompt construction combining template + git changes

## Key Improvements to Prompts

### Commit Message Prompt (`tools/commit_changes/PROMPT.md`)

**Structural Enhancements:**
1. **Clear role definition**: Establishes the AI as an "expert git commit message generator"
2. **Context section**: Explicitly explains what data will be provided
3. **Comprehensive guidelines**: Expanded from 5 rules to detailed sections covering:
   - Structure (summary + optional body)
   - All conventional commit prefixes with descriptions
   - Best practices (7 specific points)
   - Examples of good commit messages

**Content Improvements:**
- Added examples for different scenarios (simple feature, bug fix, refactoring, multiple changes)
- Explicit output format instructions to avoid markdown fences
- Example input/output pair showing expected transformation
- Emphasis on "WHAT and WHY, not HOW"
- Character limits clearly stated (50 for summary, 72 for body wrapping)

**Benefits:**
- More consistent commit message quality
- Better handling of complex multi-file changes
- Clearer guidance on when to use which prefix
- Reduced need for post-processing (markdown stripping)

### Code Review Prompt (`tools/review_changes/PROMPT.md`)

**Structural Enhancements:**
1. **Expert persona**: Positions AI as senior code reviewer with specific expertise areas
2. **Focus areas**: 7 prioritized review dimensions (correctness, security, performance, etc.)
3. **Review principles**: 6 guidelines for constructive feedback
4. **Anti-patterns**: Explicitly states what NOT to focus on

**Content Improvements:**
- **Severity levels**: Introduced 🔴 Critical, 🟡 Warning, 🔵 Info categorization
- **Structured output**: 5 clear sections (Summary, Issues, Suggestions, Breaking Changes, Positive Highlights)
- **Example output**: Full markdown example showing desired format
- **Tone guidance**: Professional, constructive, educational approach
- **Context awareness**: Notes that lock files are pre-filtered

**Benefits:**
- More actionable and prioritized feedback
- Better balance between thoroughness and pragmatism
- Encourages positive reinforcement for good practices
- Clearer communication of severity and urgency
- More educational for junior developers

## Technical Implementation

### Prompt Loading Pattern
```python
def load_prompt_template() -> str:
    """Load the prompt template from PROMPT.md file."""
    prompt_file = Path(__file__).parent / "PROMPT.md"
    try:
        return prompt_file.read_text()
    except FileNotFoundError:
        # Fallback to embedded prompt if file not found
        return """[simplified embedded prompt]"""
```

**Advantages:**
- Uses relative path resolution (`Path(__file__).parent`)
- Graceful degradation with fallback
- No performance impact (file read on each invocation is negligible)
- Easy to test different prompts without code changes

### Prompt Composition
```python
prompt = f"""{prompt_template}

---

## Git Changes to Analyze

**Git Status:**
{changes['status']}

**Staged Changes:**
{changes['staged_diff']}

**Unstaged Changes:**
{changes['diff']}"""
```

**Advantages:**
- Clean separation between template and data
- Markdown structure makes it readable for debugging
- Easy to modify data format without touching prompt logic

## Benefits of Extraction

### For Development
1. **Version Control**: Prompt changes tracked separately from code logic
2. **A/B Testing**: Easy to experiment with different prompts
3. **Collaboration**: Non-developers (PMs, tech writers) can improve prompts
4. **Review**: Prompt changes reviewed independently in PRs

### For Users
1. **Customization**: Users can modify prompts without touching Python code
2. **Transparency**: Clear understanding of what instructions are sent to AI
3. **Sharing**: Teams can share and standardize prompts across projects
4. **Debugging**: Easier to diagnose prompt-related issues

### For Maintenance
1. **Single Responsibility**: Code handles logic, prompts handle AI instruction
2. **Testing**: Can test prompt variations without code changes
3. **Documentation**: Prompts serve as self-documenting specifications
4. **Iteration**: Faster iteration on prompt quality

## Future Enhancements

### Potential Additions
1. **Prompt Variables**: Support for user-configurable sections (e.g., custom rules)
2. **Multi-Language**: Support for prompts in different languages
3. **Prompt Versioning**: Allow users to choose between different prompt strategies
4. **Contextual Prompts**: Different prompts based on project type (backend/frontend/ML)
5. **Few-Shot Examples**: Include project-specific example commits/reviews

### Advanced Features
1. **Prompt Templates**: Allow users to override with custom PROMPT.md in their repos
2. **Prompt Composition**: Combine base prompt + project-specific additions
3. **Prompt Analytics**: Track which prompt versions produce best results
4. **Interactive Prompt Builder**: CLI tool to customize prompts interactively

## Migration Guide

### For Existing Users
No action required! The code automatically:
1. Tries to load PROMPT.md
2. Falls back to embedded prompt if not found
3. Works identically to previous version

### For Prompt Customization
1. Navigate to `tools/commit_changes/PROMPT.md` or `tools/review_changes/PROMPT.md`
2. Edit the markdown file
3. Save and test with `uv run tools/commit_changes/__main__.py`
4. No need to reinstall or restart anything

### For Development
When adding new tools:
1. Create `PROMPT.md` in the tool directory
2. Add `load_prompt_template()` function
3. Build full prompt with template + data
4. Include fallback for backwards compatibility

## Comparison: Before vs After

### Before
```python
# Prompt embedded in code
prompt = f"""You are a git commit message generator...
[5 simple rules]
Return ONLY the commit message text."""
```

**Issues:**
- Hard to modify without code changes
- No examples or detailed guidance
- Mixed concerns (code + AI instruction)
- Difficult to review prompt changes

### After
```python
# Prompt loaded from file
prompt_template = load_prompt_template()
prompt = f"""{prompt_template}
---
## Git Changes to Analyze
{changes['status']}..."""
```

**Improvements:**
- ✅ Prompts in dedicated markdown files
- ✅ Rich examples and guidelines
- ✅ Separation of concerns
- ✅ Easy to review and customize
- ✅ Backwards compatible

## Conclusion

Extracting prompts to PROMPT.md files provides:
- **Better prompt quality** through comprehensive guidelines and examples
- **Easier maintenance** via separation of concerns
- **User empowerment** through simple customization
- **Team collaboration** on prompt improvements
- **Future flexibility** for advanced prompt strategies

The implementation maintains full backwards compatibility while opening up new possibilities for prompt engineering and customization.
