# Implementation Plan: Generated Gate Report

**Spec**: `spec.md`

## In Plain Terms

This plan makes the gate read a manifest (a file listing the checks a run must perform) and report
which checks it could not execute, instead of printing a single number. It reuses the script that
already produces the report, because a second script would eventually disagree with the first. The
trade-off is one more read at startup, which is cheaper than a report nobody can audit.

| Item | In plain words | Technical |
| --- | --- | --- |
| FR-001–FR-002 | The report comes from the manifest, not from a typed total, so it cannot claim checks that never ran. | `bin/gate`; §Architecture |
| FR-003 | A check that cannot fail is labelled as such rather than counted as evidence. | §Validation |
| SC-001 | The run names how many checks it examined, so a zero is visible. | `bin/gate --json` |

**Terms**

| Term | Plain words |
| --- | --- |
| manifest | a file listing the checks a run must perform |

## Technical Context

- Python 3, standard library only.
- The manifest is JSON, read once by `bin/gate`.

## Architecture

`bin/gate` loads the manifest, executes each check, and builds the report from what executed.

## Validation

- FR-001, FR-002 and FR-003 are asserted against the manifest reader.
- SC-001 is read from `bin/gate --json`.
