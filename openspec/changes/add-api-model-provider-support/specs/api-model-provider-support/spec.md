## ADDED Requirements

### Requirement: API backend selection MUST be deterministic
The system MUST select API backend execution when `model_id` uses a supported provider prefix.

#### Scenario: OpenAI-prefixed model id is routed to API backend
- **WHEN** `model_id` is formatted as `openai:<model-name>`
- **THEN** inference MUST run through the OpenAI image API backend
- **AND** diffusers local pipeline loading MUST NOT be used

#### Scenario: Google-prefixed model id is routed to API backend
- **WHEN** `model_id` is formatted as `google:<model-name>`
- **THEN** inference MUST run through the Google image API backend
- **AND** diffusers local pipeline loading MUST NOT be used

#### Scenario: Ideogram-prefixed model id is routed to API backend
- **WHEN** `model_id` is formatted as `ideogram:<model-name>`
- **THEN** inference MUST run through the Ideogram image API backend
- **AND** diffusers local pipeline loading MUST NOT be used

### Requirement: API authentication MUST be validated before request
The system MUST validate required credentials before making remote API calls.

#### Scenario: Missing API key is rejected
- **WHEN** an OpenAI API backend run is requested and `OPENAI_API_KEY` is not set
- **THEN** the run MUST fail before request execution
- **AND** the error message MUST include the missing environment variable name

#### Scenario: Missing provider credentials are rejected
- **WHEN** a Google or Ideogram API backend run is requested without required credentials
- **THEN** the run MUST fail before request execution
- **AND** the error message MUST include the missing environment variable names

### Requirement: API result handling MUST return a savable image object
The system MUST normalize API response formats into an image object compatible with existing output flow.

#### Scenario: Base64 image response is normalized
- **WHEN** API response includes image bytes via base64 payload
- **THEN** the system MUST decode it and return an image object that supports `.save()`

#### Scenario: URL image response is normalized
- **WHEN** API response includes image URL payload
- **THEN** the system MUST fetch the image and return an image object that supports `.save()`
