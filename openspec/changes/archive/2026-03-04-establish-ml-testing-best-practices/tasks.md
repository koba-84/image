## 1. OpenSpec Alignment

- [x] 1.1 `openspec validate --changes --strict --json` と `openspec status --change "establish-ml-testing-best-practices" --json` を実行し、実装開始前の整合性ログを残す
- [x] 1.2 `openspec instructions apply --change "establish-ml-testing-best-practices" --json` の `contextFiles` を確認し、実装対象と除外対象を明確化する

## 2. Test Architecture and Markers

- [x] 2.1 既存 `tests/` を unit / integration / regression / safety に分類し、pytest marker方針を実装する
- [x] 2.2 PR必須スイート（高速）と拡張スイート（重い回帰）の実行コマンドを定義し、READMEまたはテスト実行手順に反映する

## 3. Reproducibility Coverage

- [x] 3.1 主要推論テストで seed・model id/version・prompt/edit instruction・推論パラメータ・入力ID・実行環境を記録する仕組みを実装する
- [x] 3.2 同一条件再実行テストを追加し、再現性許容差を超えた場合に失敗する検証を実装する

## 4. Quality and Safety Regression

- [x] 4.1 画像品質回帰テストを追加し、ピクセル系指標＋知覚系指標の閾値判定を自動化する
- [x] 4.2 有害生成・著作権配慮・個人情報配慮の安全性ケースをテストデータとして整備し、期待挙動を検証する

## 5. Failure Handling and Evidence

- [x] 5.1 一時障害の限定リトライと決定的失敗の即時停止をCIテストランナーに実装し、各試行ログを保存する
- [x] 5.2 コミット/PR時に実行した検証コマンドと結果を変更記録へ残す運用を整備する

## 6. Additional Operations Tasks

- [x] 6.1 OpenSpecファイル編集時に `openspec status/instructions apply` を必ず実行する運用を明文化し、指示ファイルへ反映する
- [x] 6.2 AGENTS/Copilot instructions を簡素化し、OpenSpecを主ルートとする運用へ整理する
