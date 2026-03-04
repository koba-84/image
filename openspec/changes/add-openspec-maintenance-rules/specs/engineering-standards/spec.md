## ADDED Requirements

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

