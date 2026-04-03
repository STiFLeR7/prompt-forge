# Superpowers Output Format

How to structure Prompt Forge output when the target execution tool is Superpowers.

Superpowers' brainstorming phase is where quality is won or lost. A rich, pre-analyzed prompt with design considerations already surfaced lets brainstorming go deeper — exploring architectural alternatives, edge cases, and failure modes instead of asking "what does this feature do?"

---

## For Brainstorming Input

Structure as a rich feature brief with design considerations pre-loaded. The brainstorming skill will refine this, not extract it.

```
## Feature: [Name]

### Intent
[What I want to build and why — business context, user problem being solved]

### Technical landscape
- Stack: [framework, versions]
- Affected code: @[list of files that will be touched]
- Related implementations: @[similar feature already in codebase]
- Test setup: [framework, patterns in @test-file]

### Design considerations (for brainstorming to refine)

**Architecture:** [How this fits into the existing codebase structure.
Reference existing patterns. Flag any architectural decisions needed.]

**Security:** [Auth implications, input validation needs, data exposure risks.
Specific to this feature, not generic security advice.]

**Performance:** [Expected load, caching considerations, query concerns.
Reference specific DB queries or endpoints.]

**UX:** [What the user sees/experiences, error states, loading states.]

**Edge cases:** [Specific scenarios that could break, boundary conditions,
error handling requirements.]

### Testing strategy (for TDD planning)
- Must test: [critical paths — feeds TDD red phase]
- Edge cases to cover: [specific scenarios]
- What NOT to test: [things already covered]

### Research findings
[Best practices for this specific pattern + stack.
Known issues with current library versions.
Alternative approaches considered and why the chosen one is preferred.]

### Constraints
- Don't modify: @[protected files]
- Stay compatible with: [APIs, interfaces, contracts]
- Version notes: [deprecation warnings from research]
```

---

## For Direct Task Execution

When the task doesn't need brainstorming (small, well-defined), structure it so planning and TDD phases have everything:

```
## Task: [Name]

[Clear description — what to do]

Files to modify: @[list]
Follow pattern: @[reference]
Test file: @[where tests should go, following @reference-test pattern]

Test first:
- RED: [what the failing test should assert]
- GREEN: [minimal implementation to pass]
- REFACTOR: [any cleanup needed]

Constraints: [what not to touch]
Verify: [command to run]
```

---

## Detection Signals

**Superpowers indicators:**
- Skills directory with superpowers skills (brainstorming/, test-driven-development/)
- `.claude-plugin/` with superpowers plugin.json
- User mentions "superpowers", "brainstorm", "/superpowers:", "TDD workflow"
- Agents directory with code-reviewer or similar
