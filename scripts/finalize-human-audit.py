#!/usr/bin/env python3
"""Apply the completed human review to the 2,456-row audit."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
AUDIT = REPO / "audit" / "uniform-v2-2026-09-11"
QA_PATH = AUDIT / "qa_audit.csv"
CANDIDATE_PATH = AUDIT / "visual-failure-candidates.csv"
TRUE_FAILURE_PATH = AUDIT / "true_failures_for_review.csv"
UNRENDERABLE_PATH = AUDIT / "unrenderable_for_review.csv"


# These candidate numbers were visually judged usable. Their metric excursions
# remain recorded as warnings, but they do not authorize a rerender.
ACCEPTABLE_CANDIDATE_NUMBERS = {
    1,
    437, 442, 443, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455,
    456, 459, 460, 461, 462, 464,
    465, 466, 467, 468, 469, 470, 471, 472, 474, 475, 476, 477, 478, 479,
    480, 485, 486, 487, 488, 489, 490, 491, 494, 495,
    497, 499, 502, 503, 504, 505, 506, 507, 508, 509, 510, 514, 517, 518,
    519, 520, 521, 522, 524, 525, 526, 527, 528,
    529, 530, 531, 532, 533, 534, 535, 537, 538, 539, 540, 542, 543, 546,
    552, 555, 556, 557, 559, 560,
    570, 571, 576, 578, 579, 581, 582, 583, 585, 587, 588, 592,
    596, 598, 599, 600, 603, 605, 606, 612, 613, 615, 617, 618, 624,
}

UNRENDERABLE_CANDIDATE_NUMBERS = {548}

LEGACY_TRUE_FAILURE_REASONS = {
    "CRSDA02002W": "visible SAPPHIRE CRYSTAL retailer overlay across bracelet",
    "W130": "incomplete product image; lower bracelet missing",
    "W1326": "incomplete product image; lower bracelet missing",
    "WWN01 751 7761 4187-SET": "full NATO strap hardware visible",
    "WWNH24655331": "severe zoom-out with full unrolled strap and buckle visible",
    "WWNH32506730": "watch shown around a display cushion/support",
    "WWNH82565930": "full NATO strap hardware visible",
    "WWNL3.821.4.53.9": "full NATO strap hardware visible",
    "WWNWAY208D.FC8221": "full NATO strap hardware visible",
}

LEGACY_ACCEPTABLE = {
    "CRAN8194-51L",
    "CRAV0106-01L",
    "W146",
    "W211",
    "W2118",
    "W215",
    "WWNCBN2A1AA.FT6228",
    "WWNCV201AP.FC6429",
    "WWNWAZ1010.FT8024",
    "WWNWAZ1110.FT8023",
}

NUMERIC_FIELDS = ("caseW", "bboxH", "cxRatio", "cyRatio", "canvas", "color_mode", "extra_chunks")


def append_note(existing: str, addition: str) -> str:
    if addition in existing:
        return existing
    return f"{existing}; {addition}" if existing else addition


def main() -> None:
    with CANDIDATE_PATH.open(newline="", encoding="utf-8-sig") as handle:
        candidates = list(csv.DictReader(handle))
    assert len(candidates) == 625

    candidate_decisions: dict[str, tuple[str, str]] = {}
    for number, row in enumerate(candidates, start=1):
        if number in UNRENDERABLE_CANDIDATE_NUMBERS:
            decision = "unrenderable"
            reason = "non-watch stopwatch image; remove from watch inventory, do not rerender"
        elif number in ACCEPTABLE_CANDIDATE_NUMBERS:
            decision = "acceptable variation"
            reason = f"human visual review accepted: {row['reason']}"
        else:
            decision = "true failure"
            reason = row["reason"]
        assert row["sku"] not in candidate_decisions
        candidate_decisions[row["sku"]] = (decision, reason)

    with QA_PATH.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    assert len(rows) == 2456
    assert len({row["sku"] for row in rows}) == 2456
    numeric_before = {row["sku"]: tuple(row[field] for field in NUMERIC_FIELDS) for row in rows}

    for row in rows:
        sku = row["sku"]
        if sku in candidate_decisions:
            decision, reason = candidate_decisions[sku]
            row["human_classification"] = decision
            row["needs_rerender"] = "True" if decision == "true failure" else "False"
            row["pass_content"] = "False" if decision in {"true failure", "unrenderable"} else "True"
            row["notes"] = append_note(row["notes"], f"human full-resolution review: {reason}")
        elif sku in LEGACY_TRUE_FAILURE_REASONS:
            row["human_classification"] = "true failure"
            row["needs_rerender"] = "True"
            row["pass_content"] = "False"
            row["notes"] = append_note(
                row["notes"],
                f"human full-resolution review: {LEGACY_TRUE_FAILURE_REASONS[sku]}",
            )
        elif sku in LEGACY_ACCEPTABLE:
            row["human_classification"] = "acceptable variation"
            row["needs_rerender"] = "False"
            row["pass_content"] = "True"
            row["notes"] = append_note(
                row["notes"],
                "human full-resolution review accepted current image; metric warnings only",
            )

    assert numeric_before == {
        row["sku"]: tuple(row[field] for field in NUMERIC_FIELDS) for row in rows
    }

    with QA_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    review_fields = [
        "sku", "human_classification", "caseW", "bboxH", "cxRatio", "cyRatio",
        "canvas", "color_mode", "extra_chunks", "metric_warnings", "notes",
    ]
    true_failures = [row for row in rows if row["human_classification"] == "true failure"]
    unrenderable = [row for row in rows if row["human_classification"] == "unrenderable"]
    with TRUE_FAILURE_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=review_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(true_failures)
    with UNRENDERABLE_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=review_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(unrenderable)

    counts = Counter(row["human_classification"] for row in rows)
    assert counts["true failure"] == 520, counts
    assert counts["unrenderable"] == 1, counts
    assert len(true_failures) == 520
    print(f"rows={len(rows)} counts={dict(counts)}")
    print(f"true_failures={TRUE_FAILURE_PATH}")
    print(f"unrenderable={UNRENDERABLE_PATH}")


if __name__ == "__main__":
    main()
