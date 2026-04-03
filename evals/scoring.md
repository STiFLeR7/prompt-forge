# Scoring Criteria

Rubric for evaluating Prompt Forge output quality. Each criterion is scored 1-5.

---

## Criteria

### 1. Clarity (1-5)

Does the compiled prompt communicate the task unambiguously?

| Score | Definition |
|-------|-----------|
| 1 | Vague, could be interpreted multiple ways |
| 2 | Main intent clear but missing important details |
| 3 | Clear task description, some ambiguity in scope or approach |
| 4 | Clear and specific, minor details could be sharper |
| 5 | Unambiguous — a fresh engineer would know exactly what to do |

### 2. Constraints (1-5)

Are boundaries well-defined and appropriately weighted for the mode?

| Score | Definition |
|-------|-----------|
| 1 | No constraints, or constraints that contradict the task |
| 2 | Generic constraints ("be careful") with no specifics |
| 3 | Some specific constraints but missing important boundaries |
| 4 | Good constraints with file paths and specific prohibitions |
| 5 | Comprehensive, grounded constraints — nothing dangerous is left open |

### 3. Structure (1-5)

Is the prompt organized effectively for the target model and mode?

| Score | Definition |
|-------|-----------|
| 1 | Wall of text, no sections or formatting |
| 2 | Some structure but inconsistent or illogical ordering |
| 3 | Clear sections, reasonable ordering |
| 4 | Well-structured with model-appropriate formatting (XML for Claude, etc.) |
| 5 | Optimal structure — sections in the right order, right format for model and mode |

### 4. Grounding (1-5)

Are code references accurate and based on actual codebase investigation?

| Score | Definition |
|-------|-----------|
| 1 | No code references, or references to files/functions that don't exist |
| 2 | Some references but mixed with hallucinated names |
| 3 | Most references correct, a few unverified assumptions |
| 4 | All references verified, pattern examples from real code |
| 5 | Fully grounded — every path, function, type, and command verified against reality |

### 5. Leakage (1-5, inverse)

Does the prompt avoid leaking implementation decisions that should be left to the executor?

| Score | Definition |
|-------|-----------|
| 1 | Prompt dictates exact implementation (line-by-line code) |
| 2 | Over-specifies approach, leaving no room for the model's judgment |
| 3 | Mostly appropriate, a few over-specified details |
| 4 | Good balance — clear what to do, flexible on how |
| 5 | Perfect — specifies intent, constraints, and patterns without dictating implementation |

---

## Composite Score

**Total: /25** (sum of all five criteria)

| Range | Quality Level |
|-------|--------------|
| 21-25 | Production-ready — use as-is |
| 16-20 | Good — minor tweaks needed |
| 11-15 | Acceptable — needs revision in weak areas |
| 6-10  | Poor — significant issues, rewrite recommended |
| 1-5   | Failed — fundamental problems with the output |

---

## Mode-Specific Weighting

Different modes have different priorities. When evaluating, weight accordingly:

| Mode | Primary Criteria | Secondary |
|------|-----------------|-----------|
| build | Structure, Grounding | Clarity, Leakage |
| audit | Constraints, Structure | Grounding, Clarity |
| debug | Clarity, Grounding | Constraints, Structure |
| research | Leakage, Clarity | Structure, Grounding |
| optimize | Grounding, Constraints | Clarity, Structure |

---

## Cross-Model Evaluation

When comparing the same prompt across adapters:

1. **Semantic equivalence** — All three should convey the same task, scope, and constraints
2. **Format differentiation** — Each should use its model's preferred formatting
3. **No adapter leakage** — Claude-formatted prompts shouldn't contain OpenAI system/user splits and vice versa
4. **Mode consistency** — Same mode should produce same structural emphasis across adapters
