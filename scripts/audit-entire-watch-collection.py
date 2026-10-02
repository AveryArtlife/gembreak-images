#!/usr/bin/env python3
"""Read-only technical and scale audit for watch cutouts/product mains.

By default the script audits every PNG in ``watches-only``.  When an inventory
CSV is supplied, its unique SKU column becomes the authoritative scope and the
script also reports missing inventory files and repository extras.
"""

from __future__ import annotations

import csv
import argparse
import hashlib
import json
import math
import struct
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


REPO = Path(__file__).resolve().parents[1]
WATCHES = REPO / "watches-only"
PRODUCTS = REPO / "product-shots"
DEFAULT_OUT = REPO / "audit/collection-wide-2026-09-11"
EXPECTED_CUTOUT_SIZE = (1024, 1536)
EXPECTED_MAIN_SIZE = (1200, 1200)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def read_inventory(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or "SKU" not in rows[0]:
        raise ValueError(f"Inventory must contain a SKU column: {path}")
    for row in rows:
        row["SKU"] = (row.get("SKU") or "").strip()
    blank = [index for index, row in enumerate(rows, 2) if not row["SKU"]]
    if blank:
        raise ValueError(f"Blank inventory SKU rows: {blank[:20]}")
    counts = Counter(row["SKU"] for row in rows)
    duplicates = sorted(sku for sku, count in counts.items() if count > 1)
    if duplicates:
        raise ValueError(f"Duplicate inventory SKUs: {duplicates[:20]}")
    return rows


def repository_sku(sku: str) -> str:
    """Map sheet SKUs to filesystem-safe names used by the repository."""
    return sku.replace("/", "-")


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


def span_metrics(mask: np.ndarray) -> tuple[int, int]:
    row_widths = []
    for row in mask:
        xs = np.flatnonzero(row)
        if len(xs):
            row_widths.append(int(xs[-1] - xs[0] + 1))
    column_heights = []
    for column in mask.T:
        ys = np.flatnonzero(column)
        if len(ys):
            column_heights.append(int(ys[-1] - ys[0] + 1))
    return max(row_widths, default=0), max(column_heights, default=0)


def inspect_cutout(path: Path) -> dict[str, object]:
    with Image.open(path) as opened:
        fmt, mode, size = opened.format, opened.mode, opened.size
        metadata = sorted(opened.info)
        rgba = np.asarray(opened.convert("RGBA"))
    alpha = rgba[:, :, 3]
    mask = alpha > 32
    ys, xs = np.where(mask)
    if len(xs):
        bbox = [int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)]
        bbox_width = bbox[2] - bbox[0]
        bbox_height = bbox[3] - bbox[1]
        center_x = (bbox[0] + bbox[2]) / 2 / size[0]
        center_y = (bbox[1] + bbox[3]) / 2 / size[1]
    else:
        bbox = [0, 0, 0, 0]
        bbox_width = bbox_height = 0
        center_x = center_y = 0.0
    max_row_width, max_column_height = span_metrics(mask)
    count, _, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    areas = sorted((int(stats[i, cv2.CC_STAT_AREA]) for i in range(1, count)), reverse=True)
    components = sum(area >= 16 for area in areas)
    largest_ratio = areas[0] / max(1, sum(areas)) if areas else 0.0
    chunks = png_chunks(path)
    unexpected_chunks = sorted(set(chunks) - {"IHDR", "IDAT", "IEND"})

    format_failures: list[str] = []
    if fmt != "PNG": format_failures.append("not-png")
    if mode != "RGBA": format_failures.append("not-rgba")
    if size != EXPECTED_CUTOUT_SIZE: format_failures.append("wrong-canvas-size")
    if int(alpha.min()) != 0: format_failures.append("no-transparent-background")
    if int(alpha.max()) != 255: format_failures.append("no-fully-opaque-subject")
    if metadata: format_failures.append("embedded-metadata")
    if unexpected_chunks: format_failures.append("non-core-png-chunks")
    if not len(xs): format_failures.append("empty-alpha")
    if components > 1 and largest_ratio < 0.999:
        format_failures.append("detached-alpha-components")

    width_ratio = max_row_width / size[0]
    height_ratio = bbox_height / size[1]
    bbox_width_ratio = bbox_width / size[0]
    opaque_area_ratio = int(mask.sum()) / (size[0] * size[1])
    scale_reasons: list[str] = []
    # The widest visible row approximates the watch case/head.  The previously
    # rejected full-strap Hamilton measured 0.375; the accepted house framing is
    # 0.854.  0.58 catches genuinely small presentations while retaining normal
    # narrow dress-watch variation for visual review.
    if width_ratio < 0.58: scale_reasons.append("watch-head-too-narrow")
    if height_ratio < 0.72: scale_reasons.append("subject-too-short")
    if opaque_area_ratio < 0.11: scale_reasons.append("foreground-area-too-small")
    severe = width_ratio < 0.45 or height_ratio < 0.58 or opaque_area_ratio < 0.065
    edge_touching = min(bbox[0], bbox[1], size[0] - bbox[2], size[1] - bbox[3]) <= 1 if len(xs) else False

    return {
        "sku": path.stem,
        "path": str(path.relative_to(REPO)),
        "sha256": sha256(path),
        "format": fmt,
        "mode": mode,
        "width": size[0],
        "height": size[1],
        "alpha_min": int(alpha.min()),
        "alpha_max": int(alpha.max()),
        "metadata_keys": metadata,
        "png_chunks": chunks,
        "unexpected_png_chunks": unexpected_chunks,
        "alpha_bbox": bbox,
        "bbox_width_ratio": round(bbox_width_ratio, 6),
        "bbox_height_ratio": round(height_ratio, 6),
        "max_row_width_ratio": round(width_ratio, 6),
        "max_column_height_ratio": round(max_column_height / size[1], 6),
        "opaque_area_ratio": round(opaque_area_ratio, 6),
        "center_x": round(center_x, 6),
        "center_y": round(center_y, 6),
        "center_offset_x": round(abs(center_x - 0.5), 6),
        "center_offset_y": round(abs(center_y - 0.5), 6),
        "connected_components_16px": components,
        "largest_component_ratio": round(largest_ratio, 6),
        "edge_touching": edge_touching,
        "format_status": "pass" if not format_failures else "fail",
        "format_failures": format_failures,
        "scale_status": "risk" if scale_reasons else "pass",
        "scale_reasons": scale_reasons,
        "severe_scale_risk": severe,
    }


def inspect_product_main(sku: str) -> dict[str, object]:
    path = PRODUCTS / sku / "main.jpg"
    if not path.is_file():
        return {"exists": False, "format_status": "fail", "failures": ["missing-product-main"]}
    with Image.open(path) as opened:
        fmt, mode, size = opened.format, opened.mode, opened.size
    failures = []
    if fmt != "JPEG": failures.append("not-jpeg")
    if mode != "RGB": failures.append("not-rgb")
    if size != EXPECTED_MAIN_SIZE: failures.append("wrong-main-size")
    return {
        "exists": True,
        "path": str(path.relative_to(REPO)),
        "sha256": sha256(path),
        "format": fmt,
        "mode": mode,
        "width": size[0],
        "height": size[1],
        "format_status": "pass" if not failures else "fail",
        "failures": failures,
    }


def contact_sheet(records: list[dict[str, object]], destination: Path, cols: int, rows: int) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    cell_w, cell_h, label_h = 360, 500, 68
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), "black")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=16)
    for local, record in enumerate(records):
        row, col = divmod(local, cols)
        x, y = col * cell_w, row * cell_h
        with Image.open(REPO / str(record["path"])) as opened:
            rgba = opened.convert("RGBA")
        rgba.thumbnail((cell_w - 18, cell_h - label_h - 18), Image.Resampling.LANCZOS)
        background = Image.new("RGBA", rgba.size, (0, 0, 0, 255))
        background.alpha_composite(rgba)
        sheet.paste(background.convert("RGB"), (x + (cell_w - rgba.width) // 2, y + 5 + (cell_h - label_h - rgba.height) // 2))
        color = "#ff6b6b" if record["scale_status"] == "risk" else ("#ffcc66" if record["format_status"] == "fail" else "white")
        draw.text((x + 7, y + cell_h - label_h + 4), str(record["sku"])[:38], fill=color, font=font)
        draw.text(
            (x + 7, y + cell_h - label_h + 27),
            f"caseW {record['max_row_width_ratio']:.3f} | bboxH {record['bbox_height_ratio']:.3f}",
            fill=color,
            font=font,
        )
        draw.rectangle((x, y, x + cell_w - 1, y + cell_h - 1), outline="#4d4d4d", width=1)
    sheet.save(destination, "JPEG", quality=92, optimize=True)


def write_sheets(records: list[dict[str, object]], directory: Path, prefix: str, cols: int = 5, rows: int = 4) -> int:
    directory.mkdir(parents=True, exist_ok=True)
    per_sheet = cols * rows
    for number, start in enumerate(range(0, len(records), per_sheet), 1):
        contact_sheet(records[start : start + per_sheet], directory / f"{prefix}-{number:03d}.jpg", cols, rows)
    return math.ceil(len(records) / per_sheet)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory-csv", type=Path)
    parser.add_argument("--expected-count", type=int)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out = args.output.resolve()
    all_sheets = out / "all-black-contact-sheets"
    risk_sheets = out / "scale-risk-black-contact-sheets"
    repo_paths = sorted(WATCHES.glob("*.png"), key=lambda path: path.name.casefold())
    repo_by_sku = {path.stem: path for path in repo_paths}
    inventory_rows: list[dict[str, str]] = []
    missing_skus: list[str] = []
    extra_paths: list[Path] = []
    if args.inventory_csv:
        inventory_rows = read_inventory(args.inventory_csv)
        if args.expected_count is not None and len(inventory_rows) != args.expected_count:
            raise ValueError(f"Expected {args.expected_count} inventory rows; found {len(inventory_rows)}")
        inventory_skus = [row["SKU"] for row in inventory_rows]
        repository_skus = [repository_sku(sku) for sku in inventory_skus]
        repository_set = set(repository_skus)
        if len(repository_set) != len(repository_skus):
            raise ValueError("Inventory SKUs collide after filesystem-safe normalization")
        paths = [repo_by_sku[sku] for sku in repository_skus if sku in repo_by_sku]
        missing_skus = [sku for sku in inventory_skus if repository_sku(sku) not in repo_by_sku]
        extra_paths = [path for path in repo_paths if path.stem not in repository_set]
        inventory_by_repo_sku = {repository_sku(row["SKU"]): row for row in inventory_rows}
    else:
        paths = repo_paths
        inventory_by_repo_sku = {}

    records: list[dict[str, object]] = []
    for number, path in enumerate(paths, 1):
        cutout = inspect_cutout(path)
        cutout["product_main"] = inspect_product_main(path.stem)
        source_row = inventory_by_repo_sku.get(path.stem, {})
        cutout["file_sku"] = path.stem
        cutout["sku"] = source_row.get("SKU", path.stem)
        cutout["brand"] = source_row.get("Brand", "")
        cutout["model"] = source_row.get("Model / Name", "")
        cutout["distributor"] = source_row.get("Distributor", "")
        records.append(cutout)
        if number % 250 == 0:
            print(f"inspected {number}/{len(paths)}")

    format_failures = [r for r in records if r["format_status"] == "fail" or r["product_main"]["format_status"] == "fail"]
    risks = sorted(
        (r for r in records if r["scale_status"] == "risk"),
        key=lambda r: (r["max_row_width_ratio"], r["bbox_height_ratio"], r["sku"]),
    )
    severe = [r for r in risks if r["severe_scale_risk"]]
    corrective = [
        r for r in records
        if r["format_status"] == "fail"
        or r["product_main"]["format_status"] == "fail"
        or r["scale_status"] == "risk"
    ]
    corrective_skus = {r["sku"] for r in corrective}
    format_skus = {r["sku"] for r in format_failures}
    scale_skus = {r["sku"] for r in risks}
    dimensions = Counter((r["width"], r["height"]) for r in records)
    width_values = np.array([r["max_row_width_ratio"] for r in records], dtype=float)
    area_values = np.array([r["opaque_area_ratio"] for r in records], dtype=float)

    out.mkdir(parents=True, exist_ok=True)
    all_sheet_count = write_sheets(records, all_sheets, "all")
    risk_sheet_count = write_sheets(risks, risk_sheets, "risk", cols=4, rows=4)
    summary = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "repository": str(REPO),
        "scope": "inventory-csv" if args.inventory_csv else "all-repository-cutouts",
        "inventory_source": str(args.inventory_csv.resolve()) if args.inventory_csv else None,
        "inventory_source_sha256": sha256(args.inventory_csv) if args.inventory_csv else None,
        "inventory_rows": len(inventory_rows) if args.inventory_csv else None,
        "inventory_unique_skus": len(inventory_rows) if args.inventory_csv else None,
        "inventory_missing_cutouts": len(missing_skus),
        "repository_extra_cutouts": len(extra_paths),
        "repository_cutouts_total": len(repo_paths),
        "watch_cutouts_inspected": len(records),
        "product_mains_inspected": len(records),
        "expected_cutout_format": "RGBA PNG, 1024x1536, true transparent background, no metadata, core PNG chunks only",
        "expected_product_main_format": "RGB JPEG, 1200x1200",
        "cutout_format_pass": sum(r["format_status"] == "pass" for r in records),
        "cutout_format_fail": sum(r["format_status"] == "fail" for r in records),
        "product_main_format_pass": sum(r["product_main"]["format_status"] == "pass" for r in records),
        "product_main_format_fail": sum(r["product_main"]["format_status"] == "fail" for r in records),
        "scale_pass": sum(r["scale_status"] == "pass" for r in records),
        "scale_risk": len(risks),
        "severe_scale_risk": len(severe),
        "definite_short_or_incomplete_subject": sum(r["bbox_height_ratio"] < 0.72 for r in records),
        "corrective_action_skus": len(corrective_skus),
        "fully_passing_skus": len(records) - len(corrective_skus),
        "format_only_skus": len(format_skus - scale_skus),
        "scale_only_skus": len(scale_skus - format_skus),
        "format_and_scale_skus": len(format_skus & scale_skus),
        "format_failure_reason_counts": dict(Counter(reason for r in records for reason in r["format_failures"])),
        "scale_reason_counts": dict(Counter(reason for r in records for reason in r["scale_reasons"])),
        "scale_rule": "risk if widest visible watch row <58% canvas, subject height <72%, or opaque foreground <11%; severe at <45%, <58%, or <6.5% respectively",
        "max_row_width_ratio_quantiles": {str(q): round(float(np.quantile(width_values, q)), 6) for q in (0, .01, .05, .1, .25, .5, .75, .9, .95, .99, 1)},
        "opaque_area_ratio_quantiles": {str(q): round(float(np.quantile(area_values, q)), 6) for q in (0, .01, .05, .1, .25, .5, .75, .9, .95, .99, 1)},
        "cutout_dimensions": {f"{w}x{h}": count for (w, h), count in dimensions.most_common()},
        "all_black_contact_sheets": all_sheet_count,
        "scale_risk_black_contact_sheets": risk_sheet_count,
        "watch_images_modified": 0,
    }
    payload = {"summary": summary, "records": records}
    (out / "collection-wide-audit.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    columns = [
        "sku", "file_sku", "brand", "model", "distributor", "path", "width", "height", "format_status", "format_failures",
        "max_row_width_ratio", "bbox_height_ratio", "opaque_area_ratio", "center_offset_x",
        "center_offset_y", "scale_status", "scale_reasons", "severe_scale_risk", "edge_touching",
        "connected_components_16px", "largest_component_ratio",
    ]
    with (out / "all-watch-audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for record in records:
            writer.writerow({key: "|".join(record[key]) if isinstance(record.get(key), list) else record.get(key) for key in columns})
    with (out / "scale-risk-list.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for record in risks:
            writer.writerow({key: "|".join(record[key]) if isinstance(record.get(key), list) else record.get(key) for key in columns})
    with (out / "format-failure-list.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for record in format_failures:
            writer.writerow({key: "|".join(record[key]) if isinstance(record.get(key), list) else record.get(key) for key in columns})
    with (out / "corrective-action-list.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for record in corrective:
            writer.writerow({key: "|".join(record[key]) if isinstance(record.get(key), list) else record.get(key) for key in columns})

    if args.inventory_csv:
        with (out / "inventory-reconciliation.csv").open("w", newline="", encoding="utf-8") as handle:
            fields = ["sku", "brand", "model", "distributor", "cutout_status", "product_main_status"]
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            for row in inventory_rows:
                sku = row["SKU"]
                writer.writerow({
                    "sku": sku,
                    "brand": row.get("Brand", ""),
                    "model": row.get("Model / Name", ""),
                    "distributor": row.get("Distributor", ""),
                    "cutout_status": "present" if repository_sku(sku) in repo_by_sku else "missing",
                    "product_main_status": "present" if (PRODUCTS / repository_sku(sku) / "main.jpg").is_file() else "missing",
                })
        with (out / "missing-inventory-cutouts.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["sku"])
            writer.writerows([[sku] for sku in missing_skus])
        with (out / "repository-extra-cutouts.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["sku", "path"])
            writer.writerows([[path.stem, str(path.relative_to(REPO))] for path in extra_paths])
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
