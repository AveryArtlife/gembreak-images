# GemBreak Watch Images

Transparent PNG cutouts of every watch in the GemBreak mystery packs — no background, ready to composite on the site.

## Structure
- `watches-only/<SKU>.png` — 1,746 transparent, metadata-sanitized cutouts keyed by the final inventory SKU.
- `product-shots/<SKU>/main.jpg` — a 1,200 × 1,200 product image for every final inventory SKU. Existing supplemental `angle-*.jpg` and `box.jpg` images are retained where available.
- `product-shots/manifest.json` — product-image coverage by SKU.
- `product-shots/source-manifest.json` — provenance for every generated product main.
- `audit/GemBreak_Final_Image_Audit.xlsx` — row-by-row reconciliation and QA results for the final inventory.
- `scripts/sync-to-blob.mjs` — optional helper to mirror images to a Vercel Blob CDN.

## Final image QA

- Inventory rows reconciled: **1,746 / 1,746**
- Transparent PNG cutouts: **1,746 / 1,746**
- PNG files with ancillary metadata removed: **1,746 / 1,746**
- Product-main JPGs: **1,746 / 1,746**
- Product-main dimensions: **1,200 × 1,200** for every SKU
- Remaining exact-pixel duplicate groups: **6**, all documented legitimate model/regional duplicates in the audit workbook

## Integrating with the pack data
The **"GemBreak Final Pack List"** Google Sheet is the source of truth for packs, odds, values, and distributors. Every watch row carries:
- `SKU` — the join key
- `Image URL` — direct link to its cutout

Image path pattern: `watches-only/<SKU>.png`
Raw URL: `https://raw.githubusercontent.com/AveryArtlife/gembreak-images/main/watches-only/<SKU>.png`
(Raw URLs resolve only while this repo is **public**, or swap in Vercel Blob CDN URLs via the script.)

## Pricing / odds model
Packs priced as **Price = EV × 1.10** (~91% payout). Odds are a single global ladder by market value — the most expensive watch (RM 11-03, $330K) is the rarest pull site-wide.
