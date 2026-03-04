ni## 1. OpenSpec alignment

- [x] 1.1 `openspec status --change "clarify-openspec-authoring-workflow" --json` と `openspec instructions apply --change "clarify-openspec-authoring-workflow" --json` を確認する
- [x] 1.2 公式ドキュメント（getting-started/commands/cli）参照をspecへ記載する

## 2. Spec updates

- [x] 2.1 `openspec-authoring-workflow` capability specを追加し、artifact作成がコマンド駆動であることを定義する
- [x] 2.2 `engineering-standards` に実装前チェック（status/instructions apply/validate）を追加する
- [x] 2.3 公式手順に合わせて「delta spec作成→sync/archiveで本体spec反映」を要件へ追加する

## 3. Validation

- [x] 3.1 `openspec validate --changes --strict --json` を実行して整合性を確認する
- [x] 3.2 変更がartifact運用ルールのみであることを確認する
- [x] 3.3 `openspec status --change "clarify-openspec-authoring-workflow" --json` でtasks完了状態を確認する
