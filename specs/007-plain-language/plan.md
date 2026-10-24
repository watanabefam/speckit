# Implementation Plan: Plain Language — a specification a newcomer can actually use

**Branch**: `007-plain-language` | **Date**: 2026-10-24 | **Spec**: `specs/007-plain-language/spec.md`

## In Plain Terms

This plan adds one required, informative section to each specification — a paragraph, a row per
requirement, and the document's own terms — and one checker that keeps it honest. The checker is a pure
read of a single file: it collects the identifiers into a coverage report (every identifier appearing in
the explanation table) and requires a bracketed gloss (a short explanation right after the word it
explains) for each listed term. The gate then runs it over every specification and over a fixture for
each failure shape, because a rule that nothing runs rots within a release.

| Item | In plain words | Technical |
| --- | --- | --- |
| FR-001–FR-003 | The section, its opening paragraph and its two tables are required by the spec template, so the guidance arrives with the preset rather than from a skill. | `preset/templates/spec-addendum.md`; §Architecture Overview |
| FR-004–FR-005 | Every requirement is covered once; a gap, a repeat or an invented identifier is a failure with the identifier named. | `scripts/check-plain-terms.py` coverage; §Correctness Properties P-001 |
| FR-006–FR-007 | The explanation may describe but not command, and stays short enough to scan, so it cannot become a second specification. | `NORMATIVE_RE`, `PLAIN_LIMIT`; §Architecture Overview |
| FR-008–FR-009 | The document lists its own specialist words and brackets each one where a reader first meets it, instead of relying on a global dictionary. | terms parse; `GLOSS_LIMIT` in `scripts/check-plain-terms.py` |
| FR-010 | The check is a standalone script installed into every adopter project and run by the gate, so the rule reaches projects outside this repository. | `bin/speckit-init`; `scripts/self-gate.sh` §3e |
| FR-011 | Each failure shape has its own small broken spec, and the gate proves rejection by exit code and named finding. | `evals/fixtures/plain-terms/`; §Validation Strategy |
| FR-012 | The rule is written where the agent actually reads it — the contributions to `specify`, `plan`, `tasks`, `implement` and `converge`, plus the bridge. | `preset/commands/*.prepend.md`; `bin/speckit-init` |
| FR-013 | No readability score is gated and no comprehension is claimed, because the evidence does not support either. | `docs/research/plain-language-2026-10.md` §6; script header |
| FR-034 | The earlier feature's coverage-silence rule is deliberately left alone, so this layer cannot change what a green result means. | `specs/005-verification-integrity/plan.md`; §Implementation Boundaries |
| SC-002 | A spec that is structurally perfect but has no plain layer is rejected, demonstrated on a peer project's specification. | `scripts/check-plain-terms.py`; `.scratch/peers/citekit/specs/001-web-search-source/spec.md` |
| SC-005 | Adding a requirement without a row fails the gate and names the identifier. | `scripts/self-gate.sh` §3e; §Validation Strategy |

**Terms**

| Term | Plain words |
| --- | --- |
| coverage | every identifier in the document appearing in the explanation table |
| gloss | a short explanation in brackets, right after the word it explains |

## Summary

Add a required, informative `## In Plain Terms` section to every specification — a short paragraph, an
identifier-keyed plain/technical table, and a terms table — plus one checker
(`scripts/check-plain-terms.py`) that fails on a missing section, an uncovered identifier, a normative
keyword in an explanation, an over-length cell, or an unglossed term. The checker is installed with the
kit and run by `scripts/self-gate.sh` over every spec. The same rule is written into the entry point,
the five step prepends, the skill, the autonomy contract and the `AGENTS.md` bridge, because the
owner's complaint is about the workflow's output as much as about its files.

## Technical Context

**Language/Version**: Python 3 (standard library only) for the checker; bash 3.2-compatible shell for
the gate wiring.

**Primary Dependencies**: none new. `git` is not required by the checker. The `specify` CLI 1.2.2,
already present, is needed only to recompose `.opencode/commands/` after the preset changes.

**Storage**: files only — the spec documents; no database, no network.

**Testing**: fixture corpus (`evals/fixtures/plain-terms/`) driven by a small harness, plus gate
assertions on exit codes and on the six retrofitted specs.

**Target Platform**: the kit's own repository and every project that installs the preset.

**Project Type**: single project — a documentation-and-tooling repo.

**Performance Goals**: the checker finishes a 500-line spec in well under a second; it reads files and
regexes them, and the gate already takes ~3.5 minutes, so this must not be measurable there.

**Constraints**: no readability score (FR-013); no retro-fitting of requirement text (0005); the
section is informative, so it may not contain normative keywords (FR-006); the checker's headings are
English strings (Assumptions).

**Scale/Scope**: 6 spec files, 1 checker (~250 lines), 1 template section, 5 prepends, 1 entry point,
1 skill rule, 1 contract paragraph, 1 bridge paragraph, 5 fixtures, ~8 gate assertions.

## Constitution Check

| Principle | How this plan satisfies it |
| --- | --- |
| I. Evidence Over Assertion | The feature ships a checker whose exit codes are observed on five fixtures; SC-005 is observed failing, then passing. No claim of "clarity" is made — only coverage, brevity and gloss presence. |
| II. Proportionate Process | Full workflow, because the change touches the spec template (a public contract for every adopter) and six accepted artifacts. |
| III. Traceable Artifacts | Every FR has a task in `tasks.md` and every task names its requirement. |
| IV. Repair at the Source | The template is changed first, then the specs, then the baseline — not the reverse. A spec that fails is retrofitted, not excused. |
| V. Honest Enforcement | The checker enforces structure only, and both the script header and the spec say what it cannot see. The conversation half is described as policy carried by prompt text, never as enforcement. |
| Security & Prompt Boundaries | No generated file is hand-edited: the preset and `bin/speckit-init` are changed, then `bin/speckit-init` is re-run. |
| Workflow & Gates | Preset version bumps with a `CHANGELOG` entry; `./scripts/verify` must pass. |

No violation, and no entry in `## Complexity Tracking`.

## Project Structure

### Documentation (this feature)

```
specs/007-plain-language/
├── spec.md          # requirements, plain layer (dogfood)
├── plan.md          # this file
├── tasks.md         # T001… T0xx with requirement coverage
└── progress.md      # implementation record, written as work completes
docs/research/plain-language-2026-10.md   # companion, informative
decisions/0007-explanations-are-informative.md
```

### Source Code (repository root)

```
scripts/
├── check-plain-terms.py        # NEW — the checker
├── check-section-integrity.sh  # order waiver for '## In Plain Terms'
└── self-gate.sh                # assertions: fixtures, six retrofits, peer rejection

evals/fixtures/plain-terms/
├── harness.py                  # fixture driver
├── good/spec.md                # conformant control
├── no-section/spec.md          # missing section
├── uncovered/spec.md           # FR-002 in no row
├── commands/spec.md            # 'MUST' inside a plain cell
├── unglossed/spec.md           # term with no bracketed gloss
└── long-gloss/spec.md          # bracketed clause over 25 words

preset/
├── preset.yml                              # version bump + contribution description
├── templates/spec-addendum.md              # the required section + authoring rules
└── commands/speckit.{specify,plan,tasks,implement,converge}.prepend.md

commands/speckit.md              # entry point rule
skill/spec-driven-development/SKILL.md
autonomy-contract.md
bin/speckit-init                 # bridge text + install the checker
specs/00{1..6}-*/spec.md         # retrofit: ## In Plain Terms
```

## Complexity Tracking

**Not applicable — no constitutional violation and no added complexity.** The feature adds one checker
(≈300 lines of standard-library Python), one template section, and policy text in nine places. Nothing
new runs at request time, no dependency is added, and the gate gains assertions rather than a second
verification path. The `## Constitution Check` above records compliance principle by principle.

## Carried Forward

### Confirmed Decisions

- Additive and informative; requirement text unchanged (`decisions/0007`).
- Presence + coverage + brevity + gloss presence are checked; quality is not.
- No readability score.
- Conversation policy is carried by commands/skill/contract/bridge, not a constitution amendment.

### Constraints

- Python standard library only; bash 3.2 parsing.
- The checker must be installed into adopters (`.specify/scripts/`), mirroring
  `check-section-integrity.sh`.
- Coverage must read the whole document, including traceability tables, or an id could hide there.

### Assumptions

- The audience is a newcomer to the project, not to programming.
- A wrong-but-covered explanation is a review finding, not a gate failure.

### Risks

- The section becomes a ritual. Mitigation: coverage + brevity + "say something the requirement does
  not", and the review pass named in the validation plan.
- Six retrofits inherit the original author's assumptions. Mitigation: the peer test and reading two
  retrofits end to end.
- Duplication drifts. Mitigation: no normative keywords, no copied text, coverage fails on id changes.

### Open Questions

- Plan-layer coverage: parked (spec `## Future Work` row 1).
- Explanation correctness: no oracle exists; stated, not solved.

## Scope Confirmation

### In Scope

- `## In Plain Terms` in the spec template addendum, with authoring rules and the terms table.
- `scripts/check-plain-terms.py`, its fixtures, and gate assertions.
- The order waiver in `check-section-integrity.sh` so "place it early" is not reported as reordering.
- Policy text in `commands/speckit.md`, the five prepends, the skill, `global/autonomy-contract.md`, and
  the bridge inside `bin/speckit-init`.
- Six retrofits, conformance baseline regeneration, preset version bump, `CHANGELOG` entry.

### Out of Scope

- Rewording requirement text; a readability score; plan/tasks layers; translation; judging quality.

### Requirements Affected

FR-001…FR-013 of this spec; nothing in 001–006 changes. 005's FR-034 is untouched.

## Repository Findings

### Relevant Components

- `preset/templates/spec-addendum.md` — where required sections are declared; the section lands here.
- `scripts/check-section-integrity.sh` — normalises headings, waives order for a fixed list
  (`## Document Status`, `## Normative Status`, `### Which document wins`, `## Requirements Syntax`,
  `## Problem / Opportunity`). The new heading must join that list.
- `scripts/conformance-baseline.py check` — runs the section checker over `specs/*/{spec,plan,tasks}.md`
  and fails on stale entries. Adding a required heading changes every spec's required count.
- `scripts/self-gate.sh` — 1,559 lines; sections numbered, assertions counted (`examined=N`), `skip`
  available when the `specify` CLI is missing.
- `bin/speckit-init` — section 6b installs `scripts/verify`; section 2c/2d hooks and permissions;
  section 6 builds the `AGENTS.md` bridge heredoc; a later block copies `check-section-integrity.sh`.

### Existing Behavior

- Spec templates carry Document Status, Normative Status (with "Which document wins"), EARS guidance,
  Carried Forward, Problem, Goals/Non-Goals, Dependencies, MVP, Future work with the parking-lot
  distinction, Validation Plan, Requirement Traceability.
- The conformance baseline currently records `11 conformant, 5 excused, 0 stale`.
- The gate counts assertions; the last recorded figure is `examined=164`.

### Existing Tests

- `evals/fixtures/verify/harness.py` (17 cases, 12 properties) drives the verification engine.
- `scripts/self-gate.sh` asserts preset composition, prepend content, install idempotency, and the
  conformance baseline.
- No test currently reads prose quality; nothing exists to extend, so this feature adds a corpus.

### Project Conventions

- Checkers are standalone scripts with an exit-code contract (0 pass, 1 finding, 2 usage) and a
  "what it cannot do" header.
- Gate assertions use `ok` / `bad` / `skip` and contribute to `examined`.
- Every kit change carries a decision record when it constrains future work.

### Constraints Discovered

- `.opencode/commands/*.md` and `.specify/` are generated and hook-protected; regeneration goes through
  `bin/speckit-init` (which runs `specify preset update --dev`).
- The gate requires the preset version to match the newest `CHANGELOG` release, so a version bump and a
  changelog entry are one change.
- A required heading addition invalidates the baseline for all six specs; excusing them would defeat
  the feature, so all six are retrofitted.

## Architecture Overview

```
spec.md ──▶ check-plain-terms.py ──▶ exit 0/1 ──▶ self-gate.sh ──▶ PASS/FAIL
                    ▲                     │
                    │                     └── coverage report (uncovered/duplicate/unknown)
             terms table + ids
```

The checker is a pure function of one file: parse headings, collect ids, parse the section's tables,
compare. No state, no configuration, no network. The gate invokes it per spec plus on five fixtures and
asserts the exact exit code and a named message for each.

## Major Components

1. **Section parser** — find `## In Plain Terms`, split its tables, stop at the next heading of the same
   level. A fenced code block inside the section is skipped (the same defect that made the section
   checker read a shell comment as a heading).
2. **Identifier collector** — `US\d+` from `### User Story` headings, `FR-\d{3}` and `SC-\d{3}` from the
   body, including traceability tables.
3. **Row expander** — `Item` cells accept comma-separated ids and closed ranges with `–`, `-` or `...`.
4. **Term glosser** — for each term, the first prose occurrence (table lines and code spans skipped)
   must be followed by `(`…`)` of ≤ 25 words.
5. **Policy text** — the same rule, adapted per surface, in nine places.

## Data Flow

Read spec → collect ids → parse rows → diff → report `covered=N uncovered=[…] duplicate=[…]
unknown=[…]` → exit. The report is line-oriented for humans and `--json` for the gate, matching
`check-section-integrity.sh --json`.

## Interfaces and Contracts

- `python3 scripts/check-plain-terms.py [--json] <spec.md>…` — exit 0/1/2; one summary line per file.
- The table contract: header contains `Item`, `In plain words`, `Technical`; the terms table header
  contains `Term`, `Plain words`. Header matching is case-insensitive and ignores surrounding spaces.
- The section contract: heading exactly `## In Plain Terms`, placed before the first `### User Story`.

## Dependencies

- The spec template addendum and the checker ship together: the template demands the section, the
  checker verifies it. Shipping one without the other makes every spec fail or every check vacuous.
- The `AGENTS.md` bridge is written by `bin/speckit-init`; the rule must be in that heredoc, not only in
  the skill, because the skill fires on roughly 60% of requests.

## Error Handling

- Missing file → exit 2 with the path. No section → exit 1 naming the file. Malformed table (no header)
  → exit 1 naming the defect. Unparseable id range → exit 1 (`FR-009–FR-002` is reversed and reported).
- The checker never exits 0 because it found nothing to check: a spec with zero ids and zero rows is a
  finding ("nothing was examined"), copying the vacuity rule from 005. That is deliberate: an empty
  table is the shape a ritual takes.

## Security and Privacy

No external input, no network, no file writes. The checker reads only paths given on the command line
and does not follow symlinks outside the repository. Nothing here touches secrets.

## Performance and Reliability

Single pass per file; regexes are linear and bounded. The gate runs it over six specs and five
fixtures, so the added time is one process launch per file. Failure mode is a nonzero exit, never a
silent pass.

## Validation Strategy

- Fixture corpus: `good` (control) plus `no-section`, `uncovered`, `commands`, `unglossed`,
  `long-gloss`, each asserting exit 1 and a named finding.
- Gate: assert the checker is executable, that `specs/*/spec.md` all pass, that each fixture fails, that
  the template carries the section, and that the policy string is present in the seven surfaces.
- Manual: read 001 and 006 end to end; read a rendered reply.
- Peer: citekit's spec must fail with zero rows.
- Evidence for approval: `PASS examined=N`, N > 164.

## Correctness Properties

### Rules

- **P-001 — Coverage is total and unique.** For any spec, the set of rows expands to exactly the set of
  ids, with no duplicates. Checked by a generative property over id sets and row groupings.
- **P-002 — A normative keyword never passes.** For any plain cell containing `SHALL`/`MUST`/`SHOULD`
  as a word, the checker fails. Checked by generating cells with the keywords embedded in prose.
- **P-003 — Silence is failure.** For any spec with a section but no rows, the checker fails rather
  than reporting zero findings.
- **P-004 — Gloss placement is local.** For any term whose first prose use is followed by a bracketed
  gloss within the same paragraph, the checker passes that term; more than a paragraph away, it fails.

### Framework decision

**None adopted.** Plan templates elsewhere may name Hypothesis; this repository's two existing
harnesses are hand-written generators (`evals/fixtures/verify/harness.py`), and adding a dependency for
four properties over string manipulation would not pay. Property tasks therefore generate cases by
enumeration and seeded randomness in the standard library, the precedent 005 already set.

### Traceability

| Property | Requirements | Where |
| --- | --- | --- |
| P-001 | FR-004, FR-005 | `evals/fixtures/plain-terms/harness.py` |
| P-002 | FR-006 | same |
| P-003 | FR-010, Edge Cases | same |
| P-004 | FR-009 | same |

### Independence

Each property fails independently: P-001 does not depend on gloss parsing, P-004 does not depend on
coverage. The fixtures are separate files, so one defect cannot mask another.

## Alternatives Considered

1. **Rewrite requirements in plainer language.** Rejected: trades precision where it is load-bearing,
   and 0005 refuses retro-fitting accepted wording.
2. **A readability score in the gate.** Rejected on evidence: formulas do not measure comprehension
   (AHRQ, Schriver, Redish) and invite tuning to the score.
3. **A separate `plain.md` per feature.** Rejected: a second document drifts without a coverage check,
   and nothing would tie it to the ids.
4. **Require the section on plans and tasks too.** Deferred, not rejected: the owner asked for specs,
   and a plan's plain layer would restate the spec's (parking lot row 1).
5. **A global jargon dictionary in the checker.** Rejected: a fixed word list is wrong for every project
   except the one it was written for. The document's own terms table is the anchor.

## Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Table filled to satisfy the check, saying nothing | Brevity cap + "say what the requirement does not" + review of two specs |
| Retrofits inherit the original assumptions | Peer test (SC-002); independent read of 001 and 006 |
| Coverage check reads only the section and misses ids | Collector reads the whole document, including traceability tables |
| Gate noise from a heading rename | Heading string lives in one constant in the checker and one line in the template |
| Policy text becomes boilerplate in five places | Each surface gets the sentence that fits it (artifact vs reply), not a copy-paste block |

## Requirement-to-Design Traceability

| Requirement | Design element |
| --- | --- |
| FR-001–FR-003 | Template section; parser; placement rule + order waiver |
| FR-004–FR-005 | Row expander + id collector; fixture `uncovered` |
| FR-006 | Keyword scan over plain cells; fixture `commands` |
| FR-007 | Word cap; template instruction not to copy requirement text |
| FR-008–FR-009 | Terms table contract; gloss finder; fixtures `unglossed`, `long-gloss` |
| FR-010–FR-011 | Script + install step + gate assertions + fixtures |
| FR-012 | Seven policy surfaces |
| FR-013 | Script header; spec `## Out of Scope`; companion §6 |

## Implementation Boundaries

### Must Change

- `preset/templates/spec-addendum.md`, `preset/preset.yml`, `CHANGELOG.md`
- `scripts/check-plain-terms.py` (new), `scripts/check-section-integrity.sh`, `scripts/self-gate.sh`
- `preset/commands/*.prepend.md` (five), `commands/speckit.md`, `skill/.../SKILL.md`,
  `autonomy-contract.md`, `bin/speckit-init`
- `specs/00{1..6}-*/spec.md`, `specs/.conformance-baseline.json`
- `evals/fixtures/plain-terms/**` (new)

### Must Not Change

- Any requirement text in 001–006; any `Status` field in an accepted spec.
- The verification engine (`bin/speckit-verify`) and its harness.
- The constitution: a documentation rule does not need a governance amendment.

## What Changed / What Remains Open

Written at close-out in `progress.md`. Open at plan time: whether the plan layer is worth its
duplication (parking lot row 1), and whether any explanation is actually correct (review, not gate).
