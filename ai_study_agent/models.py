from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ToolResult:
    tool_name: str
    success: bool
    data: Any
    message: str = ""


@dataclass(frozen=True)
class DocumentChunk:
    source: str
    index: int
    text: str


@dataclass
class AgentResponse:
    request: str
    answer: str
    tools_used: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "request": self.request,
            "answer": self.answer,
            "tools_used": self.tools_used,
            "evidence": self.evidence,
            "warnings": self.warnings,
        }
