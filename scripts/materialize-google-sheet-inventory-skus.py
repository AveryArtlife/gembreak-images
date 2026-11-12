#!/usr/bin/env python3
"""Materialize exact repository paths for every Google Sheet inventory SKU.

Only missing exact paths are created. Existing watch files are never replaced.
Each new file is a byte-for-byte copy of a previously audited, traceable alias.
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path
from urllib.parse import urlparse


REPO = Path(__file__).resolve().parents[1]
AUDIT = REPO / "audit" / "google-sheets-inventory-sync-2026-10-01"
SHEET = AUDIT / "master-inventory-snapshot.csv"
CONTACT = REPO / "audit" / "final-list-1555-contact-sheet-manifest.csv"
WATCHES = REPO / "watches-only"
PRODUCTS = REPO / "product-shots"
EXPECTED = 1555


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv_atomic(path: Path, rows: list[dict[str, object]]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def write_json_atomic(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def alias_evidence(sheet: dict[str, str], sku: str, render_sku: str) -> str:
    image_url = sheet["image_url"]
    basename = Path(urlparse(image_url).path).stem if image_url else ""
    suffix = sku.split("-", 1)[1] if "-" in sku else sku
    if sku.endswith("-v2") and sku[:-3] == render_sku:
        return "v2-exact"
    if basename == render_sku:
        return "sheet-url-exact"
    if suffix == render_sku or suffix.removesuffix("-v2") == render_sku:
        return "brand-prefix-exact"
    raise ValueError(f"Unproven alias: {sku} -> {render_sku}")


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    sheet_rows = load_csv(SHEET)
    contact_rows = load_csv(CONTACT)
    if len(sheet_rows) != EXPECTED or len({row["sku"] for row in sheet_rows}) != EXPECTED:
        raise SystemExit("Sheet snapshot is not exactly 1,555 unique SKUs")
    if len(contact_rows) != EXPECTED or len({row["sku"] for row in contact_rows}) != EXPECTED:
        raise SystemExit("Contact manifest is not exactly 1,555 unique SKUs")
    sheet_by_sku = {row["sku"]: row for row in sheet_rows}
    contact_by_sku = {row["sku"]: row for row in contact_rows}
    if set(sheet_by_sku) != set(contact_by_sku):
        raise SystemExit("Sheet and contact-manifest SKU sets differ")

    manifest_path = PRODUCTS / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_by_sku = {entry["sku"]: entry for entry in manifest}
    source_path = PRODUCTS / "source-manifest.json"
    sources = json.loads(source_path.read_text(encoding="utf-8"))
    sources_by_sku = {entry["sku"]: entry for entry in sources}

    receipt: list[dict[str, object]] = []
    for contact in contact_rows:
        sku = contact["sku"]
        exact_png = WATCHES / f"{sku}.png"
        exact_jpg = PRODUCTS / sku / "main.jpg"
        status_before = contact["status"]
        render_sku = contact["render_sku"] or sku
        evidence = "exact-existing"
        materialized = False
        if not exact_png.is_file():
            if status_before != "alias":
                raise FileNotFoundError(f"No exact file and no approved alias for {sku}")
            evidence = alias_evidence(sheet_by_sku[sku], sku, render_sku)
            source_png = WATCHES / f"{render_sku}.png"
            source_jpg = PRODUCTS / render_sku / "main.jpg"
            if not source_png.is_file() or not source_jpg.is_file():
                raise FileNotFoundError(f"Alias source incomplete: {sku} -> {render_sku}")
            exact_png.parent.mkdir(parents=True, exist_ok=True)
            exact_jpg.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_png, exact_png)
            shutil.copyfile(source_jpg, exact_jpg)
            if sha256(source_png) != sha256(exact_png):
                raise ValueError(f"PNG copy mismatch: {sku}")
            if sha256(source_jpg) != sha256(exact_jpg):
                raise ValueError(f"JPG copy mismatch: {sku}")
            materialized = True
        elif not exact_jpg.is_file():
            raise FileNotFoundError(f"Exact PNG exists without exact product main: {sku}")

        manifest_by_sku.setdefault(sku, {"sku": sku, "files": ["main.jpg"]})
        if materialized:
            sources_by_sku[sku] = {
                "sku": sku,
                "main": f"product-shots/{sku}/main.jpg",
                "origin": "google-sheet-exact-sku-materialization",
                "source": f"watches-only/{sku}.png",
                "alias_of": render_sku,
            }
        elif sku not in sources_by_sku:
            sources_by_sku[sku] = {
                "sku": sku,
                "main": f"product-shots/{sku}/main.jpg",
                "origin": "watches-only-derived",
                "source": f"watches-only/{sku}.png",
            }
        receipt.append(
            {
                "sheet_row": int(sheet_by_sku[sku]["sheet_row"]),
                "sku": sku,
                "brand": sheet_by_sku[sku]["brand"],
                "model": sheet_by_sku[sku]["model"],
                "status_before": status_before,
                "alias_source": render_sku if render_sku != sku else "",
                "alias_evidence": evidence,
                "png_sha256": sha256(exact_png),
                "jpg_sha256": sha256(exact_jpg),
            }
        )
        contact["status"] = "exact"
        contact["render_sku"] = sku

    write_json_atomic(
        manifest_path,
        [manifest_by_sku[sku] for sku in sorted(manifest_by_sku)],
    )
    write_json_atomic(
        source_path,
        [sources_by_sku[sku] for sku in sorted(sources_by_sku)],
    )
    write_csv_atomic(CONTACT, contact_rows)
    write_csv_atomic(AUDIT / "inventory-materialization-receipt.csv", receipt)

    url_updates = []
    for row in sheet_rows:
        sku = row["sku"]
        url_updates.append(
            {
                "sheet_row": int(row["sheet_row"]),
                "sku": sku,
                "old_image_url": row["image_url"],
                "new_image_url": (
                    "https://raw.githubusercontent.com/AveryArtlife/"
                    f"gembreak-images/main/watches-only/{sku}.png"
                ),
            }
        )
    write_csv_atomic(AUDIT / "google-sheet-image-url-updates.csv", url_updates)

    summary = {
        "sheet_rows": len(sheet_rows),
        "exact_paths_before": sum(row["status_before"] == "exact" for row in receipt),
        "aliases_materialized": sum(row["status_before"] == "alias" for row in receipt),
        "exact_paths_after": sum((WATCHES / f"{row['sku']}.png").is_file() for row in sheet_rows),
        "product_mains_after": sum((PRODUCTS / row["sku"] / "main.jpg").is_file() for row in sheet_rows),
        "unproven_aliases": 0,
        "image_url_updates_planned": len(url_updates),
    }
    write_json_atomic(AUDIT / "materialization-summary.json", summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
