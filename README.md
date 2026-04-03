# Prompt Forge

**A prompt compiler skill for Claude Code, Gemini CLI, and other coding agents.**

**Solves prompt fatigue — the quality collapse that happens when you've been coding for hours and your prompts go from detailed instructions to "fix the auth thing."**

[![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/STiFLeR7/prompt-forge?style=for-the-badge&logo=github&color=181717)](https://github.com/STiFLeR7/prompt-forge)

---

## Why This Exists

You're three hours into a session. You know exactly what needs to happen — but you're too fried to write it properly. So you type "fix the login thing" and Claude hallucinates a solution to a problem you didn't describe.

The issue isn't Claude. It's your prompt. You stopped including context, constraints, file paths, test commands, and the six perspectives you'd normally think about. Not because you're lazy — because your working memory is full.

Prompt Forge sits between your tired brain and your coding agent. You type the vague thing. It reads your codebase, asks one or two easy questions, surfaces what you forgot, and hands you back a grounded, structured prompt you can paste and run.

It works with [Superpowers](https://github.com/obra/superpowers) and [GSD](https://github.com/gsd-build/get-shit-done) — or standalone with raw Claude Code and Gemini CLI.

---

## How It Works

```
You:          "fix the auth thing"

Prompt Forge: [reads your code, greps for patterns, checks docs]
              "loginUser() in auth-service.ts handles invalid passwords
               and missing users differently. Is the bug about which one?"

You:          "yeah the missing user case"

Prompt Forge: [delivers a grounded prompt with investigation steps,
               fix approach, test commands, and a security note about
               input validation you didn't think to mention]
```

The whole pipeline:

1. **Read your input** — detect fatigue signals, find the hidden intent
2. **First grounding** — read CLAUDE.md, scan the codebase, research docs
3. **Ask 1-3 questions** — grounded, easy to answer (yes/no, pick-one)
4. **Second grounding** — targeted deep-dive based on your answers
5. **Apply lenses** — 9 perspectives that fatigue makes you skip
6. **Compile the prompt** — structured, grounded, ready to paste

That's it. You get back a prompt. You paste it. Prompt Forge never writes code, never runs builds, never executes anything. It's the architect, not the builder.

---

## The 9 Lenses

Things a fresh engineer thinks about but a tired one forgets:

| # | Lens | What It Catches |
|---|------|----------------|
| 1 | **Business/Product** | Building the technically elegant wrong thing |
| 2 | **QA/Testing** | "Works on my machine" prompts with no test commands |
| 3 | **Architecture** | Spaghetti that ignores existing patterns |
| 4 | **User Experience** | Missing loading states, error messages, accessibility |
| 5 | **Security** | Unvalidated input, auth gaps, data exposure |
| 6 | **Performance** | N+1 queries, unindexed lookups, no caching strategy |
| 7 | **Developer Experience** | Code that future-you will curse past-you for |
| 8 | **Edge Cases** | Empty arrays, null users, network timeouts |
| 9 | **Migration/Compat** | Breaking changes to downstream consumers |

These aren't presented as a checklist. They're woven naturally into the prompt: *"The endpoint doesn't validate email format before the DB query — I'll include that. Also, there's no test for this route."*

---

## Modes

Prompt Forge adapts its output based on what you're doing:

| Mode | Emphasis | Auto-detected from |
|------|----------|--------------------|
| `build` | Patterns, step-by-step, done criteria | "add", "create", "implement" |
| `audit` | Constraints, checklists, verification gates | "review", "check", "secure" |
| `debug` | Investigation-first, root cause before fix | "fix", "bug", "broken" |
| `research` | Alternatives, trade-offs, comparison tables | "how", "why", "explore" |
| `optimize` | Measure first, prove the improvement | "slow", "performance", "cache" |

---

## LLM Adapters

Same prompt intelligence, different formatting for each model:

| Adapter | Formatting Style |
|---------|-----------------|
| **Claude** | XML tags, `@file` references, chain-of-thought |
| **Gemini** | MUST/MUST NOT rules, markdown structure, search grounding |
| **OpenAI** | System/user split, few-shot examples, bold constraints |

---

## Works With

- **[Superpowers](https://github.com/obra/superpowers)** — Feeds brainstorming with design considerations already surfaced, so the Socratic questioning goes deeper instead of extracting basics
- **[GSD](https://github.com/gsd-build/get-shit-done)** — Produces rich project briefs that give GSD's interview and research phases a head start instead of starting from nothing
- **Raw Claude Code / Gemini CLI** — Outputs task-type-specific blueprints (bug fix, feature, refactor, migration, performance, security, investigation, testing)

---

## What's Inside

```
prompt-forge/
├── SKILL.md                          # Skill entrypoint
├── src/
│   ├── core/
│   │   ├── intent_parser.md          # Fatigue detection, grounding, questions
│   │   ├── prompt_builder.md         # Lenses, task classification, output
│   │   ├── modes.md                  # 5 compilation modes
│   │   └── constraints.md            # The cardinal rule: never implement
│   ├── adapters/
│   │   ├── claude.md                 # Claude-specific formatting
│   │   ├── gemini.md                 # Gemini-specific formatting
│   │   └── openai.md                 # OpenAI-specific formatting
│   ├── commands/
│   │   └── prompt-forge.md           # /prompt-forge slash command
│   └── utils/
│       └── helpers.md                # Tone, collaboration, complexity adaptation
├── prompts/
│   ├── templates/                    # 8 task-type blueprints + output formats
│   └── examples/                     # Full session walkthrough
├── evals/
│   ├── test_cases.md                 # 14 functional tests
│   ├── adversarial_cases.md          # 15 boundary tests
│   ├── benchmark.md                  # Cross-model benchmarks
│   └── scoring.md                    # Scoring rubric
└── docs/
    ├── architecture.md               # System design
    └── usage.md                      # Integration guide
```

---

## Installation

```bash
npx prompt-forge-cc@latest
```

The installer prompts you to choose:
1. **Runtime** — Claude Code, Gemini CLI, or both
2. **Scope** — Global (all projects) or local (current project only)

### Non-interactive Install

```bash
# Claude Code (global — recommended)
npx prompt-forge-cc --claude --global

# Gemini CLI (global)
npx prompt-forge-cc --gemini --global

# Both runtimes
npx prompt-forge-cc --all --global

# Current project only
npx prompt-forge-cc --claude --local
```

### Verify

Start a new session and run:
```
/prompt-forge fix the auth thing
```

### Updating

```bash
npx prompt-forge-cc@latest
```

### Uninstall

```bash
npx prompt-forge-cc --uninstall
```

---

## Philosophy

- **Investigate, never implement** — Prompt Forge reads your code aggressively but never touches it
- **Fatigue is the enemy, not laziness** — "fix the thing" is a valid input
- **Grounding over guessing** — Every file path, function name, and type in the output comes from actually reading the code
- **Collaborate, don't obey** — It challenges bad assumptions and proposes alternatives
- **Match complexity to the task** — A typo fix gets a one-liner, not five sections of context

---

## Contributing

1. Fork the repository
2. Create a branch for your changes
3. Submit a PR

See `docs/architecture.md` for system design and `evals/` for validation criteria.

---

## Contributors

- **Nirvaan** ([Nirvaan05](https://github.com/Nirvaan05)) — Core Architecture, prompt system design, evaluation framework
- **Hill Patel** ([STiFLeR7](https://github.com/STiFLeR7)) — Lead Contributor, prompt system design, original extraction from Superpowers

## License

MIT — see [LICENSE](LICENSE)
