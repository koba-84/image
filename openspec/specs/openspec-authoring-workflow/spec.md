# openspec-authoring-workflow Specification

## Purpose
TBD - created by archiving change clarify-openspec-authoring-workflow. Update Purpose after archive.
## Requirements
### Requirement: OpenSpec artifact progression MUST be command-driven
For active changes, artifact creation/progression MUST use OpenSpec workflow commands (`/opsx:*`) or equivalent `openspec` CLI commands so dependency status remains authoritative.

#### Scenario: Artifact creation follows OpenSpec workflow commands
- **WHEN** a contributor starts or advances a change artifact
- **THEN** they MUST use OpenSpec workflow commands to create/progress artifacts instead of bypassing workflow state tracking

#### Scenario: Implementation starts after context confirmation
- **WHEN** implementation for a change is about to begin
- **THEN** contributors MUST confirm `openspec status --change "<name>"` and `openspec instructions apply --change "<name>"` results

### Requirement: Spec updates MUST be written as change deltas before merge
Spec additions/modifications MUST be authored in `openspec/changes/<change>/specs/<capability>/spec.md` as delta specs, and main specs MUST be updated through OpenSpec sync/archive flow.

#### Scenario: Contributor proposes a spec change
- **WHEN** a contributor needs to add or modify requirements
- **THEN** they MUST update the active change delta spec under `openspec/changes/<change>/specs/`
- **AND** they MUST NOT treat direct edits to `openspec/specs/` as the normal change path

#### Scenario: Delta specs are merged to source-of-truth specs
- **WHEN** a change is finalized or synced
- **THEN** contributors MUST use `/opsx:sync` or `/opsx:archive` (or equivalent CLI lifecycle commands) to merge delta specs into `openspec/specs/`

### Requirement: Specification purpose MUST be explicit and non-placeholder
OpenSpec source-of-truth specs MUST include a concrete purpose statement and MUST NOT use placeholders such as `TBD`.

#### Scenario: New or updated spec is reviewed
- **WHEN** a contributor creates or updates `openspec/specs/*/spec.md`
- **THEN** the `Purpose` section MUST describe the capability intent in concrete terms
- **AND** placeholder text (for example `TBD`) MUST be rejected in review

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

