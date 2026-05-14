import csv
import json
from pathlib import Path

from ai_study_agent.models import DocumentChunk, ToolResult


class FileReaderTool:
    """Reads user-provided local files and converts them into text chunks."""

    name = "file_reader"
    supported_suffixes = {".txt", ".md", ".csv", ".json"}

    def run(self, file_path: str, chunk_size: int = 900) -> ToolResult:
        path = Path(file_path)
        if not path.exists():
            return ToolResult(self.name, False, [], f"file not found: {file_path}")
        if not path.is_file():
            return ToolResult(self.name, False, [], f"path is not a file: {file_path}")
        if path.suffix.lower() not in self.supported_suffixes:
            return ToolResult(
                self.name,
                False,
                [],
                f"unsupported file type: {path.suffix or 'no extension'}",
            )

        try:
            text = self._read_as_text(path)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, csv.Error) as exc:
            return ToolResult(self.name, False, [], str(exc))

        chunks = self._chunk_text(text, str(path), chunk_size)
        return ToolResult(self.name, True, chunks, f"loaded {len(chunks)} chunks")

    def _read_as_text(self, path: Path) -> str:
        suffix = path.suffix.lower()
        if suffix in {".txt", ".md"}:
            return path.read_text(encoding="utf-8")
        if suffix == ".json":
            data = json.loads(path.read_text(encoding="utf-8"))
            return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)
        if suffix == ".csv":
            rows: list[str] = []
            with path.open("r", encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                for row_number, row in enumerate(reader, start=1):
                    values = [f"{key}: {value}" for key, value in row.items()]
                    rows.append(f"row {row_number}: " + "; ".join(values))
            return "\n".join(rows)
        raise ValueError("unsupported file type")

    def _chunk_text(self, text: str, source: str, chunk_size: int) -> list[DocumentChunk]:
        normalized = "\n".join(line.strip() for line in text.splitlines() if line.strip())
        if not normalized:
            return [DocumentChunk(source=source, index=1, text="")]

        chunks: list[DocumentChunk] = []
        start = 0
        index = 1
        while start < len(normalized):
            end = min(start + chunk_size, len(normalized))
            boundary = normalized.rfind(" ", start, end)
            if boundary <= start:
                boundary = end
            chunk = normalized[start:boundary].strip()
            if chunk:
                chunks.append(DocumentChunk(source=source, index=index, text=chunk))
                index += 1
            start = boundary + 1
        return chunks
