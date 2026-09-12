#!/usr/bin/env python3
"""Lock the approved 520-SKU rerender scope and prepare its generation queue."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def file_sku(sku: str) -> str:
    return sku.replace("/", "-")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-inventory", type=int, default=2456)
    parser.add_argument("--expected-rerenders", type=int, default=520)
    parser.add_argument("--print-queue", action="store_true")
    args = parser.parse_args()

    repo = args.repo.resolve()
    watches = repo / "watches-only"
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    inventory = read_csv(args.inventory.resolve())
    audit = read_csv(args.audit.resolve())
    if len(inventory) != args.expected_inventory:
        raise ValueError(
            f"Expected {args.expected_inventory} inventory rows, found {len(inventory)}"
        )
    if len(audit) != args.expected_inventory:
        raise ValueError(f"Expected {args.expected_inventory} audit rows, found {len(audit)}")

    inventory_by_sku = {row["SKU"].strip(): row for row in inventory}
    audit_by_sku = {row["sku"].strip(): row for row in audit}
    if len(inventory_by_sku) != len(inventory):
        duplicates = [sku for sku, count in Counter(row["SKU"].strip() for row in inventory).items() if count > 1]
        raise ValueError(f"Duplicate inventory SKUs: {duplicates[:20]}")
    if set(inventory_by_sku) != set(audit_by_sku):
        missing = sorted(set(inventory_by_sku) - set(audit_by_sku))
        extra = sorted(set(audit_by_sku) - set(inventory_by_sku))
        raise ValueError(f"Inventory/audit mismatch; missing={missing[:20]} extra={extra[:20]}")

    rerender_skus = {
        sku
        for sku, row in audit_by_sku.items()
        if row.get("needs_rerender", "").strip().lower() == "true"
        and row.get("human_classification", "").strip().lower() == "true failure"
    }
    if len(rerender_skus) != args.expected_rerenders:
        raise ValueError(
            f"Expected {args.expected_rerenders} approved rerenders, found {len(rerender_skus)}"
        )

    queue: list[dict[str, object]] = []
    hash_rows: list[dict[str, object]] = []
    missing_files: list[str] = []
    for index, inventory_row in enumerate(inventory, 1):
        sku = inventory_row["SKU"].strip()
        filename = f"{file_sku(sku)}.png"
        source = watches / filename
        if not source.is_file():
            missing_files.append(sku)
            continue
        audit_row = audit_by_sku[sku]
        allowed = sku in rerender_skus
        hash_rows.append(
            {
                "sku": sku,
                "filename": filename,
                "human_classification": audit_row.get("human_classification", ""),
                "allowed_to_change": allowed,
                "sha256_before": sha256(source),
            }
        )
        if allowed:
            queue.append(
                {
                    "index": len(queue) + 1,
                    "sku": sku,
                    "filename": filename,
                    "brand": inventory_row.get("Brand", "").strip(),
                    "model": inventory_row.get("Model / Name", "").strip(),
                    "distributor": inventory_row.get("Distributor", "").strip(),
                    "defect": audit_row.get("notes", "").strip(),
                    "source_path": str(source),
                }
            )
    if missing_files:
        raise FileNotFoundError(f"Missing inventory cutouts: {missing_files[:20]}")
    if len(queue) != args.expected_rerenders:
        raise ValueError(f"Queue contains {len(queue)} rows, expected {args.expected_rerenders}")

    with (output / "scope-lock-sha256.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(hash_rows[0]))
        writer.writeheader()
        writer.writerows(hash_rows)
    (output / "rerender-queue.json").write_text(
        json.dumps(queue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    with (output / "rerender-queue.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(queue[0]))
        writer.writeheader()
        writer.writerows(queue)
    summary = {
        "inventory_count": len(inventory),
        "rerender_count": len(queue),
        "protected_count": len(inventory) - len(queue),
        "queue_sha256": sha256(output / "rerender-queue.json"),
    }
    (output / "scope-lock-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    if args.print_queue:
        print(json.dumps(queue, ensure_ascii=False, separators=(",", ":")))
    else:
        print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
