import os

from ai_study_agent.models import ToolResult


class OpenAISynthesizerTool:
    """Uses the OpenAI Responses API to synthesize a final answer from tool evidence."""

    name = "openai_synthesizer"

    def __init__(self, model: str | None = None, api_key: str | None = None) -> None:
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

    def run(
        self,
        question: str,
        draft_answer: str,
        evidence: list[str],
        warnings: list[str],
    ) -> ToolResult:
        if not self.api_key:
            return ToolResult(self.name, False, None, "OPENAI_API_KEY is not set")

        try:
            from openai import OpenAI
        except ImportError:
            return ToolResult(self.name, False, None, "openai package is not installed")

        prompt = self._build_prompt(question, draft_answer, evidence, warnings)

        try:
            client = OpenAI(api_key=self.api_key)
            response = client.responses.create(
                model=self.model,
                instructions=(
                    "You are a careful study assistant. Use only the provided draft, "
                    "tool evidence, and warnings. Do not invent facts. Keep the answer concise."
                ),
                input=prompt,
            )
        except Exception as exc:
            return ToolResult(self.name, False, None, f"OpenAI request failed: {exc}")

        text = getattr(response, "output_text", "").strip()
        if not text:
            return ToolResult(self.name, False, None, "OpenAI response did not contain text")
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
            f"User question:\n{question or 'No question provided.'}\n\n"
            f"Draft answer from local agent tools:\n{draft_answer}\n\n"
            f"Evidence returned by tools:\n{evidence_text}\n\n"
            f"Warnings:\n{warning_text}\n\n"
            "Write the final answer. Mention uncertainty if evidence is missing."
        )
