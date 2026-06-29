"""Tests for code review skill - TDD approach."""

import pytest
from skills import CodeReviewSkill
from domain import (
    CodeReview,
    ReviewFinding,
    ReviewSection,
    ReviewAspect,
    ReviewStatus,
    FindingSeverity,
)


class TestCodeReviewSkillCreation:
    """Test creating the code review skill."""
    
    def test_skill_can_be_created(self):
        """RED: CodeReviewSkill can be instantiated."""
        skill = CodeReviewSkill()
        assert skill is not None
    
    def test_skill_has_name(self):
        """RED: Skill has a name."""
        skill = CodeReviewSkill()
        assert skill.name == "review"


class TestCodeReviewCreation:
    """Test creating code reviews."""
    
    def test_create_code_review(self):
        """RED: Can create a code review."""
        skill = CodeReviewSkill()
        
        review = skill.create_review(
            title="Feature: User Authentication",
            context={"pr_number": 123, "branch": "feat/auth"}
        )
        
        assert review.title == "Feature: User Authentication"
        assert review.status == ReviewStatus.PENDING
    
    def test_add_section_to_review(self):
        """RED: Can add sections to review."""
        skill = CodeReviewSkill()
        review = skill.create_review("Auth Feature")
        
        section = skill.add_section(
            review,
            name="Authentication Service",
            files=["src/auth/service.py", "src/auth/token.py"],
            lines_changed=234
        )
        
        assert section in review.sections
        assert section.name == "Authentication Service"


class TestFindingsAndApproval:
    """Test adding findings and approval logic."""
    
    def test_add_findings_to_review(self):
        """RED: Can add findings to review."""
        skill = CodeReviewSkill()
        review = skill.create_review("Auth Feature")
        
        finding1 = skill.add_finding(
            review,
            location="src/auth/token.py:42",
            description="Missing null check for token",
            severity=FindingSeverity.MAJOR,
            aspect=ReviewAspect.SECURITY,
            suggestion="Add guard: if not token: raise ValueError()"
        )
        
        finding2 = skill.add_finding(
            review,
            location="src/auth/service.py:15",
            description="Type hints missing",
            severity=FindingSeverity.MINOR,
            aspect=ReviewAspect.STANDARDS
        )
        
        assert len(review.findings) == 2
        assert review.status == ReviewStatus.IN_PROGRESS
    
    def test_approve_review_with_no_critical_findings(self):
        """RED: Review approved if only minor findings."""
        skill = CodeReviewSkill()
        review = skill.create_review("Auth Feature")
        
        skill.add_finding(
            review,
            location="file.py:10",
            description="Minor issue",
            severity=FindingSeverity.MINOR,
            aspect=ReviewAspect.STANDARDS
        )
        
        skill.approve_review(review)
        
        assert review.status == ReviewStatus.APPROVED
    
    def test_reject_review_with_critical_findings(self):
        """RED: Review rejected if critical findings."""
        skill = CodeReviewSkill()
        review = skill.create_review("Auth Feature")
        
        skill.add_finding(
            review,
            location="file.py:10",
            description="Security vulnerability",
            severity=FindingSeverity.CRITICAL,
            aspect=ReviewAspect.SECURITY
        )
        
        skill.approve_review(review)
        
        assert review.status == ReviewStatus.CHANGES_REQUESTED
    
    def test_get_findings_by_severity(self):
        """RED: Can retrieve findings by severity."""
        skill = CodeReviewSkill()
        review = skill.create_review("Feature")
        
        skill.add_finding(review, "a.py:1", "Critical", FindingSeverity.CRITICAL, ReviewAspect.SECURITY)
        skill.add_finding(review, "b.py:2", "Major", FindingSeverity.MAJOR, ReviewAspect.STANDARDS)
        skill.add_finding(review, "c.py:3", "Minor", FindingSeverity.MINOR, ReviewAspect.STANDARDS)
        
        critical_findings = skill.get_findings_by_severity(review, FindingSeverity.CRITICAL)
        
        assert len(critical_findings) == 1
        assert critical_findings[0].severity == FindingSeverity.CRITICAL


class TestReviewAspects:
    """Test reviewing different aspects."""
    
    def test_standards_review(self):
        """RED: Can review code standards."""
        skill = CodeReviewSkill()
        review = skill.create_review("Code Quality")
        
        findings = skill.review_standards(review)
        
        assert isinstance(findings, list)
    
    def test_spec_compliance_review(self):
        """RED: Can review spec compliance."""
        skill = CodeReviewSkill()
        review = skill.create_review("Feature Implementation")
        
        findings = skill.review_spec(review)
        
        assert isinstance(findings, list)
    
    def test_review_multiple_aspects(self):
        """RED: Can review multiple aspects in sequence."""
        skill = CodeReviewSkill()
        review = skill.create_review("Complete Review")
        
        skill.add_section(review, "Logic", ["main.py"], 50)
        skill.add_section(review, "Tests", ["test_main.py"], 80)
        
        standards = skill.review_standards(review)
        spec = skill.review_spec(review)
        
        assert isinstance(standards, list)
        assert isinstance(spec, list)


class TestGenerateReviewReport:
    """Test generating review reports."""
    
    def test_generate_minimal_report(self):
        """RED: Can generate report with no findings."""
        skill = CodeReviewSkill()
        review = skill.create_review("Simple Feature")
        skill.add_section(review, "Core", ["main.py"], 20)
        
        report = skill.generate_report(review)
        
        assert report.total_findings == 0
        assert report.critical_findings == 0
        assert report.recommendation in ("APPROVE", "REQUEST_CHANGES", "BLOCK")
    
    def test_generate_detailed_report(self):
        """RED: Can generate report with findings."""
        skill = CodeReviewSkill()
        review = skill.create_review("Feature")
        
        skill.add_section(review, "Auth", ["auth.py"], 100)
        skill.add_finding(review, "auth.py:42", "Missing validation", FindingSeverity.MAJOR, ReviewAspect.SECURITY)
        skill.add_finding(review, "auth.py:15", "Inefficient query", FindingSeverity.MINOR, ReviewAspect.PERFORMANCE)
        skill.add_finding(review, "auth.py:8", "Format issue", FindingSeverity.SUGGESTION, ReviewAspect.STANDARDS)
        
        report = skill.generate_report(review)
        
        assert report.total_findings == 3
        assert report.major_findings == 1
        assert report.minor_findings == 1
        assert report.suggestions == 1
        assert report.recommendation == "REQUEST_CHANGES"
    
    def test_report_with_critical_findings(self):
        """RED: Critical findings result in BLOCK recommendation."""
        skill = CodeReviewSkill()
        review = skill.create_review("Risky Feature")
        
        skill.add_finding(review, "file.py:1", "Security hole", FindingSeverity.CRITICAL, ReviewAspect.SECURITY)
        
        report = skill.generate_report(review)
        
        assert report.critical_findings == 1
        assert report.recommendation == "BLOCK"
