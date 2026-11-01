#!/usr/bin/env python3
"""check-search-record — assert a note that reports a null search records what was searched.

WHY THIS EXISTS
"The literature had nothing to say" is indistinguishable from "nobody looked" unless the note says
**where**, **when**, **with which words**, and **what came back**. This repository wrote that once, by
hand (`docs/research/verification-tooling-2026-10.md` §13), after the null had already been quoted in a
decision with no record behind it. Nothing made the second one happen, so the second one would have been
written the same way: from memory, in whatever shape the author felt like.

The fields are not invented here. PRISMA-S (Rethlefsen et al. 2021, `doi:10.1186/s13643-020-01542-z`) asks
for the sources and the *date last searched* (item 7), the full strategy "such that it could be repeated"
(item 8), and the numbers screened with reasons (item 17). Those four facts are what make a null checkable
by someone who was not there. `decisions/0012-search-records-are-checkable.md` records the reasoning.

WHAT IT CHECKS
A section whose heading, after an optional number (`## 13. …`, `### 4) …`), starts with "search record"
(case-insensitive), at heading level 2-4. Inside that section:

1. At least one sentence of prose. A bare table with no statement of what was asked is a spreadsheet, not
   a record.
2. A markdown table whose header carries `Source`, `Date`, `Query`, and one of `Hits` / `Result` /
   `Returned` / `Outcome` / `What came back`. Extra columns are fine — a question column makes the record
   readable, not less checkable.
3. Every data row: a named source (not blank, not `-`, not `unknown` / `various` / `several`), a date that
   parses as `YYYY-MM-DD`, a query with at least three characters and at least one letter (an empty query
   cannot be repeated), and a non-empty result. "Nothing" IS a valid result — that is the whole point of
   the section — so only blank cells fail.
4. At least one data row. A section with a header and no rows is the shape a ritual takes, and a check that
   passes on nothing is not a check (the rule feature 005 states for the gate applies here).

OPTIONAL BY DEFAULT
Most research notes contain no null at all, and forcing a section onto them would teach authors to add a
row for a search they did not run. A note without the section passes and says so. `--require-section`
demands one, for a project that wants every note to account for its searches.

WHAT IT CANNOT DO
It cannot tell whether the null is true, whether the query was a good one, or whether the author actually
ran it. It checks that the four facts a reader needs are present and well-formed. A record with a real
query and a fabricated result passes this check, which is why the record sits beside the sources it
summarises rather than instead of them.

Usage: check-search-record.py [--json] [--require-section] <file> [...]
Exit:  0 = every file conformant, or declined (no section, not required) · 1 = at least one finding ·
       2 = usage or read error.
"""
from __future__ import annotations

import datetime
import json
import re
import sys

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
# `## Search record`, `## 13. Search record`, `### 4) Search record (2026-10-31)` — numbering is how this
# repository's notes are laid out, so it must not be what fails a conforming section.
SECTION_RE = re.compile(r"^(?:\d+[.)]\s*)?search\s+record\b", re.I)
FENCE_RE = re.compile(r"^\s*```")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)

REQUIRED = ("source", "date", "query")
RESULT_COLUMNS = ("hits", "result", "returned", "outcome", "what came back")
EMPTY_SOURCE = {"", "-", "--", "—", "n/a", "na", "unknown", "various", "several", "multiple", "misc"}

MIN_PROSE = 30          # characters; a label is not a sentence
MIN_QUERY = 3           # characters, and at least one letter
MIN_RESULT = 3          # characters


class Finding:
    def __init__(self, path: str, kind: str, detail: str) -> None:
        self.path, self.kind, self.detail = path, kind, detail

    def __str__(self) -> str:
        return f"{self.path}: {self.kind}: {self.detail}"


def strip_markup(cell: str) -> str:
    return cell.replace("`", "").replace("*", "").strip()


def norm_header(cell: str) -> str:
    return re.sub(r"\s+", " ", strip_markup(cell).lower())


def split_row(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [c.strip() for c in body.split("|")]


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c.strip()) for c in cells)


def parse_date(cell: str) -> str | None:
    text = strip_markup(cell)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return None
    try:
        datetime.date.fromisoformat(text)
    except ValueError:
        return None
    return text


def check_section(path: str, lines: list[str], start: int, level: int) -> tuple[list[Finding], dict]:
    """Validate one `## Search record` section. Returns (findings, stats)."""
    findings: list[Finding] = []
    body: list[str] = []
    for line in lines[start + 1:]:
        heading = HEADING_RE.match(line)
        if heading and len(heading.group(1)) <= level:
            break
        body.append(line)

    prose = [
        l for l in body
        if l.strip() and not l.strip().startswith("|") and not HEADING_RE.match(l)
        and len(COMMENT_RE.sub("", l).strip()) >= MIN_PROSE
    ]

    # The first table that looks like a record. A section may carry more than one table (a field-definition
    # table above the record is common), so the search is for a table with the required columns rather than
    # for the first `|` line.
    header: list[str] | None = None
    rows: list[list[str]] = []
    i = 0
    while i < len(body):
        line = body[i]
        if line.strip().startswith("|") and i + 1 < len(body) and body[i + 1].strip().startswith("|"):
            candidate = split_row(line)
            sep = split_row(body[i + 1])
            if is_separator(sep) and len(candidate) == len(sep):
                names = [norm_header(c) for c in candidate]
                if all(any(r == n or r in n for n in names) for r in REQUIRED) and any(
                        any(n.startswith(r) for n in names) for r in RESULT_COLUMNS):
                    header = names
                    i += 2
                    while i < len(body) and body[i].strip().startswith("|"):
                        cells = split_row(body[i])
                        if not is_separator(cells):
                            rows.append(cells)
                        i += 1
                    break
        i += 1

    if not prose:
        findings.append(Finding(path, "no-prose",
                                "the section has no sentence saying what was asked of the source"))

    if header is None:
        findings.append(Finding(
            path, "no-table",
            "no table with Source / Date / Query and a Hits or Result column "
            "(the four facts a reader needs to repeat the search)"))
        return findings, {"rows": 0, "declined": False}

    if not rows:
        findings.append(Finding(path, "vacuous",
                                "the section has no rows — nothing was examined, which is not a record"))

    def index(*names: str) -> int:
        for name in names:
            for n, h in enumerate(header):
                if h == name or h.startswith(name):
                    return n
        return -1

    src_i = index("source")
    date_i = index("date")
    query_i = index("query")
    result_i = max(index(r) for r in RESULT_COLUMNS)

    for n, cells in enumerate(rows, start=1):
        def cell(at: int) -> str:
            return cells[at] if 0 <= at < len(cells) else ""

        if strip_markup(cell(src_i)).lower() in EMPTY_SOURCE:
            findings.append(Finding(path, "no-source",
                                    f"row {n}: no source named — a record must say where the search ran"))
        raw_date = cell(date_i)
        if parse_date(raw_date) is None:
            findings.append(Finding(path, "bad-date",
                                    f"row {n}: '{strip_markup(raw_date)}' is not a YYYY-MM-DD date "
                                    f"(PRISMA-S item 7 asks for the date last searched)"))
        query = strip_markup(cell(query_i))
        if len(query) < MIN_QUERY or not re.search(r"[A-Za-z]", query):
            findings.append(Finding(path, "no-query",
                                    f"row {n}: the query is empty — a search that cannot be repeated "
                                    f"cannot be checked"))
        result = strip_markup(cell(result_i))
        if len(result) < MIN_RESULT:
            findings.append(Finding(path, "no-result",
                                    f"row {n}: no result recorded — 'nothing' is a result and must be said"))

    return findings, {"rows": len(rows), "declined": False}


def check_file(path: str, require_section: bool) -> tuple[list[Finding], dict]:
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        return [Finding(path, "unreadable", str(exc))], {"rows": 0, "declined": False}

    text = COMMENT_RE.sub("", text)
    lines = text.splitlines()

    sections: list[tuple[int, int]] = []
    in_fence = False
    for n, line in enumerate(lines):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        heading = HEADING_RE.match(line)
        if not heading or not (2 <= len(heading.group(1)) <= 4):
            continue
        if SECTION_RE.match(heading.group(2)):
            sections.append((n, len(heading.group(1))))

    if not sections:
        if require_section:
            return [Finding(path, "missing",
                            "no '## Search record' section (--require-section)")], \
                   {"rows": 0, "declined": False}
        return [], {"rows": 0, "declined": True}

    findings: list[Finding] = []
    total_rows = 0
    for start, level in sections:
        found, stats = check_section(path, lines, start, level)
        findings.extend(found)
        total_rows += stats["rows"]
    return findings, {"rows": total_rows, "declined": False}


def main(argv: list[str]) -> int:
    as_json = "--json" in argv
    require_section = "--require-section" in argv
    paths = [a for a in argv if not a.startswith("--")]

    if not paths:
        print("usage: check-search-record.py [--json] [--require-section] <file> [...]", file=sys.stderr)
        return 2
    unknown = [a for a in argv if a.startswith("--") and a not in ("--json", "--require-section")]
    if unknown:
        print(f"check-search-record: unknown option {unknown[0]}", file=sys.stderr)
        return 2

    reports, failed = [], False
    for path in paths:
        findings, table = check_file(path, require_section)
        forced = len(findings) > 0
        failed = failed or forced
        reports.append({"file": path, "rows": table["rows"], "declined": table["declined"],
                        "findings": [str(f) for f in findings], "ok": not forced})
        if not as_json:
            for finding in findings:
                print(f"  FAIL     {finding}")
            if not forced and table["declined"]:
                print(f"  ok       {path}: no search record (optional; --require-section to demand one)")
            elif not forced:
                print(f"  ok       {path}: {table['rows']} recorded search(es), each with source, date, "
                      f"query and result")

    if as_json:
        print(json.dumps(reports, indent=2, sort_keys=True))
    elif failed:
        total = sum(len(r["findings"]) for r in reports)
        print(f"  FAIL     {total} finding(s) across {len(reports)} file(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
