from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Sequence


TRANSIENT_SIGNATURES = (
    "timeout",
    "temporarily unavailable",
    "connection reset",
    "network is unreachable",
)


def is_transient_failure(stderr: str, stdout: str) -> bool:
    merged = f"{stdout}\n{stderr}".lower()
    return any(sig in merged for sig in TRANSIENT_SIGNATURES)


def run_command(command: Sequence[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=False, capture_output=True, text=True)


def run_pytest_with_retry(
    command: Sequence[str], *, max_retries: int, log_path: Path
) -> int:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    attempt = 0
    while True:
        attempt += 1
        result = run_command(command)
        transient = is_transient_failure(result.stderr, result.stdout)
        entry = {
            "attempt": attempt,
            "returncode": result.returncode,
            "transient": transient,
        }
        with log_path.open("a", encoding="utf-8") as fp:
            fp.write(json.dumps(entry, ensure_ascii=False) + "\n")

        if result.returncode == 0:
            return 0
        if not transient:
            return result.returncode
        if attempt > max_retries:
            return result.returncode
