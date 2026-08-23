# GemBreak Product Shots

Real retail/factory product photography for each watch — an **additional** image layer
alongside the transparent cutouts in `watches-only/`. The cutouts remain the primary
composite-ready asset; these are richer shots (on-white studio photos, angles, and
box/full-set shots where available) for product detail pages, marketing, and reveals.

## Structure
- `product-shots/<SKU>/main.jpg` — best clean high-res shot of the watch
- `product-shots/<SKU>/box.jpg` — watch with its brand box / full set (where available)
- `product-shots/<SKU>/angle-N.jpg` — additional angles (dial, caseback, wrist)
- `product-shots/manifest.json` — every SKU and the files it has

## Coverage
- 192 of 197 watches have a verified product shot (every image checked against the exact reference).
- 27 have a box / full-set shot (grails + select Omega/Breitling/Tissot/Hamilton).
- 5 SKUs are intentionally omitted (no correct-variant image found yet): WW381, WW70, WW882, WW285, E79767927295 — use their `watches-only/` cutout for now.

## Sourcing
Grails: authorized-dealer full-set galleries (with box). Casios: CreationWatches catalog.
Swiss: the WatchWarehouse (distributor) listings and authorized dealers, matched to the exact reference.
