#!/usr/bin/env python3
"""Build complete product-shots/main.jpg coverage from transparent watch assets.

Existing gallery photographs are preserved. A missing ``main.jpg`` is created from
the matching ``watches-only/<SKU>.png`` on a clean white studio canvas. The script
also regenerates the public manifest and records provenance separately so derived
fallbacks can be replaced later by a second, exact-reference gallery photograph.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


CANVAS_SIZE = 1200
SUBJECT_MAX = 1080
JPEG_QUALITY = 90


def render_main(source: Path, destination: Path) -> None:
    with Image.open(source) as raw:
        image = raw.convert("RGBA")
        alpha = image.getchannel("A")
        bbox = alpha.getbbox()
        if bbox is None:
            raise ValueError(f"transparent source has no visible pixels: {source}")
        subject = image.crop(bbox)

    scale = min(SUBJECT_MAX / subject.width, SUBJECT_MAX / subject.height)
    size = (
        max(1, round(subject.width * scale)),
        max(1, round(subject.height * scale)),
    )
    if size != subject.size:
        subject = subject.resize(size, Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), "white")
    position = (
        (CANVAS_SIZE - subject.width) // 2,
        (CANVAS_SIZE - subject.height) // 2,
    )
    canvas.alpha_composite(subject, position)

    destination.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(
        destination,
        format="JPEG",
        quality=JPEG_QUALITY,
        optimize=True,
        progressive=True,
    )


def image_file_sort_key(name: str) -> tuple[int, int, str]:
    if name == "main.jpg":
        return (0, 0, name)
    if name.startswith("angle-") and name.endswith(".jpg"):
        try:
            number = int(name[6:-4])
        except ValueError:
            number = 999
        return (1, number, name)
    if name == "box.jpg":
        return (2, 0, name)
    return (3, 0, name)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root (defaults to the parent of scripts/)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace existing main.jpg files as well as filling missing files",
    )
    parser.add_argument(
        "--force-prefix",
        action="append",
        default=[],
        help="Replace existing main images only for SKUs beginning with this prefix",
    )
    args = parser.parse_args()

    repo = args.repo.resolve()
    cutout_root = repo / "watches-only"
    product_root = repo / "product-shots"
    existing_manifest_path = product_root / "source-manifest.json"

    prior_sources: dict[str, dict[str, str]] = {}
    if existing_manifest_path.exists():
        prior = json.loads(existing_manifest_path.read_text())
        prior_sources = {entry["sku"]: entry for entry in prior}

    created = 0
    preserved = 0
    source_entries: list[dict[str, str]] = []
    for source in sorted(cutout_root.glob("*.png"), key=lambda p: p.stem):
        sku = source.stem
        destination = product_root / sku / "main.jpg"
        existed = destination.exists()
        replace_prefix = any(sku.startswith(prefix) for prefix in args.force_prefix)
        if args.force or replace_prefix or not existed:
            render_main(source, destination)
            created += 1
            origin = "watches-only-derived"
            source_path = f"watches-only/{source.name}"
        else:
            preserved += 1
            previous = prior_sources.get(sku, {})
            origin = previous.get("origin", "legacy-gallery")
            source_path = previous.get("source", "")

        source_entries.append(
            {
                "sku": sku,
                "main": f"product-shots/{sku}/main.jpg",
                "origin": origin,
                "source": source_path,
            }
        )

    manifest = []
    for directory in sorted(
        (path for path in product_root.iterdir() if path.is_dir()),
        key=lambda path: path.name,
    ):
        files = sorted(
            (path.name for path in directory.glob("*.jpg")),
            key=image_file_sort_key,
        )
        if files:
            manifest.append({"sku": directory.name, "files": files})

    (product_root / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n"
    )
    existing_manifest_path.write_text(
        json.dumps(source_entries, indent=2) + "\n"
    )

    print(
        json.dumps(
            {
                "created_or_replaced": created,
                "preserved_existing": preserved,
                "manifest_skus": len(manifest),
                "source_manifest_skus": len(source_entries),
                "generated_at": datetime.now(timezone.utc).isoformat(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
