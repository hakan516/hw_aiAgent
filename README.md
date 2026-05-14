# Study Research Agent

Study Research Agent is a Python command-line assistant that answers user questions by calling tools during execution. It can read local documents, convert structured data into text, search for relevant evidence, safely evaluate arithmetic expressions, and return a grounded response.

The project is designed for a controlled deployment scenario: it runs locally, has no required network dependency, includes tests, and documents how data moves between components.

## Features

- Single-agent workflow implemented in Python.
- Tool use during execution:
  - `FileReaderTool` reads `.txt`, `.md`, `.csv`, and `.json`.
  - `TextSearchTool` ranks document chunks by query relevance.
  - `CalculatorTool` evaluates arithmetic expressions through a safe AST parser.
- CLI input and text or JSON output.
- Unit tests for tools, validation, errors, and the full workflow.
- Deployment notes and staged development journal.

## Project Structure

```text
.
├── ai_study_agent/
│   ├── agent.py
│   ├── cli.py
│   ├── models.py
│   └── tools/
├── docs/
│   ├── architecture.md
│   ├── deployment.md
│   ├── manual_demo.md
│   └── report.md
├── examples/
├── tests/
├── main.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Installation

Use Python 3.10 or newer.

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e .
```

There are no required runtime dependencies. `requirements.txt` records this and notes that `pytest` is optional for development.

## Usage

Ask a question from a local file:

```bash
python main.py "Which tool ranks evidence?" --file notes.md
```

Summarize a file:

```bash
python main.py --summary --file notes.md
```

Combine file evidence with calculation:

```bash
python main.py "What is the release budget?" --file budget.md --calculate "120 + 30"
```

Return JSON output:

```bash
python main.py "What validates workflow?" --file notes.md --json
```

After editable installation, the console command is also available:

```bash
study-agent "Which topic is most important?" --file notes.md
```

## Testing

Run the full standard-library test suite:

```bash
python -m unittest discover -s tests -v
```

The tests cover calculator behavior, file conversion, text search, input validation, error handling, CLI JSON output, and the full agent workflow.

## Manual Demo

Sample files are included in `examples/`. Additional demo commands and expected behavior are documented in `docs/manual_demo.md`.

## Data Conversion

The system accepts user text, optional arithmetic expressions, and optional local files. File content is converted into `DocumentChunk` objects:

- Markdown and text are normalized by trimming blank lines.
- JSON is parsed and re-serialized with stable formatting.
- CSV rows are converted into readable key-value text.
- Long text is split into numbered chunks while preserving source file information.

The agent then passes chunks to the search tool, receives ranked evidence, and formats the final answer with evidence references.

## Deployment Strategy

The suitable deployment strategy is a local command-line application. A safe release process would use staged deployment:

1. Run the unit test suite locally.
2. Package with `pyproject.toml`.
3. Release to a private GitHub repository.
4. Let test users install in editable mode or from a tagged release.
5. Add monitoring or logging only after privacy requirements are defined.

This strategy is appropriate because the agent reads user files and should first be used in a controlled local environment.
