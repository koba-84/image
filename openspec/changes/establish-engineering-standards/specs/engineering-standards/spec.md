## ADDED Requirements

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
