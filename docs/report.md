# Study Research Agent Report

## Final System Description and Goal

Study Research Agent is a Python AI-assisted command-line system. Its goal is to help a user analyze study notes, project files, CSV records, or JSON data by using tools during execution. The user gives a question, a file path, and optionally a calculation. The agent reads and converts the file, searches for relevant evidence, calculates when requested, and returns a meaningful answer.

## AI or Agent-Based Approach

The system uses a single-agent workflow. The `StudyResearchAgent` decides which tool calls are needed based on the user input:

- If a file is provided, it calls the file reader tool.
- If a question and readable file chunks are available, it calls the text search tool.
- If an arithmetic expression is provided, it calls the calculator tool.
- It synthesizes the final response from the tool outputs.

This is an agent-based design because the central component coordinates multiple tools to solve a user request instead of using one fixed function.

## Programming Concepts Used

- Modular project structure: source code is separated into agent, CLI, models, and tools.
- Classes and dependency injection: each tool is a class, and the agent can receive custom tool instances for testing.
- Dataclasses: `ToolResult`, `DocumentChunk`, and `AgentResponse` keep data consistent between components.
- Error handling: unsupported files, missing files, invalid calculations, and empty input are handled explicitly.
- Safe parsing: the calculator uses Python AST nodes instead of `eval`.
- File I/O and data conversion: text, Markdown, CSV, and JSON are normalized into a shared chunk format.
- Automated testing: `unittest` verifies tools, workflow, validation, and CLI output.

## Tools and Their Roles

`FileReaderTool` reads external local files. It supports `.txt`, `.md`, `.csv`, and `.json`, then converts them into `DocumentChunk` objects.

`TextSearchTool` acts as a retrieval tool. It tokenizes the user question and document chunks, ranks chunks by term overlap, and returns the most relevant evidence.

`CalculatorTool` evaluates arithmetic expressions safely. It supports common arithmetic operators and rejects unsafe Python expressions.

## Input, Output, and Data Conversion

Input can be:

- A natural-language question.
- A local file path.
- An arithmetic expression.
- A request for text or JSON output.

The data flow is:

1. CLI parses the input.
2. The agent chooses required tools.
3. The file reader converts external file formats into `DocumentChunk` records.
4. The search tool ranks chunks and returns evidence.
5. The calculator returns a numeric result when requested.
6. The agent produces an `AgentResponse`.
7. The CLI prints text or JSON.

Correctness is preserved by keeping source path and chunk number inside every evidence item.

## Testing Results and Conclusions

Testing was done with the standard-library `unittest` module. The test suite includes 13 tests:

- Calculator evaluates valid arithmetic.
- Calculator rejects unsafe expressions.
- Calculator reports division by zero.
- File reader loads Markdown text.
- File reader converts JSON into stable text.
- File reader converts CSV rows into readable key-value text.
- File reader reports missing files.
- Text search ranks relevant chunks first.
- Text search handles queries without useful search terms.
- Agent answers a question from file evidence.
- Agent combines file evidence with calculation.
- Agent validates empty input.
- CLI returns valid JSON output.

Final local result: all 13 tests passed.

## Deployment Preparation

The project includes:

- `README.md` with installation, usage, testing, and deployment instructions.
- `requirements.txt` showing that no runtime dependencies are required.
- `pyproject.toml` for editable installation and a `study-agent` console command.
- `docs/deployment.md` with setup, launch, configuration, verification, and release notes.

## Proposed Deployment Strategy

The best initial deployment is a local command-line application. This is suitable because the system reads local files and should protect user data. A staged release is recommended: test locally, push to GitHub, tag a version, share with a small user group, and only later consider API or web deployment.

## Journal

### Step 1 - 24.04

Planned system: an AI-assisted study and project research agent that answers questions from local files and performs calculations when needed.

Planned AI approach: one coordinating agent that chooses tools based on the user request.

Planned tools:

- File reader for local notes and structured files.
- Text search/retrieval for evidence.
- Calculator for numeric questions.

Preliminary programming concepts:

- Python modules and packages.
- Classes for agent and tools.
- File input/output.
- Data structures for tool results.
- Error handling.
- Basic tests.

### Step 2 - 08.05

Updated implementation progress: the project now has a package structure with agent, tools, CLI, and shared models. The first implementation supports local file reading, evidence search, and safe calculation.

Refined programming concepts actually used:

- Dataclasses for structured data exchange.
- Dependency injection for testable agent tools.
- AST parsing for safe calculator behavior.
- CSV and JSON conversion into normalized text.
- CLI argument parsing with `argparse`.

How tools are integrated: the agent receives the user request, calls `FileReaderTool` if a file is present, passes the resulting chunks to `TextSearchTool`, calls `CalculatorTool` if a calculation is present, and joins the outputs into one response.

### Step 3 - 15.05

Testing process: tests were added during implementation instead of only at the end. Tool tests verify each tool separately, while workflow tests verify the full agent and CLI.

Test scenarios:

- Valid calculation returns the correct number.
- Unsafe calculation is rejected.
- Missing file returns a readable error.
- Markdown, CSV, and JSON inputs are converted correctly.
- Search returns the most relevant chunk first.
- Empty user input is rejected.
- CLI JSON output can be parsed.
- Agent combines evidence and calculation in one answer.

Deployment preparation: the system can be run with `python main.py` or installed as `study-agent` through `pyproject.toml`.

Data conversion: file inputs are normalized into `DocumentChunk` records. JSON is parsed and formatted consistently; CSV rows become key-value text; plain text and Markdown are cleaned and chunked.

### Final Submission - 22.05

Final result: the system is a functional local AI-assisted agent that uses external tools during execution. It receives user input, calls tools, handles errors, and returns a useful response with evidence.

Final programming concepts: modular architecture, classes, dataclasses, file processing, structured error handling, safe AST parsing, CLI design, and automated testing.

Final tools: file reader, text search, and calculator.

Final testing conclusion: all 13 tests pass in the local test environment.

Final deployment preparation: README, dependency file, package metadata, console command, deployment notes, and test instructions are included.

Final deployment strategy: local CLI first, then staged GitHub releases after test verification.
