"""Domain model for team runtime execution."""

from dataclasses import dataclass, field
from typing import List, Dict, Callable
from enum import Enum
from datetime import datetime
from pathlib import Path
import uuid


class WorkerStatus(str, Enum):
    """Status of a worker."""
    IDLE = "idle"
    WORKING = "working"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class TeamStatus(str, Enum):
    """Status of a team."""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class TeamProvider(str, Enum):
    """Supported terminal provider team targets."""
    CLAUDE = "claude"
    CODEX = "codex"
    GEMINI = "gemini"
    ANTIGRAVITY = "antigravity"
    GROK = "grok"
    CURSOR = "cursor"


class TeamRequirementStatus(str, Enum):
    """Provider team runtime requirement status."""
    READY = "ready"
    BLOCKED = "blocked"


class TeamControlAction(str, Enum):
    """Provider team control action."""
    STATUS = "status"
    SHUTDOWN = "shutdown"


@dataclass
class ProviderTeamRequest:
    """A prepared provider-backed team request."""
    worker_count: int
    provider: TeamProvider
    goal_description: str
    command_preview: str = ""

    def __post_init__(self):
        """Validate provider team request."""
        if self.worker_count < 1:
            raise ValueError("Worker count must be at least 1")
        if not self.goal_description or not self.goal_description.strip():
            raise ValueError("Goal description cannot be empty")
        if not self.command_preview:
            self.command_preview = (
                f"omp team {self.worker_count}:{self.provider.value} {self.goal_description}"
            )


@dataclass(frozen=True)
class ProviderTeamReadiness:
    """Readiness check for provider-backed team execution."""
    request: ProviderTeamRequest
    status: TeamRequirementStatus
    provider_executable: str = ""
    tmux_executable: str = ""


@dataclass(frozen=True)
class TeamControlRequest:
    """Prepared provider team control request."""
    action: TeamControlAction
    team_name: str
    command_preview: str = ""

    def __post_init__(self):
        """Validate team control request."""
        if not self.team_name or not self.team_name.strip():
            raise ValueError("Team name cannot be empty")
        if not self.command_preview:
            object.__setattr__(
                self,
                "command_preview",
                f"omp team {self.action.value} {self.team_name}",
            )


@dataclass(frozen=True)
class TeamControlArtifact:
    """Persisted provider team control state."""
    action: TeamControlAction
    path: Path


@dataclass
class WorkerTask:
    """A task assigned to a worker."""
    task_id: str
    description: str
    worker_id: str
    status: WorkerStatus = WorkerStatus.IDLE
    started_at: datetime = None
    completed_at: datetime = None
    result: str = ""
    error: str = ""
    progress: int = 0  # 0-100
    
    def __post_init__(self):
        """Validate task."""
        if not self.description or not self.description.strip():
            raise ValueError("Task description cannot be empty")
    
    def start(self) -> None:
        """Mark task as started."""
        self.status = WorkerStatus.WORKING
        self.started_at = datetime.now()
    
    def complete(self, result: str = "") -> None:
        """Mark task as completed."""
        self.status = WorkerStatus.COMPLETED
        self.completed_at = datetime.now()
        self.result = result
        self.progress = 100
    
    def fail(self, error: str = "") -> None:
        """Mark task as failed."""
        self.status = WorkerStatus.FAILED
        self.error = error
        self.completed_at = datetime.now()
    
    def update_progress(self, progress: int) -> None:
        """Update task progress."""
        if progress < 0 or progress > 100:
            raise ValueError("Progress must be 0-100")
        self.progress = progress


@dataclass
class Worker:
    """A worker in a team."""
    worker_id: str
    name: str
    role: str = "executor"
    status: WorkerStatus = WorkerStatus.IDLE
    assigned_tasks: List[WorkerTask] = field(default_factory=list)
    completed_tasks: int = 0
    failed_tasks: int = 0
    
    def __post_init__(self):
        """Validate worker."""
        if not self.name or not self.name.strip():
            raise ValueError("Worker name cannot be empty")
    
    def assign_task(self, task: WorkerTask) -> None:
        """Assign a task to this worker."""
        if task in self.assigned_tasks:
            raise ValueError("Task already assigned")
        self.assigned_tasks.append(task)
    
    def get_current_task(self) -> WorkerTask:
        """Get the current task."""
        for task in self.assigned_tasks:
            if task.status == WorkerStatus.WORKING:
                return task
        return None
    
    def get_completed_tasks(self) -> List[WorkerTask]:
        """Get all completed tasks."""
        return [t for t in self.assigned_tasks if t.status == WorkerStatus.COMPLETED]
    
    def get_failed_tasks(self) -> List[WorkerTask]:
        """Get all failed tasks."""
        return [t for t in self.assigned_tasks if t.status == WorkerStatus.FAILED]


@dataclass
class Team:
    """A team of workers."""
    team_id: str
    name: str
    goal_description: str
    workers: List[Worker] = field(default_factory=list)
    status: TeamStatus = TeamStatus.IDLE
    created_at: datetime = field(default_factory=datetime.now)
    started_at: datetime = None
    completed_at: datetime = None
    tasks: List[WorkerTask] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate team."""
        if not self.name or not self.name.strip():
            raise ValueError("Team name cannot be empty")
        if not self.goal_description or not self.goal_description.strip():
            raise ValueError("Goal description cannot be empty")
    
    def add_worker(self, worker: Worker) -> None:
        """Add a worker to the team."""
        if worker in self.workers:
            raise ValueError("Worker already in team")
        self.workers.append(worker)
    
    def get_worker(self, worker_id: str) -> Worker:
        """Get a worker by ID."""
        for worker in self.workers:
            if worker.worker_id == worker_id:
                return worker
        return None
    
    def add_task(self, task: WorkerTask) -> None:
        """Add a task to the team."""
        if task in self.tasks:
            raise ValueError("Task already in team")
        self.tasks.append(task)
    
    def get_pending_tasks(self) -> List[WorkerTask]:
        """Get all pending tasks."""
        return [t for t in self.tasks if t.status == WorkerStatus.IDLE]
    
    def get_in_progress_tasks(self) -> List[WorkerTask]:
        """Get all in-progress tasks."""
        return [t for t in self.tasks if t.status == WorkerStatus.WORKING]
    
    def get_completed_tasks(self) -> List[WorkerTask]:
        """Get all completed tasks."""
        return [t for t in self.tasks if t.status == WorkerStatus.COMPLETED]
    
    def get_failed_tasks(self) -> List[WorkerTask]:
        """Get all failed tasks."""
        return [t for t in self.tasks if t.status == WorkerStatus.FAILED]
    
    def start(self) -> None:
        """Start the team."""
        self.status = TeamStatus.RUNNING
        self.started_at = datetime.now()
    
    def pause(self) -> None:
        """Pause the team."""
        self.status = TeamStatus.PAUSED
    
    def complete(self) -> None:
        """Mark team as completed."""
        self.status = TeamStatus.COMPLETED
        self.completed_at = datetime.now()
    
    def fail(self) -> None:
        """Mark team as failed."""
        self.status = TeamStatus.FAILED
        self.completed_at = datetime.now()
    
    def completion_percentage(self) -> float:
        """Get team completion percentage."""
        if not self.tasks:
            return 0.0
        completed = len(self.get_completed_tasks())
        return (completed / len(self.tasks)) * 100


@dataclass
class TeamReport:
    """Report on team execution."""
    team: Team
    total_workers: int
    total_tasks: int
    completed_tasks: int
    in_progress_tasks: int
    pending_tasks: int
    failed_tasks: int
    completion_percentage: float
    summary: str = ""
    
    def __post_init__(self):
        """Validate report."""
        if self.completion_percentage < 0 or self.completion_percentage > 100:
            raise ValueError("Completion percentage must be 0-100")
