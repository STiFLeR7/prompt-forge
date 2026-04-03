# Prompt Builder

Generates the final output: a structured intent breakdown and a copy-paste-ready execution prompt. Applies perspective lenses, classifies task type, selects the appropriate blueprint, and formats output for the target execution tool.

## Step 5: Analyze Through the Lenses

These lenses catch what fatigue makes you skip. When you're fresh, you naturally think about testing, security, edge cases, and patterns. When you're exhausted, you think about making the immediate problem go away.

**The lenses are not a one-time checklist.** They're a continuous perspective rotation — keep applying them throughout the conversation. When the developer answers your questions, re-check them. When you're writing the prompt, rotate through them again. When you think you're done, do one final pass.

### The 9 Lenses

1. **Business/Product** — Why does this change matter? Prevents building the technically elegant wrong thing.

2. **QA/Testing** — What should be tested? What could break? Prevents "works on my machine" prompts.

3. **Architecture/Design** — Does this follow existing patterns? Prevents spaghetti that someone else has to untangle.

4. **User Experience** — What does the end user see? Loading states, error messages, accessibility.

5. **Security** — Auth implications? Input validation? Prevents shipping vulnerabilities because you were too tired to think about injection.

6. **Performance/Scalability** — Will this hold up under load? Prevents slow-at-scale solutions.

7. **Developer Experience** — Will someone else understand this code? Prevents future-you from cursing past-you.

8. **Edge Cases & Error Handling** — What happens when the input is empty? When the network is down? Prevents fragile code.

9. **Migration/Backwards Compatibility** — What existing code does this affect? Prevents breaking changes.

### Surfacing Lenses Naturally

Don't present all 9 as a checklist. Weave relevant observations naturally:

**Good:** *"One thing — the endpoint you're modifying doesn't validate the email format before hitting the DB. I'll include input validation in the prompt. Also, there are no tests for this route, so I'll have Claude write a basic test too."*

**Bad:** *"Security lens: have you considered input validation? QA lens: have you considered test coverage?"*

---

## Step 6: Produce the Output

Generate **two things** and then **stop**.

### A. Structured Intent Breakdown

```
## Intent Breakdown

**Core task:** [One sentence — what are we actually doing?]
**Why it matters:** [Business/product context]
**Scope:** [What's in, what's explicitly out]
**Success criteria:** [How to know it worked]
**Constraints:** [What not to break, what to stay compatible with]

### Grounding summary:
**Codebase findings:**
- [Key pattern/convention discovered]
- [Files that will be affected]
- [Existing implementation to follow as reference]

**Research findings:**
- [Best practice or doc reference]
- [Known gotcha or version-specific note]
- [Alternative approach considered, if any]

### Relevant lenses applied:
- [Lens name]: [Key insight or consideration]
- [Lens name]: [Key insight or consideration]

### CLAUDE.md flag (if applicable):
[Anything that should live in the project's CLAUDE.md rather than in a one-off prompt]
```

### B. Refined Prompt (Copy-Paste Ready)

A prompt the developer can paste directly into their execution tool. Must be **fully grounded** — every reference to the codebase uses actual names from the code.

#### Step 6.1: Classify the Task Type

| Signal in user's request | Task type |
|--------------------------|-----------|
| "bug", "broken", "not working", "error", "fix" | Bug Fix |
| "add", "build", "create", "implement", "new" | New Feature |
| "refactor", "clean up", "reorganize", "simplify" | Refactor |
| "migrate", "upgrade", "update to", "switch from X to Y" | Migration |
| "slow", "optimize", "performance", "speed up", "cache" | Performance |
| "secure", "vulnerability", "auth", "injection", "audit" | Security |
| "how does", "explain", "understand", "trace", "what does" | Investigation |
| "test", "coverage", "spec", "write tests for" | Testing |

#### Step 6.2: Select and Fill the Blueprint

Use the blueprint from `prompts/templates/task-type-blueprints.md` for the classified task type. Each blueprint provides:
- The right **thinking mode** (e.g., "investigate first" for bugs, "measure first" for performance)
- The right **prompt structure** with sections in the right order
- The right **constraints** that prevent common failures
- A **docs-check preamble** — every prompt starts with telling Claude Code to read @CLAUDE.md

Fill in the blueprint with grounded details. Adapt it — don't copy rigidly.

#### Step 6.3: Apply Anthropic's Prompting Rules

Regardless of task type, every prompt must follow:

- **Be clear and direct.** State exactly what you want.
- **Reference real code.** Use actual file paths, function names, types. Use `@filename` syntax. Never make up names.
- **Point to existing patterns.** "Follow the pattern in `@src/routes/orders.ts`."
- **Include a feedback loop.** Tell Claude to run tests, lint, type-check after changes.
- **Include version-specific guidance.** If web research surfaced deprecations or gotchas, include them.
- **Keep it focused.** One task per prompt. If compound, suggest breaking it up.

If a task spans multiple types, use the primary type as the base and incorporate sections from the secondary type.

---

## Plugin-Aware Output Formatting

When generating the refined prompt, check if the user's project uses GSD or Superpowers. If detected, or if the user mentions either plugin, adapt the output accordingly. See `prompts/templates/gsd-output-format.md` and `prompts/templates/superpowers-output-format.md` for the adapted structures.

For medium and complex tasks, consider offering multiple output formats:

> "Here's your refined prompt. I've formatted it for direct Claude Code use. Want me to also format it for GSD or Superpowers?"
