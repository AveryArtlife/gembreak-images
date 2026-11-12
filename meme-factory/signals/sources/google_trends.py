"""Google Trends 'Trending now' RSS (public, no key). Returns the 10 newest trends per geo with approx traffic.
Works as of 2026-10-29 (tested). Only the newest ~10 per geo, so poll every 5 minutes and keep history."""
import re, html
from .http import get
GEOS = ["US", "GB", "CA", "AU"]
def trending(geos=GEOS):
    out = []
    for g in geos:
        xml = get(f"https://trends.google.com/trending/rss?geo={g}")
        for it in re.findall(r"<item>(.*?)</item>", xml, re.S):
            title = re.search(r"<title>(.*?)</title>", it, re.S)
            traffic = re.search(r"approx_traffic>(.*?)<", it)
            pub = re.search(r"pubDate>(.*?)<", it)
            news = re.findall(r"news_item_title>(.*?)<", it, re.S)
            out.append({"source": "google_trends", "geo": g,
                        "title": html.unescape(title.group(1).strip()) if title else "",
                        "approx_traffic": traffic.group(1) if traffic else "",
                        "traffic_n": int(re.sub(r"\D", "", traffic.group(1)) or 0) if traffic else 0,
                        "published": pub.group(1) if pub else "",
                        "news": [html.unescape(re.sub(r"<!\[CDATA\[|\]\]>", "", n)).strip() for n in news][:3]})
    return out
