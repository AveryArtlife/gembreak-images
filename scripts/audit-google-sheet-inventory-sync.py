#!/usr/bin/env python3
"""Audit Google Sheet inventory identity, repository paths, and image hard gates."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from PIL import Image


REPO = Path(__file__).resolve().parents[1]
AUDIT = REPO / "audit" / "google-sheets-inventory-sync-2026-10-01"
SHEET = AUDIT / "master-inventory-snapshot.csv"
RECEIPT = AUDIT / "inventory-materialization-receipt.csv"
WATCHES = REPO / "watches-only"
PRODUCTS = REPO / "product-shots"
EXPECTED = 1555
NON_WATCH = re.compile(r"\b(perfume|fragrance|earrings?|desktop clock|table clock|wall clock|fountain pen|ballpoint pen)\b", re.I)
APPROVED_VARIATIONS = {
    "WWNM049.527.33.081.00": (
        "Approved visual variation: complete upright Mido Multifort Chronograph with full bracelet; "
        "the right-side crown and pushers make the foreground-mask centroid read left of center."
    )
}


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def image_metrics(path: Path) -> dict[str, object]:
    with Image.open(path) as opened:
        opened.load()
        fmt = opened.format
        mode = opened.mode
        image = opened.convert("RGB")
    width, height = image.size
    array = np.asarray(image, dtype=np.int16)
    chroma = array.max(axis=2) - array.min(axis=2)
    foreground = (array.min(axis=2) < 244) | (chroma > 14)
    ys, xs = np.where(foreground)
    if len(xs):
        left, right = int(xs.min()), int(xs.max() + 1)
        top, bottom = int(ys.min()), int(ys.max() + 1)
        bbox_w = (right - left) / width
        bbox_h = (bottom - top) / height
        center_x = (left + right) / 2 / width
        center_y = (top + bottom) / 2 / height
    else:
        bbox_w = bbox_h = center_x = center_y = 0.0
    patch_w = max(3, min(32, width // 20))
    patch_h = max(3, min(32, height // 20))
    patches = np.concatenate(
        (
            array[:patch_h, :patch_w].reshape(-1, 3),
            array[:patch_h, width - patch_w :].reshape(-1, 3),
            array[height - patch_h :, :patch_w].reshape(-1, 3),
            array[height - patch_h :, width - patch_w :].reshape(-1, 3),
        )
    )
    near_white = float(np.mean(np.min(patches, axis=1) >= 248))
    exact_white = float(np.mean(np.all(patches == 255, axis=1)))
    return {
        "format": fmt,
        "mode": mode,
        "width": width,
        "height": height,
        "bbox_width_ratio": round(bbox_w, 6),
        "bbox_height_ratio": round(bbox_h, 6),
        "center_x": round(center_x, 6),
        "center_y": round(center_y, 6),
        "corner_near_white_fraction": round(near_white, 6),
        "corner_exact_white_fraction": round(exact_white, 6),
    }


def main() -> None:
    rows = load_csv(SHEET)
    receipt = load_csv(RECEIPT)
    if len(rows) != EXPECTED or len({row["sku"] for row in rows}) != EXPECTED:
        raise SystemExit("Sheet snapshot is not exactly 1,555 unique SKUs")
    receipt_by_sku = {row["sku"]: row for row in receipt}
    if set(receipt_by_sku) != {row["sku"] for row in rows}:
        raise SystemExit("Materialization receipt does not match sheet SKU set")

    manifest = json.loads((PRODUCTS / "manifest.json").read_text(encoding="utf-8"))
    manifest_by_sku = {entry["sku"]: entry for entry in manifest}
    source_manifest = json.loads((PRODUCTS / "source-manifest.json").read_text(encoding="utf-8"))
    source_by_sku = {entry["sku"]: entry for entry in source_manifest}

    records: list[dict[str, object]] = []
    hash_groups: dict[str, list[str]] = defaultdict(list)
    for number, row in enumerate(rows, start=1):
        sku = row["sku"]
        png = WATCHES / f"{sku}.png"
        jpg = PRODUCTS / sku / "main.jpg"
        if not png.is_file() or not jpg.is_file():
            raise FileNotFoundError(f"Incomplete exact SKU files: {sku}")
        png_metrics = image_metrics(png)
        jpg_metrics = image_metrics(jpg)
        png_hash = sha256(png)
        hash_groups[png_hash].append(sku)
        expected_url = (
            "https://raw.githubusercontent.com/AveryArtlife/"
            f"gembreak-images/main/watches-only/{sku}.png"
        )
        title_is_watch = not bool(NON_WATCH.search(f"{row['brand']} {row['model']}"))
        image_hard_pass = (
            png_metrics["format"] == "PNG"
            and png_metrics["corner_near_white_fraction"] >= 0.99
            and png_metrics["bbox_height_ratio"] >= 0.70
            and abs(float(png_metrics["center_x"]) - 0.5) <= 0.08
            and abs(float(png_metrics["center_y"]) - 0.5) <= 0.08
            and jpg_metrics["format"] == "JPEG"
            and (jpg_metrics["width"], jpg_metrics["height"]) == (1200, 1200)
            and jpg_metrics["corner_near_white_fraction"] >= 0.99
        )
        image_gate = "pass" if image_hard_pass else (
            "acceptable_variation" if sku in APPROVED_VARIATIONS else "review"
        )
        identity_gate = (
            png.stem == sku
            and jpg.parent.name == sku
            and sku in manifest_by_sku
            and sku in source_by_sku
            and title_is_watch
            and receipt_by_sku[sku]["alias_evidence"] in {
                "exact-existing",
                "v2-exact",
                "sheet-url-exact",
                "brand-prefix-exact",
            }
        )
        records.append(
            {
                "sheet_row": int(row["sheet_row"]),
                "sku": sku,
                "brand": row["brand"],
                "model": row["model"],
                "identity_evidence": receipt_by_sku[sku]["alias_evidence"],
                "alias_source": receipt_by_sku[sku]["alias_source"],
                "exact_png_path": str(png.relative_to(REPO)),
                "exact_product_path": str(jpg.relative_to(REPO)),
                "expected_image_url": expected_url,
                "sheet_image_url_before_sync": row["image_url"],
                "identity_gate": "pass" if identity_gate else "fail",
                "image_gate": image_gate,
                "visual_note": APPROVED_VARIATIONS.get(sku, ""),
                "title_is_wristwatch": title_is_watch,
                "png_sha256": png_hash,
                "png_width": png_metrics["width"],
                "png_height": png_metrics["height"],
                "png_corner_near_white": png_metrics["corner_near_white_fraction"],
                "png_bbox_width_ratio": png_metrics["bbox_width_ratio"],
                "png_bbox_height_ratio": png_metrics["bbox_height_ratio"],
                "png_center_x": png_metrics["center_x"],
                "png_center_y": png_metrics["center_y"],
                "jpg_width": jpg_metrics["width"],
                "jpg_height": jpg_metrics["height"],
                "jpg_corner_near_white": jpg_metrics["corner_near_white_fraction"],
            }
        )
        if number % 200 == 0:
            print(f"audited {number}/{EXPECTED}")

    brands_by_hash: dict[str, set[str]] = defaultdict(set)
    models_by_hash: dict[str, set[str]] = defaultdict(set)
    for record in records:
        brands_by_hash[str(record["png_sha256"])].add(str(record["brand"]).casefold())
        models_by_hash[str(record["png_sha256"])].add(str(record["model"]).casefold())
    conflicting_brand_hashes = {
        digest: skus for digest, skus in hash_groups.items() if len(brands_by_hash[digest]) > 1
    }

    AUDIT.mkdir(parents=True, exist_ok=True)
    with (AUDIT / "inventory-image-sync-audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)

    dimensions = Counter((int(r["png_width"]), int(r["png_height"])) for r in records)
    review_rows = [r for r in records if r["image_gate"] == "review"]
    summary = {
        "spreadsheet_id": "1jio2i6Xpn5gMIqgreTuNOrJ76IGUbT7aDh7FMFqwRrY",
        "sheet": "Master Inventory",
        "range": "A3:I1557",
        "inventory_rows": len(rows),
        "unique_skus": len({row["sku"] for row in rows}),
        "exact_png_paths": sum((WATCHES / f"{row['sku']}.png").is_file() for row in rows),
        "exact_product_mains": sum((PRODUCTS / row["sku"] / "main.jpg").is_file() for row in rows),
        "manifest_entries": sum(row["sku"] in manifest_by_sku for row in rows),
        "source_manifest_entries": sum(row["sku"] in source_by_sku for row in rows),
        "identity_gate_pass": sum(r["identity_gate"] == "pass" for r in records),
        "identity_gate_fail": sum(r["identity_gate"] != "pass" for r in records),
        "wristwatch_titles": sum(bool(r["title_is_wristwatch"]) for r in records),
        "non_watch_titles": sum(not bool(r["title_is_wristwatch"]) for r in records),
        "image_hard_gate_pass": sum(r["image_gate"] == "pass" for r in records),
        "image_acceptable_variation": sum(r["image_gate"] == "acceptable_variation" for r in records),
        "image_hard_gate_review": len(review_rows),
        "conflicting_brand_duplicate_hashes": len(conflicting_brand_hashes),
        "duplicate_hash_groups": sum(len(skus) > 1 for skus in hash_groups.values()),
        "png_dimensions": {f"{w}x{h}": count for (w, h), count in dimensions.most_common()},
        "sheet_image_urls_before_sync_present": sum(bool(row["image_url"]) for row in rows),
        "sheet_image_urls_before_sync_blank": sum(not bool(row["image_url"]) for row in rows),
        "sheet_image_urls_planned_exact": len(rows),
    }
    (AUDIT / "inventory-image-sync-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    with (AUDIT / "image-hard-gate-review.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(review_rows)
    (AUDIT / "conflicting-brand-duplicate-hashes.json").write_text(
        json.dumps(conflicting_brand_hashes, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
