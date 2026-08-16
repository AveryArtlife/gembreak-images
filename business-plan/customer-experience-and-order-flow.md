# Customer Experience & Order Flow Specification

### Screen-by-screen design of the two-lane peptide storefront with a real Rx gate

*Prepared August 2026. Implements the model in `retail-storefront-real-gate-model.md`. This is the product spec — the actual screens, states, and flows. Pairs with the design formula and Replit build plan (separate docs).*

---

## The mental model: one storefront, two lanes, one gate

Every visitor lands in a premium retail experience. What they can *do* forks by product type:

- **Lane 1 (OTC):** cosmetic serums + supplements → browse → add to cart → checkout → ship. Pure ecommerce.
- **Lane 2 (Rx-gated):** peptide protocols → browse → "Start Visit" → intake → **video consult** → provider decision → (if approved) pharmacy → ship + subscription.

The genius of the design is that **both lanes feel like the same store.** The consumer never experiences a jarring "now you're entering a medical portal" wall — the medical gate is woven into what feels like a smart, premium checkout. But behind the scenes, Lane 2 is a real clinical encounter with a real decision.

---

## Global experience principles

1. **Retail on the surface, medicine in the mechanism.** Optimize the storefront like any DTC brand; keep the prescribing decision genuinely clinical.
2. **Trust is the aesthetic.** In a category defined by sketchy sites, *looking* legitimate and being radically transparent (public COAs, named doctor, named pharmacy) is the core visual differentiator.
3. **Speed is a feature.** LCP <2.5s, INP <200ms. Every 0.1s ≈ +8% conversion.
4. **Mobile-first.** ~70% of traffic and the weaker conversion surface — design there first.
5. **PHI firewall.** Lane 2 clinical surfaces run on a separate, tracker-free, HIPAA-compliant subsystem. No ad pixels touch intake/consult/dashboard.
6. **Declines are graceful.** A "not approved" is a refund + alternative, never a dead end — this is both good UX and the legal integrity of the gate.

---

## The full sitemap

```
Home
├── Shop
│   ├── Skincare (Lane 1 — OTC)          → GHK-Cu, Matrixyl, Argireline serums
│   ├── Supplements (Lane 1 — OTC)        → collagen, NAD+ precursors
│   └── Peptide Protocols (Lane 2 — Rx)   → BPC-157, sermorelin, CJC/ipa, NAD+, (pending five)
├── How It Works                          → the video-Rx process, explained + trust
├── The Science                           → education hub (SEO engine)
├── Our Doctors                           → named physician(s), credentials
├── Lab Results / Verify                  → public /labs/{batch-id} COA lookup
├── About / Trust                         → licensing, pharmacy partners, compliance
├── Start Visit  (primary CTA)            → the Lane 2 funnel entry
├── Account
│   ├── Orders & Subscriptions            → Lane 1 + Lane 2 refills
│   ├── My Treatments (PHI)               → protocols, visit history, messages, labs
│   └── Care Messaging (PHI)              → provider/care-team chat
└── Cart / Checkout
```

---

## Screen-by-screen: the shopping experience

### 1. Homepage
**Job:** establish premium legitimacy in 3 seconds, route to both lanes, seed trust.
- **Hero:** clean, editorial. One headline (the positioning: legitimate + transparent peptides), one subhead, two CTAs — "Shop Skincare" (Lane 1, low-commitment entry) and "Start Visit" (Lane 2, high-intent).
- **Trust bar** directly under hero: "Licensed U.S. physicians · Named 503A pharmacy · Every batch lab-tested · [X] verified reviews." This bar is the whole brand thesis in one strip.
- **Category tiles:** Skincare / Supplements / Peptide Protocols — visually equal so the store feels like retail, not a clinic.
- **"How it works" 3-step** mini-explainer (Choose → Video visit → Delivered).
- **Featured protocol** (BPC-157 — the demand magnet) with "See if it's right for you."
- **Science/education teasers** (SEO + authority).
- **Social proof:** reviews, press, the named doctor's face + credential.
- **Transparency showcase:** "Look up any batch" → live COA lookup widget.

### 2. Collection / category pages
- Retail grid, fast filters. Lane 1 cards show price + "Add to Cart." Lane 2 cards show "from $X/mo" + "Start Visit" (never "Add to Cart" — the framing discipline).
- Lane 2 cards carry a subtle "Rx" pill and "Requires video consult" microcopy so expectations are set.

### 3. Product Detail Page — Lane 1 (OTC serum/supplement)
Standard best-in-class DTC PDP:
- Above fold: product render, name, price, star rating + review count, subscribe-and-save toggle, one-tap wallets (Shop/Apple/Google Pay), key benefit bullets.
- **Batch COA link** ("View this batch's lab results" → QR/`/labs/{id}`) — the differentiator, on every product.
- Ingredient/dose transparency, "the science" citations, UGC, reviews, sticky buy bar on mobile.

### 4. Product Detail Page — Lane 2 (Rx peptide protocol)
Looks like a premium PDP but reframed as a *treatment*:
- Above fold: clean product/vial imagery, protocol name, "from $X/mo," what it is, who it's for, **"Start Visit"** CTA (not add-to-cart).
- **Explicit expectation-setting box:** "This is a prescription treatment. You'll complete a medical intake and a video visit with a licensed provider who will determine if it's appropriate for you. If it's not, you're not charged for medication." — this single box is doing heavy legal + UX work: it frames the sale as a medical service and normalizes the possibility of "no."
- Mechanism explainer, evidence/citations, what's included (medication + provider + pharmacy + follow-up), transparent pricing breakdown, FAQ (safety, side effects, legal status stated honestly), the named doctor, the named pharmacy, batch COA transparency.
- Reviews framed as treatment experiences (compliance-reviewed, no disease-cure claims).

---

## Screen-by-screen: the Lane 2 Rx gate (the heart of the model)

This flow must feel like a smooth premium checkout while being a genuine clinical encounter. Steps:

### Step 1 — Goal / product selection
Entered via "Start Visit" from a protocol PDP or the quiz. If they came from the quiz ("what are you optimizing? recovery / metabolic / longevity / performance"), it recommends protocol(s). Retail feel: "building my order."

### Step 2 — Account + identity
Create account → **government-ID + selfie verification** (Stripe Identity/Persona). Framed as "verify it's really you, for your safety and to send your prescription" — feels like premium KYC, satisfies a LegitScript + safety requirement.

### Step 3 — Medical intake
Structured, one-question-per-screen, progress bar, mobile-optimized (the high-completion quiz pattern). Real medical history, medications, contraindication screening, goals. This is simultaneously the highest-converting UX pattern *and* the clinical record. State-gating: if the user's state isn't served (no licensed provider), route them to a waitlist + Lane 1 products instead of a dead end.

### Step 4 — Labs (protocol-dependent) ⚖️
For protocols where standard of care indicates: order a lab panel (partner lab; requisition + location finder, or at-home kit). Some lower-risk protocols may proceed to visit with labs as follow-up per the doctor's protocol. UX: "Your provider needs a baseline to prescribe safely" — trust-building, not friction-for-friction's-sake.

### Step 5 — Schedule + conduct the video visit
- Booking UI (Healthie-backed) → synchronous video with a provider licensed in the patient's state.
- Waiting-room screen sets expectations: "Your provider will review your history and labs and decide what's appropriate. Not every treatment is right for everyone."
- The visit is a **real evaluation.** Provider can approve, modify (different peptide/dose), or decline.

### Step 6 — The decision (three real outcomes)
- **Approve** → prescription created, patient sees their protocol + transparent total, confirms subscription. → Step 7.
- **Modify** → provider recommends a different protocol/dose; patient consents.
- **Decline** → clear, kind explanation + alternatives (a Lane 1 product, a different peptide, "see your PCP"), **full refund of any consult/medication charge.** This path must be genuinely built, not a theoretical branch — a nonzero decline rate is the model's legal backbone.

### Step 7 — Fulfillment + subscription
- Rx routed (Photon) to the **named 503A pharmacy** → compounded against a COA'd batch → shipped.
- Patient lands in **My Treatments** dashboard: protocol, next refill, batch COA of what they received, care messaging, follow-up schedule.
- Subscription with prepaid-quarterly option; refills tied to required follow-up visits/labs per protocol (clinical + retention).

---

## Post-purchase: the retention engine (the member dashboard)

The dashboard is where retention and ongoing-relationship legitimacy both live:
- **My Treatments:** active protocols, adherence, next shipment, dose schedule, injection/technique education.
- **Batch transparency:** the COA for the exact lot the patient received (nobody else does this — huge trust + differentiation).
- **Labs over time:** baseline + follow-up results with plain-language interpretation (Function Health-style).
- **Care messaging:** async provider/care-team chat (clinical questions hard-routed to humans, never AI).
- **Follow-up prompts:** "Time for your check-in visit to continue your protocol" — required for refills, doubles as the ongoing-relationship evidence.
- **Reorder / adjust / pause / cancel:** easy self-serve (billing transparency is the #1 telehealth complaint category — make it painless).

---

## AI layer (with the clinical firewall)

- **Guided-selling assistant (Lane 1 + product discovery only):** conversational "what are you trying to improve?" → recommends OTC products or routes to "Start Visit." Never answers medical questions.
- **Support AI:** order/subscription/shipping/billing only. Anything clinical (dosing, side effects, eligibility) → hard-routed to the care team. This split is both compliance and good care.
- **Agent-readable commerce:** schema.org/Product + FAQ markup, clean COA/pricing data → visible to ChatGPT/Google shopping agents. Trust signals double as AI-ranking signals.

---

## The states every screen must handle

- Out-of-state visitor (no licensed provider) → waitlist + Lane 1, never a hard dead end.
- Declined patient → refund + alternatives.
- Lab-out-of-range → provider review before any prescription.
- Subscription paused/failed payment → graceful dunning, easy fix.
- Batch lookup for a lot not found → clear message + support.

---

## What this delivers

A store that **feels like buying from Aesop or Ritual** and **operates like Hims** — premium retail experience, real medical gate, radical transparency as the visual brand. The next two docs turn this into (a) a concrete design formula (palette/type/layout/components synthesized from the top sites) and (b) a Replit build plan with the API stack. The site-teardown research feeding the formula is running now.
