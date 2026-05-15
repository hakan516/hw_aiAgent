import unittest

from ai_study_agent.tools import GeminiSynthesizerTool


class GeminiSynthesizerToolTest(unittest.TestCase):
    def test_synthesizer_requires_api_key(self):
        result = GeminiSynthesizerTool(api_key="").run(
            "What ranks evidence?",
            "The search tool ranks evidence.",
            ["notes.md chunk 1: The search tool ranks evidence."],
            [],
        )

        self.assertFalse(result.success)
        self.assertIn("GEMINI_API_KEY", result.message)


if __name__ == "__main__":
    unittest.main()
