---
name: prompt-forge
description: "Advanced prompt refinement: extracts intent, investigates context, and rotates perspective lenses to produce grounded execution prompts."
---

# /prompt-forge

Use Prompt Forge to write, improve, or refine your prompt for any task. It will investigate your codebase, research the ecosystem, and surface critical perspectives you might have missed before delivering a copy-paste-ready prompt for your execution tool.

## Invocation

```
/prompt-forge [your rough idea or task description]
```

## What Happens

1. **Parses your intent** — reads between the lines of what you typed, especially when fatigue makes your prompt vague
2. **Investigates** — reads your code, checks patterns, searches docs (see `src/core/intent_parser.md`)
3. **Asks smart questions** — 1-3 grounded, easy-to-answer questions
4. **Applies perspective lenses** — security, testing, architecture, edge cases, etc. (see `src/core/prompt_builder.md`)
5. **Delivers a grounded prompt** — formatted for Claude Code, GSD, or Superpowers

## Supported Execution Targets

| Target | When Detected |
|--------|---------------|
| **Claude Code** (default) | No plugin detected, or user requests it |
| **GSD** | `.planning/` directory, GSD commands, or user mentions GSD |
| **Superpowers** | Superpowers skills directory, or user mentions Superpowers |

## Boundary

Prompt Forge **investigates but never implements**. See `src/core/constraints.md` for the full boundary definition.
