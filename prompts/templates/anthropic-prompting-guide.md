# Anthropic Prompting Best Practices — Quick Reference

Distills Anthropic's official prompting documentation into actionable patterns for Claude Code prompt construction.

## 1. Core Principles

**Clarity wins.** Claude responds to clear, explicit instructions. Vagueness produces vague results. Show your prompt to a colleague with minimal context — if they'd be confused, Claude will be too.

**Context improves everything.** Providing motivation behind an instruction helps Claude make better judgment calls. Instead of "validate the input," say "validate the input — we've had injection attacks on this endpoint before."

**Specificity over length.** A short, specific prompt outperforms a long, vague one.

## 2. Structuring with XML Tags

For complex prompts, XML tags help Claude parse different sections:

```xml
<context>
We're building a REST API in Express + TypeScript.
</context>

<task>
Add rate limiting to the /api/login endpoint.
</task>

<constraints>
- Use the existing Redis connection in src/lib/redis.ts
- Don't add new dependencies
</constraints>

<verification>
Run `npm test -- --grep "rate limit"` after implementation.
</verification>
```

## 3. Few-Shot Examples

When you want Claude to follow a specific pattern, include 3-5 examples. Use for: commit message formatting, code style, API response structures, error handling patterns.

## 4. Chain of Thought

For complex decisions, ask Claude to think through its approach before coding:
- "Before making changes, explain your approach and which files you'll modify."
- "Analyze the current implementation, identify the bug, explain what's wrong, then fix it."

## 5. Long Context Handling

- **Put longform data at the top** of the prompt, above your instructions (up to 30% quality improvement).
- **Queries at the end** perform best with complex, multi-document inputs.
- **Reference specific locations** rather than relying on Claude to find things.

## 6. Agentic / Claude Code-Specific Patterns

### Give Claude a feedback loop
The single highest-impact pattern (2-3x quality improvement):
- "Run the existing test suite after making changes."
- "Run `npm run lint` after changes and fix any issues."
- "Check that the TypeScript compiler reports no errors."

### Use @ references and explicit paths
- `@src/middleware/auth.ts` instead of "the auth middleware"
- Paste screenshots for UI work
- Give URLs for API documentation

### Session management
- Start fresh sessions for distinct tasks
- If corrections exceed two attempts, restart with a clearer prompt

### Plan mode for complex work
- Use for multi-file changes and architectural decisions
- Skip for small, single-file tasks

### Subagents for parallel work
- Include "use subagents" for parallelizable tasks
- Make them feature-specific, not generic

## 7. Grounding: The Anti-Hallucination Layer

### Code grounding checklist
Before the prompt references ANY code artifact, verify:
- [ ] File path exists and is spelled correctly
- [ ] Function/method name matches the actual declaration
- [ ] Parameter names and types match the signature
- [ ] Import paths match what the codebase uses
- [ ] Test commands actually exist in package.json / Makefile

### Research grounding checklist
Before recommending ANY external approach, verify:
- [ ] The API/method is not deprecated in the project's version
- [ ] The package is compatible with the project's runtime
- [ ] The pattern works with existing architecture
- [ ] Security recommendations are current

### Common grounding failures

| Failure | What happens | Fix |
|---------|-------------|-----|
| Wrong function name | Claude creates duplicate or edits wrong function | Read the actual file |
| Wrong file path | Claude wastes tokens searching | Check directory structure |
| Outdated API reference | Code breaks at runtime | Search current docs |
| Wrong test command | Feedback loop fails | Check package.json scripts |
| Assumed patterns | Code looks foreign | Read 2-3 existing examples |

## 8. Common Anti-Patterns

- **Vague scope:** "Fix the bugs" — Claude doesn't know which bugs or when to stop.
- **Missing success criteria:** "Add caching" — Cached where? What eviction strategy?
- **No constraints:** "Refactor the API" — Claude might rewrite everything.
- **Compound tasks without structure:** Break into steps or use plan mode.
- **Assuming Claude knows your codebase:** Be explicit about files, patterns, conventions.
- **Over-prompting simple tasks:** Match prompt complexity to task complexity.

## 9. CLAUDE.md Best Practices

**What belongs:** Build/test/lint commands, code style, architecture overview, framework decisions, branch conventions, common gotchas.

**What does NOT belong:** Task-specific instructions, things Claude can infer from reading code, rigid rules without explanations.

**Sizing:** Keep under 150 lines of meaningful instructions. Use `.claude/rules/` for overflow. Use `<critical>` tags for non-negotiable rules.
