# Agentic AI for ArtLife: Client Acquisition, Marketing, and Blue-Chip Consignment Sourcing

**A deep analysis of cutting-edge agentic AI initiatives for the luxury art sector**
*Prepared August 2026 · Stack assumed: Apify + Claude Code + two dedicated AI agents (Atlas & Theo)*

---

## Executive summary

The art market is simultaneously an **AI laggard and an AI goldmine**. Surveys in 2025–26 show 84% of galleries use AI daily but only 8% have any formal AI strategy — almost all usage is copywriting and admin. Nobody in the art trade has visibly claimed the two highest-leverage agentic plays:

1. **Being the answer** when a wealthy prospect asks ChatGPT/Claude/Perplexity "who should I buy an Alec Monopoly from" or "best online gallery for blue-chip urban art" (Generative Engine Optimization — GEO/AEO). Roughly 70% of luxury AI queries are unbranded, and ~90% of URLs that AI engines cite are third-party sites, not brand sites. The niche is unclaimed.
2. **Systematic consignment sourcing** — using agents to watch the public signals that precede a sale (estates, art-secured debt, deaccessioning, provenance patterns) and put ArtLife in front of a motivated seller before the auction houses' estates departments do. Roughly $1 trillion of art will change hands generationally within a decade ("the Great Estate Rush"); ~$800M of single-owner collections hit New York in a single recent season.

The operating doctrine that the research overwhelmingly supports is what LVMH calls **"quiet tech"**: AI backstage, humans front-stage. Volume AI outbound is already dead (outbound volume is up ~6x since AI SDRs arrived; reply rates fell by a third), and visible AI in luxury-facing content triggers backlash (the Guess/Vogue AI-model scandal; the 6,000-artist letter against Christie's AI sale). The winning shape is: **agents that research, monitor, enrich, score, and draft — and a human (Avery) who sends, calls, and closes.**

Concretely, this document proposes a two-agent division of labor:

- **Atlas — the demand agent.** Owns marketing and client acquisition: GEO/AEO, content ops, social/fair-circuit listening, buyer-intent signals, personalized collector experiences (nightly lot/artist matching, WhatsApp-style concierge).
- **Theo — the supply agent.** Owns consignment intelligence: collector roster building, provenance mining, trigger monitoring (estates, UCC-1 liens, deaccessions, guarantee patterns), scoring, and warm-path mapping through fiduciaries.

Both orchestrated by **Claude Code** (subagents, MCP, scheduled Routines), fed by **Apify** (25,000+ scrapers exposed as agent tools via the Apify MCP server). Realistic all-in cost: **~$450–1,200/month** before ad spend — pocket change against a single blue-chip consignment.

---

## 1. Why now: the market context

Three structural forces make 2026 the right moment:

**The market has turned.** After two down years, global art sales returned to growth in 2025 — up 4% to $59.6B, with public auctions up 9% ([Art Basel & UBS Global Art Market Report 2026](https://www.artbasel.com/stories/the-art-basel-and-ubs-global-art-market-report-2026)). H1 2026 was the strongest first half since 2022 (~$6.77B across the big three houses, ~70% above H1 2025), and nearly a third of it came from single-owner collections. Confidence is back, but margin pressure (38% of dealers reported lower profits) is forcing the trade to look at automation.

**The Great Wealth Transfer is a supply event, not just a demand event.** ~$83T moves between generations over the coming decades, ~$1T of it in art and collectibles. Recent estates and late-life consignments — Paul Allen, Riggio (~$272M), Leonard Lauder ($400M+), Elaine Wynn, Pritzker — are the visible tip. ~70% of heirs keep *some* inherited art, but taste divergence (boomer Imp/Mod/AbEx vs. heirs who want contemporary and urban art) means enormous tranches will be sold — and the heirs receiving that money skew toward exactly the collector demographic ArtLife already serves. Millennials and Gen Z are now ~three-quarters of the HNW collecting cohort, and Christie's own AI-themed sale drew 48% Millennial/Gen Z bidders and 37% first-time buyers.

**The intelligence baseline is about to shift.** Beowolff Capital's 2025 takeover of Artnet plus a controlling stake in Artsy is explicitly aimed at AI-enabled valuation and analytics over combined auction + primary-market + user-behavior data. Whoever builds their own intelligence layer before those tools commoditize has a 12–24 month edge.

ArtLife's specific position amplifies all three: it was one of the first online-only galleries, it's strong in exactly the segment (urban/contemporary, Alec Monopoly) that inheriting generations buy, and it already operates a buy-and-sell model with an appraisal/consignment funnel (artlife.com/sell) that agentic supply-side intelligence can feed directly.

---

## 2. The doctrine: quiet tech, signal over volume

Everything below obeys four rules distilled from what worked and what blew up in 2025–26:

1. **AI backstage, humans front-stage.** LVMH's internal agent MaIA handles 2M+ requests/month across 40,000 staff, framed as "superpowering the client advisor," never replacing them. The client-facing moment — the call, the WhatsApp thread, the private view — stays human.
2. **Signal-triggered, low-volume, high-context outreach only.** AI-SDR-style volume outbound is saturated and pattern-matched as spam (6x volume, −33% replies). What still works: a real signal (auction result, museum acquisition, liquidity event, collection news) + a human-written note informed by an agent-prepared dossier.
3. **Never reveal the surveillance.** Sensitive triggers (obituaries, divorce filings, debt) may inform *timing*, never *copy*. "I saw the UCC filing" is reputationally radioactive and possibly unlawful in some framings; "we're seeing exceptional demand for [artist] this season" is a normal dealer letter.
4. **Compliance is a feature of luxury, not a tax.** GDPR/CCPA-documented processing, licensed data where possible, APAA/ADAA-grade discretion. Collectors trust dealers who are visibly careful with information.

---

## 3. Workstream A — Atlas: finding clients and marketing ArtLife

### 3.1 GEO/AEO: own the AI answer box (highest leverage, lowest risk)

The single most asymmetric opportunity found in this research. The numbers:

- 82% of very-heavy luxury spenders used AI in recent purchase journeys; 97% of AI-using luxury shoppers intend to keep using it (Bain & Comité Colbert, June 2026).
- ~70% of luxury AI queries are unbranded ("best place to buy street art online", "is Alec Monopoly a good investment").
- ~90% of URLs cited by AI engines are third-party sites — press, directories, marketplaces, forums — not brand sites.
- Traditional search is eroding (AI Overviews cut top-result CTR by up to ~58%).
- **No art gallery or advisory has visibly claimed this niche as of August 2026.**

**What Atlas does:**

- **Query intelligence.** Maintain a living map of the questions collectors actually ask AI engines ("Alec Monopoly price 2026", "urban art investment", "sell my Banksy print", "best online blue-chip gallery"), and run weekly automated checks of what ChatGPT/Claude/Perplexity/Gemini currently answer for each — logging whether ArtLife appears, who does, and which sources get cited.
- **Citation-surface campaigns.** Because 90% of citations are third-party, the play is earned/placed presence on the surfaces AI engines trust: Artsy/Artnet artist and gallery pages, ARTnews/Artnet News coverage, Wikipedia-adjacent accuracy, collector forums, YouTube. Atlas drafts the pitches, tracks placements, and re-tests visibility.
- **Answer-shaped content.** Restructure artlife.com content into direct-answer format: definitive artist guides ("Alec Monopoly: complete price history and buying guide"), comparison pages, "how to sell your [artist]" pages feeding the /sell funnel. Server-rendered HTML (AI crawlers don't execute JS), schema markup, conversational phrasing. Atlas drafts; a human edits voice.
- **The consumer-facing answer for "is X a good investment"** is a content moat: ArtLife has real market expertise and (per the site) appraisal capability — publish the data-backed answers competitors won't.

This is pure "quiet tech": no client ever sees an agent, but every AI-mediated discovery path leads to ArtLife.

### 3.2 Signal-based demand capture (replacing cold outbound)

Instead of AI-sent sequences, Atlas runs a **buyer-signal radar** and hands Avery a short daily list of humans worth a personal note:

- **Auction-result triggers:** someone who just underbid or bought an Alec Monopoly / KAWS / Banksy / Retna lot at auction is in-market this month. Apify actors exist today for LiveAuctioneers, Invaluable, Artsy, and Sotheby's search; schedule post-sale runs and diff against a watchlist of ArtLife-relevant artists.
- **Social intent:** Instagram hashtag/comment scraping (#alecmonopoly, #urbanart, fair tags like #ArtBasel, #FriezeLA) + X keyword monitoring surfaces active collectors, flippers, and new-money entrants. Engagement patterns (who comments on artist accounts, who posts unboxings/instals) beat follower counts.
- **Liquidity-event monitoring:** funding announcements, IPOs, exits, athlete/entertainer contract news in ArtLife's cultural orbit — classic "new wall space" moments. Google News RSS + Apify news actors, classified and scored by the agent before a human sees anything.
- **Fair-circuit capture:** during Miami Art Week / Basel / Frieze, Atlas monitors exhibitor lists, VIP-adjacent public chatter, and geo-tagged posts, and prepares per-person context cards for anyone Avery will meet.

The output format matters: **a daily brief of ≤10 names, each with a one-paragraph dossier and a suggested (human-to-edit) opening line** — not a sequence in a sending tool.

### 3.3 The collector concierge: personalization as product

Two patterns from 2025–26 are directly adoptable:

- **Nightly agentic lot-matching** (the Art Collector IQ pattern): collectors register the artists they own or want; an agent matches every new auction catalogue and ArtLife inventory drop against their profile and sends a personal-feeling alert. For ArtLife this is both a retention product ("your Monopoly just got a comp at Phillips — your piece is likely up 15%") and a consignment trigger (that same alert is the natural moment a collector thinks about selling — route them to /sell).
- **WhatsApp-first white-glove clienteling.** Luxury brands moved VIP relationships to WhatsApp Business API threads: previews, early access, RSVP, hybrid human+AI response. An ArtLife concierge thread — where Atlas drafts replies, preps context on each client, and a human presses send — is the LVMH "superpowered advisor" model at boutique scale.
- **Post-purchase intelligence:** every buyer's collection profile compounds — what they own (from purchases + what they share), what they've asked about, price band, pace. Atlas maintains this in the CRM and flags "ready for the next piece" moments (comp sales, artist news, anniversary of purchase).

### 3.4 Content and creative ops at scale

- Atlas turns each artwork/exhibition into the full derivative set — artist-guide updates, email, IG caption variants, YouTube script, collector one-pagers — from one source brief. This is where the 84%-of-galleries AI usage actually sits today; the edge is doing it *systematically* from a pipeline rather than ad-hoc ChatGPT tabs.
- **AI-personalized video (HeyGen/Tavus) — use invisibly.** Per-recipient faux-personal avatar videos would violate the authenticity rule (see Guess/Vogue backlash). The defensible uses: localization, and rapid production of *real* content (Avery recording once, agents versioning per audience/language).
- **Provenance-rich product pages** double as GEO assets: price history, exhibition record, condition — the pages AI engines quote when someone asks about a specific work or artist.

### 3.5 Agentic commerce: be findable, keep the close human

The protocol stack (OpenAI/Stripe's ACP, Google's AP2 mandates layer) matured in 2025–26, but in-chat luxury checkout has already had a public flop, and art will not be bought *by* agents — high-consideration, relationship-gated goods aren't agent-purchasable. The posture: make ArtLife inventory **machine-readable and quotable** (structured data, clean feeds, possibly an MCP-accessible catalog endpoint) so shopping agents can *discover and shortlist* ArtLife works — then hand off to the human relationship. Watch ACP adoption; don't build checkout for it yet.

---

## 4. Workstream B — Theo: finding blue-chip collectors with art they might sell

This is the highest-value application and the one requiring the most discipline. The economics: consignment supply is the scarcest asset in the trade (dealers historically source only ~15% of inventory from private collectors), mega-galleries have built dedicated estates practices to compete with auction houses for collections, and the generational wave is now breaking. An online-native gallery with an agentic intelligence layer can compete for consignments far above its weight class.

### 4.1 Layer 1 — Roster: who holds what

Theo builds and maintains a structured database of collectors relevant to ArtLife's market (urban/contemporary blue-chip: Basquiat, Haring, KAWS, Banksy, Kusama, Condo, plus the Monopoly ecosystem):

- **Public rosters:** ARTnews Top 200 Collectors (per-collector profiles of what they buy; the 2025 edition itself notes Top 200 collectors going "more selective on blue-chip" — a sell-side signal), Forbes/society coverage, museum boards and patron lists.
- **Provenance mining:** auction lot provenance lines ("From the collection of X"; "acquired from the above by the present owner") reconstructed from catalogues and the Artnet/Artprice databases reveal who bought what, when, and at what price. Holding-period analysis (bought 2014–2016 urban art → 10-year hold → prime resale window) is exactly the kind of pattern an agent can compute across thousands of lots.
- **Exhibition loan credits:** "Courtesy of the collection of…" in museum catalogues, wall labels, and annual reports identifies current holders of specific works — and a *loan returning home* is itself a pre-sale signal.
- **Social graph:** Instagram is the art world's public square. Who follows/comments on artist and gallery accounts, who posts installation shots, who attends which fairs — Apify's Instagram actors map this at ~$1.50–2.70 per thousand results.
- **Licensed wealth intelligence for the top tier:** Altrata/Wealth-X (2M+ curated UHNW dossiers, art-collecting tracked as an attribute, relationship-path mapping) or Windfall. Licensing beats scraping for named individuals — better data and far cleaner GDPR posture.

### 4.2 Layer 2 — Triggers: who's likely to sell, and when

The trade's classic "3 Ds" (death, divorce, debt) have expanded to six (add downsizing, discretion, disposal). Each has a public, monitorable data trail:

| Trigger | Public signal | How Theo watches it |
|---|---|---|
| Death / estate | Obituaries; probate filings; estate-sale listings; auction "estate of" consignments | News/RSS monitoring; auction catalogue diffing. *Time outreach; never reference. Route via estate attorneys/advisors.* |
| Debt / leverage | **UCC-1 financing statements** — art-secured loans are perfected via public state filings, searchable by debtor name | Periodic UCC searches on roster names (state SoS portals / CSC / Wolters Kluwer). A collector with fresh liens on artworks is leveraged. The art-lending book is $34–40B and growing — this signal set is large and almost nobody in the trade mines it systematically. |
| Divorce | Court filings (public in most US states) | *Red-line for direct use.* Timing-only, gated, never referenced. |
| Downsizing / relocation | Real-estate listings of art-hung homes; "collection moves" press; storage/shipper chatter | News + listing monitoring on roster names. |
| Institutional deaccession | Museum board minutes, annual reports, AAMD-era "direct care" sales announcements (e.g., Hispanic Society at Christie's 2025; Phillips Collection at Sotheby's) | News monitoring + auction catalogue classification. Deaccessions also mark which *categories* institutions are exiting. |
| Market behavior | Works from one provenance recurring across sales; short holding periods; estimate cuts; withdrawn lots; heavy guarantee/irrevocable-bid coverage (now ~73–78% of evening-sale value — a guaranteed consignment is a seller who demanded price certainty) | Auction-result scrapers + pattern rules over the accumulated results database. |
| Taste rotation | A collector's *buying* pivots (visible in bidding/social) away from a segment they hold deeply | Roster-level activity diffing. |

**The heir wedge is ArtLife-specific gold:** the classic estate flows to Christie's/Sotheby's trusts-and-estates teams, but the *heirs* — the people deciding what to keep — are the millennial/Gen-Z demographic ArtLife already speaks to. The estate sells the Rothko at auction; the heirs buying urban art with the proceeds, and the mid-tier works the big houses won't flatter, are ArtLife's entry. Mid-tier and unplanned estates are also *more* visible in probate records (sophisticated collections hide in trusts/LLCs), which matches ArtLife's realistic consignment band better than the Top 200 anyway.

### 4.3 Layer 3 — Score, dossier, warm path

- **Scoring.** Theo maintains a per-collector consignment-readiness score: holdings relevance × trigger recency × market timing for their segment (ArtTactic/Artnet analytics tell you *which* blue-chip segments are trading hot — flight-to-quality currently favors Modern and established names, with guarantors concentrated in blue-chip) × approachability (path quality).
- **Dossiers, not lists.** For each high-scorer: what they hold (with provenance receipts), estimated basis and current comps, trigger evidence, mutual connections, suggested approach and talking points. One page. Refreshed automatically.
- **Warm-path mapping.** The approach itself goes through humans: estate attorneys, wealth managers, art advisors (APAA members), family offices, framers, and fair-circuit relationships. Theo's job is telling Avery *who to call and why this week* — e.g., "the estate attorney for X is [name], you share [connection], and the estate includes three Harings appraised in 2019." Relationship-intelligence tools (BoardEx/RelSci within Altrata) automate the path-finding at the top tier.
- **The /sell funnel is the passive twin.** Everything in Workstream A's GEO play ("how to sell your Banksy print" ranking in AI answers) feeds inbound consignments with zero outreach risk. Supply-side GEO is even less contested than demand-side.

### 4.4 Legal and ethical guardrails (non-negotiable)

- **GDPR/CCPA:** compiling dossiers on identifiable individuals is "processing." For EU-resident collectors: documented Legitimate Interest Assessments, minimal retention, suppression lists, and a bias toward licensed data (Wealth-X-style) over scraping. Precedent to respect: CNIL fined KASPR €240K (2024) over scraped contact data; enforcement follows where the *data subject* lives. For a US-focused book of business, keep EU individuals out of scraped pipelines entirely.
- **Platform ToS:** logged-out public scraping is legally gray-to-defensible in the US (hiQ, Meta v. Bright Data), but logged-in scraping breaches ToS, and LinkedIn actively litigates (Proxycurl killed in 2025). Use no-cookie public-data actors; never scrape through an account that matters; never automate outreach from Avery's own LinkedIn/Instagram.
- **Trade norms:** APAA/ADAA codes make discretion the defining professional standard. The practical line: research from public records, published lists, auction provenance, and licensed databases is standard dealer practice; exploiting death/divorce/debt in copy, or approaching grieving families directly, is both unethical and self-defeating. Fiduciary-routed, human-delivered, signal-*timed* — never signal-*referencing*.
- **Confidentiality hygiene:** the most-flagged legal exposure in the 2026 art-market AI literature is galleries pasting collector names, prices, and sales histories into consumer LLM tools. Run everything through API/enterprise endpoints with no-training guarantees; keep the collector database encrypted and access-logged. This is also a selling point to consignors.

---

## 5. Architecture: how Atlas, Theo, Claude Code, and Apify fit together

### 5.1 The stack

```
┌────────────────────────── Human layer ──────────────────────────┐
│  Avery + team: send every message, take every call, close.      │
│  Daily briefs in; approvals out. Nothing auto-sends.            │
└─────────────────────────────────────────────────────────────────┘
                ▲ review queue / daily brief        │ approvals
┌───────────────┴────────────────────────────────────┴────────────┐
│              Orchestration: Claude Code / Agent SDK              │
│  • ATLAS (demand): geo-auditor, signal-scout, content-drafter,  │
│    concierge-prep — as Claude Code subagents                     │
│  • THEO (supply): roster-builder, provenance-miner,             │
│    trigger-watcher, scorer, dossier-writer — as subagents        │
│  • Scheduled via Claude Code Routines / cron ("scrape nightly,  │
│    brief at 8am"); each subagent has restricted tools + its own  │
│    context window                                                │
└───────────────▲──────────────────────────────▲──────────────────┘
                │ MCP (actors as tools)         │ APIs
┌───────────────┴───────────────┐  ┌───────────┴──────────────────┐
│  Apify (data plane)           │  │  Enrichment & records        │
│  IG/X/Maps/news actors;       │  │  Artnet/Artprice (licensed), │
│  LiveAuctioneers, Invaluable, │  │  Wealth-X/Windfall, UCC      │
│  Artsy, Sotheby's actors;     │  │  searches, Clay/Apollo,      │
│  Website Content Crawler;     │  │  email verification          │
│  RAG Web Browser; Schedules   │  │                              │
│  + webhooks wake the pipeline │  │                              │
└───────────────────────────────┘  └──────────────────────────────┘
                       ▼
        Collector/prospect database + CRM (Artlogic/ARTERNAL
        or a purpose-built store) — the compounding asset
```

Key mechanics, all shipping today:

- **Apify MCP server** (`mcp.apify.com`) exposes the entire actor store as tools Claude agents can discover and invoke, with output-schema inference and a configurator to pin a curated toolset (your ~8 core actors, not 25,000). Every call is a paid run — set budget caps and max-results on agent-invocable actors.
- **Apify Schedules + webhooks** handle the deterministic scraping (nightly auction diffs, weekly roster refresh); a run-finished webhook wakes the Claude pipeline to triage results. Agents shouldn't poll; scrapers shouldn't reason.
- **Claude Code subagents** (`.claude/agents/*.md`) give each function its own system prompt, restricted tool list, and isolated context — the scout can't send email; the drafter can't invoke scrapers. Atlas and Theo are best implemented not as two monoliths but as two *families* of subagents under one orchestrator each.
- **Human gate as infrastructure:** drafts land as items in a review queue (or literally as PRs/issues) — the send button is always a person.

### 5.2 Concrete Apify actor shortlist (verified to exist, Aug 2026)

| Purpose | Actor | Cost order |
|---|---|---|
| Instagram profiles/posts/hashtags | `apify/instagram-scraper` family; `apidojo/instagram-scraper` | ~$0.50–2.70 / 1k results |
| X/Twitter keyword + account monitoring | `apidojo/tweet-scraper` V2, Xquik, kaitoeasyapi | ~$0.15–0.40 / 1k tweets |
| LinkedIn public profiles (no-cookie) | `harvestapi/linkedin-profile-scraper` (+email option) | $4–10 / 1k |
| Auction results | `parseforge/liveauctioneers-scraper`, `lexis-solutions/invaluable-scraper`, `parseforge/artsy-scraper`, `powerai/sothebys-search-scraper` | niche PPR; watch for breakage |
| Galleries/advisors/designers by geo | `compass/crawler-google-places` | ~$1.50–5 / 1k places |
| Turn any website into agent-readable text | `apify/website-content-crawler`, `apify/rag-web-browser` | ~$0.20–5 / 1k pages |
| Contact details from domains | `vdrmota/contact-info-scraper` | low |
| News/RSS trigger monitoring | `lokki/news-finder-monitor`, Google News scrapers | low |

Notes: no mature Artnet actor exists (paywalled — license it instead); niche auction actors have small user bases, so build "actor returned empty" alerting and retries; Instagram scraping breaks every ~2–4 weeks by design and the flagship actors absorb that maintenance.

### 5.3 The five pipelines (what actually runs)

1. **Nightly — auction radar (Theo→Atlas shared):** scrape prior-day results for watchlist artists → diff against roster holdings and prospect list → update comps, flag buyers/underbidders (demand) and provenance/guarantee patterns (supply) → items into morning brief.
2. **Weekly — GEO audit (Atlas):** run the query map against the major AI engines → log ArtLife presence and cited sources → generate the citation-surface hit list and content tasks.
3. **Weekly — trigger sweep (Theo):** news/RSS classification for roster names + deaccession announcements + estate-sale listings; monthly UCC-1 search cycle on the top-N roster; score updates; new dossiers for anyone crossing threshold.
4. **Daily — signal brief (both):** ≤10 demand names + ≤5 supply moves, each with dossier and suggested human action. Delivered 8am; everything else stays in the database.
5. **Continuous — content factory (Atlas):** one brief in → derivative set out → human edit → publish; provenance-rich pages compound the GEO position.

### 5.4 Budget reality

~$450–1,200/month all-in for a 1–2 person operation: Apify $39–199 + usage $50–200; enrichment (Clay $149 or Apollo $49–79); email verification ~$20–40; Claude API $50–300 at this volume; optional licensed data (Artnet DB, ArtTactic reports, Wealth-X) is the real discretionary line and worth more than any scraper. Hidden costs: scraper maintenance attention and (if cold email is ever used) deliverability infrastructure — though under the signal-based doctrine, volume sending infrastructure is mostly unnecessary.

---

## 6. 90-day roadmap

**Days 1–30 — Foundations.**
Stand up the collector/prospect database and CRM discipline; pin the Apify actor shortlist behind the MCP configurator with budget caps; define Atlas/Theo subagent files in Claude Code; ship pipeline #1 (auction radar) and #2 (GEO audit — the first audit is the baseline that proves the opportunity); write the compliance SOP (LIA template, EU exclusion rule, no-logged-in-scraping rule, human-send rule).

**Days 31–60 — Intelligence.**
Roster v1: ARTnews 200 intersect urban/contemporary + provenance mining of 5 core artists' auction histories + IG social-graph pass; first UCC search cycle on top names; trigger sweep live; daily brief begins. GEO: first five answer-shaped artist/sell guides published; first citation-surface placements pitched.

**Days 61–90 — Activation.**
First fiduciary-routed consignment approaches from Theo dossiers; collector concierge pilot (lot-matching alerts for 20 best clients, WhatsApp thread for top 10); Miami Art Week prep runs on the full stack (context cards, fair-circuit listening); re-run GEO audit and measure movement; review what the agents got wrong and tighten scoring.

**KPIs:** consignment conversations opened (not sent messages); AI-engine visibility share on the query map; /sell inbound volume; brief precision (fraction of flagged names Avery judges worth acting on — target >30%); zero compliance incidents.

---

## 7. Risks and honest caveats

- **Scraper fragility is routine.** Instagram rotates anti-scraping every 2–4 weeks; niche auction actors go stale. Design for graceful degradation and alerting, not perfection.
- **LinkedIn is the highest-risk surface** — data via no-cookie actors only; outreach there manual or through purpose-built proxied tools, never Avery's own account automated.
- **Reputational asymmetry:** one "how did you know my mother died" moment costs more than a year of pipeline wins. The timing-not-referencing rule and fiduciary routing are load-bearing, not decorative.
- **The window is real but closing:** Artnet/Artsy under Beowolff will productize market intelligence; auction houses already run taste-matching recommendation engines (Sotheby's Thread Genius lineage). The durable moat isn't the tools — it's the proprietary collector database, the GEO position, and the relationships the system feeds. Start compounding now.
- Two research caveats: the reported March 2026 shutdown of OpenAI's Instant Checkout is single-source; and artsy.net/artnet news findings partly rely on secondary coverage. Neither affects the recommendations.

---

## Appendix: key sources

Market context: [Art Basel & UBS Global Art Market Report 2026](https://www.artbasel.com/stories/the-art-basel-and-ubs-global-art-market-report-2026) · [ARTnews on the Great Estate Rush](https://www.artnews.com/art-news/market/great-estate-rush-that-is-reshaping-art-market-1234794331/) · [Bloomberg "Great Boomer Art Dump"](https://www.bloomberg.com/news/newsletters/2026-08-01/no-one-is-ready-for-the-great-boomer-art-dump) · [ArtTactic H1 2026 via artcollection.io](https://artcollection.io/blog/auction-house-h1-2026-rebound-collectors) · [BofA US art market 2025](https://newsroom.bankofamerica.com/content/newsroom/press-releases/2026/03/u-s--art-market-rebounds--posting-a-23--increase-in-auction-sale.html)

AI in luxury/art: [Bain & Comité Colbert 2026](https://www.bain.com/about/media-center/press-releases/2026/ai-emerges-as-a-strategic-priority-for-luxury-as-accelerating-consumer-use-challenges-industry-to-reinvent-customer-discovery-and-experience-bain-company-and-comite-colbert/) · [LVMH MaIA / VivaTech (Forbes)](https://www.forbes.com/sites/stephaniehirschmiller/2025/06/15/how-ai-is-powering-the-luxury-industry-now-viva-tech-lvmh-loral/) · [LVMH "quiet tech" at NRF 2026](https://ouispeakfashion.com/what-must-luxury-protect-in-the-age-of-ai-lvmhs-vision-at-nrf-2026/) · [Christie's Augmented Intelligence results (ARTnews)](https://www.artnews.com/art-news/market/christies-ai-art-sale-augmented-intelligence-controversy-surpasses-expectations-1234734870/) · [Beowolff/Artnet/Artsy AI plans](https://news.artnet.com/market/ai-art-market-revolution-2666766) · [Gallery AI usage vs. policy (ARTnews)](https://www.artnews.com/art-news/news/artificial-intelligence-ai-art-galleries-report-1234777334/) · [Holland & Knight on AI in the art market](https://www.hklaw.com/en/insights/publications/2026/04/artificial-intelligence-in-the-art-market) · [Luxury AI visibility gap (Modaes)](https://www.modaes.com/global/back-stage/from-google-to-chatgpt-the-luxury-industry-faces-a-new-battle-for-visibility) · [Guess/Vogue AI backlash (CNN)](https://www.cnn.com/2025/07/31/style/vogue-ai-models-guess-campaign) · [AI SDR saturation data (Salesmotion)](https://salesmotion.io/blog/best-ai-sdr-tools-2026)

Consignment intelligence: [ARTnews Top 200 Collectors](https://www.artnews.com/art-collectors/top-200-collectors/top-200-collectors/) · [Galleries building estates practices (ARTnews)](https://www.artnews.com/art-news/market/art-galleries-securing-collector-estates-1234570394/) · [Art-secured lending rise (The Art Newspaper)](https://www.theartnewspaper.com/2018/12/06/in-debt-we-trust-the-rise-of-art-secured-lending) · [BofA art lending (Family Wealth Report)](https://www.familywealthreport.com/article.php/Bank-Of-America-Leans-Into-the-Fine-Art-Market) · [UCC search practice (Wolters Kluwer)](https://www.wolterskluwer.com/en/expert-insights/best-practices-ucc-filings-and-searches) · [Sotheby's consignment roadmap](https://www.sothebys.com/en/articles/roadmap-for-consigning-property-at-auction) · [NYU provenance research guide](https://guides.nyu.edu/provenance/art-auctions) · [Altrata UHNW prospecting](https://altrata.com/guides/prospecting-ultra-wealthy) · [CASE wealth-screening GDPR guidelines](https://www.case.org/system/files/media/inline/CASE%20guidelines%20on%20wealth%20screening%20prospect%20research%20and%20collecting%20contact%20details1.pdf) · [hiQ v. LinkedIn analysis](https://www.fbm.com/publications/what-recent-rulings-in-hiq-v-linkedin-and-other-cases-say-about-the-legality-of-data-scraping/) · [Meta v. Bright Data](https://www.quinnemanuel.com/the-firm/news-events/client-alert-meta-v-bright-data-significant-decision-for-web-scraping-industry/) · [APAA mission & ethics](https://www.artadvisors.org/association-of-professional-art-advisors-mission)

Tooling: [Apify MCP server docs](https://docs.apify.com/platform/integrations/mcp) · [Apify pricing](https://apify.com/pricing) · [RAG Web Browser](https://apify.com/apify/rag-web-browser) · [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) · [Claude Code scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks) · [Google/Yahoo sender requirements](https://www.valimail.com/blog/google-yahoo-email-sender-requirements-faqs/)
