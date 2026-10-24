# Feature Specification: Plain Language — a specification a newcomer can actually use

**Feature Branch**: `007-plain-language`

**Created**: 2026-10-24

**Status**: Draft

**Input**: User description: "speckit is slowing down development due to difficulty understanding it. Ensure each of the specs is explained to a novice clearly in a table column (alongside technical descriptions it may already have), jargon explained in brackets as it is introduced, and make this the standard policy in speckit conversation output."

## Document Status

**Status changed:** 2026-10-24 (created)

**Approved by:** not yet approved · **Authority:** owner request of 2026-10-24; implementation proceeds on the owner's "implement unless my approval or decision are absolutely necessary"

**Workflow:** full spec-driven · **Companion:** `docs/research/plain-language-2026-10.md` (informative; three research rounds, the standards, the evidence limits, and the measured peer check)

## In Plain Terms

This feature adds a short, plainly written layer to every specification: a paragraph saying what the
feature does, a table that gives each requirement a one-sentence explanation beside its identifier (the
`FR-001`-style label the requirement carries), and a list of the specialist words the document uses. It
also makes the same habit the standing rule for anything the kit says in a conversation, not only for
the documents it writes.

A few words recur below. A **gloss** (a short explanation in brackets, right after the word it explains)
is where a specialist term is first met. **Coverage** (every identifier appearing in the table) is what
the check verifies, and a table that falls behind it is reported as **staleness** (an explanation that
no longer matches the identifiers around it) rather than passed. The 45-word cap is a **proxy** (a
stand-in measure that is cheap to compute and is not the thing itself) for brevity, never a readability
score.

| Item | In plain words | Technical |
| --- | --- | --- |
| US1 | A reader new to the project can find out what a feature does before meeting the numbered requirements. | US1 — plain layer present and placed before the stories |
| US2 | A word like "informative" or "staleness" is explained where it first appears, so the reader is not left guessing. | US2 — first-use glosses and a terms table |
| US3 | The explanation cannot quietly fall out of date: if a requirement is added without an explanation, the check fails. | US3 — coverage and staleness check in the gate |
| US4 | The habit applies to chat replies too, not just to files. | US4 — entry point, prepends, skill, bridge |
| FR-001–FR-003 | Every spec must have the section, must open it with a short paragraph, and must use a table with a fixed shape. | FR-001, FR-002, FR-003 |
| FR-004–FR-005 | Every story, requirement and success criterion must appear in exactly one row; a gap, a repeat or an unknown identifier is an error. | FR-004, FR-005 |
| FR-006–FR-007 | The explanation may describe but may not command, and it must stay short instead of restating the requirement. | FR-006, FR-007 |
| FR-008–FR-009 | The document lists its own specialist words, and each one is bracketed the first time it is used. | FR-008, FR-009 |
| FR-010 | The check runs on its own, runs in the gate, and is tested against both a good and four broken specs. | FR-010 |
| FR-011 | The rule is installed with the kit and appears wherever the agent reads its instructions. | FR-011 |
| FR-012–FR-013 | No readability score may be used as a gate, and the documents must not pretend an explanation proves understanding. | FR-012, FR-013 |
| SC-001 | All six existing specs gain the section, with every identifier covered once. | SC-001 |
| SC-002 | A correct spec that lacks the section is rejected — demonstrated on a peer project's spec. | SC-002 |
| SC-003 | No explanation cell in the repository commands anything. | SC-003 |
| SC-004 | Every listed specialist word is glossed where it first appears. | SC-004 |
| SC-005 | Adding a requirement without a row fails the gate, demonstrated and then reverted. | SC-005 |
| SC-006 | The gate passes with the new checks and examines more than it did before. | SC-006 |

**Terms**

| Term | Plain words |
| --- | --- |
| gloss | a short explanation in brackets, right after the word it explains |
| coverage | every identifier in the document appearing in the explanation table |
| staleness | an explanation that no longer matches the identifiers around it |
| proxy | a stand-in measure that is convenient to compute and is not the thing itself |

## Normative Status

**Normative:** User Scenarios & Testing, Requirements, Success Criteria. Everything else in this
document is informative (explanatory text that binds nothing) — including `## In Plain Terms`, whose
explanations are never a second source of truth.

### Which document wins

This spec is authoritative for behaviour. `docs/research/plain-language-2026-10.md` is informative: it
carries the citations and the three research rounds, and where the two disagree, this spec prevails.
`decisions/0007-explanations-are-informative.md` records why this shape was chosen over rewriting the
requirements.

## Problem / Opportunity

The owner reports that the workflow slows development down because the artifacts are hard to
understand. The cost is concrete and repeated: every phase boundary asks the reader to hold a
vocabulary they were never given. Measured on this repository's own accepted specs: 126 functional
requirements and 45 success criteria, written in six documents, and **zero** of them states in ordinary
words what a requirement binds. The template's core asks a story to be described "in plain language"
and then never asks again — the numbered requirements, the identifiers, and the abbreviations carry
all the meaning.

The peer check says this is not an authoring defect here. citekit's single spec scores 25 of 27 on
section conformance and has no plain-language layer either: the kit produces well-structured documents
that are opaque to the person who was not in the room. That is the gap this feature closes, at the
level where it is cheapest — an explanation layer beside the requirement, not a rewrite of it.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A newcomer can tell what a spec binds (Priority: P1)

An owner or a new contributor opens a specification to find out what a feature does. Before the user
stories they get one short paragraph and a table that says, in ordinary words, what each story,
requirement and success criterion is for. They can decide whether to read further without decoding the
identifiers first.

**Why this priority**: This is the complaint. Everything else in the feature makes this one durable or
makes it general; on its own it already removes the cost the owner is paying.

**Independent Test**: Open each spec in `specs/`, and for ten identifiers chosen at random, read only
the `## In Plain Terms` row and state what the identifier binds. No other section is consulted.

**Acceptance Scenarios**:

1. **Given** a spec with the section placed before its first story, **When** a reader opens it, **Then**
   a paragraph and a table explain the feature before any requirement is numbered.
2. **Given** the table, **When** a row is read on its own, **Then** it says what the item is for without
   using a normative keyword.
3. **Given** a spec whose requirements changed, **When** the table no longer covers the identifier set,
   **Then** the check fails and names the identifiers.

---

### User Story 2 - Specialist terms stop being a wall (Priority: P1)

A reader meets "informative", "oracle", "hermetic" or "staleness" (an explanation that no longer
matches what it describes) and finds a short explanation in brackets at the point of first use, plus a
list of the document's own terms at the front.

**Why this priority**: A plain summary that is itself full of undefined words moves the problem one
paragraph down. The glossary and the first-use gloss are what make the summary usable.

**Independent Test**: Extract the terms table from a spec, find each term's first use in the body, and
confirm a bracketed explanation is within the same paragraph.

**Acceptance Scenarios**:

1. **Given** a term listed in a document's terms table, **When** its first use is inspected, **Then** a
   bracketed gloss follows on the same line or the next.
2. **Given** a gloss that needs a clause to explain the term, **When** it is written, **Then** it is a
   sentence rather than a bracket, and the check does not accept the bracketed clause.
3. **Given** a term used but not listed, **When** the spec is reviewed, **Then** the omission is visible
   because the list is short and sits beside the summary.

---

### User Story 3 - The explanation cannot rot (Priority: P2)

An owner adds `FR-044`. The gate fails and names the identifier that has no explanation, so the table
cannot silently drift behind the requirements it explains.

**Why this priority**: Without this, the section joins the category the kit already treats as a ritual
— present on the day it was written, wrong a month later. It is P2 only because US1/US2 deliver value
before the check exists.

**Independent Test**: Add a requirement to a spec without a row, run the check, and confirm a nonzero
exit naming that identifier; add the row, and confirm it passes.

**Acceptance Scenarios**:

1. **Given** a spec missing one identifier from the table, **When** the check runs, **Then** it exits
   nonzero and names the identifier.
2. **Given** an identifier covered by two rows, **When** the check runs, **Then** it reports the
   duplicate.
3. **Given** a spec with no `## In Plain Terms` section, **When** the check runs, **Then** it fails
   rather than reporting an empty success.
4. **Given** a clean spec, **When** the check runs, **Then** it passes and prints how many identifiers
   it covered.

---

### User Story 4 - The habit applies to conversation, not just files (Priority: P3)

An owner reads the agent's reply to a technical step and can follow it: the outcome comes first, a
specialist term is explained where it appears, and a table summarising technical work carries a plain
column.

**Why this priority**: The owner's complaint is about the workflow, which is mostly conversation. But
this half cannot be enforced — a command is prompt text — so it is carried as policy and checked in
review, after the artifacts are fixed.

**Independent Test**: Fresh-install the kit into a scratch repository, read the entry point, the five
step prepends, the skill and the `AGENTS.md` bridge, and confirm each states the rule.

**Acceptance Scenarios**:

1. **Given** a freshly installed project, **When** its materialised command files are read, **Then**
   each step that writes or reports carries the plain-language rule.
2. **Given** the `AGENTS.md` managed block, **When** it is regenerated, **Then** it states the rule in
   the bridge rather than only in the skill.
3. **Given** the autonomy contract, **When** a response is written, **Then** the contract asks for the
   plain statement of the outcome and the bracketed gloss.

### Edge Cases

- **A spec with no user stories and no numbered criteria** (a template, a stub): the section is still
  required, and its table may hold one row explaining that the document has no numbered items. The
  coverage rule then holds vacuously, which is reported as zero covered rather than as a pass on
  content.
- **An identifier appearing only in a traceability table**: it is still an identifier and must be
  covered; the check reads the whole document.
- **A term listed but never used**: reported as a stale entry, not ignored — the same rule the
  conformance baseline applies to an excuse that no longer matches.
- **A term whose first use is inside a code span or a fenced block**: not counted as first use, because
  code is not prose the reader is expected to decode.
- **A document written in another language**: the check requires the section heading and table headers
  in English; a translated spec is out of scope and says so in the document.
- **The plain table is correct but the explanations are wrong**: not detectable by the check, and the
  spec says so rather than implying the check is a quality gate.

## Requirements *(mandatory)*

### Functional Requirements

**The section (US1)**

- **FR-001**: Every specification MUST contain a section headed `## In Plain Terms`, placed before the
  first `### User Story` heading.
- **FR-002**: That section MUST open with at least two sentences of prose saying what the feature does,
  before any table.
- **FR-003**: It MUST contain a table whose header contains the columns `Item`, `In plain words` and
  `Technical`.
- **FR-004**: Every `US`, `FR` and `SC` identifier that appears in the document MUST be covered by
  exactly one row of that table. An `Item` cell MAY list several identifiers and closed ranges.
- **FR-005**: An identifier that is uncovered, covered twice, or listed but absent from the document
  MUST be reported as a failure with a nonzero exit.

**The boundary (US1)**

- **FR-006**: A cell in the `In plain words` column MUST NOT contain `SHALL`, `MUST` or `SHOULD`. The
  plain layer explains; it does not command.
- **FR-007**: A `In plain words` cell MUST be at most 45 words, and its `Technical` cell MUST point at
  the identifiers rather than restate their text.

**Terms (US2)**

- **FR-008**: The section MUST contain a terms table whose header contains `Term` and `Plain words`,
  listing each specialist term the document uses.
- **FR-009**: The first **prose** use of each listed term MUST be followed by a bracketed gloss of at
  most 25 words. Table lines MUST NOT count as a first use — listing a term is not introducing it — and
  a bracketed clause longer than 25 words MUST be reported rather than accepted.

**Enforcement (US3)**

- **FR-010**: The check MUST be a standalone script that exits `0` for a conformant spec, `1` for a
  finding, and `2` for a usage error, MUST be installed into adopter projects, and MUST be run by the
  kit's gate over every spec.
- **FR-011**: A fixture corpus MUST include a conformant spec and one fixture per failure shape —
  missing section, uncovered identifier, normative keyword, unglossed term — and the gate MUST assert
  that each is rejected.

**Policy (US4)**

- **FR-012**: The rule MUST be present in the entry point command, the `specify`, `plan`, `tasks`,
  `implement` and `converge` contributions, the skill, the autonomy contract and the `AGENTS.md`
  bridge, and MUST be delivered by the installer rather than by hand.

**Limits (US1–US3)**

- **FR-013**: The rule MUST NOT gate on a readability score, and the script and the spec MUST state
  that the check verifies presence, coverage and brevity — not whether an explanation is correct or
  understood.

### Key Entities

- **Plain row**: one table row — `Item` (identifiers), `In plain words` (a sentence), `Technical` (the
  identifiers it stands for).
- **Term**: an entry in the document's terms table, with the plain words that explain it.
- **Coverage report**: the set of identifiers found, the set covered, and the three failure lists
  (uncovered, duplicated, unknown).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: **6 of 6** accepted specs contain the section, **100%** of their `US`/`FR`/`SC`
  identifiers are covered exactly once, and **zero** identifiers are uncovered.
- **SC-002**: A spec that is section-conformant but has no plain layer is rejected — demonstrated on a
  peer project's specification with **zero** rows found.
- **SC-003**: **Zero** `In plain words` cells in the repository contain a normative keyword.
- **SC-004**: **100%** of terms in every terms table carry a bracketed gloss at first use, and **zero**
  bracketed glosses exceed the 25-word cap.
- **SC-005**: Adding one requirement without a row makes the gate fail, naming that identifier —
  observed failing, then observed passing after the row was added.
- **SC-006**: The kit gate passes with the new checks, and its examined count is strictly greater than
  the **164** it reported before this feature.

## Out of Scope

- **Rewriting requirement text in plainer words.** The requirement is what an implementation is judged
  against; `decisions/0005` already refuses to retro-fit accepted wording, and this feature adds a
  layer instead.
- **A readability score, grade level, or word-frequency gate.** Readability formulas do not measure
  comprehension (AHRQ, Schriver, Redish; see the companion §6), so a score would be a false signal that
  invites tuning.
- **Judging whether an explanation is accurate or understood.** Not machine-checkable here; the spec
  says so and the manual check is named.
- **Translating specifications.** One language, stated as an assumption.
- **A plain-language layer on `plan.md` and `tasks.md`.** The owner asked for the specs; plans and tasks
  carry the conversation policy instead. Parked, not refused.

## Evidence Base

`docs/research/plain-language-2026-10.md` — three rounds: the standards (plainlanguage.gov/OPM,
GOV.UK, Microsoft, Google, WCAG 3.1.5 and G86, ISO/IEC Directives Part 2), the limits (AHRQ, Schriver,
Redish on readability formulas; Stoll et al. 2022 on plain-language summaries; Kerwer et al. 2021 on
what makes one work), and the peer measurement (citekit, 25/27 conformance, no plain layer). Design
consequences and the points where no source supports us are recorded there rather than here.

## Assumptions

- The audience is a newcomer to **this** project, not a novice programmer. Explaining "oracle" is in
  scope; explaining what a function is, is not.
- Specifications stay in English; the check's headings are English strings.
- The owner accepts a section that is informative by construction, and accepts that a wrong explanation
  is a review finding rather than a gate failure.
- The 45-word and 25-word caps are brevity proxies chosen so a row can be read at a glance; they were
  not validated against readers, and the companion says so.

## Requirements Syntax

**Not applicable — MUST in the RFC 2119 sense, not EARS.** EARS (`SHALL`, one clause pattern per
requirement) arrived with spec 001 for requirements that must be machine-checkable in form. This
spec's requirements are checked by reading and by one script; the reason for not rewriting them into
EARS is the same one recorded in `005-verification-integrity`: converting approved wording is an
amendment with its own review, not a template migration. Note the deliberate asymmetry: requirement
text may use `MUST`, the plain layer may not — that asymmetry is this feature's subject.

## Carried Forward

### Confirmed Decisions

- The explanation is additive and informative; requirement text is unchanged (`decisions/0007`).
- The check covers presence, coverage, brevity and glosses; it does not judge quality.
- No readability score anywhere in the gate.
- The conversation policy lives in the commands, the skill, the contract and the bridge — not in a
  constitution amendment, which would need approval and a version bump for a documentation rule.

### Constraints

- Python standard library only, and the shell wrappers must parse on bash 3.2 (macOS).
- The checker is installed by `speckit-init` beside `check-section-integrity.sh`, because a check that
  only exists in the kit's own repository does not reach adopters.
- Preset changes bump the preset version and add a `CHANGELOG` entry (constitution, development
  workflow).

### Assumptions

Carried from `## Assumptions`. The load-bearing one is that a wrong-but-covered explanation is
acceptable risk: coverage prevents silence, and review catches error.

### Risks

- **The section becomes a ritual** — a table filled to satisfy the check. Mitigated by coverage plus
  brevity plus the requirement to say something the requirement does not already say; not eliminated.
- **Duplication drifts** — the plain column and the requirement diverge. Mitigated by forbidding
  normative keywords and copied text, and by the coverage check failing on identifier changes.
- **Six retrofits get it wrong** — the explanation is written by the same author as the original and
  inherits its assumptions. Mitigated by the peer test (SC-002) and by a review pass on two specs.

### Open Questions

- **Should the same section be required on plans?** Parked; the owner asked for specs, and a plan's
  plain layer would duplicate the spec's. Revisit when a plan is the first artifact a newcomer reads.
- **Can correctness of an explanation ever be checked?** Not found; an oracle would be a reader.

## Goals

- A reader who was not in the room can tell what each requirement binds, in one row, without decoding
  vocabulary.
- The explanation cannot fall behind the requirements without the gate saying so.
- The same habit is visible in the agent's conversation output, not only in the files.

## Non-Goals

- Replacing or simplifying normative requirement text.
- Measuring comprehension, reading level, or explanation quality.
- Covering `plan.md` and `tasks.md` in this feature.
- Any network dependency, model call, or new runtime dependency.

## Dependencies and External Contracts

- **The spec template addendum** (`preset/templates/spec-addendum.md`) — where the section becomes
  required; a preset change, so it bumps the preset version.
- **`scripts/check-section-integrity.sh`** — the order waiver for the new heading, so a spec that
  follows the instruction to place the section early is not reported as reordered.
- **`.specify/scripts/conformance-baseline.py`** — the baseline is regenerated because a required
  heading was added; all six specs must be retrofitted rather than excused.
- **`bin/speckit-init`** — installs the checker and carries the bridge text; `specify` CLI 1.2.2 is
  present on this machine, so the composed commands can be regenerated here.

## MVP Scope

The section, the checker with its four failure shapes, the gate assertion, the template requirement,
the policy text in the entry point and the five prepends, and the six retrofits. The peer test and the
conversation-policy review are verification, not extra scope.

## Future Work (parking lot)

| # | Idea | Noticed during | Why deferred | Revisit when |
| --- | --- | --- | --- | --- |
| 1 | Plain layer on `plan.md` | Writing this spec | Owner asked for specs; a plan's layer would duplicate the spec's | When a plan is the first artifact a newcomer reads |
| 2 | A reading test with real newcomers | Research round 2 | No access to a novel reader here; the check is structural | Before claiming any comprehension effect |
| 3 | Auto-generated plain rows from requirement text | Designing coverage | A generated summary cannot know the intent behind a requirement; it would ship fluent wrongness | If a reviewed generator is ever measured against human rows |

### Parking lot vs Non-Goals

A **Non-Goal** is refused: a readability gate, comprehension measurement, rewording the requirements.
A **parked idea** is deferred: a plan layer, a reading test, generated rows. Nothing moves from the
table into scope without its own spec.

## Validation Plan

- **Automated** — `python3 scripts/check-plain-terms.py specs/*/spec.md` over every spec; the fixture
  corpus under `evals/fixtures/plain-terms/` with one conformant and four failing specs; gate assertions
  for each fixture's exit code and for the six retrofits.
- **Manual checks** — read two retrofitted specs (001 and 006) end to end and confirm a row explains
  without commanding; read a rendered reply for the conversation rule.
- **Peer check** — run the checker against citekit's spec and confirm rejection with zero rows.
- **Negative control** — every fixture was observed failing before the checker was observed passing.
- **Evidence required for approval** — gate `PASS examined=N` with N > 164, the checker green over
  `specs/*/spec.md`, four fixture rejections, and the peer rejection.

## Requirement Traceability

| Requirement | User Story | Acceptance Criteria | Planned Design Area | Task |
| --- | --- | --- | --- | --- |
| FR-001–FR-003 | US1 | Scenarios 1–2 | `spec-addendum.md` section; checker presence check | T002, T004 |
| FR-004–FR-005 | US1, US3 | Scenarios 1, 3; US3 1–2 | checker coverage | T005 |
| FR-006–FR-007 | US1 | Scenario 2 | checker boundary; template wording | T006 |
| FR-008–FR-009 | US2 | Scenarios 1–3 | template terms table; checker gloss rule | T007 |
| FR-010–FR-011 | US3 | Scenarios 1–4 | `scripts/check-plain-terms.py`; gate; fixtures | T008, T009 |
| FR-012 | US4 | Scenarios 1–3 | entry point, prepends, skill, contract, bridge | T010, T011 |
| FR-013 | US1–US3 | Out of scope; companion §6 | script header and spec text | T003 |
