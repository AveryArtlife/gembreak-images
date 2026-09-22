# Search spec: pack-rip creators, nationwide

This is the prompt to run — by me in a session with Apify access, or by anyone
driving the actors by hand. It is written to be executed literally.

Run: `APIFY_TOKEN=... node scripts/find-ugc-creators.mjs`
The script implements this spec. This document is the reasoning behind it, and
the thing to edit when the targeting changes.

---

## Objective

Build a ranked, contactable list of US creators who can produce **pack rip and
pack rip reaction videos** for GemBreak on TikTok, Instagram Reels, and YouTube
Shorts — optimized for **cost per converted customer**, not for reach.

That distinction drives everything below. The most viral creator is usually the
wrong buy: their rate scales with followers while their purchase intent doesn't.
We want creators whose audience *buys*, at a rate we can run twenty of.

**Hard filters:** 5,000–500,000 followers. US-based. Posted within 30 days.

---

## What actually predicts conversion here

Rank on these, in this order. The script scores them; this is why.

1. **Comment rate** (comments ÷ views), weighted above like rate. Likes are
   reflexive; comments are the cheapest available proxy for intent. On unboxing
   content the comment section fills with "where'd you get that," which is a
   buying question.
2. **Format fit.** Has the creator already shot a reveal — unboxing, card break,
   mystery box, "what's inside"? A creator who has done it converts on the first
   take. A creator learning the format burns a pack getting there.
3. **Cost efficiency.** Estimated rate ÷ median views, expressed as cost per
   1k views. A 20k-follower creator pulling 80k views per post beats a
   300k-follower creator pulling 90k, at a fifth of the price.
4. **Consistency.** Posts per week over the last month. One viral fluke on a
   dormant account is not a channel.
5. **Category adjacency** — watches, jewelry, sneakers, cards, collectibles,
   hype/reseller, finance, crypto. Audience already primed for the product.
6. **Raw reach.** Last, and deliberately so.

## Disqualify

Cheap to check, expensive to miss:

- **Engagement anomalies** — like rate wildly out of band for follower count,
  or comments that are all emoji strings. Pods and bought followers.
- **Giveaway farms** — feed is mostly "tag 3 friends." That audience converts
  at zero.
- **Ad saturation** — every recent post is `#ad`. The audience has tuned out.
- **Kid-facing accounts.** GemBreak is 18+; wrong audience, and a compliance
  problem in paid.
- **No face, no voice.** Reaction is the product. A faceless montage account
  can't shoot this brief.
- **Non-US primary audience.** We can't ship them a pack.

## Search matrix

Cross format terms with niche terms. Broad on purpose — filtering happens after,
on real numbers, not on the query.

**Format:** pack rip, ripping packs, pack opening, unboxing, mystery box,
mystery pack, case break, box break, what's inside, blind box, first look

**Niche:** watch unboxing, watch collection, jewelry unboxing, iced out,
sneaker unboxing, card break, pokemon break, sports cards, collectibles haul,
grail, hype unboxing, reseller haul

**Reaction:** reacting to my pull, insane pull, best pull, worst pull,
pull reaction, opening reaction

**Hashtags:** #packrip #packopening #mysterybox #unboxing #watchtok #cardbreak
#boxbreak #hypebeast #grail #whatsinside

Cities are **tags, not filters** — NYC, Miami, LA, Atlanta, Dallas, Chicago,
Vegas, Houston, Phoenix, Philly. Useful for clustering shoots and for in-person
formats later; never a reason to exclude.

## Tiers

Different tiers get different offers, so the output separates them.

| Tier | Followers | Use |
|---|---|---|
| Nano | 5k–25k | Volume. Cheapest CPM, highest trust, run many in parallel. |
| Micro | 25k–100k | The core buy. Best conversion-per-dollar in this category. |
| Mid | 100k–500k | Selective. Only when reach multiple or comment rate is exceptional. |

Expect the winners to concentrate in nano and micro. If mid-tier dominates the
ranking, the scoring is over-weighting reach — check it.

## Output

Per platform and tier: handle, profile link, follower count, median views,
comment rate, estimated cost per 1k views, format-fit flag, category tags, last
post date, and two example video links.

Plus a combined CSV sorted by score, so the top of the file is the outreach
queue.

## Verification

Every row must come from an actual actor result. No handle, follower count, or
link may be inferred, reconstructed, or filled in from memory — a plausible-looking
dead profile costs more outreach time than an empty row. If a run returns
nothing for a query, the honest output is fewer rows and a note saying which
queries came back empty.
