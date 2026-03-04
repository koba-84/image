# image-ai

画像生成・画像編集AIの検証リポジトリです。  
再現可能で安全な実験を素早く回すための最小構成を置いています。

## 実行環境（Colab前提）

- Google Colab（Jupyter Notebook）での実行を前提とします。
- Python 3.12（`pyproject.toml` の指定: `>=3.12,<3.13`）

## セットアップ

```python
!uv python pin 3.12
!uv run --python 3.12 -- python -V  # 3.12.x を確認
!uv sync
```

## 使い方

- 依存関係は `pyproject.toml` を正として `uv sync` で同期します。
- 実験ノートは `notebooks/run.ipynb` を起点に進めてください。
- 仕様・運用ルールは `openspec/config.yaml` を参照してください。
- コマンドは Notebook セルで `!` を付けて実行してください。

## テスト運用（OpenSpec準拠）

- PR必須（高速）:
  - `!cd /content/image && PYTHONPATH=. uv run --python 3.12 -- pytest -m "unit or integration" -q`
- 拡張（回帰・安全性含む）:
  - `!cd /content/image && PYTHONPATH=. uv run --python 3.12 -- pytest -m "unit or integration or regression or safety" -q`
- モデル実ロード確認（Colab GPUでの任意実行）:
  - `!cd /content/image && PYTHONPATH=. IMAGE_AI_ENABLE_REAL_MODEL_LOAD=1 uv run --python 3.12 -- pytest tests/integration/test_real_model_loading.py -q`
- CIリトライ付きランナー（transient failureのみ再試行）:
  - `!uv run --project /Users/ryoma/Desktop/study/image --python 3.12 -- python -c "from pathlib import Path; from image_ai.ci_test_runner import run_pytest_with_retry; raise SystemExit(run_pytest_with_retry(['pytest','-m','unit or integration','-q'], max_retries=1, log_path=Path('outputs/ci_attempts.jsonl')))"` 

## 低VRAM向け詳細コード

小さいVRAMで大きめのモデルを動かすためのCLIを追加しています。  
公式の uv Projects ガイドに合わせ、Colab の Notebook セル上で `!uv run` を標準にします。

### 実行仕様（uv準拠）

1. 依存同期: `!uv sync`  
2. コマンド実行: `!uv run -- python -m image_ai.cli ...`  

```python
!uv run -- python -m image_ai.cli mode=text2img model=sdxl_base \
  prompt="cinematic night city, ultra detailed" \
  output=outputs/sdxl_low_vram.png \
  steps=24 guidance_scale=6.0 \
  height=1024 width=1024
```

```python
!uv run -- python -m image_ai.cli mode=img2img model=sd15 \
  prompt="anime style, clean lineart" \
  image=./inputs/base.png \
  output=outputs/img2img.png \
  strength=0.55
```

```python
!uv run -- python -m image_ai.cli mode=inpaint model=sd_inpaint \
  prompt="replace with red flower bouquet" \
  image=./inputs/photo.png \
  mask_image=./inputs/mask.png \
  output=outputs/inpaint.png \
  strength=0.7
```

実行時に `output.json` が自動保存され、モデルID・seed・主要パラメータを記録します。

利用可能な `model` プリセット例:
- `sdxl_base`（既定）
- `sd15`
- `sd_inpaint`
- `sd35_large`（open-weight / high quality）
- `flux1_dev`（open-weight / high quality）
- `qwen_image_2512`（open-weight, 2025-12, Tech Report + 10k+ arena評価）
- `cogview4_6b`（open-weight, 公開ベンチマーク表あり）

モデル選定仕様:
- 選定条件は `latest公開` + `研究/ベンチ根拠明示` を必須とする（実装方式は固定しない）。
- 同一ファミリは原則1モデルのみ採用し、旧版は併記しない。
- open-weight と closed(API) を同一カタログで管理する。
- 不足検証は `!uv run -- python -m image_ai.model_audit` で実施し、上位候補との差分を確認する。

研究候補モデルID（同一ファミリ1モデル）:
- `Qwen/Qwen-Image-2512`
- `HiDream-ai/HiDream-I1-Full`
- `zai-org/CogView4-6B`
- `deepseek-ai/Janus-Pro-7B`
- `zai-org/GLM-4.1V-9B-Thinking`
- `black-forest-labs/FLUX.1-schnell`
- `ByteDance/SDXL-Lightning`
- `Tencent-Hunyuan/HunyuanDiT-v1.2-Diffusers`

closed(API) 検証候補:
- `openai:gpt-image-1`
- `google:imagen-3.0-generate-002` (Vertex AI)
- `ideogram:v2`

### ディレクトリ構成（役割分割）

- `notebooks/`: 実験ノートブック
- `inputs/`: 編集対象の入力画像・マスク画像
- `outputs/`: 生成画像と実行メタデータ（`.json`）
- `image_ai/cli.py`: エントリポイント（実行フロー）
- `image_ai/config.py`: Hydra実行設定定義
- `image_ai/conf/`: Hydra設定（`mode/` `memory/` `model/` `controlnet/` のconfig group）
- `image_ai/pipeline_runner.py`: パイプライン構築・低VRAM設定・推論・メタデータ保存

### メモリ最適化の参考

- Hugging Face Diffusers Memory Optimization  
  https://huggingface.co/docs/diffusers/optimization/memory
- Hugging Face Diffusers: Loading a pipeline (`from_pretrained`)  
  https://huggingface.co/docs/diffusers/main/en/using-diffusers/loading
- Hugging Face Diffusers Image-to-Image  
  https://huggingface.co/docs/diffusers/main/en/using-diffusers/img2img
- Hugging Face Diffusers Inpaint API  
  https://huggingface.co/docs/diffusers/main/en/api/pipelines/stable_diffusion/inpaint
- pytest usage and test selection  
  https://docs.pytest.org/en/stable/how-to/usage.html
- uv Projects Guide  
  https://docs.astral.sh/uv/guides/projects/
- Cookiecutter Data Science  
  https://cookiecutter-data-science.drivendata.org/
- PyPA src layout discussion  
  https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/
- DVC Project Structure  
  https://dvc.org/doc/user-guide/project-structure

## 補足

- Linux x86_64 向け依存（`bitsandbytes`, `xformers`）は環境マーカー付きです。
- エージェント向け指示は `.github/copilot-instructions.md` を正本とし、`AGENTS.md` はそのシンボリックリンクです。
