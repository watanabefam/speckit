# Feature Specification: Plain Plans — a design a newcomer can follow

**Feature Branch**: `008-plain-plans`

**Created**: 2026-10-24

**Status**: Draft, narrowed 2026-10-25 (the layer is offered on a plan; the design-talk rule in the reply binds)

**Input**: User description: "Add the same plain-language layer to plan.md, so the design is readable by the person who did not write it."

## Document Status

**Status changed:** 2026-10-24 (created) · 2026-10-25 (narrowed: the plan layer became optional, per the owner's ruling that the documents are AI-facing first — `decisions/0009-the-rule-is-for-the-chat.md`)

**Approved by:** not yet approved · **Authority:** owner instruction of 2026-10-24, narrowed by the owner on 2026-10-25: *"I don't need plain language in the plan documents, just in the chat, because the documents are AI facing first."*

**What the narrowing changed.** FR-011 and US4 are the obligation now: how the agent *talks about a
design* — outcome first, design terms glossed, a plain column beside any design table. The section on a
plan is offered, with the rules below applying to a plan that carries one. Nothing already written was
deleted: the seven plans are accepted or drafted content (`decisions/0005`).

**Workflow:** full spec-driven · **Companion:** `docs/research/plans-plain-language-2026-10.md` (informative; four research rounds, the primary citations, and where the evidence stops)

## In Plain Terms

This feature lets an implementation plan carry the same short explanation layer a specification may
carry: a paragraph saying what will be built and why that shape, a table giving each requirement the
design choice made for it, and a list of the mechanism words the plan uses. It also makes design talk
followable in conversation, which is the half that binds. A **gloss** (a short
explanation in brackets, right after the word it explains) keeps those words from being a wall, and
**coverage** (every requirement identifier appearing in the document also appearing in the table)
keeps the explanation from falling behind the design. Each row is a **design decision** (a choice
about how the thing is built, and the reason for it) rather than a restatement of the requirement,
because the study of what readers actually understand found decisions help and format does not; and
each row must name an **artefact** (a file or command a reader can open) or a plan section, so the
reader is sent to the design instead of back to the specification.

| Item | In plain words | Technical |
| --- | --- | --- |
| US1 | A reader who did not write the plan can tell what will be built before meeting the design vocabulary. | US1 — the section exists, early, with a paragraph and one row per requirement |
| US2 | The plan's own words — "ledger", "falsify", "coverage report" — are explained where they first appear. | US2 — terms table and first-use glosses |
| US3 | A row must point at where the design lives, and the rows must keep up with the requirements. | US3 — artefact reference and identifier coverage |
| US4 | The habit applies to how the agent talks about design, not only to the file. | US4 — plan contribution, entry point, skill, bridge |
| FR-001–FR-003 | A plan may open with the section; when it does, it holds a real paragraph and the same table shape specifications use. | FR-001, FR-002, FR-003 |
| FR-004–FR-005 | Each requirement gets exactly one row; a gap, a repeat or an unknown identifier is an error. | FR-004, FR-005 |
| FR-006–FR-007 | Each row points at a section or file, explains the choice rather than restating the requirement, and stays short. | FR-006, FR-007 |
| FR-008 | The plan lists its mechanism words and brackets each one where it is first used. | FR-008 |
| FR-009–FR-010 | One checker handles specs and plans, and the gate runs it over every plan with a fixture for each failure shape. | FR-009, FR-010 |
| FR-011–FR-012 | The rule is installed with the kit, stated where the agent reads it, and never gated on a readability score or claimed to prove understanding. | FR-011, FR-012 |
| SC-001 | The seven existing plans carry the section, and every requirement they mention is covered once — an observation, not an obligation since 2026-10-25. | SC-001 |
| SC-002 | Every row in every plan names a section or a file, not only an identifier. | SC-002 |
| SC-003 | A well-structured peer plan with no plain layer is accepted by default and rejected under `--require-section`. | SC-003 |
| SC-004 | Adding a requirement to a plan without a row fails the gate, demonstrated and then reverted. | SC-004 |
| SC-005 | Every listed mechanism word is glossed at first use, and no gloss exceeds the cap. | SC-005 |
| SC-006 | The gate passes and examines more than it did before this feature. | SC-006 |

**Terms**

| Term | Plain words |
| --- | --- |
| gloss | a short explanation in brackets, right after the word it explains |
| coverage | every requirement identifier in the document appearing in the explanation table |
| design decision | a choice about how the thing is built, and the reason for it |
| artefact | a file, command or section a reader can open to see the design |

## Normative Status

**Normative:** User Scenarios & Testing, Requirements, Success Criteria. Everything else is
informative — including `## In Plain Terms`, whose explanations never bind.

### Which document wins

This spec is authoritative for behaviour. `docs/research/plans-plain-language-2026-10.md` carries the
citations and the four rounds; where the two disagree, this spec prevails.
`decisions/0008-plans-explain-the-design.md` records why the plan layer is keyed on requirements but
written as decisions.

## Problem / Opportunity

Feature `007` gave specifications a plain layer and left plans out, on the grounds that a plan layer
would duplicate the spec's. That reasoning was half right: a copy would duplicate, but a plan is the
first artifact an implementer reads, and it is where the unfamiliar words actually arrive —
*manifest*, *ledger*, *falsify*, *hermetic*, *vacuity*. The spec explains what is owed; nothing
explains how it is paid.

The measured context: this repository has **seven** plans totalling roughly 2,100 lines. Their
requirement coverage is uneven — two of the seven (`002`, `004`) were written before the plan template
and one of those (`004`) cites no requirement identifier at all. A newcomer reading the largest
(`005`, 478 lines, 43 functional requirements) meets the full design vocabulary with no entry point.

Two findings shape the repair. Ernst & Robillard (EMSE 2023, N=65) found **no significant association
between documentation format and understanding-task performance** — prior exposure to the source code
dominated. Shahin et al. (2014) found the **presence of design decisions significantly improved
understanding**. So the plan layer is not "a nicer table": it is a place where decisions and their
reasons are written down, and the table is only the cheapest way to keep that complete.

Peer check: citekit's `specs/001-web-search-source/plan.md` is well structured, readable to its
author, and carries no plain layer and no requirement identifiers. It is the negative control.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A newcomer can tell what the plan builds (Priority: P1)

A reader opening `plan.md` gets, before `## Technical Context`, a short paragraph saying what will be
built, out of what, and why this shape, then a table that gives each requirement one row: the design
choice made for it and where in the plan that design lives.

**Why this priority**: This is the whole request. Everything else keeps it true over time.

**Independent Test**: For ten requirement identifiers across the seven plans, read only the
`## In Plain Terms` row and say what the design does for that requirement and where to read more.

**Acceptance Scenarios**:

1. **Given** a plan with the section before `## Technical Context`, **When** a reader opens it,
   **Then** the paragraph and table appear before the design vocabulary.
2. **Given** a row, **When** it is read alone, **Then** it states a choice and its reason, not the
   requirement's demand.
3. **Given** a plan whose requirements changed, **When** the table no longer covers an identifier,
   **Then** the check fails and names it.

---

### User Story 2 - Mechanism words stop being a wall (Priority: P1)

A reader meets "coverage report", "falsify", "ledger" or "vacuity" and finds a bracketed gloss at the
point of first use, plus the plan's own list of mechanism words at the top of the section.

**Why this priority**: A plain summary full of undefined mechanism names moves the wall one paragraph
down. The terms table is what makes the paragraph usable.

**Independent Test**: Extract the terms table from a plan, find each term's first prose use, and
confirm a bracketed gloss within the same paragraph.

**Acceptance Scenarios**:

1. **Given** a term in the plan's terms table, **When** its first use is inspected, **Then** a
   bracketed gloss follows, at most 25 words.
2. **Given** a term that needs a clause, **When** it is written, **Then** it is a sentence and the
   bracket is not accepted as a gloss.
3. **Given** a mechanism word used but not listed, **When** the plan is reviewed, **Then** the gap is
   visible because the list is short and sits beside the explanation.

---

### User Story 3 - The explanation stays tied to the design (Priority: P2)

An owner adds `FR-044` to a plan, or writes a row that only repeats the identifier. The gate fails:
the first because no row covers the identifier, the second because a plan row must name a section or
a file where the design can be read.

**Why this priority**: Without it the section becomes a restatement of the spec with nothing about
the design — the failure mode the research identified. It is P2 because US1 and US2 deliver value on
their own.

**Independent Test**: Remove a row from a plan and run the check; then replace a `Technical` cell with
ids only and run it again. Both fail, naming the identifier or the row.

**Acceptance Scenarios**:

1. **Given** a plan missing one identifier, **When** the check runs, **Then** it exits nonzero and
   names the identifier.
2. **Given** a row whose `Technical` cell names no section and no file, **When** the check runs,
   **Then** it fails naming the row.
3. **Given** a clean plan, **When** the check runs, **Then** it passes and prints the rows, covered
   identifiers and glossed terms.

---

### User Story 4 - The habit covers design talk, not only specs (Priority: P1 — the surviving half)

The agent's reply about a design step leads with the outcome in ordinary words, glosses a design term
where it appears, and gives any table about the design a column saying what each row means.

**Why this priority**: The owner's complaint is about the workflow, which is mostly conversation.
This half cannot be enforced — a command is prompt text — so it is policy, checked in review.

**Independent Test**: Read the plan contribution, the entry point, the skill and the `AGENTS.md`
bridge of a fresh install and confirm each states the rule for plans as well as specs.

**Acceptance Scenarios**:

1. **Given** a fresh install, **When** the plan contribution is read, **Then** it carries the fill
   rule for the section and the design-specific content rule.
2. **Given** the entry point, **When** its plain-language paragraph is read, **Then** it covers plans.
3. **Given** the `AGENTS.md` bridge, **When** it is regenerated, **Then** it names plans too.

### Edge Cases

- **A plan with no requirement identifiers** (a legacy plan): the checker reports it as
  unexaminable rather than passing; the repair is to name the requirements the plan serves, which is
  an addition of one line.
- **A plan that mentions a requirement only to exclude it**: it still needs a row, and the row says
  what the plan deliberately does not do about it.
- **A requirement identifier from another feature** (a plan citing the gate's own spec): covered like
  any other identifier; the row explains what this plan does with it.
- **A plan with one section and no alternatives**: the table may hold one row; the paragraph still
  has to say why the obvious approach was chosen.
- **A property identifier** (`P-003`): not covered by the plain table. Properties already carry a
  `for any …` statement and a check method in their own table; covering them would duplicate the
  explanation the plan already gives. Recorded as a decision, not an omission.
- **A term whose first use is in a code span**: not a prose use, so not where the gloss belongs.

## Requirements *(mandatory)*

### Functional Requirements

**The section (US1)**

- **FR-001**: A `plan.md` MAY contain a section headed `## In Plain Terms`. Where it does, the section
  MUST precede `## Technical Context` — or, where that heading is absent, every top-level section other
  than `## Summary` — and the rules below apply. Where it does not, nothing is missing: the layer is
  offered, not demanded (`decisions/0009`).
- **FR-002**: The section MUST open with at least three sentences of prose before any table, saying
  what will be built, out of what, and why this shape.
- **FR-003**: It MUST contain a table whose header contains `Item`, `In plain words` and `Technical`.

**Coverage and content (US3)**

- **FR-004**: Every `FR` and `SC` identifier appearing in the plan MUST be covered by exactly one
  row; an uncovered, duplicated or unknown identifier MUST fail with a nonzero exit.
- **FR-005**: An `In plain words` cell MUST state the design choice and its reason rather than
  restating the requirement. The check cannot decide this; the template states it and review enforces
  it.
- **FR-006**: A `Technical` cell MUST name where the design lives — a section reference (`§…`) or a
  backticked artefact — and MUST NOT consist only of identifiers. The check MUST reject a row without
  either.
- **FR-007**: An `In plain words` cell MUST NOT contain `SHALL`, `MUST` or `SHOULD`, and MUST be at
  most 45 words.

**Terms (US2)**

- **FR-008**: The section MUST contain a terms table whose header contains `Term` and `Plain words`;
  each listed term MUST be followed by a bracketed gloss of at most 25 words at its first prose use
  at or after the section, and a listed term never used MUST be reported.

**Enforcement (US3)**

- **FR-009**: `scripts/check-plain-terms.py` MUST handle both artifacts, selecting the plan rules by
  file name or an explicit flag, MUST keep exit `0`/`1`/`2`, MUST be installed into adopter projects,
  and MUST be run by the kit's gate over every plan. A plan without the section MUST NOT be reported as
  a finding unless the caller passes `--require-section`.
- **FR-010**: The fixture corpus MUST add one conformant plan and one plan per failure shape — missing
  section, misplaced section, thin paragraph, `Technical` with no artefact, unglossed term — and the
  gate MUST assert each is rejected for its own reason under `--require-section`, plus that the same
  plan without the section passes when the flag is absent.

**Policy (US4)**

- **FR-011**: The rule MUST be stated in the plan contribution, the entry point, the skill and the
  `AGENTS.md` bridge, and delivered by the installer rather than by hand.

**Limits (US1–US3)**

- **FR-012**: The rule MUST NOT gate on a readability score, MUST NOT claim that the section improves
  comprehension, and the template and script MUST state that format showed no measurable effect and
  that the check verifies structure, coverage and defined terms only.

### Key Entities

- **Plan row**: `Item` (requirement identifiers), `In plain words` (the choice and its reason),
  `Technical` (a section reference or artefact).
- **Artefact reference**: a `§Section` or a backticked path in the `Technical` cell, which is what
  distinguishes a plan row from a spec row.
- **Coverage report**: identified, covered, uncovered, duplicated and unknown identifiers.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: **7 of 7** plans carry the section — an observation of the corpus — **100%** of the
  `FR`/`SC` identifiers they mention are covered exactly once, and **zero** are uncovered.
- **SC-002**: **100%** of plan rows name a section or a backticked artefact in `Technical`, and
  **zero** rows consist only of identifiers.
- **SC-003**: citekit's plan, which is well structured and has no plain layer, is accepted by default
  and rejected under `--require-section` — the negative control for both halves of the opt-in contract.
- **SC-004**: Adding one requirement identifier to a plan without a row makes the gate fail naming
  it, observed failing and then passing after the row is added.
- **SC-005**: **100%** of listed terms in every plan carry a bracketed gloss at first use, and
  **zero** glosses exceed 25 words.
- **SC-006**: The kit gate passes and its examined count is strictly greater than the **189** it
  reported before this feature.

## Out of Scope

- **A plain layer on `tasks.md`.** The plan is the artifact a newcomer reads first; tasks are a work
  queue and are already one sentence per item.
- **Rewriting plan prose.** The layer is an addition beside the design, not a simplification of it.
- **A readability score or a comprehension claim.** Format showed no measurable effect; the check
  claims structure, coverage and defined terms only.
- **Judging whether a row is accurate.** A covered-but-wrong row is a review finding.

## Evidence Base

`docs/research/plans-plain-language-2026-10.md` — four rounds: the two-level design document (Rust
RFC template, Google design docs, arc42 §1, Diátaxis), the glossing mechanics settled in `007`, the
empirical work (Ernst & Robillard 2023 on format; Shahin et al. 2014 on design decisions, via Rukmono
et al. 2025), and ISO/IEC/IEEE 42010's definition of rationale. Round four verified the citations and
added nothing.

## Assumptions

- The reader is new to this project, not new to programming. "Ledger" is explained; "a function" is
  not.
- Plans stay in English, and their identifiers follow the `FR`/`SC` convention the kit already uses.
- A plan that predates the template may need one line naming its requirements; that is an addition,
  not a rewrite.
- The three-sentence paragraph, the 45-word cell cap and the 25-word gloss cap are shape rules and
  brevity proxies, not quality measures.

## Requirements Syntax

**Not applicable — MUST in the RFC 2119 sense.** These requirements are checked by one script and by
review; they are not statements about a running system, so EARS (`SHALL`, one clause pattern per
requirement) buys nothing and the kit does not convert approved wording (`005` records the same
reason). The deliberate asymmetry from `007` holds: requirement text uses `MUST`, the plain layer may
not.

## Carried Forward

### Confirmed Decisions

- The section shape is identical to the spec's, so there is one habit and one checker (`0008`).
- Rows are keyed on requirements for decidability and written as decisions for usefulness.
- `Technical` must name an artefact or section; this is the plan-specific rule.
- Properties (`P-…`) are not covered; their own table already carries a plain statement.

### Constraints

- Python standard library only; the shell wrappers stay bash 3.2-safe.
- The preset change bumps the preset version and needs a `CHANGELOG` entry.
- The conformance baseline is regenerated because the plan template gains a required heading.

### Assumptions

Carried from `## Assumptions`. The load-bearing one is that coverage plus the artefact rule prevents
the layer from collapsing into a copy of the spec.

### Risks

- **The row restates the requirement.** Mitigated by the template's content rule, by requiring the
  artefact reference, and by review; not eliminated by a check.
- **Seven retrofits get the design wrong.** The rows are written by the author of the plans' subject.
  Mitigated by two plans read end to end and by the peer control; a non-author pass remains open.
- **The table is long where the plan is long** (`005`, 43 requirements). Mitigated by grouping rows
  into ranges, which the checker already supports.

### Open Questions

- **Should `tasks.md` follow?** Parked. A task is one sentence with a verifiable outcome; the
  vocabulary problem is smaller there.
- **Can a row's accuracy ever be checked?** No oracle exists that is not a reader, which is why the
  claim stays structural.

## Goals

- An agent reporting on a design leads with what was chosen and why, and points at where the design
  lives rather than reciting identifiers.
- A plan that explains its design cannot drift behind its own requirements without the gate saying so,
  and a plan that does not explain itself is not treated as incomplete.
- The plan stays optimised for the reader who acts on it first, which is the implementing agent.

## Non-Goals

- Simplifying or rewriting the plan's design text.
- Measuring comprehension or gating on reading level.
- A plan layer that duplicates the spec's explanations.

## Dependencies and External Contracts

- **`preset/templates/plan-addendum.md`** — where the section becomes required.
- **`scripts/check-section-integrity.sh`** — the order waiver for the new heading in plans.
- **`.specify/scripts/conformance-baseline.py`** — regenerated for the new required plan heading.
- **`bin/speckit-init`** — installs the updated checker and carries the bridge text.

## MVP Scope

The plan section in the template, plan mode in the checker with the artefact rule, five plan
fixtures, gate assertions over the seven plans, the policy sentence in the plan contribution and the
entry point, and the seven retrofits. The peer control is verification.

## Future Work (parking lot)

| # | Idea | Noticed during | Why deferred | Revisit when |
| --- | --- | --- | --- | --- |
| 1 | The same layer on `tasks.md` | Writing this spec | Tasks are one line each; the wall is in the design vocabulary | If a task list is the first artifact a newcomer reads |
| 2 | A reading test with real newcomers | Research round 3 | No novel reader here; the check is structural | Before claiming any comprehension effect |
| 3 | Generated rows from plan prose | Designing the artefact rule | A generator cannot know the reason behind a decision | If a reviewed generator is measured against human rows |

### Parking lot vs Non-Goals

A **Non-Goal** is refused: rewriting plans, a readability gate, a comprehension claim. A parked idea
is deferred: tasks, a reading test, generated rows.

## Validation Plan

- **Automated** — `python3 scripts/check-plain-terms.py specs/*/spec.md specs/*/plan.md`; the plan
  fixtures; gate assertions for each fixture's exit code and named finding; coverage of all seven
  plans.
- **Manual checks** — read `005` and `007` end to end and confirm each row states a choice and points
  at the design.
- **Peer check** — citekit's plan is rejected for the missing section.
- **Negative control** — each new fixture was observed failing before the control was observed
  passing.
- **Evidence required for approval** — gate `PASS examined=N` with N > 189, the checker green over
  specs and plans, five plan rejections.

## Requirement Traceability

| Requirement | User Story | Acceptance Criteria | Planned Design Area | Task |
| --- | --- | --- | --- | --- |
| FR-001–FR-003 | US1 | Scenarios 1–2 | `plan-addendum.md`; checker plan mode | T003, T008 |
| FR-004–FR-007 | US1, US3 | US1 3; US3 1–3 | checker coverage and artefact rule | T006, T010 |
| FR-008 | US2 | Scenarios 1–3 | template terms table; checker gloss rule | T004, T012 |
| FR-009–FR-010 | US3 | Scenarios 1–3 | `check-plain-terms.py`; gate; fixtures | T008, T014 |
| FR-011 | US4 | Scenarios 1–3 | plan contribution, entry point, skill, bridge | T019, T020 |
| FR-012 | US1–US3 | Out of scope; companion §3 | script header and spec text | T003 |
