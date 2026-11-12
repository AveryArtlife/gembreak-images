# 02 · Signal engine: detecting a story before the copycats do

## What we are detecting
A **memeable story** = a named character (usually an animal), an emotional hook (injustice, absurdity, joy), and attention that is accelerating across more than one platform. The engine's job is to put a scored candidate in front of a human inside 10 minutes of the first cross-platform spike, with the names/tickers already checked.

## Sources, fastest first

| Lag | Source | What it gives | Access | Status |
|---|---|---|---|---|
| **seconds** | **pump.fun new-token stream** (PumpPortal `wss://pumpportal.fun/api/data`, `subscribeNewToken`; Moralis/Bitquery pump.fun APIs as alternatives) | Every new token's name/symbol/creator. When 5+ coins named after the same thing appear inside an hour, the spray deployers have voted: the story is memeable and nobody has produced it. | PumpPortal (free stream; 0.5% fee only on trades through them) | Phase 1, day 3 |
| minutes | **DexScreener search** (public API) | Same copycat signal once pairs are indexed; plus exact-symbol conflict check; plus the paid-profile and boost feeds (what competitors pay for) | Free, no key | **Built** (`signals/sources/dexscreener.py`) |
| minutes | **X keyword search + trends** | Mentions per 15 min, engagement velocity, trend rank deltas | Apify `xquik/x-tweet-scraper` ($0.15/1k, `withinTime: "15m"`, `sinceId` cursor), `xquik/x-trends-scraper` ($0.15/1k) | Config entry ready |
| minutes | **TikTok keyword / sound / trending** | Plays, shares, comments by `uploadedAt`; sound spread curve | Apify `apidojo/tiktok-scraper` ($0.30/1k, `sortType: DATE_POSTED`), `clockworks/tiktok-sound-scraper` ($5/1k), `novi/fast-tiktok-api` (`type: TREND`, ~$0.40/1k) | Config entry ready |
| minutes | **Instagram post tracking + keyword** | Likes/comments/plays over time on the 3–5 posts that carry the story (Complex, People…), keyword/hashtag search | Apify `apify/instagram-scraper` ($2.70/1k, poll the same URLs every 10 min), `apidojo/instagram-scraper-api` ($0.50/1k + $0.015/tag query) | Config entry ready |
| minutes | **Reddit rising / keyword, last hour** | Score and comment velocity | Apify `automation-lab/reddit-scraper` ($1.15/1k, Standby endpoint < 10 s) — Reddit blocks server-side JSON (403 from here) | Config entry ready |
| 5–15 min | **Google Trends "Trending now"** | New trends with approx traffic and attached headlines, 4 geos | Public RSS (10 newest per geo) **Built**; Apify `data_xplorer/google-trends-trending-now` (200–500 trends, ~$0.07/run) for depth; `data_xplorer/google-trends-fast-scraper` for minute-level interest on a keyword | **Built** (RSS) |
| 15–60 min | **News velocity** | Articles/hour and distinct domains mentioning the phrase | GDELT DOC API (free, 15-min updates, one call then window locally) **Built**; Apify `lhotanova/google-news-scraper` ($2/1k, `openEndedDateRange: "1h"`) for Google News | **Built** (GDELT) |
| 15–60 min | **Google Alerts RSS** | Standing watchlist ("dog euthanized", "zoo escape", "justice for", "seized pet") | Free; create alerts → RSS → `config.json` | **Built** |
| 30–60 min | **YouTube Shorts search** | Views on last-hour uploads | Apify `apidojo/youtube-scraper` ($0.50/1k, `uploadDate: "l"`) | Optional |
| hours | **LunarCrush** topic time series | Creators/mentions/engagement once a topic exists | API plan | Stage 2+ KPI, not detection |
| hours | Facebook keyword | Reactions/shares | Apify `scraper_one/facebook-posts-search` ($5/1k) | Optional |

## Scoring (prototype weights, in `signals/score.py`)

| Signal | Max | Logic |
|---|---|---|
| Copycat launches (DexScreener now, pump.fun stream in Phase 1) | 30 | `10·log2(1+n_6h)` + 5 if their 24h volume > $50K. **−25 if a produced competitor is already live** (> $250K mcap with real liquidity): you are late, pick a different angle or pass. |
| News velocity (GDELT) | 20 | `4·log2(1+n_24h)` + 6 if the last 3h hold ≥ ¼ of the 24h count + 4 if anything in the last hour |
| Google Trends | 15 | 5 + `2·log2(1 + traffic/100)` if the phrase is on a trending list |
| Social engagement velocity (Apify) | 20 | engagement last 6h vs previous 6h, log-scaled |
| Memeability text | 15 | character word (+6), injustice word (+6), fun word (+3) |
| **No-go** | hard 0 | any no-go word (human death, children, terror, disasters with victims, abuse…) |

Thresholds: watch 40 · candidate 60 (card to the ops channel) · launch 75 (pre-fill the kit). Recalibrate weekly from post-mortems; the prototype weights are a guess calibrated on one story.

Live test (2026-10-29, three days after the Cha Cha story broke, after 15 copycats had already launched and died): the engine scores it in the 30s with the news window closed and no social configured, exactly the "too late" verdict a human reaches by hand. Run it on day one with the pump.fun stream and social velocity and the copycat burst alone would have put it over 60.

## The no-go list (also in `05-LEGAL-LINES.md`)
Human deaths, minors, terrorism, disasters with victims, sexual content, active criminal cases against private individuals, medical tragedies involving people. Animals, absurd news, sports and celebrity moments with the person's participation, product fails, "guy does thing" internet moments: yes.

## Latency budget
| Step | Target |
|---|---|
| New pump.fun token stream → copycat burst alert | < 1 min |
| Trends/X/TikTok poll cycle | 5 min (10 min for IG/YouTube/News, hourly for Trends-keyword/Facebook) |
| Candidate card in the ops channel | ≤ 10 min from first spike |
| Human approval | ≤ 5 min |

## Apify cost (from the catalogue, 10 keywords)
Polling everything every 10 min: ≈ $2.5K/month realistic (≈ $5.2K worst case). **Tiered cadence** (10-min for X, Reddit, TikTok, Trends-now; 30-min for IG, YouTube, News; hourly for Trends-keyword and Facebook): **≈ $1,700/month** plus the Apify Starter plan ($39/mo, required for the `apidojo` actors). Per-query fees dominate at low item counts, so batch keywords into one run per source wherever the actor accepts arrays.

## Running the Apify sources
- Create one **Task** per source with the input template; one **Schedule** (`*/10 * * * *`) can hold up to 10 tasks.
- Attach `ACTOR.RUN.SUCCEEDED` webhooks → ingest endpoint reads `GET /v2/datasets/{id}/items?clean=true&format=json`. For small runs call `run-sync-get-dataset-items` directly from the scheduler (what `signals/sources/apify.py` does).
- Key every item by platform post id; store `(poll_ts, likes, comments, views, shares)`; velocity = Δ/Δt between polls; mentions/hour = new ids with `createdAt` inside the window.
- Use each actor's delta filter so polls return only new items (`withinTime`, `sinceId`, `onlyPostsNewerThan`, `timeFilter: hour`, `openEndedDateRange: "1h"`, `uploadDate: "l"`, `dateRange: YESTERDAY`).

### Example inputs (copy into `signals/config.json › apify.actors`, `{q}` is the story phrase)
```json
{"actor": "xquik/x-tweet-scraper", "input": {"searchTerms": ["\"{q}\" lang:en -filter:nativeretweets"], "queryType": "Latest", "maxItems": 200, "time": {"withinTime": "6h"}}, "likes_key": "likeCount", "comments_key": "replyCount", "ts_key": "createdAt"}
{"actor": "apidojo/tiktok-scraper", "input": {"keywords": ["{q}"], "sortType": "DATE_POSTED", "dateRange": "YESTERDAY", "maxItems": 100}, "likes_key": "likes", "comments_key": "comments", "ts_key": "uploadedAtFormatted"}
{"actor": "apidojo/instagram-scraper-api", "input": {"keywords": ["{q}"], "getReels": true, "maxItems": 100}, "likes_key": "likeCount", "comments_key": "commentCount", "ts_key": "createdAt"}
{"actor": "automation-lab/reddit-scraper", "input": {"searchQuery": "{q}", "sort": "new", "timeFilter": "day", "maxPostsPerSource": 50}, "likes_key": "score", "comments_key": "numComments", "ts_key": "createdAt"}
{"actor": "lhotanova/google-news-scraper", "input": {"query": "\"{q}\"", "language": "US:en", "openEndedDateRange": "1d", "maxItems": 50, "fetchArticleDetails": false}, "likes_key": "_", "comments_key": "_", "ts_key": "publishedAt"}
```
Other catalogued actors: `apify/instagram-hashtag-scraper` ($2.60/1k), `clockworks/tiktok-scraper` ($3.70/1k + filters), `apidojo/tweet-scraper` ($0.40/1k, min 50/query), `harshmaur/reddit-scraper` ($2/1k), `data_xplorer/google-news-scraper-fast` ($4/1k, batched keywords), `delicious_zebu/youtube-video-scraper-by-keyword` ($1.20/1k, Shorts), `apify/facebook-posts-scraper` ($5/1k, pages only).

## What the prototype does today (`signals/`)
`story "<phrase>" --context "<words>"` scores one story; `trending` scores every Google-Trends item after a cheap text prefilter; `watch` loops; `conflicts <TICKER>` checks DexScreener. Stdlib only, no keys needed until Apify is added.
