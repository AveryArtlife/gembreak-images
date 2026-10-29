"""GDELT 2.0 DOC API: global news articles mentioning a phrase, with timestamps. Public, no key.
One call for the last 24h, then window locally (GDELT rate-limits back-to-back calls with 429).
GDELT updates every 15 min and can lag up to an hour, so it confirms a story rather than discovering it."""
import time, datetime
from .http import get_json
def articles(query, timespan="24h", maxrecords=250):
    for i in range(3):
        try:
            d = get_json("https://api.gdeltproject.org/api/v2/doc/doc",
                         {"query": query, "mode": "artlist", "maxrecords": maxrecords, "format": "json", "timespan": timespan, "sort": "datedesc"})
            return d.get("articles", []) if isinstance(d, dict) else []
        except Exception as e:
            if "429" in str(e) and i < 1: time.sleep(5); continue
            raise
def _age_h(seendate):
    try:
        t = datetime.datetime.strptime(seendate, "%Y%m%dT%H%M%SZ").replace(tzinfo=datetime.timezone.utc)
        return (datetime.datetime.now(datetime.timezone.utc) - t).total_seconds() / 3600
    except Exception: return 99
def velocity(query):
    a24 = articles(query, "24h")
    ages = [_age_h(a.get("seendate", "")) for a in a24]
    domains = sorted({a.get("domain", "") for a in a24})
    return {"source": "gdelt", "query": query, "n_24h": len(a24), "n_3h": sum(1 for h in ages if h <= 3), "n_1h": sum(1 for h in ages if h <= 1),
            "domains_24h": len(domains), "top_domains": domains[:12],
            "latest": [(a.get("seendate"), a.get("domain"), (a.get("title") or "")[:90]) for a in a24[:5]]}
