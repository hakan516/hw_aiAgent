# Architecture

## Components

`main.py` is the executable entry point. It delegates to `ai_study_agent.cli`.

`ai_study_agent.cli` parses command-line arguments and formats either text or JSON output.

`StudyResearchAgent` coordinates the workflow. It does not read files or calculate directly; it calls tools and combines their results.

`FileReaderTool` is responsible for external data access. It reads local files and converts supported formats into `DocumentChunk` records.

`TextSearchTool` ranks chunks against the user question.

`CalculatorTool` safely evaluates arithmetic expressions.

`GeminiSynthesizerTool` optionally calls the Gemini API after local tools have produced a draft answer and evidence.

## Workflow

```text
User input
  -> CLI parser
  -> StudyResearchAgent
  -> FileReaderTool, TextSearchTool, CalculatorTool
  -> GeminiSynthesizerTool when GEMINI_API_KEY is configured
  -> AgentResponse
  -> Text or JSON output
```

## Data Contracts

`ToolResult` keeps every tool response consistent:

- `tool_name`: which tool was called.
- `success`: whether the tool completed correctly.
- `data`: returned data.
- `message`: human-readable status or error.

`DocumentChunk` stores converted file content:

- `source`: original file path.
- `index`: chunk number.
- `text`: normalized content.

`AgentResponse` stores final output:

- `request`: user request.
- `answer`: generated response.
- `tools_used`: ordered list of called tools.
- `evidence`: source previews.
- `warnings`: recoverable problems.

## Failure Handling

Missing files, unsupported extensions, invalid calculations, and empty input are converted into warnings or validation errors. The agent can still return partial results when one tool succeeds and another tool fails.
