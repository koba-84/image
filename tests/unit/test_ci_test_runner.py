from __future__ import annotations

import json
from pathlib import Path

import pytest

from image_ai import ci_test_runner

pytestmark = pytest.mark.unit


class _Completed:
    def __init__(self, returncode: int, stdout: str = "", stderr: str = "") -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_run_pytest_with_retry_retries_transient_errors(monkeypatch, tmp_path) -> None:
    sequence = iter(
        [
            _Completed(1, stderr="Timeout while contacting package index"),
            _Completed(0, stdout="ok"),
        ]
    )
    monkeypatch.setattr(ci_test_runner, "run_command", lambda _: next(sequence))
    log_path = tmp_path / "ci" / "attempts.jsonl"

    code = ci_test_runner.run_pytest_with_retry(
        ["pytest", "-q"], max_retries=1, log_path=log_path
    )
    entries = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]

    assert code == 0
    assert len(entries) == 2
    assert entries[0]["transient"] is True
    assert entries[1]["returncode"] == 0


def test_run_pytest_with_retry_fails_fast_for_deterministic_errors(
    monkeypatch, tmp_path
) -> None:
    monkeypatch.setattr(
        ci_test_runner,
        "run_command",
        lambda _: _Completed(1, stderr="AssertionError: regression detected"),
    )
    log_path = tmp_path / "ci" / "attempts.jsonl"

    code = ci_test_runner.run_pytest_with_retry(
        ["pytest", "-q"], max_retries=3, log_path=log_path
    )
    entries = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]

    assert code == 1
    assert len(entries) == 1
    assert entries[0]["transient"] is False
