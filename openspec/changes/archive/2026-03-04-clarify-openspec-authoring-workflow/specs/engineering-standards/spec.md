## ADDED Requirements

### Requirement: OpenSpec authoring workflow MUST be explicit and validated
The project MUST require OpenSpec command-driven artifact progression, delta-spec-first authoring, and pre-implementation workflow checks for every active change.

#### Scenario: Pre-implementation checks are enforced
- **WHEN** a contributor prepares to implement a change
- **THEN** they MUST run `openspec status --change "<name>" --json`
- **AND** they MUST run `openspec instructions apply --change "<name>" --json`
- **AND** they MUST run `openspec validate --changes --strict --json`

#### Scenario: Spec changes use delta flow
- **WHEN** contributors change requirements
- **THEN** they MUST author changes in `openspec/changes/<change>/specs/`
- **AND** they MUST merge to `openspec/specs/` via sync/archive flow
