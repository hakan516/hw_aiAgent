import re
from collections import Counter

from ai_study_agent.models import DocumentChunk, ToolResult


class TextSearchTool:
    """Ranks document chunks by overlap with a user question."""

    name = "text_search"
    stop_words = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "for",
        "from",
        "how",
        "in",
        "is",
        "of",
        "on",
        "or",
        "the",
        "to",
        "what",
        "which",
        "with",
    }

    def run(self, query: str, chunks: list[DocumentChunk], limit: int = 3) -> ToolResult:
        terms = self._terms(query)
        if not terms:
            return ToolResult(self.name, False, [], "query does not contain searchable terms")

        scored: list[tuple[int, DocumentChunk]] = []
        query_counts = Counter(terms)
        for chunk in chunks:
            chunk_terms = Counter(self._terms(chunk.text))
            score = sum(min(count, chunk_terms[term]) for term, count in query_counts.items())
            if score:
                scored.append((score, chunk))

        scored.sort(key=lambda item: (-item[0], item[1].index))
        matches = [chunk for _, chunk in scored[:limit]]
        if not matches:
            return ToolResult(self.name, True, [], "no direct evidence found")
        return ToolResult(self.name, True, matches, f"found {len(matches)} relevant chunks")

    def _terms(self, text: str) -> list[str]:
        words = re.findall(r"[A-Za-z0-9_]+", text.lower())
        return [word for word in words if len(word) > 2 and word not in self.stop_words]
