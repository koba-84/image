## ADDED Requirements

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
