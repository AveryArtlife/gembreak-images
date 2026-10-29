# Higgsfield prompt pack · Cha Cha Forever ($CHA)

For Codex to run through Higgsfield (image + video). Read `CODEX-RUNBOOK.md` first. Every entry has: **ID · filename · size · prompt · negative · notes**. Filenames are load-bearing: the site (`site/index.html`, `site/wall.json`) and the content kit already reference them.

---

## 0. Master style (prepend to every image prompt)

```
MASTER STYLE: Cha Cha, a chubby fawn pug with a black mask and black folded ears, huge round glossy dark eyes, a small pink tongue tip, slightly worried forehead wrinkles, a red collar with a round gold star tag, and a GOLD HALO floating just above her head tilted about 12 degrees like it slipped. Stylised 3D character render, Pixar/DreamWorks quality, soft subsurface skin, short velvety fur, big-head proportions (head ≈ 45% of body), expressive and joyful. Lighting: warm key light from upper left, cool rim light, gentle gold bounce from the halo. Palette: pug fawn #E9C98F, mask black #1B1B1F, cha gold #F5B82E, heaven blue #9ED3FF, night navy #0B0F1A, cloud white #F8F7F2. Clean, premium, memecoin-ready. No text anywhere in the image.
```

**Negative (use on every image):**
```
text, letters, watermark, logo, signature, extra limbs, deformed eyes, two halos, realistic photo of a real dog, sad expression, tears, veterinary table, syringe, needle, cage, gravestone, blood, hospital signage, human faces, cropped head, blurry, low-res, muddy colours, grey halo, silver halo
```

**Character consistency:** attach `brand/exports/cha-mark-1024x1024.png` as the reference/character image on every generation (Higgsfield character / reference-image input, strength ~0.6–0.7). Keep the seed fixed per batch once a good Cha Cha appears; vary only the scene prompt.

**Aspect ratios used:** 1:1 (1024 or 2048), 16:9 (1920×1080 / 1600×900), 3:1 (3000×1000), 9:16 (1080×1920 video), 1.91:1 (1200×630).

---

## 1. Site slots (the page picks these up automatically)

| ID | Filename | Size | Prompt (after MASTER STYLE) |
|---|---|---|---|
| S1 | `site/assets/img/story-timeline.png` | 1600×900 | A gentle five-panel illustrated strip, left to right, same stylised 3D world, **no text**: (1) a small cosy house at dusk with a warm window, a pug silhouette in the doorway; (2) a glowing phone screen on a kitchen table showing a blurred happy pug photo, a hand reaching toward it; (3) Cha Cha standing proud and healthy on a lawn in sunshine, halo bright; (4) the same lawn now empty under grey-blue sky, only the halo floating; (5) Cha Cha dancing on a cloud at golden hour, halo back on, confetti of gold stars. Soft vignette between panels, consistent camera height, cinematic, emotional but never graphic. |
| S2 | `site/assets/img/pledge-card.png` | 1600×900 | Cha Cha sitting on a stack of three oversized gold coins (plain coins, no text) beside a small golden donation box with a paw-print slot; little paper hearts float up from the box; soft clouds behind, heaven-blue to navy gradient; a tiny gavel rests on the top coin. Composition leaves the left third empty for overlay copy. |
| S3 | `site/assets/img/wall/chacha.png` | 800×800 | Memorial portrait: Cha Cha head-and-shoulders, gentle smile, eyes bright, halo glowing, looking slightly up-left, soft cloud background in heaven blue, light gold particles. Circular-crop safe (keep the halo inside the inner 80%). |
| S4 | `site/assets/img/hero-chacha.png` | 2048×2048, transparent | Hero character: full-body Cha Cha mid cha-cha step, left front paw extended, head tilted, halo slipping, tongue out, confident. Transparent background (remove bg in post), 10% padding, no floor shadow. |

---

## 2. Social profile set

| ID | Filename | Size | Prompt |
|---|---|---|---|
| P1 | `brand/renders/pfp-01.png` | 1024×1024 | Close-up portrait of Cha Cha looking straight at camera, halo centred, navy radial background, gold rim light, tight crop (eyes on the upper third line). |
| P2 | `brand/renders/pfp-02-wink.png` | 1024×1024 | Same framing as P1, one eye winking, tongue out, halo tilted more. |
| P3 | `brand/renders/pfp-03-gavel.png` | 1024×1024 | Same framing, Cha Cha holding a tiny wooden gavel in her mouth like a stick, proud. |
| P4 | `brand/renders/pfp-04-clouds.png` | 1024×1024 | Same framing, background of fluffy cumulus in heaven blue, golden-hour light. |
| B1 | `brand/renders/banner-art.png` | 3000×1000 | Wide panorama: Cha Cha dancing on the left third on a cloud, the right two-thirds a calm navy-to-heaven-blue sky with drifting clouds and faint gold stars, space reserved for the wordmark. |
| B2 | `brand/renders/banner-pack.png` | 3000×1000 | Cha Cha leading a conga line of eight different stylised pets (dogs, cats, a rabbit, a parrot), each with its own small halo, dancing across clouds; joyful, confetti of gold stars. |

---

## 3. Meme templates (text-free; captions added in post from `docs/06-CONTENT-KIT.md`)

All 1080×1080 unless noted. Leave the top 18% and bottom 18% relatively clean for caption bars.

| ID | Filename | Prompt | Pairs with caption |
|---|---|---|---|
| M1 | `memes/m01-clap-paws.png` | Cha Cha standing on hind legs clapping her front paws, big grin, disco-ball reflections, dance floor of clouds. | Everybody clap your paws |
| M2 | `memes/m02-slide-left.png` | Cha Cha sliding to the left on a glossy floor, motion blur on the paws, halo trailing gold light. | Slide to the left |
| M3 | `memes/m03-slide-right.png` | Mirror of M2 sliding right. | Slide to the right |
| M4 | `memes/m04-real-smooth.png` | Cha Cha in sunglasses, leaning back, finger-guns pose with paws, smooth jazz lighting, purple-navy backdrop. | Cha Cha real smooth |
| M5 | `memes/m05-one-hop.png` | Cha Cha caught mid single hop, all four paws off a cloud, ears flapping up, halo one beat behind. | One hop this time |
| M6 | `memes/m06-reverse.png` | Cha Cha moonwalking backwards on a cloud, cheeky over-the-shoulder look. | Reverse, reverse |
| M7 | `memes/m07-how-low.png` | Cha Cha doing a limbo under a gold bar, belly nearly on the floor, straining happily. | How low can you go |
| M8 | `memes/m08-courthouse.png` | Cha Cha sitting upright on the steps of a classical courthouse at dawn, tiny gavel beside her, determined face, halo bright. | Justice for Cha Cha |
| M9 | `memes/m09-diamond-paws.png` | Cha Cha hugging a huge faceted diamond with both paws, eyes sparkling. | Diamond paws |
| M10 | `memes/m10-forever-wall.png` | A warm golden wall of framed pet portraits stretching into the distance, Cha Cha placing the first frame, each portrait has a small halo. | Add yours to the wall |
| M11 | `memes/m11-receipt.png` | Cha Cha proudly holding up a long blank paper receipt that curls to the floor, standing next to a gold donation box. | Receipts, not promises |
| M12 | `memes/m12-gm.png` | Cha Cha in a tiny bed on a cloud at sunrise, stretching with a yawn, halo on the nightstand next to a coffee cup. | gm |
| M13 | `memes/m13-crooked-halo.png` | Extreme close-up of Cha Cha's face with the halo hanging off one ear, unbothered. | Halo slightly crooked. Still forever. |
| M14 | `memes/m14-stare.png` | Cha Cha staring deadpan into the camera, flat lighting, white background (classic reaction-image framing). | (reaction template) |
| M15 | `memes/m15-chart.png` | Cha Cha riding a glowing gold line that rises left to right across a navy sky like a rollercoaster, arms up. | (price posts) |
| M16 | `memes/m16-pack.png` | Cha Cha at the front of a huge crowd of stylised pets all wearing small halos, stadium lighting, celebratory. | Join the pack |

---

## 4. Telegram sticker pack (16)

512×512, **transparent background**, 6px white outline around the character (add in post), single clean pose each. Prompt pattern: `[MASTER STYLE] + "sticker pose: {pose}, full body, centred, plain flat background #00FF00 for keying, no shadow"`.

| ID | Filename | Pose |
|---|---|---|
| K1 | `stickers/k01-wave.png` | waving one paw, smiling |
| K2 | `stickers/k02-clap.png` | clapping paws, eyes closed with joy |
| K3 | `stickers/k03-slide-l.png` | sliding left, arrow-like body lean |
| K4 | `stickers/k04-slide-r.png` | sliding right |
| K5 | `stickers/k05-hop.png` | mid-hop, ears up |
| K6 | `stickers/k06-gavel.png` | banging a tiny gavel, serious face |
| K7 | `stickers/k07-diamond.png` | hugging a diamond |
| K8 | `stickers/k08-laugh-cry.png` | laughing with tears of joy |
| K9 | `stickers/k09-shh.png` | paw over mouth, "shh" |
| K10 | `stickers/k10-point-up.png` | pointing upward with one paw, excited |
| K11 | `stickers/k11-sleep.png` | asleep curled up, halo as a nightlight |
| K12 | `stickers/k12-heart.png` | holding a big red heart |
| K13 | `stickers/k13-salute.png` | saluting, chest out |
| K14 | `stickers/k14-wink.png` | winking with a thumbs-up paw |
| K15 | `stickers/k15-confetti.png` | throwing gold confetti |
| K16 | `stickers/k16-gm.png` | holding a coffee mug, sleepy smile |

---

## 5. Video (Higgsfield video, 5–8s seamless loops)

| ID | Filename | Size | Prompt |
|---|---|---|---|
| V1 | `video/v01-cha-cha-slide.mp4` | 1080×1920 | Cha Cha does the Cha Cha Slide on a cloud dance floor: slide left two steps, slide right two steps, one hop, turn. Camera static, waist-up framing, disco-ball sparkles, halo bobbing on beat (120 BPM), loop-safe start and end pose. Stylised 3D, Pixar quality. No text. |
| V2 | `video/v02-idle-halo.mp4` | 1080×1080 | Cha Cha sits and breathes gently, blinks twice, halo floats up and down 2cm, gold particles drift. Seamless 6s loop for the site hero and TG pin. |
| V3 | `video/v03-forever-wall.mp4` | 1080×1920 | Slow vertical dolly along a golden wall of framed pet portraits with halos, Cha Cha's frame in the centre glows as the camera passes, warm bokeh. 8s. |
| V4 | `video/v04-coin-spin.mp4` | 1080×1080 | The $CHA coin (use `brand/exports/cha-coin-1024x1024.png` as reference) spins slowly on a navy background with gold rim light, 4s perfect loop. |

---

## 6. QA rules for every render (Codex checks before saving)

1. Fawn pug, black mask, black ears, red collar, gold star tag, **one gold halo**, tilted. Reject anything else.
2. No text, letters or logos baked in. Captions and wordmark are added in post.
3. No sad or clinical imagery (syringe, table, cage, grave). The story is sad; the character is not.
4. Not a photo of a real dog. Never use the family's photos as reference.
5. Eyes symmetrical and glossy; paws count = 4; halo not grey.
6. Correct size and filename; PNG for stills (transparent where specified), MP4 H.264 for video.
7. Stickers: background keyed out cleanly, white outline added, under 512 KB (Telegram limit).
