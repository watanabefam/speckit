# 0011 — A declared count beats a scraped one, and the run ledger travels with the repository

## Context

`decisions/0010` left two questions parked, and the owner has now answered both.

**1. The `make` adapter cannot read `examined=`.** Feature 005's engine has one adapter per runner, and the
`make` adapter reads a runner's pass/fail summary (`3 passed`). This repository's `make test` is a gate that
prints `SELF-GATE: PASS examined=218 assertion(s)` and no summary of that shape, so `runner: make` reported
`examined unknown` and the verdict was `INCOMPLETE` even with a working control. 0010 worked around it by
declaring `runner: command`, which is a manifest lie: the check runs `make test`, and the manifest said the
runner was something else.

**2. `.specify/ledger.jsonl` was untracked and not ignored.** The engine's own verdict line reads
`record: .specify/ledger.jsonl#<id>`, which is a claim that a result was written down. On one machine only,
that claim is not checkable by anyone else, and FR-012's duplicate-id check has nothing to compare across
people.

## Research

**A count should be declared, not inferred.** TAP — the oldest portable test-output protocol, and the one most
harnesses still imitate — begins with a *plan* line, `1..N`, stating how many test units the run intends to
report; the consumer reads the plan rather than counting prose (`testanything.org/tap-specification.html`). The
same idea appears in the engine's own `--json` record: the count is a field, not a sentence someone parsed.

**Merging an append-only file is a solved problem, and the answer is not `merge=union`.** Git's own
`gitattributes(5)` describes the built-in `union` driver as taking "lines from both versions, instead of leaving
conflict markers", and warns: "This tends to leave the added lines in the resulting file in random order and the
user should verify the result. Do not use this if you do not understand the implications." (git 2.56.0,
`Documentation/gitattributes.adoc`). Random order is survivable here — `speckit-ledger` sorts by (`at`, `id`) —
but the warning describes the wrong guarantee for an audit trail: union accepts whatever each side has, and an
*erasure* on one side is absorbed without a conflict. Erasure is the one edit this file exists to prevent.

**The canonical tool for this class of file treats removal as a conflict.** GNULib's `git-merge-changelog`
(Bruno Haible) exists because Git's default driver "always produces conflicts when pulling public modifications
into a privately modified ChangeLog file", since ChangeLogs are always modified at the top. It merges *entries*
rather than lines, keeps additions from both sides, and — the relevant part — a removal applied to a file that
no longer matches is "marked as a conflict", with conflicts moved to the top of the file so they cannot be
missed (`git-merge-changelog(1)`). Additions merge; deletions surface. That is the semantic this ledger wants,
and it is the semantic 005 already has in reading (sort by timestamp) and checking (duplicate ids fail).

**What CiteKit could not answer.** The scholarly lane (OpenAlex, Crossref, DOAJ, PubMed, ERIC) has no literature
on either question — it is an education/biomed corpus, and its hits for "parsing test runner output" were
off-topic (the closest, Gyori 2017, is about *test outcome reliability and flakiness*, not count extraction).
Recording that instead of dressing an unrelated record as support. The web lane surfaced the git and TAP
sources above; `docs/research/verification-tooling-2026-10.md` already carries the counting/vacuity background.

These agree with feature 005's standing invariant — *never invent a count* — and they settle the two shapes
below without adding a third mechanism.

## Decision

**1. The adapters prefer a declared count over a scraped one.** `declared_examined()` (`bin/speckit-verify`)
reads `examined=N` and is used by both the `make` and `command` adapters:

| Output | `examined` | Why |
| --- | --- | --- |
| one `examined=7` line | 7 | the command stated its own count |
| `2 passed` and `examined=5` | 5 | different units (tests run vs assertions evaluated); the declaration is the one written for this check |
| `examined=4` and `examined=9` | unknown, both named | two answers to one question; the engine does not choose |
| `examined=0` | zero-examined state | a declared zero is a statement, not a pass |
| only `3 passed` | 3 | unchanged behaviour: the summary is still read when nothing is declared |
| nothing recognisable | unknown | `INCOMPLETE`, never `PASS` |

The last declaration wins, because a wrapper prints its summary at the end, so text a test echoes earlier
cannot override the real line.

**2. This repository's manifest declares the runner it actually uses.** `.specify/verify.json` now says
`runner: "make"` for `make test`, deleting 0010's workaround. The manifest's whole point is that a reader can
check what a check runs; a field that exists to route around an adapter bug is a lie the file does not need any
more.

**3. `.specify/ledger.jsonl` is committed.** One record per line, additions only, read in (`at`, `id`) order so
merge order does not matter (FR-013). No `merge=union`: git's own documentation says the result is unordered
without verification, and an erasure would be absorbed silently. The merge rule is the one
`git-merge-changelog` encodes for this kind of file — **keep both sides' lines, never delete one** — and
`speckit-ledger verify` is what proves the file is still well-formed afterwards (duplicate ids, `PASS` with
`examined=0`, schema violations).

**4. A record made on a dirty tree is a record of that tree, not of a commit.** The fingerprint is a sha256 over
the `HEAD` tree plus the working-tree diff (FR-011), so after the change is committed the record no longer
matches anything checkable. The record that can be pointed at from outside is the one taken on a clean tree
after committing; that is stated here rather than left for a reader to discover.

## Consequences

- `runner: make` with a declared count now yields `examined=218` and `PASS`. The condition 0010 had to route
  around is gone, and so is the routing.
- A `make` target that scrapes `pytest` and prints its own assertion count is now read correctly instead of
  being mislabelled "unknown", which is the case an adopter is most likely to have.
- The ledger's history becomes part of every diff, and two people running `verify` on divergent branches will
  conflict on the same tail. The resolution is mechanical (keep both) and checkable, which is the trade being
  made: an audit trail that cannot be lost quietly is worth a conflict that takes one command to settle.
- The harness case `make-declared` asserts all five rows of the table above, and it runs inside the gate's §12
  through `harness.py --all`, so a regression names the case.

## Rejected alternatives

- **`merge=union`.** Git documents that the union is unordered and needs human verification; a deleted line
  survives as a deletion. The reader's sort fixes the ordering half and nothing fixes the erasure half.
- **One file per record.** Conflict-free by construction, and the direction GitLab took for its changelog
  (placeholders instead of a shared append point). Rejected because FR-010/FR-013 and `speckit-ledger` are
  written against one file, and a directory of records moves the conflict from git to "which file is the
  truth" — a worse problem than the one it solves.
- **Treat a summary and a declaration that differ as ambiguous.** They legitimately differ: `12 passed` counts
  tests, `examined=218` counts assertions. Comparing them would report "unknown" on every correct wrapper.
- **Leave the adapter alone.** Then every adopter whose `make test` ends in a declared count gets
  `INCOMPLETE` forever, and their response is to stop reading the verdict — the failure mode 005 exists to
  prevent.

## What this does not claim

- It does not make a count trustworthy. A wrapper can print `examined=999` it did not earn; no parser can tell.
  The guard is the negative control (`decisions/0010`), which is why the count is worth having *beside* a
  control and not instead of one.
- Committing one repository's run history is not a general policy for machine-written logs; it is a fit for a
  file whose records are immutable, individually identified, and ordered by their own timestamp.
- The ledger is evidence of runs, not of correctness. A `PASS` record says the checks ran and what they
  examined; whether those checks were worth running is FR-004/FR-005's question, and a record inherits their
  answers rather than proving them.
