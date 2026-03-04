## 1. OpenSpec Alignment

- [ ] 1.1 `openspec status --change "define-archive-governance-best-practices"` と `openspec instructions apply --change "define-archive-governance-best-practices"` を実行し、artifact状態を確認する
- [ ] 1.2 `openspec validate --changes --strict --json` を実行し、artifact整合性を確認する

## 2. Archive Governance Specification

- [ ] 2.1 `openspec-archive-governance` capability に precheck / option制限 / multi-change順序要件を定義する
- [ ] 2.2 `openspec-authoring-workflow` capability に標準archiveシーケンス要件を追加する

## 3. Operational Application

- [ ] 3.1 完了済みchangeに対して `openspec archive <change> --yes` を順次実行する
- [ ] 3.2 各archive後に `openspec validate --changes --strict --json` を実行し、結果を確認する
