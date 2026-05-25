from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_book_materials.py"

spec = importlib.util.spec_from_file_location("validate_book_materials", SCRIPT)
assert spec and spec.loader
validate_book_materials = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_book_materials)


def minimal_project(root: Path) -> None:
    (root / "markdown_output" / "chapters").mkdir(parents=True)
    (root / "markdown_output" / "chapters" / "chapter-01.md").write_text("# Chapter\n", encoding="utf-8")
    (root / "course_materials").mkdir()
    (root / "course_materials" / "source_coverage_audit.md").write_text("# Audit\n", encoding="utf-8")


class ValidateBookMaterialsTest(unittest.TestCase):
    def test_reader_question_logs_are_optional_until_directory_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            minimal_project(root)

            result = validate_book_materials.validate(root, scope="project")

        self.assertTrue(result["ok"], result["issues"])

    def test_reader_question_directory_requires_expected_log_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            minimal_project(root)
            reader_dir = root / "course_materials" / "reader_questions"
            reader_dir.mkdir()
            (reader_dir / "question-log.md").write_text("# Reader Question Log\n", encoding="utf-8")

            result = validate_book_materials.validate(root, scope="project")

        self.assertFalse(result["ok"])
        joined = "\n".join(result["issues"])
        self.assertIn("reader_questions/backwrite-candidates.md", joined)
        self.assertIn("reader_questions/applied-backwrites.md", joined)

    def test_strict_english_markers_are_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            minimal_project(root)
            kb = root / "course_materials" / "strict-notes.md"
            kb.write_text("# Notes\n\nNeeds confirmation: figure meaning.\n\n## Q&A\n\n## Update log\n", encoding="utf-8")

            result = validate_book_materials.validate(root, strict=True, scope="project", language="en")

        self.assertTrue(result["ok"], result["issues"])
        self.assertEqual([], result["warnings"])


if __name__ == "__main__":
    unittest.main()
