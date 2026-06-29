"""Domain model for ultragoal execution."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List
from enum import Enum
from datetime import datetime


class GoalStatus(str, Enum):
    """Status of a goal."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"


class GoalPriority(str, Enum):
    """Priority of a goal."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class GoalCheckpoint:
    """A checkpoint for goal verification."""
    name: str
    description: str
    completed: bool = False
    completed_at: datetime = None
    verification_notes: str = ""
    
    def __post_init__(self):
        """Validate checkpoint."""
        if not self.name or not self.name.strip():
            raise ValueError("Checkpoint name cannot be empty")
    
    def mark_complete(self, notes: str = "") -> None:
        """Mark checkpoint as complete."""
        self.completed = True
        self.completed_at = datetime.now()
        self.verification_notes = notes


@dataclass
class Goal:
    """A single goal in an ultragoal story."""
    title: str
    description: str
    acceptance_criteria: List[str] = field(default_factory=list)
    checkpoints: List[GoalCheckpoint] = field(default_factory=list)
    status: GoalStatus = GoalStatus.PENDING
    priority: GoalPriority = GoalPriority.MEDIUM
    depends_on: List[str] = field(default_factory=list)  # Goal IDs
    owner: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    started_at: datetime = None
    completed_at: datetime = None
    
    def __post_init__(self):
        """Validate goal."""
        if not self.title or not self.title.strip():
            raise ValueError("Goal title cannot be empty")
        if not self.description or not self.description.strip():
            raise ValueError("Goal description cannot be empty")
    
    def add_checkpoint(self, checkpoint: GoalCheckpoint) -> None:
        """Add a checkpoint."""
        if checkpoint in self.checkpoints:
            raise ValueError("Checkpoint already exists")
        self.checkpoints.append(checkpoint)
    
    def add_criterion(self, criterion: str) -> None:
        """Add an acceptance criterion."""
        if criterion not in self.acceptance_criteria:
            self.acceptance_criteria.append(criterion)
    
    def start(self) -> None:
        """Mark goal as started."""
        self.status = GoalStatus.IN_PROGRESS
        self.started_at = datetime.now()
    
    def complete(self) -> None:
        """Mark goal as completed."""
        self.status = GoalStatus.COMPLETED
        self.completed_at = datetime.now()
    
    def block(self) -> None:
        """Mark goal as blocked."""
        self.status = GoalStatus.BLOCKED
    
    def fail(self) -> None:
        """Mark goal as failed."""
        self.status = GoalStatus.FAILED


@dataclass
class Ultragoal:
    """A durable multi-goal execution ledger."""
    name: str
    description: str
    goals: List[Goal] = field(default_factory=list)
    status: GoalStatus = GoalStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime = None
    metadata: dict = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate ultragoal."""
        if not self.name or not self.name.strip():
            raise ValueError("Ultragoal name cannot be empty")
        if not self.description or not self.description.strip():
            raise ValueError("Ultragoal description cannot be empty")
    
    def add_goal(self, goal: Goal) -> None:
        """Add a goal to the ultragoal."""
        if goal in self.goals:
            raise ValueError("Goal already exists in ultragoal")
        self.goals.append(goal)
    
    def get_goal(self, title: str) -> Goal:
        """Get a goal by title."""
        for goal in self.goals:
            if goal.title == title:
                return goal
        raise ValueError(f"Goal '{title}' not found")
    
    def get_completed_goals(self) -> List[Goal]:
        """Get all completed goals."""
        return [g for g in self.goals if g.status == GoalStatus.COMPLETED]
    
    def get_pending_goals(self) -> List[Goal]:
        """Get all pending goals."""
        return [g for g in self.goals if g.status == GoalStatus.PENDING]
    
    def get_in_progress_goals(self) -> List[Goal]:
        """Get all in-progress goals."""
        return [g for g in self.goals if g.status == GoalStatus.IN_PROGRESS]
    
    def get_blocked_goals(self) -> List[Goal]:
        """Get all blocked goals."""
        return [g for g in self.goals if g.status == GoalStatus.BLOCKED]
    
    def completion_percentage(self) -> float:
        """Get completion percentage."""
        if not self.goals:
            return 0.0
        completed = len(self.get_completed_goals())
        return (completed / len(self.goals)) * 100


@dataclass
class UltragoalReport:
    """Report on ultragoal progress."""
    ultragoal: Ultragoal
    total_goals: int
    completed_goals: int
    in_progress_goals: int
    pending_goals: int
    blocked_goals: int
    completion_percentage: float
    summary: str = ""
    
    def __post_init__(self):
        """Validate report."""
        if self.completion_percentage < 0 or self.completion_percentage > 100:
            raise ValueError("Completion percentage must be 0-100")


@dataclass(frozen=True)
class UltragoalArtifact:
    """Durable artifact paths for an artifact-only ultragoal ledger."""

    root: Path
    brief_path: Path
    goals_path: Path
    ledger_path: Path
    plan_id: str = ""
