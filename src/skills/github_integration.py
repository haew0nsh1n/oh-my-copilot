"""GitHub integration skill."""

from typing import List, Optional
from domain import GitHubIssue, GitHubRepository, IssueType, IssuePriority


class GitHubIntegrationSkill:
    """
    A skill for GitHub integration.
    
    This skill helps:
    - Create issues from diagnostic reports
    - File bug reports
    - Create feature requests
    - Link architecture decisions to issues
    """
    
    def __init__(self):
        """Initialize the GitHub integration skill."""
        self.name = "github-integration"
        self.description = "Create and manage GitHub issues"
    
    def create_issue(
        self,
        title: str,
        description: str,
        issue_type: IssueType = IssueType.TASK,
        priority: IssuePriority = IssuePriority.MEDIUM,
        labels: List[str] | None = None,
    ) -> GitHubIssue:
        """
        Create a new GitHub issue.
        
        Args:
            title: Issue title
            description: Issue description
            issue_type: Type of issue (bug, feature, task, doc)
            priority: Priority level
            labels: Optional labels
            
        Returns:
            A GitHubIssue
        """
        issue = GitHubIssue(
            title=title,
            description=description,
            issue_type=issue_type,
            priority=priority,
            labels=labels or []
        )
        return issue
    
    def create_bug_report(
        self,
        title: str,
        description: str,
        root_cause: str,
        reproduction_steps: List[str] | None = None,
        priority: IssuePriority = IssuePriority.HIGH,
    ) -> GitHubIssue:
        """
        Create a bug report issue.
        
        Args:
            title: Bug title
            description: Bug description
            root_cause: Root cause analysis
            reproduction_steps: Steps to reproduce
            priority: Priority level
            
        Returns:
            A GitHubIssue configured as a bug report
        """
        full_description = f"{description}\n\n## Root Cause\n{root_cause}"
        
        if reproduction_steps:
            full_description += "\n\n## Reproduction Steps\n"
            for i, step in enumerate(reproduction_steps, 1):
                full_description += f"{i}. {step}\n"
        
        issue = GitHubIssue(
            title=title,
            description=full_description,
            issue_type=IssueType.BUG,
            priority=priority,
            labels=["bug", "from-diagnostic"]
        )
        return issue
    
    def create_feature_request(
        self,
        title: str,
        description: str,
        acceptance_criteria: List[str] | None = None,
    ) -> GitHubIssue:
        """
        Create a feature request issue.
        
        Args:
            title: Feature title
            description: Feature description
            acceptance_criteria: Criteria for completion
            
        Returns:
            A GitHubIssue configured as a feature request
        """
        full_description = description
        
        if acceptance_criteria:
            full_description += "\n\n## Acceptance Criteria\n"
            for criterion in acceptance_criteria:
                full_description += f"- [ ] {criterion}\n"
        
        issue = GitHubIssue(
            title=title,
            description=full_description,
            issue_type=IssueType.FEATURE,
            labels=["enhancement"]
        )
        return issue
    
    def create_repository(
        self,
        owner: str,
        name: str,
        description: str = ""
    ) -> GitHubRepository:
        """
        Create a repository reference.
        
        Args:
            owner: Repository owner
            name: Repository name
            description: Repository description
            
        Returns:
            A GitHubRepository
        """
        return GitHubRepository(
            owner=owner,
            name=name,
            description=description
        )
    
    def add_labels_to_issue(
        self,
        issue: GitHubIssue,
        *labels: str
    ) -> None:
        """
        Add labels to an issue.
        
        Args:
            issue: The issue
            labels: Labels to add
        """
        for label in labels:
            issue.add_label(label)
