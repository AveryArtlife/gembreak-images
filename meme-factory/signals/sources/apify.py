"""Apify runner (needs APIFY_TOKEN). Runs an actor synchronously and returns dataset items.
Actor ids and inputs live in config.yaml under `apify:`; see docs/02-SIGNAL-ENGINE.md for the catalogue."""
import os, json, urllib.request
def run_sync(actor_id, run_input, timeout_s=120):
    token = os.environ.get("APIFY_TOKEN")
    if not token: raise RuntimeError("APIFY_TOKEN not set")
    url = f"https://api.apify.com/v2/acts/{actor_id.replace('/', '~')}/run-sync-get-dataset-items?token={token}&timeout={timeout_s}&format=json&clean=true"
    req = urllib.request.Request(url, data=json.dumps(run_input).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout_s + 30) as r:
        return json.loads(r.read().decode())
def engagement_velocity(items, likes_key="likesCount", comments_key="commentsCount", ts_key="timestamp"):
    """Crude: total engagement on posts from the last 6h vs the 6h before. Caller maps keys per actor."""
    import time, datetime
    now = time.time(); a = b = 0
    for it in items:
        ts = it.get(ts_key); 
        try: t = datetime.datetime.fromisoformat(str(ts).replace("Z", "+00:00")).timestamp()
        except Exception: continue
        e = (it.get(likes_key) or 0) + 3 * (it.get(comments_key) or 0)
        if now - t <= 6 * 3600: a += e
        elif now - t <= 12 * 3600: b += e
    return {"eng_6h": a, "eng_prev_6h": b, "ratio": (a / b) if b else (float("inf") if a else 0)}
