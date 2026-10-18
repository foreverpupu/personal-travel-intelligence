#!/usr/bin/env python3
"""Cohen's kappa for two scorers on binary indicators.

Input CSV: run,scorer,indicator,value   (value 0/1)
Usage: python3 scripts/kappa.py scores.csv
"""
import csv
import sys
from collections import defaultdict


def kappa(pairs):
    n = len(pairs)
    if n == 0:
        return None
    agree = sum(1 for a, b in pairs if a == b)
    p_obs = agree / n
    p_a1 = sum(1 for a, _ in pairs if a == 1) / n
    p_b1 = sum(1 for _, b in pairs if b == 1) / n
    p_exp = p_a1 * p_b1 + (1 - p_a1) * (1 - p_b1)
    if p_exp == 1:
        return 1.0
    return (p_obs - p_exp) / (1 - p_exp)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "scores.csv"
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    by_indicator = defaultdict(lambda: defaultdict(dict))
    for row in rows:
        by_indicator[row["indicator"]][row["run"]][row["scorer"]] = int(row["value"])

    print(f"{'indicator':<10}{'runs':>6}{'agree':>8}{'kappa':>9}  note")
    worst = None
    for indicator in sorted(by_indicator):
        pairs = []
        for run, scorers in by_indicator[indicator].items():
            values = list(scorers.values())
            if len(values) >= 2:
                pairs.append((values[0], values[1]))
        k = kappa(pairs)
        agree = sum(1 for a, b in pairs if a == b) if pairs else 0
        note = ""
        if k is None:
            note = "no paired scores"
        elif k < 0.6:
            note = "below 0.6 — fix the indicator wording"
        if worst is None or (k is not None and k < worst):
            worst = k
        k_txt = "n/a" if k is None else f"{k:.2f}"
        print(f"{indicator:<10}{len(pairs):>6}{agree:>8}{k_txt:>9}  {note}")
    if worst is not None and worst < 0.6:
        print("\nVERDICT: agreement too low to interpret the result")
        return 1
    print("\nVERDICT: agreement acceptable")
    return 0


if __name__ == "__main__":
    sys.exit(main())
