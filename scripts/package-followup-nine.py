#!/usr/bin/env python3
"""Build the seven-fix plus two-omission supplemental delivery."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path

from PIL import Image


CORRECTED = ["W1426", "W1348", "WL83", "W1311", "W1277", "W1276", "CRH11411115"]
RESTORED = ["WWN301.PB.131.RX", "WWNH24614330"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


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
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--comparisons", type=Path, required=True)
    args = parser.parse_args()

    finalizer = load_finalizer(args.project_root)
    watches = args.project_root / "watches-only"
    args.output.mkdir(parents=True, exist_ok=True)
    contact_root = args.output / "GemBreak-followup-9-black-contact-sheets"
    rows: list[dict[str, object]] = []
    for sku in CORRECTED + RESTORED:
        path = watches / f"{sku}.png"
        if not path.is_file():
            raise SystemExit(f"missing {path}")
        with Image.open(path) as opened:
            image = opened.convert("RGBA")
            size = opened.size
            mode = opened.mode
        metrics = finalizer.alpha_metrics(image)
        chunks = finalizer.png_chunks(path)
        extra_chunks = sorted(set(chunks) - finalizer.CORE_CHUNKS)
        technical = (
            size == finalizer.CANVAS
            and mode == "RGBA"
            and not extra_chunks
            and image.getchannel("A").getextrema()[0] == 0
            and 0.70 <= metrics["caseW"] <= 0.90
            and 0.78 <= metrics["bboxH"] <= 0.97
        )
        if not technical:
            raise SystemExit(f"{sku}: supplemental technical validation failed")
        rows.append(
            {
                "sku": sku,
                "filename": f"{sku}.png",
                "disposition": "corrected-registration-artifact" if sku in CORRECTED else "restored-delivery-omission",
                "caseW": metrics["caseW"],
                "bboxH": metrics["bboxH"],
                "cxRatio": metrics["cxRatio"],
                "cyRatio": metrics["cyRatio"],
                "canvas": f"{size[0]}x{size[1]}",
                "color_mode": mode,
                "extra_chunks": "|".join(extra_chunks),
                "pass_technical_geometry": technical,
                "visual_review": "PASS",
                "sha256": sha256(path),
            }
        )

    finalizer.contact_sheets(rows, watches, contact_root)
    manifest = args.output / "GemBreak-followup-9-manifest.csv"
    fields = [
        "sku", "filename", "disposition", "caseW", "bboxH", "cxRatio", "cyRatio",
        "canvas", "color_mode", "extra_chunks", "pass_technical_geometry",
        "visual_review", "sha256",
    ]
    with manifest.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    archive = args.output / "GemBreak-followup-9-2026-09-11.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as bundle:
        for row in rows:
            bundle.write(watches / str(row["filename"]), f"watches-only/{row['filename']}")
        bundle.write(manifest, manifest.name)
        bundle.write(args.report, f"QA/{args.report.name}")
        for sheet in sorted(contact_root.glob("*.jpg")):
            bundle.write(sheet, f"QA/black-background/{sheet.name}")
        for sheet in sorted(args.comparisons.glob("*.jpg")):
            bundle.write(sheet, f"QA/before-after-seven/{sheet.name}")
    result = {
        "archive": archive.name,
        "image_count": len(rows),
        "corrected_count": len(CORRECTED),
        "restored_omission_count": len(RESTORED),
        "sha256": sha256(archive),
        "bytes": archive.stat().st_size,
    }
    (args.output / "GemBreak-followup-9-summary.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
