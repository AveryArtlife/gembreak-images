#!/usr/bin/env python3
"""Read-only GemBreak audit: metrics are warnings; visual defects drive rerenders."""

from __future__ import annotations

import argparse
import csv
import json
import math
import struct
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


REPO = Path(__file__).resolve().parents[1]
WATCHES = REPO / "watches-only"
EXPECTED_SIZE = (1024, 1536)
CASE_RANGE = (0.73, 0.83)
BBOX_HEIGHT_RANGE = (0.85, 0.95)
CENTER_RANGE = (0.47, 0.53)
ALPHA_THRESHOLD = 32
CORE_CHUNKS = {"IHDR", "IDAT", "IEND"}
ANCHORS = {
    "WWNM126710BLRO-0002",
    "CR215.30.44.21.01.002",
    "WWNA17375211B1S1",
    "CRT127.407.11.041.01",
    "WWNL3.374.4.90.2",
}


def repository_sku(sku: str) -> str:
    return sku.replace("/", "-")


def read_inventory(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or "SKU" not in rows[0]:
        raise ValueError(f"Inventory must contain a SKU column: {path}")
    for row in rows:
        row["SKU"] = (row.get("SKU") or "").strip()
    counts = Counter(row["SKU"] for row in rows)
    if "" in counts:
        raise ValueError("Inventory contains a blank SKU")
    duplicates = sorted(sku for sku, count in counts.items() if count > 1)
    if duplicates:
        raise ValueError(f"Duplicate inventory SKUs: {duplicates[:20]}")
    return rows


def png_chunks(path: Path) -> list[str]:
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return []
    names: list[str] = []
    offset = 8
    while offset + 12 <= len(data):
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        name = data[offset + 4 : offset + 8].decode("ascii", "replace")
        names.append(name)
        offset += length + 12
        if name == "IEND":
            break
    return names


def metrics(image: Image.Image) -> dict[str, float | tuple[int, int, int, int]]:
    rgba = np.asarray(image.convert("RGBA"))
    mask = rgba[:, :, 3] > ALPHA_THRESHOLD
    ys, xs = np.where(mask)
    if not len(xs):
        return {
            "caseW": 0.0,
            "bboxH": 0.0,
            "cxRatio": 0.0,
            "cyRatio": 0.0,
            "bbox": (0, 0, 0, 0),
        }
    bbox = (int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1))
    row_widths = []
    for row in mask:
        xx = np.flatnonzero(row)
        row_widths.append(int(xx[-1] - xx[0] + 1) if len(xx) else 0)
    return {
        "caseW": max(row_widths) / image.width,
        "bboxH": (bbox[3] - bbox[1]) / image.height,
        "cxRatio": ((bbox[0] + bbox[2]) / 2) / image.width,
        "cyRatio": ((bbox[1] + bbox[3]) / 2) / image.height,
        "bbox": bbox,
    }


def geometry_failures(path: Path, opened: Image.Image, measured: dict[str, object]) -> list[str]:
    failures: list[str] = []
    if opened.format != "PNG":
        failures.append("not-png")
    if opened.size != EXPECTED_SIZE:
        failures.append("canvas")
    if opened.mode != "RGBA":
        failures.append("color-mode")
    if opened.info:
        failures.append("metadata")
    unexpected = sorted(set(png_chunks(path)) - CORE_CHUNKS)
    if unexpected:
        failures.append("extra-png-chunks")
    alpha = np.asarray(opened.convert("RGBA").getchannel("A"))
    if alpha.size == 0 or int(alpha.min()) != 0:
        failures.append("background-not-transparent")
    if alpha.size == 0 or int(alpha.max()) != 255:
        failures.append("subject-not-opaque")
    case_width = float(measured["caseW"])
    bbox_height = float(measured["bboxH"])
    centre_x = float(measured["cxRatio"])
    centre_y = float(measured["cyRatio"])
    if case_width < CASE_RANGE[0]:
        failures.append("caseW-low")
    elif case_width > CASE_RANGE[1]:
        failures.append("caseW-high")
    if bbox_height < BBOX_HEIGHT_RANGE[0]:
        failures.append("bboxH-low")
    elif bbox_height > BBOX_HEIGHT_RANGE[1]:
        failures.append("bboxH-high")
    if not CENTER_RANGE[0] <= centre_x <= CENTER_RANGE[1]:
        failures.append("case-centre-x")
    if not CENTER_RANGE[0] <= centre_y <= CENTER_RANGE[1]:
        failures.append("case-centre-y")
    return failures


def historical_content_reviews(original_csv: Path, new_json: Path, pack_json: Path) -> dict[str, str]:
    coverage: dict[str, str] = {}
    with original_csv.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            coverage[row["sku"]] = "legacy catalog black-background review"
    with new_json.open(encoding="utf-8") as handle:
        for row in json.load(handle)["records"]:
            coverage[row["sku"]] = "424-watch black-background review"
    with pack_json.open(encoding="utf-8") as handle:
        for row in json.load(handle)["records"]:
            coverage[row["original_sku"]] = "544-watch individual black-background review"
    return coverage


def read_content_overrides(path: Path | None) -> dict[str, dict[str, str]]:
    if path is None:
        return {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    required = {"sku", "pass_content", "notes"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError(f"Content override CSV needs {sorted(required)}: {path}")
    return {row["sku"].strip(): row for row in rows}


def make_sheets(rows: list[dict[str, object]], output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default()
    tile_w, tile_h = 360, 500
    cols, page_size = 4, 16
    for page_index in range(math.ceil(len(rows) / page_size)):
        page_rows = rows[page_index * page_size : (page_index + 1) * page_size]
        sheet = Image.new("RGB", (tile_w * cols, tile_h * 4), "black")
        draw = ImageDraw.Draw(sheet)
        for index, row in enumerate(page_rows):
            x = index % cols * tile_w
            y = index // cols * tile_h
            path = WATCHES / f"{row['file_sku']}.png"
            with Image.open(path) as opened:
                image = opened.convert("RGBA")
            image.thumbnail((tile_w - 20, tile_h - 62), Image.Resampling.LANCZOS)
            tile = Image.new("RGBA", (tile_w, tile_h), (0, 0, 0, 255))
            tile.alpha_composite(image, ((tile_w - image.width) // 2, 4))
            sheet.paste(tile.convert("RGB"), (x, y))
            draw.text((x + 8, y + tile_h - 52), str(row["sku"]), font=font, fill=(120, 255, 150))
            draw.text(
                (x + 8, y + tile_h - 32),
                f"caseW {row['caseW']:.3f} | bboxH {row['bboxH']:.3f}",
                font=font,
                fill=(120, 255, 150),
            )
        sheet.save(output / f"all-watches-{page_index + 1:03d}.jpg", quality=94, subsampling=0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-count", type=int, default=2456)
    parser.add_argument("--content-overrides", type=Path)
    parser.add_argument("--skip-sheets", action="store_true")
    parser.add_argument(
        "--original-review",
        type=Path,
        default=Path("/Users/averyandon/Documents/Codex/2026-09-03/i-need-you-to-edit-and/work/new-watches/original-black-background-stress-report.csv"),
    )
    parser.add_argument(
        "--new-review",
        type=Path,
        default=Path("/Users/averyandon/Documents/Codex/2026-09-03/i-need-you-to-edit-and/work/new-watches/strict-qa-final.json"),
    )
    parser.add_argument(
        "--pack-review",
        type=Path,
        default=Path("/Users/averyandon/Documents/Codex/2026-09-10/higgsfield-plugin-app-6a3293e129088191abf0875820e839da-openai-curated/work/gembreak-2500pack/manual-black-background-review.json"),
    )
    args = parser.parse_args()

    inventory = read_inventory(args.inventory.resolve())
    if len(inventory) != args.expected_count:
        raise ValueError(f"Expected {args.expected_count} rows, found {len(inventory)}")
    prior_reviews = historical_content_reviews(args.original_review, args.new_review, args.pack_review)
    overrides = read_content_overrides(args.content_overrides)
    inventory_skus = {row["SKU"] for row in inventory}
    unknown_overrides = sorted(set(overrides) - inventory_skus)
    if unknown_overrides:
        raise ValueError(f"Content overrides not present in inventory: {unknown_overrides[:20]}")
    missing_coverage = sorted(row["SKU"] for row in inventory if row["SKU"] not in prior_reviews)
    if missing_coverage:
        raise ValueError(f"Inventory SKUs without prior content review: {missing_coverage[:20]}")

    records: list[dict[str, object]] = []
    for inventory_row in inventory:
        sku = inventory_row["SKU"]
        file_sku = repository_sku(sku)
        path = WATCHES / f"{file_sku}.png"
        if not path.is_file():
            raise FileNotFoundError(path)
        with Image.open(path) as opened:
            measured = metrics(opened)
            failures = geometry_failures(path, opened, measured)
            canvas = f"{opened.width}x{opened.height}"
            color_mode = opened.mode
        chunks = png_chunks(path)
        extra_chunks = sorted(set(chunks) - CORE_CHUNKS)
        override = overrides.get(sku)
        if override:
            pass_content = override["pass_content"].strip().lower() in {"1", "true", "pass", "yes"}
            content_note = override["notes"].strip()
        else:
            pass_content = True
            content_note = f"PASS_CONTENT from {prior_reviews[sku]}; pending v2 candidate recheck" if not failures else f"PASS_CONTENT from {prior_reviews[sku]}"
        pass_geometry = not failures
        if not pass_content:
            human_classification = "true failure"
        elif failures:
            human_classification = "acceptable variation"
        else:
            human_classification = "approved"
        # Numeric thresholds are intentionally warnings only. A watch enters the
        # rerender list only after a human visual review confirms a true defect.
        needs_rerender = human_classification == "true failure"
        notes = "; ".join(filter(None, [",".join(failures), content_note]))
        records.append(
            {
                "sku": sku,
                "file_sku": file_sku,
                "caseW": round(float(measured["caseW"]), 6),
                "bboxH": round(float(measured["bboxH"]), 6),
                "cxRatio": round(float(measured["cxRatio"]), 6),
                "cyRatio": round(float(measured["cyRatio"]), 6),
                "canvas": canvas,
                "color_mode": color_mode,
                "extra_chunks": "|".join(extra_chunks),
                "metric_warnings": "|".join(failures),
                "pass_geometry": pass_geometry,
                "pass_content": pass_content,
                "human_classification": human_classification,
                "needs_rerender": needs_rerender,
                "notes": notes,
            }
        )

    args.output.mkdir(parents=True, exist_ok=True)
    with (args.output / "qa_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "sku", "caseW", "bboxH", "cxRatio", "cyRatio", "canvas",
                "color_mode", "extra_chunks", "metric_warnings", "pass_geometry",
                "pass_content", "human_classification", "needs_rerender", "notes",
            ],
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(records)
    if not args.skip_sheets:
        make_sheets(records, args.output / "all-watch-black-contact-sheets")

    with (args.output / "true-failure-list.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["sku", "human_classification", "needs_rerender", "notes"],
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(record for record in records if record["human_classification"] == "true failure")

    anchor_failures = [record for record in records if record["sku"] in ANCHORS and record["needs_rerender"]]
    if anchor_failures:
        raise ValueError(f"Protected visual anchors failed: {[row['sku'] for row in anchor_failures]}")
    geometry_pass_count = sum(bool(row["pass_geometry"]) for row in records)
    print(f"rows={len(records)} geometry_pass={geometry_pass_count} geometry_warning={len(records)-geometry_pass_count}")
    print(f"content_fail={sum(not row['pass_content'] for row in records)} needs_rerender={sum(row['needs_rerender'] for row in records)}")
    print(f"protected_anchors={len(ANCHORS)} status=pass output={args.output.resolve()}")


if __name__ == "__main__":
    main()
