## ADDED Requirements

### Requirement: Mode compatibility with backend MUST be explicit
The system MUST reject unsupported mode/backend combinations with actionable errors.

#### Scenario: API backend rejects unsupported edit modes
- **WHEN** backend is API and mode is `img2img` or `inpaint`
- **THEN** the system MUST fail fast before remote inference call
- **AND** the error message MUST state that only `text2img` is currently supported

### Requirement: Metadata MUST include execution backend context
The system MUST record backend context in output metadata for auditability.

#### Scenario: API-backed run metadata
- **WHEN** inference is executed with an API backend
- **THEN** output metadata MUST include backend type and provider identifier
