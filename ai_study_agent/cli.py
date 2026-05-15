import argparse
import json
import os
from typing import Sequence

from ai_study_agent.agent import StudyResearchAgent
from ai_study_agent.config import load_env_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="study-agent",
        description="AI-assisted study agent that reads files, searches evidence, and calculates safely.",
    )
    parser.add_argument("question", nargs="?", default="", help="Question to answer.")
    parser.add_argument("-f", "--file", help="Path to a .txt, .md, .csv, or .json file.")
    parser.add_argument("-c", "--calculate", help="Arithmetic expression to evaluate.")
    parser.add_argument("--summary", action="store_true", help="Summarize the provided file.")
    parser.add_argument("--offline", action="store_true", help="Disable Gemini synthesis and use only local tools.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON output.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    load_env_file()
    parser = build_parser()
    args = parser.parse_args(argv)
    use_ai = bool(os.getenv("GEMINI_API_KEY")) and not args.offline
    agent = StudyResearchAgent(use_ai=use_ai)

    try:
        if args.summary:
            if not args.file:
                parser.error("--summary requires --file")
            response = agent.summarize_file(args.file)
        else:
            response = agent.answer(args.question, file_path=args.file, calculation=args.calculate)
    except ValueError as exc:
        parser.error(str(exc))

    if args.json:
        print(json.dumps(response.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(response.answer)
        if response.evidence:
            print("\nEvidence:")
            for item in response.evidence:
                print(f"- {item}")
        if response.warnings:
            print("\nWarnings:")
            for item in response.warnings:
                print(f"- {item}")

    return 0
