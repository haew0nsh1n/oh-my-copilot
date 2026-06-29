"""VisualRalph skill — measured visual-reference implementation loop."""

from typing import Optional
from domain import (
    VisualRalphSession, VisualIteration,
    VisualRalphStatus, VisualRalphReport,
)


class VisualRalphSkill:
    name = "visual_ralph"
    description = "Measured visual-reference implementation loop (threshold: 90+)"

    def __init__(self):
        self.sessions: dict = {}

    def create_session(self, task_description: str, reference_description: str, threshold: float = 90.0) -> VisualRalphSession:
        session = VisualRalphSession(
            task_description=task_description,
            reference_description=reference_description,
            threshold=threshold
        )
        self.sessions[task_description] = session
        return session

    def start_iteration(self, session: VisualRalphSession, description: str) -> VisualIteration:
        session.status = VisualRalphStatus.IMPLEMENTING
        return session.add_iteration(description)

    def score_iteration(self, session: VisualRalphSession, iteration: VisualIteration, score: float, notes: str = "") -> None:
        session.status = VisualRalphStatus.COMPARING
        iteration.evaluate(score)
        iteration.notes = notes
        if not iteration.passed:
            session.status = VisualRalphStatus.REFINING

    def is_passing(self, session: VisualRalphSession) -> bool:
        return session.is_passing()

    def complete(self, session: VisualRalphSession) -> None:
        session.mark_completed()

    def fail(self, session: VisualRalphSession) -> None:
        session.status = VisualRalphStatus.FAILED
        from datetime import datetime
        session.completed_at = datetime.now()

    def generate_report(self, session: VisualRalphSession) -> VisualRalphReport:
        return VisualRalphReport(
            task_description=session.task_description,
            status=session.status,
            total_iterations=len(session.iterations),
            best_score=session.best_score(),
            threshold=session.threshold,
            passed=session.is_passing(),
            summary=(
                f"{'PASS' if session.is_passing() else 'FAIL'} after {len(session.iterations)} iterations "
                f"(best: {session.best_score():.1f}, threshold: {session.threshold})"
            )
        )

    def get_session(self, task_description: str) -> Optional[VisualRalphSession]:
        return self.sessions.get(task_description)
