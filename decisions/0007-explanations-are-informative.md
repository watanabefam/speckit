# 0007 — Explanations sit beside the requirements, are informative, and are checked for coverage

> **Narrowed 2026-10-25 by `0009`.** The section is now offered rather than demanded, and the rule that
> binds is the conversation one (§5 below). Everything this decision says about *how* an explanation is
> written and checked still holds wherever a document carries one.

## Context

The owner reports that the workflow slows development down because the artifacts are hard to
understand. The complaint is specific: a reader who is new to this project cannot tell what a
requirement binds, and specialist terms arrive undefined. Two candidate repairs were on the table —
rewrite the requirements in plainer words, or add an explanation layer beside them.

Rewriting is the wrong repair. Requirement text is the thing an implementation is judged against;
simplifying it trades precision for readability in the one place precision is load-bearing, and the
accepted artifacts (`0001`…`006`) were approved in their current wording, which `decisions/0005`
already establishes is not to be retro-fitted.

## Research

Recorded in `docs/research/plain-language-2026-10.md`. The load-bearing findings:

1. **Define, do not only avoid.** GOV.UK: specialist terms are allowed if "you explain what they mean
   the first time you use them"; Google: describe the term in plain language and give the term in
   parentheses. Avoidance is preferred where a plain word exists.
2. **Brackets are for terms, not clauses.** Google's parentheses guidance warns readers skip
   parenthetical text and says to keep asides short.
3. **A parallel plain layer is an established accessibility pattern** (WCAG 2.2 SC 3.1.5, technique
   G86: a summary "in addition to the original content").
4. **A plain layer must not create obligations** — ISO/IEC Directives Part 2 forbids requirements in
   notes and examples, which is the same rule the spec template already applies to informative
   sections.
5. **Readability formulas do not measure comprehension** (AHRQ; Schriver; Redish), so they cannot be
   a gate. Nor is there evidence that adding a summary, by itself, improves comprehension (Stoll et
   al. 2022); the measured effects come from *how* it is written — explaining content-specific terms
   (Kerwer et al. 2021, N=2,288 and N=2,211).
6. **Duplication drifts.** The mitigation is to point at the authoritative text, not copy it, and to
   fail when the two fall out of step.

## Decision

**1. Every spec carries `## In Plain Terms`, placed before the user stories.** It holds one short
paragraph saying what the feature does, a table mapping each user story, requirement and success
criterion to a plain-language sentence, and a table of the terms the document uses that a newcomer
may not know.

**2. The section is informative, not a second specification.** It may not contain `SHALL`, `MUST` or
`SHOULD`, and its technical column points at the requirement ids instead of restating them. Where it
and the normative text disagree, the normative text wins — and the disagreement is a defect in the
explanation.

**3. Jargon is glossed in parentheses at first use, and the gloss is short.** A term that needs a
sentence gets a sentence; a term that needs a clause does not get a bracket. The document's own terms
table is the list of what counts as jargon here, so the rule has an anchor rather than a global word
list that would be wrong for every project.

**4. The rule is checked for coverage and staleness, and not for quality.** `scripts/check-plain-terms.py`
fails a spec when the section is missing, when any `US`, `FR` or `SC` id is not covered exactly once,
when a plain cell carries a normative keyword, when a cell exceeds the brevity cap, or when a term in
the terms table has no bracketed gloss at its first use. It cannot tell whether an explanation is
*good* — that limit is stated in the script and in the spec rather than papered over.

**5. The policy binds conversation output as well as artifacts.** The entry point command, the five
step prepends, the skill, the autonomy contract and the `AGENTS.md` bridge all carry it: lead with
what happened, gloss a specialist term the first time it is used, and put a plain column beside any
table that summarises technical work.

## Consequences

- Six accepted specs gain a section they did not have. That is an addition, not a rewrite: no
  requirement text changes, and `0005`'s rule against retro-fitting stays intact — the plain layer is
  new content, and its absence in an accepted document was a real gap, not a formatting difference.
- The brevity cap (45 words per cell) is a proxy for "short enough to read", not a readability score.
  It is labelled as such because the evidence says a score would be a false signal.
- Coverage means the table cannot rot: adding `FR-044` without a row fails the gate. That is the same
  stale-entry mechanism as the conformance baseline, applied to understanding instead of structure.
- The kit's own chat output is now in scope of a documented rule. It is not enforced — a command is
  prompt text, and `0005`'s sibling principle (`Honest Enforcement`) applies. What is enforced is the
  artifact half.
