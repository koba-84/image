## ADDED Requirements

### Requirement: Archive lifecycle checks MUST be standardized
OpenSpec archive operations MUST follow a standard sequence of verification, archive execution, and post-check.

#### Scenario: Standard archive sequence is executed
- **WHEN** a contributor finalizes a completed change
- **THEN** they MUST run `openspec status --change "<name>"`
- **AND** they MUST run `openspec archive <name> --yes`
- **AND** they MUST confirm archived path under `openspec/changes/archive/`

#### Scenario: Post-archive verification is recorded
- **WHEN** archive execution completes
- **THEN** contributors MUST run `openspec validate --changes --strict`
- **AND** they MUST record command outcomes in PR description or work log
