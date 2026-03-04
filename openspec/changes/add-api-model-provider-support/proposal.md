## Why

現在の実行経路はDiffusers前提で、`model_registry.json` に列挙済みの closed(API) モデルを実行に使えない。APIベースモデルを同じ実行フローで扱えるようにして、self-hostモデルとの比較検証を可能にする。

## What Changes

- `model_id` 文字列から実行バックエンド（local / api）を自動判定する
- `openai:<model>` / `google:<model>` / `ideogram:<model>` 形式の API モデルを text2img で実行可能にする
- API実行時の認証・エラー・メタデータ記録要件を追加する
- APIバックエンド向けのユニットテストを追加する

## Capabilities

### New Capabilities
- `api-model-provider-support`: APIモデルの判定・呼び出し・認証・エラー処理・記録要件を定義する

### Modified Capabilities
- `image-generation-workflow`: mode別実行契約に APIバックエンド選択と制約を追加する

## Impact

- Affected specs:
  - `openspec/changes/add-api-model-provider-support/specs/api-model-provider-support/spec.md`
  - `openspec/changes/add-api-model-provider-support/specs/image-generation-workflow/spec.md`
- Affected code:
  - `image_ai/pipeline_runner.py`
  - `image_ai/config.py`
  - `tests/unit/*`
