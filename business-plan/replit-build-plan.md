# Build Plan: The Peptide Storefront on Replit

### Stack, APIs, architecture, and a phased build sequence for the two-lane Rx-gated site

*Prepared August 2026. Implements the customer-experience spec. Written for a build on Replit with additional APIs available. ⚖️ = requires counsel/BAA before go-live.*

---

## The prime directive that shapes the whole architecture

**Two systems, one experience, a hard wall between them.**

- **Commerce system (NO PHI):** the storefront, catalog, Lane 1 checkout, marketing, content, COA pages. Optimized for speed + conversion + SEO. Trackers allowed.
- **Clinical system (ALL PHI, HIPAA + BAAs):** intake, ID verification, labs, video visits, prescriptions, member health dashboard, care messaging. Zero ad trackers. Access-controlled, audit-logged.

They share a design system and a single sign-on entry point — **not a database.** A patient's health data must never live in the commerce DB. This wall is the #1 architectural rule; every API choice below respects it.

---

## Recommended stack (Replit-friendly)

| Layer | Choice | Why |
|---|---|---|
| **Framework** | **Next.js (App Router) on Replit** | One framework for storefront + dashboard; SSR/ISR for speed + SEO; huge ecosystem; Replit deploys it cleanly |
| **Language** | TypeScript | Type safety across the money + medical boundary |
| **Styling** | Tailwind CSS + shadcn/ui | Fast, consistent, accessible components; matches the design formula |
| **Commerce DB** | Postgres (Replit DB/Neon) + Prisma | Products, orders, subscriptions (no PHI) |
| **Clinical data** | **Lives in Healthie**, not our DB | EHR-of-record; we hold references (IDs), never records |
| **Auth** | Clerk or Auth.js | SSO across both systems; MFA on clinical |
| **Payments** | **Stripe** (Payments + Billing + Identity) | Cards, subscriptions, and ID verification in one vendor |
| **Content/CMS** | Sanity | Structured education, claims-as-data, COA records |
| **Search** | Postgres FTS → Algolia later | Start simple |
| **Hosting/CDN** | Replit deploy + Cloudflare | Speed, caching, WAF |

---

## The API stack (where your "add more APIs" leverage goes)

Grouped by system so the PHI wall stays intact:

### Commerce-side APIs (no PHI)
- **Stripe** — payments, subscriptions (or Shopify + Loop if you prefer Shopify's commerce primitives; for a Replit custom build, Stripe Billing is lighter).
- **Sanity** — CMS/content.
- **Resend / Klaviyo** — transactional + marketing email/SMS (marketing list is non-PHI; keep treatment data out of it).
- **Algolia** — search (later).
- **Cloudflare** — CDN/WAF/images.
- **PostHog** — product analytics + session replay **(commerce pages only)**.
- **An LLM API (Claude)** — guided-selling assistant + support bot (with the clinical hard-routing firewall) + content drafting. This is where "give Claude more power" pays off: a genuinely helpful on-site product concierge and a back-office content/COA-summarization engine.

### Clinical-side APIs (PHI — all under BAA ⚖️)
- **Healthie** — EHR, scheduling, patient portal, **video visits**, care messaging. The clinical backbone.
- **Stripe Identity** — government-ID + selfie verification.
- **Photon Health** — e-prescribing → your named 503A pharmacy.
- **A labs API** (e.g., a national lab integration) — order sets, results retrieval.
- **The 503A pharmacy's integration** — order routing + status + batch/COA feed.

### The COA transparency system (your differentiator — custom, mostly non-PHI)
- Batch records in Sanity/Postgres → public `/labs/[batchId]` pages (indexable, shareable) → QR codes generated per unit. A pharmacy/manufacturer COA (PDF) upload + parse (LLM to extract purity/lab/date into structured fields) → rendered as a clean public page. This is a small build with outsized brand value.

---

## Architecture diagram (logical)

```
                    ┌─────────────────────────────┐
                    │   Next.js app (Replit)      │
                    │   shared design system      │
                    └───────────┬─────────────────┘
                                │ SSO (Clerk/Auth.js)
              ┌─────────────────┴──────────────────┐
              │                                     │
   ┌──────────▼───────────┐            ┌────────────▼─────────────┐
   │  COMMERCE (no PHI)    │   WALL     │  CLINICAL (PHI, BAA) ⚖️  │
   │  • Catalog/PDP        │  ───────   │  • Intake (Healthie)     │
   │  • Lane 1 cart/Stripe │            │  • Stripe Identity       │
   │  • Subscriptions      │            │  • Labs API              │
   │  • Content (Sanity)   │            │  • Video visit (Healthie)│
   │  • COA public pages   │            │  • Photon e-Rx → pharmacy│
   │  • Analytics/pixels   │            │  • Health dashboard      │
   │  • LLM concierge      │            │  • Care messaging        │
   └──────────┬───────────┘            └────────────┬─────────────┘
              │                                     │
       Postgres (orders,                    Healthie = record of
       products, subs)                      truth; we store only
                                            references/status
```

Data crossing the wall is minimal and one-way-ish: commerce knows "user X has an active Rx subscription + ship status"; it never sees diagnoses, labs, or visit notes.

---

## Phased build sequence

### Phase 1 — Storefront + Lane 1 (weeks 1–4) — *this is what we build first on Replit*
Fully shippable, revenue-generating, no clinical dependencies:
- Next.js + Tailwind + shadcn/ui scaffold, design system from the formula doc.
- Home, collections, Lane 1 PDPs, cart, Stripe checkout, subscriptions.
- Sanity CMS + the education hub (SEO engine live from day one).
- **The public COA lookup system** (`/labs/[batchId]` + QR) — differentiator shipped early.
- Analytics, SEO/schema markup, Core Web Vitals budget in CI.
- **Outcome:** a live, premium, fast storefront selling cosmetic + supplement SKUs with lab transparency. Real revenue while the clinical layer is built.

### Phase 2 — The Lane 2 Rx gate (weeks 4–10) ⚖️
- Auth/SSO + the PHI wall (separate data boundary, tracker-free clinical routes).
- Stripe Identity verification flow.
- Medical intake (one-question-per-screen), state-gating logic.
- Healthie integration: scheduling + video visits + care messaging.
- Labs API integration (order + results).
- Photon e-prescribing → pharmacy routing.
- The three-outcome decision flow (approve/modify/decline + refund path).
- **Outcome:** end-to-end video-Rx flow live in your doctor's licensed states.

### Phase 3 — Member dashboard + retention (weeks 8–14)
- My Treatments, batch COA of what they received, labs-over-time, care messaging, follow-up prompts, subscription self-serve.

### Phase 4 — Intelligence layer (weeks 12–16)
- LLM concierge (guided selling, Lane 1) + support bot with clinical hard-routing.
- Agent-readable commerce (schema, feeds).
- CRO iteration, churn-prediction email flows.

---

## How we'll actually work on Replit

- **You provision:** a Replit project, and API keys/accounts for the vendors as each phase needs them (Stripe first; Healthie/Photon/labs at Phase 2, which is also when BAAs get signed ⚖️).
- **I build:** in this repo (or the Replit repo), phase by phase, committing to the branch + PR you already have. I can scaffold Phase 1 immediately — it needs only Stripe + Sanity keys, and can even start with mock data.
- **Env/secrets:** all keys in Replit Secrets / env vars, never in code. Separate keys for commerce vs clinical.
- **The build order is the risk order:** Phase 1 has zero regulatory dependency, so we ship it while the ⚖️ legal/BAA/LegitScript work (which gates Phase 2) proceeds in parallel.

---

## What I need from you to start Phase 1 now

1. A brand name + basic brand direction (or let me propose 3).
2. Stripe account (test keys to start) + Sanity project.
3. Confirmation to scaffold in this repo vs. your Replit project.
4. The 3 launch SKUs' basics (names, prices, a COA sample to model the schema).

Everything else (Healthie, Photon, labs, pharmacy, LegitScript, BAAs) is Phase 2 and can be lined up while Phase 1 ships.

---

## Immediate next step

The design-formula doc (palette, typography, layout system, component specs) — synthesized from the live teardown of the top peptide/supplement/wellness sites — is the last piece before I can scaffold. That research is running now; when it lands I'll finalize the formula and can begin the Phase 1 build on your go.
