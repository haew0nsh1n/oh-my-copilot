"""VisualVerdict skill — structured visual QA loop."""

from typing import List, Optional
from domain import (
    VisualVerdictSession, VisualAsset, VisualComparison,
    VerdictStatus, VisualVerdictReport,
)


class VisualVerdictSkill:
    name = "visual_verdict"
    description = "Structured visual QA loop for screenshot/reference matching (threshold: 90+)"

    def __init__(self):
        self.sessions: dict = {}

    def create_session(self, task_description: str, threshold: float = 90.0) -> VisualVerdictSession:
        session = VisualVerdictSession(task_description=task_description, threshold=threshold)
        self.sessions[task_description] = session
        return session

    def create_asset(self, name: str, asset_type: str, path: str, description: str = "") -> VisualAsset:
        return VisualAsset(name=name, asset_type=asset_type, path=path, description=description)

    def compare(self, session: VisualVerdictSession, reference: VisualAsset, screenshot: VisualAsset, score: float, diff_notes: str = "") -> VisualComparison:
        comparison = VisualComparison(
            reference=reference,
            screenshot=screenshot,
            score=score,
            threshold=session.threshold,
            diff_notes=diff_notes
        )
        comparison.evaluate()
        session.add_comparison(comparison)
        return comparison

    def needs_retry(self, session: VisualVerdictSession) -> bool:
        return not session.all_pass() and session.comparisons != []

    def next_iteration(self, session: VisualVerdictSession) -> None:
        session.iteration += 1

    def complete(self, session: VisualVerdictSession) -> None:
        session.completed = True

    def generate_report(self, session: VisualVerdictSession) -> VisualVerdictReport:
        return VisualVerdictReport(
            task_description=session.task_description,
            iterations=session.iteration,
            average_score=session.average_score(),
            passed=session.all_pass(),
            threshold=session.threshold,
            summary=(
                f"{'PASS' if session.all_pass() else 'FAIL'} — "
                f"avg score {session.average_score():.1f} (threshold {session.threshold})"
            )
        )
