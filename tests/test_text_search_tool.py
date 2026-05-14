from ai_study_agent.models import DocumentChunk
from ai_study_agent.tools import TextSearchTool


def test_text_search_returns_relevant_chunks_first():
    chunks = [
        DocumentChunk("notes.md", 1, "Deployment is prepared with requirements and startup commands."),
        DocumentChunk("notes.md", 2, "Testing checks calculator and file reader behavior."),
    ]

    result = TextSearchTool().run("How is testing verified?", chunks)

    assert result.success is True
    assert result.data[0].index == 2


def test_text_search_handles_query_without_terms():
    result = TextSearchTool().run("to be or not to be", [])

    assert result.success is False
    assert "searchable terms" in result.message
