"""
Clean the address column in all_english_voters.xlsx and write a new workbook.

Repeated place names are kept once, in their original order:
    AMBA, AMBA, AMBA, Shahuwadi, KOLHAPUR, 415101
    -> Amba, Shahuwadi, Kolhapur, 415101

Every address is then written in title case. Other columns are unchanged.

Usage:
    python clean_addresses.py
"""
import os
import re

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "electoral_rolls_output", "all_english_voters.xlsx")
SRC_COPY = os.path.join(HERE, "electoral_rolls_output", "_voters_copy.xlsx")
DEST = os.path.join(HERE, "electoral_rolls_output", "all_english_voters_cleaned.xlsx")

ILLEGAL_XLSX = re.compile(r"[\000-\010\013\014\016-\037]")


def clean_address(value):
    if not isinstance(value, str):
        return ""
    text = ILLEGAL_XLSX.sub("", value.replace("\n", " "))
    text = re.sub(r"\s+", " ", text).strip()
    if not text or text.lower() in {"none", "nan"}:
        return ""

    kept = []
    seen = set()
    for part in text.split(","):
        words = []
        for word in part.split():
            token = word.strip(" .")
            if not token:
                continue
            key = token.casefold()
            if key in seen:
                continue
            seen.add(key)
            words.append(token.title())
        if words:
            kept.append(" ".join(words))
    return ", ".join(kept)


def source_path():
    try:
        with open(SRC, "rb"):
            return SRC
    except PermissionError:
        return SRC_COPY


def main():
    path = source_path()
    print(f"Reading {path}", flush=True)
    df = pd.read_excel(path, dtype=str)
    original = df["address"].fillna("")
    df["address"] = original.map(clean_address)
    changed = int((original.map(lambda v: re.sub(r"\s+", " ", str(v)).strip()) != df["address"]).sum())
    print(f"{changed:,} addresses changed out of {len(df):,} rows", flush=True)
    print("Examples:", flush=True)
    shown = 0
    for before, after in zip(original, df["address"]):
        if str(before).strip() != after:
            print(f"  {before}", flush=True)
            print(f"  -> {after}", flush=True)
            shown += 1
            if shown == 8:
                break

    print(f"Writing {DEST}", flush=True)
    with pd.ExcelWriter(DEST, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="All_Voters", index=False)
    print(f"Saved {len(df):,} rows", flush=True)


if __name__ == "__main__":
    main()
