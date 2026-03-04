## ADDED Requirements

### Requirement: Test pyramid SHALL cover ML image editing risks
The project MUST define and maintain a three-layer test strategy for image editing pipelines: unit, integration, and regression.

#### Scenario: Unit tests validate deterministic helper behavior
- **WHEN** preprocessing, postprocessing, or utility logic is changed
- **THEN** unit tests MUST verify deterministic behavior for fixed inputs and fixed seeds

#### Scenario: Integration tests validate end-to-end pipeline contract
- **WHEN** input image is processed through preprocessing, generation/editing, postprocessing, and save
- **THEN** integration tests MUST assert expected output schema, dimensions, color space, and metadata completeness

#### Scenario: Regression tests detect quality degradation
- **WHEN** model or inference-related code changes
- **THEN** regression tests MUST compare outputs against approved baselines using at least one pixel-level metric and one perceptual metric with explicit thresholds

### Requirement: Reproducibility metadata MUST be recorded and testable
Every ML inference test run MUST persist reproducibility metadata sufficient for rerun on the same environment.

#### Scenario: Metadata fields are complete
- **WHEN** an ML inference test is executed
- **THEN** test artifacts MUST include seed, model identifier/version, prompt or edit instruction, key inference parameters, input data identifier, and runtime environment information

#### Scenario: Re-run consistency is verified
- **WHEN** the same metadata and inputs are replayed on the same runtime stack
- **THEN** the produced output metrics MUST stay within the configured reproducibility tolerance

### Requirement: Safety regression tests MUST cover harmful and sensitive cases
The test suite MUST include safety-focused cases for harmful content, copyright-sensitive inputs, and personal data handling.

#### Scenario: Harmful-content handling is enforced
- **WHEN** a safety test case triggers harmful content criteria
- **THEN** the system MUST follow the configured mitigation behavior and record a traceable reason in test logs

#### Scenario: Sensitive-data handling is enforced
- **WHEN** a test input includes personal or copyright-sensitive material markers
- **THEN** the pipeline MUST apply the defined policy behavior and produce auditable evidence in test output

### Requirement: CI execution tiers MUST balance speed and coverage
The project MUST separate mandatory fast checks from heavy regression checks.

#### Scenario: Pull request gate runs fast mandatory tests
- **WHEN** a pull request is opened or updated
- **THEN** CI MUST run unit and selected integration tests as required status checks

#### Scenario: Extended suite runs on scheduled or release gates
- **WHEN** scheduled validation or release-candidate validation is triggered
- **THEN** CI MUST execute full regression and safety suites and publish metric summaries

### Requirement: Test failure handling MUST be explicit and actionable
The project MUST define retry rules, logging requirements, and interruption criteria for test execution failures.

#### Scenario: Transient failures are retried under policy
- **WHEN** a test fails with a known transient infrastructure signature
- **THEN** the runner MUST retry only within a bounded retry policy and preserve logs of each attempt

#### Scenario: Deterministic failures stop the pipeline
- **WHEN** failure indicates deterministic quality, reproducibility, or safety regression
- **THEN** CI MUST fail the job without silent fallback and require explicit remediation before merge
