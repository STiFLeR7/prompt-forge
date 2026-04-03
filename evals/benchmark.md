# Benchmark Framework

Cross-model benchmark methodology for evaluating Prompt Forge output quality across Claude, Gemini, and OpenAI.

---

## Benchmark Structure

Each benchmark case consists of:

1. **Raw intent** — The developer's original input
2. **Context** — Simulated codebase state (file paths, patterns, stack)
3. **Mode** — Which compilation mode to use
4. **Target models** — All three adapters produce output
5. **Evaluation** — Score each output against scoring criteria (see `scoring.md`)

---

## Benchmark Cases

### BM-01: Vague Bug Fix (Fatigue Input)

**Intent:** "fix the login thing"
**Context:** Express app with JWT auth, loginUser() has inconsistent error handling
**Mode:** debug
**Evaluates:** Fatigue signal detection, code grounding, investigation-first structure

### BM-02: New Feature (Medium Complexity)

**Intent:** "add stripe payments"
**Context:** Express + Prisma app, existing service/route patterns, no payment code yet
**Mode:** build
**Evaluates:** Pattern reference accuracy, scope boundaries, implementation structure

### BM-03: Security Audit

**Intent:** "audit the API for auth vulnerabilities"
**Context:** 5 API routes, mixed auth middleware usage, some unprotected endpoints
**Mode:** audit
**Evaluates:** Systematic checklist, constraint prominence, finding structure

### BM-04: Architecture Research

**Intent:** "should we use microservices or keep the monolith?"
**Context:** Growing Express monolith, 15 route files, 8 services, 3 developers
**Mode:** research
**Evaluates:** Multiple alternatives, trade-off analysis, structured comparison

### BM-05: Performance Optimization

**Intent:** "the dashboard is slow"
**Context:** React frontend + Express API, N+1 queries in user profile endpoint
**Mode:** optimize
**Evaluates:** Measurement-first approach, bottleneck identification, before/after structure

### BM-06: Compound Task (Should Split)

**Intent:** "fix auth, add rate limiting, and migrate to Express 5"
**Context:** Express 4.18 app
**Mode:** build
**Evaluates:** Task decomposition recommendation, refusal to produce monolithic prompt

### BM-07: Greenfield (No Codebase)

**Intent:** "build a REST API for a todo app"
**Context:** Empty project, no existing code
**Mode:** build
**Evaluates:** Handling of no-code-grounding scenario, research-based recommendations

### BM-08: Tiny Task (Over-engineering Risk)

**Intent:** "fix typo in README line 12"
**Context:** Simple README.md with a typo
**Mode:** build
**Evaluates:** Complexity matching — output should be minimal, not over-structured

---

## Running Benchmarks

### Manual Evaluation

1. For each benchmark case, run Prompt Forge with the specified intent, context, and mode
2. Generate output for all three adapters (Claude, Gemini, OpenAI)
3. Score each output using `scoring.md` rubric
4. Record scores in a comparison table

### Comparison Table Template

| Case | Adapter | Clarity | Constraints | Structure | Grounding | Leakage | Total |
|------|---------|---------|-------------|-----------|-----------|---------|-------|
| BM-01 | Claude | /5 | /5 | /5 | /5 | /5 | /25 |
| BM-01 | Gemini | /5 | /5 | /5 | /5 | /5 | /25 |
| BM-01 | OpenAI | /5 | /5 | /5 | /5 | /5 | /25 |

### What to Look For

- **Cross-model consistency:** Same intent should produce semantically equivalent prompts across adapters, just formatted differently
- **Adapter differentiation:** Claude output should use XML tags, Gemini should use MUST/MUST NOT, OpenAI should use system/user split
- **Mode impact:** Same intent in different modes should produce structurally different prompts
- **Complexity matching:** Simple inputs should produce simple outputs
