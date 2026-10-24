# Tasks: Plain Language — a specification a newcomer can actually use

**Input**: `specs/007-plain-language/spec.md`, `specs/007-plain-language/plan.md`

**Prerequisites**: the spec is Draft until the owner approves it; implementation of the reversible
parts proceeds on the owner's instruction of 2026-10-24.

## Generation note — the stopping rule, declared before round 1

The work stops when `scripts/check-plain-terms.py` reports zero findings over `specs/*/spec.md`, its
five fixtures each produce the asserted exit code, and the gate is green with an examined count above
the 164 recorded before this feature. A retrofit that the checker accepts but that reads as jargon is
not "done" — it is a review finding, and the review of 001 and 006 (T014) is part of the stopping rule
for that reason.

## Format: `[ID] [P?] [Story] Description`

- **[P]** — can run in parallel (different files, no dependency)
- **[Story]** — the user story the task serves (US1…US4)
- Every task names one verifiable outcome and the requirement it serves

## Path Conventions

Single project, repository root. Scripts in `scripts/`, fixtures in `evals/fixtures/plain-terms/`,
generated project files under `.specify/` and `.opencode/` are **never hand-edited** — they are
recomposed by `bin/speckit-init`.

## Phase 1: Setup (Shared Infrastructure)

- [x] T001 Record the pre-change baseline: run `./scripts/verify` and capture `SELF-GATE: PASS examined=N` (expected N=164). → verify: the number is written into `specs/007-plain-language/progress.md` before any edit (SC-006)
- [x] T002 [P] Read the seven policy surfaces (`commands/speckit.md`, the five `preset/commands/*.prepend.md`, `skill/spec-driven-development/SKILL.md`, `autonomy-contract.md`, the bridge heredoc in `bin/speckit-init`) and note where each already talks about reader-facing prose. → verify: the note names each surface and its current wording (FR-012)

## Phase 2: Foundational (Blocking Prerequisites)

- [x] T003 Add `## In Plain Terms` to `preset/templates/spec-addendum.md`: the paragraph, the two table contracts (`Item | In plain words | Technical`, `Term | Plain words`), the placement rule (before the first user story), the normative-keyword ban, the no-copy rule, and the 45/25-word caps labelled as brevity proxies. → verify: `bash .specify/scripts/bash/resolve-template.sh spec-template` contains the heading and both headers (FR-001–FR-003, FR-006–FR-009)
- [x] T004 Add `## In Plain Terms` to the order-waiver list in `scripts/check-section-integrity.sh`, with the reason (the template instructs the author to place it early). → verify: a spec carrying it before the first story is not reported `ORDER` (FR-001)
- [x] T005 Bump `preset/preset.yml` to 1.17.0, describe the new contribution, and add the `CHANGELOG` entry. → verify: gate assertion "preset version is the newest CHANGELOG release" passes

## Phase 3: User Story 1 - A newcomer can tell what a spec binds (Priority: P1) 🎯 MVP

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [x] T006 [P] [US1] Create `evals/fixtures/plain-terms/good/spec.md` (conformant control) and `no-section/spec.md`, each with three stories, ten requirements and three criteria. → verify: the control passes the checker; `no-section` fails naming the missing heading (FR-001, FR-010)
- [x] T007 [P] [US1] Create `uncovered/spec.md` (`FR-002` in no row) and `duplicate/spec.md` (one id in two rows). → verify: each fails naming the identifier (FR-004, FR-005)

### Implementation for User Story 1

- [x] T008 [US1] Write `scripts/check-plain-terms.py`: section finder (stops at the next same-level heading, skips fenced blocks and HTML comments), table parser, identifier collector (`US` from story headings, `FR`/`SC` from the whole body including traceability tables), row expander (comma lists, closed ranges with `–`, `-`, `...`), coverage diff, and the `--json` form. Exit 0/1/2. → verify: `python3 scripts/check-plain-terms.py evals/fixtures/plain-terms/good/spec.md` exits 0 and prints `covered=N`; `no-section` exits 1 (FR-003–FR-005, FR-010)
- [x] T009 [US1] Add the vacuity rule: a spec with a section but no rows, or with no ids at all, fails with "nothing was examined" rather than passing. → verify: an empty-table fixture exits 1 (FR-010, P-003)
- [x] T010 [US1] Add the boundary checks: normative keywords (`SHALL`, `MUST`, `SHOULD`) in a plain cell, and the 45-word cap. → verify: `commands/spec.md` fails naming the keyword; a 46-word cell fails naming the cell (FR-006, FR-007)

## Phase 4: User Story 2 - Specialist terms stop being a wall (Priority: P2)

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [x] T011 [P] [US2] Create `unglossed/spec.md` (a listed term whose first use has no bracket) and `long-gloss/spec.md` (a 30-word bracketed clause). → verify: both exit 1 with the term named (FR-009)

### Implementation for User Story 2

- [x] T012 [US2] Add the terms-table parser and the first-use gloss finder: first prose occurrence outside the section and outside code spans must be followed by `(`…`)` within the same paragraph, ≤ 25 words. → verify: `good` passes; `unglossed` and `long-gloss` fail; a term whose first use is inside a code span is skipped (FR-008, FR-009, P-004)

## Phase 5: User Story 3 - The explanation cannot rot (Priority: P3)

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [x] T013 [P] [US3] Write `evals/fixtures/plain-terms/harness.py --all` driving the six fixtures and four properties (P-001…P-004), printing one line per check and exiting nonzero on any mismatch. → verify: 6 cases + 4 properties reported, all green (FR-010, FR-011)

### Implementation for User Story 3

- [x] T014 [US3] Install the checker from `bin/speckit-init` into `.specify/scripts/check-plain-terms.py` (executable), mirroring the `check-section-integrity.sh` copy — refresh when the source differs, warn when the installed copy was edited locally. → verify: a scratch install contains the file with mode +x (FR-010)
- [x] T015 [US3] Add gate assertions to `scripts/self-gate.sh`: checker present and executable; `specs/*/spec.md` all pass; each fixture produces its asserted exit code and named finding; harness reports 6 cases + 4 properties. → verify: `./scripts/verify` green, examined > 164 (FR-010, FR-011, SC-006)
- [x] T016 [P] [US3] Retrofit `## In Plain Terms` into `specs/001`, `002`, `003` (paragraph, rows for every story/FR/SC, terms table, glosses at first use). → verify: checker exits 0 on each, and no requirement text changed (`git diff` shows additions only) (SC-001)
- [x] T017 [P] [US3] Retrofit `specs/004`, `005`, `006` the same way. → verify: checker exits 0 on all six; `python3 scripts/conformance-baseline.py check` green with a regenerated baseline if counts moved (SC-001, SC-003)
- [x] T018 [US3] Run the checker against a peer specification (citekit, `.scratch/peers/citekit/specs/001-web-search-source/spec.md`) and record the rejection. → verify: exit 1, `rows=0`, recorded in `progress.md` (SC-002)

## Phase 6: User Story 4 - The habit applies to conversation, not just files (Priority: P2)

### Implementation for User Story 4

- [x] T019 [US4] Add the rule to `commands/speckit.md` (non-negotiables), the `specify`, `plan`, `tasks`, `implement` and `converge` prepends, `skill/spec-driven-development/SKILL.md` (cross-cutting rules), and `autonomy-contract.md` (a short section on how a reply is written). Each surface gets the sentence that fits it, not a copy-paste block. → verify: `grep` finds the rule in all nine, and the gate asserts the key strings (FR-012)
- [x] T020 [US4] Add the rule to the `AGENTS.md` bridge heredoc in `bin/speckit-init`, in three lines. → verify: a scratch install's managed block contains it (FR-012)

## Phase N: Polish & Cross-Cutting Concerns

- [x] T021 Re-run `bin/speckit-init` (with `--no-mcp`) so `.opencode/commands/` and `.specify/presets/` are recomposed from the preset — never by hand. → verify: `git status` shows the composed files changed and the hook did not block; `specify preset info` reports 1.17.0 (FR-012)
- [x] T022 Read `specs/001` and `specs/006` end to end and repair any row that restates a requirement, commands, or explains nothing. → verify: the repair list is empty or the repairs are committed (SC-001, SC-003)
- [x] T023 Write `specs/007-plain-language/progress.md` (identity line, one `Task N: complete (<evidence>)` per closed task) and confirm `bin/speckit-resume specs/007-plain-language` reports `COMPLETE` only when every task has a line. → verify: `bin/speckit-resume` output
- [x] T024 Run `./scripts/verify` and record `SELF-GATE: PASS examined=N` with N > 164 in `progress.md`; commit on the feature branch. → verify: gate green; commit message names the feature (SC-006)

## Dependencies & Execution Order

### Phase Dependencies

Phase 1 → Phase 2 (the template must demand the section before the checker is worth writing) →
Phase 3 → Phase 4 → Phase 5. Phase 6 is independent of the checker and can run in parallel with
Phase 3–5.

### User Story Dependencies

US2 depends on US1's parser (both read the same section). US3 depends on US1 and US2 having a checker
to run. US4 depends on nothing.

### Within Each User Story

Fixture before checker (the test that proves the failure exists), checker before gate assertion, gate
assertion before retrofit — so the retrofit is measured, not eyeballed.

### Parallel Opportunities

T002, T006, T007, T011, T013, T016, T017 and T025–T028 touch different files and can run together.

## Parallel Example: User Story 1

```bash
# The three fixtures are separate files — write them together, then run the checker once:
python3 scripts/check-plain-terms.py evals/fixtures/plain-terms/{good,no-section,uncovered}/spec.md

# The two retrofits are separate documents:
# T016 and T017 can be executed in either order; only the baseline regeneration depends on both.
```

## Implementation Strategy

### MVP First (User Story 1 Only)

T003 + T008 + T010 deliver US1 — a section contract and a checker that enforces it — and that alone
removes the owner's stated cost, with no retrofit needed to be useful.

### Incremental Delivery

US2 (glosses), then US3 (gate wiring and the six retrofits), then US4 (the conversation policy). Each
slice leaves the gate green and the checker running over the real specs, so a failure is attributable
to the slice that caused it rather than to the batch of retrofits.

### Parallel Team Strategy

One worker: the checker and its fixtures (T008–T013), because they share a file. A second: the six
retrofits (T016–T017), which only add sections. A third: the policy text (T019–T020), which touches the
commands and the bridge and cannot affect the checker.

**MVP first**: T003 + T008 + T010 deliver US1, whose value does not depend on any other slice. — a section contract and a checker that enforces it —
and that alone removes the owner's stated cost. US2 (glosses) is the second slice, US3 (gate wiring and
retrofits) the third, US4 (conversation policy) rides alongside because it touches different files.

**Incremental delivery**: after each slice the gate is green and the checker runs over the real specs,
so a failure is attributable to the slice that caused it rather than to the set of six retrofits.

## Notes

- The checker is installed, not referenced, so an adopter gets it. A check that exists only in the
  kit's own repository would leave every downstream project with a template that demands a section and
  no way to verify it.
- No new runtime dependency. Python 3 standard library only.
- The retrofits are additions; `git diff --stat` on a spec must show `0 deletions` outside the inserted
  block, or the task is wrong.

## Task Detail Block

The shape every T00x above follows when it is executed:

```
T0nn — <one-line outcome>
Why:     <the requirement or decision it serves>
Touch:   <files>
Check:   <the command run and the exact output that proves it>
If it fails: <the cause to look for first, not a retry>
```

## T005: Reject a normative keyword in a plain cell

```
T010 — a plain cell that commands is a failure
Why:     FR-006; the plain layer explains and must not become a second normative voice
Touch:   scripts/check-plain-terms.py, evals/fixtures/plain-terms/commands/spec.md
Check:   python3 scripts/check-plain-terms.py evals/fixtures/plain-terms/commands/spec.md
         → exit 1, 'commands/spec.md: normative keyword MUST in row SC-002'
If it fails: <first check the word-boundary match — 'MUSTARD' must not match>
```

### Worked example

A real failure from this feature's own dogfooding is the fixture that caught it: the first checker read
`MUST` with a substring match, so the plain cell "a must-read for newcomers" failed. The repair was a
word-boundary match plus the rule that the keyword must be upper case — a normative keyword is written
`MUST`, and prose about obligation is not a requirement.

## Task Rules

- One verifiable outcome per task; if it needs two commands to prove, it is two tasks.
- A task that changes a generated file is invalid: change the source and re-run the installer.
- A retrofit task may only add text. If a retrofit needs to change a requirement to make the
  explanation true, the requirement was wrong — stop, record it, and repair at the source.
- The checker's own tests are fixtures, not assertions about the checker's opinion: an exit code and a
  named finding, or it is not a test.

## Property-Based Test Tasks

- [x] T025 [P] P-001 — generate id sets and row groupings; assert the coverage diff is exactly the set
  difference, in both directions. → verify: harness `--property P-001` green, and red against a checker
  that stops at the first uncovered id (FR-004, FR-005)
- [x] T026 [P] P-002 — embed `SHALL`/`MUST`/`SHOULD` in otherwise plain sentences; assert each fails,
  and that `must` lower-case and `MUSTARD` do not. → verify: `--property P-002` (FR-006)
- [x] T027 [P] P-003 — for every generated spec with a section and zero rows, assert failure. → verify:
  `--property P-003` (FR-010, Edge Cases)
- [x] T028 [P] P-004 — place a gloss at 1, 2, 3 and 30 words from the term, and in the next paragraph;
  assert pass/pass/pass/fail/fail. → verify: `--property P-004` (FR-009)

### Worked example

```python
# P-004: the boundary the rule claims is "same paragraph", so the test walks the boundary.
for distance, expect_ok in [(1, True), (3, True), (30, True), ("next-paragraph", False)]:
    spec = render(term="vacuity", gloss_words=distance)
    assert (checker(spec) == 0) is expect_ok
```

## Requirement Coverage

| Requirement | Task | Status |
| --- | --- | --- |
| FR-001 | T003, T004 | ☐ |
| FR-002 | T003 | ☐ |
| FR-003 | T003, T008 | ☐ |
| FR-004 | T007, T008, T025 | ☐ |
| FR-005 | T007, T008, T025 | ☐ |
| FR-006 | T003, T010, T026 | ☐ |
| FR-007 | T003, T010 | ☐ |
| FR-008 | T003, T012 | ☐ |
| FR-009 | T011, T012, T028 | ☐ |
| FR-010 | T008, T009, T013, T014, T015, T027 | ☐ |
| FR-011 | T013, T015 | ☐ |
| FR-012 | T019, T020, T021 | ☐ |
| FR-013 | T003, T008 | ☐ |

| Property | Requirement | Task | Kind |
| --- | --- | --- | --- |
| P-001 | FR-004, FR-005 | T025 | property-test |
| P-002 | FR-006 | T026 | property-test |
| P-003 | FR-010 | T027 | property-test |
| P-004 | FR-009 | T028 | property-test |
