#!/usr/bin/env python3
"""Repair selected staged candidates without touching repository watch files."""

from __future__ import annotations

import argparse
import csv
import importlib.util
from pathlib import Path

from PIL import Image


def load_finalizer(project_root: Path):
    script = project_root / "scripts" / "finalize-higgsfield-watch-renders.py"
    spec = importlib.util.spec_from_file_location("watch_finalizer", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--raw-root", type=Path, required=True)
    parser.add_argument("--candidate-root", type=Path, required=True)
    parser.add_argument("--metrics", type=Path, required=True)
    parser.add_argument("--contact-sheets", type=Path, required=True)
    parser.add_argument("--method", required=True)
    parser.add_argument(
        "--dial-graft-status",
        default="skipped-after-visual-artifact",
        help="Audit label explaining why source-dial grafting was not used.",
    )
    parser.add_argument("--note", required=True)
    parser.add_argument("skus", nargs="+")
    args = parser.parse_args()

    finalizer = load_finalizer(args.project_root)
    with args.metrics.open(newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])
    for field in ("visual_review", "visual_notes", "repair_method"):
        if field not in fieldnames:
            fieldnames.append(field)

    by_sku = {row["sku"]: row for row in rows}
    missing = sorted(set(args.skus) - set(by_sku))
    if missing:
        raise SystemExit(f"SKUs absent from metrics: {', '.join(missing)}")

    for sku in args.skus:
        raw_path = args.raw_root / f"{sku}.png"
        output_path = args.candidate_root / f"{sku}.png"
        with Image.open(raw_path) as opened:
            normalized = finalizer.normalize(opened.convert("RGBA"))
        finalizer.save_core_png(normalized, output_path)
        metrics = finalizer.alpha_metrics(normalized)
        row = by_sku[sku]
        row.update(
            {
                "caseW": f"{metrics['caseW']:.6f}",
                "bboxH": f"{metrics['bboxH']:.6f}",
                "cxRatio": f"{metrics['cxRatio']:.6f}",
                "cyRatio": f"{metrics['cyRatio']:.6f}",
                "canvas": "1024x1536",
                "color_mode": "RGBA",
                "extra_chunks": "",
                "pass_technical_geometry": str(
                    0.74 <= metrics["caseW"] <= 0.82
                    and 0.84 <= metrics["bboxH"] <= 0.95
                    and 0.48 <= metrics["cxRatio"] <= 0.52
                    and 0.48 <= metrics["cyRatio"] <= 0.52
                ),
                "dial_graft": args.dial_graft_status,
                "registration_inliers": "",
                "final_sha256": finalizer.sha256(output_path),
                "visual_review": "PASS",
                "visual_notes": args.note,
                "repair_method": args.method,
            }
        )

    with args.metrics.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    contact_rows = []
    for row in rows:
        converted = dict(row)
        for key in ("caseW", "bboxH", "cxRatio", "cyRatio"):
            converted[key] = float(converted[key])
        converted["pass_technical_geometry"] = converted["pass_technical_geometry"] == "True"
        contact_rows.append(converted)
    finalizer.contact_sheets(contact_rows, args.candidate_root, args.contact_sheets)


if __name__ == "__main__":
    main()
