#!/usr/bin/env python3
"""Build one zoomable QA contact sheet for all 1,555 final-list SKUs."""

from __future__ import annotations

import csv
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "audit" / "final-list-1555-contact-sheet-manifest.csv"
OUTPUT = REPO / "audit" / "final-list-1555-contact-sheet.jpg"
EXPECTED = 1555

COLS = 40
TILE_W = 220
TILE_H = 270
HEADER_H = 150
IMAGE_BOX = (202, 211)

STATUS_STYLE = {
    "exact": ("#159447", "EXACT RENDER"),
    "alias": ("#D18400", "ALIAS RENDER"),
    "missing": ("#C62828", "MISSING RENDER"),
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf") if bold else Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
        Path("/System/Library/Fonts/Supplemental/Helvetica.ttc"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf") if bold else Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    )
    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def fit_text(draw: ImageDraw.ImageDraw, value: str, maximum: int, initial: int, bold: bool = False):
    for size in range(initial, 8, -1):
        selected = font(size, bold=bold)
        if draw.textbbox((0, 0), value, font=selected)[2] <= maximum:
            return selected
    return font(9, bold=bold)


def load_render(path: Path) -> Image.Image:
    with Image.open(path) as opened:
        image = opened.convert("RGBA")
    background = Image.new("RGBA", image.size, "white")
    background.alpha_composite(image)
    image = background.convert("RGB")
    return ImageOps.contain(image, IMAGE_BOX, Image.Resampling.LANCZOS)


def main() -> None:
    with MANIFEST.open(newline="", encoding="utf-8-sig") as handle:
        records = list(csv.DictReader(handle))
    if len(records) != EXPECTED or len({row["sku"] for row in records}) != EXPECTED:
        raise SystemExit("Contact-sheet manifest is not exactly 1,555 unique SKUs")

    rows = math.ceil(EXPECTED / COLS)
    width = COLS * TILE_W
    height = HEADER_H + rows * TILE_H
    sheet = Image.new("RGB", (width, height), "#E6E6E6")
    draw = ImageDraw.Draw(sheet)

    title_font = font(42, bold=True)
    body_font = font(23)
    draw.rectangle((0, 0, width, HEADER_H), fill="#101318")
    draw.text((30, 20), "GEMBREAK FINAL LIST — ALL 1,555 SKU RENDERS", fill="white", font=title_font)
    draw.text(
        (31, 83),
        "Green: exact SKU file  |  Amber: traceable legacy/variant alias  |  Red: required render missing",
        fill="#D8DEE9",
        font=body_font,
    )
    exact = sum(record["status"] == "exact" for record in records)
    alias = sum(record["status"] == "alias" for record in records)
    missing = sum(record["status"] == "missing" for record in records)
    draw.text(
        (width - 1570, 24),
        f"{exact:,} EXACT   {alias:,} ALIAS   {missing:,} MISSING",
        fill="#73E49C",
        font=font(28, bold=True),
    )

    label_font = font(12, bold=True)
    status_font = font(11)
    for slot, record in enumerate(records):
        col = slot % COLS
        row = slot // COLS
        x = col * TILE_W
        y = HEADER_H + row * TILE_H
        status = record["status"]
        color, status_label = STATUS_STYLE[status]

        draw.rectangle((x, y, x + TILE_W - 1, y + TILE_H - 1), fill="white", outline="#B7BCC4", width=1)
        draw.rectangle((x, y, x + TILE_W - 1, y + 5), fill=color)

        if status != "missing":
            render_path = REPO / "watches-only" / f"{record['render_sku']}.png"
            if not render_path.is_file():
                raise FileNotFoundError(render_path)
            image = load_render(render_path)
            px = x + (TILE_W - image.width) // 2
            py = y + 8 + (218 - image.height) // 2
            sheet.paste(image, (px, py))
        else:
            draw.rectangle((x + 12, y + 18, x + TILE_W - 13, y + 216), fill="#FFF2F2", outline=color, width=3)
            draw.line((x + 42, y + 48, x + TILE_W - 43, y + 184), fill=color, width=8)
            draw.line((x + TILE_W - 43, y + 48, x + 42, y + 184), fill=color, width=8)
            missing_font = font(18, bold=True)
            text = "MISSING"
            tw = draw.textbbox((0, 0), text, font=missing_font)[2]
            draw.rectangle((x + (TILE_W - tw) // 2 - 8, y + 105, x + (TILE_W + tw) // 2 + 8, y + 133), fill="white")
            draw.text((x + (TILE_W - tw) // 2, y + 107), text, fill=color, font=missing_font)

        draw.rectangle((x, y + 222, x + TILE_W - 1, y + TILE_H - 1), fill="#101318")
        first = f"{int(record['index']):04d} {record['sku']}"
        first_font = fit_text(draw, first, TILE_W - 12, 12, bold=True)
        draw.text((x + 6, y + 229), first, fill="white", font=first_font)
        if status == "alias":
            detail = f"{status_label}: {record['render_sku']}"
        else:
            detail = status_label
        detail_font = fit_text(draw, detail, TILE_W - 12, 11)
        draw.text((x + 6, y + 249), detail, fill=color, font=detail_font)

    sheet.save(OUTPUT, "JPEG", quality=93, subsampling=0, optimize=True)
    print(f"output={OUTPUT} size={sheet.size[0]}x{sheet.size[1]} skus={len(records)}")


if __name__ == "__main__":
    main()
