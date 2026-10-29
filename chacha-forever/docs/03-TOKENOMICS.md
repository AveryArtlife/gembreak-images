# 03 · Tokenomics: $CHA

> Numbers marked **(verify)** change on pump.fun's side without notice. Confirm each one in pump.fun's docs on launch morning and update this file.

## Summary

| Item | Value |
|---|---|
| Chain | Solana (SPL) |
| Launchpad | pump.fun (bonding curve → PumpSwap) |
| Name / Symbol | Cha Cha Forever / **CHA** |
| Total supply | **1,000,000,000 CHA** (pump.fun fixed supply, 6 decimals) |
| Presale / airdrop / team allocation | **None. 0%.** |
| Mint authority | Revoked (pump.fun default) |
| Freeze authority | None (pump.fun default) |
| Metadata update authority | Revoke after the token image/description are final (pump.fun feature since Jan 2026) |
| Launch-wallet buy | 1.5–2.0% of supply in the creation transaction (public wallet, see below) |
| Liquidity | Protocol-managed. On graduation the curve's SOL and remaining tokens migrate to the canonical PumpSwap pool. **(verify LP burn/lock wording in docs; historically pump.fun burned the LP.)** |
| Creator fees | 0.30% of bonding-curve volume; tiered 0.95% → 0.05% on PumpSwap by market cap (Smithii, Oct 2026) **(verify)**. Older guides say 1% curve fee with 0.05% to creator. |
| The Cha Cha Pledge | 50% of all creator fees → animal welfare + family advocacy; 30% → growth; 20% → ops |

---

## 1. Distribution: 100% fair launch

Every token enters circulation through the bonding curve. Nobody, including the team, receives tokens outside the public market.

Why: the two biggest animal coins ($PNUT, $MOODENG) were fair launches. Traders' first on-chain check is Bubblemaps and the holder tab; a team allocation or bundled wallets is the fastest way to get labelled a rug in minute one.

### Launch-wallet buy (the only "insider" position, and it is public)
- Buy **1.5–2.0% of supply** inside the creation transaction (roughly 2–3 SOL at curve-start prices; price it day-of).
- Wallet address published in the pinned tweet, TG pin, and on the site **before** launch, labelled "Cha Cha Launch Wallet".
- Pledge, in writing: **no sells for 30 days**, then no more than 10% of the remaining position per week, each sale announced in advance.
- Why not 0%: with no creation buy, snipers own the whole bottom of the curve and dump on the community within minutes. A small, public, locked position is the honest alternative.

### Sniper and bundle policy
- No bundling. No additional wallets buying in the first block.
- The CA goes out at the same second on X, Telegram and the site. Never pre-shared, never DM'd.
- Launch from a fresh wallet funded from a CEX withdrawal, so wallet-history tools show nothing suspicious.

---

## 2. Bonding curve and graduation

| Stage | What happens | Numbers **(verify)** |
|---|---|---|
| Creation | Token minted, metadata set, creation buy executed | Creation cost ≈ 0.02 SOL |
| Curve | Price follows pump.fun's constant-product virtual curve | Trade fee 1.25%; creator receives 0.30% of volume |
| Graduation | When the curve fills (~$69K market cap; ~85 SOL raised historically) the token migrates automatically to a canonical PumpSwap pool | Migration fee ≈ 0.015 SOL |
| PumpSwap | Open AMM trading, indexed by DexScreener / Jupiter / all terminals | Creator fee tiers: 0.30% until ~420 SOL mcap, then 0.95% sliding down to 0.05% above ~98,240 SOL mcap |

Target: graduate **inside hour one**. A coin that sits on the curve for a day is a coin nobody wanted.

---

## 3. Creator fee model and the Cha Cha Pledge

### Fee accrual per $1M of volume

| Phase | Creator share | Fee per $1M volume |
|---|---|---|
| Bonding curve | 0.30% | $3,000 |
| PumpSwap, small cap (just above 420 SOL) | up to 0.95% | up to $9,500 |
| PumpSwap, mid cap | sliding | $500–$9,500 |
| PumpSwap, large cap (≥ 98,240 SOL ≈ $20M+) | 0.05% | $500 |
| *Older fee model, if still in force* | 0.05% everywhere | $500 |

### Scenario table (illustrative, not a forecast)

| Day-1 volume | Creator fees (new model) | Creator fees (old model) | → Pledge wallet (50%) |
|---|---|---|---|
| $2M | ~$6–15K | ~$1K | $3–7.5K |
| $20M | ~$25–60K | ~$10K | $12–30K |
| $200M (PNUT-scale day) | ~$100–250K | ~$100K | $50–125K |

### Allocation of every claimed fee

| Bucket | Share | Wallet | Use |
|---|---|---|---|
| **Cha Cha Pledge** | **50%** | Public "Pledge" wallet, published pre-launch | Donations to named animal-welfare organisations (candidates: Best Friends Animal Society, ASPCA, Coweta County Humane Society) and, if they accept, the Belote family's legal/advocacy costs. First donation within 7 days of launch, with the tx hash posted. |
| Growth | 30% | Treasury multisig (Squads, 2-of-3) | DexScreener Enhanced Token Info + boosts, KOL posts, meme bounties, TG stickers/animations, CEX listing fees if any |
| Ops | 20% | Treasury multisig | Team time, tooling, domains, design |

Rules:
- Claim fees on a fixed cadence (daily in week 1, weekly after) and post the claim tx each time.
- Monthly "Pledge Report" with every outgoing tx. Receipts beat promises.
- No burns are promised. Burns from the growth bucket are a tactical tool, decided and announced case by case.

---

## 4. Holder health targets

| Metric | Hour 1 | Day 1 | Day 7 |
|---|---|---|---|
| Launch wallet | ≤ 2% | ≤ 2% | ≤ 2% |
| Top-10 wallets (excluding pool) | < 20% | < 15% | < 12% |
| Holders | 300+ | 1,500+ | 5,000+ |
| Bubblemaps | No cluster > 5% | same | same |
| RugCheck | "Good" | same | same |

These numbers are what CEX listing desks and the big terminals' "safety" tabs look at. They are also what we publish on the site's **Proof** section.

---

## 5. Exchange ladder (what to expect, what to prepare)

1. **Day 0–2:** DEX only. DexScreener trending + Jupiter strict list (automatic once volume is there).
2. **Day 1–5:** Tier-2 CEXs (MEXC, LBank, Gate, Bitget) list hot pump.fun tokens unprompted once they trend and clear ~$10M market cap with real holders. Have the listing pack ready: 512px PNG logo, 200-word description, socials, CA, Solscan link, Pledge wallet.
3. **Day 5+:** Binance Futures / Bybit / OKX follow social volume (LunarCrush topic rank, X mentions) and sustained volume. This is the PNUT step-function. Nothing we do forces it; the only lever is sustained attention.

---

## 6. Proof links to publish on the site

- Solscan token page (supply, authorities)
- RugCheck.xyz report
- Bubblemaps
- DexScreener pair
- Launch wallet, Pledge wallet, Treasury multisig (all Solscan)
- pump.fun creator profile (fee claims are visible)

---

## 7. What we do not do

- No presale, no "whitelist", no OTC deals, no KOL token allocations (KOLs are paid in SOL from the growth bucket, disclosed).
- No tax tokens, no reflections, no "anti-whale" contract tricks (SPL on pump.fun can't do them anyway, and traders distrust them).
- No roadmap promises tied to market cap milestones. Phases are about the mission, not the chart.
