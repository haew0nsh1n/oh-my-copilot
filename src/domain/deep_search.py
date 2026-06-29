"""Domain model for deep codebase search."""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class SearchScope(str, Enum):
    CODEBASE = "codebase"
    SYMBOLS = "symbols"
    PATTERNS = "patterns"
    DEPENDENCIES = "dependencies"
    ALL = "all"


@dataclass
class SearchResult:
    file_path: str
    line_number: int
    content: str
    relevance_score: float = 0.0
    context_lines: List[str] = field(default_factory=list)


@dataclass
class DeepSearchSession:
    query: str
    scope: SearchScope = SearchScope.ALL
    results: List[SearchResult] = field(default_factory=list)
    max_results: int = 50
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.query or not self.query.strip():
            raise ValueError("Query cannot be empty")

    def add_result(self, result: SearchResult) -> None:
        if len(self.results) < self.max_results:
            self.results.append(result)

    def get_top_results(self, n: int = 10) -> List[SearchResult]:
        sorted_results = sorted(self.results, key=lambda r: r.relevance_score, reverse=True)
        return sorted_results[:n]

    def has_results(self) -> bool:
        return len(self.results) > 0


@dataclass
class DeepSearchReport:
    query: str
    scope: SearchScope
    total_results: int = 0
    top_files: List[str] = field(default_factory=list)
    summary: str = ""
