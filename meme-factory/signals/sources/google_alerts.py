"""Google Alerts RSS. Create alerts at google.com/alerts for your standing watchlist (e.g. 'dog euthanized', 'zoo animal viral',
'justice for', 'squirrel seized') with 'Deliver to: RSS feed', paste the feed URLs into config. Polled like any feed."""
import re, html
from .http import get
def items(feed_url):
    xml = get(feed_url); out = []
    for e in re.findall(r"<entry>(.*?)</entry>", xml, re.S):
        t = re.search(r"<title[^>]*>(.*?)</title>", e, re.S); l = re.search(r'<link[^>]*href="([^"]+)"', e); p = re.search(r"<published>(.*?)</published>", e)
        out.append({"source": "google_alerts", "title": html.unescape(re.sub(r"<[^>]+>", "", t.group(1))) if t else "", "url": l.group(1) if l else "", "published": p.group(1) if p else ""})
    return out
