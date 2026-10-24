# Tasks: Plain Plans — a design a newcomer can follow

**Input**: `specs/008-plain-plans/spec.md`, `specs/008-plain-plans/plan.md`

**Prerequisites**: the spec is Draft until the owner approves it; the reversible parts proceed on the
owner's instruction of 2026-10-24.

## Generation note — the stopping rule, declared before round 1

The work stops when `scripts/check-plain-terms.py` reports zero findings over `specs/*/spec.md` and
`specs/*/plan.md`, each plan fixture produces its asserted exit code for its own reason, and the gate
is green with an examined count above the **189** recorded at `007`'s close. A retrofit the checker
accepts but that reads as a restatement of the spec is a review finding — hence T022, which is part
of the stopping rule.

## Format: `[ID] [P?] [Story] Description`

- **[P]** — can run in parallel (different files, no dependency)
- **[Story]** — the user story the task serves (US1…US4)
- Every task names one verifiable outcome and the requirement it serves

## Path Conventions

Single project, repository root. Generated files under `.specify/` and `.opencode/` are recomposed by
`bin/speckit-init`, never edited.

## Phase 1: Setup

- [x] T001 Record the pre-change baseline: `make test` → `SELF-GATE: PASS examined=189 assertion(s)`; write the number into `progress.md`. → verify: the number is recorded before any edit (SC-006)
- [x] T002 Read the five surfaces this feature touches — the plan template, the plan contribution, the gate §3e block, `bin/speckit-init`'s copy step, the conformance baseline — and note the exact strings each asserts. → verify: the note names the assertion for each (FR-009, FR-011)

## Phase 2: Foundational

- [x] T003 Add `## In Plain Terms` to `preset/templates/plan-addendum.md`: placement before `## Technical Context`, the three-part shape, the content rule (a decision and its reason, never a restatement), the artefact rule, the properties exclusion, the 45/25-word caps labelled as proxies, and the evidence limit (format showed no effect). → verify: `bash .specify/scripts/bash/resolve-template.sh plan-template` contains the heading and both table headers (FR-001–FR-003, FR-005–FR-008, FR-012)
- [x] T004 Add the heading to the order-waiver list in `scripts/check-section-integrity.sh` for plans, with the reason. → verify: a plan carrying it early is not reported `ORDER` (FR-001)
- [x] T005 Bump `preset/preset.yml` to 1.18.0, describe the contribution, and add the `CHANGELOG` entry. → verify: gate assertion "preset version is the newest CHANGELOG release" passes

## Phase 3: User Story 1 - A newcomer can tell what the plan builds (Priority: P1) 🎯 MVP

### Tests for User Story 1

- [x] T006 [P] [US1] Create `evals/fixtures/plain-terms/plan-good/plan.md` (conformant control) and `plan-no-section/plan.md`. → verify: the control passes in auto mode; the second exits 1 with `no-section` (FR-001, FR-010)
- [x] T007 [P] [US1] Create `plan-misplaced/plan.md` (section after `## Technical Context`) and `plan-thin-paragraph/plan.md` (two sentences). → verify: each fails naming its own rule (FR-001, FR-002)

### Implementation for User Story 1

- [x] T008 [US1] Add `--kind auto|spec|plan` and `artifact_kind()` to `scripts/check-plain-terms.py`; branch placement (`before ## Technical Context`, else before the first top-level section other than `## Summary`) and the paragraph threshold (3 sentences for plans, 2 for specs). Unknown `--kind` exits 2. → verify: `plan-good` exits 0; `plan-misplaced` and `plan-thin-paragraph` exit 1; a spec fixture is unaffected (FR-001–FR-003, FR-009)
- [x] T009 [US1] Share the identifier collector and coverage diff across modes; exclude `P-…` properties explicitly in a comment and in the template. → verify: a plan row naming `P-003` alone does not create coverage; a dropped `FR` is named (FR-004, FR-005)
- [x] T010 [US1] Add the artefact rule: a plan row's raw `Technical` cell must contain `§` or a backtick; `check_file` reports `no-artefact` naming the row. → verify: `plan-no-artefact` exits 1 with that finding; the control passes (FR-006)
- [x] T011 [US1] Keep the boundary rules shared: uppercase `SHALL`/`MUST`/`SHOULD` rejection and the 45-word cap apply in plan mode. → verify: a plan fixture with a 50-word cell exits 1 (FR-007)

## Phase 4: User Story 2 - Mechanism words stop being a wall (Priority: P2)

### Tests for User Story 2

- [x] T012 [P] [US2] Create `plan-unglossed/plan.md` (a listed mechanism word with no bracket at first use). → verify: exit 1 naming the term (FR-008)
### Implementation for User Story 2

- [x] T013 [US2] Extend the gloss finder to plan mode without duplicating it; the terms table, first-prose-use rule and 25-word cap are shared. → verify: `plan-unglossed` fails; `plan-good` reports its glossed terms (FR-008)

## Phase 5: User Story 3 - The explanation stays tied to the design (Priority: P2)

### Tests for User Story 3

- [x] T014 [US3] Extend `evals/fixtures/plain-terms/harness.py` with the plan cases and properties P-001…P-005; `--all` drives spec and plan cases. → verify: harness prints one line per check and exits nonzero on any mismatch (FR-010)
### Implementation for User Story 3

- [x] T015 [US3] Install the updated checker from `bin/speckit-init` (the existing copy step already refreshes it). → verify: a scratch install's `.specify/scripts/check-plain-terms.py` matches the source and runs `--kind plan` (FR-009)
- [x] T016 [US3] Add gate §3f: checker handles plans; all seven plans pass; five plan fixtures rejected for their own reason; teeth on a real plan; harness count; peer plan control; policy surfaces. → verify: `make test` green, examined > 189 (FR-009, FR-010, SC-006)
- [x] T017 [P] [US3] Retrofit `specs/001`, `002`, `003` plans: paragraph, rows covering every `FR`/`SC` they mention with an artefact reference, terms table with glosses. → verify: checker exits 0 on each; `git diff` shows additions only (SC-001, SC-002)
- [x] T018 [P] [US3] Retrofit `specs/004`, `005`, `007` plans, adding one line naming the requirements `004` serves (it cites none). `006` has no plan artifact. → verify: checker exits 0 on all seven plans; conformance baseline green after regeneration (SC-001, SC-002)
- [x] T019 [US3] Run the checker against citekit's `specs/001-web-search-source/plan.md` and record the rejection. → verify: exit 1, `no-section`, recorded in `progress.md` (SC-003)
- [x] T020 [US3] Demonstrate the teeth on a real plan: remove one row, observe the gate or checker fail naming the identifier, restore it. → verify: failure observed, then pass (SC-004)

## Phase 6: User Story 4 - The habit covers design talk (Priority: P3)

### Implementation for User Story 4

- [x] T021 [US4] Add the fill rule to `preset/commands/speckit.plan.prepend.md` (replacing the lighter vocabulary rule with one that names the section and the artefact requirement), and name plans in `commands/speckit.md`, `skill/spec-driven-development/SKILL.md` and `global/autonomy-contract.md`. → verify: the gate's §3f surface check finds the rule in each (FR-011)
- [x] T022 [US4] Add the rule to the `AGENTS.md` bridge heredoc in `bin/speckit-init`, naming plans as well as specs. → verify: a scratch install's managed block contains it (FR-011)

## Phase N: Polish

- [x] T023 Run `bin/speckit-init --no-mcp` so `.opencode/commands/` and `.specify/presets/` are recomposed. → verify: `specify preset info` reports 1.18.0; the plan command carries the new rule (FR-011)
- [x] T024 Read `specs/005` and `specs/007` plans end to end and repair any row that restates a requirement, explains nothing about the design, or points only at ids. → verify: the repair list is empty or the repairs are committed (SC-001, SC-002)
- [x] T025 Write `progress.md` (one line per task with evidence) and confirm `bin/speckit-resume specs/008-plain-plans` reports `COMPLETE`. → verify: the resume output
- [x] T026 Run `make test`, record `SELF-GATE: PASS examined=N` with N > 189, and commit on the feature branch. → verify: gate green; commit names the feature (SC-006)

## Dependencies & Execution Order

### Phase Dependencies

Phase 1 → Phase 2 (the template must demand the section before the checker is worth extending) →
Phase 3 → Phase 4 → Phase 5 → Phase 6 → Polish. Phase 6 touches different files and may run while the
checker is being extended.

### User Story Dependencies

US2 shares the gloss finder with US1's parser, so T013 follows T008. US3 depends on both, because it
measures the rules they add. US4 depends on nothing executable, only on the template's final wording.

### Within Each User Story

Fixture before checker, checker before gate assertion, gate assertion before retrofit — so the retrofit
is measured rather than eyeballed.

### Parallel Opportunities

T006, T007 and T012 are separate files. T017 and T018 are separate documents. T021 and T022 touch
different files but must both wait for the template's wording to settle.

## Parallel Example: User Story 1

```bash
# The two fixtures are separate files — write them together, then run the checker once:
python3 scripts/check-plain-terms.py evals/fixtures/plain-terms/plan-{good,no-section}/plan.md

# The retrofits are separate documents: T017 and T018 can run in either order.
```

## Implementation Strategy

### MVP First

T003 + T008 + T010 deliver US1: a plan section and a checker that enforces its shape. That alone gives
a reader somewhere to start.

### Incremental Delivery

US2 (glosses), then US3 (fixtures, gate, retrofits), then US4 (policy). Each slice leaves the checker
green over the corpus, so a failure belongs to the slice that caused it.

### Parallel Team Strategy

One worker on the checker and harness (T008–T014), because they share a file. A second on the six
retrofits (T017–T018), which only add sections. A third on the policy text (T021–T022), which cannot
affect the checker.

## Notes

- The content rule — a row states the choice and why — is review, not code. The template says so and
  the gate cannot pretend otherwise.
- No new dependency. The script keeps to `json`, `re`, `sys`.
- Retrofits are additions; a retrofit that has to change a requirement to make a row true is a
  contradiction to repair at the source, not a row to rewrite.

## Task Detail Block

```
T0nn — <one-line outcome>
Why:     <the requirement or decision it serves>
Touch:   <files>
Check:   <the command run and the exact output that proves it>
If it fails: <the cause to look for first, not a retry>
```

### Worked example

```
T010 — a plan row that names no artefact is a failure
Why:     FR-006; the row must send the reader into the design, not back to the spec
Touch:   scripts/check-plain-terms.py, evals/fixtures/plain-terms/plan-no-artefact/plan.md
Check:   python3 scripts/check-plain-terms.py evals/fixtures/plain-terms/plan-no-artefact/plan.md
         → exit 1, 'row 1: the Technical cell names no section (§) or file'
If it fails: <check that the raw cell is inspected, not the normalised one — norm() strips backticks>
```

## Task Rules

- One verifiable outcome per task; two commands to prove means two tasks.
- A task that edits a generated file is invalid: change the source and re-run the installer.
- A plan row may only be added; it may not soften the design it explains.

## Property-Based Test Tasks

- [x] T027 [P] P-001 — generate id sets and groupings; assert the uncovered set is exactly the set
  difference, and that grouping never changes the verdict. → verify: `harness.py --property P-001`
  green, red against a checker that stops at the first uncovered id (FR-004)
- [x] T028 [P] P-002 — render `Technical` cells with no `§`, no backtick, one of each, and both;
  assert fail/fail/pass/pass. → verify: `--property P-002` (FR-006)
- [x] T029 [P] P-003 — place the section before, between and after the technical context headings;
  assert pass/fail/fail. → verify: `--property P-003` (FR-001)
- [x] T030 [P] P-004 — render paragraphs of 1, 2, 3 and 5 sentences; assert fail/fail/pass/pass.
  → verify: `--property P-004` (FR-002)
- [x] T031 [P] P-005 — run every spec fixture in auto and plan mode; assert auto matches the previous
  verdicts and plan mode differs only where the placement rule changes it. → verify: `--property
  P-005` (FR-009)

### Worked example

```python
# P-005: the boundary is the presence of a pointer, so the test walks both sides of it.
for cell, expect_ok in [("FR-001", False), ("§Generated", True), ("`bin/gate`", True)]:
    assert (checker(plan_with(technical=cell)) == 0) is expect_ok
```

## Requirement Coverage

| Requirement | Task | Status |
| --- | --- | --- |
| FR-001 | T003, T004, T008, T029 | ☐ |
| FR-002 | T003, T008, T030 | ☐ |
| FR-003 | T003, T008 | ☐ |
| FR-004 | T008, T009, T027 | ☐ |
| FR-005 | T003, T017, T018, T024 | ☐ |
| FR-006 | T003, T010, T028 | ☐ |
| FR-007 | T003, T011 | ☐ |
| FR-008 | T003, T012, T013 | ☐ |
| FR-009 | T008, T015, T016, T031 | ☐ |
| FR-010 | T006, T007, T016 | ☐ |
| FR-011 | T021, T022, T023 | ☐ |
| FR-012 | T003, T008 | ☐ |

| Property | Requirement | Task | Kind |
| --- | --- | --- | --- |
| P-001 | FR-004 | T027 | property-test |
| P-002 | FR-006 | T028 | property-test |
| P-003 | FR-001 | T029 | property-test |
| P-004 | FR-002 | T030 | property-test |
| P-005 | FR-009 | T031 | property-test |
