# 05 · Proposed structure: team, wallets, tools, repo

## Team (5 seats, can be 3 people)

| Seat | Owns | Day-of shift |
|---|---|---|
| **Launcher** | The launch wallet, pump.fun creation, fee claims, the Pledge transfers. Only person who touches keys. | Hour 0–4 |
| **Community lead** | Telegram, X replies, voice chats, mod roster, scam-defence pins. | Hours 0–12, then rotating |
| **Content lead** | Meme queue, TikTok cuts, story graphics, site updates (Forever Wall), Codex → Higgsfield render runs. | Daily |
| **Outreach lead** | KOL list, reporter follow-ups, animal-org contact, CEX listing packs. | Daily |
| **Pledge liaison** | Receives fees' 50%, executes donations, writes the monthly Pledge Report, the single point of contact for the family (once, politely). | Weekly |

Nobody holds two of: launch wallet, treasury multisig quorum, Pledge wallet.

---

## Wallets

| Wallet | Type | Published? | Purpose |
|---|---|---|---|
| Launch wallet | Hot (Phantom/Backpack), fresh, CEX-funded | Yes, pre-launch | Token creation, creation buy, fee claims |
| Pledge wallet | Hot, fresh | Yes, pre-launch | Receives 50% of every fee claim; outgoing only to named orgs |
| Treasury | Squads multisig 2-of-3 | Yes | Growth (30%) + ops (20%) |
| Mod tip jar | Optional | No | Small SOL for mods |

Key hygiene: hardware wallet for the multisig signers; launch wallet seed written once, stored offline; no browser extensions beyond the wallet on the launch machine.

---

## Tools

| Need | Tool |
|---|---|
| Launch | pump.fun (web), backup: pump.fun via Photon/Axiom "create" |
| Trading terminals to watch | Axiom, Photon, BullX, Trojan (TG bot) |
| Charts / discovery | DexScreener (Enhanced Token Info + Boosts), DexTools, Birdeye |
| Safety proofs | RugCheck.xyz, Bubblemaps, Solscan |
| Social analytics | LunarCrush (create the `$cha` topic), X analytics, TG Combot |
| Anti-spam | Rose bot (TG), Combot; X: restrict replies for the first 10 minutes on the CA tweet |
| Treasury | Squads multisig; Streamflow if we ever lock anything |
| Site hosting | Vercel (`site/`), DNS at the registrar, Cloudflare proxy optional |
| Image pipeline | Codex + Higgsfield (`prompts/`), Playwright for exports (`scripts/export.mjs`) |
| Payments to KOLs | SOL from treasury, logged in `ops/kol-ledger.csv` (create on day 0) |

---

## Surfaces checklist

| Surface | Handle / URL | Status |
|---|---|---|
| Website | chachaforever.com (+ .xyz, .io, .fun, chacha4ever.com, justiceforchacha.com redirects) | Unregistered as of 2026-10-29 |
| X | @chachaforever | To secure |
| Telegram | t.me/chachaforever | To secure |
| TikTok | @chachaforever | To secure |
| Instagram | @chachaforever | To secure |
| YouTube | @chachaforever (Shorts only) | To secure |
| pump.fun profile | "Cha Cha Forever" | Create with launch wallet |
| DexScreener | Enhanced Token Info | Submit at T+2min |
| CoinGecko / CMC | Listing forms | Submit day 1 (CG), day 2 (CMC) |

---

## Repo layout (this repo)

```
chacha-forever/
├── README.md                 ← start here
├── docs/
│   ├── 01-RESEARCH.md        ← virality research + competitive scan
│   ├── 02-BRAND.md           ← name, voice, visual identity, guardrails
│   ├── 03-TOKENOMICS.md      ← supply, fees, Pledge, proofs
│   ├── 04-LAUNCH-PLAN.md     ← T-24h → day 30 runbook
│   ├── 05-STRUCTURE.md       ← this file
│   └── 06-CONTENT-KIT.md     ← tweets, pins, FAQ, how-to-buy
├── brand/
│   ├── palette.json          ← design tokens
│   ├── logo/*.svg            ← source logos
│   └── exports/*.png         ← rendered PNGs (token image, avatar, banner, OG)
├── site/                     ← static landing page (Vercel / GitHub Pages)
│   ├── index.html
│   ├── styles.css
│   ├── app.js                ← CONTRACT_ADDRESS lives here
│   ├── assets/img/           ← Higgsfield renders go here
│   └── vercel.json
├── prompts/
│   ├── HIGGSFIELD-PROMPT-PACK.md ← every image, with prompt + size + filename
│   └── CODEX-RUNBOOK.md          ← how Codex runs the pack and QA's it
├── scripts/
│   └── export.mjs            ← SVG → PNG exports with Playwright
└── .github/workflows/pages.yml ← GitHub Pages deploy of site/ (once it is its own repo)
```

### Making it its own repository

This project was built inside `gembreak-images` on the branch `claude/chacha-forever` because the cloud session's GitHub app cannot create repositories. To split it out:

```bash
# 1. create an empty repo on GitHub named chacha-forever (private until launch)
# 2. from a clone of gembreak-images on the claude/chacha-forever branch:
git subtree split --prefix=chacha-forever -b chacha-forever-only
git push git@github.com:AveryArtlife/chacha-forever.git chacha-forever-only:main
# 3. point Vercel at the new repo, root directory = site/
```

---

## Decision log

| Date | Decision | Why |
|---|---|---|
| 2026-10-29 | Name: Cha Cha Forever, ticker CHA | Unique vs 6 dead "Justice for Cha Cha" launches; evergreen; ticker has zero DexScreener conflicts |
| 2026-10-29 | pump.fun over bonk.fun | Terminal reach + creator fee stream funds the Pledge |
| 2026-10-29 | Fair launch, 1.5–2% public creation buy, 30-day no-sell | Bubblemaps-clean, honest sniper defence |
| 2026-10-29 | 50/30/20 fee split with public Pledge wallet | Media angle + trust; receipts over promises |
| 2026-10-29 | Original character art only | Family's photos are theirs; also avoids a takedown risk |
