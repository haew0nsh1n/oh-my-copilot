"""DeepSearch skill — deep codebase search."""

from typing import List, Optional
from domain import (
    DeepSearchSession, SearchResult, SearchScope, DeepSearchReport,
)


class DeepSearchSkill:
    name = "deepsearch"
    description = "Deep codebase search — symbols, patterns, and dependency mapping"

    def __init__(self):
        self.sessions: dict = {}

    def create_session(self, query: str, scope: SearchScope = SearchScope.ALL, max_results: int = 50) -> DeepSearchSession:
        session = DeepSearchSession(query=query, scope=scope, max_results=max_results)
        self.sessions[query] = session
        return session

    def add_result(self, session: DeepSearchSession, file_path: str, line_number: int, content: str, relevance_score: float = 0.5, context_lines: List[str] = None) -> SearchResult:
        result = SearchResult(
            file_path=file_path,
            line_number=line_number,
            content=content,
            relevance_score=relevance_score,
            context_lines=context_lines or []
        )
        session.add_result(result)
        return result

    def get_top_results(self, session: DeepSearchSession, n: int = 10) -> List[SearchResult]:
        return session.get_top_results(n)

    def generate_report(self, session: DeepSearchSession) -> DeepSearchReport:
        top = session.get_top_results(5)
        top_files = list(dict.fromkeys(r.file_path for r in top))
        return DeepSearchReport(
            query=session.query,
            scope=session.scope,
            total_results=len(session.results),
            top_files=top_files,
            summary=f"Found {len(session.results)} results for '{session.query}' in scope {session.scope.value}"
        )

    def get_session(self, query: str) -> Optional[DeepSearchSession]:
        return self.sessions.get(query)
