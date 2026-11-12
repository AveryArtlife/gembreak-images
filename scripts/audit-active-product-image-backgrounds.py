#!/usr/bin/env python3
"""Audit every active manifest-referenced product JPG for opaque white edges."""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


REPO = Path(__file__).resolve().parents[1]
AUDIT = REPO / "audit" / "white-background-hard-gate-2026-09-29"
NEAR_WHITE = 248


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inspect(path: Path) -> dict[str, object]:
    with Image.open(path) as opened:
        opened.load()
        mode = opened.mode
        has_alpha = "A" in opened.getbands()
        image = opened.convert("RGB")
    width, height = image.size
    patch_width = max(3, min(32, width // 20))
    patch_height = max(3, min(32, height // 20))
    pixels: list[tuple[int, int, int]] = []
    for box in (
        (0, 0, patch_width, patch_height),
        (width - patch_width, 0, width, patch_height),
        (0, height - patch_height, patch_width, height),
        (width - patch_width, height - patch_height, width, height),
    ):
        pixels.extend(image.crop(box).get_flattened_data())
    exact = sum(pixel == (255, 255, 255) for pixel in pixels) / len(pixels)
    near = sum(min(pixel) >= NEAR_WHITE for pixel in pixels) / len(pixels)
    passed = not has_alpha and near >= 0.99
    return {
        "sku": path.parent.name,
        "filename": path.name,
        "role": "final-main" if path.name == "main.jpg" else "secondary-gallery",
        "path": str(path.relative_to(REPO)),
        "width": width,
        "height": height,
        "mode": mode,
        "has_alpha": has_alpha,
        "corner_exact_white_fraction": round(exact, 6),
        "corner_near_white_fraction": round(near, 6),
        "white_background_gate": "pass" if passed else "fail",
        "sha256": sha256(path),
    }


def main() -> None:
    manifest = json.loads((REPO / "product-shots" / "manifest.json").read_text())
    manifest_paths = {
        REPO / "product-shots" / entry["sku"] / filename
        for entry in manifest
        for filename in entry["files"]
    }
    active_paths = set((REPO / "product-shots").glob("*/*.jpg"))
    if manifest_paths != active_paths:
        raise ValueError(
            f"manifest/file mismatch: manifest-only={len(manifest_paths-active_paths)}, "
            f"filesystem-only={len(active_paths-manifest_paths)}"
        )
    rows = [inspect(path) for path in sorted(active_paths)]
    failures = [row for row in rows if row["white_background_gate"] != "pass"]
    if failures:
        raise ValueError(f"active product-image white-background failures: {len(failures)}")

    AUDIT.mkdir(parents=True, exist_ok=True)
    with (AUDIT / "all-active-product-images-white-background-audit.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "manifest_skus": len(manifest),
        "active_product_images": len(rows),
        "final_main_images": sum(row["role"] == "final-main" for row in rows),
        "compliant_secondary_gallery_images": sum(
            row["role"] == "secondary-gallery" for row in rows
        ),
        "white_background_failures": len(failures),
        "manifest_matches_filesystem": True,
    }
    (AUDIT / "all-active-product-images-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
