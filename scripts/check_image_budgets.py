#!/usr/bin/env python3
"""Fail CI when generated images exceed configured size budgets."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".avif"}


def _format_kb(num_bytes: int) -> str:
    return f"{num_bytes / 1024:.1f}KB"


def _collect_images(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Check generated image size budgets")
    parser.add_argument("images_dir", type=Path, help="Directory with generated image assets")
    parser.add_argument("--max-file-kb", type=int, default=450, help="Max size in KB for any single image")
    parser.add_argument("--max-total-kb", type=int, default=1600, help="Max total size in KB across all images")
    parser.add_argument("--top", type=int, default=8, help="How many largest images to print")
    args = parser.parse_args()

    images = _collect_images(args.images_dir)
    if not images:
        print(f"No image files found under {args.images_dir}")
        return 0

    file_budget_bytes = args.max_file_kb * 1024
    total_budget_bytes = args.max_total_kb * 1024

    sized = [(path, path.stat().st_size) for path in images]
    total_size = sum(size for _, size in sized)
    oversized = [(path, size) for path, size in sized if size > file_budget_bytes]

    print(f"Checked {len(sized)} images in {args.images_dir}")
    print(f"Total image payload: {_format_kb(total_size)} (budget: {args.max_total_kb}KB)")

    print("Largest images:")
    for path, size in sorted(sized, key=lambda item: item[1], reverse=True)[: args.top]:
        print(f"  - {path}: {_format_kb(size)}")

    failed = False
    if total_size > total_budget_bytes:
        failed = True
        print(
            f"ERROR: Total image payload {_format_kb(total_size)} exceeds budget of {args.max_total_kb}KB",
            file=sys.stderr,
        )

    if oversized:
        failed = True
        print(
            f"ERROR: Found {len(oversized)} images above per-file budget of {args.max_file_kb}KB",
            file=sys.stderr,
        )
        for path, size in oversized:
            print(f"  - {path}: {_format_kb(size)}", file=sys.stderr)

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
