"""Domain model for goal-mode research missions."""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class ResearchGoalStatus(str, Enum):
    """Status of a research goal."""
    STARTING = "starting"
    IN_PROGRESS = "in_progress"
    VALIDATING = "validating"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ResearchMission:
    """A research mission with goal-mode focus."""
    title: str
    research_focus: str
    professor_prompt: str = ""  # Professor-style guidance
    critic_prompt: str = ""  # Critic-style challenge
    status: ResearchGoalStatus = ResearchGoalStatus.STARTING
    findings: List[str] = field(default_factory=list)
    validations: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate mission."""
        if not self.title or not self.title.strip():
            raise ValueError("Mission title cannot be empty")
        if not self.research_focus or not self.research_focus.strip():
            raise ValueError("Research focus cannot be empty")
    
    def add_finding(self, finding: str) -> None:
        """Add a finding."""
        self.findings.append(finding)
    
    def add_validation(self, validation: str) -> None:
        """Add a validation result."""
        self.validations.append(validation)
    
    def get_findings_count(self) -> int:
        """Get number of findings."""
        return len(self.findings)
    
    def get_validations_count(self) -> int:
        """Get number of validations."""
        return len(self.validations)
    
    def is_complete(self) -> bool:
        """Check if mission is complete."""
        return (
            len(self.findings) > 0 and
            len(self.validations) > 0 and
            self.status == ResearchGoalStatus.COMPLETED
        )


@dataclass
class ProfessorReview:
    """Professor-style guidance review."""
    mission: ResearchMission
    guidance: str
    recommended_next_steps: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class CriticReview:
    """Critic-style challenge review."""
    mission: ResearchMission
    challenges: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ResearchGoalReport:
    """Report from research goal."""
    title: str
    status: ResearchGoalStatus
    findings_count: int = 0
    validations_count: int = 0
    completed_at: Optional[datetime] = None
    summary: str = ""
    is_complete: bool = False
