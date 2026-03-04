## Why

OpenSpec artifacts currently allow references that conflict with current operating rules, including references to `.copilot/session` usage and outdated references to prior archived changes. This causes operational drift and confusion in future changes.

## What Changes

- Add explicit OpenSpec maintenance requirements to avoid `.copilot/session` operational dependency in project artifacts.
- Add cleanup requirements to remove unnecessary references to prior/archived changes from active OpenSpec artifacts.
- Define verification tasks so future changes keep references minimal and current.

## Capabilities

### Modified Capabilities
- `engineering-standards`: add OpenSpec artifact hygiene requirements for session-path references and stale historical references.

## Impact

- Affected specs: `openspec/changes/add-openspec-maintenance-rules/specs/engineering-standards/spec.md`
- Affected process: OpenSpec artifact authoring/review for active changes

