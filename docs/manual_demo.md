# Manual Demo Scenarios

These scenarios show the system behavior without needing external services.

## Scenario 1: Answer From Markdown Evidence

```bash
python main.py "Which tool ranks evidence?" --file examples/study_notes.md
```

Expected behavior: the response mentions that the search tool ranks evidence and prints an evidence section with the source chunk.

## Scenario 2: Summarize a CSV File

```bash
python main.py --summary --file examples/tasks.csv
```

Expected behavior: the response summarizes converted CSV rows as readable text.

## Scenario 3: JSON Output

```bash
python main.py "How is deployment prepared?" --file examples/project_data.json --json
```

Expected behavior: the output is valid JSON with `answer`, `tools_used`, and `evidence`.

## Scenario 4: Calculation Tool

```bash
python main.py "Calculate final score" --calculate "80 + 15 / 3"
```

Expected behavior: the calculator returns `85.0`.

## Scenario 5: Optional OpenAI API Synthesis

Install the optional dependency and set an API key:

```bash
python -m pip install -e ".[ai]"
$env:OPENAI_API_KEY="your_api_key_here"
```

Run:

```bash
python main.py "Which tool ranks evidence?" --file examples/study_notes.md --ai
```

Expected behavior: the local tools read and search the file first, then the OpenAI synthesizer writes a cleaner final answer from the retrieved evidence.
