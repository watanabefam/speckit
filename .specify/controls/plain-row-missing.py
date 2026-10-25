#!/usr/bin/env python3
"""Control mutation: delete one coverage row from a specification's plain table.

This is the defect the gate exists to catch, in its cheapest honest form: a specification that gained a
requirement and kept a table claiming to cover it. The row is removed from the first specification that
has one, so the file is named in the run rather than assumed.

It runs against a copy (`scripts/negative-control.sh` makes one), never this tree.

Exit 0 and print the identifier when a row was removed; exit 1 when there was nothing to remove, so the
control reports `not-run` instead of inventing a mutant that does not exist.
"""
import glob
import os
import sys

SECTION = "## In Plain Terms"
ID_PREFIXES = ("US", "FR-", "SC-")


def mutate(path):
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()

    start = next((i for i, line in enumerate(lines) if line.rstrip() == SECTION), None)
    if start is None:
        return None
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))

    target = None
    for i in range(start + 1, end):
        stripped = lines[i].lstrip()
        if not stripped.startswith("|"):
            continue
        cell = stripped.split("|")[1].strip()
        if cell.startswith(ID_PREFIXES):
            target = (i, cell)
    if target is None:
        return None

    index, identifier = target
    del lines[index]
    with open(path, "w", encoding="utf-8") as fh:
        fh.writelines(lines)
    return identifier


def main():
    for path in sorted(glob.glob(os.path.join("specs", "*", "spec.md"))):
        identifier = mutate(path)
        if identifier:
            print("removed %s from %s" % (identifier, path))
            return 0
    print("no specification has a coverage row to remove", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
