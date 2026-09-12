#!/usr/bin/env python3
"""Normalize a directory of Higgsfield PNGs into the catalog canvas."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

from PIL import Image


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    script = args.project_root / "scripts" / "finalize-higgsfield-watch-renders.py"
    spec = importlib.util.spec_from_file_location("watch_finalizer", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {script}")
    finalizer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(finalizer)

    for path in sorted(args.input.glob("*.png")):
        with Image.open(path) as opened:
            normalized = finalizer.normalize(opened.convert("RGBA"))
        finalizer.save_core_png(normalized, args.output / path.name)


if __name__ == "__main__":
    main()
