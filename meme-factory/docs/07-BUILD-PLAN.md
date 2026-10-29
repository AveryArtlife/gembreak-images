# 07 · Build plan: from this repo to a running factory

## What exists today
- `chacha-forever/`: a complete produced-launch kit (docs, brand pipeline, site template with `CONFIG`, Higgsfield prompt pack, export scripts). It is the template the factory stamps out.
- `meme-factory/signals/`: a working signal engine prototype (Google Trends RSS, GDELT news velocity, DexScreener copycat counter and ticker-conflict check, Google Alerts feeds, Apify runner) with a 0–100 scorer and a `watch` loop. Stdlib only. Tested live on the Cha Cha story.
- Research: operator audit, traction tools, legal lines, pseudonymous ops.

## Phase 1 · Semi-automated (2 weeks, one engineer + you)
Goal: a Telegram ops channel that pings you with a scored candidate card within 10 minutes of a story spiking, and a one-command launch once you approve.

| Day | Deliverable |
|---|---|
| 1–2 | Signal engine as a service: `watch` loop in a container (Fly.io/Railway), Postgres for history, Telegram bot posts candidate cards (score, notes, copycat table, suggested names with conflict check). Add Apify actors from `02-SIGNAL-ENGINE.md` (Instagram post engagement, TikTok hashtag, X search, Reddit). |
| 3–4 | pump.fun new-token stream (PumpPortal WebSocket `wss://pumpportal.fun/api/data` `subscribeNewToken`) → live copycat counter per keyword (seconds, not minutes). Helius webhooks for holder counts on our own launches. |
| 5–7 | Kit generator: LLM fills the `chacha-forever` templates (names, story copy with attribution rules, thread, pins, FAQ); image model renders the character from the house prompt + story photo as likeness reference; `build-logos.py` composites coin/banner/OG; site deployed to `<name>.<hub>` via Vercel API. Human picks the character and name. |
| 8–9 | Launcher: PumpPortal `create` (IPFS metadata + creation buy in one tx) from the launch wallet; post-launch script edits the X pin, TG pin and site `CONFIG`; ETI submission checklist; proof links auto-filled. |
| 10 | KPI tracker: DexScreener pair stats + Helius holders + top-10 concentration every 60s; stage triggers from `03-STAGE-GATED-LAUNCH-LADDER.md` as alerts. |
| 11–12 | Dry runs on devnet / a throwaway token; on-call rota; post-mortem template. |
| 13–14 | Legal review of pledge language, KOL disclosure template, no-go list (`05-LEGAL-LINES.md`). First live story. |

## Phase 2 · Automated edges (weeks 3–6)
- X pay-per-use API for scheduled persona posts; Telegram bot for pins/announcements (humans still reply).
- Persona/account pool: 5 aged X + TG sets, rotation and health checks.
- KOL CRM: rates, last-10-call quality, disclosure compliance, payment ledger from the treasury multisig.
- Stage-2/3 playbooks as checklists the bot walks you through (boost packs, CG/CMC forms, CEX packs generated from the kit).
- Project-owned liquidity playbook (Meteora DLMM/Memecoin Pool) with position templates.
- Scoring recalibration from post-mortems (which signals predicted Stage 2?).

## Phase 3 · Portfolio (month 2+)
- 20–40 launches/month capacity; weekly review of conversion by story type (animal-justice, animal-cute, absurd-news, sports moment, celebrity moment).
- A hub brand for the factory ("launched by …") that accumulates trust across coins: public ledger of every launch, its pledge receipts, and its outcome. This is the legitimacy layer nobody else has, and it compounds.
- Optional: open the hub as a launchpad for others (fee share), the Clanker/Believe model with vetting.

## Stack
Python 3.12 workers · Postgres · Telegram bot (ops) · Apify · Google Trends RSS + GDELT · PumpPortal (create + stream) · Helius (RPC, webhooks) · DexScreener API · Vercel API · Claude/GPT for classification and copy · Higgsfield (+ a fast fallback image API) · Meteora/Jupiter SDKs (Stage 3) · Squads multisig.

## Team
| Seat | Load |
|---|---|
| Engineer (signals, launcher, trackers) | full-time for 6 weeks, then part-time |
| Designer/content (character pipeline, memes, video) | full-time |
| Community lead (TG/X, raids, livestream host) | full-time, on-call rota |
| Ops/legal liaison (KOL ledger, CEX packs, pledge reports, counsel) | part-time |
| You | approver, launcher of record, capital allocation |

## Monthly cost (excluding stage budgets)
| Item | Est. |
|---|---|
| Apify (10 keywords, tiered cadence) + Starter plan | ~$1,700 + $39 |
| Helius + PumpPortal + RPC | $100–300 |
| X API pay-per-use (posts) | $50–150 |
| Hosting (Fly/Railway, Vercel, Postgres) | $50–100 |
| Image generation credits | $200–500 |
| Domain pool (hub + 10 brand domains) | $300 one-off |
| Legal retainer | $1–2K (plus $5–10K setup) |
| Persona SIMs/VPN | $50 |
| **Run-rate** | **~$3.5–5K/month** + stage budgets (~$60K/month at 30 launches, see 03) |

## Risks and the mitigation we already designed
| Risk | Mitigation |
|---|---|
| Launching on a story that isn't memeable (false positives) | Copycat counter + human gate; thresholds recalibrated weekly |
| Being late anyway | Pump.fun stream tripwire (seconds), kit templates, pre-aged accounts, pre-owned hub domain |
| Platform bans | Official APIs, no bought accounts, humans in community, rotation |
| Legal | Red list is hard-coded into the process; counsel on retainer; pledge receipts |
| Reputation ("they coin tragedies") | No-go list; animals/absurd/joy stories only; pledge mechanic; public ledger of outcomes |
| SOL price / market regime | Stage budgets in SOL for on-chain items; pause rule when memecoin sector volume falls below a threshold |
