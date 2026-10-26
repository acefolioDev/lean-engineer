#!/usr/bin/env python3
"""Summarize common test-runner logs without discarding the original log."""
from __future__ import annotations
import argparse
import re
from pathlib import Path

SUMMARY_PATTERNS = [
    re.compile(r"(\d+\s+passed(?:,\s*\d+\s+skipped)?(?:,\s*\d+\s+failed)?(?:,\s*\d+\s+errors?)?.*)", re.I),
    re.compile(r"(tests?:\s*\d+.*)", re.I),
    re.compile(r"(test result:.*)", re.I),
    re.compile(r"(passed|failed|error|errors|skipped|no tests found).*$", re.I),
]
FAIL_PATTERNS = re.compile(r"(FAIL(?:ED)?|ERROR|AssertionError|Exception|Traceback|not ok \d+|✖|❌)", re.I)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", help="path to saved test output")
    parser.add_argument("--failure-lines", type=int, default=12)
    args = parser.parse_args()
    path = Path(args.log)
    if not path.is_file():
        parser.error(f"log not found: {path}")
    lines = path.read_text(errors="replace").splitlines()
    summaries = []
    for line in lines:
        if any(p.search(line) for p in SUMMARY_PATTERNS):
            cleaned = line.strip()
            if cleaned and cleaned not in summaries:
                summaries.append(cleaned)
    failures = []
    for i, line in enumerate(lines):
        if FAIL_PATTERNS.search(line):
            for candidate in lines[max(0, i-1):min(len(lines), i+2)]:
                candidate = candidate.strip()
                if candidate and candidate not in failures:
                    failures.append(candidate)
    print(f"Log: {path} ({len(lines)} lines)")
    print("\nSummary:")
    if summaries:
        for line in summaries[-8:]:
            print(f"  {line[:300]}")
    else:
        print("  No recognized summary line; inspect the original log.")
    print("\nFailure/error context:")
    if failures:
        for line in failures[:max(0, args.failure_lines)]:
            print(f"  {line[:300]}")
        if len(failures) > args.failure_lines:
            print(f"  ... {len(failures)-args.failure_lines} additional distinct lines omitted")
    else:
        print("  No obvious failure markers found (this does not prove success).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
