"""Tests for GitHub integration skill."""

import pytest
from skills import GitHubIntegrationSkill
from domain import IssueType, IssuePriority


class TestGitHubIntegrationSkillBasics:
    """Test basic GitHub integration skill functionality."""
    
    def test_skill_can_be_created(self):
        """RED: Skill can be instantiated."""
        skill = GitHubIntegrationSkill()
        assert skill is not None
    
    def test_skill_has_name(self):
        """RED: Skill has a name."""
        skill = GitHubIntegrationSkill()
        assert skill.name == "github-integration"


class TestIssueCreation:
    """Test issue creation."""
    
    def test_create_basic_issue(self):
        """RED: Can create a basic issue."""
        skill = GitHubIntegrationSkill()
        issue = skill.create_issue(
            title="Add user authentication",
            description="Implement OAuth2 authentication"
        )
        assert issue.title == "Add user authentication"
        assert issue.description == "Implement OAuth2 authentication"
        assert issue.issue_type == IssueType.TASK
    
    def test_create_issue_with_priority(self):
        """RED: Can create issue with priority."""
        skill = GitHubIntegrationSkill()
        issue = skill.create_issue(
            title="Fix critical bug",
            description="Session timeout causes 500 error",
            issue_type=IssueType.BUG,
            priority=IssuePriority.CRITICAL
        )
        assert issue.priority == IssuePriority.CRITICAL
        assert issue.issue_type == IssueType.BUG
    
    def test_create_issue_with_labels(self):
        """RED: Can create issue with labels."""
        skill = GitHubIntegrationSkill()
        issue = skill.create_issue(
            title="Improve docs",
            description="Add API documentation",
            labels=["documentation", "help wanted"]
        )
        assert len(issue.labels) == 2
        assert "documentation" in issue.labels


class TestBugReporting:
    """Test bug report creation."""
    
    def test_create_bug_report(self):
        """RED: Can create a bug report."""
        skill = GitHubIntegrationSkill()
        issue = skill.create_bug_report(
            title="Login fails intermittently",
            description="Users cannot log in occasionally",
            root_cause="Race condition in session management"
        )
        assert issue.issue_type == IssueType.BUG
        assert "Race condition" in issue.description
        assert "from-diagnostic" in issue.labels
    
    def test_bug_report_with_steps(self):
        """RED: Bug report includes reproduction steps."""
        skill = GitHubIntegrationSkill()
        issue = skill.create_bug_report(
            title="Upload fails",
            description="File upload times out",
            root_cause="Network timeout handling issue",
            reproduction_steps=[
                "Click upload button",
                "Select large file",
                "Wait for timeout"
            ]
        )
        assert "1. Click upload button" in issue.description
        assert "2. Select large file" in issue.description
        assert "3. Wait for timeout" in issue.description


class TestFeatureRequests:
    """Test feature request creation."""
    
    def test_create_feature_request(self):
        """RED: Can create a feature request."""
        skill = GitHubIntegrationSkill()
        issue = skill.create_feature_request(
            title="Add dark mode",
            description="Implement dark theme for the UI"
        )
        assert issue.issue_type == IssueType.FEATURE
        assert "enhancement" in issue.labels
    
    def test_feature_request_with_criteria(self):
        """RED: Feature request includes acceptance criteria."""
        skill = GitHubIntegrationSkill()
        issue = skill.create_feature_request(
            title="User settings page",
            description="Create a user settings page",
            acceptance_criteria=[
                "Display user profile",
                "Allow password change",
                "Save preferences"
            ]
        )
        assert "[ ] Display user profile" in issue.description
        assert "[ ] Allow password change" in issue.description
        assert "[ ] Save preferences" in issue.description


class TestRepositoryManagement:
    """Test repository management."""
    
    def test_create_repository(self):
        """RED: Can create a repository reference."""
        skill = GitHubIntegrationSkill()
        repo = skill.create_repository(
            owner="myteam",
            name="my-project",
            description="A cool project"
        )
        assert repo.owner == "myteam"
        assert repo.name == "my-project"
        assert repo.full_name == "myteam/my-project"
    
    def test_repository_full_name(self):
        """RED: Repository full_name is correct."""
        skill = GitHubIntegrationSkill()
        repo = skill.create_repository("octocat", "Hello-World")
        assert repo.full_name == "octocat/Hello-World"


class TestLabelManagement:
    """Test label management."""
    
    def test_add_labels_to_issue(self):
        """RED: Can add labels to an issue."""
        skill = GitHubIntegrationSkill()
        issue = skill.create_issue(
            title="New feature",
            description="Some feature"
        )
        skill.add_labels_to_issue(issue, "urgent", "backend")
        assert "urgent" in issue.labels
        assert "backend" in issue.labels
    
    def test_duplicate_labels_not_added(self):
        """RED: Duplicate labels are not added."""
        skill = GitHubIntegrationSkill()
        issue = skill.create_issue(
            title="Bug",
            description="Some bug",
            labels=["bug"]
        )
        skill.add_labels_to_issue(issue, "bug")
        assert issue.labels.count("bug") == 1


class TestIssueValidation:
    """Test issue validation."""
    
    def test_empty_title_raises_error(self):
        """RED: Empty title raises ValueError."""
        skill = GitHubIntegrationSkill()
        with pytest.raises(ValueError, match="Title cannot be empty"):
            skill.create_issue(
                title="",
                description="Some description"
            )
    
    def test_empty_description_raises_error(self):
        """RED: Empty description raises ValueError."""
        skill = GitHubIntegrationSkill()
        with pytest.raises(ValueError, match="Description cannot be empty"):
            skill.create_issue(
                title="Some title",
                description=""
            )


class TestRepositoryValidation:
    """Test repository validation."""
    
    def test_empty_owner_raises_error(self):
        """RED: Empty owner raises ValueError."""
        skill = GitHubIntegrationSkill()
        with pytest.raises(ValueError, match="Owner cannot be empty"):
            skill.create_repository(
                owner="",
                name="project"
            )
    
    def test_empty_name_raises_error(self):
        """RED: Empty name raises ValueError."""
        skill = GitHubIntegrationSkill()
        with pytest.raises(ValueError, match="Name cannot be empty"):
            skill.create_repository(
                owner="user",
                name=""
            )
