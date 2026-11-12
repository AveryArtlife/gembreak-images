#!/usr/bin/env python3
"""Package the approved 520 watch PNGs into exactly three delivery archives."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import zipfile
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--scope-lock", type=Path, required=True)
    parser.add_argument("--metrics", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--qa-audit", type=Path, required=True)
    parser.add_argument("--integrity-csv", type=Path, required=True)
    parser.add_argument("--integrity-json", type=Path, required=True)
    parser.add_argument("--visual-summary", type=Path, required=True)
    parser.add_argument("--contact-sheets", type=Path, required=True)
    parser.add_argument("--targeted-comparisons", type=Path, required=True)
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    with args.scope_lock.open(newline="") as handle:
        scope = [
            row for row in csv.DictReader(handle)
            if row["allowed_to_change"].lower() == "true"
        ]
    if len(scope) != 520:
        raise SystemExit(f"expected 520 approved files, found {len(scope)}")
    with args.metrics.open(newline="") as handle:
        metrics = {row["sku"]: row for row in csv.DictReader(handle)}
    if set(metrics) != {row["sku"] for row in scope}:
        raise SystemExit("metrics and scope SKU sets differ")
    if any(row["visual_review"] != "PASS" for row in metrics.values()):
        raise SystemExit("one or more rerenders has not passed visual review")

    part_sizes = (174, 173, 173)
    parts: list[list[dict[str, str]]] = []
    start = 0
    for size in part_sizes:
        parts.append(scope[start : start + size])
        start += size

    manifest_fields = [
        "part",
        "sku",
        "filename",
        "sha256",
        "caseW",
        "bboxH",
        "cxRatio",
        "cyRatio",
        "metric_warnings",
        "visual_review",
        "repair_method",
    ]
    manifest_rows: list[dict[str, str]] = []
    for part_number, rows in enumerate(parts, 1):
        for row in rows:
            image = args.project_root / "watches-only" / row["filename"]
            metric = metrics[row["sku"]]
            manifest_rows.append(
                {
                    "part": str(part_number),
                    "sku": row["sku"],
                    "filename": row["filename"],
                    "sha256": sha256(image),
                    "caseW": metric["caseW"],
                    "bboxH": metric["bboxH"],
                    "cxRatio": metric["cxRatio"],
                    "cyRatio": metric["cyRatio"],
                    "metric_warnings": metric["metric_warnings"],
                    "visual_review": metric["visual_review"],
                    "repair_method": metric["repair_method"],
                }
            )
    manifest_path = args.output / "GemBreak-520-fixed-manifest.csv"
    with manifest_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=manifest_fields)
        writer.writeheader()
        writer.writerows(manifest_rows)

    archive_rows = []
    for part_number, rows in enumerate(parts, 1):
        archive = args.output / f"GemBreak-520-fixed-part-{part_number}-of-3.zip"
        part_manifest = args.output / f"part-{part_number}-manifest.csv"
        with part_manifest.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=manifest_fields)
            writer.writeheader()
            writer.writerows(row for row in manifest_rows if row["part"] == str(part_number))
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as bundle:
            for row in rows:
                image = args.project_root / "watches-only" / row["filename"]
                bundle.write(image, f"watches-only/{row['filename']}")
            bundle.write(manifest_path, manifest_path.name)
            bundle.write(part_manifest, part_manifest.name)
            if part_number == 3:
                qa_files = [
                    args.qa_audit,
                    args.metrics,
                    args.integrity_csv,
                    args.integrity_json,
                    args.visual_summary,
                ]
                for qa_file in qa_files:
                    bundle.write(qa_file, f"QA/{qa_file.name}")
                for sheet in sorted(args.contact_sheets.glob("*.jpg")):
                    bundle.write(sheet, f"QA/black-background-contact-sheets/{sheet.name}")
                for sheet in sorted(args.targeted_comparisons.glob("*.jpg")):
                    bundle.write(sheet, f"QA/targeted-repair-comparisons/{sheet.name}")
        archive_rows.append(
            {
                "archive": archive.name,
                "image_count": len(rows),
                "sha256": sha256(archive),
                "bytes": archive.stat().st_size,
            }
        )
    (args.output / "delivery-summary.json").write_text(
        json.dumps(
            {
                "image_total": 520,
                "archive_count": 3,
                "parts": archive_rows,
                "qa_included_in": "GemBreak-520-fixed-part-3-of-3.zip",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    print(json.dumps(archive_rows, indent=2))


if __name__ == "__main__":
    main()
