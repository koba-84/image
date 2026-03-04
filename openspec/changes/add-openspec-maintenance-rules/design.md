## Context

This project treats OpenSpec artifacts as the source of truth for implementation behavior and process requirements. To keep artifacts reliable, references must remain focused on active change context and avoid stale operational assumptions.

## Decisions

1. Add a rule that OpenSpec change artifacts MUST NOT require `.copilot/session` paths for operational flow.
   - Rationale: session-local paths are runtime-specific and should not become repository process requirements.
2. Add a rule that active OpenSpec artifacts MUST avoid unnecessary references to archived/prior changes.
   - Rationale: stale references increase ambiguity and maintenance cost.
3. Enforce both items via tasks and validation checks in each relevant change.
   - Rationale: rule-only statements are insufficient without repeatable verification.

## Risks / Trade-offs

- Stricter review may add small overhead to artifact updates.
- Cleanup work may require touching already-complete changes for reference hygiene.

## Migration Plan

1. Add spec requirements for OpenSpec maintenance hygiene.
2. Add concrete tasks for `.copilot/session` exclusion and stale-reference cleanup.
3. Validate with `openspec validate --changes --strict --json`.

