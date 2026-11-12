# GemBreak Watch Images

Transparent PNG cutouts of every watch in the GemBreak mystery packs — no background, ready to composite on the site.

## Structure
- `watches-only/<SKU>.png` — 3,344 transparent, metadata-sanitized cutouts keyed by SKU.
- `product-shots/<SKU>/main.jpg` — a 1,200 × 1,200 product image for every active catalog SKU. Existing compliant supplemental gallery images are retained where available.
- `product-shots/manifest.json` — product-image coverage by SKU.
- `product-shots/source-manifest.json` — provenance for every generated product main.
- `audit/GemBreak_Final_Image_Audit.xlsx` — row-by-row reconciliation and QA results for the final inventory.
- `scripts/sync-to-blob.mjs` — optional helper to mirror images to a Vercel Blob CDN.

## Final image QA

- Active catalog image pairs: **3,344 / 3,344**
- Google Sheet `Master Inventory` rows reconciled by exact SKU: **1,555 / 1,555**
- Transparent PNG cutouts: **3,344 / 3,344**
- Product-main JPGs: **3,344 / 3,344**
- Product-main dimensions: **1,200 × 1,200** for every SKU
- Google Sheet identity failures: **0**
- Google Sheet non-watch titles: **0**
- Active catalog white-background failures: **0**

## Integrating with the pack data
The **"GemBreak Final Pack List"** Google Sheet is the source of truth for packs, odds, values, and distributors. Every watch row carries:
- `SKU` — the join key
- `Image URL` — direct link to its cutout

Image path pattern: `watches-only/<SKU>.png`
Raw URL: `https://raw.githubusercontent.com/AveryArtlife/gembreak-images/main/watches-only/<SKU>.png`
(Raw URLs resolve only while this repo is **public**, or swap in Vercel Blob CDN URLs via the script.)

## Pricing / odds model
Packs priced as **Price = EV × 1.10** (~91% payout). Odds are a single global ladder by market value — the most expensive watch (RM 11-03, $330K) is the rarest pull site-wide.
