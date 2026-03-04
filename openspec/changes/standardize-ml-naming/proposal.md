## Why

既存コードには「意味は通るが業界標準語彙に寄っていない」関数名が残っており、MLエンジニアが外部ドキュメント（Diffusers/PyTorch/pytest）と対応付けて理解しづらい。標準的に定着した名称がある箇所はそれに寄せる方針を仕様として固定する。

## What Changes

- ML/推論系の命名規約を「PEP 8の形式 + 公式API語彙への整合」に更新する。
- Diffusersのロード処理や推論実行など、標準語彙が明確な関数名を優先する要求を追加する。
- 既存の曖昧名を段階的に標準語彙へ置換し、テスト名も同一方針で更新する。
- PR時に「名称変更が公式語彙と整合しているか」を確認する運用を追加する。

## Capabilities

### New Capabilities
- `ml-naming-standardization`: MLコードにおける標準語彙ベースの命名要求（関数/テスト）を定義する

### Modified Capabilities
- `engineering-standards`: 命名規約に「標準名が存在する場合はそれを優先する」要件を追加する

## Impact

- Affected code: `image_ai/pipeline_runner.py`, `image_ai/cli.py`, `tests/unit/*`
- Affected specs: `openspec/changes/standardize-ml-naming/specs/ml-naming-standardization/spec.md`, `openspec/changes/standardize-ml-naming/specs/engineering-standards/spec.md`
- Risk: 名称変更で既存参照が壊れる可能性（テストで検証）
- Safety: 命名変更のみで推論ロジック・安全性判定ロジック自体は変更しない

