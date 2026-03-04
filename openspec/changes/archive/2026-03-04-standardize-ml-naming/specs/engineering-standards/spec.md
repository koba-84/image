## MODIFIED Requirements

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

