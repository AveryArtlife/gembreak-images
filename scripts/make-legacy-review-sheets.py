#!/usr/bin/env python3
"""Build black-background sheets for legacy-only audit flags."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPO = Path(__file__).resolve().parents[1]
WATCHES = REPO / "watches-only"
OUTPUT = REPO / "audit" / "uniform-v2-2026-09-11" / "legacy-only-review-sheets"
SKUS = [
    "CRAN8194-51L",
    "CRAV0106-01L",
    "CRSDA02002W",
    "W130",
    "W1326",
    "W146",
    "W211",
    "W2118",
    "W215",
    "WWN01 751 7761 4187-SET",
    "WWNCBN2A1AA.FT6228",
    "WWNCV201AP.FC6429",
    "WWNH24655331",
    "WWNH32506730",
    "WWNH82565930",
    "WWNL3.821.4.53.9",
    "WWNWAY208D.FC8221",
    "WWNWAZ1010.FT8024",
    "WWNWAZ1110.FT8023",
]


def file_sku(sku: str) -> str:
    return sku.replace("/", "-")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default(size=18)
    tile_w, tile_h = 720, 1000
    for page_index in range(math.ceil(len(SKUS) / 4)):
        sheet = Image.new("RGB", (tile_w * 2, tile_h * 2), "black")
        draw = ImageDraw.Draw(sheet)
        for index, sku in enumerate(SKUS[page_index * 4 : (page_index + 1) * 4]):
            x = index % 2 * tile_w
            y = index // 2 * tile_h
            path = WATCHES / f"{file_sku(sku)}.png"
            with Image.open(path) as opened:
                watch = opened.convert("RGBA")
            watch.thumbnail((tile_w - 30, tile_h - 90), Image.Resampling.LANCZOS)
            tile = Image.new("RGBA", (tile_w, tile_h), (0, 0, 0, 255))
            tile.alpha_composite(watch, ((tile_w - watch.width) // 2, 8))
            sheet.paste(tile.convert("RGB"), (x, y))
            draw.text(
                (x + 12, y + tile_h - 62),
                f"#{page_index * 4 + index + 1}  {sku}",
                font=font,
                fill=(120, 255, 150),
            )
        sheet.save(OUTPUT / f"legacy-review-{page_index + 1:02d}.jpg", quality=96, subsampling=0)
    print(f"skus={len(SKUS)} sheets={math.ceil(len(SKUS) / 4)} output={OUTPUT}")


if __name__ == "__main__":
    main()
