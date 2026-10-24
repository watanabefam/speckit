# Feature Specification: Fixture — a small cache

**Feature Branch**: `900-fixture-cache`

**Status**: Draft

## In Plain Terms

This fixture describes a cache that keeps the last computed answer and serves it again until it is too
old. It exists so the plain-terms checker has a document that satisfies every rule it enforces.

| Item | In plain words | Technical |
| --- | --- | --- |
| US1 | A caller asks twice and the second answer comes from the cache instead of being recomputed. | US1 |
| FR-001 | Nothing is stored until someone asks for it. | FR-001 |
| FR-002 | A stored answer is served again while it is still young enough to use. | FR-002 |
| FR-003 | An answer that is too old is never served. | FR-003 |
| SC-001 | The second call is noticeably cheaper than the first. | SC-001 |
| SC-002 | No out-of-date value is ever observed. | SC-002 |

**Terms**

| Term | Plain words |
| --- | --- |
| stale | older than the allowed age, so it must not be served |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Read from the cache (Priority: P1)

A caller asks for a value twice, and the second answer comes from the cache.

**Why this priority**: it is the whole feature.

**Independent Test**: ask twice and count the recomputations.

**Acceptance Scenarios**:

1. **Given** an empty cache, **When** the caller asks, **Then** the value is computed once and stored.

## Requirements *(mandatory)*

- **FR-001**: The cache MUST NOT store a value before it is requested.
- **FR-002**: The cache MUST serve a stored value while it is not stale (older than the allowed age, which in this fixture means older than the configured lifetime measured in seconds since the value was first computed by the caller of the cache).
- **FR-003**: The cache MUST NOT serve a stale value.

## Success Criteria *(mandatory)*

- **SC-001**: The second call takes at most half the time of the first.
- **SC-002**: Zero stale values are observed across the trial.
