# Claude Adapter

Formats Prompt Forge output for Anthropic Claude models (Claude Code, Claude API, Claude chat).

## Role Definition

Claude responds best to direct, structured instructions with explicit constraints. It follows XML tags reliably and benefits from chain-of-thought prompting.

```
You are a senior software engineer working on this codebase. Follow instructions precisely.
Read all referenced files before making changes. Verify your work after each step.
```

## Instruction Structure

Claude excels with this layout:

1. **Preamble** — Read project context first (`@CLAUDE.md`, referenced files)
2. **Context block** — Background, stack, current state (use XML `<context>` tags for complex prompts)
3. **Task block** — Clear, imperative instructions (use XML `<task>` tags)
4. **Constraints block** — What NOT to do (use XML `<constraints>` tags)
5. **Verification block** — Feedback loop commands (test, lint, typecheck)

### XML Tag Usage

Claude reliably parses XML structure. Use it for multi-section prompts:

```xml
<context>
Express 4.18 + Prisma 5.x + PostgreSQL. Auth via JWT in @src/middleware/auth.ts.
</context>

<task>
Add rate limiting to /api/login. Limit to 5 attempts per IP per 15-minute window.
</task>

<constraints>
- Use existing Redis connection in @src/lib/redis.ts
- Do not add new dependencies
- Preserve existing error response format
</constraints>

<verification>
Run `npm test` after changes. Fix any failures before completing.
Run `npm run lint` — no new warnings.
</verification>
```

For simple prompts, skip XML — plain markdown with clear sections works fine.

## Constraint Formatting

Claude respects constraints best when they are:
- **Explicit and negative** — "Do NOT modify auth.ts" over "be careful with auth.ts"
- **Positioned after the task** — constraints after instructions reduce accidental ignoring
- **Grouped together** — one constraints section, not scattered throughout
- **Explained briefly** — "Do NOT use class components — project migrated to hooks in Q3" is stronger than "Do NOT use class components"

## Output Expectations

Tell Claude what format to deliver results in:

```
After implementing:
1. Run `npm test` — report pass/fail
2. Run `npm run typecheck` — report any errors
3. Summarize what you changed and why
```

Claude benefits from explicit feedback loops — "run X, then fix any issues" produces 2-3x better results than "make sure it works."

## @ Reference Convention

Claude Code uses `@filename` to reference files. Always use this syntax:
- `@src/routes/orders.ts` not "the orders route file"
- `@CLAUDE.md` not "the project conventions"

## Mode Adjustments for Claude

| Mode | Claude-Specific Emphasis |
|------|-------------------------|
| build | Reference existing patterns with @ syntax, step-by-step with test gates |
| audit | XML `<constraints>` block, explicit negative instructions, checklist format |
| debug | "Explain what's wrong before fixing" — Claude naturally supports chain-of-thought |
| research | "Read these files, then explain" — leverage Claude's strong comprehension |
| optimize | "Profile first, propose second, implement third" — explicit ordering |
