"""DexScreener public API (no key). Two signals:
1. Copycat counter: how many pairs matching the story's words were created in the last N hours, and their volume.
   When spray deployers launch 10+ copies of a story inside an hour, the story is memeable. Fastest tripwire we have.
2. Exact-symbol conflict check for our own ticker.
Also exposes the paid-profile and boost feeds for watching what competitors pay for."""
import time, re
from .http import get_json
def search(q):
    return get_json("https://api.dexscreener.com/latest/dex/search", {"q": q}).get("pairs", []) or []
def _norm(x): return re.sub(r"[^a-z0-9]", "", (x or "").lower())
def copycats(phrase, hours=48, chain="solana"):
    """Pairs whose token NAME contains the story phrase (space/punctuation-insensitive: 'chacha' matches 'Justice for Cha Cha'),
    created in the last `hours`. Searches the phrase and each word of 4+ letters, then filters strictly."""
    now = time.time() * 1000; seen = {}; key = _norm(phrase)
    terms = [phrase] + [w for w in phrase.split() if len(w) >= 4 and _norm(w) != key]
    for t in terms:
        for p in search(t):
            if chain and p.get("chainId") != chain: continue
            created = p.get("pairCreatedAt") or 0
            if created and now - created > hours * 3600 * 1000: continue
            bt = p.get("baseToken") or {}; name = bt.get("name", ""); addr = bt.get("address")
            if key not in _norm(name) and key not in _norm(bt.get("symbol", "")): continue
            seen[addr] = {"name": name, "symbol": bt.get("symbol"), "dex": p.get("dexId"),
                          "mcap": p.get("marketCap") or p.get("fdv") or 0, "vol24": (p.get("volume") or {}).get("h24") or 0,
                          "liq": (p.get("liquidity") or {}).get("usd") or 0, "age_h": round((now - created) / 3.6e6, 1) if created else None,
                          "url": p.get("url")}
    rows = sorted(seen.values(), key=lambda r: -(r["mcap"] or 0))
    return {"source": "dexscreener", "phrase": phrase, "n_launches": len(rows), "n_last_6h": sum(1 for r in rows if r["age_h"] is not None and r["age_h"] <= 6),
            "max_mcap": max([r["mcap"] for r in rows] or [0]), "total_vol24": sum(r["vol24"] for r in rows), "rows": rows[:25]}
def symbol_conflicts(symbol):
    return [p for p in search(symbol) if (p.get("baseToken") or {}).get("symbol", "").upper() == symbol.upper()]
def latest_profiles():  # tokens that just paid for Enhanced Token Info
    return get_json("https://api.dexscreener.com/token-profiles/latest/v1")
def latest_boosts():    # tokens that just bought boosts
    return get_json("https://api.dexscreener.com/token-boosts/latest/v1")
