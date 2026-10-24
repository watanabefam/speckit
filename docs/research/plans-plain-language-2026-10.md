# Plain language for implementation plans — evidence and design limits

Companion to `specs/008-plain-plans/`. Informative: it carries the citations and the reasoning;
where it and the spec disagree, the spec prevails.

**Question.** Specs carry `## In Plain Terms` (feature 007) so a reader who was not in the room can
tell what a requirement binds. Plans do not, and a plan is where the design vocabulary arrives:
components, mechanisms, trade-offs, and identifiers carried over from the spec. Does a design
document have a documented plain layer to copy, what actually helps a newcomer understand a design,
and what can a check verify?

**Stopping rule, declared before round 1.** Iterate while a round can change one of four decisions:
the **shape** of the layer (section, table, or a column inside tables the plan already has), the
**unit** it is keyed on (requirements, decisions, components, or fixed sections), the
**enforcement** (which properties a script can decide), and the **claim** the feature is allowed to
make about understanding. A round that only re-confirms a source or verifies a citation is empty.
Stop after two consecutive empty rounds.

**Rounds run: 4.**

| Round | What was searched | What it changed |
| --- | --- | --- |
| 1 | The design-document template canon: Rust RFC template, Google design docs, arc42 section 1, Diátaxis | Settled **shape** — overview and guide-level material comes before the technical portion, and it points at detail rather than copying it |
| 2 | Glossing and the reader's blind spot: GOV.UK/Google parentheses rules, expert blind spot | No change: confirms 007's first-use bracket rule and the 25-word cap |
| 3 | Empirical work on architecture understanding: Ernst & Robillard 2023, Shahin et al. 2014 (via Rukmono et al. 2025), ISO/IEC/IEEE 42010 rationale | Changed the **unit** — rows are keyed on requirements but written as the choice and its rationale, because decisions are what the evidence says helps; also bounded the **claim** |
| 4 | Verified the Ernst & Robillard citation at its abstract and the 42010 rationale definition at the standard's own conceptual-model page | Empty: confirmed round 3, added no design element |

Round three is the reason the feature is not merely "the spec layer again". Round four is the
primary-source check the plan command's research rules require; it is recorded as empty rather than
as a fifth round, because a citation trace cannot change a decision by itself.

## 1. A design document has a documented two-level shape

**Rust RFC template** — `Summary` (one paragraph), `Motivation`, then **`Guide-level explanation`**
and **`Reference-level explanation`**, in that order. The guide-level section is defined as:

> Explain the proposal as if it was already included in the language and you were teaching it to
> another Rust programmer. That generally means: introducing new named concepts; explaining the
> feature largely in terms of examples; explaining how Rust programmers should *think* about the
> feature… If applicable, provide sample error messages… describe the differences between teaching
> this to existing Rust programmers and new Rust programmers.

The reference-level section is "the technical portion", and it "should return to the examples given
in the previous section". ([template](https://github.com/rust-lang/rfcs/blob/master/0000-template.md))

Two things follow. The plain layer is **teaching**, not a summary of the technical text: it
introduces *named concepts*. And the two levels are about the **same object** — the reference
section returns to the guide's examples — so keying both layers on the same requirements is not
duplication; it is the shape the canon already uses.

**Google design docs** (Malte Ubl) — the first section is `Context and scope`: "a very rough
overview of the landscape in which the new system is being built and what is actually being built.
This isn't a requirements doc. Keep it succinct! The goal is that readers are brought up to speed…
detailed info can be linked to." The design itself "should start with an overview and then go into
details", and the document's length target is 10–20 pages.
([Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/))

**arc42 §1 (Introduction and Goals)** — the requirements overview is "short description of the
functional requirements… extract (or abstract) of requirements. Links to the (hopefully existing)
requirements documents". Its form guidance is explicit about the cost this feature risks:

> Keep these excerpts as short as possible. Balance readability of this document with potential
> redundancy w.r.t. requirements documents.

([arc42 section 1](https://docs.arc42.org/section-1/))

That is the strongest argument *against* copying the spec's plain rows into the plan: a second copy
of the same explanation is redundancy the standard tells authors to balance away. It is why the plan
row is written as the design choice, and why its `Technical` cell must name where the design lives.

**Diátaxis, explanation** — explanation is "understanding-oriented", "higher and wider" than
reference, answers "Can you tell me about…?", and "tends to absorb other things… allowing them to
creep in interferes with the explanation itself". ([Diátaxis](https://diataxis.fr/explanation/))

Consequence: the layer is bounded. It explains; it does not take over the data flow, the contracts,
or the error handling. Those stay in their sections, where a reader who needs them knows to look.

## 2. The mechanics of glossing were settled in 007, and nothing here overturns them

GOV.UK allows a specialist term provided it is explained at first use; Google documents "briefly
describe it in parentheses on first reference" and warns readers may skip parenthetical text, so a
bracket holds a term, not a clause. The expert blind spot literature is the mechanism behind the
failure mode: expertise makes it hard to perceive what a novice will find difficult (Nathan &
Koedinger's framing, cited in the newer architecture-explanation study below). The 25-word bracket
cap and the 45-word cell cap are brevity **proxies** (cheap stand-in measures), not readability
scores — the AHRQ, Schriver and Redish findings in
[`plain-language-2026-10.md`](plain-language-2026-10.md) §6 still apply, and no score is gated on.

Round two added no new rule. It is recorded because an empty round that is not logged cannot be
told apart from no round at all.

## 3. Format does not measurably help; decisions do

**Ernst & Robillard (2023)**, *A Study of Documentation for Software Architecture*, EMSE. A
controlled questionnaire study, N=65, comparing **narrative essays** with **structured documents**
for answering architecture-understanding questions:

> We… observed no significant association between the format of architecture documentation and
> performance on architecture understanding tasks. Instead, prior exposure to the source code of the
> system was the dominant factor associated with answer quality… Although more participants agreed
> that the structured document was easier to navigate and use for writing code, this relation was
> not statistically significant. We conclude… our results contradict the hypothesis that the format
> of architectural documentation matters.

([arXiv:2305.17286](https://arxiv.org/abs/2305.17286), accepted to EMSE)

**Shahin et al. (2014)**, on Architectural Design Decisions, as reported by Rukmono et al. (2025):

> The study found that while the use of ADDs in documentation does not affect task completion time,
> the presence of ADDs significantly improves architecture design understanding.

**Rukmono et al. (2025)**, *From Expert to Novice: An Empirical Study on Software Architecture
Explanations*, 17 interviews (9 explainers, 8 explainees):

> An explanation must balance both problem and technical domains while considering the explainee's
> role, experience, and the goal of the explanation. The concept of the **explanation window**, which
> adjusts the level of detail and scope, is introduced… effective software architecture explanations
> hinge on addressing key concerns such as the system's context, complexity management, and the
> rationale behind architectural decisions.

([arXiv:2503.08628](https://arxiv.org/html/2503.08628v1))

Three consequences, and the first one is the reason this feature is not "007 applied to plans":

1. **Do not claim the table improves understanding.** Format showed no effect; a structural check
   can only claim presence, coverage and defined terms. The spec says so.
2. **Write the row as a decision with its reason.** The content that measurably improved
   understanding was the design decisions and their rationale — not the presentation. A row that
   restates the requirement has copied the thing the evidence says is not the difficulty.
3. **Adjust the window.** The explanation is for a newcomer to *this* project: it says what the
   piece is and why it exists at that level of detail, and leaves the precise contract to the
   contract section.

## 4. Rationale is part of an architecture description, not an extra

ISO/IEC/IEEE 42010's conceptual model defines **Rationale** as:

> Rationale records the explanation, justification or reasoning about Architecture Decisions that
> have been made and architectural alternatives not chosen.

([42010 conceptual model](http://www.iso-architecture.org/ieee-1471/cm/))

So a design description whose decisions carry no rationale is incomplete by the standard's own
vocabulary. The plan template already asks for `Alternatives Considered` and a traceability reason;
the plain layer makes the same demand in the reader's words, which is the smallest form of it.

## Design that follows

| Decision | Evidence | What it rules out |
| --- | --- | --- |
| Plans carry the **same section and columns** as specs (`## In Plain Terms`, `Item \| In plain words \| Technical`, then `Term \| Plain words`) | 1, 3 | a second shape to learn; two checkers; a plan layer that reads as a different genre |
| Placed before `## Technical Context` (before the first section other than `Summary`) | 1 | a guide-level explanation that arrives after the reference detail |
| Rows are **keyed on the plan's requirement ids** but written as the **design choice and its reason** | 1, 3, 4 | a copy of the spec's rows; a table of non-decisions; a table keyed on prose component names that no check can enumerate |
| `Technical` must name the **artefact or section** (a `§` reference or a backticked path), not only ids | 1, 3 | an id echo that sends the reader back to the spec; a row that explains nothing about how |
| The document's **mechanism words** go in the terms table and are glossed at first use | 2 | undefined vocabulary — the failure the owner reported for specs, moved into the design |
| Rows carrying normative keywords are rejected, and cells are capped at 45 words | 007 §1, 3 | a second normative voice; a row that becomes a paragraph and stops being scannable |
| The check verifies presence, placement, coverage, the artefact reference and the glosses — **not** whether a row is right or understood | 3 | a claim of comprehension gains the study does not support |

## Limits of this pass

- The evidence is about *architecture* documentation with newcomers, not about this kit's plan
  template with its owner. The design borrows the direction of the finding (decisions and rationale
  help; format does not), not a measured effect size for this artifact.
- Shahin et al. was read through Rukmono et al.'s summary, not at the primary paper; it is cited
  as reported and marked so.
- ISO/IEC/IEEE 42010 was read at the standard's conceptual-model page, not the paid text.
- The peer check is citekit's `specs/001-web-search-source/plan.md`: a competent, well-structured
  plan with no plain layer and no requirement ids. It is a negative control for the missing section,
  not for a wrong one.
