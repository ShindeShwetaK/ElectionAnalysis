"""
Copy every English electoral-roll PDF (file name ending in _EN.pdf) into one folder.

Default (no arguments) — this folder's 490 archive into all_together:
    python collect_en_pdfs.py

Optional overrides:
    python collect_en_pdfs.py  <source_folder_or_zip>  <destination_folder>

- If the source is a .zip (including 490_without.zip), English PDFs are read
  straight out of the archive. You do not need to unzip it first.
- If the source is a folder, the script searches that folder, its sub-folders,
  and any .zip files inside them.
- Copies files (your originals are left untouched). Marathi (_MR) files are skipped.
- Safe to run again: files already in the destination are skipped.
"""
import os
import re
import sys
import zipfile
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SRC = os.path.join(HERE, "496_without.zip")
DEFAULT_DEST = os.path.join(HERE, "all_together")

SUFFIX = "_en.pdf"   # compared in lower case, so _EN.pdf and _en.pdf both match
MR_SUFFIX = "_mr.pdf"


def district_code(name):
    m = re.search(r"DIST(\d+)", name, re.I)
    return f"DIST{m.group(1)}" if m else "unknown"


def main():
    if len(sys.argv) == 1:
        src, dest = DEFAULT_SRC, DEFAULT_DEST
    elif len(sys.argv) == 3:
        src, dest = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    else:
        print(__doc__)
        sys.exit(1)

    if not os.path.exists(src):
        print(f"Source not found: {src}")
        sys.exit(1)

    os.makedirs(dest, exist_ok=True)
    dest_prefix = os.path.join(os.path.abspath(dest), "")

    copied, skipped_existing, marathi = Counter(), 0, 0

    def save(name, read_bytes):
        nonlocal skipped_existing
        target = os.path.join(dest, os.path.basename(name))
        if os.path.exists(target):
            skipped_existing += 1
            return
        with open(target, "wb") as f:
            f.write(read_bytes())
        copied[district_code(name)] += 1

    def take_from_zip(path):
        nonlocal marathi
        with zipfile.ZipFile(path) as zf:
            for member in zf.namelist():
                if member.endswith("/"):
                    continue
                base = os.path.basename(member).lower()
                if base.endswith(SUFFIX):
                    save(member, lambda m=member, z=zf: z.read(m))
                elif base.endswith(MR_SUFFIX):
                    marathi += 1

    if os.path.isfile(src):
        take_from_zip(src)
    else:
        for root, dirs, files in os.walk(src):
            if os.path.abspath(root).startswith(dest_prefix):
                dirs[:] = []
                continue
            for fn in files:
                path = os.path.join(root, fn)
                low = fn.lower()
                if low.endswith(SUFFIX):
                    save(fn, lambda p=path: open(p, "rb").read())
                elif low.endswith(MR_SUFFIX):
                    marathi += 1
                elif low.endswith(".zip") or zipfile.is_zipfile(path):
                    take_from_zip(path)

    print(f"Source: {src}")
    print(f"English PDFs copied: {sum(copied.values())}")
    for code, n in sorted(copied.items()):
        print(f"  {code}: {n} files")
    print(f"Already in destination (skipped): {skipped_existing}")
    print(f"Marathi PDFs ignored: {marathi}")
    print(f"Destination: {dest}")


if __name__ == "__main__":
    main()
