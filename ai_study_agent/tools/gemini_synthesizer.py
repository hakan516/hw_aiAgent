import os

from ai_study_agent.models import ToolResult


class GeminiSynthesizerTool:
    """Uses the Gemini API to synthesize a final answer from tool evidence."""

    name = "gemini_synthesizer"

    def __init__(self, model: str | None = None, api_key: str | None = None) -> None:
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        self.api_key = api_key if api_key is not None else os.getenv("GEMINI_API_KEY")

    def run(
        self,
        question: str,
        draft_answer: str,
        evidence: list[str],
        warnings: list[str],
    ) -> ToolResult:
        if not self.api_key:
            return ToolResult(self.name, False, None, "GEMINI_API_KEY is not set")

        try:
            from google import genai
        except ImportError:
            return ToolResult(self.name, False, None, "google-genai package is not installed")

        prompt = self._build_prompt(question, draft_answer, evidence, warnings)

        try:
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
        except Exception as exc:
            return ToolResult(self.name, False, None, f"Gemini request failed: {exc}")

        text = getattr(response, "text", "").strip()
        if not text:
            return ToolResult(self.name, False, None, "Gemini response did not contain text")
        return ToolResult(self.name, True, text, f"generated with {self.model}")

    def _build_prompt(
        self,
        question: str,
        draft_answer: str,
        evidence: list[str],
        warnings: list[str],
    ) -> str:
        evidence_text = "\n".join(f"- {item}" for item in evidence) or "- No direct evidence."
        warning_text = "\n".join(f"- {item}" for item in warnings) or "- None."
        return (
            "You are a careful study assistant. Use only the provided draft, "
            "tool evidence, and warnings. Do not invent facts. Keep the answer concise.\n\n"
            f"User question:\n{question or 'No question provided.'}\n\n"
            f"Draft answer from local agent tools:\n{draft_answer}\n\n"
            f"Evidence returned by tools:\n{evidence_text}\n\n"
            f"Warnings:\n{warning_text}\n\n"
            "Write the final answer. Mention uncertainty if evidence is missing."
        )
