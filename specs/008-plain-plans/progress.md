# Progress — plan: specs/008-plain-plans/plan.md

Ledger for `specs/008-plain-plans`. One line per task, evidence in parentheses.
`bin/speckit-resume` reads the plan identity from the first line and the tasks from here.

Task 1: complete (pre-change baseline `SELF-GATE: PASS examined=189`, carried from 007's close-out; this
feature's gate reports 206, so the increase is 17 assertions ([SC-006]))
Task 2: complete (five surfaces read before editing: plan template, plan contribution, gate §3e block,
installer copy step, conformance baseline)
Task 3: complete (`preset/templates/plan-addendum.md` carries `## In Plain Terms`; gate §3f asserts the
template still requires it)
Task 4: complete (`check-section-integrity.sh` already waived the heading name from 007; conformance on
`specs/008-plain-plans/plan.md` reports `all 44 required sections present, in template order, none
empty` — no ORDER finding, which is the assertion that matters)
Task 5: complete (`specify preset info` → 1.18.0; gate: preset version matches the newest CHANGELOG
release `1.18.0`)
Task 6: complete (`plan-good` exits 0 with `3 rows, 4 identifiers covered`; `plan-no-section` exits 1 with
`missing '## In Plain Terms' (see the plan template)`)
Task 7: complete (`plan-misplaced` → `does not come before '## Technical Context'`;
`plan-thin-paragraph` → `fewer than 3 sentences of prose`)
Task 8: complete (`--kind auto|spec|plan` parsed; auto reads the basename; an unknown value exits 2;
`plan-good` 0, `plan-misplaced` 1, and the 8 spec fixtures keep their previous exit codes)
Task 9: complete (coverage shared; body ranges expand — `P-008` shows a `FR-001–FR-012` scope line and
grouped rows cover all twelve, while covering only the endpoints names `FR-002`)
Task 10: complete (`plan-no-artefact` exits 1 with `row 1: the Technical cell names no section (§) or
file`; the raw cell is inspected so backticks survive)
Task 11: complete (a 50-word `In plain words` cell in a copy of this plan → `long-cell: row 9: 50 words
(cap 45)`, so the shared brevity rule runs in plan mode)
Task 12: complete (`plan-unglossed` exits 1 with `'manifest' has no bracketed gloss at first use`)
Task 13: complete (the terms table, first-prose-use rule and 25-word cap are the spec implementation,
called from both modes; `plan-good` reports `1 terms glossed`)
Task 14: complete (`harness.py --all` → `PLAIN-TERMS: PASS 91 checks`: 8 spec cases, 6 plan cases,
9 properties; gate asserts ≥91)
Task 15: complete (`bin/speckit-init` copied the updated checker to `.specify/scripts/`; gate: the
installed copy matches the source)
Task 16: complete (gate §3f contributes 17 assertions: template, corpus of 7 plans, 6 fixtures, teeth on
a real plan, the mode-is-a-branch check, 6 policy surfaces, peer plan control; gate green)
Task 17: complete (`specs/001`, `002`, `003` plans pass; `git diff` shows additions only)
Task 18: complete (`004`, `005`, `007` pass, and `004` gains `Covers FR-001–FR-010 and SC-001–SC-006`;
`006` has no plan artifact. All 7 plans green, conformance `17 conformant, 5 excused, 0 failure(s), 0
stale entr(ies)`)
Task 19: complete (citekit `specs/001-web-search-source/plan.md` → exit 1, `no-section`; a competent,
well-structured peer plan, so a genuine negative control ([SC-003]))
Task 20: complete (a copy of this plan with `FR-044` added and no row → `uncovered: FR-044 has no row`;
the real plan restores to exit 0)
Task 21: complete (gate §3f finds the rule in the plan contribution, the entry point, the skill, the
autonomy contract and the installer bridge; each is surface-specific, not a pasted block)
Task 22: complete (`AGENTS.md` managed block now reads `Every spec and every plan carries
'## In Plain Terms'`; gate asserts `every plan carries`)
Task 23: complete (`bin/speckit-init --no-mcp` → `preset up to date: spec-driven-development v1.18.0`,
13 commands recomposed; `.opencode/commands/speckit.plan.md` carries `Fill '## In Plain Terms' as you
design`)
Task 24: complete (005 and 007 read end to end; one repair — 007's row for `FR-012` said "the contribute
to" and mislabelled the plan contribution's list, now names the five contributions correctly)
Task 25: complete (`bin/speckit-resume specs/008-plain-plans` prints `COMPLETE`; every task above has a
line)
Task 26: complete (`make test` → `SELF-GATE: PASS examined=206 assertion(s)`, exit 0; committed on
`freebuff/df0ce130206f368964b24af5`)
Task 27: complete (P-001, 12 trials: grouped coverage passes, a dropped identifier is named, a repeat is
reported)
Task 28: complete (P-002: `FR-001`, `SC-001, FR-001` fail; `§Generated`, `` `bin/gate` ``, and both
together pass)
Task 29: complete (P-003: before the technical context passes, after it fails, after `## Summary` passes)
Task 30: complete (P-004: 1 and 2 sentences fail, 3 and 5 pass)
Task 31: complete (P-005: auto detection by file name, `--kind` override, and a spec fixture that passes
under spec rules while failing the three-sentence rule under plan rules)

## What this feature does not claim

- The check cannot tell whether a row states the real design decision. That is the template's content
  rule and review; the script header and the template say so. The evidence is also why: the format of a
  design document showed no measurable effect on understanding (Ernst & Robillard 2023), while the
  presence of design decisions and their rationale did (Shahin et al. 2014, via Rukmono et al. 2025).
- The six retrofits were written by the author of the plans' subject. Task 24 is a read-through, not an
  independent review; a non-author pass is outstanding.
- The conversation half is policy. Six surfaces carry it and the gate asserts their presence; nothing
  can assert that a reply followed it.
- `tasks.md` is unchanged and out of scope; `006` has no plan artifact, so the corpus is seven plans
  including this feature's own.

## Open at close-out

- `Status` remains `Draft`: implementation proceeded on the owner's instruction, and approval of the
  specification itself is still the owner's to give.
- The plan layer's long-term maintenance is the same risk 007 recorded: a covered-but-wrong row is a
  review finding. The artefact rule is the one mechanical defence, because a row that points nowhere is
  rejected.
