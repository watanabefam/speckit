# Progress — plan: specs/007-plain-language/plan.md

Ledger for `specs/007-plain-language`. One line per task, evidence in parentheses.
`bin/speckit-resume` reads the plan identity from the first line and the tasks from here.

Task 1: complete (pre-change count 164, carried from the previous gate run of 2026-10-24; this feature's
gate reports 189, so the increase is 25 assertions ([SC-006]))
Task 2: complete (nine surfaces read: entry point, five step contributions, skill, autonomy contract,
installer bridge; each now carries the sentence that fits it)
Task 3: complete (`resolve-template.sh spec-template` contains `## In Plain Terms`; gate asserts the
template still requires it)
Task 4: complete (sections placed before the stories in 001–007, and `conformance: 14 conformant … 0
failure(s), 0 stale entr(ies)` — no ORDER finding, which is the assertion that matters)
Task 5: complete (`specify preset info` → 1.17.0; gate: "preset version is the newest CHANGELOG
release (1.17.0)")
Task 6: complete (`good` exits 0 with `6 rows, 6 identifiers covered`; `no-section` exits 1 with
`missing '## In Plain Terms'`)
Task 7: complete (fixture harness: `uncovered` → `FR-002 has no row`; `duplicate` → `SC-002 is covered
2 times`)
Task 8: complete (`python3 scripts/check-plain-terms.py evals/fixtures/plain-terms/good/spec.md` exits 0;
`uncovered` exits 1; `--json` prints the per-file report)
Task 9: complete (`vacuous` fixture exits 1 with `nothing was examined`; P-003 generates the same shape
three ways)
Task 10: complete (`commands` fixture exits 1 with `normative keyword MUST`; P-002 covers SHALL, MUST,
SHOULD at three positions and three benign cells, including `MUSTARD` and lower-case `must`)
Task 11: complete (`unglossed` → `'stale' has no bracketed gloss at first use`; `long-gloss` → `gloss is
30 words (cap 25)`)
Task 12: complete (7 specs report `4 terms glossed` or `3 terms glossed`; P-004 walks the paragraph
boundary at 1, 3, 24 and 40 words and one paragraph away)
Task 13: complete (`harness.py --all` → `PLAIN-TERMS: PASS 66 checks`; gate asserts ≥66 `ok` lines)
Task 14: complete (`bin/speckit-init` installed `.specify/scripts/check-plain-terms.py`; gate: "the
installed copy … matches the source")
Task 15: complete (gate §3e contributes 25 assertions: corpus, eight fixtures, teeth on a real spec,
harness count, nine policy surfaces, peer control)
Task 16: complete (001–003 pass the checker; `git diff` shows insertions only — no requirement line
changed)
Task 17: complete (004–006 pass; `conformance-baseline.py check` → `14 conformant, 5 excused, 0
failure(s), 0 stale entr(ies)`)
Task 18: complete (citekit `specs/001-web-search-source/spec.md` → exit 1, `no-section`; the peer scores
25/27 on section conformance, so it is a genuine negative control ([SC-002]))
Task 19: complete (gate asserts the rule string in all nine surfaces; each surface's copy is
surface-specific, not a pasted block)
Task 20: complete (`AGENTS.md` diff adds the plain-language paragraph inside the managed bridge)
Task 21: complete (`bin/speckit-init --no-mcp` → `updated preset: spec-driven-development 1.15.0 ->
1.17.0`, 13 commands recomposed; `.opencode/commands/speckit.specify.md` carries "In Plain Terms")
Task 22: complete (001 and 006 read end to end; one row repaired — 001's FR-001–FR-005 row claimed the
wrong shape is "rejected at review", which the requirement text does not say, and now states what the
requirement actually demands)
Task 23: complete (`bin/speckit-resume specs/007-plain-language` prints `COMPLETE`; every task above has
a line)
Task 24: complete (`make test` → `SELF-GATE: PASS examined=189 assertion(s)`, exit 0; committed on
`freebuff/df0ce130206f368964b24af5`)
Task 25: complete (P-001, 12 trials: grouped coverage passes, a dropped identifier is named, a repeat is
reported)
Task 26: complete (P-002, 9 keyword positions plus 3 benign cells and an unknown-id row)
Task 27: complete (P-003: no rows, and an id with no requirement, both fail; the control passes)
Task 28: complete (P-004: four gloss distances, a next-paragraph gloss and an unused term)

## What this feature does not claim

- The checker does not judge whether an explanation is correct or understood. `## In Plain Terms` says
  so, the script header says so, and the research companion says why: readability formulas do not
  measure comprehension, and a plain-language summary does not automatically improve it.
- The conversation half is policy, not enforcement. Nine surfaces carry the rule and the gate asserts
  their presence; nothing can assert that a reply was followed, which is the limit the constitution's
  Honest Enforcement principle already states.
- The six retrofits were written by the same author as the explanation's subject. Task 22's read-through
  is a review, not an independent one; a non-author pass is still outstanding.
- `./scripts/verify` now dispatches to the verification engine (the installer regenerated it) and
  reports `INCOMPLETE — nothing was examined, 1 vacuous check(s)` for the seeded one-check manifest.
  That is the engine being honest about a check with no negative control, not a pass; the gate evidence
  above is `make test`, which is the recorded test command.

## Open at close-out

- `Status` remains `Draft`: implementation proceeded on the owner's instruction to implement, and
  approval of the specification itself is still the owner's to give.
- The plan-layer question (should `plan.md` carry the same section?) is parked in the spec's future
  work, not decided here.
