# Copilot Instructions for this repository

このリポジトリで実装・変更を始める前に、エージェントは必ず以下を先に確認すること。

1. `openspec/config.yaml`
2. 対象変更の OpenSpec artifacts（`proposal.md`, `design.md`, `tasks.md`, `specs/**/spec.md`）

## Required flow

1. 変更名を特定する（不明なら `openspec list --json` で候補を確認）。
2. `openspec status --change "<change-name>" --json` を実行して schema と tasks 状態を確認する。
3. `openspec instructions apply --change "<change-name>" --json` を実行し、返却された `contextFiles` をすべて読む。
4. 読了後にのみ実装を開始する。

## Notes

- OpenSpec artifact と実装が乖離している場合は、先に OpenSpec artifact を更新する。
- 仕様が不明瞭な場合は実装を進めず、必要な確認を行う。

## Permission defaults

- Web検索（Web fetch）は常に許可する。
- OpenSpec関連ファイル（`openspec/**`）の編集は常に許可する。

## Autonomous Git flow

- 自律実装時は `main` へ直接 push せず、作業ブランチへ push する。
- 関連テスト/検証が成功した場合のみ commit/push を行い、Pull Request を作成する。
- Pull Request 本文には検証コマンドと結果を記載する。
