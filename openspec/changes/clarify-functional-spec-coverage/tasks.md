## 1. OpenSpec Alignment

- [x] 1.1 `openspec status --change "clarify-functional-spec-coverage" --json` と `openspec instructions apply --change "clarify-functional-spec-coverage" --json` を実行し、artifact依存関係と適用可能状態を確認する
- [x] 1.2 `openspec validate --changes --strict --json` を実行し、change artifacts の整合性を確認する

## 2. Functional Specification Coverage

- [x] 2.1 `image-generation-workflow` spec に mode別入力契約（text2img/img2img/inpaint）を定義する
- [x] 2.2 出力成果物（画像＋メタデータ）の必須要件と記録項目を定義する
- [x] 2.3 入力不足・実行失敗時のログ/エラーハンドリング要件を定義する

## 3. Authoring Clarity

- [x] 3.1 `openspec-authoring-workflow` spec に Purposeの非プレースホルダ要件を追加する
- [x] 3.2 `openspec/specs/openspec-authoring-workflow/spec.md` の Purpose更新を行うための実施手順（sync/archive）を明文化する
