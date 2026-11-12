#!/usr/bin/env python3
"""Build large black-background sheets for conservative candidate confirmation."""

from __future__ import annotations

import csv
import math
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPO = Path(__file__).resolve().parents[1]
AUDIT = REPO / "audit" / "uniform-v2-2026-09-11"
WATCHES = REPO / "watches-only"
CANDIDATES = AUDIT / "visual-failure-candidates.csv"
OUTPUT = AUDIT / "candidate-confirmation-sheets"


def file_sku(sku: str) -> str:
    return sku.replace("/", "-")


def main() -> None:
    with CANDIDATES.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    OUTPUT.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default(size=18)
    small = ImageFont.load_default(size=15)
    tile_w, tile_h = 720, 1000
    page_size = 4

    for page_index in range(math.ceil(len(rows) / page_size)):
        page_rows = rows[page_index * page_size : (page_index + 1) * page_size]
        sheet = Image.new("RGB", (tile_w * 2, tile_h * 2), "black")
        draw = ImageDraw.Draw(sheet)
        for index, row in enumerate(page_rows):
            x = index % 2 * tile_w
            y = index // 2 * tile_h
            path = WATCHES / f"{file_sku(row['sku'])}.png"
            with Image.open(path) as opened:
                image = opened.convert("RGBA")
            image.thumbnail((tile_w - 30, tile_h - 135), Image.Resampling.LANCZOS)
            tile = Image.new("RGBA", (tile_w, tile_h), (0, 0, 0, 255))
            tile.alpha_composite(image, ((tile_w - image.width) // 2, 8))
            sheet.paste(tile.convert("RGB"), (x, y))
            draw.text((x + 12, y + tile_h - 112), f"#{page_index * page_size + index + 1}  {row['sku']}", font=font, fill=(120, 255, 150))
            wrapped = textwrap.wrap(row["reason"], width=72)[:3]
            for line_index, line in enumerate(wrapped):
                draw.text((x + 12, y + tile_h - 82 + line_index * 19), line, font=small, fill=(255, 220, 120))
        sheet.save(OUTPUT / f"candidate-review-{page_index + 1:03d}.jpg", quality=96, subsampling=0)

    print(f"candidates={len(rows)} sheets={math.ceil(len(rows) / page_size)} output={OUTPUT}")


if __name__ == "__main__":
    main()
