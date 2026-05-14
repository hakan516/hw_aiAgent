import json

from ai_study_agent.models import DocumentChunk
from ai_study_agent.tools import FileReaderTool


def test_file_reader_loads_markdown_chunks(tmp_path):
    file_path = tmp_path / "notes.md"
    file_path.write_text("# Agent Notes\nTools help the agent gather evidence.", encoding="utf-8")

    result = FileReaderTool().run(str(file_path))

    assert result.success is True
    assert isinstance(result.data[0], DocumentChunk)
    assert "Tools help" in result.data[0].text


def test_file_reader_converts_json_to_stable_text(tmp_path):
    file_path = tmp_path / "data.json"
    file_path.write_text(json.dumps({"topic": "agents", "score": 5}), encoding="utf-8")

    result = FileReaderTool().run(str(file_path))

    assert result.success is True
    assert '"score": 5' in result.data[0].text
    assert '"topic": "agents"' in result.data[0].text


def test_file_reader_converts_csv_rows_to_text(tmp_path):
    file_path = tmp_path / "tasks.csv"
    file_path.write_text("name,status\nTesting,done\nDeployment,planned\n", encoding="utf-8")

    result = FileReaderTool().run(str(file_path))

    assert result.success is True
    assert "row 1: name: Testing; status: done" in result.data[0].text


def test_file_reader_rejects_missing_file():
    result = FileReaderTool().run("missing.md")

    assert result.success is False
    assert "file not found" in result.message
