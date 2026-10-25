# 0009 — The plain-language rule binds the conversation; the artifact layer is offered, not demanded

## Context

Decisions `0007` and `0008` made an informative `## In Plain Terms` section **required** on every
specification and every plan, and added a checker that fails a document without one. Both features were
built and their retrofits written.

The owner then supplied the fact the first design had wrong:

> "I don't need plain language in the plan documents, just in the chat, because the documents are AI
> facing first."

That premise is checkable in this repository and it holds. The artifacts are read by an agent before a
person: `AGENTS.md` opens by telling the agent to check the workflow first, the commands route through
the skill, and the plans exist to be implemented from. A human reads them second, when reviewing or when
returning months later. `0007`'s research was about human comprehension and still describes *how* to
write plainly; it does not establish that every document must carry a second, human-facing layer.

## Decision

**1. The obligation moves to the conversation.** The reply is the artifact a person actually reads at
the moment of work, and it is where the rule binds: lead with the outcome in ordinary words, gloss a
specialist term in short brackets at first use, and give any table that summarises technical work a
column saying what each row means. This is unchanged from `0007` §5 and `0008` FR-011 — it is the half
that survives, and it is now the whole of the obligation.

**2. The artifact layer becomes optional and stays checked.** A spec or plan MAY carry
`## In Plain Terms`. Where it does, every rule in `0007`/`0008` still applies — identifiers covered once,
no normative keyword in an explanation, a plan row naming a section or a file — because a table nobody
validates rots into a promise the document no longer keeps. Where it does not, nothing is missing.

**3. The checker enforces conformance, not presence.** `scripts/check-plain-terms.py` passes a document
that declines the layer and says so (`no plain layer (optional; --require-section to demand one)`).
`--require-section` restores the old behaviour for a project that wants the layer everywhere; it lives
in the caller's verify manifest, not in the kit's default. The two fixtures whose only defect is the
absent section, and both peer controls, are now run in both directions — absence passes, and the flag
still rejects it — so "optional" cannot decay into "the check stopped running".

**4. Nothing written is deleted.** The seven specs and seven plans that carry the section keep it. They
are accepted or drafted content, and `0005` refuses to retro-fit accepted documents in either
direction; deleting an informative layer to make a rule simpler would be that retro-fit. The change is
to what future documents owe, not to what past documents say.

## Consequences

- `specs/007`/`008` are narrowed in place: FR-001 changes from MUST-contain to MAY-contain, the
  enforcement requirements gain the tolerance clause, and US4/FR-012 (the conversation half) becomes the
  priority rather than the afterthought. Both remain `Draft`, so amending them is legitimate rather than
  the retro-fit `0005` refuses.
- The `Technical` rule for plan rows and the artefact pointer survive, and they were the two mechanisms
  that helped an agent: a row that points at the design stops an agent from "improving" a deliberate
  compromise, because the reason and the location sit beside the choice.
- An adopter that wants the layer can demand it in one flag. That is a better default than the reverse:
  a demand baked into the template forces every project to maintain a table it did not ask for, and the
  failure mode — a stale table that reads as documentation — is worse than its absence.
- The kit's own evidence and the six retrofits remain as the worked example, not as an obligation.
- `0007`'s coverage checker, gloss rule and brevity cap are untouched. Only the trigger changed.

## Rejected alternatives

- **Delete the sections from the retrofitted documents.** Reverses `0005`, destroys the glossary content
  that keeps two different meanings of "ledger" apart, and removes the only worked example of the shape.
- **Keep the requirement and stop checking it.** A demanded section nothing verifies is the ritual
  `0007` was written to prevent; the honest version of "we no longer need this" is to stop demanding it,
  not to stop looking.
- **Make the checker optional by removing it.** Then a document that carries a stale table has no way to
  find out, which is the failure mode a coverage check exists for.
- **Move the plain sections into a separate document.** A summary that lives elsewhere is a second source
  of truth with no mechanism keeping it in step; the section sits inside the text it explains or not at
  all.
