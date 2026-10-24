---

<!--
  Appended by the spec-driven-development preset (strategy: append).
  The core sections above (Summary, Technical Context, Constitution Check, Project
  Structure, Complexity Tracking) remain authoritative. These sections carry the
  design-phase reasoning the core template does not ask for.
-->

## In Plain Terms

**This section is required, and it is informative.** It exists so a reader who did not write the plan
can tell what will be built before meeting the design vocabulary — the components, the mechanisms,
the trade-offs, and the identifiers carried over from the spec. It is not a second design: where it
and the plan's technical sections disagree, the plan wins, and the disagreement is a defect in the
explanation.

**Place it before `## Technical Context`** — where that heading is absent, before every top-level
section other than `## Summary`. A reader who needs the explanation should not have to pass the
design to find it. This follows the established shape of a design document: a guide-level explanation
before the reference-level detail (the Rust RFC template does exactly this, and Google's design docs
open with a succinct context section that links detail instead of copying it).

Three parts, in this order:

1. **A paragraph of at least three sentences**, before any table, saying what will be built, out of
   what already exists, and why this shape rather than the obvious alternative.
2. **The table.** One row per explanation, with exactly these columns:

   | Item | In plain words | Technical |
   | --- | --- | --- |
   | FR-001–FR-003 | What was chosen for these requirements, and what it buys. | `scripts/check-plain-terms.py`; §Architecture Overview |

   `Item` holds identifiers — `FR-007`, `SC-002` — comma-separated or as a closed range
   (`FR-001–FR-006`). Rows may group, but **every** `FR` and `SC` identifier the plan mentions must
   appear in exactly one row. `Technical` must name **where the design lives**: a section reference
   (`§Architecture Overview`) or a backticked artefact (`bin/speckit-verify`). Identifiers alone do
   not satisfy it.
3. **The terms table.** The plan's own mechanism words, each with the plain words that explain it.

   | Term | Plain words |
   | --- | --- |
   | ledger | a file that records what was done, one line per item, so a later reader can check it |

**Rules that the check enforces, and why each exists:**

- **A row states the design choice and its reason — never a restatement of the requirement.** The
  spec already explains what is owed, and its row is the place for that. The evidence says the format
  of a design document does not measurably change understanding, while the presence of design
  decisions and their rationale does (Ernst & Robillard 2023, N=65; Shahin et al. 2014 as reported by
  Rukmono et al. 2025 — `docs/research/plans-plain-language-2026-10.md` §3). A row that repeats
  `FR-004` has copied the one thing the evidence says is not the difficulty. This rule is **review**,
  not a check: the script cannot tell a decision from a paraphrase.
- **`Technical` must name a section or a file.** An identifier-only cell sends the reader back to the
  spec and says nothing about how the thing is built. This is the one rule that differs from a spec's
  table, and it is checked.
- **No `SHALL`, `MUST` or `SHOULD` in an `In plain words` cell.** The plain layer explains; it must
  not command. Two normative voices eventually disagree, and the reader cannot tell which binds.
- **At most 45 words per cell.** A brevity **proxy**, not a readability score. A long cell is a sign
  the row covers something that deserves its own row.
- **A bracketed gloss at first prose use.** Every term in the terms table must be followed by `(...)`
  the first time it appears in a sentence at or after this section, and the bracket holds **at most 25
  words**. Table lines do not count, so listing a term is not introducing it; the metadata above this
  section is status, not reading. Google warns that readers skip parenthetical text, so a bracket is
  for a term, never for a clause.
- **Properties are not covered.** A `P-00x` property already carries its `for any …` statement and
  check method in `## Correctness Properties`, so covering it here would duplicate the explanation the
  plan already gives. This is a decision, not an omission.
- **Nothing is exempt for being obvious.** A short plan needs a short row, not no row.

**What the check cannot do, stated so nobody trusts it further than it goes:** it verifies that the
section exists and is early, that the paragraph is long enough, that every identifier is covered once,
that each row names a section or a file, that no cell commands, and that the listed terms are glossed.
It cannot tell whether a row states the real reason, and it cannot tell whether a reader understood it.
The design of this layer is ours; no standard mandates a two-column table, and the research record
says so rather than borrowing authority for it.

**The same habit applies to what the agent says.** A reply about a design leads with the outcome in
ordinary words, glosses a design term the first time it uses it, and puts a plain column beside any
table that summarises the design.

## Carried Forward

### Confirmed Decisions

- [Settled in the spec or by the user]

### Constraints

- [Technical or operational constraint]

### Assumptions

- [Assumption this design depends on]

### Risks

- [Risk introduced or inherited]

### Open Questions

- [Unresolved item that affects the design]

## Scope Confirmation

### In Scope

- [What this change delivers]

### Out of Scope

- [What it deliberately does not touch]

### Requirements Affected

- [FR-00x addressed / deliberately not addressed]

## Repository Findings

Filled in from inspecting the code, **before** proposing changes. A plan written without
this section is not trustworthy.

**Sweep before you list.** A new block, field, entity, or enum member almost always appears
in more than one place. Search the repository for every occurrence of the concept — not just
the obvious component. Check at least:

- the schema or definition
- **any layer that enumerates the same set** — a validation schema (Zod, JSON Schema), a type
  union, a literal enum, a registry, a route table
- the component / handler
- the renderer or dispatch site
- existing tests and fixtures

A file that re-lists the same set (for example a `_template` enum mirroring the list of block
types) MUST be updated too, or the build fails on the new value — and it will fail *late*,
at implementation or typecheck. Enumerate those files here explicitly.

### Relevant Components

- [Files, modules, services]

### Existing Behavior

- [What happens today]

### Existing Tests

- [What already covers this area, and what does not]

### Project Conventions

- [Patterns this change must follow]

### Constraints Discovered

- [Constraint found in the code that the spec did not mention]

## Architecture Overview

[The shape of the solution, in a paragraph or a small diagram. Prefer existing patterns.]

## Major Components

- [Component and its responsibility]

## Data Flow

[How data moves through the change: input, transformation, storage, output.]

## Interfaces and Contracts

- [Function signature, API route, schema, event — anything a caller depends on]

## Dependencies

- [New dependency, and why it is justified. Prefer none.]

## Error Handling

[What can fail, how it surfaces, and what the user sees.]

## Security and Privacy

[Only if relevant. Otherwise state "Not applicable" and why.]

## Performance and Reliability

[Only if relevant. Otherwise state "Not applicable" and why. Note any known limits.]

## Validation Strategy

[How the design will be verified once implemented — tests, checks, and manual steps.]

## Correctness Properties

A **correctness property** is a universally-quantified statement about how the system must
behave — an invariant or contract that holds regardless of the specific data. Example-based tests
check the examples you thought of; a property is checked against many generated inputs, so it
finds the cases you did not.

The distinction from a functional requirement is *quantification*, not importance. `FR-001` says
"when the user submits X, the system returns Y" — one example, pass or fail. A property says "for
any input in domain D, P holds" — an oracle that judges many runs. The lineage is Hoare triples,
Liskov & Guttag invariants, and Meyer's design-by-contract (`require` / `ensure` / `invariant`).

Not every requirement maps cleanly to a property. Map what you can, and **opt out explicitly** for
the rest — a vacuous property is worse than a recorded opt-out.

| Property ID | Requirement | Spec rule | Scope | `for any …` statement | Falsification | Check method | Non-mapped reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P-001 | FR-001 | the spec sentence this encodes | operation / type / system | `for any <domain>, <property that must hold>` | a command or input that must make it fail | property-test | — |
| — | FR-002 | — | — | — | — | — | qualitative / no decidable oracle |

**Spec rule** — the sentence in `spec.md` the property encodes, quoted or cited. A property that
cannot name its rule is a generic test with a generator attached.

**Falsification** — a command (or a recorded input) that makes the property fail *before* it is
trusted. A property that passes but cannot fail is not evidence, and the demonstration is executed,
not described: `bin/speckit-verify` runs `falsify` first and refuses to count the check as evidence
when it passes. Both fields become `spec_rule` and `falsify` on the check in `.specify/verify.json`
for `kind: property`.

**Scope** — what the property ranges over. `operation` (holds for one call — a Hoare triple),
`type` (holds for every instance — a class invariant), or `system` (holds across components or over
a sequence of states, e.g. "no two replicas disagree"). An unscoped invariant is unverifiable: you
cannot check a claim without knowing what it claims about.

**Check method** — how the property is actually enforced. One of:

| Method | Use when |
| --- | --- |
| `runtime-assert` | cheap to check on every execution (pre/post-conditions, class invariants) |
| `property-test` | a generator can produce the input domain (round-trip, idempotence, invariant-preservation) |
| `model-check` | the risk is a concurrency or protocol bug worth exploring exhaustively (TLA+) |
| `review-only` | no executable check is practical — **state why**, and accept it is weaker |

A property with no check method is not a property; it is a wish. Non-executable prose is acceptable
only under `review-only`, and only with the reason recorded.

### Rules

- **Start every property with `for any`.** A statement naming specific values is an example, not
  a property. `for any request carrying an expired token, the response is 401` is a property;
  `request #5 returns 401` is a test case.
- **Name the check method.** A property you cannot check is a wish — see the table above. `review-only`
  is a legitimate answer, but it must be chosen, not fallen into.
- **Most properties are one of five shapes.** Reach for these first; they are well understood and
  each has a standard way to generate inputs:

  | Shape | Statement | Example |
  | --- | --- | --- |
  | Round-trip | `decode(encode(x)) == x` | `for any event, parsing its serialised form yields the same event` |
  | Idempotence | `f(f(x)) == f(x)` | `for any deck, validating it twice reports the same result` |
  | Invariant-preservation | after any operation, I still holds | `for any review outcome, the log stays append-only` |
  | Commutativity | `f(g(x)) == g(f(x))` | `for any two independent edits, order does not change the result` |
  | Model-equivalence | impl(x) matches a simple reference | `for any schedule, the optimised scheduler agrees with the naive one` |

- **One requirement may yield several properties** (1:many) — split by input domain, not by
  convenience. Two properties about one requirement are fine; one property pretending to cover
  two is not.
- **The statement needs a decidable oracle.** If you cannot say how a run would be judged pass or
  fail, it is not a property. Requirements that are qualitative, or that depend on
  non-deterministic or external behaviour with no observable contract, opt out.
- **Opt-out rule:** a non-mapped requirement gets **no P-ID**, and its reason goes in one line in
  the `Non-mapped reason` column. Never both a property and an opt-out, and never neither — every
  requirement is either mapped or explicitly opted out. A requirement that is neither is a gap in
  this plan.

### Framework decision

Property-based testing needs a framework. **Detect one; never assume one.** Record the decision
here so `tasks.md` follows it verbatim instead of guessing.

- **Detected** — framework name, or `none found`
- **Version / where found** — the dependency entry, test config, or existing property test
- **Signal** — what in the repository indicated it
- **Decision** — `adopt` the detected framework, or `fallback` to example-based tests

Per-ecosystem signals to look for — a *detection checklist*, not a default. Do not add a
dependency merely because it appears here.

| Ecosystem | Look for |
| --- | --- |
| Python | `hypothesis` in dependencies, or existing `@given` tests |
| JavaScript / TypeScript | `fast-check` (`fc.assert` / `fc.property`) |
| JVM | `jqwik`, `junit-quickcheck`, `scalacheck` |
| Rust | `proptest`, `quickcheck` |
| Haskell | `QuickCheck` |
| Erlang / Elixir | `PropEr`, `StreamData` |

If **no framework is found**, decide explicitly between adopting one and falling back to
example-based tests, and record which. `tasks.md` follows this decision verbatim.

### Traceability

Each property links a requirement to the test that checks it: `FR-xxx → P-xxx → T0xx`. A property
with no task is unbuilt; a property test with no requirement is scope creep — the same symmetry
that applies between requirements and tasks.

### Independence

This is template text, so it applies when the command runs — whether or not the
`spec-driven-development` skill loaded. Under the `lean` preset, which replaces the commands and
bypasses templates entirely, it does not apply: choose `lean` or this preset, not both.

## Alternatives Considered

| Option | Advantages | Disadvantages | Decision |
| --- | --- | --- | --- |
| [Alternative] | | | Rejected / Selected |

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |

## Requirement-to-Design Traceability

Every design decision should serve a requirement. Every requirement should have a design.

| Requirement | Design Decision | Reason |
| --- | --- | --- |
| FR-001 | | |

## Implementation Boundaries

### Must Change

- [Required for correctness]

### Must Not Change

- [Explicitly out of bounds — behaviour, contract, or file that must survive untouched]

## What Changed / What Remains Open

- **Changed from the spec:** —
- **Still open:** —
- **Needs approval:** —
