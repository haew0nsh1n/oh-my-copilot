"""Domain model for autopilot autonomous execution."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime


class AutopilotPhase(str, Enum):
    """Phases in autopilot execution."""
    INTERVIEW = "interview"
    PLANNING = "planning"
    EXECUTION = "execution"
    REVIEW = "review"
    QA = "qa"
    CLEANUP = "cleanup"
    COMPLETE = "complete"


class AutopilotStatus(str, Enum):
    """Status of autopilot run."""
    STARTING = "starting"
    IN_PROGRESS = "in_progress"
    REPLANNING = "replanning"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AutopilotPhaseResult:
    """Result from one phase of autopilot."""
    phase: AutopilotPhase
    success: bool
    output: str = ""
    error: str = ""
    duration_seconds: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class AutopilotWorkflow:
    """Autonomous execution workflow that loops until complete."""
    task_description: str
    status: AutopilotStatus = AutopilotStatus.STARTING
    current_phase: AutopilotPhase = AutopilotPhase.INTERVIEW
    phase_results: List[AutopilotPhaseResult] = field(default_factory=list)
    replan_count: int = 0
    max_replans: int = 3  # Prevent infinite loops
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate workflow."""
        if not self.task_description or not self.task_description.strip():
            raise ValueError("Task description cannot be empty")
    
    def add_phase_result(self, result: AutopilotPhaseResult) -> None:
        """Add a phase result."""
        self.phase_results.append(result)
    
    def get_phase_results(self, phase: AutopilotPhase) -> List[AutopilotPhaseResult]:
        """Get all results for a specific phase."""
        return [r for r in self.phase_results if r.phase == phase]
    
    def can_replan(self) -> bool:
        """Check if we can replan."""
        return self.replan_count < self.max_replans
    
    def should_replan(self) -> bool:
        """Check if review/QA requires replanning."""
        # If code review or QA failed, we need to replan
        review_results = self.get_phase_results(AutopilotPhase.REVIEW)
        qa_results = self.get_phase_results(AutopilotPhase.QA)
        
        return any(not r.success for r in review_results + qa_results)
    
    def mark_completed(self) -> None:
        """Mark workflow as completed."""
        self.status = AutopilotStatus.COMPLETED
        self.current_phase = AutopilotPhase.COMPLETE
        self.completed_at = datetime.now()


@dataclass
class AutopilotReport:
    """Report from autopilot execution."""
    task_description: str
    status: AutopilotStatus
    total_phases: int = 0
    successful_phases: int = 0
    replan_count: int = 0
    completed_at: Optional[datetime] = None
    summary: str = ""
    phase_breakdown: Dict[str, bool] = field(default_factory=dict)
