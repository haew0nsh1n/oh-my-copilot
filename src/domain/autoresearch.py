"""Domain model for bounded research with validation gates."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
from enum import Enum
from datetime import datetime


class ResearchStatus(str, Enum):
    """Status of a research task."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    VALIDATING = "validating"
    COMPLETED = "completed"
    FAILED = "failed"


class EvidenceType(str, Enum):
    """Type of evidence found."""
    DOCUMENTATION = "documentation"
    CODE_EXAMPLE = "code_example"
    REFERENCE = "reference"
    BEST_PRACTICE = "best_practice"
    BENCHMARK = "benchmark"


@dataclass
class ResearchTarget:
    """A target for research."""
    topic: str
    query: str
    keywords: List[str] = field(default_factory=list)
    expected_findings: List[str] = field(default_factory=list)


@dataclass
class Evidence:
    """A piece of evidence found during research."""
    title: str
    evidence_type: EvidenceType
    source: str
    content: str
    found_at: datetime = field(default_factory=datetime.now)
    relevance_score: float = 0.0  # 0.0 to 1.0
    
    def __post_init__(self):
        """Validate evidence."""
        if not self.title or not self.title.strip():
            raise ValueError("Evidence title cannot be empty")
        if self.relevance_score < 0.0 or self.relevance_score > 1.0:
            raise ValueError("Relevance score must be between 0.0 and 1.0")


@dataclass
class ResearchTask:
    """A bounded research task."""
    task_id: str
    target: ResearchTarget
    status: ResearchStatus = ResearchStatus.PENDING
    evidence: List[Evidence] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    max_items: int = 10  # Max evidence items
    min_relevance: float = 0.5  # Minimum relevance score
    
    def add_evidence(self, evidence: Evidence) -> bool:
        """
        Add evidence to the task.
        
        Args:
            evidence: The evidence to add
            
        Returns:
            True if added, False if max items reached
        """
        if len(self.evidence) >= self.max_items:
            return False
        
        if evidence.relevance_score >= self.min_relevance:
            self.evidence.append(evidence)
            return True
        
        return False
    
    def get_high_relevance_evidence(self) -> List[Evidence]:
        """Get high relevance evidence."""
        return [e for e in self.evidence if e.relevance_score >= 0.8]
    
    def is_complete(self) -> bool:
        """Check if research is complete."""
        return len(self.evidence) >= 3  # At least 3 pieces of evidence


@dataclass
class ValidationGate:
    """A validation gate for research results."""
    name: str
    description: str
    validator: str = ""  # Description of validation
    required: bool = True
    
    def __post_init__(self):
        """Validate gate."""
        if not self.name or not self.name.strip():
            raise ValueError("Gate name cannot be empty")


@dataclass
class ResearchReport:
    """Report from research."""
    task_id: str
    topic: str
    status: ResearchStatus
    evidence_count: int = 0
    completed_at: Optional[datetime] = None
    evidence_summary: List[str] = field(default_factory=list)
    validated: bool = False
