## 1. OpenSpec alignment

- [x] 1.1 `openspec validate --changes --strict --json` と `openspec status --change "standardize-ml-naming" --json` を実行して、実装前整合性を確認する
- [x] 1.2 `openspec instructions apply --change "standardize-ml-naming" --json` で contextFiles を確認し、対象ファイルを確定する

## 2. Standard naming implementation

- [x] 2.1 Diffusersロード関連の関数名を公式語彙ベース（load/pretrained/pipeline）へ揃え、参照箇所を更新する
- [x] 2.2 pytest発見規約に沿って命名標準テストのファイル名・テスト名を一意かつ明確に更新する

## 3. Verification and evidence

- [x] 3.1 `openspec validate --changes --strict --json` と `PYTHONPATH=/Users/ryoma/Desktop/study/image uv run --project /Users/ryoma/Desktop/study/image --python 3.12 -- pytest -q` を実行し、成功を確認する
- [x] 3.2 変更差分に「命名変更のみで挙動不変」であることを確認し、検証コマンドと結果を記録する
