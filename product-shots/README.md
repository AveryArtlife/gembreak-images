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
- All 1,746 watches in the final inventory have a `main.jpg`.
- 192 SKUs retain the original verified retail/factory gallery set; where an exact
  second gallery photograph was not yet available, `main.jpg` is derived from the
  matching transparent `watches-only/<SKU>.png` on a clean white studio canvas.
- Additional angles and box/full-set shots remain optional and are included only
  where an exact-reference source is available.
- `source-manifest.json` distinguishes legacy gallery photographs from clean
  cutout-derived coverage so the latter can be upgraded without ambiguity.

## Sourcing
Grails: authorized-dealer full-set galleries (with box). Casios: CreationWatches catalog.
Swiss: the WatchWarehouse (distributor) listings and authorized dealers, matched to the exact reference.

## Maintenance
Run `python3 scripts/build-product-mains.py` after adding inventory or replacing a
transparent cutout. It fills missing main images without overwriting existing
galleries, then regenerates both manifests. Use `--force` only when intentionally
rebuilding every main image from the transparent cutouts, or `--force-prefix CR`
to rebuild only one SKU family.
