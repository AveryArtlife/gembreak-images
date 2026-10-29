# Codex runbook · rendering the Cha Cha Forever visuals with Higgsfield

You are Codex. Your job: turn `HIGGSFIELD-PROMPT-PACK.md` into files in this repo, in the right places, passing QA. Same pipeline as the GemBreak watch renders.

## Inputs
- Prompt pack: `prompts/HIGGSFIELD-PROMPT-PACK.md` (IDs S1–S4, P1–P4, B1–B2, M1–M16, K1–K16, V1–V4).
- Character reference: `brand/exports/cha-mark-1024x1024.png` (attach to every generation).
- Coin reference (V4 only): `brand/exports/cha-coin-1024x1024.png`.
- Palette: `brand/palette.json`.

## Output locations
| Group | Folder |
|---|---|
| S1–S4 | `site/assets/img/` (exact filenames in the pack; `S3` goes in `site/assets/img/wall/`) |
| P, B | `brand/renders/` |
| M | `brand/renders/memes/` |
| K | `brand/renders/stickers/` |
| V | `brand/renders/video/` |

Create folders as needed. Keep a `brand/renders/MANIFEST.csv` with: `id,filename,seed,model,prompt_hash,qa_pass,notes`.

## Procedure
1. **Pin the character.** Generate P1 four times with the reference image attached. Pick the one that best matches `docs/02-BRAND.md › The character` (fawn, black mask, one tilted gold halo, red collar, star tag). Record its seed. Reuse that seed and reference for every still.
2. **Batch order:** S1–S4 first (the site needs them), then P/B, then M, then K, then V.
3. For each entry: `MASTER STYLE + entry prompt`, negative prompt from section 0, aspect ratio from the size column. Generate 2 variations, keep the best, delete the rest.
4. **Post-processing**
   - S4 and all K stickers: remove background (key #00FF00 or use remove-bg), trim, pad 8%, and for stickers add a 6px white outline and downscale to 512×512, < 512 KB.
   - Memes: export at 1080×1080 PNG. Do **not** add captions; the content lead adds text from `docs/06-CONTENT-KIT.md`.
   - Video: H.264 MP4, 30fps, loop-checked (first and last frame near-identical), < 15 MB.
5. **QA** every file against section 6 of the pack. Anything failing gets regenerated, not "fixed enough".
6. Run `node scripts/export.mjs` (regenerates logo PNGs; harmless to re-run).
7. Open `site/index.html` locally (`npx serve site`) and confirm the story, pledge and wall images now appear in their slots.
8. Commit with message `Add Higgsfield renders: <ids>` and update `MANIFEST.csv`.

## Hard rules
- Never use real photos of Cha Cha or the Belote family as references or outputs.
- No text in generated images. No hospital or clinic names or logos anywhere.
- No sad/clinical imagery of the character (see pack section 6).
- Do not change filenames; the site and content kit depend on them.
