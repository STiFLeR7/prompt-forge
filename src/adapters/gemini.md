# Gemini Adapter

Formats Prompt Forge output for Google Gemini models (Gemini CLI, Gemini API, AI Studio).

## Role Definition

Gemini responds well to clear role framing and benefits from structured markdown. It handles long context well and supports grounding with Google Search.

```
Role: Senior software engineer performing a focused task on this codebase.
Approach: Read all relevant files first, then plan your approach, then implement.
Standard: Production-quality code that follows existing project patterns.
```

## Instruction Structure

Gemini works best with this layout:

1. **Role and approach** — Set the persona and methodology upfront
2. **Context** — Background information, stack details, file references
3. **Task** — Clear, numbered steps with explicit ordering
4. **Rules** — Constraints as a bulleted list with "MUST" / "MUST NOT" language
5. **Output format** — What to deliver and how to verify

### Markdown Structure

Gemini parses markdown headers and lists reliably. Use them for structure:

```markdown
## Context
Express 4.18 app with Prisma 5.x and PostgreSQL.
Auth handled by JWT middleware in `src/middleware/auth.ts`.

## Task
1. Add rate limiting to `/api/login`
2. Limit to 5 attempts per IP per 15-minute window
3. Use the existing Redis connection in `src/lib/redis.ts`

## Rules
- MUST NOT add new dependencies
- MUST NOT change the existing error response format
- MUST follow the middleware pattern in `src/middleware/auth.ts`

## Verification
- Run `npm test` — all tests pass
- Run `npm run lint` — no new warnings
```

## Constraint Formatting

Gemini responds best to constraints when they use:
- **MUST / MUST NOT** language — stronger signal than "don't" or "avoid"
- **Rules section** — separated clearly from the task itself
- **Positive + negative pairs** — "MUST use Prisma client, MUST NOT write raw SQL"
- **Numbered priority** — if constraints conflict, number them by importance

## Output Expectations

Gemini benefits from explicit output structure requests:

```
## Expected Output
1. Modified files with changes explained
2. Test results from `npm test`
3. Summary of approach taken and any trade-offs
```

## File Reference Convention

Gemini CLI uses backtick paths. Always use:
- `src/routes/orders.ts` not "the orders route file"
- Include relative paths from project root

## Grounding Note

Gemini has native Google Search grounding. For research-heavy prompts, you can include:
```
Use Google Search to verify current best practices for [topic] before implementing.
```

## Mode Adjustments for Gemini

| Mode | Gemini-Specific Emphasis |
|------|------------------------|
| build | Numbered step-by-step, explicit pattern references with file paths |
| audit | MUST/MUST NOT rules list, checklist output format |
| debug | "Analyze → Hypothesize → Verify → Fix" — explicit methodology steps |
| research | Leverage search grounding, ask for alternatives with trade-off tables |
| optimize | Request measurement data in structured table format before/after |
