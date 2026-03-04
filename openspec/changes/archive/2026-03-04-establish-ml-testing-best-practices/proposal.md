## Why

画像生成・画像編集のML検証では、通常のユニットテストだけでは品質劣化や再現性崩れを検出しにくく、回帰に気づくまでの時間が長くなりやすい。  
PyTorch再現性ガイド（seed固定と非決定性要因の制御）および production ML testing の実務知見（テスト/監視の層別化）を反映した、測定可能なテスト基準をOpenSpecで明文化する。

## What Changes

- ML画像編集向けの新規 capability `ml-testing-practices` を追加し、テスト戦略を仕様化する。
- テスト階層（unit / integration / regression）ごとの必須観点を定義する。
- 再現性テスト要件（seed・モデルID・推論パラメータ・実行環境の記録と固定条件）を定義する。
- 画像品質回帰テスト要件（指標・しきい値・ゴールデンデータ更新手順）を定義する。
- 安全性テスト要件（有害/著作権/個人情報に関する入力ケースと期待挙動）を定義する。
- CIでの実行ルール（軽量必須スイートと重い検証スイートの分離）を定義する。

## Capabilities

### New Capabilities
- `ml-testing-practices`: 画像編集MLプロジェクトで再現性・品質・安全性を担保するためのテスト要件を定義する。

### Modified Capabilities
- なし

## Impact

- Affected specs: `openspec/changes/establish-ml-testing-best-practices/specs/ml-testing-practices/spec.md`
- Affected code/process: `tests/` 配下構成、pytestマーカー/実行コマンド、回帰用入力データ管理、CIテストジョブ分割
- Success indicators:
  - 仕様で定義した必須テストカテゴリが `tasks.md` に実装タスクとして網羅される
  - 回帰時に「再現性欠如」「品質劣化」「安全性逸脱」をそれぞれ検出可能な受け入れ条件が記述される
- Non-goals:
  - 新しい学習モデルの実装
  - 推論アルゴリズム自体の性能最適化
