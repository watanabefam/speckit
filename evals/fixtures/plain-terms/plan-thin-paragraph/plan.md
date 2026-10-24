# Implementation Plan: Generated Gate Report

**Spec**: `spec.md`

## In Plain Terms

This plan makes the gate read a manifest (a file listing the checks a run must perform) and report
which checks it could not execute. It reuses the script that already produces the report.

| Item | In plain words | Technical |
| --- | --- | --- |
| FR-001–FR-003 | The report comes from the manifest, so it cannot claim checks that never ran. | `bin/gate`; §Architecture |
| SC-001 | The run names how many checks it examined. | `bin/gate --json` |

**Terms**

| Term | Plain words |
| --- | --- |
| manifest | a file listing the checks a run must perform |

## Technical Context

- Python 3, standard library only.

## Validation

- FR-001, FR-002, FR-003 and SC-001 are asserted against the manifest reader.
