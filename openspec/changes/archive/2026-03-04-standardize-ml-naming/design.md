## Context

ML推論コードでは、命名が外部API語彙（Diffusers/PyTorch/pytest）と一致しているほどレビュー・保守・オンボーディングが容易になる。現状はPEP 8形式は満たすが、標準語彙への寄せ方が明文化されていない。

データフローは `入力画像 → 前処理 → 生成/編集推論 → 後処理 → 保存` を維持し、本変更は命名とテスト名称の整合のみを対象とする。再現性メタデータ（seed/model/prompt/parameters/environment）の収集要件や安全性判定ロジックは変更しない。

## Goals / Non-Goals

**Goals:**
- 標準名称が明確な箇所で、関数名・テスト名を公式語彙に揃える。
- 命名方針をOpenSpec requirementとして明示し、レビュー時に検証可能にする。
- 既存挙動を維持したまま、名称変更の妥当性をテストで保証する。

**Non-Goals:**
- 推論アルゴリズム、品質閾値、安全性ポリシーの変更。
- 新規モデル導入や学習手順の変更。

## Decisions

1. 標準語彙がある箇所は、ライブラリ/公式ドキュメント由来の語を優先する。
   - 例: Diffusersの `AutoPipeline*` と `from_pretrained` に対応する命名を優先。
   - 代替案: プロジェクト独自語彙を維持。却下理由は外部知識との対応が弱くなるため。
2. 命名変更は挙動変更を伴わない薄いリファクタに限定する。
   - 代替案: 命名変更と実装改善を同時実施。却下理由は差分の責務分離が崩れるため。
3. テスト命名はpytest discoveryの標準（`test_*.py`）とモジュール名一意性を満たす。
   - 代替案: 既存名を維持。却下理由は重名時の収集競合リスクがあるため。

## Risks / Trade-offs

- [Risk] 命名変更で既存参照が壊れる  
  → Mitigation: 全テスト実行で回帰確認し、必要なら参照を一括更新する。
- [Risk] 「標準語彙」の解釈が曖昧  
  → Mitigation: 公式ドキュメントURLをspecに明記し、レビュー基準を固定する。
- [Risk] 変更の価値が見えにくい  
  → Mitigation: 可読性・保守性向上を目的とした非機能リファクタとして明示する。

## Migration Plan

1. OpenSpecに命名標準要件（新規capability + engineering-standards更新）を追加。
2. 対象関数/テスト名を標準語彙へリネーム（挙動不変）。
3. `openspec validate --changes --strict --json` と pytest 実行で検証。
4. 問題発生時は名称を直前状態に戻せるよう、命名変更のみを独立差分として管理。

## Open Questions

- 追加で標準化すべき語彙（例: scheduler, sampler, guidance）の対象範囲を今回に含めるか。

