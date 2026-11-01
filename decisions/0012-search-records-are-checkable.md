# 0012 — A null search is recorded in a checkable shape, and the shape is checked

## Context

`decisions/0011` ended with a negative result written down by hand: `docs/research/verification-tooling-2026-10.md`
§13 recorded what the scholarly lane was asked, which words were used, on which day, and what came back. The
reasoning there was sound and the record was a one-off. Nothing required the next null to look like it, and the
fields were chosen while writing rather than declared before.

The failure mode is cheap and invisible: a note says "the literature had nothing to say", a decision cites it,
and the next reader cannot tell that sentence from one written by an author who never opened a browser. §13's
own opening names the problem — a negative that is not written down is indistinguishable from a search nobody
ran — but a *shape* that lives in one section is not a rule.

## Research

`docs/research/search-record-2026-10-31.md` carries the four rounds, the sources and the queries. What settled
the fields:

- **PRISMA-S** (Rethlefsen et al. 2021, `doi:10.1186/s13643-020-01542-z`, read at PMC8270366) asks for the
  sources and the *date last searched* (item 7), the full strategy "such that it could be repeated" (item 8),
  and the numbers with reasons for exclusions (item 17). Those are the four facts, named by a reporting
  standard rather than invented here.
- **The 2023 cross-sectional metaresearch study** (`doi:10.1016/j.jclinepi.2023.111229`) is the empirical case
  for bothering: search strategies are "poorly reported and not reproducible" at scale, so the default is that
  a null arrives unverifiable.
- **The negative-results literature** (publication bias) explains *why* nulls matter but adds no field; it is
  about publishing results, not about documenting searches. Recorded as such rather than stretched.
- **Docs-as-code linters** (Vale, markdownlint) enforce mechanics and style. None of them asks whether a record
  contains its own evidence, which is the gap this check fills; the kit's `check-plain-terms.py` is the closer
  precedent, because it validates a section's coverage rather than its prose.
- **Software-engineering review guidance** (Kitchenham; Wohlin 2020, *Information and Software Technology*)
  uses the same four facts in different words — "search string", "databases", "date of search" — and added
  nothing to the list.

The fourth round produced no finding that could change a field, which is the stopping rule declared before
round 1 (`decisions/0002`). Research closed there.

**CiteKit was not available** in this environment: `bin/speckit-mcp` prints `skip CiteKit not found`, and no
`CITEKIT_HOME` is set. Its widest source, OpenAlex, was queried directly, and the limitation is stated in the
note rather than papered over with a claim that a CiteKit run happened.

## Decision

**1. The record has four facts and one shape.** A research note that reports a null carries a section headed
`## Search record` (level 2-4; an optional leading number is allowed, because this repository numbers its
sections). Inside it, one table, one row per search actually run:

| Column | Why it is required | Source |
| --- | --- | --- |
| `Source` | "the literature" is not a place; a reader has to know which corpus was searched | PRISMA-S item 7 |
| `Date` (`YYYY-MM-DD`) | a search is a point in time; an undated null is re-run forever | PRISMA-S item 7 |
| `Query` | the words are what makes the null repeatable — and what shows it was a poor query | PRISMA-S item 8 |
| `Hits` or `What came back` | "nothing" is a result and must be said; a blank cell hides whether anybody looked | PRISMA-S item 17 |

Extra columns are allowed and encouraged — a question column, a verdict column. The check is on the four facts,
not on the table's width.

**2. `scripts/check-search-record.py` enforces the shape.** It also requires one sentence of prose in the
section (a table with no statement of what was asked is a spreadsheet), and it rejects a section with a header
and no rows: a record that examined nothing is not a record, which is the same rule feature 005 applies to the
gate.

**3. It is optional by default, with `--require-section` to demand it.** Most research notes contain no null,
and forcing a section onto them teaches authors to add a row for a search they did not run. This mirrors
`decisions/0009`'s opt-in shape rather than inventing a second convention.

**4. It ships the way the other checkers ship.** `bin/speckit-init` copies it into `.specify/scripts/`, the gate
asserts the source and the installed copy match, and `scripts/self-gate.sh` §3g runs it over `docs/research/`
and over six fixtures, so the failure shapes are exercised on every gate run rather than trusted.

**5. §13 is retro-fitted, not left as an exception.** The existing table gained `Source` and `Date` columns and
the heading. An example that predates the rule and does not satisfy it is an argument against the rule.

**6. The record lives in the note; the decision cites it.** A second copy in the decision would drift.

## Consequences

- A reader can re-run any recorded null and get their own answer, which is the only test of a negative that
  exists.
- A note with a null and no record now fails the gate's research-note scan, so the omission is visible in the
  same run that reports everything else.
- Writing a null costs one table row. Writing a *dishonest* one costs the same, and this check cannot tell the
  difference — see below.
- Six fixtures and a corpus run are added to the gate, which is the cost of making a prose rule executable.

## Rejected alternatives

- **Leave it as prose in §13.** That is exactly the state being repaired: one hand-written example, no rule, and
  the next author free to write "nothing found" with no dates.
- **Require the section in every research note.** It would fail notes that report no null at all, and the
  cheapest way to pass would be a fabricated row — a check that manufactures the dishonesty it exists to catch.
- **All 16 PRISMA-S items.** PRISMA-S describes a review protocol; a development note needs the facts that let a
  reader repeat a search, not the facts that let a reviewer appraise a review. Using four of sixteen is a choice
  stated here, not an oversight.
- **Record searches in the JSONL ledger.** The ledger answers "did the checks run", and it is machine-written by
  the engine. A search record answers "why does this note claim the literature is silent", and it has to sit
  where the claim is read. Two stores for one subject would also mean two places to forget.
- **Scrape the search tool automatically.** There is no stable interface to scrape here — the web searches are
  prose results — and CiteKit, which would have one, was absent. A field a human fills in is honest about being
  written by a human.

## What this does not claim

- It does not make a null true, or even likely. A fabricated row passes; a real row in the wrong corpus passes.
  It makes the record checkable, which is all a checker can do.
- It does not say a null from a corpus outside software engineering is evidence about software engineering. §13
  already states that limit, and this decision inherits it.
- The date is the date of the search, not the publication date of what came back. Nothing here checks that the
  hits described are the hits that were returned.
- It does not cover searches recorded inside the reply rather than a note. The conversation is not a durable
  artifact, so a claim resting only on it is still §13's original problem.
