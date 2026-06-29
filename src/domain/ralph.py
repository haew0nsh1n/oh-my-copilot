"""Domain model for single-owner completion loops."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime


class RalphLoopStatus(str, Enum):
    """Status of a Ralph completion loop."""
    STARTING = "starting"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class LoopIteration:
    """One iteration of the completion loop."""
    iteration_number: int
    owner: str
    description: str
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    success: bool = False
    output: str = ""
    error: str = ""
    
    def complete(self, success: bool = True, output: str = "") -> None:
        """Complete the iteration."""
        self.end_time = datetime.now()
        self.success = success
        self.output = output


@dataclass
class RalphCompletion:
    """Single-owner persistent completion loop."""
    task_title: str
    owner: str
    description: str = ""
    status: RalphLoopStatus = RalphLoopStatus.STARTING
    iterations: List[LoopIteration] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    max_iterations: int = 100  # Safety limit
    
    def __post_init__(self):
        """Validate completion."""
        if not self.task_title or not self.task_title.strip():
            raise ValueError("Task title cannot be empty")
        if not self.owner or not self.owner.strip():
            raise ValueError("Owner cannot be empty")
    
    def add_iteration(self, description: str) -> LoopIteration:
        """Add a new iteration."""
        iteration = LoopIteration(
            iteration_number=len(self.iterations) + 1,
            owner=self.owner,
            description=description
        )
        self.iterations.append(iteration)
        self.status = RalphLoopStatus.IN_PROGRESS
        return iteration
    
    def get_current_iteration(self) -> Optional[LoopIteration]:
        """Get the current iteration."""
        if self.iterations:
            return self.iterations[-1]
        return None
    
    def get_successful_iterations(self) -> List[LoopIteration]:
        """Get successful iterations."""
        return [i for i in self.iterations if i.success]
    
    def can_continue(self) -> bool:
        """Check if loop can continue."""
        return len(self.iterations) < self.max_iterations
    
    def mark_completed(self) -> None:
        """Mark as completed."""
        self.status = RalphLoopStatus.COMPLETED
        self.completed_at = datetime.now()


@dataclass
class RalphReport:
    """Report from Ralph completion."""
    task_title: str
    owner: str
    status: RalphLoopStatus
    total_iterations: int = 0
    successful_iterations: int = 0
    completed_at: Optional[datetime] = None
    summary: str = ""
