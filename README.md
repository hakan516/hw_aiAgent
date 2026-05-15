# Study Research Agent

Study Research Agent is a Python command-line assistant that answers questions by combining local tools with optional Gemini API synthesis. It can read documents, convert structured data into text, search for relevant evidence, safely evaluate arithmetic expressions, and return a grounded answer.

The system runs in two modes:

- API-backed mode: if `GEMINI_API_KEY` is configured, local tools run first and Gemini synthesizes the final answer from the retrieved evidence.
- Offline mode: if no API key is configured, or if `--offline` is passed, the system uses only local deterministic tools.

## Features

- Single-agent workflow implemented in Python.
- Tool use during execution:
  - `FileReaderTool` reads `.txt`, `.md`, `.csv`, and `.json` files.
  - `TextSearchTool` ranks document chunks by relevance to the question.
  - `CalculatorTool` evaluates arithmetic expressions through a safe AST parser.
  - `GeminiSynthesizerTool` uses the Gemini API when an API key is configured.
- CLI input with text or JSON output.
- Unit tests for tools, validation, errors, API fallback, `.env` loading, and the full workflow.
- Deployment notes, architecture documentation, manual demo scenarios, and staged project report.

## Project Structure

```text
.
|-- ai_study_agent/
|   |-- agent.py
|   |-- cli.py
|   |-- config.py
|   |-- models.py
|   `-- tools/
|-- docs/
|   |-- architecture.md
|   |-- deployment.md
|   |-- manual_demo.md
|   `-- report.md
|-- examples/
|   |-- project_data.json
|   |-- study_notes.md
|   `-- tasks.csv
|-- tests/
|-- .env.example
|-- main.py
|-- pyproject.toml
|-- requirements.txt
`-- README.md
```

## Installation

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e .
```

For Gemini API synthesis, install the API dependency:

```bash
python -m pip install -r requirements.txt
```

Package installation also supports optional dependency groups:

```bash
python -m pip install -e ".[ai]"
```

## Configuration

Create a local `.env` file in the project root by copying `.env.example`:

```text
GEMINI_API_KEY=replace_with_api_key
GEMINI_MODEL=gemini-2.0-flash
```

The real `.env` file is ignored by Git and should not be committed.

`GEMINI_API_KEY` enables automatic API-backed synthesis. `GEMINI_MODEL` is optional; the default model is `gemini-2.0-flash`.

## Usage

Ask a question from a Markdown file:

```bash
python main.py "Which tool ranks evidence?" --file examples/study_notes.md
```

Summarize a CSV file:

```bash
python main.py --summary --file examples/tasks.csv
```

Ask about JSON data and return machine-readable output:

```bash
python main.py "How is deployment prepared?" --file examples/project_data.json --json
```

Combine file evidence with calculation:

```bash
python main.py "What is the total release budget?" --file examples/study_notes.md --calculate "120 + 30"
```

Force local-only execution even when `.env` contains an API key:

```bash
python main.py "Which tool ranks evidence?" --file examples/study_notes.md --offline
```

After editable installation, the console command is also available:

```bash
study-agent "Which tool ranks evidence?" --file examples/study_notes.md
```

## Testing

Run the full standard-library test suite:

```bash
python -m unittest discover -s tests -v
```

The tests cover calculator behavior, file conversion, text search, input validation, error handling, CLI JSON output, `.env` loading, AI synthesis fallback, and the full agent workflow.

## Manual Demo

Sample files are included in `examples/`. Additional demo commands and expected behavior are documented in `docs/manual_demo.md`.

## Data Conversion

The system accepts natural-language questions, optional arithmetic expressions, and optional local files. File content is converted into `DocumentChunk` objects:

- Markdown and text are normalized by trimming blank lines.
- JSON is parsed and re-serialized with stable formatting.
- CSV rows are converted into readable key-value text.
- Long text is split into numbered chunks while preserving source file information.

The agent passes chunks to the search tool, receives ranked evidence, and prepares a draft answer. If `GEMINI_API_KEY` is configured, the Gemini synthesizer rewrites the final answer using only the local draft, retrieved evidence, and warnings. Use `--offline` to skip API synthesis.

## Deployment Strategy

The suitable initial deployment strategy is a local command-line application. A controlled release process is:

1. Run the unit test suite locally.
2. Package with `pyproject.toml`.
3. Push the repository to GitHub.
4. Create a tagged release after tests pass.
5. Share installation and configuration instructions with test users.

This approach keeps file processing local while allowing API-backed synthesis when explicitly configured.
