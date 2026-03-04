## Why

OpenSpec公式ドキュメントの運用方針（`/opsx:*` または `openspec` CLIでartifactを進める）と、エージェント実装時の編集手段（Edit/apply_patch等）の関係が仕様上で明確でない。誤解を防ぐため、正しい運用をrequirementsとして固定する。

## What Changes

- OpenSpec artifact作成/進行はOpenSpecコマンド駆動で行うことを要件化する。
- 仕様追加・変更は `openspec/changes/<change>/specs/<capability>/spec.md` のdelta specで行い、`openspec/specs/` 直接更新を通常運用から除外することを明示する。
- delta specの本体spec反映は `/opsx:sync` または `/opsx:archive` に従うことを明示する。
- 実装前の `openspec status` / `openspec instructions apply` / `openspec validate` の確認運用を明記する。

## Capabilities

### New Capabilities
- `openspec-authoring-workflow`: OpenSpec artifact作成・delta spec運用・検証の正しい実行順序を定義する

### Modified Capabilities
- `engineering-standards`: OpenSpec運用ルールにコマンド駆動作成とdelta spec反映手順を追加する

## Impact

- Affected specs: `openspec/changes/clarify-openspec-authoring-workflow/specs/openspec-authoring-workflow/spec.md`, `openspec/changes/clarify-openspec-authoring-workflow/specs/engineering-standards/spec.md`
- Process impact: OpenSpec artifact作成の運用が明文化される
- No runtime code behavior changes
