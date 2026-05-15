from ai_study_agent.models import AgentResponse, DocumentChunk
from ai_study_agent.tools import CalculatorTool, FileReaderTool, GeminiSynthesizerTool, TextSearchTool


class StudyResearchAgent:
    """Coordinates tools to answer questions from files and calculations."""

    def __init__(
        self,
        file_reader: FileReaderTool | None = None,
        search: TextSearchTool | None = None,
        calculator: CalculatorTool | None = None,
        synthesizer: GeminiSynthesizerTool | None = None,
        use_ai: bool = False,
    ) -> None:
        self.file_reader = file_reader or FileReaderTool()
        self.search = search or TextSearchTool()
        self.calculator = calculator or CalculatorTool()
        self.synthesizer = synthesizer or GeminiSynthesizerTool()
        self.use_ai = use_ai

    def answer(
        self,
        question: str,
        file_path: str | None = None,
        calculation: str | None = None,
    ) -> AgentResponse:
        clean_question = question.strip()
        if not clean_question and not calculation:
            raise ValueError("question or calculation is required")

        request = clean_question or f"Calculate: {calculation}"
        tools_used: list[str] = []
        warnings: list[str] = []
        evidence: list[str] = []
        answer_parts: list[str] = []

        if file_path:
            chunks = self._load_chunks(file_path, tools_used, warnings)
            if chunks:
                file_answer, file_evidence = self._answer_from_chunks(clean_question, chunks, tools_used)
                answer_parts.append(file_answer)
                evidence.extend(file_evidence)

        if calculation:
            calc_result = self.calculator.run(calculation)
            tools_used.append(calc_result.tool_name)
            if calc_result.success:
                answer_parts.append(f"Calculation result: {calculation} = {calc_result.data}")
            else:
                warnings.append(f"Calculation failed: {calc_result.message}")

        if not answer_parts:
            if clean_question:
                answer_parts.append(self._fallback_answer(clean_question))
            else:
                answer_parts.append("No result could be produced from the provided input.")

        final_answer = "\n".join(answer_parts)
        if self.use_ai:
            ai_result = self.synthesizer.run(request, final_answer, evidence, warnings)
            tools_used.append(ai_result.tool_name)
            if ai_result.success:
                final_answer = ai_result.data
            else:
                warnings.append(f"AI synthesis skipped: {ai_result.message}")

        return AgentResponse(
            request=request,
            answer=final_answer,
            tools_used=tools_used,
            evidence=evidence,
            warnings=warnings,
        )

    def summarize_file(self, file_path: str) -> AgentResponse:
        chunks = self._load_chunks(file_path, [], [])
        if not chunks:
            return AgentResponse(
                request=f"Summarize {file_path}",
                answer="The file could not be summarized.",
                tools_used=[self.file_reader.name],
                warnings=[f"No readable content found in {file_path}"],
            )

        summary = self._summarize_chunks(chunks)
        tools_used = [self.file_reader.name]
        evidence = [self._format_evidence(chunk) for chunk in chunks[:3]]
        warnings: list[str] = []
        if self.use_ai:
            ai_result = self.synthesizer.run(f"Summarize {file_path}", summary, evidence, warnings)
            tools_used.append(ai_result.tool_name)
            if ai_result.success:
                summary = ai_result.data
            else:
                warnings.append(f"AI synthesis skipped: {ai_result.message}")

        return AgentResponse(
            request=f"Summarize {file_path}",
            answer=summary,
            tools_used=tools_used,
            evidence=evidence,
            warnings=warnings,
        )

    def _load_chunks(
        self,
        file_path: str,
        tools_used: list[str],
        warnings: list[str],
    ) -> list[DocumentChunk]:
        result = self.file_reader.run(file_path)
        tools_used.append(result.tool_name)
        if not result.success:
            warnings.append(result.message)
            return []
        return result.data

    def _answer_from_chunks(
        self,
        question: str,
        chunks: list[DocumentChunk],
        tools_used: list[str],
    ) -> tuple[str, list[str]]:
        if not question:
            return self._summarize_chunks(chunks), [self._format_evidence(chunk) for chunk in chunks[:3]]

        result = self.search.run(question, chunks)
        tools_used.append(result.tool_name)
        matches: list[DocumentChunk] = result.data
        if not matches:
            return (
                "I could not find direct evidence in the file. "
                "The closest overall summary is: " + self._summarize_chunks(chunks),
                [],
            )

        evidence = [self._format_evidence(chunk) for chunk in matches]
        answer = self._synthesize_answer(question, matches)
        return answer, evidence

    def _synthesize_answer(self, question: str, matches: list[DocumentChunk]) -> str:
        sentences: list[str] = []
        for chunk in matches:
            sentences.extend(self._split_sentences(chunk.text))
        selected = sentences[:4] if sentences else [matches[0].text]
        joined = " ".join(selected)
        return f"Based on the file, the answer to '{question}' is: {joined}"

    def _summarize_chunks(self, chunks: list[DocumentChunk]) -> str:
        text = " ".join(chunk.text for chunk in chunks)
        sentences = self._split_sentences(text)
        selected = sentences[:5] if sentences else [text[:500]]
        return "Summary: " + " ".join(selected)

    def _fallback_answer(self, question: str) -> str:
        return (
            "I need a readable file or calculation tool input to produce grounded results. "
            f"Received question: {question}"
        )

    def _split_sentences(self, text: str) -> list[str]:
        separators = text.replace("?", ".").replace("!", ".").split(".")
        return [item.strip() + "." for item in separators if item.strip()]

    def _format_evidence(self, chunk: DocumentChunk) -> str:
        preview = chunk.text[:240].strip()
        if len(chunk.text) > 240:
            preview += "..."
        return f"{chunk.source} chunk {chunk.index}: {preview}"
