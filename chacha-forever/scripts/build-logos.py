#!/usr/bin/env python3
"""Assemble the composite logos (coin, avatar, lockup, banner, OG) from brand/logo/cha-mark.svg.
Edit cha-mark.svg, run this, then `node scripts/export.mjs`."""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
logo = root / 'brand' / 'logo'
mark = (logo / 'cha-mark.svg').read_text()
defs = re.search(r'<defs>(.*?)</defs>', mark, re.S).group(1)
body = mark.split('<!-- BODY -->', 1)[1].rsplit('</svg>', 1)[0]
FONT = "font-family=\"Fredoka, 'Arial Rounded MT Bold', 'Nunito', 'Segoe UI', Arial, sans-serif\""
EXTRA = '''
    <linearGradient id="rim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFE994"/><stop offset="0.45" stop-color="#F5B82E"/><stop offset="1" stop-color="#B87A08"/></linearGradient>
    <radialGradient id="face" cx="50%" cy="30%" r="80%"><stop offset="0" stop-color="#1E2A4A"/><stop offset="1" stop-color="#0B0F1A"/></radialGradient>
    <radialGradient id="night" cx="50%" cy="0%" r="90%"><stop offset="0" stop-color="#1E2A4A"/><stop offset="1" stop-color="#0B0F1A"/></radialGradient>
    <radialGradient id="sky" cx="50%" cy="20%" r="85%"><stop offset="0" stop-color="#DDF1FF"/><stop offset="0.6" stop-color="#9ED3FF"/><stop offset="1" stop-color="#5FA9E8"/></radialGradient>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#F5B82E" stop-opacity="0.55"/><stop offset="0.55" stop-color="#F5B82E" stop-opacity="0.18"/><stop offset="1" stop-color="#F5B82E" stop-opacity="0"/></radialGradient>
    <path id="rimPath" d="M256,256 m-230,0 a230,230 0 1,1 460,0 a230,230 0 1,1 -460,0"/>
'''
def svg(w, h, label, inner):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}">\n'
            f'  <defs>{defs}{EXTRA}</defs>\n{inner}\n</svg>\n')
def mark_at(tx, ty, s, glow=True, glow_r=190):
    g = f'<circle cx="256" cy="300" r="{glow_r}" fill="url(#glow)"/>' if glow else ''
    return f'<g transform="translate({tx} {ty}) scale({s})">{g}{body}</g>'
coin_body = ('<circle cx="256" cy="256" r="254" fill="url(#rim)"/><circle cx="256" cy="256" r="254" fill="none" stroke="#9A6606" stroke-width="3"/>'
             '<circle cx="256" cy="256" r="208" fill="url(#face)" stroke="#9A6606" stroke-width="4"/>'
             '<circle cx="256" cy="256" r="200" fill="none" stroke="#F5B82E" stroke-width="2" opacity="0.5"/>'
             + mark_at(256 - 256*0.74, 262 - 262*0.74, 0.74))
coin = coin_body + (f'<text {FONT} font-weight="700" font-size="25" letter-spacing="3.5" fill="#1B1B1F">'
        '<textPath href="#rimPath" startOffset="0">CHA CHA FOREVER ✦ $CHA ✦ CHA CHA FOREVER ✦ $CHA ✦</textPath></text>')
(logo / 'cha-coin.svg').write_text(svg(512, 512, '$CHA coin', coin))
avatar = ('<circle cx="256" cy="256" r="256" fill="url(#sky)"/><circle cx="256" cy="256" r="244" fill="none" stroke="#F5B82E" stroke-width="6"/>'
          '<g fill="#FFFFFF" opacity="0.45"><ellipse cx="120" cy="420" rx="90" ry="26"/><ellipse cx="400" cy="130" rx="70" ry="20"/></g>'
          + mark_at(256 - 256*0.86, 266 - 262*0.86, 0.86, glow=False))
(logo / 'cha-avatar.svg').write_text(svg(512, 512, 'Cha Cha Forever avatar', avatar))
lockup = (f'<g transform="translate(30 20) scale(0.86)">{coin_body}</g>'
          f'<text x="520" y="250" {FONT} font-weight="700" font-size="190" fill="#F8F7F2" stroke="#0B0F1A" stroke-width="10" paint-order="stroke" letter-spacing="-3">CHA CHA</text>'
          f'<text x="526" y="360" {FONT} font-weight="600" font-size="74" fill="url(#halo)" stroke="#0B0F1A" stroke-width="8" paint-order="stroke" letter-spacing="24">FOREVER</text>'
          f'<rect x="1206" y="296" width="200" height="74" rx="37" fill="#F5B82E"/><text x="1306" y="348" text-anchor="middle" {FONT} font-weight="700" font-size="46" fill="#1B1B1F">$CHA</text>')
(logo / 'cha-lockup.svg').write_text(svg(1600, 480, 'Cha Cha Forever lockup', lockup))
clouds = '<g fill="#F8F7F2" opacity="0.06"><ellipse cx="180" cy="430" rx="220" ry="60"/><ellipse cx="1320" cy="90" rx="200" ry="52"/><ellipse cx="900" cy="470" rx="260" ry="50"/><ellipse cx="620" cy="40" rx="150" ry="40"/></g>'
banner = ('<rect width="1500" height="500" fill="url(#night)"/>' + clouds + mark_at(60, 10, 0.94) +
          f'<text x="560" y="215" {FONT} font-weight="700" font-size="150" fill="#F8F7F2" letter-spacing="-3">CHA CHA</text>'
          f'<text x="566" y="300" {FONT} font-weight="600" font-size="62" fill="url(#halo)" letter-spacing="22">FOREVER</text>'
          '<text x="566" y="372" font-family="Inter, \'Segoe UI\', Arial, sans-serif" font-weight="500" font-size="30" fill="#D7DBE5">Justice for Cha Cha. Forever on-chain.</text>'
          f'<rect x="566" y="402" width="170" height="58" rx="29" fill="#F5B82E"/><text x="651" y="442" text-anchor="middle" {FONT} font-weight="700" font-size="34" fill="#1B1B1F">$CHA</text>'
          '<text x="760" y="441" font-family="Inter, \'Segoe UI\', Arial, sans-serif" font-weight="500" font-size="26" fill="#9AA3B5">chachaforever.com</text>')
(logo / 'cha-banner.svg').write_text(svg(1500, 500, 'Cha Cha Forever banner', banner))
og = ('<rect width="1200" height="630" fill="url(#night)"/>'
      '<g fill="#F8F7F2" opacity="0.06"><ellipse cx="150" cy="560" rx="220" ry="60"/><ellipse cx="1060" cy="80" rx="200" ry="52"/><ellipse cx="760" cy="600" rx="260" ry="50"/></g>'
      f'<g transform="translate(830 90) scale(0.75)">{coin_body}</g>'
      f'<text x="70" y="140" {FONT} font-weight="600" font-size="28" fill="#F5B82E" letter-spacing="6">JUSTICE FOR CHA CHA</text>'
      f'<text x="66" y="250" {FONT} font-weight="700" font-size="96" fill="#F8F7F2" letter-spacing="-2">They couldn\'t</text>'
      f'<text x="66" y="350" {FONT} font-weight="700" font-size="96" fill="#F8F7F2" letter-spacing="-2">bury her twice.</text>'
      '<text x="70" y="425" font-family="Inter, \'Segoe UI\', Arial, sans-serif" font-weight="500" font-size="27" fill="#D7DBE5">Fair launch · 0% team · 50% of creator fees → animal welfare</text>'
      f'<rect x="70" y="470" width="170" height="60" rx="30" fill="#F5B82E"/><text x="155" y="511" text-anchor="middle" {FONT} font-weight="700" font-size="36" fill="#1B1B1F">$CHA</text>'
      '<text x="262" y="510" font-family="Inter, \'Segoe UI\', Arial, sans-serif" font-weight="500" font-size="28" fill="#9AA3B5">chachaforever.com</text>')
(logo / 'cha-og.svg').write_text(svg(1200, 630, 'Cha Cha Forever', og))
print('built coin, avatar, lockup, banner, og')
