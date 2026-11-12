# 01 · Operator audit: who launches memecoins at scale, who makes money, and where the gap is

Date: 2026-10-29. Sources at the end. Figures are the best available; several come from on-chain analytics firms rather than audited reports.

## The short version

Four kinds of operators run the launch economy today. Three of them make money without ever building anything a holder could trust. None of them combines **speed**, **production quality** and **honest proofs**. That combination is the gap.

| Archetype | What they do | Evidence of scale | Why it works | Why we don't copy it |
|---|---|---|---|---|
| **A. Bundling devs** | Create the coin and buy a hidden chunk in block 0 through 2–20 "fresh" wallets, then sell into the first pump. | Bitquery, 8.2M pump.fun launches (Oct 30 2025 → Oct 7 2026): devs bundled on **21%** of launches; devs + bundles netted **$579M** vs **$31.5M** for independent snipers. | They own the bottom of the curve before anyone can see it. | It is the single behaviour every terminal now flags in red, it ends the coin in minutes, and selling a hidden position into buyers you induced is fraud exposure, not a grey area. |
| **B. Serial spray deployers** | Launch hundreds of coins a day, each a lottery ticket; harvest the 0.7% that graduate and the tiny early profits on the rest. | Arkham-derived reports: one wallet **29,834** launches, **208** graduated (0.7%), **~$3.8M** trading profit; top 25 deployers **~770K** tokens / **~$128M**; 12 clusters averaged 320 launches each and were **18%** of all creations (Jan–Apr 2025). | Volume. Creation costs ~0.02 SOL; a coin is a $3 bet. | Zero brand, zero trust, zero survival. 79% of pump.fun tokens stop trading on day one. Our own Cha Cha scan: 15+ copycat launches, best at $8.6K. |
| **C. Platforms and agents (picks and shovels)** | Capture a fee on creation and on every trade. | Clanker (Base): **$50M+** cumulative fees, **$8M in one week** (Feb 2026), acquired by Farcaster; Bankr spun out its own launcher Feb 2026; Believe (Solana) turns an X reply into a token; pump.fun itself (10–30K launches/day, 50% of revenue buys $PUMP). | Whoever owns the venue earns on all the lottery tickets. | Not our business today. But the model tells us what the venues reward: speed, social-native triggers, and fee sharing with creators. |
| **D. Produced launches** | A real character, site, socials, community and a story people repeat for free. | $PNUT ($2.4B), $MOODENG (~$700M), $CHILLGUY (~$650M). Each one had a recognisable image, fair launch, and a crowd that distributed it. | Attention compounds on something that looks finished. | This is us. The problem is that these launched *inside* the news window by luck of timing, not by system. |

**The gap:** a system that produces a D-grade launch at A/B speed (under an hour from signal), with capital that only scales when the market says yes.

## What the venues and tools reward (the mechanics we design for)

- **pump.fun front page:** position is driven by recent on-chain activity; third-party measurement puts the top-10 at roughly 100 "bumps" per minute. Graduation (~$69K market cap) is a visibility step-function because PumpSwap pairs get indexed everywhere.
- **Terminals (Axiom, Photon, BullX, GMGN, Trojan):** rank by volume, transactions, unique buyers per hour and token age; they label dev %, bundles, snipers, top-10 %. GMGN's Solana trending on Oct 20 2026 had pump.fun as launchpad for 15 of the top 20.
- **DexScreener:** free indexing within minutes once liquidity exists; **Enhanced Token Info** $299 (profile, logo, socials; ~15 min processing); **Boosts** $99–$3,999 (500 boosts = Golden Ticker); a July 2026 sample showed boosts of 100–600 SOL on competing launches. Research outlets now treat an early paid boost as a *risk signal*, so boosts are a hour-2 tool, not a minute-1 tool.
- **Telegram call channels and KOLs:** $100–$1.5K per micro post, $1.5–8K mid, $8–50K+ for 300K+ accounts. Calls work when the chart already moves; they do not start a chart.
- **CEXs:** MEXC lists hot pump.fun tokens within hours to days once they trend with real holders (461 new spot tokens Nov 2024–Feb 2025, more than Gate and Bitget). Gate works through pre-commitments. Bitget via MemeX. Listing desks look at holders, top-10 concentration, volume, socials and whether the project answers email.

## Failure modes we have to engineer out

1. **Late.** The story breaks, six copycats launch in the first hour with a screenshot logo, the narrative is "burned" by the time a produced launch appears. (Cha Cha: Oct 26 story, 15 launches by Oct 29, none produced.)
2. **Invisible.** No ETI, no socials, no livestream, so the token is a bare ticker on DexScreener.
3. **Untrusted.** Bundled supply, unknown dev, LP unclear. One red flag on Bubblemaps and the terminal crowd leaves.
4. **Over-funded too early.** Paying KOLs before there is a chart burns the budget and signals desperation.
5. **No second act.** Sadness/outrage alone fades in 3–5 days; coins without a fun layer and a UGC mechanic die on day 4.

## Operators and products to keep watching

| Who | Why | How to track |
|---|---|---|
| Clanker / Bankr (Base) | AI-agent launch UX; fee-sharing model; best signal of "launch from a social post" | clanker.world, Bankr changelog |
| Believe (Solana) | Tweet-to-token; dynamic anti-snipe fees; graduation on engagement thresholds | believe.app, @launchacoin |
| pump.fun top deployers | What spray looks like; what tickers they hit first (they are a free virality oracle: when 20 copies of a story launch in an hour, the story is memeable) | Arkham clusters; PumpPortal/Moralis new-token streams |
| Bitquery investigations | Monthly bundling/sniping stats; case studies (KIMCHI: 3 linked wallets took $104K in 9 minutes) | bitquery.io/investigations |
| DexScreener boost leaderboard | Who is paying to be seen, and whether it works | `/token-boosts/latest/v1` |
| Pons and other new launchpads | Claims of 10K+ daily deployments (unverified) | DefiLlama launchpad revenue |

## Sources
- Bitquery, "Pump.fun Devs' Bundles Made $579M+, Snipers Just $31.5M" (Oct 2026): https://bitquery.io/investigations/pump-fun-snipers-bundles
- Bitquery, KIMCHI case: https://bitquery.io/investigations/kimchi-pumpfun-launch-snipers
- Arkham-derived deployer analyses (Medium summaries, treat as indicative): https://medium.com/@porwalabhay830301/pump-fun-deployers-exposed-arkham-analytics-reveals-3-8m-profit-pattern-7540d37cc181 , https://medium.com/@MedallionAnalytics/how-serial-deployers-drain-solanas-ecosystem-f49110279bb9
- crypto.news, 79% day-one dropout (Oct 2026): https://crypto.news/pump-fun-memecoin-trader-fatigue-token-survival/
- Clanker fees: https://cointelegraph.com/news/clanker-ai-memecoin-fees-355k-tokens , https://www.kucoin.com/news/articles/clanker-protocol-reaches-8-million-weekly-fee-milestone-as-ai-agent-social-trading-ignites-base
- Believe: https://www.dextools.io/tutorials/what-is-believe-tweet-to-token-launchpad-2026
- DexScreener ETI: https://marketplace.dexscreener.com/product/token-info ; boosts analysis: https://openliquid.io/blog/dexscreener-boost-feature-explained/ , https://yellow.com/research/pump-fun-creator-tokens-210-percent-surge-july-2026
- KOL rate cards: https://cryptokolz.com/memecoin-influencers , https://www.luvkaizen.com/solutions/crypto-kol-agency
- pump.fun front-page heuristics: https://medium.com/@jump_bit/the-cheapest-way-to-hit-pump-funs-front-page-in-2026-0be90690e23a
- MEXC listing velocity: https://acionista.com.br/mexc-e-a-corrida-do-ouro-on-chain-velocidade-estrategia-e-valorizacao/
