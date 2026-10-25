# Implementation Plan: Plain Plans — a design a newcomer can follow

**Branch**: `008-plain-plans` | **Date**: 2026-10-24 | **Spec**: `specs/008-plain-plans/spec.md`

**Narrowed 2026-10-25** (`decisions/0009-the-rule-is-for-the-chat.md`): the plan layer is offered rather
than required. Read "required" below as "offered", and the artefact rule and placement rule as applying
to a plan that carries the section. The design-talk half in the reply is unaffected and is now the
obligation.

## Summary

Add `kind` to the checker, plan rules to the template, five plan fixtures and one generated property
set, wire them into the gate, retrofit seven plans, and state the rule in the surfaces the agent
reads. One new script mode, no new artifact type.

## In Plain Terms

This plan extends the existing plain-terms checker with a **plan mode** (a second set of rules,
chosen by the file's name, for documents that describe how something is built) so a plan can explain
its own design the way a spec explains its requirements. The checker keeps one **coverage** (every
identifier in the document appearing in the explanation table) rule for both artifacts and adds one
plan-only rule: a row must name a section or a file where the design can be read — an **artefact**
(a file, command or section a reader can open) — instead of only repeating identifiers. Template,
fixtures, gate assertions and the seven existing plans follow; nothing about the spec layer changes.

The unit is the requirement identifier, because that is the only set the script can enumerate. The
content of each row is the design choice and its reason, because the empirical evidence says
decisions and their rationale are what improve understanding, while presentation format showed no
measurable effect. A **gloss** (a short bracketed explanation at first use) keeps the plan's
mechanism words from being a wall.

| Item | In plain words | Technical |
| --- | --- | --- |
| FR-001–FR-003 | Each plan opens with the same section layout a spec uses, but placed before the technical context so the reader is oriented first. | `preset/templates/plan-addendum.md` §In Plain Terms; checker placement rule |
| FR-004–FR-005 | Every requirement the plan mentions gets exactly one row, written as the choice made and why, so the table cannot pass by repeating the spec. | `check_plan` coverage; template content rule |
| FR-006 | A row that only repeats identifiers is rejected, because it sends the reader back to the spec instead of into the design. | `ARTEFACT_RE` in `scripts/check-plain-terms.py` |
| FR-007 | A row explains and does not command, and stays short enough to scan. | `NORMATIVE_RE`, `PLAIN_LIMIT` |
| FR-008 | The plan lists the mechanism words it uses and brackets each one where it first appears. | terms-table parse; `GLOSS_LIMIT` |
| FR-009 | One script handles both kinds of document and the gate runs it over every plan. | `--kind` flag; gate §3f |
| FR-010 | Each failure has its own small broken plan, so the gate proves rejection rather than asserting it. | `evals/fixtures/plain-terms/plan-*`; harness |
| FR-011 | The rule is installed with the kit and appears in the files the agent reads. | `bin/speckit-init`; plan contribution |
| FR-012 | No score is gated and no understanding is claimed, because the evidence does not support either. | `scripts/check-plain-terms.py` header; template limits paragraph |
| SC-001 | All seven plans gain the section with their requirements covered. | retrofit of `specs/00*/plan.md` |
| SC-002 | Every row points at a section or a file. | `has_artefact` over the corpus |
| SC-003 | A competent peer plan without the layer is rejected. | citekit `plan.md` |
| SC-004 | Dropping a row makes the gate fail, observed and then reverted. | §3f teeth test |
| SC-005 | No unglossed term and no over-long gloss remains. | `scripts/check-plain-terms.py` over the corpus |
| SC-006 | The gate is green and examines more than before. | `make test` |

**Terms**

| Term | Plain words |
| --- | --- |
| plan mode | the second rule set in the checker, chosen for documents that describe how something is built |
| coverage | every identifier in the document appearing in the explanation table |
| artefact | a file, command or section a reader can open to see the design |
| gloss | a short bracketed explanation at first use |

## Technical Context

- **Language**: Python 3 standard library only; the checker is a single file with no imports beyond
  `json`, `re`, `sys`.
- **Platform**: macOS and Linux; the shell wrappers remain bash 3.2-safe.
- **Dependencies**: none new. `bin/speckit-init` already installs `check-plain-terms.py` to
  `.specify/scripts/`; the same file gains the mode.
- **Testing**: fixture corpus plus a generated property harness
  (`evals/fixtures/plain-terms/harness.py`), driven by `scripts/self-gate.sh` §3e/§3f and `make test`.
- **Compatibility**: spec mode keeps its current findings and exit codes; the gate's existing 25
  §3e assertions must not change meaning.

## Constitution Check

- **Requirements before code** — spec `008` precedes this plan; the plan's plain section is written
  before the checker implements the rule it describes. Pass.
- **Evidence before done** — each fixture is observed failing before the control passes; the gate
  count is compared with the **189** recorded at `007`'s close. Pass.
- **Honest enforcement** — the content rule (a row states a decision) is review, not a check, and is
  labelled so in the template. Pass.
- **Proportion** — no new dependency, no new command, one script and one artifact section. Pass.

## Project Structure

### Documentation (this feature)

```text
specs/008-plain-plans/
├── spec.md
├── plan.md
├── tasks.md
└── progress.md
```

### Source Code (repository root)

```text
scripts/check-plain-terms.py        # plan mode, artefact rule, --kind
scripts/self-gate.sh                # §3f assertions over plans and plan fixtures
preset/templates/plan-addendum.md   # the required section and its rules
preset/commands/speckit.plan.prepend.md  # the fill rule for the design layer
preset/preset.yml                   # 1.18.0
evals/fixtures/plain-terms/plan-*/  # one control and five broken plans
evals/fixtures/plain-terms/harness.py    # plan properties P-005…P-009
specs/*/plan.md                     # seven retrofits
```

**Structure Decision**: the repository is a single project rooted at the workspace; scripts live in
`scripts/` and are installed by `bin/speckit-init` into `.specify/scripts/`. No new directory is
introduced.

## Complexity Tracking

Not applicable — no new project, dependency, data store or external contract. The one new option is a
flag on an existing script.

## Carried Forward

### Confirmed Decisions

- The section heading and columns are identical to the spec layer (`0008`).
- Requirement identifiers are the coverage unit; `P-…` properties are excluded and the reason is in
  the template.
- `Technical` must contain `§` or a backtick.
- No readability score, no comprehension claim.

### Constraints

- Bash 3.2 compatibility for the gate; Python 3 stdlib only.
- Generated files (`.specify/`, `.opencode/`, `AGENTS.md` block) are never hand-edited.
- The gate's examined count must rise, so the new assertions are additional, not replacements.

### Assumptions

- Plans name the requirements they serve. `004` does not, and gains one line.
- Plans carry `FR`/`SC` identifiers; a plan that deliberately has none is reported as unexaminable.

### Risks

- **Retrofit quality** — seven plans written by the same author; mitigated by reading two end to end
  and by the peer control.
- **Coverage noise from cross-feature ids** — a plan may cite another feature's requirement; the row
  explains what this plan does with it, which is correct but adds rows.
- **Mode detection surprises** — mitigated by an explicit `--kind` and by treating an unknown
  basename as a spec, with the fixture asserting the default.

### Open Questions

- Whether `tasks.md` follows is parked, not decided.
- Whether the artefact rule should accept a bare filename without backticks: not for now; a
  backticked path is unambiguous and cheap to write.

## Scope Confirmation

### In Scope

- Plan mode in the checker, including placement, three-sentence paragraph, coverage, artefact rule,
  brevity and glosses.
- The plan template section and its rules.
- Five plan fixtures, generated properties, gate assertions.
- Seven retrofits, including one line of requirement ids in `004`'s plan.
- Policy text in the plan contribution, entry point, skill, installer bridge.
- Preset 1.18.0, `CHANGELOG`, conformance baseline regeneration.

### Out of Scope

- `tasks.md`, spec-mode changes, generated rows, readability scoring.

### Requirements Affected

FR-001–FR-012, SC-001–SC-006.

## Repository Findings

Inspected before designing:

- `scripts/check-plain-terms.py` — one `check_file` with spec rules hard-coded; `SECTION_RE`,
  `IDENT_RE`, `PLAIN_LIMIT`, `GLOSS_LIMIT`, `expand_item`, `parse_tables`, `column_index`.
- `scripts/self-gate.sh` §3e — corpus over `specs/*/spec.md`, eight fixture probes, a teeth test, a
  harness count of ≥66, nine policy surfaces, one peer spec.
- `preset/templates/plan-addendum.md` — the appended section list; the plan contribution names that
  list verbatim, so adding a heading requires editing both or the command instructs the agent to drop
  the new section.
- `scripts/check-section-integrity.sh` — an `ORDER` waiver list keyed on heading names.
- `scripts/conformance-baseline.py` — a generated baseline of required headings per artifact kind.
- `bin/speckit-init` — installs `check-plain-terms.py` and regenerates the composed commands; the
  bridge heredoc carries the agent-facing rule.
- `evals/fixtures/plain-terms/harness.py` — renders synthetic specs and runs the checker; 66 checks.

### Relevant Components

- the checker, the gate, the plan template, the plan contribution, the installer, the fixture harness.

### Existing Behavior

- `check-plain-terms.py specs/008-plain-plans/spec.md` → `16 rows, 22 identifiers covered, 4 terms
  glossed`. Plans are not checked at all, and a plan passed to the script is checked as a spec.

### Existing Tests

- §3e covers the spec corpus and eight spec fixtures; nothing covers a plan or a plan-shaped
  document.

### Project Conventions

- One script per rule, with a header stating what it cannot do; a fixture per failure shape; a gate
  assertion per claim; a generated file is never edited; a preset change bumps the version and the
  changelog.

### Constraints Discovered

- `check-section-integrity.sh` matches headings by name across artifact kinds, so a plan waiver must
  be added or plans following the new placement instruction are reported as reordered.
- `column_index` already accepts a header cell containing extra words, which the plan template can
  rely on.
- `norm()` strips `*` and backticks, so a `Technical` cell's backticks survive the artefact check but
  not the header match — the artefact rule must read the raw cell, not the normalised one.

## Architecture Overview

The checker gains a small dispatch layer. `artifact_kind(path, override)` returns `spec` or `plan`
from `--kind` or the file name. `check_file` keeps the shared parsing (section span, tables,
identifiers, terms) and delegates the artifact-specific decisions to two rule sets: the existing spec
placement and two-sentence paragraph, or the plan placement, three-sentence paragraph and artefact
requirement. Coverage, duplicates, unknown identifiers, the normative-keyword ban, the word cap and
the gloss rules stay shared, because they mean the same thing for both artifacts.

## Major Components

- **`kind` dispatch** — selects rules; `auto` by basename, explicit `--kind` for other names.
- **Placement rules** — spec: before the first `### User Story`; plan: before `## Technical Context`,
  else before the first top-level section other than `## Summary`.
- **Artefact rule** — each plan row's raw `Technical` cell must contain `§` or a backtick.
- **Paragraph rule** — three sentences for plans, two for specs.
- **Template section** — `preset/templates/plan-addendum.md`.
- **Fixture corpus and harness** — `plan-good`, `plan-no-section`, `plan-misplaced`,
  `plan-thin-paragraph`, `plan-no-artefact`, plus a generated property set.
- **Gate section §3f** — corpus, fixtures, teeth, harness, peer control, policy surfaces.

## Data Flow

`path` → `artifact_kind` → `parse` (unfenced lines, section span, tables) → `collect_ids` (FR/SC from
the whole body, section excluded) → rules (placement, paragraph, coverage, artefact, brevity,
glosses) → `findings[]` → exit code `0`/`1`/`2` and a per-file summary line or `--json`.

## Interfaces and Contracts

- CLI: `check-plain-terms.py [--json] [--kind auto|spec|plan] <file> [...]`. Exit `0` conformant,
  `1` at least one finding, `2` usage or read error. Unchanged from the spec-only contract apart from
  the optional flag.
- Finding kinds added: `plan-placement`, `thin-paragraph`, `no-artefact`. Existing kinds keep their
  names and messages, so the gate's §3e probes stay valid.
- Template contract: `## In Plain Terms` with `Item | In plain words | Technical` and
  `Term | Plain words`, placed as above.

## Dependencies

- None new. `bin/speckit-init` installs the updated script through its existing copy step.

## Error Handling

- An unreadable file exits `2` with the path; an unknown `--kind` value exits `2` with the allowed
  values. A plan with no `## In Plain Terms` reports `no-section` and stops, as for specs, because
  later findings would be noise. A plan that is misdetected (a spec named `plan.md`) will fail the
  plan placement rule; the error message names the expected heading so the fix is obvious.

## Security and Privacy

Not applicable — the script reads local Markdown and prints findings; it writes nothing and makes no
network call.

## Performance and Reliability

Linear in document size; the seven plans add roughly 2,100 lines, which is negligible. Reliability
comes from the fixture corpus and the gate, not from the script's runtime.

## Validation Strategy

- `python3 scripts/check-plain-terms.py specs/*/spec.md specs/*/plan.md` → all conformant.
- Each plan fixture produces its asserted exit code and named finding.
- `make test` → `SELF-GATE: PASS examined=N`, N > 189.
- Manual read of `005` and `007` plans.
- Peer control: citekit's plan is rejected.

## Correctness Properties

| Property ID | Requirement | Spec rule | Scope | `for any …` statement | Falsification | Check method | Non-mapped reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P-001 | FR-004 | each requirement gets exactly one row | operation | for any plan and any grouping of its identifiers into rows, the set of uncovered identifiers equals the set difference, and grouping never changes the verdict | drop one id from the control and observe `uncovered` | property-test | — |
| P-002 | FR-006 | a row must point at the design | operation | for any `Technical` cell containing neither `§` nor a backtick, the check fails naming the row; with either, it does not | remove the section reference from a control row | property-test | — |
| P-003 | FR-001 | placement before the technical context | operation | for any plan whose section appears after `## Technical Context`, the check fails; before it, passes | move the section in the control | property-test | — |
| P-004 | FR-002 | three sentences before any table | operation | for any paragraph of 1 or 2 sentences the check fails; 3 or more passes | shorten the control's paragraph | property-test | — |
| P-005 | FR-009 | one script, two modes | operation | for any spec fixture, `--kind plan` changes the verdict and auto mode does not | run the spec control under both kinds | property-test | — |

**Falsification** — each property is demonstrated on a fixture that must fail before the control is
accepted, and the gate repeats the demonstration.

**Scope** — `operation`: the claim is about one check run on one document.

### Rules

- **A property names its check method.** Every row above is `property-test`; a plan row with `—` there
  would be a wish.
- **The oracle is the harness, not the checker's opinion.** Each generated case is a document the
  checker either accepts or rejects; the expectation is written in the harness before the checker runs
  it.
- **Falsification is executed, not described.** P-002, P-003 and P-004 each fail a fixture first; the
  gate repeats the demonstration on a real plan (`§3f`).
- **Opt out explicitly.** No requirement here is left both unmapped and unexplained; the coverage table
  in `tasks.md` names a task and a property for every requirement.

### Framework decision

**None adopted.** The existing harness is plain Python with generated inputs; a property-testing
dependency is not justified for a text checker and would be the only runtime dependency in the kit's
scripts. Properties are checked by the harness (`property-test`), the gate (`runtime-assert`), and by
reading the fixture each one names.

### Traceability

`FR-004 → P-001 → T027`, `FR-006 → P-002 → T028`, `FR-001 → P-003 → T029`, `FR-002 → P-004 → T030`,
`FR-009 → P-005 → T031`. A property with no task would be unbuilt; a task with no requirement would be
scope creep.

### Independence

This is template and script text, so it applies whenever `/speckit.plan` runs with this preset — whether
or not the skill loaded. Under the `lean` preset, which replaces the commands and bypasses templates,
it does not apply.

## Alternatives Considered

| Option | Advantages | Disadvantages | Decision |
| --- | --- | --- | --- |
| A separate `check-plan-terms.py` | Independent evolution; smaller files | Two installs, two contracts, two habits; the shared rules would drift | Rejected |
| A plain column inside each existing plan table | Literal "alongside the technical descriptions"; no new section | Tables vary per plan and are absent in two; no place for the paragraph or the terms; the checker would have to special-case seven table shapes | Rejected |
| Rows keyed on component names instead of requirements | Closer to how a reader thinks about a design | Prose names are not enumerable, so coverage cannot be decided, and the table would rot silently | Rejected |
| Rows keyed on requirements, written as decisions, with a required artefact reference | Decidable coverage; content matched to the evidence; one shape across artifacts | Requires an artefact in every row, which is stricter than the spec layer | Selected |

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Seven retrofits are thin or copy the spec | Medium | High | Content rule in the template; manual read of two plans; artefact rule forces a pointer |
| Coverage grows noisy for plans citing other features | Medium | Low | Rows explain what *this* plan does with the identifier; grouping keeps the count down |
| Mode auto-detection misreads a renamed file | Low | Medium | `--kind` override documented in the script header and the template |
| The gate's §3e probes break on a refactor | Low | High | Existing findings and messages preserved; §3e asserted unchanged in the same run |

## Requirement-to-Design Traceability

| Requirement | Design Decision | Reason |
| --- | --- | --- |
| FR-001–FR-003 | Section contract in the plan template; placement in `check_file` | The guide level must arrive before the reference detail |
| FR-004–FR-005 | Shared coverage; content rule in the template | Coverage is decidable; the decision-vs-restatement rule is not |
| FR-006 | `ARTEFACT_RE` on the raw cell | The only plan-specific rule; it separates a plan row from a spec row |
| FR-007 | Shared `NORMATIVE_RE` and `PLAIN_LIMIT` | Same boundary as the spec layer, one implementation |
| FR-008 | Shared terms parse and gloss finder | The mechanism words are the plan's jargon |
| FR-009–FR-010 | `--kind`, fixtures, gate §3f | One script and one fixture per failure shape |
| FR-011 | Plan contribution, entry point, skill, bridge | The rule must be present where the agent reads |
| FR-012 | Script header and template limits paragraph | The evidence supports structure, not comprehension claims |

## Implementation Boundaries

### Must Change

- `scripts/check-plain-terms.py`, `scripts/self-gate.sh`, `preset/templates/plan-addendum.md`,
  `preset/commands/speckit.plan.prepend.md`, `preset/preset.yml`, `CHANGELOG.md`,
  `bin/speckit-init`, `commands/speckit.md`, `skill/spec-driven-development/SKILL.md`,
  `scripts/check-section-integrity.sh`, the fixture corpus, seven `plan.md` files, the conformance
  baseline.

### Must Not Change

- The spec rules' behaviour and messages (§3e depends on them), the spec addendum's contract, the
  gate's existing assertion count, and any requirement text in `specs/00*/spec.md`.

## What Changed / What Remains Open

- **Changed from the spec:** nothing at spec level; the artefact rule was made mechanical rather than
  review-only, because it is the rule that keeps the layer from being a copy.
- **Still open:** `tasks.md`; a non-author read of the seven retrofits.
- **Needs approval:** the spec's `Draft` status.
