"""Domain model for visual reference implementation loop."""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class VisualRalphStatus(str, Enum):
    STARTING = "starting"
    IMPLEMENTING = "implementing"
    COMPARING = "comparing"
    REFINING = "refining"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class VisualIteration:
    iteration_number: int
    description: str
    score: float = 0.0
    threshold: float = 90.0
    notes: str = ""
    passed: bool = False
    timestamp: datetime = field(default_factory=datetime.now)

    def evaluate(self, score: float) -> None:
        self.score = score
        self.passed = score >= self.threshold


@dataclass
class VisualRalphSession:
    """Measured visual-reference implementation loop."""
    task_description: str
    reference_description: str
    threshold: float = 90.0
    status: VisualRalphStatus = VisualRalphStatus.STARTING
    iterations: List[VisualIteration] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.task_description or not self.task_description.strip():
            raise ValueError("Task description cannot be empty")

    def add_iteration(self, description: str) -> VisualIteration:
        iteration = VisualIteration(
            iteration_number=len(self.iterations) + 1,
            description=description,
            threshold=self.threshold
        )
        self.iterations.append(iteration)
        self.status = VisualRalphStatus.IMPLEMENTING
        return iteration

    def best_score(self) -> float:
        if not self.iterations:
            return 0.0
        return max(i.score for i in self.iterations)

    def is_passing(self) -> bool:
        return any(i.passed for i in self.iterations)

    def mark_completed(self) -> None:
        self.status = VisualRalphStatus.COMPLETED
        self.completed_at = datetime.now()


@dataclass
class VisualRalphReport:
    task_description: str
    status: VisualRalphStatus
    total_iterations: int = 0
    best_score: float = 0.0
    threshold: float = 90.0
    passed: bool = False
    summary: str = ""
