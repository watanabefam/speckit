# Implementation Plan: Review and Stress-Test Gate

**Feature Branch**: `002-review-and-stress-gate` · **Date**: 2026-10-16 · **Spec**: `spec.md`

## In Plain Terms

This plan adds two rules to the converge step — a review by someone who did not do the work, and a
stress test (an attempt to make the change fail using the case it is meant to reject) — instead of a new
step or a new artifact. Both ship as a prepend (instructions placed ahead of a command's own steps), so
they arrive whether or not the assistant's skill loads. The decision that shapes the rest is that the
review stops on severity, not on silence, because an unbounded reviewer keeps producing findings and
the change never closes.

| Item | In plain words | Technical |
| --- | --- | --- |
| FR-001 | Someone other than the author reviews the change before completion is reported, folded into converge rather than made a new step. | `preset/commands/speckit.converge.prepend.md`; §Design Decisions |
| FR-002, FR-006 | A finding must come with a command or a line reference; one without evidence is dismissed with a reason rather than counted. | `speckit.converge.prepend.md` review rule; §Risks |
| FR-003 | The review stops when no unresolved finding is HIGH, and is capped at three passes, so a critic asked to find problems cannot stall the change. | §Design Decisions; §Correctness Properties P-003 |
| FR-004–FR-005 | A change that asserts a property is attacked at its negative case first, and a confirmed bypass is kept as a fixture so the same hole cannot return. | `scripts/self-gate.sh`; §Correctness Properties P-001 |
| FR-007 | Prose with no falsifiable oracle is probed for loopholes instead of stress-tested, because there is nothing to execute. | §Design Decisions; §Correctness Properties P-004 |
| FR-008 | The rules are delivered as command text, which is the only delivery that does not depend on the skill loading. | `preset/preset.yml`; `strategy: "prepend"` |
| FR-009 | The new rules sit beside the existing completion-evidence rule without contradicting or repeating it. | `speckit.converge.prepend.md`; §Implementation Boundaries |
| FR-010 | The gate asserts the rule and its bound in the source prepend and in the composed command, so a dropped rule is a failed build. | `scripts/self-gate.sh` §3b, §5 |
| SC-002 | A reviewer who did not do the work can find a real defect and record it with evidence. | §Validation Strategy |
| SC-003 | The materialised command carries the review rule and its severity bound, not just the source file. | `scripts/self-gate.sh` §5 |
| SC-004 | The review terminates on severity rather than running until the reviewer goes quiet. | §Correctness Properties P-005 |
| SC-005 | The gate is green and the preset version matches the newest release entry. | `scripts/self-gate.sh` §1c |

**Terms**

| Term | Plain words |
| --- | --- |
| stress test | an attempt to make the change fail, using the case it is meant to reject |
| prepend | instructions placed ahead of a command's own steps |

## Summary

Add two rule sections to `preset/commands/speckit.converge.prepend.md` — *review by a context that
did not do the work*, and *stress the properties the change asserts* — plus the gate assertions that
make them load-bearing. No new pipeline step, no new artifact type: the review folds into converge,
which already owns close-out.

## Technical Context

- Delivery: preset command prepend (`strategy: "prepend"`), composed after frontmatter onto
  `.opencode/commands/speckit.converge.md`. Same mechanism as the existing converge/specify rules.
- Verification: `scripts/self-gate.sh` (§3b source markers, §5 materialised-command check) and
  `bin/speckit-check` (drift).
- No code, no dependencies, no schema. Bash 3.2-safe gate edits only.

## Design Decisions

- **A rule in converge, not a new step.** Converge already owns "Completion requires evidence" and
  boundary checks; review is the missing sibling. Alternatives — a separate `/speckit.review`, or a
  hook — were rejected: a separate step fragments close-out, and a hook cannot judge.
- **Bounded and severity-gated, not "until zero findings".** Grounded in the self-critique paradox
  (`research.md` [S2]) and the kit's own `specify` precedent (max 3 iterations). A critic told to find
  problems will invent them; the stop signal is severity, not silence.
- **Evidence-bearing findings.** Mirrors AMTSO's "observable evidence over asserted outcomes"
  (`research.md` [S6]); a finding without `file:line`/reproducing command is dismissed with a reason.
- **Stress test triggered by assertion, not size.** Read from red-team practice — verify at the
  action boundary, keep every confirmed bypass as a regression case (`research.md` [S3]–[S6]).
- **Advisory, and stated as advisory.** Like every command rule, this guarantees the rule is read,
  not obeyed. The spec and the rule say so.

## Correctness Properties

Framework decision: **none adopted.** This is a prompt-text change verified by the kit's existing
shell gate; no property-based testing framework is added (`research.md`). Properties below are
checked by deterministic shell assertions (runtime-assert) or by review.

| Property ID | Requirement | Property (for any …) | Check method | Scope |
| --- | --- | --- | --- | --- |
| P-001 | FR-010, SC-002 | for any edit that removes the converge review's evidence bullet (`Every finding carries evidence`) or its severity bound (`Stop when no UNRESOLVED`), the self-gate reports FAIL | runtime-assert | system |
| P-002 | FR-008, SC-003 | for any fresh install, the materialised `.opencode/commands/speckit.converge.md` contains the review rule and its severity bound | runtime-assert | system |
| P-003 | FR-009 | for any converge prepend content, the review rule does not contradict or duplicate the completion-evidence rule | review-only | operation |
| P-004 | FR-006 | for any review finding missing `file:line` or a reproducing command, the rule directs dismissal-with-reason rather than action | review-only | operation |
| P-005 | FR-003, SC-004 | for any review run, termination is defined by unresolved HIGH severity, not by the reviewer's silence | review-only | operation |
| P-006 | (invariant) | for any preset version, it equals the newest `## [x.y.z]` CHANGELOG entry (pre-existing §1c) | runtime-assert | system |

**Non-mapped requirements** (opt-out, with reason): FR-001, FR-002, FR-004, FR-005, FR-007 are
statements about what the converge command must *prescribe*. They are not independently falsifiable
without executing an agent, so no property is forced; they are covered indirectly by P-001/P-002 (the
rule is present and load-bearing) and P-004/P-005 (the rule's operative sentences).

## Implementation Boundaries

- **Must Not Change**: `bin/speckit-init`, `hooks/speckit-hooks.yaml`, the four template addenda,
  `preset/commands/speckit.{specify,plan,tasks,implement}.prepend.md`. This feature touches converge
  and the gate only.
- **Must Not Change**: the existing `### Completion requires evidence` rule — the new rules add to
  it, never contradict or duplicate it (FR-009).
- No new dependency, no named external tool, no enforcement claim.

## Risks

| Risk | Mitigation |
| --- | --- |
| Rule ignored (prompt text) | Accepted and stated; the gate proves the rule is *present*, not obeyed. Review is an outer-loop aid, not a guarantee. |
| Rule bloats the converge command | Two sections, ≤8 bullets, reviewed for length; converge remains the shortest command. |
| "Zero findings" misread as the goal | Bound and severity language is explicit in the rule and asserted by FR-003/SC-004. |
| Gate assertion is keyword-only (the kit's own criticism) | §3b, §5 assert the operating sentences (evidence bullet + severity bound), not only headings, and T008 negative-tests one; substring matching is still a keyword check — recorded as residual H3 in `progress.md`. |

## Requirement Traceability

| Requirement | Design area | Task |
| --- | --- | --- |
| FR-001..FR-007, FR-009 | converge prepend | T004, T005 |
| FR-008 | prepend mechanism | T004, T005 |
| FR-010 | self-gate §3b, §5 | T006, T007 |
| SC-002 | negative test | T008 |
| SC-005 | gate + version/changelog | T006, T009 |
