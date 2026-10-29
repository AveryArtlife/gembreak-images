"""Score a story 0–100 from the sources. Weights are a starting point; recalibrate from post-mortems.
Signals (max points):
  copycat launches on DexScreener     30  (the market is already trying; nobody produced it)
  news velocity (GDELT)               20
  Google Trends presence/traffic      15
  social engagement velocity (Apify)  20  (0 if not configured)
  memeability text heuristics         15  (character + injustice/fun words)
Hard stop: any no-go word → score 0.
Penalty: a produced competitor already > $250K mcap with liquidity → -25 (you are late)."""
import math
def text_score(text, cfg):
    t = text.lower()
    if any(w in t for w in cfg["no_go_words"]): return 0, True
    c = any(w in t for w in cfg["character_words"]); i = any(w in t for w in cfg["injustice_words"]); f = any(w in t for w in cfg["fun_words"])
    return (6 if c else 0) + (6 if i else 0) + (3 if f else 0), False
def score(story_text, copy, news, trends_hit, social, cfg):
    s = 0; notes = []
    m, nogo = text_score(story_text, cfg["memeability"])
    if nogo: return 0, ["NO-GO word present"]
    s += m; notes.append(f"memeability {m}/15")
    # copycats: log-scaled count in last 6h, bonus for total volume, penalty if someone produced it already
    n6 = copy.get("n_last_6h", 0); n = copy.get("n_launches", 0)
    cp = min(30, 10 * math.log2(1 + n6) + (5 if copy.get("total_vol24", 0) > 50_000 else 0))
    s += cp; notes.append(f"copycats {n6} in 6h / {n} in 48h → {cp:.0f}/30")
    if copy.get("max_mcap", 0) > 250_000 and any(r.get("liq", 0) > 20_000 for r in copy.get("rows", [])):
        s -= 25; notes.append("produced competitor already live (-25)")
    # news velocity
    n1, n3, n24 = news.get("n_1h", 0), news.get("n_3h", 0), news.get("n_24h", 0)
    nv = min(20, 4 * math.log2(1 + n24) + (6 if n3 and n3 >= n24 / 4 else 0) + (4 if n1 else 0))
    s += nv; notes.append(f"news {n1}/{n3}/{n24} (1h/3h/24h), {news.get('domains_24h', 0)} domains → {nv:.0f}/20")
    # trends
    tv = 0
    if trends_hit: tv = min(15, 5 + 2 * math.log2(1 + trends_hit.get("traffic_n", 0) / 100))
    s += tv; notes.append(f"google trends {'hit ' + trends_hit.get('approx_traffic', '') if trends_hit else 'no'} → {tv:.0f}/15")
    # social
    sv = 0
    if social and social.get("ratio") not in (None, 0):
        r = social["ratio"]; sv = min(20, 8 + 4 * math.log2(1 + (r if r != float('inf') else 8)))
    s += sv; notes.append(f"social velocity → {sv:.0f}/20" if social else "social: not configured (0/20)")
    return max(0, min(100, round(s))), notes
