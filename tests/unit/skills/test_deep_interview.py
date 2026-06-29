"""Tests for deep interview skill."""

import pytest
from skills import DeepInterviewSkill
from domain import QuestionType, InterviewPhase


class TestDeepInterviewSkillBasics:
    """Test basic deep interview skill functionality."""
    
    def test_skill_can_be_created(self):
        """RED: Skill can be instantiated."""
        skill = DeepInterviewSkill()
        assert skill is not None
    
    def test_skill_has_name(self):
        """RED: Skill has a name."""
        skill = DeepInterviewSkill()
        assert skill.name == "deep-interview"


class TestSessionCreation:
    """Test session creation."""
    
    def test_create_session(self):
        """RED: Can create a session."""
        skill = DeepInterviewSkill()
        session = skill.create_session("Implement user authentication")
        assert session.prompt == "Implement user authentication"
        assert session.phase == InterviewPhase.EXPLORING
        assert len(session.questions) > 0


class TestQuestionManagement:
    """Test question management."""
    
    def test_ask_question(self):
        """RED: Can ask questions."""
        skill = DeepInterviewSkill()
        session = skill.create_session("Build a payment system")
        question = skill.ask_question(
            session,
            "What payment methods should we support?",
            QuestionType.SCOPE
        )
        assert question.question_type == QuestionType.SCOPE
        assert len(session.questions) > 1
    
    def test_answer_question(self):
        """RED: Can answer questions."""
        skill = DeepInterviewSkill()
        session = skill.create_session("Build a payment system")
        questions = session.questions
        answer = skill.answer_question(
            session,
            questions[0],
            "The goal is secure payment processing"
        )
        assert answer.answer == "The goal is secure payment processing"
        assert len(session.answers) == 1


class TestClarification:
    """Test clarification methods."""
    
    def test_clarify_goals(self):
        """RED: Can clarify goals."""
        skill = DeepInterviewSkill()
        session = skill.create_session("Build an API")
        skill.clarify_goals(
            session,
            "Support REST endpoints",
            "Scale to 1M requests/day"
        )
        assert len(session.goals) == 2
    
    def test_clarify_non_goals(self):
        """RED: Can clarify non-goals."""
        skill = DeepInterviewSkill()
        session = skill.create_session("Build an API")
        skill.clarify_non_goals(session, "GraphQL support", "Mobile apps")
        assert len(session.non_goals) == 2
    
    def test_identify_assumptions(self):
        """RED: Can identify assumptions."""
        skill = DeepInterviewSkill()
        session = skill.create_session("Build an API")
        skill.identify_assumptions(
            session,
            "Users have stable internet",
            "Database is always available"
        )
        assert len(session.assumptions) == 2
    
    def test_identify_risks(self):
        """RED: Can identify risks."""
        skill = DeepInterviewSkill()
        session = skill.create_session("Build an API")
        skill.identify_risks(
            session,
            "Performance degradation under load",
            "Security vulnerabilities"
        )
        assert len(session.risks) == 2
    
    def test_identify_constraints(self):
        """RED: Can identify constraints."""
        skill = DeepInterviewSkill()
        session = skill.create_session("Build an API")
        skill.identify_constraints(
            session,
            "Must use Python 3.10+",
            "PostgreSQL required"
        )
        assert len(session.constraints) == 2


class TestReporting:
    """Test report generation."""
    
    def test_generate_report(self):
        """RED: Can generate report."""
        skill = DeepInterviewSkill()
        session = skill.create_session("Build authentication")
        skill.clarify_goals(session, "Secure login", "OAuth2 support")
        skill.identify_risks(session, "Brute force attacks")
        report = skill.generate_report(session)
        assert report.clarified_prompt == session.prompt
        assert len(report.goals) == 2
        assert len(report.risks) == 1
        assert session.phase == InterviewPhase.COMPLETED
