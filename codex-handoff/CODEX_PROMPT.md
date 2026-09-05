# Codex prompt — GemBreak dead-on watch renders

You produced the GemBreak `watches-only/` image set (transparent PNG cutouts, keyed by SKU,
in the `gembreak-images` repo). A rigorous two-pass independent image audit flagged 689 of
them. I need you to fix exactly these, listed in the attached `codex_deadon_render_list.csv`.

## The two problems to fix (see the `Issue` column)
1. **ANGLED** (677 watches) — the image is a three-quarter / "hero" angle. Produce a
   **dead-on, forward-facing** version: dial square to the camera, perfectly round (or
   square) dial — NOT an ellipse — 12 at top, crown to the right, case not rotated, no
   visible case flank. For most of these brands (Rado, Movado, TAG, Victorinox, Citizen
   Promaster, Orient/Seiko divers) **no dead-on photograph exists anywhere**, so this must
   be a render/recompose, not a re-source.
2. **WATERMARK** (52 watches) — a faint "CreationWatches" retailer overlay sits on the
   strap/bracelet below the case. Produce a **clean, watermark-free** version. (40 of
   these are also angled — fix both in one dead-on render.)

## Non-negotiable requirements (the bar the rest of the set already meets)
- Keep the **exact watch**: same dial color/texture, hands, indices, bezel, case metal,
  sub-dials, date window, and the **exact strap/bracelet material and color** shown in the
  reference image. Only the camera angle (and the watermark) changes — do not restyle the watch.
- **Strap or bracelet attached at BOTH lugs**, clearly visible on both sides, material
  identifiable.
- **No** watermark, retailer text, URL, badge, or overlay.
- Clean **single** watch, **transparent background**, sharp (not blurry/upscaled),
  metadata-stripped PNG.
- Output path: **`watches-only/<SKU>.png`**, filename = the exact `SKU` value (the join key).

## CSV columns
- `SKU` — join key + output filename.
- `Brand`, `Model_Reference` — confirm the exact model from the reference number.
- `MarketValue`, `Pack` — context only.
- `Issue` — `ANGLED-P1 (both auditors)` = do these first (highest confidence, 193);
  `ANGLED-P2 (one auditor)` = borderline tilt (484); `WATERMARK (needs clean)` = watermark.
  Some rows carry both tags.
- `CurrentImageURL_reference` — the current (angled/watermarked) image. **Use it as the
  visual reference** for the exact dial/bezel/hands/strap to reproduce dead-on and clean.
  (Repo is private — resolves only while you have access / it's public.)

## Order
Do **ANGLED-P1 (193)** first, then the watermark-only ones (quick clean-ups), then
ANGLED-P2. Deliver as you go so we can spot-check batches.

## Definition of done, per watch
A transparent PNG at `watches-only/<SKU>.png` that is: dead-on forward-facing, the same
exact watch as the reference, strap/bracelet visible at both lugs, no watermark, clean and
sharp on a transparent background.
