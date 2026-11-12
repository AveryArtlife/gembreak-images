#!/usr/bin/env python3
"""Inject the current cha-mark.svg (nav) and cha-coin.svg (hero) into site/index.html between marker comments.
Run after scripts/build-logos.py. Gradient ids are suffixed so the two inline SVGs never collide."""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
idx = root / 'site' / 'index.html'
def load(name, suffix, strip_size=False):
    s = (root / 'brand' / 'logo' / name).read_text()
    s = re.sub(r'\s+width="\d+" height="\d+"', '', s, count=1) if strip_size else s
    s = re.sub(r'\s+role="img"\s+aria-label="[^"]*"', ' aria-hidden="true"', s, count=1)
    for i in sorted(set(re.findall(r'id="([A-Za-z0-9_-]+)"', s)), key=len, reverse=True):
        s = s.replace(f'id="{i}"', f'id="{i}{suffix}"').replace(f'url(#{i})', f'url(#{i}{suffix})').replace(f'href="#{i}"', f'href="#{i}{suffix}"')
    return s.replace('<!-- BODY -->', '')
html = idx.read_text()
html = re.sub(r'<!-- BRAND-MARK -->.*?<!-- /BRAND-MARK -->', lambda m: '<!-- BRAND-MARK -->' + load('cha-mark.svg', '-n', True) + '<!-- /BRAND-MARK -->', html, flags=re.S)
html = re.sub(r'<!-- HERO-COIN -->.*?<!-- /HERO-COIN -->', lambda m: '<!-- HERO-COIN -->' + load('cha-coin.svg', '-h', True) + '<!-- /HERO-COIN -->', html, flags=re.S)
idx.write_text(html)
print('inlined mark + coin into site/index.html')
