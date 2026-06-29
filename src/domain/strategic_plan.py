"""Domain model for simple strategic planning."""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class PlanPhase(str, Enum):
    """Phases in a plan."""
    DISCOVERY = "discovery"
    STRATEGY = "strategy"
    EXECUTION = "execution"
    VALIDATION = "validation"


class StrategyPlanStatus(str, Enum):
    """Status of a strategy plan."""
    DRAFT = "draft"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


@dataclass
class PlanObjective:
    """An objective within a plan."""
    title: str
    description: str
    phase: PlanPhase = PlanPhase.STRATEGY
    status: StrategyPlanStatus = StrategyPlanStatus.DRAFT
    dependencies: List[str] = field(default_factory=list)
    estimated_hours: float = 0.0
    completed_at: Optional[datetime] = None


@dataclass
class StrategicPlan:
    """A high-level strategic plan (simpler than RalPlan)."""
    title: str
    vision: str
    goals: List[str] = field(default_factory=list)
    objectives: List[PlanObjective] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    status: StrategyPlanStatus = StrategyPlanStatus.DRAFT
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    approval_notes: str = ""
    
    def __post_init__(self):
        """Validate plan."""
        if not self.title or not self.title.strip():
            raise ValueError("Plan title cannot be empty")
        if not self.vision or not self.vision.strip():
            raise ValueError("Plan vision cannot be empty")
    
    def add_goal(self, goal: str) -> None:
        """Add a goal."""
        self.goals.append(goal)
    
    def add_objective(self, objective: PlanObjective) -> None:
        """Add an objective."""
        self.objectives.append(objective)
    
    def add_constraint(self, constraint: str) -> None:
        """Add a constraint."""
        self.constraints.append(constraint)
    
    def add_assumption(self, assumption: str) -> None:
        """Add an assumption."""
        self.assumptions.append(assumption)
    
    def get_objectives_by_phase(self, phase: PlanPhase) -> List[PlanObjective]:
        """Get objectives for a phase."""
        return [o for o in self.objectives if o.phase == phase]
    
    def get_total_estimated_hours(self) -> float:
        """Get total estimated hours."""
        return sum(o.estimated_hours for o in self.objectives)
    
    def mark_approved(self, notes: str = "") -> None:
        """Mark plan as approved."""
        self.status = StrategyPlanStatus.APPROVED
        self.approval_notes = notes
        self.updated_at = datetime.now()


@dataclass
class StrategicPlanReport:
    """Report from strategic planning."""
    title: str
    vision: str
    status: StrategyPlanStatus
    goal_count: int = 0
    objective_count: int = 0
    total_estimated_hours: float = 0.0
    summary: str = ""
