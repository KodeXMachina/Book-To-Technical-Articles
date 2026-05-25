from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "qa_backwrite_log.py"


class QaBackwriteLogCliTest(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_log_dir_cannot_escape_project_root_even_in_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_cli(
                tmp,
                "--question",
                "路径测试",
                "--answer-summary",
                "测试",
                "--log-dir",
                "../../outside",
                "--dry-run",
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("log-dir", result.stderr)

    def test_chinese_question_entry_id_has_hash_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_cli(
                tmp,
                "--question",
                "为什么这里要区分对象生命周期和指针生命周期？",
                "--answer-summary",
                "测试",
                "--dry-run",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, re.compile(r"## \d{8}-\d{6}-question-[0-9a-f]{8}"))

    def test_zh_language_writes_chinese_headings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_cli(
                tmp,
                "--question",
                "为什么这里要区分对象生命周期和指针生命周期？",
                "--answer-summary",
                "测试",
                "--language",
                "zh",
                "--dry-run",
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("### 读者问题", result.stdout)
        self.assertIn("### 回答摘要", result.stdout)
        self.assertIn("### 书内/项目证据", result.stdout)


if __name__ == "__main__":
    unittest.main()
