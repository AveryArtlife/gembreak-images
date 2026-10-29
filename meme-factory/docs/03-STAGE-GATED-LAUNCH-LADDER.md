# 03 · The stage-gated launch ladder

The thesis: **spray like a serial deployer, produce like PNUT, and let the market decide how much capital each coin gets.** Every launch starts cheap and finished-looking; money only follows measured reaction. Nothing below is spent on a coin the market has not already voted for.

Numbers in SOL where they are on-chain; dollar figures are vendor prices as of Oct 2026. Conversion assumptions are labelled; they are a model, not a forecast.

## The ladder

| Stage | Trigger (all must hold) | Budget | What happens | Kill rule |
|---|---|---|---|---|
| **0 · Watch** | Signal engine score ≥ 60/100 (see `02-SIGNAL-ENGINE.md`), story passes the no-go list, no produced competitor live | $0 | Ops bot posts the candidate card (story, score, suggested names/tickers with DexScreener conflict check, draft angle). **Human gate 1**: approve or pass, inside 5 minutes. Kit generator starts drafting in parallel (name options, story copy, character prompt, site preview). | Score falls below 40 before approval |
| **1 · Launch** | Gate 1 approved | **~3–5 SOL + $299** (creation 0.02 SOL, creation buy 2–4 SOL, ETI $299, domain ~$15) | Target **T+45 min from first signal**: final name/ticker; token image and 1 hero render; site live on a pre-owned hub domain (`<name>.hub.xyz`) with CA placeholder; X + TG from the persona pool, pins drafted; **create token via PumpPortal with the public creation buy**; CA posted in 3 places; Enhanced Token Info submitted; story thread + 5 memes go out; reply-guy the top 3 news posts; pump.fun livestream opens with the character on screen. | At T+60: < 150 holders or not graduated → freeze spend. Site stays up, one honest "we tried" post, move on. |
| **2 · Confirm** | T+30–90 min: graduated; holders ≥ 300 and rising; top-10 (ex-pool) < 20%; unique buyers/hour up two intervals in a row; story mentions still accelerating | **$1–3K** | 3–5 micro/mid KOL calls (disclosed, paid in SOL); TG raid budget; first creator-fee claim → 50% to the pledge wallet, receipt posted; small DexScreener boost pack; Higgsfield meme batch 2 (12 images); second thread with proofs (Bubblemaps/RugCheck). | Any of: holders flat for 2 hours, top-10 > 25%, dev-labelled wallet selling, story dies (mentions −50% hour over hour) |
| **3 · Scale** | $1–3M market cap; holders ≥ 2,000; 24h volume ≥ $2M; story still in the news cycle; at least one organic mega-account post | **$10–25K** | KOL wave 2 (mid + 1 macro, disclosed); CEX listing packs to MEXC, Gate, Bitget, LBank; CoinGecko + CMC; treasury seeds **project-owned liquidity** (Meteora DLMM/Memecoin pool, locked) to tighten the spread; PR pitch to the reporters who broke the story, led with the pledge receipt; merch drop; Forever-Wall-style UGC mechanic launches. | Volume −70% from peak for 48h with no catalyst → stop paid spend, keep community and receipts going |
| **4 · Institutionalise** | $10M+ sustained 72h; CEX listed; community mods self-organised | **$50K+** | CEX market-making agreement (two-sided quotes, no volume targets); charity partnership announcement; foundation/multisig hand-over plan; second catalyst calendar (court dates, anniversaries, sequels); consider a doxxed front person for the flagship. | Team capacity. Hand to CTO publicly if the team can't run it. |

## Latency budget (the part that beats the spray deployers)

| Step | Target | How |
|---|---|---|
| Signal → candidate card | ≤ 10 min after the story's first cross-platform spike | Polling every 5 min across sources; copycat-launch counter is the fastest tripwire |
| Candidate → approval | ≤ 5 min | One human on call, Telegram button |
| Approval → token live | ≤ 30 min | Kit templates (this repo), pre-aged accounts, pre-owned hub domain, PumpPortal script, image model with a cached style |
| Token live → ETI + thread + livestream | ≤ 15 min | Checklist bot |
| **Total: first signal → produced launch live** | **≤ 60 min** | vs. 2–3 days for a hand-built kit (Cha Cha), vs. 2 minutes for a screenshot-logo copycat |

## Kit factory: what gets generated per launch

Everything in `chacha-forever/` becomes a template with variables:

| Asset | Generated how | Time |
|---|---|---|
| Name/ticker shortlist + conflict check | LLM proposes 10; script checks DexScreener exact-symbol conflicts and copycat count | 1 min |
| Story copy (hero, timeline, FAQ, thread, TG pins) | LLM from the article set, with attribution rules baked in ("according to the family") | 2 min |
| Character | Image model with the house style prompt (`prompts/` pattern) + likeness reference from the story's photos; 4 variations, human picks one | 5–8 min |
| Token image / avatar / banner / OG | `build-logos.py` pattern: character composited into the coin/banner templates | 1 min |
| Site | `site/` template with `CONFIG`; deploy via Vercel API to `<name>.<hub>` | 2 min |
| Socials | Pre-aged persona accounts renamed; pins and bios filled from templates | 3 min |
| Token | PumpPortal `create` with IPFS metadata + creation buy in one tx | 1 min |
| Proof pack | RugCheck/Bubblemaps/Solscan links auto-filled once the CA exists | 0 |

## Portfolio economics (assumptions, not promises)

| Assumption | Value |
|---|---|
| Launches per month at Stage 1 | 20–40 (only stories that clear the gate) |
| Stage 1 cost | ~$900 (3.5 SOL at ~$170 + $299) |
| Stage 1 → 2 conversion | 20% |
| Stage 2 → 3 | 15% |
| Stage 3 → 4 | 15% |
| Expected spend per launch | ≈ $900 + 0.20×$2,000 + 0.03×$17,500 + 0.0045×$50,000 ≈ **$2,050** |
| Monthly spend at 30 launches | ≈ **$60K** |

Revenue levers per coin: creator fees (0.30% of curve volume; 0.95% sliding to 0.05% on PumpSwap), the 2% treasury position (locked, sold on a published schedule), merch. One coin that does $20M of day-one volume pays ~$25–60K in fees; one $PNUT-scale outcome pays for the year. The model lives or dies on Stage 1→2 conversion, which is why the signal engine and the kit quality are the whole product.

## Operating cadence

- **On-call rota**: one approver and one launcher awake at all times (stories break at 3am ET as often as 3pm).
- **Post-mortem per launch** (10 lines): signal score, time-to-launch, copycats at launch, Stage reached, spend, fees earned, what the market said.
- **Weekly**: recalibrate thresholds from the post-mortems; update the no-go list; rotate persona accounts that got rate-limited.
