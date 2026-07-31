# IcyBox reveal images

Photorealistic "reveal" image per watch: the REAL product photo (dial/markings 100% authentic, never AI-altered) composited into an AI-generated open luxury presentation box with a rarity-colored glow (blue = value tier, purple = mid, gold = grail).

- File = `<SKU>.jpg`, where SKU matches the `SKU`/`CreationID` column in the GemBreak sheet's pack tabs. Grails are `G0`–`G7`.
- `manifest.csv` maps every pack SKU → brand, name, retail, packs, image, has_image.
- 179 of 197 done. The 18 without images are Eastern classic Casios (F-91W, A-158, AE-1200 variants) not hosted on the source CDN — pending a Casio image source.

Join: `sheet.SKU` → `icybox/<SKU>.jpg`
