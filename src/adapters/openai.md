# OpenAI Adapter

Formats Prompt Forge output for OpenAI models (GPT-4o, o1/o3, Codex, ChatGPT).

## Role Definition

OpenAI models respond strongly to system-level role definition. Set the persona clearly:

```
You are a senior software engineer. You write clean, tested, production-ready code.
You follow existing project patterns exactly. You verify your work before reporting completion.
```

## Instruction Structure

OpenAI models work best with this layout:

1. **System context** — Role + project background (maps to system message in API)
2. **User task** — Direct, imperative instructions
3. **Constraints** — Boundaries and prohibitions as a clear list
4. **Examples** — Few-shot examples when pattern-following is critical
5. **Output specification** — What format to deliver in

### System/User Split

For API usage, structure maps naturally to message roles:

```
[System]
You are a senior engineer working on an Express 4.18 + Prisma 5.x + PostgreSQL app.
Project conventions: services are class-based, routes use Zod validation,
errors follow AppError pattern in src/lib/errors.ts.

[User]
Add rate limiting to /api/login. Limit to 5 attempts per IP per 15-minute window.

Requirements:
- Use existing Redis connection in src/lib/redis.ts
- Do not add new dependencies
- Preserve existing error response format
- Follow middleware pattern in src/middleware/auth.ts

After implementing, run `npm test` and fix any failures.
```

For chat/agent usage, combine into a single structured prompt with clear sections.

## Constraint Formatting

OpenAI models respect constraints best when:
- **Listed explicitly** — bullet points, not embedded in prose
- **Negative constraints are bolded** — "**Do NOT** modify auth.ts"
- **Placed after the task** — instructions first, then boundaries
- **Few-shot reinforced** — if a constraint is critical, show an example of correct behavior

## Output Expectations

OpenAI models benefit from explicit format requests:

```
Output format:
1. List of files changed
2. For each file: what changed and why
3. Test results
4. Any concerns or follow-up items
```

For code generation, specify: "Write complete, runnable code — not pseudocode or snippets."

## File Reference Convention

Use standard path notation:
- `src/routes/orders.ts` not "the orders file"
- Include full relative paths from project root
- For multi-file tasks, list all files upfront

## Few-Shot Patterns

OpenAI models benefit significantly from examples. When the task requires following a specific pattern:

```
Example of the pattern to follow (from src/routes/orders.ts):
- Router definition at top
- Zod schema for validation
- Auth middleware in chain
- Service call, not direct DB access
- JSON response with consistent format

Now apply this same pattern to create src/routes/payments.ts.
```

## Mode Adjustments for OpenAI

| Mode | OpenAI-Specific Emphasis |
|------|------------------------|
| build | Few-shot examples from codebase, explicit pattern references |
| audit | Bold **DO NOT** constraints, checklist output with pass/fail |
| debug | Chain-of-thought: "Think step by step about what could cause this" |
| research | Request structured comparison tables, pros/cons format |
| optimize | Ask for profiling analysis before implementation, metrics-focused |
