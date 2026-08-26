# Private Sales Proposal — Five Certified Marvel Keys (August 2026)

Generates `Private-Sales-Proposal-Marvel-Keys-Aug-2026.pdf`, an 8-page
client-facing proposal for five CGC-certified Marvel keys: Amazing Fantasy #15
(CGC 8.0, QES), Marvel Spotlight #5 (CGC 9.8), Fantastic Four #1 (CGC 8.5),
The Incredible Hulk #181 (CGC 9.8), and The Amazing Spider-Man #13 (CGC 9.4).
Each lot page carries the CGC cert number, page quality, and creator credits
taken from the slab labels.

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

`.png` and `.jpeg` extensions also work. Any book without an image falls back
to a typographic placeholder panel. Edit `BOOKS` in `generate_proposal.py` to
adjust pricing, copy, or lot order.
