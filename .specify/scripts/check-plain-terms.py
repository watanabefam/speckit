#!/usr/bin/env python3
"""check-plain-terms — assert a specification explains itself to a newcomer.

WHY THIS EXISTS
An owner reported the workflow was slow to use because the artifacts were hard to understand: 126
requirements across six documents, none of which said in ordinary words what it binds. The repair is an
informative `## In Plain Terms` section (see `preset/templates/spec-addendum.md` and
`decisions/0007-explanations-are-informative.md`). A section that is demanded but unverified rots: the
first requirement added without a row turns the table into a half-truth nobody notices. This checks the
two properties that are text, so the rest can be review.

OPTIONAL BY DEFAULT
The owner's ruling of 2026-10-25 narrowed this to a conversation rule: the artifacts are read by an
agent first, so a plainly written layer on `spec.md` and `plan.md` is a convenience, not an
obligation (`decisions/0009-the-rule-is-for-the-chat.md`). A document without `## In Plain Terms`
therefore passes, and says so — an absence is not a defect, and a check that failed every document
which never opted in would force the layer on projects that do not want it.

What is still enforced is the half that would otherwise rot: a document that *does* carry the section
must conform. Drift in a table nobody validates is worse than no table, because it reads as a promise.
`--require-section` demands one; a project that wants the layer everywhere puts that flag in its
verify manifest, and the kit's own fixtures use it to keep the failure path under test.

WHAT IT CHECKS (a document that carries the section)
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

A PLAN IS CHECKED FOR THE SAME THINGS, PLUS A POINTER
The `plan.md` artifact carries the same section and columns, and rules 4-7 apply unchanged. Three
things differ, and each exists because a plan is a design rather than a set of obligations (see
`decisions/0008-plans-explain-the-design.md`):

- **Placement.** The section must come before `## Technical Context` (or, where that heading is
  absent, before the first top-level section other than `## Summary`) — the guide level before the
  reference level.
- **The paragraph.** Three sentences, not two: a plan has to say what will be built, out of what,
  and why this shape.
- **The `Technical` cell.** It must name a section (`§…`) or a backticked artefact, and may not
  consist only of identifiers. A spec row points at the requirement it stands for; a plan row that
  did the same would send the reader back to the spec and say nothing about the design.

The mode is chosen by file name (`plan.md`), with `--kind` to override it. Mode affects those three
rules only; coverage, brevity, the keyword ban and the gloss rules are shared, so the two artifacts
cannot drift apart.

WHAT IT CANNOT DO
It cannot tell whether an explanation is correct, whether it says anything the requirement does not
already say, or whether a reader understood it. Nor can it tell whether a plan row states the design
choice rather than restating the requirement: that is the template's content rule, and review.

There is no oracle for either, and the evidence says a readability score would be a false one (AHRQ,
Schriver, Redish — `docs/research/plain-language-2026-10.md` §6). A covered-but-wrong row is a review
finding, not a gate failure. That limit is the reason this script checks coverage rather than quality.

VACUITY
A spec with the section but no rows fails as "nothing was examined", and so does a spec with no
identifiers at all. An empty table is the shape a ritual takes, and a check that passes on nothing is
not a check (the rule 005 states for the gate applies here).

Usage: check-plain-terms.py [--json] [--require-section] [--kind auto|spec|plan] <file> [...]
Exit:  0 = every file conformant, or declined (no section, not required) · 1 = at least one finding ·
       2 = usage or read error.
"""
from __future__ import annotations

import json
import os
import re
import sys

SECTION_RE = re.compile(r"^##\s+In Plain Terms\s*$")
PLAN_CONTEXT_RE = re.compile(r"^##\s+Technical Context\s*$")
SUMMARY_RE = re.compile(r"^##\s+Summary\s*$")
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

# The minimum opening paragraph, per artifact kind. A plan has one more job than a spec: it says what
# will exist, not only what is owed.
MIN_SENTENCES = {"spec": 2, "plan": 3}

REQUIRED_COLUMNS = ("item", "in plain words", "technical")
TERM_COLUMNS = ("term", "plain words")


class Finding:
    def __init__(self, path: str, kind: str, detail: str) -> None:
        self.path, self.kind, self.detail = path, kind, detail

    def __str__(self) -> str:
        return f"{self.path}: {self.kind}: {self.detail}"


def artifact_kind(path: str, override: str = "auto") -> str:
    """Which rule set applies. `--kind` wins; otherwise a `plan.md` basename means a plan.

    A file name is a weak signal, so the override exists and the template names it. Guessing from
    content was rejected: a plan that happens to lack `## Technical Context` would silently fall
    back to spec rules and pass under a contract it was never written against.
    """
    if override in MIN_SENTENCES:
        return override
    return "plan" if os.path.basename(path).lower() == "plan.md" else "spec"


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


def has_artefact(cell: str) -> bool:
    """A plan's Technical cell must point somewhere a reader can go: a section or a backticked path.

    The raw cell is inspected, not `norm()`ed, because normalisation strips the backticks this rule
    exists to find. An identifier alone is deliberately not enough: it is what the spec row already
    says, and it sends the reader back rather than into the design.
    """
    return "§" in cell or "`" in cell


def plan_placement_ok(lines: list[str], start: int) -> bool:
    """Above `## Technical Context`; failing that, nothing but `## Summary` may precede it."""
    context = next((i for i, l in enumerate(lines) if PLAN_CONTEXT_RE.match(l)), None)
    if context is not None:
        return start < context
    for line in lines[:start]:
        if HEADING_RE.match(line) and line.startswith("## ") and not SUMMARY_RE.match(line):
            return False
    return True


def check_file(path: str, kind: str = "spec", require_section: bool = False) -> tuple[list[Finding], dict]:
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
        # Optional by default (2026-10-25 ruling): declining the layer is not a finding. `declined`
        # travels in the table so the caller can say which of the two zero-finding outcomes it got —
        # "checked and clean" and "nothing to check" are different claims.
        if require_section:
            findings.append(Finding(path, "no-section",
                                    f"missing '## In Plain Terms' (see the {kind} template)"))
            return findings, table
        return [], {**table, "declined": kind}
    start, end = span

    # Placement: the explanation comes before the detail it explains.
    if kind == "plan":
        if not plan_placement_ok(lines, start):
            findings.append(Finding(path, "placement",
                                    "the section does not come before '## Technical Context'"))
    else:
        story_at = next((i for i, l in enumerate(lines) if STORY_RE.match(l)), None)
        if story_at is not None and story_at < start:
            findings.append(Finding(path, "placement",
                                    "the section comes after the first '### User Story' heading"))

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
    if sentence_count(prose) < MIN_SENTENCES[kind]:
        findings.append(Finding(path, "no-summary",
                                f"the section opens with fewer than {MIN_SENTENCES[kind]} sentences of prose"))

    # Identifiers the document uses. The section itself is excluded: a row mentioning an id must not
    # be what makes that id exist, or the table would validate itself.
    body_lines = lines[:start] + lines[end:]
    doc_ids: set[str] = set()
    for line in body_lines:
        scan = INLINE_CODE_RE.sub("", line)   # `FR-044` in an example is not a requirement
        # Expand closed ranges here too. A plan that says "covers FR-001–FR-012" in one line has
        # declared twelve requirements, and a plan's one-line scope statement is exactly how the
        # legacy plans name what they serve. Collecting only the range's endpoints would let eleven
        # of the twelve go uncovered while the table looked complete.
        doc_ids.update(expand_item(scan, [], path, "body"))
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
            technical = row[plain_idx["technical"]] if len(row) > plain_idx["technical"] else ""
            if not item.strip():
                findings.append(Finding(path, "empty-item", f"{where}: no identifier"))
            if not plain.strip():
                findings.append(Finding(path, "empty-plain", f"{where}: no explanation"))
                continue
            if kind == "plan" and not has_artefact(technical):
                findings.append(Finding(path, "no-artefact",
                                        f"{where}: the Technical cell names no section (§) or file"))
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
    require_section = "--require-section" in argv
    kind = "auto"
    rest: list[str] = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--kind":
            if i + 1 >= len(argv):
                print("check-plain-terms: --kind needs a value (auto, spec or plan)", file=sys.stderr)
                return 2
            kind = argv[i + 1]
            i += 2
            continue
        if arg.startswith("--kind="):
            kind = arg.split("=", 1)[1]
        elif arg not in ("--json", "--require-section"):
            rest.append(arg)
        i += 1

    if kind not in ("auto", "spec", "plan"):
        print(f"check-plain-terms: unknown --kind '{kind}' (auto, spec or plan)", file=sys.stderr)
        return 2
    paths = rest
    if not paths:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        print("usage: check-plain-terms.py [--json] [--require-section] [--kind auto|spec|plan] <file> [...]",
              file=sys.stderr)
        return 2

    reports, failed = [], False
    for path in paths:
        findings, table = check_file(path, artifact_kind(path, kind), require_section)
        forced = len(findings) > 0
        failed = failed or forced
        reports.append({"table": table, "findings": [str(f) for f in findings], "ok": not forced})
        if not as_json:
            for finding in findings:
                print(f"  FAIL     {finding}")
            if not forced and table.get("declined"):
                print(f"  ok       {path}: no plain layer (optional; --require-section to demand one)")
            elif not forced:
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
