"""Diagnostic skill for bug investigation and root cause analysis."""

from typing import List
from domain import (
    DiagnosticSession,
    ErrorEvidence,
    ErrorLocation,
    RootCauseHypothesis,
    DiagnosticReport,
    ErrorSeverity,
)


class DiagnosticSkill:
    """
    A skill for systematically diagnosing bugs and errors.
    
    This skill helps:
    - Collect error evidence
    - Generate root cause hypotheses
    - Conduct systematic investigation
    - Generate diagnostic reports
    """
    
    def __init__(self):
        """Initialize the diagnostic skill."""
        self.name = "diagnosing-bugs"
        self.description = "Systematically diagnose bugs and find root causes"
    
    def create_session(
        self,
        error_summary: str,
        severity: ErrorSeverity
    ) -> DiagnosticSession:
        """
        Create a new diagnostic session.
        
        Args:
            error_summary: Summary of the error or problem
            severity: Severity level of the error
            
        Returns:
            A new DiagnosticSession
        """
        return DiagnosticSession(
            error_summary=error_summary,
            severity=severity
        )
    
    def add_evidence(
        self,
        session: DiagnosticSession,
        error_message: str,
        error_type: str,
        location: ErrorLocation,
        context: dict | None = None,
    ) -> ErrorEvidence:
        """
        Add error evidence to the diagnostic session.
        
        Args:
            session: The diagnostic session
            error_message: The error message
            error_type: Type of error (e.g., TypeError, TimeoutError)
            location: Where the error occurred
            context: Optional context about the error
            
        Returns:
            The created ErrorEvidence
        """
        evidence = ErrorEvidence(
            error_message=error_message,
            error_type=error_type,
            location=location,
            context=context or {}
        )
        session.add_evidence(evidence)
        return evidence
    
    def add_hypothesis(
        self,
        session: DiagnosticSession,
        description: str,
        confidence: float,
        supporting_evidence: List[str] | None = None,
    ) -> RootCauseHypothesis:
        """
        Add a root cause hypothesis.
        
        Args:
            session: The diagnostic session
            description: Description of the hypothesized root cause
            confidence: Confidence level (0.0 to 1.0)
            supporting_evidence: Optional initial supporting evidence
            
        Returns:
            The created RootCauseHypothesis
        """
        hypothesis = RootCauseHypothesis(
            description=description,
            confidence=confidence,
            supporting_evidence=supporting_evidence or []
        )
        session.add_hypothesis(hypothesis)
        return hypothesis
    
    def add_supporting_evidence(
        self,
        hypothesis: RootCauseHypothesis,
        evidence: str
    ) -> None:
        """
        Add supporting evidence to a hypothesis.
        
        Args:
            hypothesis: The hypothesis
            evidence: Evidence supporting this hypothesis
        """
        if not evidence or not evidence.strip():
            raise ValueError("Evidence cannot be empty")
        hypothesis.supporting_evidence.append(evidence)
    
    def add_contradicting_evidence(
        self,
        hypothesis: RootCauseHypothesis,
        evidence: str
    ) -> None:
        """
        Add contradicting evidence to a hypothesis.
        
        Args:
            hypothesis: The hypothesis
            evidence: Evidence contradicting this hypothesis
        """
        if not evidence or not evidence.strip():
            raise ValueError("Evidence cannot be empty")
        hypothesis.contradicting_evidence.append(evidence)
    
    def add_resolution_step(
        self,
        session: DiagnosticSession,
        step: str
    ) -> None:
        """
        Add a resolution step to fix the issue.
        
        Args:
            session: The diagnostic session
            step: A step to resolve the issue
        """
        session.add_resolution_step(step)
    
    def generate_report(
        self,
        session: DiagnosticSession,
        root_cause: str,
        affected_components: List[str] | None = None,
        workaround: str = "",
        permanent_fix: str = "",
        prevention_measures: List[str] | None = None,
    ) -> DiagnosticReport:
        """
        Generate a diagnostic report.
        
        Args:
            session: The diagnostic session
            root_cause: The identified root cause
            affected_components: Components affected by the bug
            workaround: Temporary workaround if available
            permanent_fix: Permanent fix description
            prevention_measures: Measures to prevent this bug in the future
            
        Returns:
            A DiagnosticReport
        """
        return DiagnosticReport(
            session=session,
            root_cause=root_cause,
            affected_components=affected_components or [],
            workaround=workaround,
            permanent_fix=permanent_fix,
            prevention_measures=prevention_measures or []
        )
