# image-generation-workflow Specification

## Purpose
TBD - created by archiving change clarify-functional-spec-coverage. Update Purpose after archive.
## Requirements
### Requirement: Mode-specific input contract MUST be explicit
The system MUST define required inputs per generation mode so execution preconditions are deterministic.

#### Scenario: text2img input contract
- **WHEN** mode is `text2img`
- **THEN** `prompt` MUST be provided
- **AND** `image` and `mask_image` MUST NOT be required

#### Scenario: img2img input contract
- **WHEN** mode is `img2img`
- **THEN** `prompt` and `image` MUST be provided
- **AND** `mask_image` MUST NOT be required

#### Scenario: inpaint input contract
- **WHEN** mode is `inpaint`
- **THEN** `prompt`, `image`, and `mask_image` MUST be provided

### Requirement: Output artifact contract MUST be reproducible
The system MUST produce a deterministic artifact set for each successful run.

#### Scenario: image output exists on success
- **WHEN** inference succeeds
- **THEN** an output image file MUST be written at the configured output path

#### Scenario: metadata output exists on success
- **WHEN** inference succeeds
- **THEN** metadata MUST be written alongside the output image
- **AND** metadata MUST include at least mode, model identifier, prompt, seed, steps, guidance scale, and output size

### Requirement: Failure handling MUST be observable and actionable
The system MUST fail with traceable context when preconditions or runtime execution fail.

#### Scenario: missing required inputs are rejected before inference
- **WHEN** required inputs for the selected mode are missing
- **THEN** the system MUST stop before model inference
- **AND** the error message MUST identify the missing input names

#### Scenario: runtime failure leaves diagnostic evidence
- **WHEN** model loading or inference fails at runtime
- **THEN** the system MUST emit an error log containing mode, model identifier, and failure stage

