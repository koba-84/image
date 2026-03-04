## Why

画像生成・画像編集AIの検証を継続的に行うにあたり、実験再現性・安全性・レビュー品質を担保する共通ルールが未定義である。初期段階でコーディング規約とGit運用規約を仕様化し、以後の変更の品質を安定化させる必要がある。

## What Changes

- OpenSpecのプロジェクトコンテキストに、画像AI検証向けコーディング規約とGit規約を追加する
- 規約を仕様(Requirements/Scenarios)として明文化し、遵守確認可能な受け入れ条件を定義する
- 以降の提案・設計・タスクで規約を参照できるよう、OpenSpec artifactルールを整備する
- エージェントの自律作業を「ブランチpush + PR作成」前提で運用するため、最小権限トークン/PR証跡要件を追加する

## Capabilities

### New Capabilities
- `engineering-standards`: 画像AI検証プロジェクトにおけるコーディング規約・Git運用規約・運用上の受け入れ条件を定義する

### Modified Capabilities
- (none)

## Impact

- Affected area: `openspec/config.yaml`, `openspec/changes/archive/2026-03-04-establish-engineering-standards/*`
- Process impact: 仕様/設計/実装タスク作成時に規約準拠が標準フローになる
- Risk reduction: 再現不能実験、曖昧なコミット履歴、レビュー漏れ、過剰権限トークン運用を低減する
