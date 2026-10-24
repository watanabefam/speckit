#!/usr/bin/env python3
"""check-plain-terms — assert a specification explains itself to a newcomer.

WHY THIS EXISTS
An owner reported the workflow was slow to use because the artifacts were hard to understand: 126
requirements across six documents, none of which said in ordinary words what it binds. The repair is an
informative `## In Plain Terms` section (see `preset/templates/spec-addendum.md` and
`decisions/0007-explanations-are-informative.md`). A section that is demanded but unverified rots: the
first requirement added without a row turns the table into a half-truth nobody notices. This checks the
two properties that are text, so the rest can be review.

WHAT IT CHECKS
1. The section exists, and it comes before the first `### User Story` heading.
2. It opens with at least two sentences of prose before any table.
3. A table whose header carries `Item`, `In plain words` and `Technical` exists.
4. Every `US`, `FR` and `SC` identifier in the document is covered by exactly one row. An `Item` cell
   may list identifiers comma-separated or as a closed range (`FR-001–FR-006`, `FR-001-FR-006`,
   `FR-001...FR-006`, `FR-001–006`).
5. No `In plain words` cell contains `SHALL`, `MUST` or `SHOULD` (upper case only: `must` in prose is
   not a normative keyword, and a substring match would fail `MUSTARD`).
6. No `In plain words` cell exceeds 45 words — a brevity proxy, never a readability score.
7. A terms table (`Term`, `Plain words`) exists; every listed term is used somewhere in the document's
   prose at or after this section, is followed by a bracketed gloss at its first prose use in the same
   paragraph, and that gloss is at most 25 words. Table lines are skipped when looking for the first
   use (listing a term is not introducing it), and so is everything above the section: a reader is
   introduced to the vocabulary here, and the metadata block — which may quote the requester verbatim —
   is not where a gloss belongs.

WHAT IT CANNOT DO
It cannot tell whether an explanation is correct, whether it says anything the requirement does not
already say, or whether a reader understood it. There is no oracle for those, and the evidence says a
readability score would be a false one (AHRQ, Schriver, Redish —
`docs/research/plain-language-2026-10.md` §6). A covered-but-wrong row is a review finding, not a gate
failure. That limit is the reason this script checks coverage rather than quality.

VACUITY
A spec with the section but no rows fails as "nothing was examined", and so does a spec with no
identifiers at all. An empty table is the shape a ritual takes, and a check that passes on nothing is
not a check (the rule 005 states for the gate applies here).

Usage: check-plain-terms.py [--json] <spec.md> [<spec.md> ...]
Exit:  0 = every file conformant · 1 = at least one finding · 2 = usage or read error.
"""
from __future__ import annotations

import json
import re
import sys

SECTION_RE = re.compile(r"^##\s+In Plain Terms\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s")
STORY_RE = re.compile(r"^###\s+User Story\s+(\d+)\b")
IDENT_RE = re.compile(r"\b(FR|SC)-(\d{3})\b")
US_RE = re.compile(r"\bUS(\d+)\b")
FENCE_RE = re.compile(r"^\s*```")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)

PLAIN_LIMIT = 45
GLOSS_LIMIT = 25
NORMATIVE_RE = re.compile(r"\b(SHALL|MUST|SHOULD)\b")

REQUIRED_COLUMNS = ("item", "in plain words", "technical")
TERM_COLUMNS = ("term", "plain words")


class Finding:
    def __init__(self, path: str, kind: str, detail: str) -> None:
        self.path, self.kind, self.detail = path, kind, detail

    def __str__(self) -> str:
        return f"{self.path}: {self.kind}: {self.detail}"


def norm(cell: str) -> str:
    return re.sub(r"\s+", " ", cell.strip().strip("*`")).lower()


def cells(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [c.strip() for c in body.split("|")]


def is_separator(line: str) -> bool:
    return bool(re.fullmatch(r"\|?[\s:|-]+\|?", line.strip())) and "---" in line


def unfenced(lines: list[str]) -> list[str]:
    """Blank out fenced blocks: a shell comment is not a heading, a code line is not prose."""
    out, infence = [], False
    for line in lines:
        if FENCE_RE.match(line):
            infence = not infence
            out.append("")
            continue
        out.append("" if infence else line)
    return out


def find_section(lines: list[str]) -> tuple[int, int] | None:
    """Return [start, end) of the section body, or None when the heading is absent."""
    start = None
    for i, line in enumerate(lines):
        if SECTION_RE.match(line):
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        m = HEADING_RE.match(lines[j])
        if m and len(m.group(1)) <= 2:
            end = j
            break
    return start, end


def parse_tables(lines: list[str]) -> list[tuple[list[str], list[list[str]]]]:
    """Every markdown table in `lines`, as (header, rows). A table needs a separator row."""
    tables, i = [], 0
    while i < len(lines):
        if lines[i].strip().startswith("|"):
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i])
                i += 1
            if len(block) >= 2 and is_separator(block[1]):
                tables.append((cells(block[0]), [cells(l) for l in block[2:]]))
        else:
            i += 1
    return tables


def column_index(header: list[str], names: tuple[str, ...]) -> dict[str, int] | None:
    """Map each required column name to its index. A header cell may carry extra words —
    'Technical wording it stands for' satisfies 'technical' — because demanding the exact cell made a
    correct table report as 'no table at all', which is the least fixable message a check can give."""
    cells_norm = [(norm(h), n) for n, h in enumerate(header)]
    found: dict[str, int] = {}
    for name in names:
        hit = next((n for key, n in cells_norm if name in key), None)
        if hit is None:
            return None
        found[name] = hit
    return found


def expand_item(cell: str, findings: list[Finding], path: str, where: str) -> list[str]:
    """Ids named by an Item cell: comma lists, US tokens, and closed ranges in four spellings."""
    ids: list[str] = []
    for m in US_RE.finditer(cell):
        ids.append(f"US{int(m.group(1))}")
    # Ranges first, so the endpoints are not counted twice.
    consumed: list[tuple[int, int]] = []
    range_re = re.compile(
        r"\b(FR|SC)-(\d{3})\s*(?:–|—|-|\.\.\.)\s*(?:(FR|SC)-)?(\d{3})\b"
    )
    for m in range_re.finditer(cell):
        lo, hi = int(m.group(2)), int(m.group(4))
        prefix = m.group(1)
        if m.group(3) and m.group(3) != prefix:
            findings.append(Finding(path, "bad-range", f"{where}: '{m.group(0)}' mixes {m.group(1)} and {m.group(3)}"))
            consumed.append(m.span())
            continue
        consumed.append(m.span())
        if lo > hi:
            findings.append(Finding(path, "bad-range", f"{where}: '{m.group(0)}' runs backwards"))
            continue
        ids.extend(f"{prefix}-{n:03d}" for n in range(lo, hi + 1))
    for m in IDENT_RE.finditer(cell):
        if any(a <= m.start() < b for a, b in consumed):
            continue
        ids.append(f"{m.group(1)}-{m.group(2)}")
    return ids


def sentence_count(text: str) -> int:
    return len([s for s in re.split(r"[.!?](?:\s|$)", text.strip()) if s.strip()])


def gloss_after(paragraph: str, start: int) -> tuple[str, int] | None:
    """The first bracket after `start` in `paragraph`: (content, word count), or None."""
    open_at = paragraph.find("(", start)
    if open_at == -1:
        return None
    close_at = paragraph.find(")", open_at)
    if close_at == -1:
        return None
    content = paragraph[open_at + 1:close_at].strip()
    return content, len(content.split())


def check_file(path: str) -> tuple[list[Finding], dict]:
    findings: list[Finding] = []
    try:
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
    except OSError as exc:
        raise SystemExit(f"check-plain-terms: cannot read {path}: {exc}")

    lines = unfenced(raw.splitlines())
    table = {"artifact": path, "rows": 0, "covered": 0, "terms": 0}

    span = find_section(lines)
    if span is None:
        findings.append(Finding(path, "no-section", "missing '## In Plain Terms' (see the spec template)"))
        return findings, table
    start, end = span

    # Placement: the explanation comes before the first story.
    story_at = next((i for i, l in enumerate(lines) if STORY_RE.match(l)), None)
    if story_at is not None and story_at < start:
        findings.append(Finding(path, "placement", "the section comes after the first '### User Story' heading"))

    body = [COMMENT_RE.sub("", l) for l in lines[start + 1:end]]
    tables = parse_tables(body)

    plain_idx = next((column_index(h, REQUIRED_COLUMNS) for h, _ in tables if column_index(h, REQUIRED_COLUMNS)), None)
    terms_idx = next((column_index(h, TERM_COLUMNS) for h, _ in tables if column_index(h, TERM_COLUMNS)), None)

    if plain_idx is None:
        findings.append(Finding(path, "no-table", "no table with columns 'Item', 'In plain words', 'Technical'"))
    if terms_idx is None:
        findings.append(Finding(path, "no-terms", "no table with columns 'Term', 'Plain words'"))

    # The paragraph before the first table.
    first_table = next((i for i, l in enumerate(body) if l.strip().startswith("|")), len(body))
    prose = " ".join(l.strip() for l in body[:first_table] if l.strip())
    if sentence_count(prose) < 2:
        findings.append(Finding(path, "no-summary", "the section opens with fewer than two sentences of prose"))

    # Identifiers the document uses. The section itself is excluded: a row mentioning an id must not
    # be what makes that id exist, or the table would validate itself.
    body_lines = lines[:start] + lines[end:]
    doc_ids: set[str] = set()
    for line in body_lines:
        scan = INLINE_CODE_RE.sub("", line)   # `FR-044` in an example is not a requirement
        for m in IDENT_RE.finditer(scan):
            doc_ids.add(f"{m.group(1)}-{m.group(2)}")
        m = STORY_RE.match(scan)
        if m:
            doc_ids.add(f"US{int(m.group(1))}")

    covered: dict[str, int] = {}
    rows = 0
    if plain_idx is not None:
        header, data = next(h for h in tables if column_index(h[0], REQUIRED_COLUMNS))
        for n, row in enumerate(data):
            if not any(c for c in row):
                continue
            rows += 1
            where = f"row {n + 1}"
            item = row[plain_idx["item"]] if len(row) > plain_idx["item"] else ""
            plain = row[plain_idx["in plain words"]] if len(row) > plain_idx["in plain words"] else ""
            if not item.strip():
                findings.append(Finding(path, "empty-item", f"{where}: no identifier"))
            if not plain.strip():
                findings.append(Finding(path, "empty-plain", f"{where}: no explanation"))
                continue
            for ident in expand_item(item, findings, path, where):
                covered[ident] = covered.get(ident, 0) + 1
            width = len(plain.split())
            if width > PLAIN_LIMIT:
                findings.append(Finding(path, "long-cell", f"{where}: {width} words (cap {PLAIN_LIMIT})"))
            for m in NORMATIVE_RE.finditer(plain):
                findings.append(Finding(path, "commands", f"{where}: normative keyword {m.group(1)} in an explanation"))

    for ident in sorted(doc_ids - set(covered)):
        findings.append(Finding(path, "uncovered", f"{ident} has no row"))
    for ident in sorted(k for k, v in covered.items() if v > 1):
        findings.append(Finding(path, "duplicate", f"{ident} is covered {covered[ident]} times"))
    for ident in sorted(set(covered) - doc_ids):
        findings.append(Finding(path, "unknown", f"{ident} is covered but not in the document"))

    if not doc_ids and rows == 0:
        findings.append(Finding(path, "vacuous", "no identifiers and no rows — nothing was examined"))

    table.update(rows=rows, covered=len(set(covered) & doc_ids) if doc_ids else 0)

    # Terms: listed, used, glossed at first use, and short enough to be a gloss.
    term_rows = 0
    if terms_idx is not None:
        header, data = next(h for h in tables if column_index(h[0], TERM_COLUMNS))
        # First *prose* use, from this section onward: table lines and headings are blanked. Listing a
        # term does not introduce it, a heading is a label rather than a sentence, and the metadata
        # above the section (status, and often a verbatim quote of the requester) is not where a reader
        # is introduced — nor may a gloss be edited into a quotation.
        prose_body = "\n".join(
            "" if l.strip().startswith("|") or HEADING_RE.match(l) else l for l in lines[start:])
        prose_body = INLINE_CODE_RE.sub("", COMMENT_RE.sub("", prose_body))
        for n, row in enumerate(data):
            if not any(c for c in row):
                continue
            term_rows += 1
            term = row[terms_idx["term"]] if len(row) > terms_idx["term"] else ""
            term = term.strip().strip("*`")
            if not term:
                findings.append(Finding(path, "empty-term", f"terms row {n + 1}: no term"))
                continue
            # A term is listed in the singular and matched with an optional plural ending: a gloss on
            # "semantic defects" introduces "semantic defect", and failing that would teach authors to
            # list plurals instead of fixing anything.
            use = re.search(r"(?<![\w-])" + re.escape(term) + r"(?:s|es)?(?![\w-])", prose_body, re.I)
            if use is None:
                findings.append(Finding(path, "stale-term", f"'{term}' is listed but never used in the body"))
                continue
            para_start = prose_body.rfind("\n\n", 0, use.start()) + 2
            para_end = prose_body.find("\n\n", use.end())
            para_end = len(prose_body) if para_end == -1 else para_end
            paragraph = prose_body[para_start:para_end]
            offset = use.end() - para_start
            gloss = gloss_after(paragraph, offset)
            if gloss is None:
                findings.append(Finding(path, "unglossed", f"'{term}' has no bracketed gloss at first use"))
            elif gloss[1] > GLOSS_LIMIT:
                findings.append(Finding(path, "long-gloss", f"'{term}': gloss is {gloss[1]} words (cap {GLOSS_LIMIT})"))

    table["terms"] = term_rows
    return findings, table


def main(argv: list[str]) -> int:
    as_json = "--json" in argv
    paths = [a for a in argv if a != "--json"]
    if not paths:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        print("usage: check-plain-terms.py [--json] <spec.md> [...]", file=sys.stderr)
        return 2

    reports, failed = [], False
    for path in paths:
        findings, table = check_file(path)
        forced = len(findings) > 0
        failed = failed or forced
        reports.append({"table": table, "findings": [str(f) for f in findings], "ok": not forced})
        if not as_json:
            for finding in findings:
                print(f"  FAIL     {finding}")
            if not forced:
                print(f"  ok       {path}: {table['rows']} rows, {table['covered']} identifiers covered, "
                      f"{table['terms']} terms glossed")

    if as_json:
        print(json.dumps(reports, indent=2, sort_keys=True))
    elif failed:
        bad = sum(len(r["findings"]) for r in reports)
        print(f"  FAIL     {bad} finding(s) across {len(reports)} file(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
