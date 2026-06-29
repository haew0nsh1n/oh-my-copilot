"""Code review skill for systematic code quality assessment."""

from typing import List
from domain import (
    CodeReview,
    ReviewFinding,
    ReviewSection,
    ReviewReport,
    ReviewAspect,
    FindingSeverity,
)


class CodeReviewSkill:
    """
    A skill for systematic code reviews.
    
    Reviews code across two dimensions:
    - Standards: Does it follow repo conventions?
    - Spec: Does it match the requirements?
    """
    
    def __init__(self):
        """Initialize the code review skill."""
        self.name = "review"
        self.description = "Systematic code review (standards + spec)"
    
    def create_review(
        self,
        title: str,
        context: dict | None = None,
    ) -> CodeReview:
        """
        Create a new code review.
        
        Args:
            title: Title of the review
            context: Optional context (PR number, branch, etc.)
            
        Returns:
            A new CodeReview
        """
        return CodeReview(
            title=title,
            context=context or {}
        )
    
    def add_section(
        self,
        review: CodeReview,
        name: str,
        files: List[str] | None = None,
        lines_changed: int = 0,
        description: str = "",
    ) -> ReviewSection:
        """
        Add a section to the review.
        
        Args:
            review: The code review
            name: Section name
            files: Files in this section
            lines_changed: Number of lines changed
            description: Section description
            
        Returns:
            The created ReviewSection
        """
        section = ReviewSection(
            name=name,
            files=files or [],
            lines_changed=lines_changed,
            description=description
        )
        review.add_section(section)
        return section
    
    def add_finding(
        self,
        review: CodeReview,
        location: str,
        description: str,
        severity: FindingSeverity,
        aspect: ReviewAspect,
        suggestion: str = "",
    ) -> ReviewFinding:
        """
        Add a finding to the review.
        
        Args:
            review: The code review
            location: File location (file.py:line or file.py:function)
            description: Description of the finding
            severity: Severity level
            aspect: Which aspect (standards, spec, etc.)
            suggestion: Optional suggestion to fix
            
        Returns:
            The created ReviewFinding
        """
        finding = ReviewFinding(
            location=location,
            description=description,
            severity=severity,
            aspect=aspect,
            suggestion=suggestion
        )
        review.add_finding(finding)
        return finding
    
    def review_standards(self, review: CodeReview) -> List[ReviewFinding]:
        """
        Review code standards compliance.
        
        Args:
            review: The code review
            
        Returns:
            List of findings related to standards
        """
        return [
            f for f in review.findings
            if f.aspect == ReviewAspect.STANDARDS
        ]
    
    def review_spec(self, review: CodeReview) -> List[ReviewFinding]:
        """
        Review spec compliance.
        
        Args:
            review: The code review
            
        Returns:
            List of findings related to spec
        """
        return [
            f for f in review.findings
            if f.aspect == ReviewAspect.SPEC
        ]
    
    def get_findings_by_severity(
        self,
        review: CodeReview,
        severity: FindingSeverity
    ) -> List[ReviewFinding]:
        """
        Get all findings of a specific severity.
        
        Args:
            review: The code review
            severity: The severity level
            
        Returns:
            List of findings with that severity
        """
        return review.get_findings_by_severity(severity)
    
    def approve_review(self, review: CodeReview) -> None:
        """
        Approve or request changes on the review.
        
        Args:
            review: The code review
        """
        review.approve()
    
    def generate_report(self, review: CodeReview) -> ReviewReport:
        """
        Generate a comprehensive review report.
        
        Args:
            review: The code review
            
        Returns:
            A ReviewReport with summary and recommendation
        """
        critical = len(review.get_findings_by_severity(FindingSeverity.CRITICAL))
        major = len(review.get_findings_by_severity(FindingSeverity.MAJOR))
        minor = len(review.get_findings_by_severity(FindingSeverity.MINOR))
        suggestions = len(review.get_findings_by_severity(FindingSeverity.SUGGESTION))
        
        total = critical + major + minor + suggestions
        
        # Determine recommendation
        if critical > 0:
            recommendation = "BLOCK"
            summary = f"Critical security/functionality issues found ({critical})"
        elif major > 0:
            recommendation = "REQUEST_CHANGES"
            summary = f"Major issues must be addressed ({major})"
        elif minor > 0:
            recommendation = "APPROVE"
            summary = f"Minor improvements suggested ({minor})"
        else:
            recommendation = "APPROVE"
            summary = "All checks passed"
        
        return ReviewReport(
            review=review,
            total_findings=total,
            critical_findings=critical,
            major_findings=major,
            minor_findings=minor,
            suggestions=suggestions,
            recommendation=recommendation,
            summary=summary
        )
