# 05 · Legal lines: what is illegal, what is grey, what is clean

Operating principle from the brief: follow the law, be aggressive inside it. This is not legal advice; get a crypto-literate lawyer on retainer before the first automated launch (budgeted in `07-BUILD-PLAN.md`). The point of this page is that the team never has to guess in the moment.

## Red: never, because it is a crime or a lawsuit, not a ToS problem

| Practice | Why it is red | Evidence |
|---|---|---|
| **Wash trading / "volume bots" / fake market making** | Market manipulation. The DOJ ran an undercover token (NexFundAI) in *Operation Token Mirrors* and charged 18 people and firms in Oct 2024. Gotbit's founder was sentenced in June 2025 with **$23M** forfeited; CLS Global was sentenced in Apr 2025 (probation, barred from US crypto markets, $428K); more Gotbit staff charged March 2026. The SEC filed civil cases alongside. | DOJ releases (justice.gov/usao-ma), Decrypt, CoinCentral |
| **Hidden supply sold into your own buyers** (bundled block-0 wallets, undisclosed insider wallets, "cabal" allocations) | Inducing purchases while concealing that you are the seller is securities/commodities fraud territory and wire fraud territory; it is also what every terminal flags. | Bitquery: 21% of launches bundled; terminals label it |
| **Paying promoters without disclosing it** where the token could be deemed a security | Securities Act §17(b) requires disclosing receipt **and amount**; no intent needed. Kardashian: $1.26M and a 3-year bar for an "#AD" that was ruled insufficient. Mayweather, Khaled, and six celebrities in the Justin Sun case settled. | SEC orders 2018–2023 |
| **Pump-and-dump coordination** (telling a community "hold" while you sell; scheduling dumps with KOLs) | Fraud. Also civil class actions. | Standard |
| **Impersonation** (claiming to be the family, the clinic, a news outlet, a charity) | Fraud, trademark, defamation. | — |
| **Defamation by assertion** (stating "the clinic killed a healthy dog" as fact) | The story is the family's allegation. Attribute it. | — |
| **Using a minor's image**, or anyone's likeness for endorsement without permission | Right of publicity; child-image rules; platform bans. | — |
| **Stories involving a human death, a child victim, terrorism, or a disaster with victims** | Beyond ethics, these invite IIED/defamation claims, platform-wide bans and payment-processor exits. Hard no-go list in `02-SIGNAL-ENGINE.md`. | — |

## Amber: legal, but it costs trust or breaks a platform's rules. Decide case by case, disclose by default.

| Practice | Risk | Our rule |
|---|---|---|
| Paid KOL / call-channel posts | §17(b) if "security"; FTC Endorsement Guides regardless | Every paid post carries "#ad · paid in SOL by the $X team" in the post itself. We keep a ledger. If a KOL refuses disclosure, no deal. |
| DexScreener Boosts, DEXTools fast-track, paid trending slots | Legal; traders now read an *early* boost as a rug signal | Hour 2+, never minute 1; buy ETI first (profile), boosts only once holders and volume are real |
| Public, disclosed creator buy (2–5%) at creation | Legal; mild stigma over 5% | Publish wallets before CA; lock terms in writing; never sell into a pump |
| Launching several coins on the same story | Legal; looks like spray if visible | One produced launch per story. If the first ticker is sniped, a second with a *different* name is fine, the first gets abandoned publicly |
| Multiple social accounts / aged accounts / automation via unofficial APIs | Platform ToS; ban risk (X pay-per-use API exists, Telegram punishes MTProto userbots that flood) | Official APIs only for posting; humans for community; no bought accounts; aged "persona" accounts are fine |
| Sniping other people's launches | Legal | Not our game, but the signal engine watches snipers as a virality oracle |
| Using the story subject's name/likeness: **animals** | Low risk (no publicity rights) | Fine; family photos only credited/embedded or with permission |
| Using a **person's** name/likeness (e.g., the Hawk Tuah pattern) | Right of publicity; higher ban risk | Only with the person's participation (then it is a "celebrity coin" with its own rules) |
| Market making by providing real liquidity (Meteora DLMM / Raydium CLMM positions, CEX MM agreements) | Legal if it is two-sided liquidity, not self-trading | Yes, documented in `04-EARLY-TRACTION-TOOLS.md`; written agreement; no "volume targets" |
| Charity pledges | Legal; becomes fraud if not honoured | Receipts on-chain, monthly report, named recipients |
| Pseudonymous team | Legal | See `06-PSEUDONYMOUS-OPS.md`. Pseudonymous to the public, never to regulators, exchanges or your own lawyer |

## Green: do all of it

Fair launch, public wallets, locked treasury, Enhanced Token Info, livestreams, organic raids, community meme contests paid in SOL, press outreach with receipts, merch with profits to the pledge, CEX listing applications, Jupiter/CoinGecko/CMC listings, DLMM liquidity, buybacks announced in advance, CTO hand-over when the team is done.

## Structure and tax

- Operate through an entity (a US LLC in a crypto-friendly state, or an offshore entity if counsel prefers) that owns the creator wallets and signs KOL and MM agreements. Pseudonymity is between you and the public, not you and the IRS.
- Creator fees and treasury sales are income. Keep the wallet map and the fee ledger clean from day one.
- One counsel review of: the pledge language, the KOL disclosure template, the MM agreement, and the no-go list. About $5–10K up front; it pays for itself the first time a reporter or an exchange asks.

## Sources
- DOJ, Gotbit sentencing: https://www.justice.gov/usao-ma/pr/cryptocurrency-financial-services-firm-gotbit-and-founder-sentenced-market-manipulation
- DOJ, CLS Global sentencing: https://www.justice.gov/usao-ma/pr/cryptocurrency-financial-services-firm-sentenced-cryptocurrency-wash-trading
- Decrypt on Gotbit: https://decrypt.co/325111/gotbit-founder-sentenced-prison-crypto-wash-trading
- SEC touting cases (Kardashian, Mayweather/Khaled, Sun): https://www.dglaw.com/sec-penalizes-kim-kardashian-over-1-million-for-paid-crypto-post/ , https://www.proskauer.com/blog/first-punch-floyd-mayweather-and-dj-khaled-settle-with-sec-over-unlawful-touting-of-icos , https://whitecase.com/insight-alert/sec-continues-prove-it-most-powerful-influencer-how-avoid-touting-charges
- Bitquery bundling stats: https://bitquery.io/investigations/pump-fun-snipers-bundles
