# Plain language for specifications — evidence and design limits

Companion to `specs/007-plain-language/`. Informative: it carries the citations and the reasoning;
where it and the spec disagree, the spec prevails.

**Question.** An owner reports that the kit slows development down because the artifacts are hard to
understand. Three proposals arrived with that complaint: give every spec a plain-language column
beside its technical text, gloss jargon in brackets as it is introduced, and make both the standing
policy for spec-driven output. Which of those is supported, in what form, and what can be checked?

**Stopping rule, declared before round 1.** Iterate while a round can change a decision: the shape of
the explanation (paragraph, table, or both), whether jargon is avoided or defined, which mechanism
enforces any of it, and whether a readability score may gate. Stop when two consecutive rounds add
nothing that changes one of those four. Rounds run: three. Round three (the pattern and drift check)
confirmed round two's design and added only the informative/binding split, which was already the
template's rule; a fourth round was not run because no remaining question was decision-relevant.

## What the primary standards say

1. **Avoid jargon where a plain word works; define it where it does not.** The federal guidance's
   indexed heading is "Avoid legal, foreign, and technical jargon"; OPM's plain-language page says
   "Avoid using undefined technical terms"
   ([Digital.gov guide](https://digital.gov/guides/plain-language),
   [OPM](https://www.opm.gov/information-management/plain-language/)). GOV.UK is more precise:
   "Avoid government 'buzzwords' and jargon", but "Where you need to use specialist terms, you can.
   They're not always jargon. You just need to explain what they mean the first time you use them"
   ([clear language](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/)).
   Microsoft accepts jargon as shorthand for a well-understood audience and warns it "can impede
   understanding" for others ([avoid jargon](https://learn.microsoft.com/en-us/style-guide/word-choice/avoid-jargon)).
2. **First use in parentheses is a documented convention, not an invention.** Google's jargon page
   says to describe the term "in plain language" and give the term in parentheses, or "briefly
   describe it in parentheses on first reference" ([jargon](https://developers.google.com/style/jargon)).
   GOV.UK's A–Z glosses an abbreviation the same way — "Personal Independence Payment (PIP)" — and
   reserves square brackets for editorial notes
   ([A–Z](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/style-guides/a-to-z-style-guide/)).
   Chicago uses parentheses for translations and abbreviation introductions
   ([FAQ](https://www.chicagomanualofstyle.org/qanda/data/faq/topics/Abbreviations/faq0105.html)).
3. **But do not bury meaning in a bracket.** Google's parentheses page warns readers may skip
   parenthetical text, and says to keep in-sentence asides short or move longer material to its own
   sentence ([parentheses](https://developers.google.com/style/parentheses)). So a gloss is for a
   term, not for a clause.
4. **A parallel plain layer is an accessibility pattern.** WCAG 2.2 SC 3.1.5 (AAA) asks for
   "supplemental content, or a version" when text exceeds lower-secondary reading level, and technique
   G86 describes a summary "provided in addition to the original content"
   ([understanding 3.1.5](https://www.w3.org/WAI/WCAG22/Understanding/reading-level.html),
   [G86](https://www.w3.org/WAI/WCAG22/Techniques/general/G86)).
5. **The plain layer must not create obligations.** ISO/IEC Directives Part 2 states that notes and
   examples "shall not contain requirements"; this repository's template already applies that rule to
   informative sections (`## Normative Status`). *Unverified against the live ISO text* — the page
   blocked retrieval; the rule is consistent with the template's existing citation and with W3C's
   separation of supplemental content.

## What the evidence does **not** support

6. **A readability score is not a comprehension measure.** AHRQ warns that formulas "do not measure
   comprehension or reading ease" and that different formulas score the same text years apart
   ([AHRQ](https://www.ahrq.gov/talkingquality/resources/writing/tip6.html)); Schriver's review is
   summarised as finding the formulas unreliable measures of text quality, recommending usability
   testing instead ([Center for Plain Language](https://centerforplainlanguage.org/most-readability-formulas-outdated-and-overrated/)),
   and AHRQ cites Redish's critique ([PDF](https://redish.net/wp-content/uploads/Redish_on_Readability_Formulas.pdf)).
   **Consequence: no Flesch or grade-level gate.** A word-count cap may be used as a brevity *proxy*,
   and must be labelled one.
7. **Adding a summary does not automatically improve comprehension.** A systematic review found 90
   relevant papers, 33 empirical, too heterogeneous to meta-analyse, with evidence "scarce for many
   common PLS-writing recommendations" ([Stoll et al., 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9170105/)).
   The two large randomised studies that do show effects test *how* a summary is written: in samples
   of N=2,288 and N=2,211, explaining or replacing content-specific technical terms mattered
   ([Kerwer et al., 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8717946/)). **Consequence: the
   claim is bounded.** The rule may claim it lowers the cost of first contact and removes undefined
   terms; it may not claim measured comprehension gains.
8. **No source mandates a two-column plain/technical table.** The pattern is our design, built from
   the summary-plus-detail split IEEE 830's outline uses and from G86's "in addition to the original".
   Said plainly so the design is not mistaken for a standard.

## What duplication costs, and the mitigation

9. Duplicated prose drifts. No empirical rate was found — treat it as a credible risk, not a
   measurement. The mitigations that exist are single-sourcing (DITA content references) and
   linking a summary to its authoritative clause rather than copying it
   ([DITA](https://dita-lang.org/)). **Consequence: the plain column may not restate a requirement;
   it points at the id, and the check fails when the id set changes without the table** — the
   stale-entry mechanism `decisions/0005` already uses for conformance baselines.

## What the peer set has

10. **citekit carries the same gap.** Its one spec scores 25/27 on section conformance and contains
    no plain-language layer at all, so the readability problem is not a defect of this kit's
    authoring — it is what the whole peer set does. It is a usable negative control for the new
    check: a correct, conformant spec that the check should reject on this rule alone.

## Design that follows

| Decision | Evidence | What it rules out |
| --- | --- | --- |
| A required `## In Plain Terms` section per spec: one short paragraph, an id-keyed plain/technical table, and a terms table | 1, 2, 4, 8 | a prose preamble nobody maintains; a summary that floats free of the requirements |
| Plain cells are informative: no `SHALL`/`MUST`, no copied requirement text, id references only | 5, 9 | a second normative voice that can contradict the first |
| Jargon is glossed in parentheses on first use, and long explanations go in a sentence | 2, 3 | a bracket holding a clause; unexplained acronyms |
| The plain layer is checked for **coverage and staleness**, not for quality | 6, 9 | a readability score as a gate; a table that rots silently |
| The policy also binds conversation output, not only artifacts | 1, 2 | a rule that fixes the documents and leaves the chat unreadable |

## Limits of this pass

- Two ISO quotes (Part 2 notes/examples; 29148 definitions) could not be verified against the live
  text; both are used only where the repository already relied on them.
- No A/B measurement was run on this kit's own specs with real newcomers. The success criteria are
  therefore structural (coverage, gloss presence, length) plus a named manual check, not a
  comprehension effect size.
- The peer sweep covered nine repositories already cloned for the earlier audit, not the ecosystem.
