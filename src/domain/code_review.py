"""Domain model for code review and quality assessment."""

from dataclasses import dataclass, field
from typing import List
from enum import Enum


class ReviewAspect(str, Enum):
    """Aspects of code to review."""
    STANDARDS = "standards"
    SPEC = "spec"
    PERFORMANCE = "performance"
    SECURITY = "security"
    TESTABILITY = "testability"


class ReviewStatus(str, Enum):
    """Status of a code review."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    CHANGES_REQUESTED = "changes_requested"
    BLOCKED = "blocked"


class FindingSeverity(str, Enum):
    """Severity of a review finding."""
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    SUGGESTION = "suggestion"


@dataclass
class ReviewFinding:
    """A finding from code review."""
    location: str  # file:line or file:function
    description: str
    severity: FindingSeverity
    aspect: ReviewAspect
    suggestion: str = ""
    
    def __post_init__(self):
        """Validate finding."""
        if not self.location or not self.location.strip():
            raise ValueError("Location cannot be empty")
        if not self.description or not self.description.strip():
            raise ValueError("Description cannot be empty")


@dataclass
class ReviewSection:
    """A section of code under review."""
    name: str
    files: List[str] = field(default_factory=list)
    lines_changed: int = 0
    description: str = ""
    
    def __post_init__(self):
        """Validate section."""
        if not self.name or not self.name.strip():
            raise ValueError("Section name cannot be empty")


@dataclass
class CodeReview:
    """A code review for changes."""
    title: str
    sections: List[ReviewSection] = field(default_factory=list)
    findings: List[ReviewFinding] = field(default_factory=list)
    status: ReviewStatus = ReviewStatus.PENDING
    context: dict = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate review."""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
    
    def add_section(self, section: ReviewSection) -> None:
        """Add a section to review."""
        if section in self.sections:
            raise ValueError("Section already exists")
        self.sections.append(section)
    
    def add_finding(self, finding: ReviewFinding) -> None:
        """Add a finding to the review."""
        self.findings.append(finding)
        self.status = ReviewStatus.IN_PROGRESS
    
    def approve(self) -> None:
        """Approve the review if no critical/major findings."""
        critical_major = [
            f for f in self.findings
            if f.severity in (FindingSeverity.CRITICAL, FindingSeverity.MAJOR)
        ]
        if critical_major:
            self.status = ReviewStatus.CHANGES_REQUESTED
        else:
            self.status = ReviewStatus.APPROVED
    
    def get_findings_by_severity(self, severity: FindingSeverity) -> List[ReviewFinding]:
        """Get all findings of a specific severity."""
        return [f for f in self.findings if f.severity == severity]


@dataclass
class ReviewReport:
    """Final review report."""
    review: CodeReview
    total_findings: int
    critical_findings: int
    major_findings: int
    minor_findings: int
    suggestions: int
    recommendation: str
    summary: str = ""
    
    def __post_init__(self):
        """Validate report."""
        if not self.recommendation or not self.recommendation.strip():
            raise ValueError("Recommendation cannot be empty")
