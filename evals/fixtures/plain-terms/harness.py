#!/usr/bin/env python3
"""Fixture harness for `scripts/check-plain-terms.py`.

Eight fixtures, each of which must fail (or pass, for the control) for one named reason, plus four
properties that generate documents instead of reading them. The discipline is the one
`evals/fixtures/verify/harness.py` already uses: a check that has never been observed failing is not
evidence, so every failure shape below was written before the checker was.

Usage:
  harness.py --all                  every case and property
  harness.py --case <name>          one fixture
  harness.py --property P-00n       one property
  harness.py --list                 names only

Exit: 0 = all selected checks passed · 1 = at least one failed · 2 = usage error.
"""
from __future__ import annotations

import argparse
import importlib.util
import random
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CHECKER = ROOT / "scripts" / "check-plain-terms.py"

CASES = {
    # name: (expected exit, expected substring of the finding)
    "good": (0, "ok"),
    "no-section": (1, "missing '## In Plain Terms'"),
    "uncovered": (1, "FR-002 has no row"),
    "duplicate": (1, "SC-002 is covered 2 times"),
    "commands": (1, "normative keyword MUST"),
    "unglossed": (1, "'stale' has no bracketed gloss"),
    "long-gloss": (1, "gloss is 30 words"),
    "vacuous": (1, "nothing was examined"),
}

failures: list[str] = []
checks = 0


def load_checker():
    spec = importlib.util.spec_from_file_location("plain_terms", CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def report(ok: bool, label: str, detail: str = "") -> None:
    global checks
    checks += 1
    if ok:
        print(f"  ok       {label}")
    else:
        print(f"  FAIL     {label}{(' — ' + detail) if detail else ''}")
        failures.append(label)


def run_case(name: str) -> None:
    want_exit, needle = CASES[name]
    path = HERE / name / "spec.md"
    proc = subprocess.run(
        [sys.executable, str(CHECKER), str(path)], capture_output=True, text=True
    )
    out = proc.stdout + proc.stderr
    report(
        proc.returncode == want_exit and needle in out,
        f"case {name}",
        f"exit {proc.returncode} (want {want_exit}), output: {out.strip()[:200]}",
    )


# --------------------------------------------------------------------------------------------
# Generators for the properties. Each builds a whole specification, because the rules are about a
# document: a fragment would let a defect hide in the part that was not generated.
# --------------------------------------------------------------------------------------------

def plain_cell(text: str) -> str:
    return text


def build(ids: list[str], rows: list[tuple[str, str, str]], terms=("fixture-value",),
          gloss="plain words",
          term_use="The fixture-value (a generated stand-in) is used here.") -> str:
    lines = ["# Generated specification", "", "## In Plain Terms", "",
             "This fixture exists to exercise the checker. It is generated, and it says nothing else.",
             "", "| Item | In plain words | Technical |", "| --- | --- | --- |"]
    for item, plain, technical in rows:
        lines.append(f"| {item} | {plain} | {technical} |")
    if terms:
        lines += ["", "**Terms**", "", "| Term | Plain words |", "| --- | --- |"]
        for term in terms:
            lines.append(f"| {term} | {gloss} |")
    lines += ["", "## User Scenarios & Testing", ""]
    if terms:
        lines += [term_use, ""]
    for ident in ids:
        if ident.startswith("US"):
            lines += [f"### User Story {ident[2:]} - Generated", "",
                      "A generated story with one acceptance scenario.", ""]
        else:
            lines.append(f"- **{ident}**: Generated text for {ident}.")
    return "\n".join(lines) + "\n"


def check_text(module, text: str):
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as fh:
        fh.write(text)
        path = fh.name
    findings, table = module.check_file(path)
    Path(path).unlink()
    return findings, table


def kinds(findings) -> list[str]:
    return [f.kind for f in findings]


def p_001(module, rng: random.Random) -> None:
    """Coverage is total and unique, in both directions."""
    for trial in range(12):
        n = rng.randint(1, 8)
        ids = [f"FR-{i:03d}" for i in range(1, n + 1)]
        rng.shuffle(ids)
        groups, cursor = [], 0
        while cursor < n:
            size = rng.randint(1, min(3, n - cursor))
            groups.append(ids[cursor:cursor + size])
            cursor += size
        rows = [(", ".join(g), f"Explanation {k + 1} for a generated group.", ", ".join(g))
                for k, g in enumerate(groups)]
        findings, _ = check_text(module, build(ids, rows))
        report(not findings, f"P-001 trial {trial}: grouped coverage passes", str(kinds(findings)))

        # Drop one identifier from the rows: the check must name it.
        victim = ids[rng.randrange(n)]
        dropped = [r for r in rows if victim not in r[0].split(", ")]
        findings, _ = check_text(module, build(ids, dropped))
        report("uncovered" in kinds(findings) and any(victim in f.detail for f in findings),
               f"P-001 trial {trial}: a missing {victim} is named", str(kinds(findings)))

        # Cover one identifier twice: duplicate, not silence.
        copy = list(rows) + [(ids[0], "The same identifier, explained again.", ids[0])]
        findings, _ = check_text(module, build(ids, copy))
        report("duplicate" in kinds(findings), f"P-001 trial {trial}: a repeat is reported",
               str(kinds(findings)))


def p_002(module, rng: random.Random) -> None:
    """A normative keyword is a failure in any sentence; case and substrings are not keywords."""
    ids = ["FR-001"]
    for keyword in ("SHALL", "MUST", "SHOULD"):
        for position in ("start", "middle", "end"):
            cell = {
                "start": f"{keyword} be served.",
                "middle": f"The cache {keyword} be served.",
                "end": f"The cache is served, {keyword}.",
            }[position]
            findings, _ = check_text(module, build(ids, [("FR-001", cell, "FR-001")]))
            report("commands" in kinds(findings), f"P-002 {keyword} at {position} fails",
                   str(kinds(findings)))
    for benign in ("The cache must be served.", "A MUSTARD seed is not a keyword.",
                   "It shouldered the load."):
        findings, _ = check_text(module, build(ids, [("FR-001", benign, "FR-001")]))
        report(not findings, f"P-002 benign cell passes: {benign[:24]}…", str(kinds(findings)))

    # An identifier that is not in the document is reported, not silently counted.
    findings, _ = check_text(module, build(["FR-001"], [("FR-001", "Fine.", "FR-001"),
                                                       ("FR-009", "Invented.", "FR-009")]))
    report("unknown" in kinds(findings), "P-002/coverage: a row for an absent id is reported",
           str(kinds(findings)))


def p_003(module, rng: random.Random) -> None:
    """Silence is failure: no rows, or no identifiers at all."""
    text = build([], [])
    findings, _ = check_text(module, text)
    report("vacuous" in kinds(findings), "P-003 a section with no rows fails", str(kinds(findings)))

    text = build([], [("FR-001", "An explanation with nothing to explain.", "FR-001")])
    findings, _ = check_text(module, text)
    report("unknown" in kinds(findings), "P-003 an id with no requirement fails", str(kinds(findings)))

    # And the control: the same shape with one real identifier passes.
    findings, _ = check_text(module, build(["FR-001"], [("FR-001", "One explained thing.", "FR-001")]))
    report(not findings, "P-003 control: one identifier and one row passes", str(kinds(findings)))


def p_004(module, rng: random.Random) -> None:
    """A gloss must be local and short; the boundary is the paragraph."""
    ids = ["FR-001"]
    for distance, want in ((1, True), (3, True), (24, True), (40, False)):
        filler = " ".join(["word"] * (distance - 1)) if distance > 1 else ""
        use = f"not stale ({filler} explained)" if filler else "not stale (explained)"
        findings, _ = check_text(module, build(ids, [("FR-001", "Explained.", "FR-001")],
                                               terms=("stale",), term_use=use))
        got = "unglossed" not in kinds(findings) and "long-gloss" not in kinds(findings)
        report(got is want, f"P-004 gloss at {distance} words -> {'pass' if want else 'fail'}",
               str(kinds(findings)))

    # The next paragraph is not "first use": the gloss must travel with the term.
    text = build(ids, [("FR-001", "Explained.", "FR-001")], terms=("stale",),
                 term_use="not stale.\n\nLater, stale (gloss).")
    findings, _ = check_text(module, text)
    report("unglossed" in kinds(findings), "P-004 a gloss in the next paragraph does not count",
           str(kinds(findings)))

    # A term listed but never used is a stale entry, not a silent pass.
    findings, _ = check_text(module, build(ids, [("FR-001", "Explained.", "FR-001")],
                                           terms=("absent-term",), term_use="nothing here"))
    report("stale-term" in kinds(findings), "P-004 an unused listed term is reported",
           str(kinds(findings)))


PROPERTIES = {"P-001": p_001, "P-002": p_002, "P-003": p_003, "P-004": p_004}


def main() -> int:
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--case")
    parser.add_argument("--property")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()

    if args.list:
        print("cases: " + ", ".join(CASES))
        print("properties: " + ", ".join(PROPERTIES))
        return 0
    if not (args.all or args.case or args.property):
        parser.print_usage()
        return 2
    if args.case and args.case not in CASES:
        print(f"unknown case '{args.case}'; have: {', '.join(CASES)}", file=sys.stderr)
        return 2
    if args.property and args.property not in PROPERTIES:
        print(f"unknown property '{args.property}'; have: {', '.join(PROPERTIES)}", file=sys.stderr)
        return 2

    module = load_checker()
    rng = random.Random(20261024)

    if args.all or args.case:
        for name in CASES:
            if args.case is None or args.case == name:
                run_case(name)
    if args.all or args.property:
        for name, fn in PROPERTIES.items():
            if args.property is None or args.property == name:
                fn(module, rng)

    print()
    if failures:
        print(f"PLAIN-TERMS: FAIL {len(failures)} of {checks} checks")
        return 1
    print(f"PLAIN-TERMS: PASS {checks} checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
