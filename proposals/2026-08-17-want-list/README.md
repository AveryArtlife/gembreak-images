# Private Sales Proposal — Comic Want List (August 2026)

Generates `Private-Sales-Proposal-Comics-Aug-2026.pdf`, an 8-page client-facing
proposal for the five certified books offered in the August 17, 2026 want-list
email (Action Comics #1, Fantastic Four #1, Amazing Fantasy #15, The Incredible
Hulk #1, All Star Comics #8).

## Regenerating

```bash
pip install reportlab pillow
python3 generate_proposal.py
```

## Adding cover images

Drop images of the certified copies into `covers/` named by book key, then
re-run the script:

| File | Book |
| --- | --- |
| `covers/action1.jpg` | Action Comics #1 |
| `covers/ff1.jpg` | Fantastic Four #1 |
| `covers/af15.jpg` | Amazing Fantasy #15 |
| `covers/hulk1.jpg` | The Incredible Hulk #1 |
| `covers/allstar8.jpg` | All Star Comics #8 |

`.png` and `.jpeg` extensions also work. Any book without an image falls back
to a typographic placeholder panel.

Prices shown are the client-facing asking prices only; edit `BOOKS` in
`generate_proposal.py` to adjust pricing, copy, or ordering.
