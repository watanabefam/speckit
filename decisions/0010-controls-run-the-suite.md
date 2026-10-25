# 0010 — A negative control runs the suite against a mutant, and fails for the stated reason

## Context

Feature 005 built `bin/speckit-verify` and its contract: a check is evidence only if it declares an oracle
outside the code under test **and** its declared negative control has failed. A test check with no control
is reported `vacuous`, and the verdict is `INCOMPLETE`.

`bin/speckit-init` deliberately seeds a manifest *without* a control, so a fresh install reports
`INCOMPLETE` until the owner supplies one. This repository is an owner, and it had not: `./scripts/verify`
answered `INCOMPLETE — nothing was examined, 1 vacuous check(s)` on every run, including runs where the
whole 218-assertion gate passed. A command that says "I checked nothing" every time teaches its reader to
skip its output, and then it cannot warn them about anything.

The manifest's `control` field is documented as "a command that must FAIL", and the engine's own
measurement fixture uses the minimal form: `python -c "import sys; sys.exit(1)"`
(`evals/measure-sc004.py`). That form is honest about one thing only — that the runner can see a non-zero
status. It is a test of the runner, not of the suite.

## Research

**A control has to travel the same path as the sample.** In laboratory practice a negative control is
processed identically to the specimen and must produce the expected negative result; if it does not, the
run is invalid rather than merely unlucky (FDA EUA templates put it as "the negative control must be
negative"; 10 CFR 26 Subpart G says each analytical run carries controls that must be negative). The
translation is not decorative: a control that bypasses the entry point is measuring a different pipeline.

**The software form of that idea is a mutant.** Mutation testing seeds a small syntactic change and asks
whether the suite notices; Stryker's documentation states the premise plainly ("if your tests are good,
they should catch the change and fail… if they still pass, your tests might not be strong enough") and
adds the cost discipline this repository needs ("don't chase a 100% mutation score"). Just et al. (FSE
2014, DOI 10.1145/2635868.2635929) is the study that justifies mutants as a stand-in for real faults, and
it is careful about what it shows: mutants *couple* with real faults, they are not identical to them.
Petrović et al. (TSE 2021, DOI 10.1109/tse.2021.3107634) is the industrial account of running this at
scale, where the answer is selection — a sampled mutant, not a campaign.

**Passing for the wrong reason is a named failure.** Model checking learned this as *vacuity*: a property
can hold trivially, and a pass is only meaningful if the result depends on the thing under test
(Kupferman & Vardi, STTT 2003, DOI 10.1007/s100090100062; Beer et al., FMSD 2001, DOI
10.1023/a:1008779610539). The practical consequence here is that "the suite exited non-zero" is not the
signal — a broken copy, a missing tool or a typo in the control all produce a non-zero exit too.

**The oracle has to be outside the code under test** (Barr et al., TSE 2015, DOI 10.1109/tse.2014.2372785),
which is what feature 005's `oracle` field already enforces. The control is the complementary half: the
oracle says where the expected value comes from, the control says the machinery can reach a verdict at all.

Those four sources agree, and they agree with `0006`: a silence is not a result. Convergence was on the
shape below, not on adding a fifth mechanism.

## Decision

**1. The control is a mutant of this tree, run through the declared command.** `scripts/negative-control.sh`
copies the tree, applies a mutator, runs the manifest's command for the check, and judges the outcome. The
command is read from the manifest rather than repeated on the control line, so a control can never end up
measuring a command the check does not run.

**2. The mutation is one this gate exists to catch.** `.specify/controls/plain-row-missing.py` deletes one
coverage row from a specification's plain table — the drift between a document's claims and its content.
It is the defect `specs/007` was built around, and the gate already asserts it can see it (§3e/§3f teeth);
the control is the manifest-level statement of the same fact.

**3. The failure must arrive for the stated reason.** The control requires the expected text
(`has no row`) in the failing output. Without that half, any breakage reads as detection: a copy that lost
a tool, a mutator that pointed at the wrong file, a suite that failed on its own fixture. This is the
vacuity point, applied to the control itself.

**4. The three outcomes are the engine's, and they are a contract.**
`1` = the mutant was caught, by the expected message (the check is evidence); `0` = the suite stayed green
under the mutation (the engine reports `vacuous`, which is the right diagnosis); `127` = the control could
not demonstrate anything — no mutant, no such command, or a red run for the wrong reason (`not-run`, never
evidence). `bin/speckit-verify:476-500` already distinguishes exactly these three, so the script invents
no new vocabulary.

**5. Always a copy, never in place.** A control that edits the tree it is judging leaves that tree broken if
it is interrupted, and every later run then measures the mutant. The gate asserts the source tree is
unchanged after the fixture runs.

**6. One sampled mutant, reported as validity rather than as a score.** The control says "this suite can
notice this class of defect", not "this suite is strong". Feature 005's contract already requires that a
mutation percentage is labelled `budget` and never `verdict`; a single mutant is that discipline taken to
its minimum, and it is why the run has a bounded cost (~85 s here) instead of unbounded.

**7. The check declares `runner: "command"`, not `runner: "make"`.** The engine's `make` adapter reads
pass/fail summary counts and has no `examined=` branch, so `make test` under `runner: make` reported
`examined unknown` and the verdict stayed `INCOMPLETE` even with the control in place. The `command`
adapter reads `examined=N`, which is this suite's own convention. The alternative — teaching the `make`
adapter the `examined=` fallback — changes an implemented adapter in feature 005 and belongs in that
feature's specification, not in a control change. Recorded as parked work below.

## Consequences

- `./scripts/verify --all` now reports `SELF-VERIFY: PASS — 1 check(s), 0 skipped, 0 failed (examined all
  declared checks)`, exit 0, `examined=218`, with a durable ledger record.
- A verify run now costs about 2 m 46 s here: 85 s of control, 79 s of suite, and the copy. That is the
  price of a control that is worth having, and it is the number to watch if the suite grows — the engine
  caches nothing, so each run pays it again.
- The gate's §3g asserts the contract cheaply (a throwaway tree, four invocations, no suite run), because
  a verification that costs a minute and a half is the first one a maintainer deletes.
- The control proves one defect class per run. A different mutation would prove a different class; adding
  a second mutator is a small change to this script's arguments, and doing so would multiply the cost.

## Rejected alternatives

- **`exit 1` as the control.** Cheap and always "fails", so the engine would accept it and every run would
  claim evidence. It proves the runner propagates an exit code — nothing about the suite.
- **A control that runs the checker alone.** Fast, but it is not the check: the check is the gate, and a
  control that bypasses it measures a pipeline no one declared.
- **A full mutation campaign (Stryker, mutmut, PIT).** No new dependency, no build step, and the cost at
  this repository's size buys a strength score nobody asked to gate on. A sampled mutant through the real
  entry point is the smaller true statement.
- **Running the control only in the nightly job.** Then the per-change run is back to claiming evidence it
  has not earned, which is the state this decision exists to leave.

## What this does not claim

- One mutant is not a fault model. It shows the gate can catch *this* defect; it does not bound what the
  gate misses, and nothing here should be read as a mutation score.
- The control demonstrates the gate's teeth, not its correctness: a gate that catches the wrong thing
  consistently would pass this control too.
- The expected message is a grep, not a parse. A future message change breaks the control loudly (it
  returns `127`, which is `INCOMPLETE`), which is the safe direction but not a good one to land in often.

## Parked

- The `make` adapter cannot read `examined=`. Any adopter whose `make test` wraps a suite that prints
  `examined=N` gets `examined unknown` and an `INCOMPLETE` verdict with a working control. The fix is a
  three-line fallback in `bin/speckit-verify`, plus a harness case and an amendment to `specs/005` — a
  feature-sized change, not a fast-lane one.
- A second mutator (for example: neuter `check-plain-terms.py` in both copies and require the fixture
  assertions to notice) would cover the "the checker stopped detecting" class, at double the cost.
