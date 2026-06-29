"""Ultrawork skill — max parallel execution."""

from typing import List, Optional
from domain import (
    UltraworkSession, WorkLane, UltraworkStatus, LaneStatus, UltraworkReport,
)


class UltraworkSkill:
    name = "ultrawork"
    description = "Max parallel execution across independent lanes"

    def __init__(self):
        self.sessions: dict = {}

    def create_session(self, goal: str) -> UltraworkSession:
        session = UltraworkSession(goal=goal)
        session.status = UltraworkStatus.RUNNING
        self.sessions[goal] = session
        return session

    def add_lane(self, session: UltraworkSession, lane_id: str, description: str, worker_hint: str = "") -> WorkLane:
        lane = WorkLane(lane_id=lane_id, description=description, worker_hint=worker_hint)
        session.add_lane(lane)
        return lane

    def start_lane(self, lane: WorkLane) -> None:
        lane.start()

    def complete_lane(self, lane: WorkLane, output: str = "") -> None:
        lane.complete(output)

    def fail_lane(self, lane: WorkLane, reason: str = "") -> None:
        lane.fail(reason)

    def complete_session(self, session: UltraworkSession) -> None:
        session.status = UltraworkStatus.COMPLETED
        from datetime import datetime
        session.completed_at = datetime.now()

    def generate_report(self, session: UltraworkSession) -> UltraworkReport:
        completed = session.get_completed_lanes()
        failed = [l for l in session.lanes if l.status == LaneStatus.FAILED]
        return UltraworkReport(
            goal=session.goal,
            status=session.status,
            total_lanes=len(session.lanes),
            completed_lanes=len(completed),
            failed_lanes=len(failed),
            summary=f"{len(completed)}/{len(session.lanes)} lanes completed ({session.completion_rate():.0%})"
        )

    def get_session(self, goal: str) -> Optional[UltraworkSession]:
        return self.sessions.get(goal)
