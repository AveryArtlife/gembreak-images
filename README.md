# GemBreak Watch Images

Transparent PNG cutouts of every watch in the GemBreak mystery packs — no background, ready to composite on the site.

## Structure
- `watches-only/<SKU>.png` — the cutout for each watch, keyed by its SKU (197 watches, incl. the Richard Mille grail `RM1103.png`).
- `scripts/sync-to-blob.mjs` — optional helper to mirror images to a Vercel Blob CDN.

## Integrating with the pack data
The **"GemBreak Final Pack List"** Google Sheet is the source of truth for packs, odds, values, and distributors. Every watch row carries:
- `SKU` — the join key
- `Image URL` — direct link to its cutout

Image path pattern: `watches-only/<SKU>.png`
Raw URL: `https://raw.githubusercontent.com/AveryArtlife/gembreak-images/main/watches-only/<SKU>.png`
(Raw URLs resolve only while this repo is **public**, or swap in Vercel Blob CDN URLs via the script.)

## Pricing / odds model
Packs priced as **Price = EV × 1.10** (~91% payout). Odds are a single global ladder by market value — the most expensive watch (RM 11-03, $330K) is the rarest pull site-wide.
