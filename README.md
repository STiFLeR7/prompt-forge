# Prompt Forge

> **A Prompt Compiler for Agentic Systems**

Prompt Forge is an LLM-agnostic prompt compilation framework that transforms vague developer intent into structured, grounded execution prompts — optimized for Claude, Gemini, and OpenAI models.

It extracts what you actually mean (especially when you're too tired to say it clearly), investigates your codebase, surfaces the perspectives fatigue makes you forget, and compiles a ready-to-execute prompt tailored to your target model.

---

## The Problem

**Developer fatigue kills prompt quality.** After a few hours of coding, your prompts go from "Refactor the auth middleware to use async/await, preserving the existing error handling, and run the test suite after" to "fix the auth thing." You know what you mean. Your LLM doesn't.

The problem isn't laziness — it's cognitive depletion. Edge cases, test coverage, security implications, existing patterns — these drop off when your working memory is full.

## What Prompt Forge Does

1. **Extracts your real intent** from whatever half-formed thought you type
2. **Investigates the code** so the prompt references real names, real paths, real patterns
3. **Surfaces the perspectives you're too tired to think about** — security, edge cases, testing, performance, compatibility
4. **Compiles a grounded prompt** optimized for your target model (Claude, Gemini, or OpenAI)

## How It Works

```
You type:     "fix the auth thing"

Prompt Forge: [reads your code, finds the bug, checks patterns]
              "I see loginUser() handles invalid passwords and missing
               users differently. Is the bug about the missing user case?"

You:          "yeah"

Prompt Forge: [delivers a grounded, model-optimized prompt with
               investigation steps, fix approach, test commands,
               and a security note you forgot to mention]
```

### The Pipeline

```
Raw Intent → Intent Parser → Lens Analysis → Mode Selection → Adapter → Compiled Prompt
```

| Stage | What Happens |
|-------|-------------|
| Intent Parser | Detect fatigue signals, ground in code + docs, ask smart questions |
| Lens Analysis | Apply 9 perspective lenses (security, testing, architecture, etc.) |
| Mode Selection | Apply mode-specific emphasis (build, audit, debug, research, optimize) |
| Adapter | Format for target model (Claude, Gemini, OpenAI) |

### The 9 Perspective Lenses

1. **Business/Product** — Are we solving the right problem?
2. **QA/Testing** — What should be tested? What could break?
3. **Architecture/Design** — Does this follow existing patterns?
4. **User Experience** — Loading states, error messages, accessibility
5. **Security** — Auth, input validation, data exposure
6. **Performance/Scalability** — Will this hold under load?
7. **Developer Experience** — Will someone else understand this code?
8. **Edge Cases & Error Handling** — Empty input, network down, concurrent access
9. **Migration/Backwards Compatibility** — What existing code does this affect?

### Modes

| Mode | Emphasis |
|------|----------|
| `build` | Implementation structure, patterns, step-by-step construction |
| `audit` | Constraints, compliance, what NOT to do, verification gates |
| `debug` | Investigation-first, root cause analysis, reproduction steps |
| `research` | Exploration, alternatives, trade-off analysis, documentation |
| `optimize` | Measurement-first, bottleneck identification, before/after metrics |

## Usage

### CLI

```bash
pf forge "add stripe payments" --model claude --mode build
pf forge "why is the dashboard slow" --model gemini --mode debug
pf forge "audit the auth flow" --model openai --mode audit
```

### API

```bash
curl -X POST http://localhost:8000/forge \
  -H "Content-Type: application/json" \
  -d '{"intent": "add stripe payments", "target_model": "claude", "mode": "build"}'
```

### As a Skill (Claude Code / Superpowers / GSD)

```
/prompt-forge add stripe payments
```

## The Cardinal Rule

**Prompt Forge investigates but never implements.** It reads files, searches code, fetches docs — but it never writes code, runs builds, or executes the prompt it generates. You copy the prompt, you choose when and where to run it.

## Directory Structure

```
prompt-forge/
├── SKILL.md                              # Skill entrypoint + module index
├── CONTRIBUTORS.md                       # Project contributors
├── LICENSE                               # MIT
├── README.md                             # This file
│
├── src/
│   ├── core/
│   │   ├── intent_parser.md              # Steps 1-4: input → grounding → questions
│   │   ├── prompt_builder.md             # Steps 5-6: lenses → classification → output
│   │   ├── constraints.md                # Cardinal rule + scope boundaries
│   │   └── modes.md                      # 5 compilation modes
│   ├── adapters/
│   │   ├── claude.md                     # Claude/Anthropic formatting
│   │   ├── gemini.md                     # Gemini/Google formatting
│   │   └── openai.md                     # OpenAI/GPT formatting
│   ├── commands/
│   │   └── prompt-forge.md               # Slash command entrypoint
│   └── utils/
│       └── helpers.md                    # Tone, collaboration, complexity adaptation
│
├── prompts/
│   ├── templates/                        # 8 task-type blueprints + output formats
│   └── examples/                         # Full walkthrough examples
│
├── evals/
│   ├── test_cases.md                     # 14 functional test cases
│   ├── adversarial_cases.md              # 15 boundary/failure mode tests
│   ├── benchmark.md                      # Cross-model benchmark framework
│   └── scoring.md                        # Scoring criteria and rubrics
│
├── api/
│   └── main.py                           # FastAPI server (POST /forge)
│
├── cli/
│   └── pf.py                             # CLI tool
│
└── docs/
    ├── architecture.md                   # System design + mode system
    └── usage.md                          # Integration guide
```

## Installation

```bash
# API server
pip install fastapi uvicorn
cd api && uvicorn main:app --reload

# CLI
python cli/pf.py forge "your intent" --model claude --mode build
```

## Contributors

- **Nirvaan** ([Nirvaan05](https://github.com/Nirvaan05)) — Core Architecture, prompt system design, evaluation framework
- **Hill Patel** ([STiFLeR7](https://github.com/STiFLeR7)) — Lead Contributor, prompt system design, original extraction from Superpowers

## License

MIT — see [LICENSE](LICENSE)
