"""Tests for diagnostic skill - TDD approach."""

import pytest
from datetime import datetime
from skills import DiagnosticSkill
from domain import (
    DiagnosticSession,
    ErrorEvidence,
    ErrorLocation,
    RootCauseHypothesis,
    DiagnosticReport,
    ErrorSeverity,
    DiagnosticStatus,
)


class TestDiagnosticSkillCreation:
    """Test creating the diagnostic skill."""
    
    def test_skill_can_be_created(self):
        """RED: DiagnosticSkill can be instantiated."""
        skill = DiagnosticSkill()
        assert skill is not None
    
    def test_skill_has_name(self):
        """RED: Skill has a name."""
        skill = DiagnosticSkill()
        assert skill.name == "diagnosing-bugs"


class TestDiagnosticSessionCreation:
    """Test creating diagnostic sessions."""
    
    def test_create_diagnostic_session(self):
        """RED: Can create a diagnostic session."""
        skill = DiagnosticSkill()
        
        session = skill.create_session(
            error_summary="Authentication fails intermittently",
            severity=ErrorSeverity.HIGH
        )
        
        assert session.error_summary == "Authentication fails intermittently"
        assert session.severity == ErrorSeverity.HIGH
        assert session.status == DiagnosticStatus.INITIAL
    
    def test_add_evidence_to_session(self):
        """RED: Can add error evidence."""
        skill = DiagnosticSkill()
        session = skill.create_session("Auth fails", ErrorSeverity.HIGH)
        
        location = ErrorLocation(
            file_path="src/auth.py",
            line_number=42,
            function_name="authenticate"
        )
        
        evidence = skill.add_evidence(
            session=session,
            error_message="TokenExpiredError: token has expired",
            error_type="TokenExpiredError",
            location=location
        )
        
        assert evidence in session.evidence
        assert session.status == DiagnosticStatus.INVESTIGATING


class TestHypothesesGeneration:
    """Test generating root cause hypotheses."""
    
    def test_add_hypothesis_to_session(self):
        """RED: Can add root cause hypothesis."""
        skill = DiagnosticSkill()
        session = skill.create_session("Auth fails", ErrorSeverity.HIGH)
        
        hypothesis = skill.add_hypothesis(
            session=session,
            description="Token refresh mechanism is broken",
            confidence=0.85
        )
        
        assert hypothesis in session.hypotheses
        assert hypothesis.confidence == 0.85
    
    def test_add_multiple_hypotheses(self):
        """RED: Can add and compare multiple hypotheses."""
        skill = DiagnosticSkill()
        session = skill.create_session("Auth fails", ErrorSeverity.HIGH)
        
        hyp1 = skill.add_hypothesis(session, "Token refresh broken", 0.85)
        hyp2 = skill.add_hypothesis(session, "Clock skew between services", 0.60)
        hyp3 = skill.add_hypothesis(session, "Database connection timeout", 0.40)
        
        assert len(session.hypotheses) == 3
        
        # Get most likely hypothesis
        most_likely = max(session.hypotheses, key=lambda h: h.confidence)
        assert most_likely == hyp1


class TestDiagnosticInvestigation:
    """Test conducting diagnostic investigation."""
    
    def test_select_most_likely_hypothesis(self):
        """RED: Can select the most likely hypothesis."""
        skill = DiagnosticSkill()
        session = skill.create_session("Auth fails", ErrorSeverity.HIGH)
        
        hyp1 = skill.add_hypothesis(session, "Token refresh broken", 0.85)
        skill.add_hypothesis(session, "Clock skew", 0.60)
        
        session.select_hypothesis(hyp1)
        
        assert session.selected_hypothesis == hyp1
        assert session.status == DiagnosticStatus.ROOT_CAUSE_FOUND
    
    def test_add_evidence_to_hypothesis(self):
        """RED: Can add supporting evidence to hypothesis."""
        skill = DiagnosticSkill()
        session = skill.create_session("Auth fails", ErrorSeverity.HIGH)
        
        hypothesis = skill.add_hypothesis(session, "Token refresh broken", 0.85)
        
        skill.add_supporting_evidence(
            hypothesis,
            "Token refresh endpoint returns 500 errors"
        )
        
        skill.add_supporting_evidence(
            hypothesis,
            "Redis cache timeout logs present"
        )
        
        assert len(hypothesis.supporting_evidence) == 2


class TestDiagnosticResolution:
    """Test generating resolution steps."""
    
    def test_generate_resolution_plan(self):
        """RED: Can generate resolution steps."""
        skill = DiagnosticSkill()
        session = skill.create_session("Auth fails", ErrorSeverity.HIGH)
        
        location = ErrorLocation(
            file_path="src/auth/token.py",
            line_number=125,
            function_name="refresh_token"
        )
        
        evidence = skill.add_evidence(
            session,
            "TokenExpiredError: token expired",
            "TokenExpiredError",
            location
        )
        
        hypothesis = skill.add_hypothesis(
            session,
            "Token refresh timeout too short",
            0.90
        )
        
        session.select_hypothesis(hypothesis)
        
        skill.add_resolution_step(session, "Increase token refresh timeout to 30s")
        skill.add_resolution_step(session, "Add retry logic with exponential backoff")
        skill.add_resolution_step(session, "Monitor token refresh metrics")
        
        assert len(session.resolution_steps) == 3
    
    def test_generate_diagnostic_report(self):
        """RED: Can generate comprehensive diagnostic report."""
        skill = DiagnosticSkill()
        session = skill.create_session("Auth fails", ErrorSeverity.HIGH)
        
        location = ErrorLocation(
            file_path="src/auth/token.py",
            line_number=125,
            function_name="refresh_token"
        )
        
        skill.add_evidence(
            session,
            "TokenExpiredError",
            "TokenExpiredError",
            location
        )
        
        hypothesis = skill.add_hypothesis(
            session,
            "Token refresh timeout too short",
            0.90
        )
        
        session.select_hypothesis(hypothesis)
        
        skill.add_resolution_step(session, "Increase timeout to 30s")
        skill.add_resolution_step(session, "Add retry logic")
        
        report = skill.generate_report(
            session=session,
            root_cause="Token refresh endpoint timeout was 5s, too short for slow networks",
            affected_components=["AuthService", "TokenManager"],
            permanent_fix="Increase timeout to 30s and add exponential backoff retry",
            prevention_measures=[
                "Set timeouts based on SLA requirements",
                "Monitor timeout-related errors in production",
                "Load test token refresh under network latency"
            ]
        )
        
        assert report.root_cause == "Token refresh endpoint timeout was 5s, too short for slow networks"
        assert len(report.affected_components) == 2
        assert len(report.prevention_measures) == 3


class TestDiagnosticValueObjects:
    """Test diagnostic value objects and constraints."""
    
    def test_error_location_validation(self):
        """RED: ErrorLocation validates input."""
        with pytest.raises(ValueError, match="File path cannot be empty"):
            ErrorLocation("", 10, "func")
        
        with pytest.raises(ValueError, match="Line number must be positive"):
            ErrorLocation("file.py", 0, "func")
    
    def test_hypothesis_confidence_validation(self):
        """RED: Hypothesis validates confidence range."""
        with pytest.raises(ValueError, match="Confidence must be between"):
            RootCauseHypothesis("desc", 1.5)
        
        with pytest.raises(ValueError, match="Confidence must be between"):
            RootCauseHypothesis("desc", -0.1)
    
    def test_valid_hypothesis_confidence(self):
        """RED: Valid confidence values accepted."""
        hyp_min = RootCauseHypothesis("desc", 0.0)
        hyp_mid = RootCauseHypothesis("desc", 0.5)
        hyp_max = RootCauseHypothesis("desc", 1.0)
        
        assert hyp_min.confidence == 0.0
        assert hyp_mid.confidence == 0.5
        assert hyp_max.confidence == 1.0
