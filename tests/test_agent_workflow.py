import json

import pytest

from ai_study_agent.agent import StudyResearchAgent
from ai_study_agent.cli import main


def test_agent_answers_question_from_file(tmp_path):
    file_path = tmp_path / "project.md"
    file_path.write_text(
        "The system uses a file reader tool. The search tool ranks evidence for answers.",
        encoding="utf-8",
    )

    response = StudyResearchAgent().answer("Which tool ranks evidence?", file_path=str(file_path))

    assert "search tool ranks evidence" in response.answer
    assert response.tools_used == ["file_reader", "text_search"]
    assert response.evidence


def test_agent_combines_file_answer_and_calculation(tmp_path):
    file_path = tmp_path / "budget.md"
    file_path.write_text("Deployment cost is estimated before release.", encoding="utf-8")

    response = StudyResearchAgent().answer(
        "What is estimated?",
        file_path=str(file_path),
        calculation="120 + 30",
    )

    assert "Deployment cost" in response.answer
    assert "120 + 30 = 150" in response.answer
    assert "calculator" in response.tools_used


def test_agent_validates_empty_input():
    with pytest.raises(ValueError):
        StudyResearchAgent().answer("")


def test_cli_prints_json_output(tmp_path, capsys):
    file_path = tmp_path / "notes.md"
    file_path.write_text("Testing validates the main workflow.", encoding="utf-8")

    exit_code = main(["What validates workflow?", "--file", str(file_path), "--json"])
    output = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert output["tools_used"] == ["file_reader", "text_search"]
    assert "Testing validates" in output["answer"]
