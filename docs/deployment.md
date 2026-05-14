# Deployment Preparation

## Target Mode

The first deployment target is a local command-line tool. This keeps user files on the user's computer and avoids external service failures during assessment.

## Requirements

- Python 3.10 or newer.
- Git for cloning and version control.
- No required runtime packages for offline mode.
- Optional AI mode package: `openai`.
- Optional: `pytest` if the developer prefers pytest over the standard `unittest` runner.

## Setup

```bash
git clone https://github.com/hakan516/hw_aiAgent.git
cd hw_aiAgent
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e .
```

For OpenAI API synthesis:

```bash
python -m pip install -e ".[ai]"
$env:OPENAI_API_KEY="your_api_key_here"
```

## Launch

```bash
python main.py "Which tool is used for evidence?" --file docs/report.md
```

or:

```bash
study-agent "Which tool is used for evidence?" --file docs/report.md
```

## Configuration

No environment variables are required for offline mode. The system is intentionally offline-friendly and deterministic for easier testing.

Optional AI configuration:

- `OPENAI_API_KEY`: required only when using `--ai`.
- `OPENAI_MODEL`: optional model override. Default: `gpt-5`.

## Verification Before Release

```bash
python -m unittest discover -s tests -v
```

Expected result: all tests pass.

## Proposed Safe Release Strategy

Use a staged release:

1. Local developer testing.
2. GitHub push to `main`.
3. Tag a version after tests pass.
4. Share installation instructions with a small group of users.
5. Collect feedback before adding web/API deployment.

The project could later become a web service, but the local CLI is safer for the first release because the system reads local files.
