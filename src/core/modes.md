# Compilation Modes

Prompt Forge supports 5 modes that alter how the compiled prompt is structured. Each mode shifts the emphasis — what comes first, what gets the most detail, and what constraints are tightened.

The mode does NOT change the core pipeline (intent parsing, grounding, lenses). It changes the **output emphasis** in the final compiled prompt.

---

## build

**Purpose:** Construct something new or extend existing functionality.

**Emphasis:** Implementation structure, pattern references, step-by-step construction.

**Prompt adjustments:**
- Lead with pattern references ("Follow the implementation in @reference-file")
- Break work into numbered, verifiable steps
- Include test gates between steps
- Emphasize "done criteria" at the end
- Scope boundaries are explicit (IN/OUT lists)

**Constraint weight:** Medium — focus is on what to build, not what to avoid.

**Best for:** New features, integrations, adding endpoints, creating components.

---

## audit

**Purpose:** Review, verify, or harden existing code.

**Emphasis:** Constraints, compliance, what NOT to do, verification gates.

**Prompt adjustments:**
- Lead with the audit scope and checklist
- Constraints section is prominent and detailed
- Use systematic checklist format (security vectors, code quality, etc.)
- Require explanation of each finding before any fix
- Output should be structured as findings + recommendations

**Constraint weight:** High — the prompt is primarily about boundaries and rules.

**Best for:** Security review, code audit, compliance checks, pre-merge review.

---

## debug

**Purpose:** Investigate and fix a problem.

**Emphasis:** Investigation-first, root cause analysis, reproduction steps.

**Prompt adjustments:**
- Lead with symptoms and reproduction steps
- Explicitly require root cause identification BEFORE any fix
- Include "check if this pattern exists elsewhere" step
- Require verification that the fix resolves the issue
- Add regression check: "ensure no other tests broke"

**Constraint weight:** Medium — focus is on "understand before fixing."

**Best for:** Bug fixes, error investigation, performance issues, flaky tests.

---

## research

**Purpose:** Explore, understand, or evaluate options.

**Emphasis:** Exploration, alternatives, trade-off analysis, documentation.

**Prompt adjustments:**
- Lead with the question or exploration goal
- Request multiple approaches with trade-offs
- Ask for structured comparison (table format)
- Specify READ ONLY — no modifications
- Request sources and confidence levels

**Constraint weight:** Low — focus is on breadth of exploration.

**Best for:** Architecture decisions, library evaluation, understanding code, feasibility analysis.

---

## optimize

**Purpose:** Improve performance, reduce cost, or increase efficiency.

**Emphasis:** Measurement-first, bottleneck identification, before/after metrics.

**Prompt adjustments:**
- Lead with "measure before changing anything"
- Require profiling or benchmarking data before any optimization
- Explicitly prevent premature optimization ("don't optimize what you haven't measured")
- Request before/after comparison
- Readability constraint: "don't sacrifice clarity for marginal gains"

**Constraint weight:** Medium — focus is on "prove the improvement."

**Best for:** Slow endpoints, expensive queries, bundle size, memory usage, build time.

---

## Mode Selection Logic

If the user doesn't specify a mode, infer from intent:

| Intent Signal | Default Mode |
|---------------|-------------|
| "add", "build", "create", "implement" | build |
| "audit", "review", "check", "verify", "secure" | audit |
| "fix", "bug", "broken", "error", "debug" | debug |
| "how", "why", "explore", "compare", "understand" | research |
| "slow", "optimize", "performance", "speed", "cache" | optimize |

If ambiguous, default to `build`.
