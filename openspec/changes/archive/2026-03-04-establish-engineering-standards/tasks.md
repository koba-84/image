## 1. OpenSpec alignment

- [ ] 1.1 現行OpenSpec設定を更新し、コーディング規約/Git規約をcontextとrulesへ反映する（完了条件: `openspec instructions proposal --change establish-engineering-standards --json` で規約がcontext/rulesに表示される）
- [ ] 1.2 artifact ID整合性を確認し、schemaエラーが出ない状態にする（完了条件: instructions実行時にUnknown artifact IDエラーが出ない）

## 2. Specification formalization

- [ ] 2.1 規約をcapability specとして定義する（完了条件: `specs/engineering-standards/spec.md` にRequirements/Scenariosが存在する）
- [ ] 2.2 受け入れ条件に再現性・安全性・Git追跡性を含める（完了条件: 各観点をカバーするScenarioが最低1つある）

## 3. Verification

- [ ] 3.1 OpenSpec statusでtasks到達可能状態を確認する（完了条件: `openspec status --change establish-engineering-standards` でtasksが認識される）
- [ ] 3.2 差分確認を行い、本変更で追加したファイルのみをレビュー対象として整理する（完了条件: `git diff -- openspec/config.yaml openspec/changes/establish-engineering-standards` で確認可能）
- [ ] 3.3 自律PR運用要件を確認する（完了条件: spec/config上で「main以外へのpush」「PR本文の検証証跡」「最小権限認証」が確認できる）
