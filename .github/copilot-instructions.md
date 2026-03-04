# Copilot Instructions (OpenSpec-first)

このリポジトリは **OpenSpecを正本** とする。仕様変更・設計・実装計画は `openspec/changes/**` のみで管理する。

## 必須フロー（実装前）

1. 変更名を決める（不明なら `openspec list --json`）。
2. `openspec status --change "<change-name>" --json`
3. `openspec instructions apply --change "<change-name>" --json`
4. 返却された `contextFiles` をすべて読む。
5. ここまで完了後に実装を開始する。

## OpenSpec編集時のルール

- `openspec/` 配下の編集では、編集前に必ず上記コマンドを実行して結果を確認する。
- 仕様の衝突時は OpenSpec artifacts（`openspec/specs/**/spec.md` と active change）を優先する。
- `.copilot/plan.md` を作業ルートとして使わない。

## Python / Test 実行

- Pythonは3.12系を使用する。
- pytestは以下で固定実行する:  
  `PYTHONPATH=/Users/ryoma/Desktop/study/image uv run --project /Users/ryoma/Desktop/study/image --python 3.12 -- pytest`

## Git運用

- `main` へ直接pushしない。PR経由で統合する。
- 仕様変更は実装より先にOpenSpec artifactsを更新する。
