#!/usr/bin/env python3
"""Print a compact repository file inventory without reading source contents."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

DEFAULT_IGNORES = {
    ".git", ".hg", ".svn", ".idea", ".vscode", ".next", ".nuxt", ".turbo",
    "node_modules", "vendor", "dist", "build", "coverage", "__pycache__",
    ".venv", "venv", "target", "Pods", ".gradle", ".dart_tool",
}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    parser.add_argument("--max-files", type=int, default=120)
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--include-hidden", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    found = []
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        parts = rel.parts
        if any(p in DEFAULT_IGNORES for p in parts):
            continue
        if not args.include_hidden and any(p.startswith(".") for p in parts[:-1]):
            continue
        if path.is_file():
            try:
                size = path.stat().st_size
            except OSError:
                size = None
            found.append({"path": rel.as_posix(), "bytes": size})
    found.sort(key=lambda x: (x["path"].count("/"), x["path"].lower()))
    truncated = len(found) > max(0, args.max_files)
    found = found[:max(0, args.max_files)]
    result = {"root": str(root), "files_shown": len(found), "truncated": truncated, "files": found}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Repository: {root}")
        print(f"Files shown: {len(found)}" + (" (truncated)" if truncated else ""))
        for item in found:
            size = f'{item["bytes"]:>9} B' if item["bytes"] is not None else "        ?"
            print(f'{size}  {item["path"]}')
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
