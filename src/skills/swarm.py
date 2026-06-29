"""Swarm skill — team compatibility facade over TeamRuntime."""

from typing import Optional
from domain import (
    SwarmSession, SwarmWorker, SwarmTask, SwarmStatus, SwarmReport,
)


class SwarmSkill:
    name = "swarm"
    description = "Team compatibility facade — same API as $team but with swarm semantics"

    def __init__(self):
        self.sessions: dict = {}

    def create_session(self, goal: str, worker_count: int = 3) -> SwarmSession:
        import uuid
        session = SwarmSession(goal=goal, worker_count=worker_count)
        session.status = SwarmStatus.RUNNING
        # Auto-create workers
        for i in range(worker_count):
            worker = SwarmWorker(worker_id=str(uuid.uuid4())[:8], role=f"worker-{i+1}")
            session.add_worker(worker)
        self.sessions[goal] = session
        return session

    def add_task(self, session: SwarmSession, task_id: str, description: str) -> SwarmTask:
        task = SwarmTask(task_id=task_id, description=description)
        session.add_task(task)
        return task

    def assign_task(self, task: SwarmTask, worker: SwarmWorker) -> None:
        task.assigned_to = worker.worker_id
        worker.assigned_task = task.task_id

    def complete_task(self, task: SwarmTask, output: str = "") -> None:
        task.completed = True
        task.output = output

    def complete_session(self, session: SwarmSession) -> None:
        session.status = SwarmStatus.COMPLETED
        from datetime import datetime
        session.completed_at = datetime.now()

    def generate_report(self, session: SwarmSession) -> SwarmReport:
        completed = session.get_completed_tasks()
        return SwarmReport(
            goal=session.goal,
            worker_count=len(session.workers),
            status=session.status,
            total_tasks=len(session.tasks),
            completed_tasks=len(completed),
            summary=f"Swarm: {len(completed)}/{len(session.tasks)} tasks done with {len(session.workers)} workers"
        )

    def get_session(self, goal: str) -> Optional[SwarmSession]:
        return self.sessions.get(goal)
