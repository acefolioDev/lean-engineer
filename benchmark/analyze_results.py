#!/usr/bin/env python3
"""Summarize paired benchmark CSV rows; uses only the Python standard library."""
import argparse
import csv
import statistics
from collections import defaultdict
from pathlib import Path

def truth(v):
    return str(v).strip().lower() in {"1", "true", "yes", "pass", "passed"}

def num(row, key):
    try:
        return float(row.get(key, "") or 0)
    except ValueError:
        return 0.0

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("csv_file", help="results.csv")
    args = p.parse_args()
    rows = list(csv.DictReader(Path(args.csv_file).open(newline="", encoding="utf-8")))
    groups = defaultdict(list)
    for r in rows:
        groups[(r.get("task_id", ""), r.get("condition", "").strip().lower())].append(r)
    summary = defaultdict(list)
    for (task, condition), rs in groups.items():
        r = rs[-1]
        total = num(r, "input_tokens") + num(r, "output_tokens")
        cost = num(r, "cost_usd")
        success = truth(r.get("completed")) and truth(r.get("acceptance_passed"))
        summary[condition].append((task, total, cost, success, num(r, "duration_seconds")))
    print(f"Rows: {len(rows)}")
    for cond, vals in sorted(summary.items()):
        totals = [v[1] for v in vals]
        costs = [v[2] for v in vals]
        successes = [v for v in vals if v[3]]
        print(f"\n{cond}: tasks={len(vals)}, accepted={len(successes)}/{len(vals)}")
        print(f"  median total tokens: {statistics.median(totals) if totals else 0:.0f}")
        print(f"  median cost USD: {statistics.median(costs) if costs else 0:.6f}")
        if successes:
            print(f"  cost per successful task (aggregate): ${sum(v[2] for v in vals)/len(successes):.6f}")
    by_task = defaultdict(dict)
    for cond, vals in summary.items():
        for task, tokens, cost, success, duration in vals:
            by_task[task][cond] = (tokens, cost, success)
    pairs = [(t, d) for t, d in by_task.items() if "baseline" in d and "skill" in d]
    if pairs:
        token_changes = []
        cost_changes = []
        for task, d in pairs:
            b, s = d["baseline"], d["skill"]
            if b[0] > 0:
                token_changes.append((b[0] - s[0]) / b[0] * 100)
            if b[1] > 0:
                cost_changes.append((b[1] - s[1]) / b[1] * 100)
        print(f"\nPaired tasks: {len(pairs)}")
        if token_changes:
            print(f"  median token reduction: {statistics.median(token_changes):.1f}% (positive = fewer tokens)")
        if cost_changes:
            print(f"  median cost reduction: {statistics.median(cost_changes):.1f}% (positive = lower cost)")
        b_rate = sum(d["baseline"][2] for _, d in pairs) / len(pairs)
        s_rate = sum(d["skill"][2] for _, d in pairs) / len(pairs)
        print(f"  acceptance rate baseline={b_rate:.1%}, skill={s_rate:.1%}")
    else:
        print("\nNo paired tasks found. Each task needs both condition=baseline and condition=skill.")
    print("\nNote: this simple summary is descriptive, not a statistical significance test.")

if __name__ == "__main__":
    main()
