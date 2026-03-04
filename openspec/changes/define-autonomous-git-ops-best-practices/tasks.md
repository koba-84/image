## 1. OpenSpec Alignment

- [x] 1.1 `openspec status --change "define-autonomous-git-ops-best-practices" --json` と `openspec instructions apply --change "define-autonomous-git-ops-best-practices" --json` を実行し、artifact依存関係と適用可能状態を確認する
- [x] 1.2 `openspec validate --changes --strict --json` を実行し、active change artifacts が整合していることを確認する

## 2. Autonomous Git Workflow Requirements

- [x] 2.1 `engineering-standards` delta spec に clean-working-tree checkpoint (`git status --short` empty) 要件を定義する
- [x] 2.2 commit粒度（1コミット1目的）と Conventional Commits 準拠要件を定義する
- [x] 2.3 protected branch / PR 経由統合と push前同期の要件を定義する

## 3. Operational Application

- [x] 3.1 現在の未コミット差分を確認し、論理単位で分割または整理してコミットする
- [x] 3.2 最終的に `git status --short` が空であることを確認し、結果を作業ログに残す
