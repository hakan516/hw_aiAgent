import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from ai_study_agent.agent import StudyResearchAgent
from ai_study_agent.cli import main


class AgentWorkflowTest(unittest.TestCase):
    def test_agent_answers_question_from_file(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "project.md"
            file_path.write_text(
                "The system uses a file reader tool. The search tool ranks evidence for answers.",
                encoding="utf-8",
            )

            response = StudyResearchAgent().answer("Which tool ranks evidence?", file_path=str(file_path))

        self.assertIn("search tool ranks evidence", response.answer)
        self.assertEqual(response.tools_used, ["file_reader", "text_search"])
        self.assertTrue(response.evidence)

    def test_agent_combines_file_answer_and_calculation(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "budget.md"
            file_path.write_text("Deployment cost is estimated before release.", encoding="utf-8")

            response = StudyResearchAgent().answer(
                "What is estimated?",
                file_path=str(file_path),
                calculation="120 + 30",
            )

        self.assertIn("Deployment cost", response.answer)
        self.assertIn("120 + 30 = 150", response.answer)
        self.assertIn("calculator", response.tools_used)

    def test_agent_validates_empty_input(self):
        with self.assertRaises(ValueError):
            StudyResearchAgent().answer("")

    def test_cli_prints_json_output(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "notes.md"
            file_path.write_text("Testing validates the main workflow.", encoding="utf-8")
            stream = StringIO()

            with redirect_stdout(stream):
                exit_code = main(["What validates workflow?", "--file", str(file_path), "--json"])

        output = json.loads(stream.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(output["tools_used"], ["file_reader", "text_search"])
        self.assertIn("Testing validates", output["answer"])


if __name__ == "__main__":
    unittest.main()
