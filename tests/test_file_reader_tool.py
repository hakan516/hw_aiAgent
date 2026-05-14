import json
import tempfile
import unittest
from pathlib import Path

from ai_study_agent.models import DocumentChunk
from ai_study_agent.tools import FileReaderTool


class FileReaderToolTest(unittest.TestCase):
    def test_file_reader_loads_markdown_chunks(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "notes.md"
            file_path.write_text("# Agent Notes\nTools help the agent gather evidence.", encoding="utf-8")

            result = FileReaderTool().run(str(file_path))

        self.assertTrue(result.success)
        self.assertIsInstance(result.data[0], DocumentChunk)
        self.assertIn("Tools help", result.data[0].text)

    def test_file_reader_converts_json_to_stable_text(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "data.json"
            file_path.write_text(json.dumps({"topic": "agents", "score": 5}), encoding="utf-8")

            result = FileReaderTool().run(str(file_path))

        self.assertTrue(result.success)
        self.assertIn('"score": 5', result.data[0].text)
        self.assertIn('"topic": "agents"', result.data[0].text)

    def test_file_reader_converts_csv_rows_to_text(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "tasks.csv"
            file_path.write_text("name,status\nTesting,done\nDeployment,planned\n", encoding="utf-8")

            result = FileReaderTool().run(str(file_path))

        self.assertTrue(result.success)
        self.assertIn("row 1: name: Testing; status: done", result.data[0].text)

    def test_file_reader_rejects_missing_file(self):
        result = FileReaderTool().run("missing.md")

        self.assertFalse(result.success)
        self.assertIn("file not found", result.message)


if __name__ == "__main__":
    unittest.main()
