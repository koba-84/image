## 1. OpenSpec maintenance scope

- [x] 1.1 `.copilot/session` 利用を前提にする記述を OpenSpec active change artifacts から排除する（完了条件: active changes 内で `.copilot/session` / `session-state` 参照が不要要件として残っていない）
- [x] 1.2 以前の change（特に archive 済み change）への不要参照を active artifacts から削除する（完了条件: active changes の proposal/design/tasks/spec で、実装判断に不要な過去change参照がない）

## 2. Verification

- [x] 2.1 `openspec validate --changes --strict --json` が成功することを確認する
- [x] 2.2 `openspec status --change "add-openspec-maintenance-rules" --json` と `openspec instructions apply --change "add-openspec-maintenance-rules" --json` で artifacts/contextFiles が正しく認識されることを確認する
