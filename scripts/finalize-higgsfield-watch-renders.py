#!/usr/bin/env python3
"""Normalize Higgsfield watch edits and preserve authentic source dial pixels.

The script never writes to ``watches-only``. It creates a reviewable staging set,
records geometry/technical metrics, and emits black-background contact sheets.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import struct
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


CANVAS = (1024, 1536)
TARGET_CASE_WIDTH = 0.78
TARGET_VISIBLE_HEIGHT = 1400
ALPHA_THRESHOLD = 32
CORE_CHUNKS = {"IHDR", "IDAT", "IEND"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def clear_hidden_rgb(image: Image.Image) -> Image.Image:
    array = np.asarray(image.convert("RGBA")).copy()
    array[array[:, :, 3] == 0, :3] = 0
    return Image.fromarray(array, "RGBA")


def premultiplied_resize(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return image.convert("RGBa").resize(size, Image.Resampling.LANCZOS).convert("RGBA")


def alpha_metrics(image: Image.Image) -> dict[str, object]:
    rgba = np.asarray(image.convert("RGBA"))
    mask = rgba[:, :, 3] > ALPHA_THRESHOLD
    ys, xs = np.where(mask)
    if not len(xs):
        return {"caseW": 0.0, "bboxH": 0.0, "cxRatio": 0.0, "cyRatio": 0.0, "bbox": (0, 0, 0, 0)}
    bbox = (int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1))
    row_widths = []
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
    }


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


def register_source(source: np.ndarray, target: np.ndarray) -> tuple[np.ndarray | None, dict[str, object]]:
    source_rgb = source[:, :, :3]
    target_rgb = target[:, :, :3]
    source_gray = cv2.cvtColor(source_rgb, cv2.COLOR_RGB2GRAY)
    target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_RGB2GRAY)
    source_mask = (source[:, :, 3] > ALPHA_THRESHOLD).astype(np.uint8) * 255
    target_mask = (target[:, :, 3] > ALPHA_THRESHOLD).astype(np.uint8) * 255
    sift = cv2.SIFT_create(nfeatures=5000)
    source_keys, source_desc = sift.detectAndCompute(source_gray, source_mask)
    target_keys, target_desc = sift.detectAndCompute(target_gray, target_mask)
    diagnostics: dict[str, object] = {
        "source_keypoints": len(source_keys),
        "target_keypoints": len(target_keys),
        "good_matches": 0,
        "inliers": 0,
    }
    if source_desc is None or target_desc is None:
        return None, diagnostics
    matcher = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=120))
    pairs = matcher.knnMatch(source_desc, target_desc, k=2)
    good = [first for first, second in pairs if first.distance < 0.74 * second.distance]
    if len(good) < 16:
        good = [first for first, second in pairs if first.distance < 0.82 * second.distance]
    diagnostics["good_matches"] = len(good)
    if len(good) < 12:
        return None, diagnostics
    source_points = np.float32([source_keys[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    target_points = np.float32([target_keys[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    homography, inlier_mask = cv2.findHomography(source_points, target_points, cv2.RANSAC, 5.0)
    if homography is None or inlier_mask is None:
        return None, diagnostics
    inliers = int(inlier_mask.sum())
    diagnostics["inliers"] = inliers
    diagnostics["inlier_ratio"] = round(inliers / len(good), 4)
    if inliers < 12 or inliers / len(good) < 0.15:
        return None, diagnostics
    diagnostics["target_points"] = target_points[inlier_mask.ravel().astype(bool), 0, :].tolist()
    return homography, diagnostics


def dominant_case_circle(target: np.ndarray, points: list[list[float]]) -> tuple[float, float, float] | None:
    gray = cv2.cvtColor(target[:, :, :3], cv2.COLOR_RGB2GRAY)
    gray = cv2.medianBlur(gray, 5)
    height, width = gray.shape
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=max(40, min(height, width) // 5),
        param1=120,
        param2=58,
        minRadius=max(20, int(min(height, width) * 0.18)),
        maxRadius=int(min(height, width) * 0.48),
    )
    alpha = target[:, :, 3] > ALPHA_THRESHOLD
    ys, xs = np.where(alpha)
    if not len(xs):
        return None
    expected_x = float(np.median([point[0] for point in points])) if points else (xs.min() + xs.max()) / 2
    expected_y = float(np.median([point[1] for point in points])) if points else (ys.min() + ys.max()) / 2
    if circles is None:
        return None
    candidates = circles[0]
    scored = []
    for x, y, radius in candidates:
        distance = math.hypot(x - expected_x, y - expected_y)
        score = float(radius) - 0.8 * distance
        scored.append((score, float(x), float(y), float(radius)))
    _, x, y, radius = max(scored)
    if radius < width * 0.24 or abs(x - width / 2) > width * 0.2:
        return None
    return x, y, radius


def graft_authentic_dial(source_image: Image.Image, target_image: Image.Image) -> tuple[Image.Image, dict[str, object]]:
    source = np.asarray(source_image.convert("RGBA"))
    target = np.asarray(target_image.convert("RGBA"))
    homography, diagnostics = register_source(source, target)
    if homography is None:
        diagnostics["dial_graft"] = "registration-failed"
        return target_image.convert("RGBA"), diagnostics

    height, width = target.shape[:2]
    warped = cv2.warpPerspective(
        source,
        homography,
        (width, height),
        flags=cv2.INTER_LANCZOS4,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0, 0),
    )
    points = diagnostics.pop("target_points", [])
    circle = dominant_case_circle(target, points)
    if circle is not None:
        center_x, center_y, outer_radius = circle
        radius_x = radius_y = outer_radius * 0.70
        diagnostics["dial_mask"] = "round"
        diagnostics["case_circle"] = [round(center_x, 2), round(center_y, 2), round(outer_radius, 2)]
    else:
        alpha = target[:, :, 3] > ALPHA_THRESHOLD
        ys, xs = np.where(alpha)
        center_x = (xs.min() + xs.max()) / 2
        center_y = (ys.min() + ys.max()) / 2
        radius_x = (xs.max() - xs.min()) * 0.34
        radius_y = radius_x
        diagnostics["dial_mask"] = "fallback"

    yy, xx = np.mgrid[0:height, 0:width]
    distance = np.sqrt(((xx - center_x) / radius_x) ** 2 + ((yy - center_y) / radius_y) ** 2)
    feather = np.clip((1.0 - distance) / 0.018, 0.0, 1.0)
    feather *= warped[:, :, 3].astype(np.float32) / 255.0
    blend = feather[:, :, None]
    result = target.astype(np.float32)
    result[:, :, :3] = warped[:, :, :3] * blend + target[:, :, :3] * (1.0 - blend)
    result[:, :, 3] = np.maximum(target[:, :, 3], (warped[:, :, 3] * feather)).astype(np.float32)
    result = np.clip(result, 0, 255).astype(np.uint8)
    diagnostics["dial_graft"] = "applied"
    return Image.fromarray(result, "RGBA"), diagnostics


def normalize(image: Image.Image) -> Image.Image:
    source = clear_hidden_rgb(image)
    metrics = alpha_metrics(source)
    max_row_width = float(metrics["caseW"]) * source.width
    if max_row_width <= 0:
        raise ValueError("empty alpha subject")
    scale = (TARGET_CASE_WIDTH * CANVAS[0]) / max_row_width
    resized = premultiplied_resize(
        source,
        (max(1, round(source.width * scale)), max(1, round(source.height * scale))),
    )
    resized_metrics = alpha_metrics(resized)
    left, top, right, bottom = (int(value) for value in resized_metrics["bbox"])
    center_x = (left + right) / 2
    center_y = (top + bottom) / 2
    offset_x = round(CANVAS[0] / 2 - center_x)
    offset_y = round(CANVAS[1] / 2 - center_y)
    canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    canvas.alpha_composite(resized, (offset_x, offset_y))
    array = np.asarray(canvas).copy()
    margin = (CANVAS[1] - TARGET_VISIBLE_HEIGHT) // 2
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
    tile_width, tile_height = 360, 500
    columns, page_size = 4, 16
    for page_index in range(math.ceil(len(rows) / page_size)):
        page_rows = rows[page_index * page_size : (page_index + 1) * page_size]
        sheet = Image.new("RGB", (columns * tile_width, 4 * tile_height), "black")
        draw = ImageDraw.Draw(sheet)
        for index, row in enumerate(page_rows):
            x = (index % columns) * tile_width
            y = (index // columns) * tile_height
            with Image.open(image_root / str(row["filename"])) as opened:
                subject = opened.convert("RGBA")
            subject.thumbnail((tile_width - 20, tile_height - 60), Image.Resampling.LANCZOS)
            tile = Image.new("RGBA", (tile_width, tile_height), (0, 0, 0, 255))
            tile.alpha_composite(subject, ((tile_width - subject.width) // 2, 4))
            sheet.paste(tile.convert("RGB"), (x, y))
            color = (120, 255, 150) if row["pass_technical_geometry"] else (255, 100, 100)
            draw.text((x + 8, y + tile_height - 52), str(row["sku"]), font=font, fill=color)
            draw.text(
                (x + 8, y + tile_height - 32),
                f"caseW {row['caseW']:.3f} | bboxH {row['bboxH']:.3f}",
                font=font,
                fill=color,
            )
        sheet.save(output / f"fixed-{page_index + 1:03d}.jpg", quality=94, subsampling=0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--only", action="append", default=[])
    args = parser.parse_args()

    queue = json.loads(args.queue.read_text(encoding="utf-8"))
    selected = set(args.only)
    if selected:
        queue = [row for row in queue if row["sku"] in selected]
    final_root = args.output / "watches-only"
    report_rows: list[dict[str, object]] = []
    unrendered: list[dict[str, str]] = []
    for row in queue:
        sku = str(row["sku"])
        filename = str(row["filename"])
        source_path = Path(str(row["source_path"]))
        raw_path = args.raw / filename
        if not raw_path.is_file():
            unrendered.append({"sku": sku, "reason": "missing Higgsfield result"})
            continue
        with Image.open(source_path) as opened:
            source = opened.convert("RGBA")
        with Image.open(raw_path) as opened:
            target = opened.convert("RGBA")
        grafted, registration = graft_authentic_dial(source, target)
        finalized = normalize(grafted)
        output_path = final_root / filename
        save_core_png(finalized, output_path)
        metrics = alpha_metrics(finalized)
        chunks = png_chunks(output_path)
        pass_geometry = (
            finalized.size == CANVAS
            and 0.73 <= float(metrics["caseW"]) <= 0.83
            and 0.85 <= float(metrics["bboxH"]) <= 0.95
            and 0.47 <= float(metrics["cxRatio"]) <= 0.53
            and 0.47 <= float(metrics["cyRatio"]) <= 0.53
        )
        pass_technical = finalized.mode == "RGBA" and not (set(chunks) - CORE_CHUNKS)
        pass_combined = pass_geometry and pass_technical
        if not pass_combined:
            unrendered.append({"sku": sku, "reason": "technical or geometry validation failed"})
        report_rows.append(
            {
                "sku": sku,
                "filename": filename,
                "caseW": round(float(metrics["caseW"]), 6),
                "bboxH": round(float(metrics["bboxH"]), 6),
                "cxRatio": round(float(metrics["cxRatio"]), 6),
                "cyRatio": round(float(metrics["cyRatio"]), 6),
                "canvas": f"{finalized.width}x{finalized.height}",
                "color_mode": finalized.mode,
                "extra_chunks": ";".join(sorted(set(chunks) - CORE_CHUNKS)),
                "pass_technical_geometry": pass_combined,
                "dial_graft": registration.get("dial_graft", ""),
                "registration_inliers": registration.get("inliers", 0),
                "source_sha256": sha256(source_path),
                "final_sha256": sha256(output_path),
                "visual_review": "PENDING",
            }
        )

    args.output.mkdir(parents=True, exist_ok=True)
    fields = list(report_rows[0]) if report_rows else ["sku", "filename"]
    with (args.output / "qa_rerender_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(report_rows)
    with (args.output / "unrendered.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["sku", "reason"])
        writer.writeheader()
        writer.writerows(unrendered)
    contact_sheets(report_rows, final_root, args.output / "black-background-contact-sheets")
    print(
        json.dumps(
            {
                "processed": len(report_rows),
                "technical_geometry_pass": sum(bool(row["pass_technical_geometry"]) for row in report_rows),
                "dial_graft_applied": sum(row["dial_graft"] == "applied" for row in report_rows),
                "unrendered": len(unrendered),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
