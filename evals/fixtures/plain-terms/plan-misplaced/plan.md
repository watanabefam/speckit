# Implementation Plan: Generated Gate Report

**Spec**: `spec.md`

## Technical Context

- Python 3, standard library only.
- The manifest is JSON, read once by `bin/gate`.

## In Plain Terms

This plan makes the gate read a manifest (a file listing the checks a run must perform) and report
which checks it could not execute. It reuses the script that already produces the report, because a
second script would eventually disagree with the first. The trade-off is one more read at startup.

| Item | In plain words | Technical |
| --- | --- | --- |
| FR-001–FR-003 | The report comes from the manifest, so it cannot claim checks that never ran. | `bin/gate`; §Architecture |
| SC-001 | The run names how many checks it examined. | `bin/gate --json` |

**Terms**

| Term | Plain words |
| --- | --- |
| manifest | a file listing the checks a run must perform |

## Architecture

`bin/gate` loads the manifest, executes each check, and builds the report from what executed.

## Validation

- FR-001, FR-002, FR-003 and SC-001 are asserted against the manifest reader.
