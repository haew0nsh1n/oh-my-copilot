"""Domain model for diagnostic session and bug reports."""

from dataclasses import dataclass, field
from typing import List
from enum import Enum
from datetime import datetime


class ErrorSeverity(str, Enum):
    """Severity level of an error."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class DiagnosticStatus(str, Enum):
    """Status of diagnostic investigation."""
    INITIAL = "initial"
    INVESTIGATING = "investigating"
    ROOT_CAUSE_FOUND = "root_cause_found"
    RESOLVED = "resolved"


@dataclass
class ErrorLocation:
    """Where an error occurred."""
    file_path: str
    line_number: int
    function_name: str = ""
    code_snippet: str = ""
    
    def __post_init__(self):
        """Validate location."""
        if not self.file_path or not self.file_path.strip():
            raise ValueError("File path cannot be empty")
        if self.line_number < 1:
            raise ValueError("Line number must be positive")


@dataclass
class ErrorEvidence:
    """Evidence about an error."""
    error_message: str
    error_type: str
    location: ErrorLocation
    timestamp: datetime = field(default_factory=datetime.now)
    context: dict = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate evidence."""
        if not self.error_message or not self.error_message.strip():
            raise ValueError("Error message cannot be empty")
        if not self.error_type or not self.error_type.strip():
            raise ValueError("Error type cannot be empty")


@dataclass
class RootCauseHypothesis:
    """A hypothesis about the root cause of an error."""
    description: str
    confidence: float  # 0.0 to 1.0
    supporting_evidence: List[str] = field(default_factory=list)
    contradicting_evidence: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate hypothesis."""
        if not self.description or not self.description.strip():
            raise ValueError("Description cannot be empty")
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError("Confidence must be between 0.0 and 1.0")


@dataclass
class DiagnosticSession:
    """A diagnostic session for investigating errors."""
    error_summary: str
    severity: ErrorSeverity
    evidence: List[ErrorEvidence] = field(default_factory=list)
    hypotheses: List[RootCauseHypothesis] = field(default_factory=list)
    selected_hypothesis: RootCauseHypothesis | None = None
    status: DiagnosticStatus = DiagnosticStatus.INITIAL
    resolution_steps: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate session."""
        if not self.error_summary or not self.error_summary.strip():
            raise ValueError("Error summary cannot be empty")
    
    def add_evidence(self, evidence: ErrorEvidence) -> None:
        """Add evidence to the diagnostic session."""
        if evidence in self.evidence:
            raise ValueError("Evidence already exists")
        self.evidence.append(evidence)
        self.status = DiagnosticStatus.INVESTIGATING
    
    def add_hypothesis(self, hypothesis: RootCauseHypothesis) -> None:
        """Add a root cause hypothesis."""
        if hypothesis in self.hypotheses:
            raise ValueError("Hypothesis already exists")
        self.hypotheses.append(hypothesis)
    
    def select_hypothesis(self, hypothesis: RootCauseHypothesis) -> None:
        """Select the most likely root cause hypothesis."""
        if hypothesis not in self.hypotheses:
            raise ValueError("Hypothesis not in session")
        self.selected_hypothesis = hypothesis
        self.status = DiagnosticStatus.ROOT_CAUSE_FOUND
    
    def add_resolution_step(self, step: str) -> None:
        """Add a step to resolve the issue."""
        if not step or not step.strip():
            raise ValueError("Resolution step cannot be empty")
        self.resolution_steps.append(step)


@dataclass
class DiagnosticReport:
    """Final report from a diagnostic session."""
    session: DiagnosticSession
    root_cause: str
    affected_components: List[str] = field(default_factory=list)
    workaround: str = ""
    permanent_fix: str = ""
    prevention_measures: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate report."""
        if not self.root_cause or not self.root_cause.strip():
            raise ValueError("Root cause cannot be empty")
