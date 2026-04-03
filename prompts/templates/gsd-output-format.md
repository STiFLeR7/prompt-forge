# GSD Output Format

How to structure Prompt Forge output when the target execution tool is GSD (Get Shit Done).

GSD's quality depends on what goes into the interview phase. If the initial description is vague, the interview wastes time extracting basics. If it's rich and grounded, the interview goes deeper.

---

## For `/gsd:new-project` or `/gsd:new-milestone`

Structure the input as a rich project brief. This becomes the starting point for GSD's interview.

```
## Project/Feature: [Name]

### What I'm building
[2-3 sentences: what it does, who it's for, why it matters]

### Technical environment
- Runtime: [Node 20, Python 3.12, etc.]
- Framework: [Express 4.18, Next.js 15, Django 5, etc.]
- Database: [PostgreSQL + Prisma 5.x, MongoDB + Mongoose, etc.]
- Auth: [JWT in @src/middleware/auth.ts, OAuth via @src/lib/oauth.ts, etc.]
- Testing: [Jest + Supertest, pattern in @tests/routes/orders.test.ts]
- Key packages: [list with versions from package.json]

### Existing patterns to follow
- API routes follow the pattern in @src/routes/orders.ts
- Services follow @src/services/order-service.ts
- DB access through Prisma client in @src/lib/prisma.ts
- Error handling uses AppError class in @src/lib/errors.ts

### Scope boundaries
IN: [what to build — be specific]
OUT: [what NOT to touch — be explicit]

### Non-functional requirements
- Security: [specific concerns from security lens]
- Performance: [specific requirements from performance lens]
- Compatibility: [what must keep working]

### Success criteria
[Testable statements — "user can do X", "endpoint returns Y when Z"]

### Research findings
[From Prompt Forge's web research — best practices, gotchas, version-specific guidance.
This gives GSD's research agents a head start.]
```

---

## For `/gsd:quick`

Structure as a focused task description. This is what GSD plans and executes directly.

```
[Task description — clear, grounded, 2-3 sentences max]

Technical context: [stack, affected files with @references]
Follow pattern in: @[reference file]
Constraints: [what not to break]
Verify: [test command + what to check]

Research note: [any version-specific gotcha or best practice]
```

---

## Detection Signals

**GSD indicators:**
- `.planning/` directory exists
- `.claude/commands/gsd/` directory with slash command files
- User mentions "gsd", "/gsd:", "planning directory", or "roadmap"
- `SUMMARY.md` or `PROJECT.md` in `.planning/`
