# Test Cases — Prompt Forge Validation

These test cases verify that Prompt Forge produces correct, grounded, well-structured output across the full workflow.

---

## TC-01: Fatigue Signal Detection

**Input:** "fix the thing"
**Expected behavior:**
- Recognizes extreme vagueness as a fatigue signal, not laziness
- Does NOT ask "what thing?" as an open-ended question
- Instead, investigates the codebase first, then asks a grounded yes/no question like "Is this about the broken `loginUser()` in auth-service.ts?"
- Produces a short, focused prompt (small/tired mode)

---

## TC-02: First Grounding Pass — CLAUDE.md Read

**Input:** Any prompt in a project with CLAUDE.md
**Expected behavior:**
- Reads CLAUDE.md before any other investigation
- References conventions from CLAUDE.md in the final prompt
- Detects drift between CLAUDE.md and actual code (if any)
- Flags missing CLAUDE.md when it doesn't exist

---

## TC-03: Code Grounding Accuracy

**Input:** "add a new API endpoint for user profiles"
**Expected behavior:**
- All file paths in the output exist in the actual codebase
- All function names match their actual declarations
- All type/interface names are correct
- Pattern references point to real, working implementations
- Test commands match what's in package.json/Makefile

---

## TC-04: Web Research Integration

**Input:** "migrate from Express 4 to Express 5"
**Expected behavior:**
- Searches for Express 5 migration guide and breaking changes
- Includes version-specific gotchas in the prompt
- References official documentation, not blog posts
- Notes any deprecated APIs that the project currently uses

---

## TC-05: Question Quality — Fatigue-Friendly

**Input:** Short/vague prompt from a "tired" developer
**Expected behavior:**
- Questions are yes/no or pick-one format
- Questions show investigative work ("I see X in the code, is this about Y?")
- No open-ended questions that require recall from an exhausted brain
- Maximum 2-3 questions for medium tasks, 1 for small tasks

---

## TC-06: Lens Application — All 9 Covered

**Input:** Complex feature request
**Expected behavior:**
- At least 5-7 lenses are applied for complex tasks
- Lenses are woven into observations, not listed as a checklist
- Each lens produces a specific, actionable insight (not generic advice)
- Insights reference actual code/patterns from the codebase

---

## TC-07: Task Type Classification

**Inputs and expected types:**

| Input | Expected Type |
|-------|---------------|
| "the login is broken" | Bug Fix |
| "add user profiles" | New Feature |
| "clean up the auth module" | Refactor |
| "upgrade to React 19" | Migration |
| "the dashboard loads slowly" | Performance |
| "audit the API for vulnerabilities" | Security |
| "how does the payment flow work?" | Investigation |
| "write tests for the user service" | Testing |

**Expected behavior:** Each produces a prompt using the correct blueprint structure from `prompts/templates/task-type-blueprints.md`.

---

## TC-08: Blueprint Adherence

**Input:** Any classified task
**Expected behavior:**
- Prompt follows the blueprint structure for that task type
- Docs-check preamble is present ("Before starting, read @CLAUDE.md...")
- Sections appear in the correct order per the blueprint
- Verification section uses actual project commands
- Constraints section is present and grounded

---

## TC-09: Plugin Detection and Output Format

**Scenario A:** Project has `.planning/` directory
**Expected:** GSD-optimized output format

**Scenario B:** Project has superpowers skills directory
**Expected:** Superpowers-optimized output format

**Scenario C:** Neither detected
**Expected:** Standard Claude Code task-type blueprint

**Scenario D:** Both detected
**Expected:** Asks user which format, or offers all three

---

## TC-10: Cardinal Rule Enforcement

**Input:** Developer says "go ahead and implement it" after receiving prompt
**Expected behavior:**
- Does NOT start implementing
- Responds with: "I've built the prompt — paste it into [tool] to kick it off. Want me to tweak anything first?"
- Never writes/modifies source code files
- Never runs build/test/lint/deploy commands

---

## TC-11: Scope Boundary — No CLAUDE.md Bootstrapping

**Input:** Project without CLAUDE.md
**Expected behavior:**
- Mentions that CLAUDE.md doesn't exist
- May suggest creating one as a brief note AFTER delivering the prompt
- Does NOT create CLAUDE.md itself
- Does NOT create prompt-forge-context.md itself

---

## TC-12: Complexity Adaptation

**Input A:** "fix the login bug" (small)
**Expected:** Fast code analysis, 1 question, short prompt, no full intent breakdown

**Input B:** "add Stripe payments" (medium)
**Expected:** Full code analysis, 2-3 questions, full intent breakdown + prompt

**Input C:** "migrate the monolith to microservices" (complex)
**Expected:** Deep analysis, thorough research, most lenses, suggest plan mode/sub-tasks

---

## TC-13: Multi-Format Output Offer

**Input:** Medium or complex task with plugin detected
**Expected behavior:**
- Offers the primary format based on detected plugin
- Offers to reformat for alternative tools
- All formats contain the same grounded content, just structured differently

---

## TC-14: Alternative Approach Surfacing

**Input:** Developer suggests approach X, but research reveals approach Y is better
**Expected behavior:**
- Surfaces the alternative with trade-offs
- Does not silently ignore it
- Lets the developer decide
- Can rewrite the prompt for either approach
