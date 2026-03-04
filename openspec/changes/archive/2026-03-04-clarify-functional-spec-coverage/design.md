## Context

リポジトリでは推論パイプライン実装と設定が先行し、OpenSpec上の機能要求が十分に分解されていない。結果としてレビュー時に「どこまでを満たせば完了か」が曖昧になりやすい。

## Goals / Non-Goals

**Goals:**
- モード別の必須入力と出力保証を仕様化する
- 再現性のためのメタデータ要件を仕様化する
- 実行失敗時のログ・終了条件を仕様化する
- OpenSpec authoring spec に目的明示ルールを追加する

**Non-Goals:**
- 推論アルゴリズムやモデル選定ロジックの変更
- 実装コードの即時改修
- CIジョブ構成の変更

## Decisions

1. 機能仕様は新規 capability `image-generation-workflow` に分離する。
- 理由: プロセス規約(`engineering-standards`)と機能契約を分離し、参照しやすくするため。
- 代替案: `engineering-standards` へ追記。却下理由は、運用規約と機能要件が混在し可読性が下がるため。

2. 再現性は「出力時のメタデータ記録」を必須要件として定義する。
- 理由: 実装差分よりも再実行可能性の保証が重要なため。
- 代替案: テスト運用ドキュメントのみに記載。却下理由は、規範力が弱く受け入れ基準として機能しないため。

3. `openspec-authoring-workflow` には目的のプレースホルダ禁止を追加する。
- 理由: 既存の `Purpose: TBD` 問題を再発防止し、仕様理解コストを下げるため。
- 代替案: レビュー時の口頭運用。却下理由は、運用依存で継続性が低いため。

## Risks / Trade-offs

- [Risk] 要件を増やしすぎると仕様が重くなる → [Mitigation] モード入出力・再現性・失敗時挙動の最小セットに限定する
- [Risk] 既存実装との差異が出る可能性 → [Mitigation] 仕様追加後に差分レビュータスクを明示し、段階的に合わせる

## Migration Plan

1. 本changeをレビューし、`openspec validate --changes --strict --json` を通過させる。
2. `openspec/changes/clarify-functional-spec-coverage/specs/` の delta spec を sync/archive フローで `openspec/specs/` に反映する。
3. 反映時に `openspec/specs/openspec-authoring-workflow/spec.md` の Purpose を具体文へ更新し、`TBD` を残さない。
