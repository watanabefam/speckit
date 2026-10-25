---

<!--
  Appended by the spec-driven-development preset (strategy: append).
  The core sections above remain authoritative and unchanged. These sections add
  problem framing and traceability that the core template does not carry.
-->

<!--
  WHEN A SECTION DOES NOT APPLY

  Keep the heading and say why: `Not applicable — <reason>`. Never delete it. The reason belongs
  in the section because the whole point of a fixed outline is that a reader can tell "this did not
  apply" from "this was forgotten" — a deleted heading is indistinguishable from an omission, and
  the omission is the failure mode this outline exists to catch.

  A bare `N/A` is accepted by the checker (it is content), and there is no reviewed tooling that
  requires a justification after a non-applicability claim — so the obligation to write a reason is
  a rule of this template, enforced by review, not by the machine.

  An empty section is NOT accepted: `scripts/check-section-integrity.sh` fails an artifact whose
  required heading has nothing under it, because filling the outline with empty headings would make
  conformance a ritual. A heading whose only content is subsections is fine (container sections are
  expected); a heading followed by a code block is fine (the block is content).

  A section that never applies to any spec of this kind is a template defect, not an authoring
  defect: mark it OPTIONAL in the template, which the checker honours, rather than asking every
  author to write "not applicable".
-->

## Document Status

**Place this block immediately after the core metadata block** (the `Feature Branch` / `Created` /
`Status` / `Input` lines), not at the end where this section lands.

The core template already carries a `**Status**` field. **Do not add a second status field** — two
status fields will eventually disagree, and a reader will not know which one to believe. This
section *defines* the core field's lifecycle and records the approval metadata the core does not ask
for.

**Lifecycle for the core `Status` field** — an open set, in the manner of MADR (Markdown
Architectural Decision Records), which deliberately does not standardise a closed enum:

`Draft` → `Accepted` → `Deprecated` | `Superseded by <id>`

`Draft` means not yet agreed; `Accepted` means in effect and safe to rely on; `Deprecated` means
discouraged but not replaced; `Superseded by <id>` means replaced, and must name its replacement.
**Never edit a superseded spec, and never reuse an id.**

Record the remaining metadata here:

```
**Status changed:** YYYY-MM-DD (last status change)
**Approved by:** <who> · **Authority:** <what authorised it>
**Workflow:** <full spec-driven | short path> · **Companion:** <path, or "none">
```

Approval is **three separate facts** — who, when, and under what authority. Do not collapse them
into the status word: `Accepted` does not say who accepted it, or why they were entitled to. This is
the field a reader needs when asking "can I rely on this?", so it has to answer that.

## Normative Status

A specification has two kinds of content, and conflating them is how specs become untestable.

- **Normative** — binds conformance. A requirement here is one an implementation can be judged
  against, pass or fail.
- **Informative** — assists understanding. Rationale, background, examples, and notes.

This distinction is standard, not stylistic: ISO/IEC Directives Part 2 §3.2 defines it, the W3C QA
Framework requires a spec to state how the two are distinguished, and IETF practice splits
references into normative and informative. Two rules follow, and both are checkable:

1. **Requirements live only in normative sections.** ISO/IEC is explicit that notes and examples
   "shall not contain requirements" — they are always informative. Do not smuggle a requirement into
   a note, an example, or a comment. A reader who skips the informative material must still be able
   to build the right thing.
2. **Normative keywords do not appear in informative sections.** If a rationale section says
   "the system SHALL…", either it is a requirement that belongs above, or the wording is wrong.
   Avoid language that *sounds* binding outside the normative sections.

**State the boundary in the document.** Say which sections are normative. Silence leaves the reader
to guess, and the guess is usually that everything binds.

### Which document wins

When a companion document exists — research notes, a design rationale, a brief — declare the
authority relationship explicitly and **with a dated reference**:

> This spec is authoritative for behaviour. `<companion path>` is informative: it carries research
> and rationale, and where the two disagree, this spec prevails.

There is no automatic precedence between two documents. ISO, W3C, and IETF all require the
relationship to be stated (a dated reference fixes the version; an undated one floats and will
eventually contradict you). A companion document that is not labelled informative will be read as
competing with the spec, and nobody will know which one to follow.

## In Plain Terms

**This section is optional, and it is informative.** It exists so a reader who was not in the room can
tell what the feature does before meeting the numbered requirements. It is not a second specification:
where it and the normative text disagree, the normative text wins, and the disagreement is a defect in
the explanation.

**Why optional.** The owner's ruling of 2026-10-25 (`decisions/0009-the-rule-is-for-the-chat.md`): these
artifacts are read by an agent first, so a plainly written layer is a convenience for the human who
reads second, not an obligation on every document. The conversation is where the rule binds; this
section is where it *may* show up in the artifact. What the kit does enforce is that a section you do
carry stays true — leave it out and the checker says so and passes, fill it in and it must cover every
identifier. A project that wants it everywhere passes `--require-section`.

**Place it before the first `### User Story` heading** — a reader who needs the explanation should not
have to pass the requirements to find it.

Three parts, in this order:

1. **A paragraph.** At least two sentences saying what the feature does, in the words you would use to
   a colleague who has never read this repository. Before any table.
2. **The table.** One row per explanation, with exactly these columns:

   | Item | In plain words | Technical |
   | --- | --- | --- |
   | FR-001–FR-003 | What these requirements make happen, for whom, and why it matters. | FR-001, FR-002, FR-003 |

   `Item` holds identifiers — `US1`, `FR-007`, `SC-002` — and may list several, comma-separated or as a
   closed range (`FR-001–FR-006`). Rows may group, but **every** `US`, `FR` and `SC` identifier in the
   document must appear in exactly one row. `Technical` points at the identifiers; it does not restate
   their text, because a copy drifts and an id does not.
3. **The terms table.** The specialist words this document uses, each with the plain words that explain
   it. This is the document's own list: there is no global dictionary, because a term that is jargon in
   one project is ordinary in another.

   | Term | Plain words |
   | --- | --- |
   | normative | the text a build can be judged against — pass or fail |

**Rules that the check enforces**, and why each exists:

- **No `SHALL`, `MUST` or `SHOULD` in an `In plain words` cell.** The plain layer explains; it must not
  command. Two normative voices eventually disagree, and the reader cannot tell which one binds. (The
  asymmetry is deliberate: the requirement text uses `MUST`, the explanation may not.)
- **At most 45 words per cell.** A brevity **proxy**, not a readability score — formulas measure
  sentence length, not understanding (see `docs/research/plain-language-2026-10.md` §6). A long cell is
  a sign the row is covering something that deserves its own row.
- **A bracketed gloss at first prose use.** Every term in the terms table must be followed by `(...)`
  the first time it appears in a **sentence at or after this section** — the paragraph above is the
  natural place — and the bracket holds **at most 25 words**. Table lines do not count, so listing a
  term is not the same as introducing it; nor does the metadata above this section, which is status
  rather than reading and may quote the requester verbatim. This is the convention GOV.UK and Google both document; neither supports burying a
  clause in a bracket. If the term needs a sentence, write a sentence and keep the bracket for the term.
- **Once you keep the section, nothing in it is exempt for being obvious.** A short spec needs a short
  row, not a heading with nothing under it.

**What the check cannot do, stated so nobody trusts it further than it goes:** it verifies that the
section exists, that every identifier is covered once, that no cell commands, and that the listed terms
are glossed. It cannot tell whether an explanation is *correct*, and it cannot tell whether a reader
understood it. A covered-but-wrong row is a review finding, not a gate failure — the same limit
`decisions/0004` records for a section that is present but empty.

**The same habit applies to what the agent says.** A reply leads with what happened in ordinary words,
glosses a specialist term the first time it uses it, and puts a plain column beside any table that
summarises technical work. The entry point, the step contributions and the skill carry that rule; this
section is where it shows up in the artifact.

## Requirements Syntax (EARS)

Every functional requirement is written in **EARS** (Easy Approach to Requirements Syntax). EARS
constrains free-form prose into a small set of testable shapes, so a reviewer can write an
acceptance check from the requirement text alone.

**Use `SHALL` for every required behaviour — never MUST, SHOULD, or a bare lowercase verb.**
`SHALL` is the only normative keyword here (RFC 2119 sense). Mixing in MUST, or writing "the
system validates…", leaves it ambiguous whether the behaviour is binding.

**But do not `SHALL` everything.** RFC 2119 §6 is explicit that these keywords "must be used with
care and sparingly", and "must not be used to try to impose a particular method on implementors
where the method is not required for interoperability." A requirement that merely describes how
something happens to work is informative — write it as prose. Reserving `SHALL` for behaviour that
actually binds is what keeps the word meaningful; a spec where every sentence is `SHALL` has
abolished the distinction it was trying to make.

| Pattern | Keyword | Shape | Use when |
| --- | --- | --- | --- |
| Ubiquitous | *(none)* | `THE <system> SHALL <response>` | the behaviour is always active |
| Event-driven | `WHEN` | `WHEN <trigger> THE <system> SHALL <response>` | a response is required to a triggering event |
| State-driven | `WHILE` | `WHILE <state> THE <system> SHALL <response>` | the behaviour holds while a state is true |
| Optional feature | `WHERE` | `WHERE <feature is included> THE <system> SHALL <response>` | it applies only to variants that include a feature |
| Unwanted behaviour | `IF` / `THEN` | `IF <unwanted condition> THEN THE <system> SHALL <response>` | a response is required to a fault, failure, or undesired situation |

Examples:

- **Ubiquitous** — `THE <system> SHALL prevent concurrent edits to the same record.`
- **Event-driven** — `WHEN a request carries an expired token, THE <system> SHALL reject it with an authentication error.`
- **State-driven** — `WHILE a sync is in progress, THE <system> SHALL queue further writes.`
- **Optional feature** — `WHERE audit logging is enabled, THE <system> SHALL record the acting user.`
- **Unwanted behaviour** — `IF the upstream service is unavailable, THEN THE <system> SHALL retry with backoff and report a degraded status.`

**Clause order is fixed** and follows temporal logic: preconditions (`WHILE`, `WHERE`) precede
the trigger (`WHEN`), which precedes the system response. Requirements that combine keywords are
**complex** — e.g. `WHILE <state>, WHEN <trigger>, THE <system> SHALL <response>`. Use the fewest
clauses that work; if a requirement needs more than three, split it.

**Common misuse:** `WHEN` is for an event, not a state; `WHILE` is for a state, not an event;
`IF…THEN` is for unwanted behaviour and is evaluated on the second pass — do not use it for the
normal path; `WHERE` denotes a variant, not a location.

This guidance is deliberately **language-agnostic**. The property-based testing framework (if any)
is decided per project in `plan.md`. Do not hardcode a framework (e.g. Hypothesis) into a
requirement.

## Carried Forward

Summary of what this artifact inherits from the work before it. Keep it short — it is a
handoff, not a retelling.

### Confirmed Decisions

- [Decision already settled by the user or by earlier evidence]

### Constraints

- [Constraint that limits the solution space]

### Assumptions

- [Assumption being carried in; becomes a risk if it is wrong]

### Risks

- [Known risk, and how it would show up]

### Open Questions

- [Unresolved item that affects behavior, scope, architecture, or acceptance]

## Problem / Opportunity

[What problem or opportunity exists, for whom, and why does it matter now? If this is not a
real problem, the feature should not be built.]

*Placement:* this block is appended last, but problem-first reading is better than requirements-first,
so `scripts/check-section-integrity.sh` waives ORDER for this heading (presence is still required).
Put it directly after the document-status block if the document reads better that way.

## Goals

- [Outcome this feature is meant to produce]

## Non-Goals

- [Explicitly **not** being solved here. Prevents silent scope expansion.]

## Dependencies and External Contracts

- [Service, API, data source, schema, or external contract this feature depends on, and what
  happens if it changes]

## MVP Scope

[The smallest slice that delivers the value of the highest-priority user story. Everything
else is Future Work.]

## Future Work (parking lot)

Deliberately deferred. Not part of this feature's acceptance criteria. Must not be implemented
without explicit approval.

This section is also the **parking lot**: the place an out-of-scope idea goes the moment you notice
it, so it is neither acted on nor lost. Scope control without somewhere to put the idea produces one
of two failures — silent scope creep, or an idea that gets dropped and never seen again. Parking is
the door in the wall.

**Capture, do not act.** When you notice something worth doing that is not in the approved scope:
write it here, and continue the task you were on. Do not implement it because it is small, obvious,
or adjacent. Do not silently drop it either — an unrecorded idea is indistinguishable from one that
was never had.

| # | Idea | Noticed during | Why deferred | Revisit when |
| --- | --- | --- | --- | --- |
| 1 | | | | |

- **Noticed during** — the phase or task where it surfaced. Useful context when it comes back.
- **Why deferred** — one line. "Not this feature" is acceptable; unstated is not.
- **Revisit when** — a trigger: after this ships, when the schema changes, if users ask. A parked
  idea with no revisit condition is just a nicer way of losing it.

### Parking lot vs Non-Goals

They are different, and conflating them hides work:

- **Non-Goals** are decided **upfront** — deliberately excluded from this feature, on purpose.
- **The parking lot** is noticed **in passing** — not yet decided, just not now.

A Non-Goal is a decision. A parked idea is a deferral awaiting one.

**Review the parking lot at close-out** (`/speckit.converge`) and at each phase boundary. Promote
an item to a spec, keep it parked with a reason, or delete it deliberately. What must not happen is
reviewing it never.

## Validation Plan

How this feature will be proven, before implementation starts.

- **Automated tests** —
- **Manual checks** —
- **Data or migration checks** —
- **Security / privacy checks** —
- **Performance checks** —
- **Evidence required for approval** —

## Requirement Traceability

Fill in as the work progresses. A requirement with no task is unbuilt; a task with no
requirement is scope creep.

| Requirement | User Story | Acceptance Criteria | Planned Design Area | Task |
| --- | --- | --- | --- | --- |
| FR-001 | US1 | Given / When / Then | | |
