## Why

Current Git operations are not autonomous enough to keep the working tree clean, and a large amount of uncommitted work accumulates. We need explicit, web-backed workflow rules that force small, reviewable units of work and require zero-pending state at defined checkpoints.

## What Changes

- Add enforceable autonomous Git operations requirements for:
  - short-lived branch workflow with PR-based integration
  - branch protection expectations for `main`
  - small, structured commits with Conventional Commits format
  - mandatory "working tree clean" checks before push/PR completion
  - explicit autonomous push success verification and PR creation/update after push
- Define task-level verification so the team can repeatedly apply this workflow and avoid uncommitted backlog.

## Web References

- GitHub Docs: About pull requests (`https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests`)
- GitHub Docs: About protected branches (`https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches`)
- Conventional Commits 1.0.0 (`https://www.conventionalcommits.org/en/v1.0.0/`)
- Atlassian Git Workflows (`https://www.atlassian.com/git/tutorials/comparing-workflows`)

## Capabilities

### Modified Capabilities
- `engineering-standards`: strengthen autonomous Git execution rules to reduce uncommitted drift and enforce clean checkpoints.

## Impact

- Affected specs: `openspec/changes/define-autonomous-git-ops-best-practices/specs/engineering-standards/spec.md`
- Affected process: commit/push/PR lifecycle and day-to-day local Git hygiene
