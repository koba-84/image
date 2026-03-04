## ADDED Requirements

### Requirement: Specification purpose MUST be explicit and non-placeholder
OpenSpec source-of-truth specs MUST include a concrete purpose statement and MUST NOT use placeholders such as `TBD`.

#### Scenario: New or updated spec is reviewed
- **WHEN** a contributor creates or updates `openspec/specs/*/spec.md`
- **THEN** the `Purpose` section MUST describe the capability intent in concrete terms
- **AND** placeholder text (for example `TBD`) MUST be rejected in review
