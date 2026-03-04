## 1. OpenSpec Alignment

- [x] 1.1 `openspec status --change add-api-model-provider-support` と `openspec instructions apply --change add-api-model-provider-support` を実行し、artifact状態を確認する
- [x] 1.2 `openspec validate --changes --strict --json` を実行し、change artifacts の整合性を確認する

## 2. Backend Routing Implementation

- [x] 2.1 `model_id` から local/api を判定するルーティング処理を追加する
- [x] 2.2 `openai:<model>` の text2img API実行経路を追加する
- [x] 2.3 APIキー不足・未対応modeのエラーを明示化する

## 3. Metadata and Tests

- [x] 3.1 メタデータへ backend/provider を追加する
- [x] 3.2 API分岐と未対応modeのユニットテストを追加する
- [x] 3.3 関連pytestを実行して結果を確認する
