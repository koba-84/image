## Purpose

Define enforceable engineering standards for reproducibility, safety, and traceable Git operations in this image AI project.
## Requirements
### Requirement: Coding standards are reproducibility-first
The project MUST enforce coding standards that prioritize reproducibility and safe image processing for image generation/editing experiments.

#### Scenario: Experiment metadata is recorded
- **WHEN** a new experiment script or notebook is added
- **THEN** the change MUST define how seed, model/version, prompt, input data, and key parameters are recorded for rerun

#### Scenario: Image processing boundaries are explicit
- **WHEN** image input/output processing logic is implemented
- **THEN** the change MUST specify image format, color space, and resolution handling without implicit conversion assumptions

### Requirement: Naming conventions are explicit and consistent
The project MUST apply a consistent naming convention based on Python best practices.

#### Scenario: Variables and functions follow snake_case
- **WHEN** contributors add or modify Python code
- **THEN** variable names and function names MUST use `snake_case`, and names MUST describe intent

#### Scenario: Classes and constants use dedicated styles
- **WHEN** contributors define classes or constants
- **THEN** classes MUST use `PascalCase` and constants MUST use `UPPER_SNAKE_CASE`

### Requirement: Git workflow is reviewable and traceable
The project MUST use a Git workflow that keeps history machine-readable and reviewable.

#### Scenario: Commit format follows convention
- **WHEN** contributors create commits
- **THEN** commit messages MUST follow Conventional Commits with a valid type prefix

#### Scenario: Breaking change is explicitly declared
- **WHEN** a change introduces backward incompatibility
- **THEN** the commit MUST include either `!` in type/scope or a `BREAKING CHANGE:` footer

#### Scenario: Main branch is protected by process
- **WHEN** code is integrated into main
- **THEN** changes MUST be merged through Pull Request review instead of direct push

### Requirement: Autonomous commits are guardrailed
The project MUST allow agent-driven autonomous commits only with verification and safety controls.

#### Scenario: Agent commits after verification
- **WHEN** an agent completes an implementation task
- **THEN** the agent MUST run relevant tests or validation commands and commit only if they pass

#### Scenario: Agent commit scope is controlled
- **WHEN** an agent creates a commit
- **THEN** the agent MUST ensure only intended files are included and MUST avoid committing secrets or personal data

#### Scenario: Agent push is branch-scoped
- **WHEN** an agent pushes autonomous changes
- **THEN** the push MUST target a non-`main` branch and be followed by Pull Request creation

#### Scenario: Autonomous PR contains verification evidence
- **WHEN** an agent opens a Pull Request
- **THEN** the PR description MUST include executed validation commands, outcomes, and rollback notes

#### Scenario: Automation token is least-privilege
- **WHEN** an agent authenticates for autonomous push/PR operations
- **THEN** the credential scope MUST be limited to the minimum required repository permissions (for example `contents:write` and `pull-requests:write`)

### Requirement: OpenSpec artifacts stay aligned before implementation
The project MUST update OpenSpec artifacts before implementation when behavior or process requirements change.

#### Scenario: Spec-impacting change starts
- **WHEN** a contributor plans a change that affects behavior, quality gates, or process rules
- **THEN** proposal/design/tasks/spec artifacts MUST be updated before or alongside implementation tasks

### Requirement: OpenSpec is authoritative for behavior requirements
The project MUST treat OpenSpec specs and active change artifacts as the authoritative source for behavior and process requirements.

#### Scenario: Instruction conflict is detected
- **WHEN** repository instructions (for example AGENTS or tool guidance files) conflict with OpenSpec artifacts
- **THEN** contributors MUST follow OpenSpec artifacts
- **AND** update the conflicting instruction files so they become operational guidance consistent with OpenSpec

### Requirement: Execution fallback handling is explicit
The project MUST define a fallback workflow for cases where an agent cannot complete work as expected.

#### Scenario: Agent investigates capability before escalation
- **WHEN** an agent cannot complete a requested task with the current approach
- **THEN** the agent MUST investigate available skills, tools, and project instructions, and retry with a better approach before asking for escalation

#### Scenario: Blockers are escalated with traceable context
- **WHEN** an agent still cannot proceed after capability investigation and retry
- **THEN** the agent MUST report the blocker, attempted investigation/retry steps, and the specific missing requirement or dependency

### Requirement: Model selection governance is explicit and auditable
The project MUST keep model selection criteria explicit, version-deduplicated by family, and auditable across open-weight and closed API candidates.

#### Scenario: One model per family is enforced
- **WHEN** model candidates are documented or refreshed
- **THEN** only one active model per family MUST be listed, preferring the latest and strongest evidence-backed variant

#### Scenario: Candidate coverage is periodically verified
- **WHEN** candidate models are reviewed
- **THEN** maintainers MUST run a reproducible audit that checks for missing high-signal families and reports gaps

#### Scenario: Closed API models are included in verification
- **WHEN** model coverage is audited
- **THEN** the audit MUST include closed API candidates with provider, model identifier, and API reference metadata

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

