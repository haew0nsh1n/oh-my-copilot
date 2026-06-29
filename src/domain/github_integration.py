"""Domain model for GitHub integration."""

from dataclasses import dataclass, field
from typing import List
from enum import Enum


class IssueType(str, Enum):
    """Type of GitHub issue."""
    BUG = "bug"
    FEATURE = "feature"
    TASK = "task"
    DOCUMENTATION = "documentation"


class IssuePriority(str, Enum):
    """Priority level."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class GitHubIssue:
    """A GitHub issue representation."""
    title: str
    description: str
    issue_type: IssueType = IssueType.TASK
    priority: IssuePriority = IssuePriority.MEDIUM
    labels: List[str] = field(default_factory=list)
    assignee: str = ""
    
    def __post_init__(self):
        """Validate issue."""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        if not self.description or not self.description.strip():
            raise ValueError("Description cannot be empty")
    
    def add_label(self, label: str) -> None:
        """Add a label to the issue."""
        if label not in self.labels:
            self.labels.append(label)


@dataclass
class GitHubRepository:
    """A GitHub repository."""
    owner: str
    name: str
    description: str = ""
    
    def __post_init__(self):
        """Validate repository."""
        if not self.owner or not self.owner.strip():
            raise ValueError("Owner cannot be empty")
        if not self.name or not self.name.strip():
            raise ValueError("Name cannot be empty")
    
    @property
    def full_name(self) -> str:
        """Get full repository name."""
        return f"{self.owner}/{self.name}"
