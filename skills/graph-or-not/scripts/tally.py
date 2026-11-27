#!/usr/bin/env python3
"""Add up a delimited export (CSV, TSV, semicolon-separated): totals and shares per group.

Usage:
    python3 tally.py FILE --by COLUMN [--by COLUMN ...] [--sum COLUMN] [--where COLUMN=VALUE ...]

    --by      column(s) to group on, for example a depth, a route or a status column
    --sum     numeric column to add up per group; without it, rows are counted
    --where   keep only rows where COLUMN equals VALUE (repeatable)

Prints one line per group with its total and its share of the grand total, largest first.
Reads the file only. Standard library only, no network.
"""
import argparse
import csv
import re
import sys
from collections import defaultdict


def number(text):
    """'1,104,220', '1 104 220', '12.5' and '' as a float; None when it is not a number."""
    cleaned = re.sub(r"[,\s_\u00a0']", "", text or "")
    if cleaned == "":
        return 0.0
    try:
        return float(cleaned)
    except ValueError:
        return None


def show(value):
    return f"{int(value):,}" if float(value).is_integer() else f"{value:,.2f}"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Totals and shares per group for a delimited export.")
    parser.add_argument("file")
    parser.add_argument("--by", action="append", required=True, metavar="COLUMN")
    parser.add_argument("--sum", dest="total", metavar="COLUMN")
    parser.add_argument("--where", action="append", default=[], metavar="COLUMN=VALUE")
    args = parser.parse_args(argv)

    filters = []
    for item in args.where:
        if "=" not in item:
            parser.error(f"--where needs COLUMN=VALUE, got {item!r}")
        filters.append(tuple(item.split("=", 1)))

    with open(args.file, newline="", encoding="utf-8-sig") as handle:
        sample = handle.read(8192)
        handle.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        except csv.Error:
            dialect = csv.excel
        reader = csv.DictReader(handle, dialect=dialect)
        columns = [c.strip() for c in (reader.fieldnames or [])]
        reader.fieldnames = columns
        wanted = args.by + ([args.total] if args.total else []) + [c for c, _ in filters]
        missing = [c for c in wanted if c not in columns]
        if missing:
            sys.exit(f"no column named {', '.join(missing)}; the file has: {', '.join(columns)}")

        groups, rows, kept, skipped = defaultdict(float), defaultdict(int), 0, 0
        for row in reader:
            if any((row.get(c) or "").strip() != v for c, v in filters):
                continue
            value = 1.0
            if args.total:
                value = number(row.get(args.total))
                if value is None:
                    skipped += 1
                    continue
            key = tuple((row.get(c) or "").strip() or "(blank)" for c in args.by)
            groups[key] += value
            rows[key] += 1
            kept += 1

    grand = sum(groups.values())
    what = f"sum of {args.total}" if args.total else "rows"
    print(f"{args.file}: {kept:,} rows kept; {what} = {show(grand)}")
    if skipped:
        print(f"skipped {skipped:,} rows whose {args.total} is not a number")
    width = max([len(" / ".join(k)) for k in groups] + [len(" / ".join(args.by))])
    print(f"{' / '.join(args.by):<{width}}  {'rows':>9}  {what:>18}  {'share':>8}")
    for key, value in sorted(groups.items(), key=lambda kv: -kv[1]):
        share = f"{100 * value / grand:.2f}%" if grand else "n/a"
        print(f"{' / '.join(key):<{width}}  {rows[key]:>9,}  {show(value):>18}  {share:>8}")


if __name__ == "__main__":
    main()
