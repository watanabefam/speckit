# Feature Specification: Fixture — a small cache

**Feature Branch**: `900-fixture-cache`

**Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Read from the cache (Priority: P1)

A caller asks for a value twice, and the second answer comes from the cache.

**Why this priority**: it is the whole feature.

**Independent Test**: ask twice and count the recomputations.

**Acceptance Scenarios**:

1. **Given** an empty cache, **When** the caller asks, **Then** the value is computed once and stored.

## Requirements *(mandatory)*

- **FR-001**: The cache MUST NOT store a value before it is requested.
- **FR-002**: The cache MUST serve a stored value while it is not stale (older than the allowed age, so it must not be served).
- **FR-003**: The cache MUST NOT serve a stale value.

## Success Criteria *(mandatory)*

- **SC-001**: The second call takes at most half the time of the first.
- **SC-002**: Zero stale values are observed across the trial.
