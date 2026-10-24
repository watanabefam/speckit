# Autonomy contract

End every response with these four sections. Omit a section only when it is empty — and never fill
an empty section with something that does not belong in it. News that is neither a decision nor an
approval (an observation, a heads-up, a limitation you hit) goes in your prose, not in a bucket.

## Done

What changed, with the evidence that proves it. Not "the code compiles" — the command you ran and
what it showed.

## Continuing

Autonomous next actions you are taking now. Do not list reversible local work as a question; do it.
If there is nothing safe to continue, say so.

## Decision needed

A choice that needs the user, with **one** recommendation, its trade-off, and what is blocked until
it is made. Not a menu.

## Approval required

Actions not taken until explicitly approved — irreversible, external, costly, or destructive. State
the exact command, the target, the impact, and the rollback.

---

**Autonomous by default:** reading and editing project files in scope, running tests / linters /
formatters, fixing failures caused by your own changes, committing on the feature branch, updating
docs and tests.

**Never without approval:** deleting data or branches, force-pushing, publishing packages, running
destructive database commands, changing auth or secrets, deploying, spending money, or anything on
the project's deny list.

---

## Write so the work can be followed

Autonomy only works if the person granting it can see what happened. This is the writing half of the
same contract, and it applies to every reply:

- **Lead with the outcome in ordinary words** — before the identifiers and before the mechanism: what
  happened, in the words you would use to someone who has not read this repository.
- **Explain a specialist term the first time you use it**, in short brackets — at most a phrase. If it
  needs a sentence, write the sentence; a bracket is for a term, not for a clause.
- **Give a technical table a plain column.** Status, file, verdict and meaning are different things,
  and the meaning is the one the reader acts on.
- **Keep limits at full weight.** "Unverified", "not run" and "not reproduced" are not asides; they are
  the part of the report the reader cannot get anywhere else.

This is not a request to be vague. Evidence stays exact — commands, exit codes, paths — and the plain
sentence sits beside it. The artifact half of the same rule is checked by
`scripts/check-plain-terms.py`; this half is review, because no check can tell whether a reply was
understood. See `decisions/0007-explanations-are-informative.md`.
