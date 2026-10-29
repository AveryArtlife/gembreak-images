# Cha Cha Forever · $CHA

> The Georgia pug a vet clinic was paid to put down, secretly kept alive, then killed when her family found out. **Justice for Cha Cha. Forever on-chain.**

This repo is the complete launch kit for the $CHA memecoin: research, brand, tokenomics, launch runbook, website, logo system, and the Higgsfield prompt pack for every visual.

**Status:** pre-launch. No contract exists yet. Nothing here is live until `site/app.js › CONFIG.CONTRACT_ADDRESS` is filled.

## Start here

| Read | For |
|---|---|
| [`docs/01-RESEARCH.md`](docs/01-RESEARCH.md) | Why this can work: comparables (PNUT, MOODENG), base rates, the 11 virality rules, the competitive scan (6 dead "Justice for Cha Cha" launches), launchpad choice |
| [`docs/02-BRAND.md`](docs/02-BRAND.md) | The name decision (**Cha Cha Forever**, ticker **CHA**), voice, character, visual identity, guardrails |
| [`docs/03-TOKENOMICS.md`](docs/03-TOKENOMICS.md) | 1B supply, 100% fair launch, 0% team, public launch wallet, creator-fee split 50 / 30 / 20 (the Cha Cha Pledge) |
| [`docs/04-LAUNCH-PLAN.md`](docs/04-LAUNCH-PLAN.md) | T-24h checklist, the scripted first 60 minutes, amplifier targets, 30-day content engine |
| [`docs/05-STRUCTURE.md`](docs/05-STRUCTURE.md) | Team seats, wallets, tools, handles and domains to secure, how to split this folder into its own repo |
| [`docs/06-CONTENT-KIT.md`](docs/06-CONTENT-KIT.md) | Pinned tweet, story thread, TG pins, reply templates, FAQ, meme captions, TikTok scripts |
| [`docs/07-IMAGERY-AUDIT.md`](docs/07-IMAGERY-AUDIT.md) | Real photo vs cartoon across 29 memecoins, and why $CHA uses both: a cartoon drawn from her real photos as the token image, the real photos credited on the site |
| [`prompts/HIGGSFIELD-PROMPT-PACK.md`](prompts/HIGGSFIELD-PROMPT-PACK.md) + [`prompts/CODEX-RUNBOOK.md`](prompts/CODEX-RUNBOOK.md) | Every image and video, with prompts, sizes and filenames, and the procedure for Codex to render them |

## The brand in one glance

![Cha Cha Forever lockup](brand/exports/cha-lockup-1600x480.png)

Cha Cha is an **all-black pug** with a pink braided leash; the character is drawn from her press photos (`brand/reference/`, likeness only). Edit `brand/logo/cha-mark.svg`, then:

```bash
python3 scripts/build-logos.py   # rebuilds coin, avatar, lockup, banner, OG from the mark
node scripts/export.mjs          # SVG → PNG (needs Playwright + Chromium: npx playwright install chromium)
python3 scripts/inline-logos.py  # re-inlines the mark and coin into site/index.html
```

Rendered PNGs (token image 512/1024, avatar 400/800, X banner 1500×500, OG 1200×630, favicon) live in `brand/exports/`.

## The website

`site/` is a static page (no build step): `index.html`, `styles.css`, `app.js`, `wall.json`, self-hosted fonts.

```bash
npx serve site                   # local preview at http://localhost:3000
```

Deploy: import the repo in Vercel with **Root Directory = `site`**, or push to `main` and let `.github/workflows/pages.yml` publish to GitHub Pages (once this is its own repo).

At launch, edit `site/app.js`:
```js
CONTRACT_ADDRESS: '<pump.fun CA>',
PLEDGE_WALLET: '<address>', LAUNCH_WALLET: '<address>', TREASURY_MULTISIG: '<squads address>',
LINKS: { x, telegram, tiktok, instagram, wallForm }
```
Everything on the page (CA boxes, buy/chart/proof links, live DexScreener stats) keys off that one value. Add donations to `CONFIG.DONATIONS` and pets to `wall.json`.

Image slots the page fills automatically when Codex drops renders in: `site/assets/img/story-timeline.png`, `pledge-card.png`, `wall/chacha.png`.

Real photos: `site/assets/img/real/` holds two credited family photos as published by LADbible and UNILAD. They render only when `CONFIG.SHOW_REAL_PHOTOS` is `true` (see the README in that folder); the Instagram embed of Complex's post is on by default.

## Repo map

```
docs/        research · brand · tokenomics · launch plan · structure · content kit
brand/       palette.json · logo/*.svg · exports/*.png · renders/ (Higgsfield output)
site/        static landing page
prompts/     Higgsfield prompt pack + Codex runbook
scripts/     export.mjs (SVG → PNG)
```

## Guardrails (read before posting anything)

Not affiliated with Cha Cha's family or Senoia Animal Hospital. Real photos only credited, never memed, never the one with their son. No naming or targeting clinic staff. No promises of returns. Full list in `docs/02-BRAND.md`.
