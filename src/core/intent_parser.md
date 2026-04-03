# Intent Parser

Extracts the developer's real intent from raw input — especially when fatigue obscures what they actually mean. Runs two grounding passes: one before asking questions (to ask smarter questions), one after (to fully ground the final prompt).

## Step 1: Receive Raw Input and Read the Fatigue Level

The user gives you their rough idea. Read it carefully — not just for content, but for **signals of fatigue and missing intent.**

### Fatigue Signals

| Signal | What It Means |
|--------|---------------|
| Extremely short/vague prompts ("fix the thing", "make it work") | Exhausted prompts, not lazy ones. The developer knows what they want but can't articulate it. |
| Missing context they'd normally include | No mention of which file, function, or what "it" refers to. A fresh developer would specify. |
| Scope creep in a single sentence | "fix the login and also add rate limiting and maybe cache the sessions" — fatigue-driven stream of consciousness. Untangle into separate tasks. |
| No success criteria | They say what to do but not how they'll know it worked. |
| Frustration signals ("this stupid bug", "ugh just") | Developer has been fighting this problem and needs fresh perspective. |

**Your job:** Don't accept input at face value. Assume there's an iceberg of intent beneath the surface. The grounding passes and questions will pull it out.

---

## Step 2: First Grounding Pass — Reconnaissance

Before asking a single question, investigate. Read in this order:

### 2.1 CLAUDE.md

Always read this first if it exists. It's the project's living brain — conventions, decisions, commands, anti-patterns. Everything you learn here shapes your questions and the final prompt.

### 2.2 Project Structure and Task-Specific Files

Read only the files needed to ground the user's current request. Start broad enough to understand the codebase shape, then narrow quickly to the actual task.

### 2.3 Deep Code Analysis

Read the codebase to ground yourself in reality. This prevents the #1 source of bad prompts: prompts that describe code that doesn't match what actually exists.

**What to investigate:**

- **Relevant files and structure.** Identify which files, modules, and directories are involved. Read them. Know the actual function names, parameter names, type signatures, and variable names. The refined prompt must reference these exactly — never guess.

- **Existing patterns.** Look at how similar features were implemented elsewhere. Find an existing endpoint and understand the pattern: middleware, validation, response format. Reference specific examples.

- **Dependencies and imports.** Check packages, versions, configuration. Prevents prompts that introduce conflicting dependencies.

- **Potential conflicts and surface area.** Map what the proposed change would touch. Which files need modification? Which modules depend on the affected code? Are there tests? Types/interfaces that need updating?

**How to do it:**
- Read directory structures to orient yourself
- Open and read the specific files related to the request
- Search for patterns (grep for similar implementations)
- Check config files (package.json, tsconfig, .env.example, etc.)
- Look at test files to understand testing patterns

**The grounding rule:** Every file path, function name, variable name, type name, and parameter name that appears in the final prompt must come from actually reading the code.

### 2.4 Deep Web Research + Approach Exploration

**Task-specific research (every session):**
- **Official documentation.** Look up the docs for the specific frameworks, libraries, and APIs involved.
- **Best practices for the pattern.** Search for current recommended approaches.
- **Known issues and gotchas.** Version-specific bugs, migration guides, security advisories.
- **Alternative approaches.** Actively look for better ways. Present trade-offs.

**Proactive approach exploration (when relevant):**
Don't just research the specific task — explore how other tools, frameworks, and methodologies think about the same class of problem.

When the developer shares a tool/link/approach:
1. Read it. Understand the *core principle* — not surface features, but the underlying thinking pattern.
2. Extract what's applicable to the current task and project.
3. Incorporate that thinking into the prompt you generate.

When the developer doesn't share anything — explore on your own for medium and complex tasks.

---

## Step 3: Ask Informed Clarifying Questions

Ask 2-3 sharp questions. These should be **specific, grounded, and easy for a tired brain to answer.**

### The Fatigue-Friendly Question Rule

- **Yes/no or pick-one format** — "Is this the JWT middleware in `auth.ts` or the session check in `session.ts`?"
- **Show your work** — "I see X, Y, and Z in the code. Is the issue with X?"
- **Suggest, don't ask open-ended** — "This would affect `UserService` and `/api/users` routes. Sound right?"
- **Surface what they're missing** — "I noticed there's no test coverage for this endpoint. Want me to include that?"

After your questions, offer: *"Want me to go deeper, or is this enough to work with?"*

For small/tired prompts, you might only ask 1 question — and it might just be a confirmation.

---

## Step 4: Second Grounding Pass — Targeted Deep-Dive

Based on the user's answers, do a focused follow-up investigation:

- If they clarified the scope, read any additional files now in scope
- If they mentioned a specific library or API, research its docs
- If they pointed out a constraint you missed, verify it in the code
- Cross-check that every concrete detail in the upcoming prompt matches reality

This pass is usually faster — you're filling specific gaps, not doing broad reconnaissance.
