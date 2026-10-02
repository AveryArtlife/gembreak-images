#!/usr/bin/env python3
"""Build source-vs-staged comparison sheets for targeted visual QA."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def composite(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    subject = image.convert("RGBA")
    subject.thumbnail(size, Image.Resampling.LANCZOS)
    panel = Image.new("RGB", size, (18, 18, 18))
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    layer.alpha_composite(subject, ((size[0] - subject.width) // 2, (size[1] - subject.height) // 2))
    panel.paste(layer.convert("RGB"), (0, 0))
    return panel


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--staged-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("skus", nargs="+")
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default()
    panel_w, panel_h = 480, 660
    item_w, item_h = panel_w * 2, panel_h + 52
    per_page = 4
    for page_index in range(math.ceil(len(args.skus) / per_page)):
        page_skus = args.skus[page_index * per_page : (page_index + 1) * per_page]
        sheet = Image.new("RGB", (item_w * 2, item_h * 2), "black")
        draw = ImageDraw.Draw(sheet)
        for item_index, sku in enumerate(page_skus):
            x = (item_index % 2) * item_w
            y = (item_index // 2) * item_h
            source_path = args.source_root / f"{sku}.png"
            staged_path = args.staged_root / f"{sku}.png"
            with Image.open(source_path) as opened:
                source = composite(opened, (panel_w, panel_h))
            with Image.open(staged_path) as opened:
                staged = composite(opened, (panel_w, panel_h))
            sheet.paste(source, (x, y))
            sheet.paste(staged, (x + panel_w, y))
            draw.text((x + 8, y + panel_h + 8), f"{sku} | SOURCE", font=font, fill=(170, 210, 255))
            draw.text((x + panel_w + 8, y + panel_h + 8), f"{sku} | STAGED", font=font, fill=(120, 255, 150))
        sheet.save(args.output / f"comparison-{page_index + 1:03d}.jpg", quality=92, subsampling=0)


if __name__ == "__main__":
    main()
