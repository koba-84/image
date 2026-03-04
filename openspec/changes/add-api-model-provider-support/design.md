## Context

既存CLIは `load_pipeline_for_mode -> configure_diffusers_pipeline -> run_inference` の流れでDiffusersパイプラインを利用する。APIモデルの追加では同じ入口を維持しつつ、内部でバックエンドを分岐する必要がある。

## Goals / Non-Goals

**Goals:**
- `model_id` から local/api を判定する
- `openai:<model>` で text2img 実行を可能にする
- APIキー未設定時に明確なエラーを返す
- 実行メタデータに backend/provider を残す

**Non-Goals:**
- 全APIプロバイダ一括対応
- API版 img2img/inpaint の実装
- 高度なリトライ/スロットリング実装

## Decisions

1. `model_id` の接頭辞でバックエンドを判定する（`openai:` は API、それ以外は local）。
- 理由: 既存設定との互換性を保ちながら実装変更を最小化できるため。

2. APIクライアントは `pipeline_runner.py` に小さな内部クラスとして実装し、CLIの呼び出し順序は維持する。
- 理由: 既存コードの責務分割を大きく崩さないため。

3. API実行は初期段階で `text2img` のみ対応し、他modeは明示的にNotImplementedエラーを返す。
- 理由: 要件を満たしつつ破壊的な複雑化を避けるため。

## Risks / Trade-offs

- [Risk] API仕様差分でレスポンス形式が揺れる → [Mitigation] `b64_json` / `url` の両形式を受ける実装にする
- [Risk] 環境変数依存で実行失敗しやすい → [Mitigation] 不足時に必須env名を含むエラーを返す

## Migration Plan

1. delta spec と tasks を追加し `openspec validate --changes --strict` を通す。
2. 実装後にユニットテストを追加し、API分岐の回帰を確認する。
3. 将来のprovider追加は `provider:model` 形式に追記して拡張する。
