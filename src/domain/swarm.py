"""Domain model for swarm (team compatibility facade)."""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class SwarmStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class SwarmWorker:
    worker_id: str
    role: str
    assigned_task: str = ""
    completed: bool = False


@dataclass
class SwarmTask:
    task_id: str
    description: str
    assigned_to: str = ""
    completed: bool = False
    output: str = ""


@dataclass
class SwarmSession:
    """Facade over TeamRuntime for backward compatibility."""
    goal: str
    worker_count: int = 3
    workers: List[SwarmWorker] = field(default_factory=list)
    tasks: List[SwarmTask] = field(default_factory=list)
    status: SwarmStatus = SwarmStatus.IDLE
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.goal or not self.goal.strip():
            raise ValueError("Goal cannot be empty")

    def add_worker(self, worker: SwarmWorker) -> None:
        self.workers.append(worker)

    def add_task(self, task: SwarmTask) -> None:
        self.tasks.append(task)

    def get_completed_tasks(self) -> List[SwarmTask]:
        return [t for t in self.tasks if t.completed]

    def completion_rate(self) -> float:
        if not self.tasks:
            return 0.0
        return len(self.get_completed_tasks()) / len(self.tasks)


@dataclass
class SwarmReport:
    goal: str
    worker_count: int
    status: SwarmStatus
    total_tasks: int = 0
    completed_tasks: int = 0
    summary: str = ""
