## Context

The repository already requires PR-based integration and conventional commit formatting, but it does not explicitly define autonomous guardrails that prevent large uncommitted backlog from persisting. We need deterministic checkpoints that agents can execute without manual interpretation.

## Decisions

1. Keep PR-first integration and codify branch protection expectations as required guardrails.
   - Rationale: GitHub protected branch rules enforce review/status gates and prevent direct or unsafe updates to key branches.
2. Require granular, conventional-commit-based local commits during autonomous execution.
   - Rationale: Conventional Commits provides machine-readable history and makes verification/reporting easier.
3. Require explicit clean-working-tree checks at key lifecycle points.
   - Rationale: `git status --short` empty state before push/PR close prevents hidden local leftovers.
4. Require pre-push synchronization and conflict resolution workflow.
   - Rationale: Workflow guidance from common Git team practices reduces integration surprises.
5. Require autonomous push success verification and immediate PR creation/update.
   - Rationale: autonomous execution must complete publish/review handoff, not stop at local commits.

## Risks / Trade-offs

- More frequent commits/checks may increase short-term overhead.
- Strict clean-check gates can block progress when unrelated local changes exist, requiring additional staging discipline.

## Migration Plan

1. Add delta requirements in the active change spec for autonomous Git operations and clean-tree checkpoints.
2. Add concrete tasks to operationalize required checks and evidence.
3. Validate OpenSpec artifacts and then apply workflow by creating commits, pushing the branch, and creating/updating PR evidence.

## References

- https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- https://www.conventionalcommits.org/en/v1.0.0/
- https://www.atlassian.com/git/tutorials/comparing-workflows
