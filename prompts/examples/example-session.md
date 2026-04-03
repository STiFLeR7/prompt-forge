# Example Session — From Vague Input to Grounded Prompt

Demonstrates how Prompt Forge transforms a tired developer's vague input into a fully grounded execution prompt across all three output formats.

---

## Raw Input

> "add stripe payments"

---

## What Prompt Forge Does

1. **Reads fatigue signals:** Short, no context about what kind of payments, no mention of which part of the app. Classic fatigue prompt.

2. **First grounding pass:** Reads CLAUDE.md, scans project structure, finds Express 4.18 + Prisma 5.x + PostgreSQL, existing user auth via JWT, existing service patterns.

3. **Asks 1-2 questions:**
   > "I see your app has user accounts with JWT auth. For payments — is this one-time purchases (Stripe Checkout) or recurring subscriptions (Stripe Billing)? Also, I noticed there's no webhook endpoint yet — I'll include that in the prompt."

4. **Applies lenses:**
   - **Security:** Webhook signature verification, raw body parsing requirement
   - **Architecture:** Follow existing service pattern
   - **Testing:** No payment tests exist yet

5. **Produces output** in the appropriate format.

---

## Output: Standard Claude Code Prompt

```
Before starting, read @CLAUDE.md for project conventions.

## Context
Express 4.18 app with Prisma 5.x, PostgreSQL. Existing user auth
via JWT in @src/middleware/auth.ts. No payment system exists yet.

## Task
Add Stripe Checkout integration for one-time payments.

## Pattern reference
Follow the existing implementation pattern in @src/routes/orders.ts for:
- Route structure and middleware chain
- Zod request validation
- Service layer calls
- Error response format

## Implementation plan
1. Add `stripe` package (check compatibility with Node 20)
2. Create @src/services/payment-service.ts following @src/services/order-service.ts pattern
3. Create @src/routes/payments.ts with checkout session creation endpoint
4. Add webhook endpoint at /api/webhooks/stripe using express.raw() middleware
   IMPORTANT: Webhook route must use express.raw() BEFORE express.json()
5. Add Prisma model for Payment records
6. Write tests following @tests/routes/orders.test.ts pattern

## Constraints
- Use Stripe Checkout (hosted page), not Elements
- Webhook signature verification is mandatory — use stripe.webhooks.constructEvent()
- Do NOT store card details — Stripe handles PCI compliance
- Add STRIPE_SECRET_KEY and STRIPE_WEBHOOK_SECRET to .env.example

## Verification
- Run `npm test` — all tests pass including new payment tests
- Run `npm run typecheck` — no type errors
- Run `npm run lint` — clean
```

---

## Output: GSD-Optimized (`/gsd:quick` input)

```
Add Stripe Checkout integration for one-time payments to the Express/Prisma app.
Create payment service, checkout route, and webhook endpoint.

Technical context: Express 4.18, Prisma 5.x, PostgreSQL, JWT auth in @src/middleware/auth.ts
Follow pattern in: @src/routes/orders.ts and @src/services/order-service.ts
Constraints: Use hosted Checkout page, verify webhook signatures, no card storage
Verify: npm test && npm run typecheck && npm run lint

Research note: Express 4.18 webhook routes need express.raw() middleware
BEFORE express.json() — order matters for Stripe signature verification.
```

---

## Output: Superpowers-Optimized (`/brainstorm` input)

```
## Feature: Stripe Checkout Integration

### Intent
Add one-time payment capability so users can purchase premium features.
No payment system exists yet — this is greenfield within the existing Express app.

### Technical landscape
- Stack: Express 4.18, Prisma 5.x, PostgreSQL, Node 20
- Affected code: new files + @src/app.ts (middleware order for webhook)
- Related implementations: @src/routes/orders.ts, @src/services/order-service.ts
- Test setup: Jest + Supertest, patterns in @tests/routes/orders.test.ts

### Design considerations
**Security:** Webhook signature verification critical — use stripe.webhooks.constructEvent().
Raw body parsing needed for webhook endpoint. Never store card details.

**Architecture:** Follow existing service pattern. Payment service handles Stripe API calls,
route handles HTTP, Prisma model stores payment records.

**Edge cases:** Webhook delivery can fail/retry — ensure idempotent payment recording.
Handle Checkout session expiry. Handle refund webhooks.

### Testing strategy
- Must test: checkout session creation, webhook signature verification, payment recording
- Edge cases: duplicate webhook delivery, expired sessions, invalid signatures
- What NOT to test: Stripe's own API behavior

### Constraints
- STRIPE_SECRET_KEY and STRIPE_WEBHOOK_SECRET via env vars
- express.raw() middleware BEFORE express.json() on webhook route
```

---

## Key Observations

- The same "add stripe payments" produced three different formats, all with the same grounded content.
- Every file path, function name, and pattern reference came from reading the actual codebase.
- Security and architecture insights were surfaced by the lenses — not requested by the developer.
- The webhook middleware ordering gotcha came from web research, not developer input.
