#!/usr/bin/env python3
"""Prints the markdown table for docs/07-IMAGERY-AUDIT.md from the CoinGecko dump (scratch: cg/coins.json).
Classification (subject real? token image photo/cartoon?) is hand-labelled from the token images on 2026-10-29."""
import json, sys
rows = {r['id']: r for r in json.load(open(sys.argv[1]))}
# id: (display, subject, token image type, notes)
LABELS = {
 'dogecoin':            ('Dogecoin DOGE', 'real dog (Kabosu)', 'photo', 'the original meme photo, on a coin'),
 'dogwifcoin':          ('dogwifhat WIF', 'real dog (Achi)', 'photo', 'the meme photo itself'),
 'popcat':              ('Popcat', 'real cat (Oatmeal)', 'photo', 'the meme frame itself'),
 'peanut-the-squirrel': ('Peanut the Squirrel PNUT', 'real squirrel, news story', 'cartoon of the iconic photo', 'cowboy-hat photo redrawn as a character'),
 'moo-deng':            ('Moo Deng', 'real hippo, viral clips', 'cartoon of the iconic pose', 'the screaming-hippo pose, illustrated'),
 'neiro-3':             ('Neiro', 'real dog (Kabosu successor)', 'cartoon on a coin', 'a rival Neiro token used the real photo; both ran'),
 'michi':               ('Michi', 'real cat', 'photo', 'meme photo'),
 'fred-the-raccoon':    ('Fred the Raccoon', 'real raccoon, news story', 'photo (stylised glow)', 'same week as PNUT, never broke out'),
 'gigachad-2':          ('GigaChad', 'real person (meme)', 'photo', ''),
 'mother-iggy':         ('Mother Iggy', 'real person (Iggy Azalea)', 'photo', 'celebrity launch'),
 'smoking-chicken-fish':('Smoking Chicken Fish', 'real photo meme', 'photo', ''),
 'hawk-tuah':           ('Hawk Tuah', 'real person, viral clip', 'cartoon', 'collapsed amid insider-dump claims'),
 'offcial-mascot-of-the-holy-year': ('Luce', 'official mascot (figure)', 'photo of the mascot', ''),
 'chill-guy':           ('Chill Guy', 'fictional character', 'cartoon', 'the artwork is the meme'),
 'pepe':                ('Pepe', 'fictional character', 'cartoon', ''),
 'based-brett':         ('Brett', 'fictional character', 'cartoon', ''),
 'bonk':                ('Bonk', 'fictional Shiba', 'cartoon', ''),
 'shiba-inu':           ('Shiba Inu SHIB', 'fictional Shiba', 'cartoon', ''),
 'floki':               ('Floki', 'named after a real dog, drawn', 'cartoon', ''),
 'baby-doge-coin':      ('Baby Doge', 'fictional', 'cartoon', ''),
 'cat-in-a-dogs-world': ('MEW', 'fictional cat', 'cartoon', ''),
 'ponke':               ('Ponke', 'fictional', 'cartoon', ''),
 'hoppy-meme':          ('Hoppy', 'fictional (Pepe spin-off)', 'cartoon', ''),
 'maneki':              ('Maneki', 'fictional', 'cartoon', ''),
 'wen-4':               ('Wen', 'fictional cat', 'cartoon', ''),
 'pudgy-penguins':      ('Pudgy Penguins', 'NFT IP', 'cartoon', ''),
 'ai16z':               ('ai16z', 'fictional', 'cartoon (anime)', ''),
 'fartcoin':            ('Fartcoin', 'no subject', 'text', ''),
 'goatseus-maximus':    ('Goatseus Maximus', 'no subject', 'ascii', ''),
}
def m(n): return '—' if not n else (f'${n/1e9:.1f}B' if n >= 1e9 else f'${n/1e6:,.0f}M')
print('| Coin | Subject | Token image | Est. ATH market cap | ATH date | Now | Note |')
print('|---|---|---|---|---|---|---|')
for cid, (name, subj, img, note) in sorted(LABELS.items(), key=lambda kv: -(rows.get(kv[0], {}).get('ath_mcap_est') or 0)):
    r = rows.get(cid)
    if not r: print(f'| {name} | {subj} | {img} | n/a | | | {note} |'); continue
    print(f"| {name} | {subj} | {img} | {m(r['ath_mcap_est'])} | {str(r['ath_date'])[:10]} | {m(r['mcap_usd'])} | {note} |")
