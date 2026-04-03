# Architecture

## System Overview

Prompt Forge is an LLM-agnostic prompt compiler. Raw developer intent enters the pipeline; a structured, grounded, model-optimized prompt exits. The system never implements — it only investigates and compiles.

```
Raw Intent (vague, tired)
        |
        v
+----------------------+
|   Intent Parser      |  src/core/intent_parser.md
|                      |
|  Step 1: Read input  |  Detect fatigue signals
|  Step 2: Ground #1   |  CLAUDE.md -> code -> web research
|  Step 3: Questions   |  Fatigue-friendly, grounded
|  Step 4: Ground #2   |  Targeted deep-dive from answers
+----------+-----------+
           |
           v
+----------------------+
|   Prompt Builder     |  src/core/prompt_builder.md
|                      |
|  Step 5: Lenses      |  9 perspective lenses
|  Step 6: Classify    |  8 task types
|  Step 6: Blueprint   |  prompts/templates/task-type-blueprints.md
+----------+-----------+
           |
           v
+----------------------+
|   Mode Engine        |  src/core/modes.md
|                      |
|  build / audit /     |  Adjusts prompt emphasis,
|  debug / research /  |  constraint weight, and
|  optimize            |  section ordering
+----------+-----------+
           |
           v
+----------------------+
|   Adapter Layer      |  src/adapters/
|                      |
|  claude.md           |  XML tags, @ references
|  gemini.md           |  MUST/MUST NOT, markdown
|  openai.md           |  System/user split, few-shot
+----------+-----------+
           |
           v
+----------------------+
|   Constraints        |  src/core/constraints.md
|                      |
|  Cardinal Rule       |  Investigate, never implement
|  Scope boundary      |  Prompt delivery = job done
+----------+-----------+
           |
           v
   Compiled Prompt (copy-paste ready, model-optimized)
```

## Directory Map

```
prompt-forge/
|-- SKILL.md                              # Skill entrypoint + module index
|-- CONTRIBUTORS.md                       # Project contributors
|-- LICENSE                               # MIT
|-- README.md                             # Project overview
|
|-- src/
|   |-- core/
|   |   |-- intent_parser.md              # Steps 1-4: input -> grounding -> questions
|   |   |-- prompt_builder.md             # Steps 5-6: lenses -> classification -> output
|   |   |-- constraints.md                # Cardinal rule + scope boundaries
|   |   +-- modes.md                      # 5 compilation modes
|   |-- adapters/
|   |   |-- claude.md                     # Claude/Anthropic formatting
|   |   |-- gemini.md                     # Gemini/Google formatting
|   |   +-- openai.md                     # OpenAI/GPT formatting
|   |-- commands/
|   |   +-- prompt-forge.md               # Slash command entrypoint
|   +-- utils/
|       +-- helpers.md                    # Tone, collaboration, complexity adaptation
|
|-- prompts/
|   |-- templates/                        # 8 task-type blueprints + output formats
|   +-- examples/                         # Walkthrough examples
|
|-- evals/
|   |-- test_cases.md                     # 14 functional test cases
|   |-- adversarial_cases.md              # 15 boundary/failure mode tests
|   |-- benchmark.md                      # Cross-model benchmark framework
|   +-- scoring.md                        # Scoring rubric (clarity, constraints, etc.)
|
+-- docs/
    |-- architecture.md                   # This file
    +-- usage.md                          # Integration guide
```

## Design Decisions

### Modular Over Monolithic

Core logic is decomposed into focused modules:
- **intent_parser.md** — investigation workflow (Steps 1-4)
- **prompt_builder.md** — output generation (Steps 5-6)
- **modes.md** — compilation mode engine (5 modes)
- **constraints.md** — behavioral boundary (the Cardinal Rule)
- **helpers.md** — tone, style, and complexity adaptation

### Adapter Pattern

LLM-specific formatting is isolated in `src/adapters/`. Each adapter defines:
- Role definition style
- Instruction structure preferences
- Constraint formatting conventions
- Output expectations
- Mode-specific adjustments

This means adding a new model is one file — no changes to core logic.

### Mode System

Five modes alter prompt emphasis without changing the core pipeline:

| Mode | Lead Emphasis | Constraint Weight |
|------|--------------|-------------------|
| build | Implementation structure, patterns | Medium |
| audit | Constraints, compliance, verification | High |
| debug | Investigation-first, root cause | Medium |
| research | Exploration, alternatives, trade-offs | Low |
| optimize | Measurement-first, bottlenecks | Medium |

Modes are auto-detected from intent keywords when not specified. See `src/core/modes.md` for full documentation.

### Templates as First-Class Citizens

Task-type blueprints, plugin output formats, and the context file template live in `prompts/templates/` — they're data, not logic. Easy to extend or customize.

### Separation of Concerns

| Concern | Location |
|---------|----------|
| What to investigate | `src/core/intent_parser.md` |
| What to produce | `src/core/prompt_builder.md` |
| How to emphasize | `src/core/modes.md` |
| How to format per model | `src/adapters/` |
| What never to do | `src/core/constraints.md` |
| How to communicate | `src/utils/helpers.md` |
| Prompt structures | `prompts/templates/` |
| Quality validation | `evals/` |

## CLAUDE.md Integration

Prompt Forge has a two-way relationship with project CLAUDE.md files:
1. **Reads** CLAUDE.md to understand project conventions (always first)
2. **Proposes additions** when it discovers patterns during investigation
3. **Never writes** CLAUDE.md directly — only suggests exact text

## Plugin Integration

Prompt Forge detects and adapts to workflow plugins:
- **GSD** — Rich project briefs for interview/research phases
- **Superpowers** — Design-consideration-loaded briefs for brainstorming
- **Standard** — Task-type blueprints for direct Claude Code / Gemini / OpenAI use

Detection is signal-based. When neither plugin is detected, standard blueprints are used.
