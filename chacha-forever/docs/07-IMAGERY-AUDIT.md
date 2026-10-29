# 07 · Imagery audit: real photo vs cartoon for animal-story coins

**Question:** do coins built on real animals (and real viral moments) perform better with a real photo or a cartoon as the token image? And what should $CHA do?

**Method (2026-10-29):** pulled the token image and all-time-high data from CoinGecko for 29 memecoins, hand-labelled each token image as *photo* or *cartoon* and each subject as *real* or *fictional*, then compared. ATH market cap is estimated as ATH price × current circulating supply (CoinGecko does not expose historical market cap on the free tier), so treat the column as order-of-magnitude. Three rows (Michi, Fred, Hawk Tuah) resolved to the wrong or a relaunched token on CoinGecko and were replaced with figures from 2024 press coverage, marked "(press)". Token images were checked by eye; the contact sheet is `docs/data/token-image-contact-sheet.jpg` and the raw dump is `docs/data/coingecko-comparables-2026-10-29.json`.

## The table

| Coin | Subject | Token image | Est. ATH market cap | ATH date | Now | Note |
|---|---|---|---|---|---|---|
| Dogecoin DOGE | real dog (Kabosu) | photo | $114.5B | 2021-05-07 | $12.2B | the original meme photo, on a coin |
| Shiba Inu SHIB | fictional Shiba | cartoon | $50.8B | 2021-10-27 | $2.9B |  |
| Pepe | fictional character | cartoon | $11.8B | 2024-12-09 | $2.1B |  |
| Bonk | fictional Shiba | cartoon | $5.1B | 2024-11-19 | $266M |  |
| dogwifhat WIF | real dog (Achi) | photo | $4.8B | 2024-03-31 | $177M | the meme photo itself |
| Pudgy Penguins | NFT IP | cartoon | $4.3B | 2024-12-17 | $476M |  |
| Floki | named after a real dog, drawn | cartoon | $3.3B | 2024-06-04 | $224M |  |
| ai16z | fictional | cartoon (anime) | $2.7B | 2025-01-01 | $0M |  |
| Fartcoin | no subject | text | $2.5B | 2025-01-19 | $127M |  |
| Peanut the Squirrel PNUT | real squirrel, news story | cartoon of the iconic photo | $2.4B | 2024-11-13 | $41M | cowboy-hat photo redrawn as a character |
| Brett | fictional character | cartoon | $2.3B | 2024-12-01 | $45M |  |
| Popcat | real cat (Oatmeal) | photo | $2.0B | 2024-11-17 | $41M | the meme frame itself |
| Goatseus Maximus | no subject | ascii | $1.3B | 2024-11-17 | $14M |  |
| Neiro | real dog (Kabosu successor) | cartoon on a coin | $1.3B | 2024-11-12 | $28M | a rival Neiro token used the real photo; both ran |
| Baby Doge | fictional | cartoon | $1.2B | 2024-12-09 | $63M |  |
| MEW | fictional cat | cartoon | $1.1B | 2024-11-17 | $38M |  |
| GigaChad | real person (meme) | photo | $914M | 2025-01-03 | $18M |  |
| Moo Deng | real hippo, viral clips | cartoon of the iconic pose | $674M | 2024-11-15 | $36M | the screaming-hippo pose, illustrated |
| Chill Guy | fictional character | cartoon | $657M | 2024-11-27 | $9M | the artwork is the meme |
| Ponke | fictional | cartoon | $465M | 2024-11-18 | $10M |  |
| Wen | fictional cat | cartoon | $371M | 2024-03-27 | $4M |  |
| Luce | official mascot (figure) | photo of the mascot | $319M | 2024-11-13 | $0M |  |
| Maneki | fictional | cartoon | $244M | 2024-04-25 | $2M |  |
| Mother Iggy | real person (Iggy Azalea) | photo | $223M | 2024-06-06 | $0M | celebrity launch |
| Smoking Chicken Fish | real photo meme | photo | $145M | 2024-10-14 | $0M |  |
| Hoppy | fictional (Pepe spin-off) | cartoon | $142M | 2024-10-31 | $1M |  |
| Hawk Tuah | real person, viral clip | cartoon | ~$490M FDV (press) | 2024-12-04 | — | estimate from circulating supply is unreliable here; collapsed within hours amid insider-dump claims |
| Michi | real cat | photo | ~$300M (press) | 2024 | — | CoinGecko search returned a different 2026 "michi"; figure from 2024 coverage |
| Fred the Raccoon | real raccoon, news story | photo (stylised glow) | ~$100M (press) | 2024-11 | — | CoinGecko id resolved to a 2026 relaunch; the Nov 2024 token peaked near $100M and faded within days |

## What the data actually says

1. **Among real-subject coins, both formats have produced billion-dollar outcomes.** Photo: DOGE (Kabosu), WIF, POPCAT. Cartoon-of-the-real-thing: PNUT, MOODENG, Neiro. There is no clean "photos win" or "cartoons win".
2. **What separates the winners from the also-rans is whether the token image *is the image people already saw*.** WIF, POPCAT and DOGE are literally the meme frame. PNUT's cartoon reproduces the cowboy-hat photo that every news story ran. MOODENG's cartoon is the screaming-hippo pose from the viral clips. Fred the Raccoon used a nice photo that nobody recognised, launched the same week as PNUT, and never broke out.
3. **News-driven animal coins (the $CHA genre: PNUT, MOODENG, Fred, Neiro) skew cartoon at the top.** The likely reasons, in order of how much we believe them: a cartoon can be put on stickers, memes, merch and video without re-licensing someone else's photo; a cartoon gives the community a consistent character to remix; and a redrawn version of the famous photo keeps the recognition while sidestepping the owner's copyright.
4. **Photos carry the emotional and credibility load.** In every PNUT/MOODENG community the real photos and news clips circulated constantly, posted by holders, not by the team. The team owned the character; the crowd distributed the reality.
5. **Pure-fiction cartoons (PEPE, Brett, Chill Guy, MEW) are a different genre** and tell us nothing about Cha Cha: there is no "real" image to be faithful to.

## Recommendation for $CHA: both, with a clear split

| Surface | Use | Why |
|---|---|---|
| Token image (pump.fun, DexScreener, CEX listings) | **Cartoon that reproduces her leash photo**: black pug, pink braided collar, looking up, plus the halo | Recognition (it's the photo, drawn) + ownable + no third-party photo on the listing |
| X/TG avatar, stickers, memes, merch, video | Cartoon | Consistency, remixability, no licensing |
| Website "The real Cha Cha" section | Real photos **beside** the cartoon, credited | Proof it's a real dog and a real story; the "this is her" moment converts sceptics |
| Story thread, press, reply-guying news posts | Real photos via the outlets' own posts and Instagram embeds; screenshots of coverage | Credibility; lets the crowd do the distribution the way PNUT holders did |
| Memorial / Forever Wall entry for Cha Cha | Real photo if the family okays it, otherwise the portrait render (S3) | Respect |

Implemented: the character has been redrawn from her photos (all-black, pink braided collar, button ears); `site/index.html` has a "The real Cha Cha" section showing the two solo photos next to the character, with credits, behind `SHOW_REAL_PHOTOS`, and an Instagram embed of Complex's post on by default.

## Guardrails that come with using real photos

- Credit every photo to the family and the outlet it ran in. Never present them as ours.
- Never the photo with the family's son. He is a minor.
- Never meme, caption, or edit the real photos. Memes use the character.
- Hosted copies stay behind the flag until the family has okayed it or the project owner accepts the takedown risk; the Instagram embed is the default (Instagram serves the images, not us).
- If the family asks for removal, remove within the hour and say so publicly.

## Sources
- CoinGecko API (`/search`, `/coins/{id}`), 2026-10-29.
- Comparables timeline and peaks: see `01-RESEARCH.md › 2`.
