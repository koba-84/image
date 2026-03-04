## Why

現状のOpenSpecは開発プロセス要件は明確だが、画像生成/編集機能の振る舞い要件が薄く、受け入れ基準が分散している。あわせて `openspec-authoring-workflow` の意図を要件として明文化し、仕様の読みやすさを高める。

## What Changes

- 画像生成/編集の機能仕様を新規 capability として定義する
- 実行モード別の入力/出力契約、メタデータ記録、失敗時挙動を要件化する
- OpenSpec authoring workflow に「仕様文書の目的を明示する」要件を追加する

## Capabilities

### New Capabilities
- `image-generation-workflow`: text2img/img2img/inpaint の実行契約、再現性、出力保証を定義する

### Modified Capabilities
- `openspec-authoring-workflow`: 仕様文書の目的をプレースホルダなしで明示する要件を追加する

## Impact

- Affected specs:
  - `openspec/changes/clarify-functional-spec-coverage/specs/image-generation-workflow/spec.md`
  - `openspec/changes/clarify-functional-spec-coverage/specs/openspec-authoring-workflow/spec.md`
- Affected process: 機能仕様レビュー時の受け入れ判断基準、OpenSpec文書品質チェック
