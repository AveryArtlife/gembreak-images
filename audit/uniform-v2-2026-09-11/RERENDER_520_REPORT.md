# Approved 520-watch remediation

Date: 2026-09-11

## Result

- Authoritative inventory: 2,456 watches
- Approved rerender scope: 520 true failures
- Protected files: 1,936
- Installed candidate/hash matches: 520
- Protected files verified byte-for-byte unchanged: 1,936
- Final visual passes: 520
- Final technical sanity passes: 520
- Remaining visual failures in the approved scope: 0

Only the 520 rows marked `allowed_to_change=True` in
`rerender-scope-lock/scope-lock-sha256.csv` were installed into
`watches-only/`.

## QA method

Each approved image was reviewed on black for product identity, dead-on front
orientation, correct compact bracelet or strap presentation, transparency,
visible watermarking, loose fastening hardware, opened strap tails, and obvious
generation artifacts. Source-dial registration was used where it was visually
safe; 16 registration artifacts were replaced with the clean Higgsfield raw
render, and 23 images received targeted Higgsfield visual retries.

Four visually acceptable images have a `bboxH-low` numerical warning. The
measurements are retained in `qa_rerender_metrics.csv` and `qa_audit.csv`; in
accordance with the review policy, numerical target deviations are warnings and
did not override the individual visual pass.

## Evidence

- `qa_audit.csv`: all 2,456 original classifications plus post-remediation
  measurements, warnings, review result, and SHA-256.
- `rerender-staging/final-candidates/qa_rerender_metrics.csv`: final metrics and
  review notes for the 520 installed files.
- `scope-integrity-after-rerender.csv`: before/after hash evidence for every
  inventory SKU.
- `scope-integrity-after-rerender.json`: final integrity totals.
- `rerender-staging/final-candidates/visual-review-summary.json`: final 520-file
  visual/technical summary.
- `rerender-staging/final-candidates/black-background-contact-sheets/`: the 33
  final contact sheets included in the delivery archive.

The large raw-generation and duplicate staging PNGs are intentionally not
required for repository delivery because the approved final PNGs are installed
at their canonical `watches-only/` paths.
