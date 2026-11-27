"""What a column or attribute really holds, judged from its values. Standard library only.

A declared type says little: dates live in text, flags are 'Y'/'N', numbers carry separators, timestamps are
integers. `describe(values)` looks at a sample of non-null values and returns short phrases for the snapshot.
"""
from __future__ import annotations

import datetime
import re

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ISO_DATETIME = re.compile(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:?\d{2})?$")
YEAR_FIRST = re.compile(r"^\d{4}[/.]\d{1,2}[/.]\d{1,2}$")
THREE_PART = re.compile(r"^(\d{1,2})([/.\-])(\d{1,2})\2(\d{4}|\d{2})$")
PLAIN_NUMBER = re.compile(r"^[+-]?\d+(\.\d+)?$")
FORMATTED_NUMBER = re.compile(r"^[+-]?[$€£¥]?\s?\d{1,3}([,. ' ]\d{3})+([.,]\d+)?\s?[%$€£¥]?$|^[+-]?[$€£¥]\s?\d+([.,]\d+)?$|^[+-]?\d+([.,]\d+)?\s?[%$€£¥]$")

EPOCH_S = (631152000, 4102444800)            # 1990-01-01 .. 2100-01-01
EPOCH_MS = (EPOCH_S[0] * 1000, EPOCH_S[1] * 1000)


def _utc(seconds: float) -> str:
    return datetime.datetime.fromtimestamp(seconds, datetime.timezone.utc).strftime("%Y-%m-%d")


def type_name(value) -> str:
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "str"
    if value is None:
        return "null"
    return type(value).__name__


def describe(values: list) -> list[str]:
    """Phrases about the stored form of `values` (a sample of distinct non-null values)."""
    values = [v for v in values if v is not None]
    if not values:
        return []
    notes: list[str] = []
    texts = [v for v in values if isinstance(v, str)]
    ints = [v for v in values if isinstance(v, int) and not isinstance(v, bool)]
    if texts and len(texts) == len(values):
        stripped = [t.strip() for t in texts]
        if all(ISO_DATE.match(t) for t in stripped):
            notes.append("ISO date text YYYY-MM-DD")
        elif all(ISO_DATETIME.match(t) for t in stripped):
            sep = "T" if "T" in stripped[0] else "space"
            zone = "with zone" if re.search(r"(Z|[+-]\d{2}:?\d{2})$", stripped[0]) else "no zone"
            notes.append(f"ISO datetime text ({sep} separator, {zone})")
        elif all(YEAR_FIRST.match(t) for t in stripped):
            notes.append("date text, year first with / or .")
        elif all(THREE_PART.match(t) for t in stripped):
            parts = [THREE_PART.match(t).groups() for t in stripped]
            sep = parts[0][1]
            first_big = any(int(p[0]) > 12 for p in parts)
            second_big = any(int(p[2]) > 12 for p in parts)
            if first_big and not second_big:
                notes.append(f"day-first date text DD{sep}MM{sep}YYYY: comparing or sorting it as text is not date order, rebuild the date first")
            elif second_big and not first_big:
                notes.append(f"month-first date text MM{sep}DD{sep}YYYY: comparing or sorting it as text is not date order, rebuild the date first")
            else:
                notes.append(f"date text NN{sep}NN{sep}YYYY, day-first or month-first not decidable from the sample: ask or check the writer")
        elif all(PLAIN_NUMBER.match(t) for t in stripped):
            notes.append("numbers stored as text: cast before comparing, sorting or summing")
        elif all(FORMATTED_NUMBER.match(t) for t in stripped):
            notes.append("formatted numbers stored as text (separators or currency signs): strip them, then cast")
    elif ints and len(ints) == len(values) and len(ints) >= 2:
        low, high = min(ints), max(ints)
        if EPOCH_S[0] <= low and high <= EPOCH_S[1]:
            notes.append(f"looks like epoch seconds ({_utc(low)} to {_utc(high)} UTC)")
        elif EPOCH_MS[0] <= low and high <= EPOCH_MS[1]:
            notes.append(f"looks like epoch milliseconds ({_utc(low / 1000)} to {_utc(high / 1000)} UTC)")
        elif 19000101 <= low and high <= 21001231 and all(1 <= (v // 100) % 100 <= 12 and 1 <= v % 100 <= 31 for v in ints):
            notes.append("looks like dates as integers YYYYMMDD")
    kinds = sorted({type_name(v) for v in values})
    if len(kinds) > 1:
        notes.append("mixed value types: " + ", ".join(kinds))
    return notes


def tokens(name: str) -> set[str]:
    """Lower-case word stems of an identifier: OrderItems, order_item and tblOrderItem all share {order, item}."""
    words = re.findall(r"[A-Z]+(?![a-z])|[A-Z]?[a-z]+|\d+", name.replace("-", "_"))
    out = set()
    for word in words:
        word = word.lower()
        if word in ("tbl", "t", "id", "ids", "fk", "pk", "ref", "no", "num", "key", "code"):
            continue
        if len(word) > 3 and word.endswith("ies"):
            word = word[:-3] + "y"
        elif len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
            word = word[:-1]
        out.add(word)
    return out
