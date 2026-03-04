from __future__ import annotations

from pathlib import Path

import hydra
from omegaconf import DictConfig

from image_ai.config import build_runtime_config
from image_ai.pipeline_runner import (
    configure_diffusers_pipeline,
    load_pipeline_for_mode,
    run_inference,
    save_inference_metadata,
    select_torch_device,
    select_torch_dtype,
)


@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig) -> None:
    runtime_config = build_runtime_config(cfg)
    device = select_torch_device(runtime_config.device)
    dtype = select_torch_dtype(device)
    pipe = load_pipeline_for_mode(runtime_config.mode, runtime_config.model_id, dtype)
    configure_diffusers_pipeline(pipe, runtime_config, device)
    result = run_inference(pipe, runtime_config)

    output_path = Path(runtime_config.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.save(output_path)
    print(f"[INFO] image: {output_path}")
    print(
        f"[INFO] run: mode={runtime_config.mode} model={runtime_config.model_id} seed={runtime_config.seed} device={device} offload={runtime_config.offload}"
    )
    save_inference_metadata(runtime_config, device, dtype)


if __name__ == "__main__":
    main()
