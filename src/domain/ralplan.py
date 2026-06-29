"""Domain model for architecture planning and approval."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime


class PlanStatus(str, Enum):
    """Status of a plan."""
    DRAFT = "draft"
    ARCHITECT_REVIEW = "architect_review"
    CRITIC_REVIEW = "critic_review"
    APPROVED = "approved"
    REJECTED = "rejected"


class ReviewRole(str, Enum):
    """Reviewer role."""
    ARCHITECT = "architect"
    CRITIC = "critic"


@dataclass
class ReviewEvidence:
    """Evidence from a reviewer."""
    role: ReviewRole
    reviewer: str
    verdict: str
    reasoning: str
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ArchitecturePlan:
    """A complete architecture and implementation plan."""
    title: str
    description: str
    requirements: List[str] = field(default_factory=list)
    design_decisions: List[str] = field(default_factory=list)
    implementation_steps: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    tradeoffs: List[str] = field(default_factory=list)
    status: PlanStatus = PlanStatus.DRAFT
    evidence: List[ReviewEvidence] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    approved_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate plan."""
        if not self.title or not self.title.strip():
            raise ValueError("Plan title cannot be empty")
    
    def add_evidence(self, evidence: ReviewEvidence) -> None:
        """Add review evidence."""
        self.evidence.append(evidence)
    
    def get_architect_evidence(self) -> Optional[ReviewEvidence]:
        """Get architect review evidence."""
        for e in self.evidence:
            if e.role == ReviewRole.ARCHITECT:
                return e
        return None
    
    def get_critic_evidence(self) -> Optional[ReviewEvidence]:
        """Get critic review evidence."""
        for e in self.evidence:
            if e.role == ReviewRole.CRITIC:
                return e
        return None
    
    def is_architect_approved(self) -> bool:
        """Check if architect approved."""
        evidence = self.get_architect_evidence()
        return evidence is not None and evidence.verdict.lower() in ["approved", "accept"]
    
    def is_critic_approved(self) -> bool:
        """Check if critic approved."""
        evidence = self.get_critic_evidence()
        return evidence is not None and evidence.verdict.lower() in ["approved", "accept"]
    
    def is_ready_for_execution(self) -> bool:
        """Check if plan is approved and ready."""
        return (
            self.status == PlanStatus.APPROVED and
            self.is_architect_approved() and
            self.is_critic_approved()
        )


@dataclass
class RalPlanReport:
    """Report from planning."""
    plan: ArchitecturePlan
    status: PlanStatus
    architect_verdict: Optional[str] = None
    critic_verdict: Optional[str] = None
    ready_for_execution: bool = False
    next_steps: List[str] = field(default_factory=list)
