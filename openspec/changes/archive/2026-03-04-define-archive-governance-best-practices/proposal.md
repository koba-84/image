## Why

現在の仕様には archive 実行前後の必須チェックやオプション使用条件が明確に定義されておらず、運用が担当者依存になっている。OpenSpec公式の推奨フローに合わせて、再現可能な archive 運用要件を明文化する必要がある。

## What Changes

- archive 実行前チェック（status/tasks/validate）を必須化する
- `--skip-specs` と `--no-validate` の使用条件を限定する
- 複数changeをarchiveする際の順序と衝突解消の手順を定義する
- archive後に実施すべき検証と証跡要件を定義する

## Capabilities

### New Capabilities
- `openspec-archive-governance`: archive 実行の運用ガバナンスと検証手順を定義する

### Modified Capabilities
- `openspec-authoring-workflow`: archive 実行の必須チェックとオプション利用条件を要件として追加する

## Impact

- Affected specs:
  - `openspec/changes/define-archive-governance-best-practices/specs/openspec-archive-governance/spec.md`
  - `openspec/changes/define-archive-governance-best-practices/specs/openspec-authoring-workflow/spec.md`
- Affected process: change完了後のarchive手順、複数changeの統合順序、review時の証跡確認
