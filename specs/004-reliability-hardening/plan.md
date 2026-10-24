# Plan — Reliability Hardening

**Spec:** `spec.md` · **Tasks:** `tasks.md` · **Ledger:** `progress.md`

## In Plain Terms

This plan repairs the gate first, because every other check in the kit is judged by it, then closes the
two places where a guard (a hook that refuses a dangerous command) allowed an action it could not read,
and only then widens the checker and the resume path. The ordering is the design: a fix measured by a
dishonest gate is not measured at all. Two dependency removals carry most of the benefit — `jq` leaves
the hook bodies, and the installer reports drift (a generated file that no longer matches its source)
instead of trusting a version string.

| Item | In plain words | Technical |
| --- | --- | --- |
| FR-001 | A skipped section names itself and a bare PASS is never printed in its place. | §Decisions D4; `bin/speckit-verify` verdict |
| FR-002 | Hook bodies use the Python already required by the installer instead of `jq`, removing the condition under which the guards silently stood aside. | §Decisions D1; `hooks/speckit-hooks.yaml` |
| FR-003–FR-004 | The installer adds a permission block when it is absent and never rewrites one the owner already has. | §Decisions D3; `bin/speckit-init` |
| FR-005 | Each guard body is executed against blocking, allowing and malformed payloads rather than grepped for a string. | §Decisions D5; `scripts/self-gate.sh` |
| FR-006 | Drift is computed from artifacts that exist in the project, not from a version string that can lie. | §Decisions D6; `bin/speckit-check` |
| FR-007 | Resume compares the ledger's plan identity, and a ledger written before the header existed still works. | §Decisions D7; `bin/speckit-resume` |
| FR-008 | A second install describes only the work it actually did. | §Decisions D3; `bin/speckit-init` |
| FR-009 | The gate asserts that a second install leaves the prepends and the permission block unchanged. | `scripts/self-gate.sh`; §Verification |
| FR-010 | The Commands block describes `scripts/verify` as running the recorded checks, which is what it does. | §Decisions D6; `AGENTS.md` Commands block |
| SC-001, SC-003, SC-005 | A skip is visible under strict mode, a brownfield install keeps every key it had, and a second install changes nothing. | `scripts/self-gate.sh`; §Verification |
| SC-002, SC-004, SC-006 | The guard probes return the expected exit codes, each removed artifact is reported as drift, and a mismatched ledger exits 2. | `scripts/self-gate.sh`; `bin/speckit-resume` |

**Terms**

| Term | Plain words |
| --- | --- |
| guard | a hook that refuses a dangerous command before it runs |
| drift | a generated file that no longer matches the source it was generated from |

## Approach

Covers FR-001–FR-010 and SC-001–SC-006 of `spec.md`.

Fix in dependency order: make the gate honest first (it is the oracle for everything else), then
close the two fail-open paths, then widen the checker and resume.

## Decisions

- **D1 — Remove `jq`; use `python3` in hook bodies.** `python3` is already required by the
  installer and `speckit-resume`. Removing a dependency is better than checking for it, and it
  removes the exact condition under which the guards silently stood aside.
- **D2 — Fail closed on unparseable payloads (exit 2).** The plugin always sends JSON; anything else
  is an unexpected shape. Allowing it is how a guard disappears when the payload shape changes.
- **D3 — Additive JSON merge only for `opencode.json`.** JSONC with comments cannot be round-tripped
  safely, so `.jsonc` keeps the print-only path and says why.
- **D4 — Skips are a third state.** The verdict becomes PASS / FAIL / INCOMPLETE; `--strict` turns
  INCOMPLETE into a non-zero exit for CI.
- **D5 — Behavioural probes, not string checks.** Extract each hook body from the YAML and execute it
  with real payloads, including a `PATH` with no `jq`.
- **D6 — Checker uses evidence already present.** It greps for the prepend marker in each composed
  command and for the permission/contract/verify artifacts, instead of trusting a version string.
- **D7 — Resume compares ledger identity.** Backward compatible: a ledger with no header still works.

## Risks

- **Hook latency.** Python startup adds ~40 ms per guarded call. Acceptable; the prefilter means it
  only runs for candidate commands.
- **False blocks on malformed payloads.** Deliberate: a guard that cannot read its input must not
  allow the action.
- **Policy change for skips.** CI that relied on skips exiting 0 now needs `--strict` to see them;
  the default keeps the old exit code but stops calling a skip a PASS.

## Verification

`./scripts/self-gate.sh --strict` and `make test`, plus the browser-free probes inside the gate.
