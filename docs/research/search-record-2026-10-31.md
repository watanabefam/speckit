# Recording a search that found nothing

**Date:** 2026-10-31 · **Settles:** `decisions/0012-search-records-are-checkable.md` and
`scripts/check-search-record.py`.
**Question:** If a lane returns nothing, what must the note contain so the next reader can trust the null —
and can that shape be checked, rather than trusted?

**Method.** Four rounds, with the stopping rule declared before round 1 (`decisions/0002`): stop when a full
round adds no finding that could change a required field or the rule text; a source that only confirms a
settled field does not count as progress.

| Round | Question | Result |
| --- | --- | --- |
| 1 | What do reporting standards require of a search record? | **Changed the design** — the fields are source, date last searched, the query itself, and what came back (PRISMA-S items 7, 8, 17). A null without the words used cannot be repeated. |
| 2 | Does the negative-results literature add anything? | **Added no field, and changed the framing** — publication-bias work explains why nulls matter, and is about *publishing results*, not about documenting searches. Recorded as adjacent rather than as support for the fields. |
| 3 | Is enforcing a record's shape by a checker established practice? | **Added no field** — docs-as-code linters (Vale, markdownlint) check mechanics and style, and none asks whether a record contains its own evidence. This kit's `check-plain-terms.py` is the closer precedent: it validates coverage of a section rather than its prose. |
| 4 | Does software-engineering review guidance name different fields? | **Empty** — Kitchenham's guidelines and Wohlin 2020 use the same four facts under different names ("search string", "databases", "date of search"). Research closed here. |

**Status of the scholarly lane, corrected after first publication.** The first draft of this note said CiteKit
was absent, because `bin/speckit-mcp` prints `skip CiteKit not found — nothing to register` and `CITEKIT_HOME` is
unset. That inference was wrong: registration is one way in, not the only way. A checkout of
`watanabefam/citekit` sits in this repo's `.scratch/peers/`, its headless CLI (`node tools/search.mjs`, driving the
same adapters the browser app runs) needs no key for six of its nine sources, and it ran here on **2026-10-31** at
commit **`39bd120`** — in a detached worktree, so the pinned `46feeb2` copy stays as cited elsewhere.

The mistake is worth keeping visible, because CiteKit's own skill names it: `skills/evidence-search/SKILL.md`
tells an agent *"Do not report 'CiteKit needs a browser, so an agent cannot use it' without opening `tools/`"* and
lists that claim in its rationalization table as something an agent has actually done. This note's first draft is
an instance of it. What caught it was the user naming the checkout path, not the note's own method.

Rows 1–4 below are the searches as originally run (OpenAlex directly, and the host web tool). Rows 5–7 re-ran the
same questions through CiteKit afterwards. They changed the lane's status and added no field, so the stopping rule
in `decisions/0002` still closes at round 4: a correction to provenance is not a research finding.

## What settled the fields

### PRISMA-S names the four facts

Rethlefsen et al. 2021, *PRISMA-S: an extension to the PRISMA Statement for Reporting Literature Searches in
Systematic Reviews*, `doi:10.1186/s13643-020-01542-z`, read at PMC8270366 on 2026-10-31:

- **Item 7** asks for all information sources, and the **date each was last searched**.
- **Item 8** asks for the full search strategy "such that it could be repeated".
- **Item 17** asks for the numbers screened, with reasons for exclusions.

Those three items are why the required columns are `Source`, `Date`, `Query` and `Hits` / `What came back`, and
why the table is required rather than the prose — a sentence can gesture at these four facts without stating
any of them.

### The metaresearch says the default is a useless null

*Systematic review search strategies are poorly reported and not reproducible: a cross-sectional metaresearch
study* (`doi:10.1016/j.jclinepi.2023.111229`, J Clin Epidemiol 2023; title, year and DOI read from OpenAlex on
2026-10-31, the paper itself not fetched) found search strategies poorly reported and not reproducible at
scale. That is the empirical case for writing source, date, query and result rather than the conclusion alone:
if the well-resourced literature cannot reproduce its own searches, an unreported search is worth roughly
nothing.

### The negative-results literature is adjacent, not load-bearing

OpenAlex surfaced publication-bias studies — *Dealing with the positive publication bias: Why you should really
publish your negative results* (2017), *Publication bias — Importance of studies with negative results!* (2019),
*Publication Bias: The Elephant in the Review* (2016). They argue that unpublished nulls distort a field. They
do not name a field a search record must carry, and this note does not use them as if they did: the reason to
record a null here is that a claim rests on it, not that science has a filing problem.

### Checking a document's shape is normal; checking its evidence is not

Round 3 looked for prior art in documentation tooling. The answer was uniform: Vale and markdownlint enforce
style, heading order and formatting (`Docs Linting Guide`, Fern, 2026-01-17; markdownlint's rule list). A
search that returns ten results describing docs-as-code linting and none describing a check on whether a record
states its own evidence is the gap this checker occupies. That is a *narrow* claim: it says no reviewed tool
does this, not that nobody has ever written such a check.

## The decision this note supports

`decisions/0012` fixes four required columns, one required sentence of prose, at least one row, and a checker
that is optional by default with `--require-section` to demand the section everywhere. §13 of
`verification-tooling-2026-10.md` was retro-fitted to the same shape, because an example that predates the rule
and does not satisfy it argues against the rule.

## Search record

The searches below are the ones this note's own nulls rest on. A row that says "nothing" is a result and is
recorded as one.

| # | Question asked | Source | Date | Query | Hits | What came back |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Does the negative-results literature add a field beyond source, date, query and result? | OpenAlex works API | 2026-10-31 | `negative results reporting guidelines publication bias` | 685 288 | publication-bias studies about *publishing* nulls (2010, 2016, 2017, 2019); **no field for recording a search** |
| 2 | Does information-retrieval work document searches differently? | OpenAlex works API | 2026-10-31 | `documenting search strategies reproducibility information retrieval` | 73 053 | *Errors in search strategies used in systematic reviews and their effects on information retrieval* (2019), plus IR benchmarks from 1965–2019; confirms the failure mode, adds no field |
| 3 | Is a required-shape document check established in documentation tooling? | Google, via the search tool | 2026-10-31 | `Vale markdownlint documentation linting CI required sections docs-as-code enforce structure` | 10 results | docs-linting guides and markdownlint's rule list; all mechanics and style, **none about a record's evidence**, which is the gap claimed above |
| 4 | Does software-engineering review guidance name different fields? | Google, via the search tool | 2026-10-31 | `Wohlin 2020 guidelines search strategy update systematic literature reviews software engineering report search strings databases dates` | 10 results | Wohlin 2020 (IST) and Kitchenham's guidelines: "search string", "databases", "date of search" — the same four facts, no extra field |
| 5 | Does the negative-results literature add a field? (re-run through CiteKit, not OpenAlex alone) | CiteKit `39bd120` — openalex, crossref, epmc, pubmed, eric, doaj | 2026-10-31 | `negative results reporting guidelines publication bias` | 30 records, 28 distinct DOIs | the same publication-bias papers as row 1. The lane also screened its 28 DOIs and reported 1 retraction on record and 1 record carrying PubPeer comments (flagged as criticised, not retracted) — **still no field for recording a search** |
| 6 | Is there guidance that names more than the four fields? | CiteKit `39bd120` — six sources | 2026-10-31 | `documenting search strategies reproducibility information retrieval` | 28 records, 23 distinct DOIs | *Errors in search strategies used in systematic reviews and their effects on information retrieval* (2019, `doi:10.5195/jmla.2019.567`); *Searching for studies: a guide to information retrieval for Campbell systematic reviews* (2017, `doi:10.4073/cmg.2016.1`); *Reproducible study identification and selection in systematic reviews* (2026, `doi:10.1136/bmjopen-2026-123460`). The Campbell guide is the one result that **could** hold a fifth field; its text was not fetched, so this row claims no fifth field **appeared in the results**, not that the guide contains none |
| 7 | Does the standards lane confirm the four facts through CiteKit? | CiteKit `39bd120` — six sources | 2026-10-31 | `reporting search strategy checklist peer review reproducibility` | 23 records, 22 distinct DOIs | PRISMA-S (2021) ranked first, with *Analysis of the reporting of search strategies in Cochrane systematic reviews* (2009); **confirms the four facts, adds nothing** |

OpenAlex counts are full-text match counts, not counts of relevant records. 685 288 is the size of a haystack;
it is not "685 288 studies show".

## What this does not claim

- A record is not evidence of absence. A null from a corpus outside software engineering is weak evidence about
  software engineering: it says the question was not asked *there*.
- The checker cannot tell a real record from a fabricated one. A row with a plausible source, date, query and
  result passes whether or not anybody ran it. What it enforces is that the four facts a reader needs exist and
  are well-formed.
- The `Date` column is the date of the search, not the publication date of a hit. Nothing here compares the
  described hits with the ones actually returned.
- The absence of prior art in round 3 is a null from one search over web results, not a survey of the tooling
  field. It is recorded in the shape it argues for, which is the only honest way to close a note about recording
  nulls.
- **The CiteKit rows are a peer checkout, not the author's working copy.** They ran at `39bd120` from a clone in
  `.scratch/`, on Node 26, with `--no-enrich` and `--per 5`; another revision may rank, dedupe or screen
  differently. The four facts do not depend on the ranking, which is why the correction changes the lane's status
  and not the decision.
- **The retraction and PubPeer counts are the tool's, not this note's.** Row 5 reports them because the lane
  printed them; nobody here checked the retraction record against a register.

## Sources added by this note

- Rethlefsen et al. 2021, PRISMA-S — `doi:10.1186/s13643-020-01542-z`; items 7, 8 and 17 read at PMC8270366,
  2026-10-31
- *Systematic review search strategies are poorly reported and not reproducible: a cross-sectional metaresearch
  study* — `doi:10.1016/j.jclinepi.2023.111229` (metadata via OpenAlex, 2026-10-31; paper not fetched)
- *Dealing with the positive publication bias: Why you should really publish your negative results* (2017) —
  OpenAlex record, title and year only
- *Publication bias — Importance of studies with negative results!* (2019) — OpenAlex record, title and year only
- *Publication Bias: The Elephant in the Review* (2016) — OpenAlex record, title and year only
- Wohlin 2020, *Guidelines for the search strategy to update systematic literature reviews in software
  engineering*, Information and Software Technology — `doi:10.1016/j.infsof.2020.106366` (web result, 2026-10-31;
  abstract metadata only)
- Fern, *Docs Linting Guide* (2026-01-17); markdownlint `doc/Rules.md` — web results, read as descriptions of the
  tools' scope, 2026-10-31
- `watanabefam/citekit` `39bd120` (2026-10-29) — `tools/search.mjs` and `skills/evidence-search/SKILL.md` read in
  the peer checkout, 2026-10-31; the four-field findings re-derived through its six keyless sources
- Kugley et al. 2017, *Searching for studies: a guide to information retrieval for Campbell systematic reviews* —
  `doi:10.4073/cmg.2016.1` (metadata via CiteKit, 2026-10-31; text not fetched)
