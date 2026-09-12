# GemBreak Visual Audit Decision Policy

This policy protects currently usable images from unnecessary regeneration.

## Classification

- `approved`: visually correct, upright, complete, and already close to the catalog presentation.
- `acceptable variation`: visually usable with harmless differences in canvas size, scale, centering, or mild natural bracelet taper/perspective.
- `true failure`: a human reviewer confirms a material presentation or content defect.
- `unrenderable`: the product cannot be reliably identified or the source file cannot be reviewed.

## True-failure conditions

A watch is a true failure only when at least one material defect is visible: strong angle or non-upright presentation; clipped case; head-only or incomplete/mismatched bracelet or strap; exposed buckle, holes, tail, or keeper hardware that conflicts with the established catalog crop; severe zoom-out; opaque/background contamination; visible watermark or overlay; wrong or mangled product details; or obvious generation damage.

Minor numerical deviations are not true failures by themselves. A slightly wider/narrower watch, a different transparent canvas size, mild depth in a correctly presented bracelet, or small centering differences remain approved or acceptable when visually usable.

## Numeric safeguards

`caseW`, `bboxH`, `cxRatio`, `cyRatio`, canvas, color mode, PNG chunks, and threshold warnings remain in `qa_audit.csv`. Extreme values trigger a closer visual check but never automatically set `needs_rerender=true`.

Only `human_classification=true failure` sets `needs_rerender=true`. Approved and acceptable images remain byte-for-byte unchanged.
