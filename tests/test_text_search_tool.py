import unittest

from ai_study_agent.models import DocumentChunk
from ai_study_agent.tools import TextSearchTool


class TextSearchToolTest(unittest.TestCase):
    def test_text_search_returns_relevant_chunks_first(self):
        chunks = [
            DocumentChunk("notes.md", 1, "Deployment is prepared with requirements and startup commands."),
            DocumentChunk("notes.md", 2, "Testing checks calculator and file reader behavior."),
        ]

        result = TextSearchTool().run("How is testing verified?", chunks)

        self.assertTrue(result.success)
        self.assertEqual(result.data[0].index, 2)

    def test_text_search_handles_query_without_terms(self):
        result = TextSearchTool().run("to be or not to be", [])

        self.assertFalse(result.success)
        self.assertIn("searchable terms", result.message)


if __name__ == "__main__":
    unittest.main()
