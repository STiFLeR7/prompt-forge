# Task-Type Prompt Blueprints

Each task type has a different prompt structure because each type requires different thinking from Claude Code. The prompt shape signals the right mode.

Every blueprint includes a docs-check preamble — Claude Code should read the relevant project CLAUDE.md before starting work.

---

## 1. Bug Fix / Debugging

**Thinking mode:** Investigate first, understand the root cause, then fix. Never guess-and-patch.

```
Before starting, read @CLAUDE.md for project conventions.

## Bug report
[What's happening — symptoms, error messages, reproduction steps]

## Expected behavior
[What should happen instead]

## Affected code
[Specific files/functions where the bug likely lives — grounded from code analysis]

## Investigation steps
1. First, reproduce the issue by [specific steps/commands]
2. Read and understand the relevant code path: [grounded file list]
3. Identify the root cause — explain what's wrong and why before writing any fix
4. Check if this same bug pattern exists elsewhere in the codebase
5. Implement the fix
6. Verify the fix resolves the issue without introducing regressions

## Constraints
- Do NOT apply a surface-level patch — find and fix the root cause
- Do NOT modify [files/modules that should stay untouched]
- Preserve existing behavior for [related functionality]

## Verification
- Run `[actual test command from project]` — all tests must pass
- Specifically test: [the exact scenario that was broken]
- Run `[lint/typecheck command]` — no new warnings
```

---

## 2. New Feature / Implementation

**Thinking mode:** Follow existing patterns, build incrementally, verify as you go.

```
Before starting, read @CLAUDE.md for project conventions.

## Context
[What part of the app, current state, why this feature is needed — business context]

## Feature requirements
[Clear description of what to build]

## Pattern reference
Follow the existing implementation pattern in @[reference file] for:
- [Routing / API structure]
- [Validation approach]
- [Error handling]
- [Response format]
- [Test structure]

## Implementation plan
1. [Step-by-step breakdown — each step is a verifiable unit]
2. After each step, run `[test command]` to verify nothing broke
3. [Continue steps...]

## Scope boundaries
- IN scope: [explicit list]
- OUT of scope: [explicit list]
- Do NOT refactor existing code unless directly necessary

## Technical notes
- [Version-specific guidance from web research]
- [Dependency notes]
- [Architecture notes from code analysis]

## Done criteria
- [ ] Feature works as described
- [ ] Tests written and passing: `[test command]`
- [ ] Types/interfaces updated
- [ ] No lint errors: `[lint command]`
- [ ] Follows existing patterns — code should look like it belongs
```

---

## 3. Refactor / Code Improvement

**Thinking mode:** Understand deeply, change structure without changing behavior, verify continuously.

```
Before starting, read @CLAUDE.md for project conventions.

## Current state
[What the code looks like now — specific files, the problem with the current structure]

## Desired state
[What the code should look like after — structural improvement, not new behavior]

## The rule: behavior must not change
This is a refactor, not a feature. External behavior must remain identical. Every existing test must continue to pass at every step.

## Files in scope
[Explicit grounded list]

## Files NOT in scope — do not modify
[Explicit list]

## Approach
1. First, run `[test command]` to establish a green baseline
2. [First refactor step — small, verifiable]
3. Run tests again — must still pass
4. [Next step]
5. Run tests again
6. [Continue — never more than one structural change between test runs]

## Verification
- All existing tests pass: `[test command]`
- No new lint warnings: `[lint command]`
- No type errors: `[typecheck command]`
- Git diff should show structural changes only — no behavior changes
```

---

## 4. Migration / Upgrade

**Thinking mode:** Incremental, backwards-compatible, rollback-aware. Never big-bang.

```
Before starting, read @CLAUDE.md for project conventions.

## Migration overview
[What's being migrated — from X to Y, why, what's at stake]

## Current stack
- [Framework/library]: [current version]
- [Relevant config files]
- [Current patterns in use]

## Target stack
- [Framework/library]: [target version]
- [New patterns to adopt]
- [Deprecations to address]

## Migration strategy: incremental, not big-bang

### Phase 1: Preparation
1. [Setup step — install new dependency alongside old]
2. Verify existing tests still pass: `[test command]`

### Phase 2: Gradual migration
1. [Migrate one module as a pilot]
2. Test thoroughly: `[test command]`
3. [Continue one at a time]

### Phase 3: Cleanup
1. [Remove old dependencies/code]
2. [Update configs]
3. Final full test run

## Known gotchas
[Version-specific issues from web research — breaking changes, renamed APIs]

## Verification
- Full test suite passes at each phase: `[test command]`
- No deprecation warnings from [target framework]
```

---

## 5. Performance Optimization

**Thinking mode:** Measure first, optimize the bottleneck, verify improvement with numbers.

```
Before starting, read @CLAUDE.md for project conventions.

## Performance problem
[What's slow — specific endpoint, operation, or page. Include metrics if available]

## Affected code
[Grounded file paths and functions]

## Investigation first — do NOT optimize before profiling
1. Read and trace the full execution path
2. Identify the actual bottleneck — DB queries? Network calls? Computation? Memory?
3. If there are N+1 queries, count them
4. Explain the bottleneck and proposed optimization before implementing

## Optimization constraints
- Do NOT change external API/behavior
- Do NOT add new dependencies without mentioning it first
- Readability over cleverness

## Verification
- Run existing tests: `[test command]` — must pass
- [Benchmark command to prove improvement]
- Check that related endpoints aren't negatively affected
```

---

## 6. Security Hardening

**Thinking mode:** Assume adversarial input. Audit systematically, fix comprehensively.

```
Before starting, read @CLAUDE.md for project conventions.

## Security concern
[What needs hardening — specific area, known vulnerability, or audit scope]

## Systematic audit checklist
For each file in scope, check:
1. **Input validation** — Are all user inputs validated and sanitized?
2. **Authentication** — Are protected routes properly guarded?
3. **Authorization** — Can users access only their own resources?
4. **Data exposure** — Are sensitive fields stripped from responses?
5. **Secrets handling** — Are secrets in env vars, not hardcoded?
6. **SQL/NoSQL injection** — Are queries parameterized?
7. **XSS/CSRF** — Are outputs escaped? CSRF tokens in place?
8. **Dependencies** — Run `npm audit` or equivalent

## Fix approach
- Explain the risk before fixing each vulnerability
- Use the framework's built-in security features where available

## Verification
- All existing tests pass: `[test command]`
- `npm audit` shows no high/critical vulnerabilities
```

---

## 7. Investigation / Understanding Code

**Thinking mode:** Read, trace, explain. No modifications unless explicitly asked.

```
Before starting, read @CLAUDE.md for project context.

## What I want to understand
[The question — how does X work? Why does Y happen?]

## Starting points
[Grounded file paths and functions]

## Investigation approach
1. Read the relevant code paths starting from [entry point]
2. Trace the execution flow — what calls what, in what order
3. Map dependencies
4. Identify non-obvious behavior

## Output format
- High-level summary (2-3 sentences)
- Step-by-step flow walkthrough
- Call out anything surprising or risky

## Rules
- READ ONLY — do not modify any files
- Don't guess — if something is ambiguous, say so
```

---

## 8. Testing / Test Coverage

**Thinking mode:** Understand the code's contract, then write tests that verify it — including edge cases.

```
Before starting, read @CLAUDE.md for testing conventions.

## What to test
[Specific module/function/endpoint — grounded paths]

## Existing test setup
- Test framework: [from package.json]
- Test location: [where tests live]
- Existing examples: follow patterns in @[reference test file]

## Coverage requirements
1. **Happy path** — [normal expected behavior]
2. **Edge cases** — [specific edge cases from code analysis]
3. **Error cases** — [what should fail and how]
4. **Boundary conditions** — [empty arrays, null values, max lengths]

## Constraints
- Do NOT modify the source code — only add/modify test files
- Use existing test utilities in @[test helpers file]

## Verification
- All new tests pass: `[test command]`
- All existing tests still pass
```

---

## Task Classification Guide

| Signal | Task Type |
|--------|-----------|
| "bug", "broken", "not working", "error", "fix" | Bug Fix |
| "add", "build", "create", "implement", "new" | New Feature |
| "refactor", "clean up", "reorganize", "simplify" | Refactor |
| "migrate", "upgrade", "update to", "switch from X to Y" | Migration |
| "slow", "optimize", "performance", "speed up", "cache" | Performance |
| "secure", "vulnerability", "auth", "injection", "audit" | Security |
| "how does", "explain", "understand", "trace", "what does" | Investigation |
| "test", "coverage", "spec", "write tests for" | Testing |

If a task spans multiple types, use the **primary** type as the base and incorporate relevant sections from the secondary type. For compound tasks, suggest separate prompts.
