# Deployment Preparation

## Target Mode

The first deployment target is a local command-line tool. This keeps file processing local and avoids external service failures during normal offline use.

## Requirements

- Python 3.10 or newer.
- Git for cloning and version control.
- No required runtime packages for offline mode.
- Optional AI mode package: `google-genai`.
- Optional: `pytest` if the developer prefers pytest over the standard `unittest` runner.

## Setup

```bash
git clone https://github.com/hakan516/hw_aiAgent.git
cd hw_aiAgent
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e .
```

For Gemini API synthesis:

```bash
python -m pip install -e ".[ai]"
```

Create `.env` from `.env.example` and add the API key. The real `.env` file is ignored by Git.

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

- `GEMINI_API_KEY`: enables Gemini API synthesis when present.
- `GEMINI_MODEL`: optional model override. Default: `gemini-2.0-flash`.

These values can be placed in a local `.env` file:

```text
GEMINI_API_KEY=replace_with_api_key
GEMINI_MODEL=gemini-2.0-flash
```

When `GEMINI_API_KEY` exists, API synthesis is used automatically. Add `--offline` to any command to force local-only behavior.

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

The project can later be deployed as a web service or API-based assistant. The local CLI is the safest first release because file processing remains under user control.
