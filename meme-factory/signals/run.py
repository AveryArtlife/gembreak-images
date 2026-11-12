#!/usr/bin/env python3
"""Signal engine CLI.
  python3 run.py story "cha cha" --context "pug euthanized vet clinic"   # core phrase + context words
  python3 run.py trending [--limit N]            # score the top-N Google Trends 'trending now' items (default 15) after a text prefilter
  python3 run.py watch                           # loop: trending + alerts every N minutes, print candidates ≥ threshold
  python3 run.py conflicts CHA                   # exact-symbol conflicts on DexScreener
Set APIFY_TOKEN and fill config.json › apify.actors to add social velocity."""
import sys, json, time, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sources import google_trends, gdelt, dexscreener, google_alerts
from score import score
CFG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")))
def social_for(q):
    acts = CFG["apify"].get("actors") or []
    if not acts or not os.environ.get(CFG["apify"]["token_env"]): return None
    from sources import apify
    agg = {"eng_6h": 0, "eng_prev_6h": 0}
    for a in acts:
        try:
            items = apify.run_sync(a["actor"], json.loads(json.dumps(a["input"]).replace("{q}", q)))
            v = apify.engagement_velocity(items, a.get("likes_key", "likesCount"), a.get("comments_key", "commentsCount"), a.get("ts_key", "timestamp"))
            agg["eng_6h"] += v["eng_6h"]; agg["eng_prev_6h"] += v["eng_prev_6h"]
        except Exception as e: print("apify", a.get("actor"), "failed:", e, file=sys.stderr)
    agg["ratio"] = agg["eng_6h"] / agg["eng_prev_6h"] if agg["eng_prev_6h"] else (float("inf") if agg["eng_6h"] else 0)
    return agg
def story(q, trends=None, extra_text="", prefilter=False):
    """q = the story's core phrase (what copycat tokens get named after, e.g. 'cha cha'); extra_text = context words for memeability."""
    if prefilter:  # cheap text gate before any network call (used by the trending scan)
        from score import text_score
        m, nogo = text_score(q + " " + extra_text, CFG["memeability"])
        if nogo or m == 0: return {"story": q, "score": 0, "notes": ["prefiltered: no character/injustice/fun words" if not nogo else "NO-GO"], "copycats": {"n_last_6h": 0, "n_launches": 0, "rows": []}, "news": {"n_24h": 0}, "trends": None}
    copy = dexscreener.copycats(q); news = gdelt.velocity(f'"{q}"' if " " in q else q)
    th = None
    for t in (trends if trends is not None else google_trends.trending(CFG["geos"])):
        if q.lower() in t["title"].lower() or t["title"].lower() in q.lower(): th = t; break
    text = " ".join([q, extra_text] + [x[2] for x in news.get("latest", [])] + ((th or {}).get("news") or []))
    s, notes = score(text, copy, news, th, social_for(q), CFG)
    return {"story": q, "score": s, "notes": notes, "copycats": copy, "news": {k: v for k, v in news.items() if k != "latest"}, "trends": th}
def pretty(r):
    print(f"\n=== {r['story']}  →  SCORE {r['score']}/100  ({'LAUNCH' if r['score']>=CFG['thresholds']['launch'] else 'CANDIDATE' if r['score']>=CFG['thresholds']['candidate'] else 'watch' if r['score']>=CFG['thresholds']['watch'] else 'pass'})")
    for n in r["notes"]: print("  -", n)
    for c in r["copycats"]["rows"][:6]: print(f"    copycat: {c['name'][:28]:28} {str(c['symbol']):8} mcap ${c['mcap']:>10,.0f} vol24 ${c['vol24']:>10,.0f} age {c['age_h']}h {c['dex']}")
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "trending"
    if cmd == "story":
        args = sys.argv[2:]; ctx = ""
        if "--context" in args: i = args.index("--context"); ctx = " ".join(args[i + 1:]); args = args[:i]
        pretty(story(" ".join(args), extra_text=ctx))
    elif cmd == "conflicts":
        c = dexscreener.symbol_conflicts(sys.argv[2]); print(f"{len(c)} exact-symbol pairs for {sys.argv[2]}"); [print(" ", (p['baseToken'] or {}).get('name'), p.get('chainId'), p.get('marketCap')) for p in c[:10]]
    elif cmd in ("trending", "watch"):
        while True:
            tr = google_trends.trending(CFG["geos"]); seen = set(); results = []
            limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else CFG.get("trending_limit", 15)
            for t in sorted(tr, key=lambda x: -x["traffic_n"])[:limit]:
                k = t["title"].lower()
                if k in seen or not k: continue
                seen.add(k)
                try: results.append(story(t["title"], trends=tr, extra_text=" ".join(t.get("news") or []), prefilter=True))
                except Exception as e: print("err", k, e, file=sys.stderr)
            for f in CFG.get("google_alert_feeds") or []:
                try:
                    for it in google_alerts.items(f)[:5]: results.append(story(it["title"][:60]))
                except Exception as e: print("alerts err", e, file=sys.stderr)
            results.sort(key=lambda r: -r["score"])
            print(f"\n{time.strftime('%Y-%m-%d %H:%M:%S')}  scanned {len(results)} stories; top:")
            for r in results[:8]: print(f"  {r['score']:3d}  {r['story'][:40]:40}  copycats6h={r['copycats']['n_last_6h']} news24h={r['news']['n_24h']}")
            for r in results:
                if r["score"] >= CFG["thresholds"]["candidate"]: pretty(r)
            if cmd == "trending": break
            time.sleep(CFG["poll_minutes"] * 60)
