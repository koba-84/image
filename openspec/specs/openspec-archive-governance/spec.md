# openspec-archive-governance Specification

## Purpose
TBD - created by archiving change define-archive-governance-best-practices. Update Purpose after archive.
## Requirements
### Requirement: Archive execution prechecks MUST be explicit
Contributors MUST verify change completion and spec consistency before running `openspec archive`.

#### Scenario: Precheck before archiving a single change
- **WHEN** a contributor is about to run `openspec archive <change-name>`
- **THEN** they MUST confirm `openspec status --change "<change-name>"` shows artifacts complete
- **AND** they MUST run `openspec validate --changes --strict`

### Requirement: Archive option usage MUST be restricted and auditable
Risky archive options MUST be limited to explicit conditions with traceable rationale.

#### Scenario: Using --skip-specs
- **WHEN** a contributor uses `openspec archive --skip-specs`
- **THEN** the change MUST be doc-only or tooling-only with no spec delta to merge
- **AND** the contributor MUST record the reason in the work log or PR description

#### Scenario: Using --no-validate
- **WHEN** a contributor uses `openspec archive --no-validate`
- **THEN** they MUST document the blocking reason for normal validation
- **AND** they MUST run `openspec validate --changes --strict` immediately after blocker resolution

### Requirement: Multi-change archive sequence MUST minimize conflicts
When archiving multiple completed changes, contributors MUST apply an order that reduces merge conflicts and preserves traceability.

#### Scenario: Multiple completed changes exist
- **WHEN** two or more completed changes are pending archive
- **THEN** contributors MUST archive in chronological order (oldest first)
- **AND** they MUST run validation after each archive step

#### Scenario: Spec conflict is detected during archive
- **WHEN** archive reports spec conflict
- **THEN** contributors MUST resolve conflict before the next change archive
- **AND** they MUST record the resolution basis in the PR or work log

