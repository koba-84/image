from __future__ import annotations

import json
from pathlib import Path
import unittest

import pytest

pytestmark = pytest.mark.unit


class CopilotPermissionConfigTest(unittest.TestCase):
    def test_copilot_config_has_trusted_folder_only(self) -> None:
        repo_root = Path(__file__).resolve().parents[2]
        config_path = repo_root / ".copilot" / "config.json"

        raw = json.loads(config_path.read_text(encoding="utf-8"))
        trusted_folders = raw.get("trusted_folders", [])

        self.assertIn(str(repo_root), trusted_folders)
        self.assertNotIn("allowed_urls", raw)
        self.assertNotIn("allowed_tools", raw)


if __name__ == "__main__":
    unittest.main()
