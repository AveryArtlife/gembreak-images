#!/usr/bin/env python3
"""Atomically install only approved rerenders and prove protected files unchanged."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import tempfile
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
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--rerender-metrics", type=Path, required=True)
    parser.add_argument("--qa-audit", type=Path, required=True)
    parser.add_argument("--integrity-csv", type=Path, required=True)
    parser.add_argument("--integrity-json", type=Path, required=True)
    parser.add_argument("--visual-summary", type=Path, required=True)
    parser.add_argument("--install", action="store_true")
    args = parser.parse_args()

    watches = args.project_root / "watches-only"
    with args.scope_lock.open(newline="") as handle:
        scope = list(csv.DictReader(handle))
    allowed = [row for row in scope if row["allowed_to_change"].lower() == "true"]
    protected = [row for row in scope if row["allowed_to_change"].lower() != "true"]
    if len(scope) != 2456 or len(allowed) != 520 or len(protected) != 1936:
        raise SystemExit(
            f"unexpected scope counts: total={len(scope)} allowed={len(allowed)} "
            f"protected={len(protected)}"
        )

    missing_repo = [row["filename"] for row in scope if not (watches / row["filename"]).is_file()]
    missing_candidates = [
        row["filename"] for row in allowed if not (args.candidates / row["filename"]).is_file()
    ]
    extra_candidates = sorted(
        path.name for path in args.candidates.glob("*.png")
        if path.name not in {row["filename"] for row in allowed}
    )
    changed_protected_before = [
        row["filename"]
        for row in protected
        if sha256(watches / row["filename"]) != row["sha256_before"]
    ]
    if missing_repo or missing_candidates or extra_candidates or changed_protected_before:
        raise SystemExit(
            json.dumps(
                {
                    "missing_repo": missing_repo,
                    "missing_candidates": missing_candidates,
                    "extra_candidates": extra_candidates,
                    "changed_protected_before": changed_protected_before,
                },
                indent=2,
            )
        )

    if not args.install:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "scope_total": len(scope),
                    "approved_to_replace": len(allowed),
                    "protected_verified_unchanged": len(protected),
                    "candidate_set_exact": True,
                },
                indent=2,
            )
        )
        return

    for row in allowed:
        source = args.candidates / row["filename"]
        target = watches / row["filename"]
        descriptor, temporary = tempfile.mkstemp(prefix=f".{target.stem}.", suffix=".png", dir=target.parent)
        os.close(descriptor)
        temporary_path = Path(temporary)
        try:
            shutil.copyfile(source, temporary_path)
            if sha256(temporary_path) != sha256(source):
                raise RuntimeError(f"temporary copy hash mismatch for {row['filename']}")
            os.replace(temporary_path, target)
        finally:
            temporary_path.unlink(missing_ok=True)

    integrity_rows: list[dict[str, str]] = []
    failures: list[str] = []
    for row in scope:
        path = watches / row["filename"]
        after = sha256(path)
        mutable = row["allowed_to_change"].lower() == "true"
        candidate_hash = sha256(args.candidates / row["filename"]) if mutable else ""
        verified = after == candidate_hash if mutable else after == row["sha256_before"]
        if not verified:
            failures.append(row["filename"])
        integrity_rows.append(
            {
                "sku": row["sku"],
                "filename": row["filename"],
                "human_classification": row["human_classification"],
                "allowed_to_change": row["allowed_to_change"],
                "sha256_before": row["sha256_before"],
                "sha256_after": after,
                "candidate_sha256": candidate_hash,
                "verification": "candidate-match" if mutable and verified else (
                    "protected-unchanged" if verified else "FAIL"
                ),
            }
        )
    if failures:
        raise SystemExit(f"post-install integrity failures: {', '.join(failures)}")

    args.integrity_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.integrity_csv.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(integrity_rows[0]))
        writer.writeheader()
        writer.writerows(integrity_rows)

    with args.rerender_metrics.open(newline="") as handle:
        rerender_rows = list(csv.DictReader(handle))
    rerender_by_sku = {row["sku"]: row for row in rerender_rows}
    with args.qa_audit.open(newline="") as handle:
        reader = csv.DictReader(handle)
        qa_rows = list(reader)
        qa_fields = list(reader.fieldnames or [])
    added_fields = [
        "remediation_status",
        "post_remediation_needs_rerender",
        "post_caseW",
        "post_bboxH",
        "post_cxRatio",
        "post_cyRatio",
        "post_canvas",
        "post_color_mode",
        "post_metric_warnings",
        "post_visual_review",
        "post_sha256",
    ]
    for field in added_fields:
        if field not in qa_fields:
            qa_fields.append(field)
    scope_by_sku = {row["sku"]: row for row in integrity_rows}
    for row in qa_rows:
        rerender = rerender_by_sku.get(row["sku"])
        integrity = scope_by_sku[row["sku"]]
        if rerender:
            row.update(
                {
                    "remediation_status": "rerendered-and-approved",
                    "post_remediation_needs_rerender": "False",
                    "post_caseW": rerender["caseW"],
                    "post_bboxH": rerender["bboxH"],
                    "post_cxRatio": rerender["cxRatio"],
                    "post_cyRatio": rerender["cyRatio"],
                    "post_canvas": rerender["canvas"],
                    "post_color_mode": rerender["color_mode"],
                    "post_metric_warnings": rerender["metric_warnings"],
                    "post_visual_review": rerender["visual_review"],
                    "post_sha256": integrity["sha256_after"],
                }
            )
        else:
            row.update(
                {
                    "remediation_status": "unchanged-protected",
                    "post_remediation_needs_rerender": row["needs_rerender"],
                    "post_caseW": row["caseW"],
                    "post_bboxH": row["bboxH"],
                    "post_cxRatio": row["cxRatio"],
                    "post_cyRatio": row["cyRatio"],
                    "post_canvas": row["canvas"],
                    "post_color_mode": row["color_mode"],
                    "post_metric_warnings": row["metric_warnings"],
                    "post_visual_review": row["human_classification"],
                    "post_sha256": integrity["sha256_after"],
                }
            )
    with args.qa_audit.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=qa_fields)
        writer.writeheader()
        writer.writerows(qa_rows)

    result = {
        "inventory_total": len(scope),
        "installed_candidate_matches": len(allowed),
        "protected_unchanged": len(protected),
        "scope_integrity_failures": 0,
        "qa_rows": len(qa_rows),
        "repository_updated": True,
    }
    args.integrity_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    visual = json.loads(args.visual_summary.read_text())
    visual["repository_updated"] = True
    visual["protected_hashes_verified_after_install"] = len(protected)
    visual["installed_candidate_matches"] = len(allowed)
    args.visual_summary.write_text(json.dumps(visual, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
