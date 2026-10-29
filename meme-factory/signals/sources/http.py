"""Tiny stdlib HTTP helper (no third-party deps so this runs anywhere)."""
import json, urllib.request, urllib.parse, time
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36 meme-factory-signals/0.1"
def get(url, params=None, headers=None, timeout=25, retries=2):
    if params: url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    h = {"User-Agent": UA, "Accept": "*/*"}; h.update(headers or {})
    for i in range(retries + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=timeout) as r:
                return r.read().decode("utf-8", "ignore")
        except Exception as e:
            if i == retries: raise
            time.sleep(1.5 * (i + 1))
def get_json(url, params=None, headers=None, timeout=25):
    return json.loads(get(url, params, headers, timeout))
