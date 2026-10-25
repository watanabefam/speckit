# 0008 — Plans explain the design beside the requirements, and the explanation is checked

> **Narrowed 2026-10-25 by `0009`.** A plan is offered this layer rather than required to carry it; the
> rule that binds is design talk in the reply, and the artefact rule below applies to a plan that
> opts in. The reason a row names a decision and points at where the design lives is unchanged — that
> half is what an implementing agent reads.

## Context

Feature 007 gave every specification an informative `## In Plain Terms` section and made plain
language the rule for the kit's own replies. It deliberately left `plan.md` out, and recorded the
reason: a plan's layer looked like it would duplicate the spec's. The owner has now asked for the
plan to be readable too — a plan is the first artifact an implementer reads, and it is where the
design vocabulary (components, mechanisms, trade-offs) arrives without definition.

The open question was not whether to add something but **what the plan's unit should be**. A copy of
the spec's rows would explain the obligation a second time. Rows keyed on decisions would be
unverifiable, because plans do not number their decisions. The research
(`docs/research/plans-plain-language-2026-10.md`) settled it.

## Research

1. **The two-level design document is established practice.** The Rust RFC template places a
   *Guide-level explanation* ("explain… as if you were teaching it to another Rust programmer";
   introduce named concepts) before the *Reference-level explanation*, and tells the reference
   section to return to the guide's examples. Google's design docs open with a succinct "context and
   scope" that links detail rather than copying it. arc42 §1 asks for a short extract of the
   requirements with links, and explicitly warns to "balance readability… with potential redundancy
   w.r.t. requirements documents".
2. **Format does not measurably improve understanding.** Ernst & Robillard (EMSE 2023, N=65) found
   no significant association between narrative versus structured architecture documentation and
   understanding-task performance; prior exposure to the source code dominated.
3. **Decisions and rationale do.** Shahin et al. (2014, as reported by Rukmono et al. 2025) found the
   presence of architectural design decisions significantly improved understanding, while not
   changing task time. Rukmono et al.'s interviews describe an "explanation window" that balances the
   problem and technical domains, and name the rationale behind decisions as a key concern.
4. **Rationale is part of an architecture description.** ISO/IEC/IEEE 42010 defines Rationale as the
   explanation or justification of architecture decisions "and architectural alternatives not
   chosen".
5. **Diátaxis warns that explanation absorbs what belongs elsewhere** — it must stay bounded, and
   the reference detail keeps its own home.

## Decision

**1. Every plan carries the same `## In Plain Terms` section as a spec**, with the same two tables
and the same columns. One shape to learn, one checker, one habit. It is placed before
`## Technical Context` — before the first section other than `Summary` — because the guide level
comes before the reference level.

**2. Rows are keyed on the plan's requirement ids, but the content is the design choice and why.**
Coverage is decidable only against identifiers. The sentence, though, answers "what did we choose,
and what does it buy?" — not "what does `FR-004` demand?" — because that is the part the evidence
says a reader cannot supply for themselves. A row that restates the requirement is a defect in the
explanation, and the template says so.

**3. `Technical` must name where the design lives.** For a plan the cell must reference a section
(`§Architecture Overview`) or a backticked artefact (`bin/speckit-verify`), not merely repeat ids. An
id-only cell sends the reader back to the spec and explains nothing about how the thing is built.
This is the one rule that differs from the spec layer, and it is checked.

**4. The terms table lists the plan's mechanisms**, glossed in brackets at first prose use, at most
25 words. A plan that explains its requirements but leaves "coverage report", "falsify" or "ledger"
undefined has moved the wall, not removed it.

**5. The check is extended, not duplicated.** `scripts/check-plain-terms.py` gains a plan mode
(`--kind auto|spec|plan`, auto by file name) with the plan's placement rule, a three-sentence
paragraph, the artefact reference, and the same coverage, brevity and gloss rules. The gate runs it
over every spec and every plan.

**6. The claim is bounded.** Format showed no effect on understanding, so neither the template nor
the check claims one. What the check can say is: the section is present and early, every requirement
is covered once, every row points at the design, every listed mechanism is defined. Whether a row is
*right* remains a review finding, exactly as `0004` records for a section that is present but empty.

## Consequences

- Six accepted plans gain a section they did not have (this feature's own plan carries it from the
  start). One of the six (`004`) does not cite a single requirement id, so it gains one line naming
  the requirements it covers — an addition that makes the existing design traceable rather than a
  rewrite of it.
- `plan.md` is now a checked artifact in two ways (section conformance and plain terms). The
  conformance baseline is regenerated, and the order waiver is extended so a plan that follows the
  instruction to place the section early is not reported as reordered.
- The template demands a shape the evidence does **not** say improves comprehension. It is adopted
  because it defines the terms and states the decisions — the two things the evidence does support —
  and because a documented rule with a check is the only form this kit can hold. That distinction is
  in the spec, the script header and the research record.
- The spec/plan division stays intact: the spec's row says what is owed, the plan's row says how it
  is paid and why that way. Neither is a copy, and the plan's `Technical` cell is required to point
  at the design so the difference is visible.
