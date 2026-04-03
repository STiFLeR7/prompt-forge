# Usage Guide

## Quick Start

Invoke Prompt Forge when you need help writing a prompt — especially when you're tired, stuck, or unsure how to articulate what you want.

```
/prompt-forge [your rough idea]
```

That's it. Prompt Forge will investigate your codebase, ask a few easy questions, and deliver a copy-paste-ready prompt.

## When to Use Prompt Forge

- You know what you want but can't articulate it clearly
- You're too deep in a session to think about edge cases, testing, security
- You're starting a complex task and want a well-structured prompt before diving in
- You want to use GSD or Superpowers but need a strong initial description
- You want a fresh perspective on your approach before committing to it

## When NOT to Use Prompt Forge

- Simple, well-defined tasks you can articulate clearly ("fix the typo on line 12")
- You want someone to execute the task, not write a prompt for it
- You need code review or debugging (use those specific tools instead)

## What Prompt Forge Does

1. **Reads your input** — detects fatigue signals, identifies hidden intent
2. **Investigates** — reads your code, checks patterns, searches documentation
3. **Asks 1-3 questions** — grounded, easy to answer (yes/no, pick-one)
4. **Applies perspective lenses** — security, testing, architecture, edge cases, performance, etc.
5. **Delivers a grounded prompt** — formatted for your execution tool

## What Prompt Forge Does NOT Do

- Write or modify code
- Run builds, tests, or deployments
- Execute the prompt it generates
- Create or modify CLAUDE.md (it only suggests additions)

## Output Formats

### Standard Claude Code (Default)

Used when no workflow plugin is detected. Follows task-type-specific blueprints (bug fix, new feature, refactor, migration, performance, security, investigation, testing).

### GSD-Optimized

Used when GSD is detected (`.planning/` directory, GSD commands). Produces rich project briefs for `/gsd:new-project`, `/gsd:new-milestone`, or focused task descriptions for `/gsd:quick`.

### Superpowers-Optimized

Used when Superpowers is detected (skills directory, user mentions). Produces design-consideration-loaded briefs for `/superpowers:brainstorm` or TDD-ready task descriptions for direct execution.

## Integration as a Standalone Skill

### In Claude Code

Place the skill directory where your Claude Code installation discovers skills. The command entrypoint is `src/commands/prompt-forge.md`.

### In Other Agent Frameworks

Prompt Forge is pure markdown — no code dependencies. To integrate:

1. Load `SKILL.md` as the skill's entrypoint
2. Make the `src/core/`, `prompts/templates/`, and `src/utils/` files available as references
3. Ensure the agent has access to: file reading, grep/search, web search, web fetch

### As a Reference

Even without formal integration, the templates in `prompts/templates/` can be used as standalone references for writing better prompts manually.

## The Collaboration Loop

Prompt Forge isn't a one-shot tool. It's a conversation:

```
You: "fix the auth thing"
PF: [investigates] "I see loginUser() handles invalid passwords
    and missing users differently. Is the bug about which one?"
You: "yeah the missing user case"
PF: [delivers prompt with grounded fix approach + test]
You: "also include rate limiting"
PF: "That's a separate concern — want me to write a second prompt
    for rate limiting, or bundle it into this one?"
```

## Tips for Best Results

1. **Don't filter yourself.** Type whatever comes to mind, however vague. Prompt Forge is designed for tired, vague input.

2. **Answer questions with minimal effort.** "yeah", "no", "the first one" — all valid answers. Prompt Forge does the heavy lifting.

3. **Push back.** If the prompt doesn't match your intent, say so. Prompt Forge will rework it.

4. **Ask for alternatives.** "Is there a better way to do this?" triggers deeper research.

5. **Specify your execution tool.** "Format this for GSD" or "I'll paste this into Superpowers" helps Prompt Forge choose the right output format.
