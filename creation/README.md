# Creation Watches pack images

3 hi-res images per watch (`1`, `2`, `3` — .jpg or .webp), self-hosted from Creation Watches' CDN.

- Folder name = `creation_id` (matches the `CreationID` column in the GemBreak sheet's CW pack tabs / `CW Master`).
- `manifest.csv` maps each id → brand, name, cost, retail, which packs it appears in, and its image files.
- 107 of 130 pack watches have images. The 23 gaps are Eastern-sourced classic Casios (F-91W, some AE-1200WH variants) not carried on Creation's CDN.

Join: `sheet.CreationID` → `creation/<id>/1.jpg`
