# ml-naming-standardization Specification

## Purpose
TBD - created by archiving change standardize-ml-naming. Update Purpose after archive.
## Requirements
### Requirement: ML inference helpers MUST use established library terminology when available
The project MUST use established terminology from official library documentation for helper names when a clear standard term exists for the same operation.

#### Scenario: Diffusers pipeline loading helper naming
- **WHEN** code wraps `AutoPipelineForText2Image` / `AutoPipelineForImage2Image` / `AutoPipelineForInpainting` with `from_pretrained`
- **THEN** helper names MUST explicitly express pipeline loading semantics (for example `load_*_pipeline*`) rather than ambiguous generic builder terms

#### Scenario: Runtime behavior remains unchanged after naming refactor
- **WHEN** helper names are changed to match standard terminology
- **THEN** functional behavior and output quality/safety outcomes MUST remain equivalent under the existing test suite

### Requirement: Test module naming MUST stay pytest-discoverable and unambiguous
Test files for naming-standard validation MUST follow pytest discovery conventions and avoid module name collisions in the repository test layout.

#### Scenario: Test file name follows pytest discovery convention
- **WHEN** a new test validates ML naming standardization
- **THEN** the file name MUST match `test_*.py` or `*_test.py`

#### Scenario: Test module basename collision is prevented
- **WHEN** tests are collected with default pytest import behavior
- **THEN** test module basenames MUST be unique or otherwise structured to avoid import-file mismatch errors

