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
The project MUST apply a consistent naming convention based on Python best practices and MUST prefer established official terminology when a standard name exists for the same ML operation.

#### Scenario: Variables and functions follow snake_case
- **WHEN** contributors add or modify Python code
- **THEN** variable names and function names MUST use `snake_case`, and names MUST describe intent

#### Scenario: Classes and constants use dedicated styles
- **WHEN** contributors define classes or constants
- **THEN** classes MUST use `PascalCase` and constants MUST use `UPPER_SNAKE_CASE`

#### Scenario: Standard ML terminology is prioritized
- **WHEN** an operation has an established term in official documentation (for example Diffusers/PyTorch/pytest)
- **THEN** contributors MUST prefer that standard term over project-local ad hoc wording for function and test naming

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

### Requirement: OpenSpec artifacts MUST not depend on `.copilot/session` paths
Active OpenSpec artifacts MUST avoid defining repository process rules that require `.copilot/session` (or equivalent session-local state paths) as part of normal project workflow.

#### Scenario: Session-path dependency is rejected
- **WHEN** proposal/design/tasks/spec artifacts for an active change are created or updated
- **THEN** they MUST NOT require `.copilot/session` or `session-state` paths for repository workflow decisions

### Requirement: Active artifacts MUST avoid stale references to archived changes
Active OpenSpec artifacts MUST keep references focused on currently relevant specs/changes and remove unnecessary references to prior archived changes.

#### Scenario: Stale historical reference is cleaned up
- **WHEN** an active change artifact includes references to archived or superseded changes
- **THEN** maintainers MUST remove references that are not required for current implementation or verification decisions

### Requirement: Autonomous Git lifecycle MUST enforce clean checkpoints
Autonomous contributors MUST keep the working tree auditable and avoid persistent uncommitted backlog by enforcing clean-check checkpoints.

#### Scenario: Agent validates clean state before push
- **WHEN** an agent is about to push a branch
- **THEN** the agent MUST run `git status --short`
- **AND** the output MUST be empty before `git push`

#### Scenario: Agent validates clean state after commit series
- **WHEN** an agent finishes the intended commit sequence for a task
- **THEN** the agent MUST verify no unintended tracked or untracked leftovers remain
- **AND** any remaining intended work MUST be committed in an additional scoped commit

### Requirement: Autonomous commits MUST be granular and machine-readable
Autonomous contributors MUST create small, focused commits with structured messages.

#### Scenario: Commit message follows Conventional Commits
- **WHEN** an agent creates a commit
- **THEN** the message MUST use a valid Conventional Commits type prefix (for example `feat:`, `fix:`, `chore:`)

#### Scenario: Commit scope maps to one logical change
- **WHEN** an agent stages files for a commit
- **THEN** staged files MUST correspond to a single logical purpose
- **AND** unrelated edits MUST be split into separate commits

#### Scenario: Agent commits at logical checkpoints
- **WHEN** an agent completes a logical unit of work (for example one requirement/task chunk) or is about to switch context
- **THEN** the agent MUST create a scoped commit before starting the next logical unit
- **AND** the agent MUST NOT defer all local changes into one large end-of-session commit

### Requirement: Autonomous branch integration MUST remain protected
Autonomous contributors MUST integrate through reviewable PR flow and protected branch expectations.

#### Scenario: Main integration goes through PR checks
- **WHEN** autonomous work targets `main`
- **THEN** integration MUST occur through Pull Request review and required checks
- **AND** direct push to `main` MUST NOT be used

#### Scenario: Branch synchronization happens before push
- **WHEN** an agent prepares to publish local commits
- **THEN** the agent MUST synchronize with upstream branch state
- **AND** resolve conflicts before final push/PR update

#### Scenario: Agent pushes immediately after local verification
- **WHEN** commits for the current task scope are complete and required validation commands pass
- **THEN** the agent MUST push that scope without unnecessary delay
- **AND** the agent MUST avoid keeping validated commits only in local state across additional unrelated work

#### Scenario: Agent pushes only review branch
- **WHEN** an agent pushes autonomous commits
- **THEN** the push target MUST be a non-`main` branch
- **AND** the agent MUST verify push success from command output

#### Scenario: Agent opens PR after successful push
- **WHEN** an autonomous branch push succeeds
- **THEN** the agent MUST open or update a Pull Request for review before mainline integration
- **AND** the PR body MUST include executed validation commands and outcomes

#### Scenario: Agent records commit and push checkpoint evidence
- **WHEN** an agent completes a logical work unit and publishes it
- **THEN** the agent MUST leave traceable evidence of commit timing and push timing (for example command logs or PR timeline)
- **AND** reviewers MUST be able to verify that commit occurred at logical boundary and push occurred immediately after required validation

