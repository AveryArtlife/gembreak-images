# Private Sales Proposal — Six Certified Comic Book Keys (August 2026)

Generates `Private-Sales-Proposal-Comic-Keys-Aug-2026.pdf`, a 9-page
client-facing proposal for six CGC-certified keys: Amazing Fantasy #15
(CGC 8.0, QES), Marvel Spotlight #5 (CGC 9.8), Fantastic Four #1 (CGC 8.5),
The Incredible Hulk #181 (CGC 9.8), The Amazing Spider-Man #13 (CGC 9.4), and
Action Comics #241 (CGC 9.2). Each lot page carries the CGC cert number, page
quality, and creator credits taken from the slab labels.

## Regenerating

```bash
pip install reportlab pillow
python3 generate_proposal.py
```

## Adding cover images

Drop photos of the certified copies into `covers/` named by book key, then
re-run the script:

| File | Book |
| --- | --- |
| `covers/af15.jpg` | Amazing Fantasy #15 |
| `covers/ms5.jpg` | Marvel Spotlight #5 |
| `covers/ff1.jpg` | Fantastic Four #1 |
| `covers/hulk181.jpg` | The Incredible Hulk #181 |
| `covers/asm13.jpg` | The Amazing Spider-Man #13 |
| `covers/action241.jpg` | Action Comics #241 |

`.png` and `.jpeg` extensions also work, and filenames are matched loosely —
`Amazing Fantasy 15.jpg`, `AF15.PNG`, `ghost-rider.jpg`, and `wolverine.jpg`
all resolve to the right lot (see `ALIASES` in the script). Any book without an
image falls back to a typographic placeholder panel.

Edit `BOOKS` in `generate_proposal.py` to adjust pricing, copy, or lot order.

## Cover image status

Verified against each slab's CGC certification number:

| Lot | Cover file | Cert |
| --- | --- | --- |
| Amazing Fantasy #15 | `covers/af15.jpg` | 1971545001 |
| Marvel Spotlight #5 | `covers/ms5.jpg` | 4757016020 |
| Fantastic Four #1 | `covers/ff1.jpg` | 1201137001 |
| The Incredible Hulk #181 | `covers/hulk181.jpg` | 4748401011 |
| The Amazing Spider-Man #13 | *awaiting image* | 3949630002 |
| Action Comics #241 | *awaiting image* | 4614192004 |

`covers/not-in-proposal/` holds two uploaded slabs that are not lots in this
proposal — an Incredible Hulk #1 (CGC 8.0, QES, cert 3832523002) and a second
Amazing Fantasy #15 (CGC 8.0, cert 4615094001, distinct from the copy above).
Both need pricing before they can be added.
