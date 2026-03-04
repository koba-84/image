## Context

OpenSpec CLI には `archive` コマンドとオプションがあるが、現行specでは「いつ」「どの条件で」使うかが不足している。特に複数changeの同時完了時に、順序やコンフリクト検知の統一ルールが不足している。

## Goals / Non-Goals

**Goals:**
- archive 実行前の必須チェックを統一する
- 危険オプションの利用条件を明示する
- 複数changeのarchive順序と衝突対応を明確化する
- archive後の検証とログ記録要件を定義する

**Non-Goals:**
- OpenSpec CLI自体の実装変更
- 既存changeの仕様内容の再設計
- GitHub保護ルールの設定変更

## Decisions

1. archive前に `openspec status --change <name>` と `openspec validate --changes --strict` を必須化する。
- 理由: 完了状態と仕様整合性を機械的に確認するため。

2. `--skip-specs` は doc/tooling-only change のみ許可し、理由記録を必須化する。
- 理由: 意図せぬ spec 未反映を防ぐため。

3. `--no-validate` は原則禁止とし、例外時は明示理由と再検証を必須化する。
- 理由: 破損状態の持ち込みリスクが高いため。

4. 複数change archive時は古いchangeから順に適用し、都度 validate する。
- 理由: spec衝突時の原因特定を容易にするため。

## Risks / Trade-offs

- [Risk] チェック手順が増えて作業時間が伸びる → [Mitigation] コマンドを固定しテンプレ化する
- [Risk] 例外処理が硬直化する → [Mitigation] 例外時の条件と記録要件を明示して運用可能性を残す

## Migration Plan

1. 本changeのdelta specを作成し、`openspec validate --changes --strict --json` を通過させる。
2. 完了済みchangeに対して新ルールで archive を実行し、結果を記録する。
3. 本changeを archive して main specs へ反映する。
