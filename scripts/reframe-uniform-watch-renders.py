#!/usr/bin/env python3
"""Stage watch cutouts in the GemBreak visual-reference house style.

This script is deliberately non-destructive: it reads the authoritative inventory
and current ``watches-only`` cutouts, then writes a complete staged batch beneath
``--output``.  Files already matching the five approved visual anchors are copied
byte-for-byte.  Technical or geometry outliers are reframed without synthesizing
new watch details.

The measurable geometry is calibrated to the approved reference files rather than
the contradictory numeric ranges in CODEX_UNIFORM_RENDER_PROMPT.md:

* canvas: 1024 x 1536 RGBA
* max visible row width proxy: 0.70 .. 0.86 (target 0.78)
* alpha bounding-box height: 0.88 .. 0.93 (target 1400/1536 = 0.9115)
* alpha bounding-box centre: within 0.03 of the canvas centre

The max-row-width value is only a repeatable proxy for visual case scale.  Content,
model fidelity, buckle/holes, and view angle still require black-background review.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
import shutil
import struct
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


REPO = Path(__file__).resolve().parents[1]
WATCHES = REPO / "watches-only"
CANVAS = (1024, 1536)
TARGET_CASE_WIDTH = 0.78
CASE_WIDTH_RANGE = (0.70, 0.86)
TARGET_BBOX_HEIGHT = 1400
BBOX_HEIGHT_RANGE = (0.88, 0.93)
CENTER_TOLERANCE = 0.03
ALPHA_THRESHOLD = 32
CORE_CHUNKS = {"IHDR", "IDAT", "IEND"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def repository_sku(sku: str) -> str:
    return sku.replace("/", "-")


def read_inventory(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or "SKU" not in rows[0]:
        raise ValueError(f"Inventory must contain a SKU column: {path}")
    for row in rows:
        row["SKU"] = (row.get("SKU") or "").strip()
    blanks = [index for index, row in enumerate(rows, 2) if not row["SKU"]]
    if blanks:
        raise ValueError(f"Blank inventory SKU rows: {blanks[:20]}")
    counts = Counter(row["SKU"] for row in rows)
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


def alpha_metrics(image: Image.Image) -> dict[str, float | int | tuple[int, int, int, int]]:
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
            "opaque_pixels": 0,
        }
    bbox = (int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1))
    row_widths: list[int] = []
    for row in mask:
        xx = np.flatnonzero(row)
        row_widths.append(int(xx[-1] - xx[0] + 1) if len(xx) else 0)
    width, height = image.size
    return {
        "caseW": max(row_widths) / width,
        "bboxH": (bbox[3] - bbox[1]) / height,
        "cxRatio": ((bbox[0] + bbox[2]) / 2) / width,
        "cyRatio": ((bbox[1] + bbox[3]) / 2) / height,
        "bbox": bbox,
        "opaque_pixels": int(mask.sum()),
    }


def technical_failures(path: Path, image: Image.Image) -> list[str]:
    failures: list[str] = []
    if image.format != "PNG":
        failures.append("not-png")
    if image.mode != "RGBA":
        failures.append("not-rgba")
    if image.size != CANVAS:
        failures.append("wrong-canvas-size")
    alpha = np.asarray(image.convert("RGBA").getchannel("A"))
    if alpha.size == 0 or int(alpha.min()) != 0:
        failures.append("no-transparent-background")
    if alpha.size == 0 or int(alpha.max()) != 255:
        failures.append("no-fully-opaque-subject")
    if image.info:
        failures.append("embedded-metadata")
    if set(png_chunks(path)) - CORE_CHUNKS:
        failures.append("non-core-png-chunks")
    if not np.any(alpha > ALPHA_THRESHOLD):
        failures.append("empty-alpha")
    return failures


def geometry_failures(metrics: dict[str, object]) -> list[str]:
    failures: list[str] = []
    case_width = float(metrics["caseW"])
    bbox_height = float(metrics["bboxH"])
    centre_x = float(metrics["cxRatio"])
    centre_y = float(metrics["cyRatio"])
    if not CASE_WIDTH_RANGE[0] <= case_width <= CASE_WIDTH_RANGE[1]:
        failures.append("case-scale")
    if not BBOX_HEIGHT_RANGE[0] <= bbox_height <= BBOX_HEIGHT_RANGE[1]:
        failures.append("subject-height")
    if abs(centre_x - 0.5) > CENTER_TOLERANCE:
        failures.append("horizontal-centre")
    if abs(centre_y - 0.5) > CENTER_TOLERANCE:
        failures.append("vertical-centre")
    return failures


def clear_hidden_rgb(image: Image.Image) -> Image.Image:
    array = np.asarray(image.convert("RGBA")).copy()
    array[array[:, :, 3] == 0, :3] = 0
    return Image.fromarray(array, "RGBA")


def premultiplied_resize(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return image.convert("RGBa").resize(size, Image.Resampling.LANCZOS).convert("RGBA")


def reframe(image: Image.Image) -> Image.Image:
    """Scale the existing exact watch and trim only the remote strap ends."""
    source = clear_hidden_rgb(image)
    before = alpha_metrics(source)
    max_row_width_pixels = float(before["caseW"]) * source.width
    if max_row_width_pixels <= 0:
        raise ValueError("empty alpha subject")

    scale = (TARGET_CASE_WIDTH * CANVAS[0]) / max_row_width_pixels
    resized_size = (
        max(1, round(source.width * scale)),
        max(1, round(source.height * scale)),
    )
    resized = premultiplied_resize(source, resized_size)
    resized_metrics = alpha_metrics(resized)
    bbox = tuple(int(value) for value in resized_metrics["bbox"])
    bbox_centre_x = (bbox[0] + bbox[2]) / 2
    bbox_centre_y = (bbox[1] + bbox[3]) / 2

    left = round(CANVAS[0] / 2 - bbox_centre_x)
    top = round(CANVAS[1] / 2 - bbox_centre_y)
    canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    canvas.alpha_composite(resized, (left, top))

    # The approved anchors use 68 px transparent margins above and below the
    # visible watch.  Clear outside that symmetric 1400 px band.  This trims
    # distant buckle/tail/clasp portions while retaining the case and attached
    # strap/link segments.  It cannot invent missing straps; such files fail QA.
    array = np.asarray(canvas).copy()
    margin = (CANVAS[1] - TARGET_BBOX_HEIGHT) // 2
    array[:margin, :, :] = 0
    array[CANVAS[1] - margin :, :, :] = 0
    array[array[:, :, 3] == 0, :3] = 0
    return Image.fromarray(array, "RGBA")


def save_core_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    clear_hidden_rgb(image).save(path, format="PNG", optimize=True, compress_level=9)


def contact_sheets(rows: list[dict[str, object]], image_root: Path, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default()
    tile_w, tile_h = 360, 500
    cols, page_size = 4, 16
    for page_index in range(math.ceil(len(rows) / page_size)):
        page_rows = rows[page_index * page_size : (page_index + 1) * page_size]
        sheet = Image.new("RGB", (cols * tile_w, 4 * tile_h), "black")
        draw = ImageDraw.Draw(sheet)
        for index, row in enumerate(page_rows):
            x = (index % cols) * tile_w
            y = (index // cols) * tile_h
            path = image_root / f"{row['file_sku']}.png"
            with Image.open(path) as opened:
                subject = opened.convert("RGBA")
            subject.thumbnail((tile_w - 20, tile_h - 58), Image.Resampling.LANCZOS)
            tile = Image.new("RGBA", (tile_w, tile_h), (0, 0, 0, 255))
            tile.alpha_composite(subject, ((tile_w - subject.width) // 2, 4))
            sheet.paste(tile.convert("RGB"), (x, y))
            colour = (120, 255, 150) if row["pass_geometry"] else (255, 100, 100)
            draw.text((x + 8, y + tile_h - 50), str(row["sku"]), font=font, fill=colour)
            draw.text(
                (x + 8, y + tile_h - 30),
                f"caseW {row['caseW']:.3f} | bboxH {row['bboxH']:.3f}",
                font=font,
                fill=colour,
            )
        sheet.save(output / f"uniform-{page_index + 1:03d}.jpg", quality=92, subsampling=0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-count", type=int, default=2456)
    parser.add_argument("--sku", action="append", default=[], help="Stage only selected SKU(s) for a pilot")
    parser.add_argument("--contact-sheets", action="store_true")
    args = parser.parse_args()

    inventory = read_inventory(args.inventory.resolve())
    if len(inventory) != args.expected_count:
        raise ValueError(f"Expected {args.expected_count} inventory rows, found {len(inventory)}")
    selected = set(args.sku)
    if selected:
        missing_selection = selected - {row["SKU"] for row in inventory}
        if missing_selection:
            raise ValueError(f"Selected SKUs are not in inventory: {sorted(missing_selection)}")
        inventory = [row for row in inventory if row["SKU"] in selected]

    image_output = args.output.resolve() / "watches-only"
    image_output.mkdir(parents=True, exist_ok=True)
    report_rows: list[dict[str, object]] = []
    unrendered: list[dict[str, str]] = []

    for row in inventory:
        sku = row["SKU"]
        file_sku = repository_sku(sku)
        source = WATCHES / f"{file_sku}.png"
        destination = image_output / f"{file_sku}.png"
        if not source.is_file():
            unrendered.append({"sku": sku, "reason": "missing source cutout"})
            continue
        with Image.open(source) as opened:
            original_format = opened.format
            original_mode = opened.mode
            original_size = opened.size
            original_info = dict(opened.info)
            original = opened.convert("RGBA")
            original.format = original_format
            original.info = original_info
            tech = technical_failures(source, opened)
        source_metrics = alpha_metrics(original)
        geom = geometry_failures(source_metrics)
        action = "copied"
        if tech or geom:
            candidate = reframe(original)
            save_core_png(candidate, destination)
            action = "reframed"
        else:
            shutil.copy2(source, destination)

        with Image.open(destination) as staged_opened:
            staged = staged_opened.convert("RGBA")
            staged_metrics = alpha_metrics(staged)
            staged_tech = technical_failures(destination, staged_opened)
        staged_geom = geometry_failures(staged_metrics)
        pass_geometry = not staged_tech and not staged_geom
        if not pass_geometry:
            unrendered.append(
                {
                    "sku": sku,
                    "reason": ";".join(staged_tech + staged_geom),
                }
            )
        report_rows.append(
            {
                "sku": sku,
                "file_sku": file_sku,
                "caseW": round(float(staged_metrics["caseW"]), 6),
                "bboxH": round(float(staged_metrics["bboxH"]), 6),
                "cxRatio": round(float(staged_metrics["cxRatio"]), 6),
                "cyRatio": round(float(staged_metrics["cyRatio"]), 6),
                "pass_geometry": pass_geometry,
                "pass_content": "PENDING_VISUAL_REVIEW",
                "action": action,
                "source_width": original_size[0],
                "source_height": original_size[1],
                "source_sha256": sha256(source),
                "staged_sha256": sha256(destination),
                "source_technical_failures": ";".join(tech),
                "source_geometry_failures": ";".join(geom),
                "staged_failures": ";".join(staged_tech + staged_geom),
            }
        )

    args.output.mkdir(parents=True, exist_ok=True)
    fieldnames = list(report_rows[0]) if report_rows else [
        "sku", "file_sku", "caseW", "bboxH", "cxRatio", "cyRatio",
        "pass_geometry", "pass_content", "action",
    ]
    with (args.output / "qa_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(report_rows)
    with (args.output / "unrendered.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["sku", "reason"])
        writer.writeheader()
        writer.writerows(unrendered)
    if args.contact_sheets:
        contact_sheets(report_rows, image_output, args.output / "black-contact-sheets")

    copied = sum(row["action"] == "copied" for row in report_rows)
    reframed = sum(row["action"] == "reframed" for row in report_rows)
    passing = sum(bool(row["pass_geometry"]) for row in report_rows)
    print(f"staged={len(report_rows)} copied={copied} reframed={reframed} geometry_pass={passing}")
    print(f"unrendered={len(unrendered)} output={args.output.resolve()}")


if __name__ == "__main__":
    main()
