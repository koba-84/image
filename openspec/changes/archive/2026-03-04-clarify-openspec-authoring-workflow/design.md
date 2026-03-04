## Context

OpenSpec公式ドキュメントは、artifactの進行を `/opsx:*` または `openspec` CLI コマンドで管理し、仕様変更は `openspec/changes/<change>/specs/<capability>/spec.md` のdelta specとして記述して、`/opsx:sync` または `/opsx:archive` で `openspec/specs/` へ反映する運用を前提としている。

## Goals / Non-Goals

**Goals:**
- artifact作成/進行の正規ルートをOpenSpecコマンド駆動として明示する。
- 仕様追加・変更はchange配下delta specで行うことを明示する。
- 本体spec反映はsync/archive経由で行うことを明示する。
- 実装前確認（status / instructions apply / validate）を運用ルールとして固定する。

**Non-Goals:**
- アプリケーション実装コードの変更。
- OpenSpec CLI自体の機能追加。

## Decisions

1. artifactの新規作成/進行はOpenSpecコマンド（`/opsx:*` or `openspec` CLI）を正規手段とする。  
   - 代替案: 任意ファイルを先に手作業作成。  
   - 却下理由: 依存順序とstatus追跡が崩れるため。
2. 仕様変更はactive change配下のdelta specで記述し、`openspec/specs/` へはsync/archiveで反映する。  
   - 代替案: `openspec/specs/` を直接編集。  
   - 却下理由: 変更履歴と差分意図（ADDED/MODIFIED/REMOVED）追跡が崩れるため。
3. 実装前に `openspec status` / `openspec instructions apply` / `openspec validate` を確認する。  
   - 代替案: `validate` のみ。  
   - 却下理由: artifact依存関係やcontext取りこぼしを防げないため。

## Risks / Trade-offs

- [Risk] 手作業でartifactを先に作る運用が残る  
  → Mitigation: requirementで明示し、レビュー時に確認する。
- [Risk] 本体spec直接編集が再発する  
  → Mitigation: 「delta spec→sync/archive反映」をspecに明記する。

## Migration Plan

1. 新規capabilityとengineering-standards修正のdelta specを追加。
2. tasksに確認手順を定義。
3. `openspec validate --changes --strict --json` で整合確認。

## Open Questions

- 将来的にこの運用確認をCIで自動判定するか。
