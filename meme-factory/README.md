# Meme Factory · a legitimate, stage-gated, news-reactive memecoin launch system

Plan and prototype for launching produced memecoins within an hour of a story showing early virality, then scaling capital only when the market reacts. Built from the research and the `chacha-forever/` kit in this repo.

| Read | What |
|---|---|
| [`docs/01-OPERATOR-AUDIT.md`](docs/01-OPERATOR-AUDIT.md) | Who launches at scale, who makes money (bundling devs $579M, serial deployers, Clanker-style platforms), what venues reward, where the gap is |
| [`docs/02-SIGNAL-ENGINE.md`](docs/02-SIGNAL-ENGINE.md) | Detection: Apify actors, Google Trends/Alerts, GDELT, DexScreener copycat counter, pump.fun stream; scoring; no-go list; latency budget |
| [`docs/03-STAGE-GATED-LAUNCH-LADDER.md`](docs/03-STAGE-GATED-LAUNCH-LADDER.md) | The ladder: Watch → Launch → Confirm → Scale → Institutionalise, with triggers, budgets, kill rules, kit factory, portfolio math |
| [`docs/04-EARLY-TRACTION-TOOLS.md`](docs/04-EARLY-TRACTION-TOOLS.md) | Ranked tools for hour 0–1, 1–6, day 1–7; market making vs. wash trading; the honest $5K hour-one budget |
| [`docs/05-LEGAL-LINES.md`](docs/05-LEGAL-LINES.md) | Red / amber / green with the DOJ and SEC cases that define the lines |
| [`docs/06-PSEUDONYMOUS-OPS.md`](docs/06-PSEUDONYMOUS-OPS.md) | Domains, handles, payments, hosting, wallet hygiene; what still exposes you |
| [`docs/07-BUILD-PLAN.md`](docs/07-BUILD-PLAN.md) | Two-week semi-automated MVP, then automation and portfolio; stack, team, costs, risks |
| [`signals/`](signals/) | Working prototype: `python3 signals/run.py story "cha cha pug"` · `trending` · `watch` · `conflicts CHA` |

## Signal engine quick start
```bash
cd meme-factory/signals
python3 run.py story "cha cha pug"     # score one story from DexScreener copycats + GDELT news + Google Trends
python3 run.py trending                 # score everything on Google Trends 'trending now' (US/GB/CA/AU)
python3 run.py watch                    # loop every 5 min, print candidates above threshold
python3 run.py conflicts CHA            # exact-symbol conflicts before picking a ticker
export APIFY_TOKEN=...                  # then fill config.json › apify.actors from docs/02 to add social velocity
```
No third-party dependencies. GDELT and Google Trends are public; Reddit and pump.fun's own API block server-side calls, which is what Apify and PumpPortal are for.
