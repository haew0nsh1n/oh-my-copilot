"""Tests for ralplan skill."""

import pytest
from skills import RalPlanSkill
from domain import PlanStatus, ReviewRole


class TestRalPlanBasics:
    """Test basic ralplan skill functionality."""
    
    def test_skill_can_be_created(self):
        """RED: Skill can be instantiated."""
        skill = RalPlanSkill()
        assert skill is not None
    
    def test_skill_has_name(self):
        """RED: Skill has a name."""
        skill = RalPlanSkill()
        assert skill.name == "ralplan"


class TestPlanCreation:
    """Test plan creation."""
    
    def test_create_plan(self):
        """RED: Can create a plan."""
        skill = RalPlanSkill()
        
        plan = skill.create_plan(
            "Auth System",
            "Redesign authentication system",
            requirements=["OAuth2", "JWT support", "MFA"]
        )
        
        assert plan.title == "Auth System"
        assert len(plan.requirements) == 3
    
    def test_add_design_decision(self):
        """RED: Can add design decisions."""
        skill = RalPlanSkill()
        plan = skill.create_plan("Plan", "Description")
        
        skill.add_design_decision(plan, "Use OAuth2 for external auth")
        
        assert len(plan.design_decisions) == 1


class TestArchitectReview:
    """Test architect review."""
    
    def test_architect_approval(self):
        """RED: Can submit architect approval."""
        skill = RalPlanSkill()
        plan = skill.create_plan("Plan", "Description")
        
        evidence = skill.submit_architect_review(
            plan,
            "Approved",
            "Good architecture choice",
            "Alice"
        )
        
        assert evidence.role == ReviewRole.ARCHITECT
        assert plan.is_architect_approved()
        assert plan.status == PlanStatus.CRITIC_REVIEW
    
    def test_architect_rejection(self):
        """RED: Can reject plan at architect stage."""
        skill = RalPlanSkill()
        plan = skill.create_plan("Plan", "Description")
        
        skill.submit_architect_review(
            plan,
            "Rejected",
            "Design has issues",
            "Alice"
        )
        
        assert not plan.is_architect_approved()
        assert plan.status == PlanStatus.REJECTED


class TestCriticReview:
    """Test critic review."""
    
    def test_critic_approval_after_architect(self):
        """RED: Can get critic approval after architect."""
        skill = RalPlanSkill()
        plan = skill.create_plan("Plan", "Description")
        
        skill.submit_architect_review(plan, "Approved", "Good", "Alice")
        skill.submit_critic_review(plan, "Approved", "Well reasoned", "Bob")
        
        assert plan.is_critic_approved()
        assert plan.status == PlanStatus.APPROVED
    
    def test_critic_rejection_blocks_approval(self):
        """RED: Critic rejection blocks full approval."""
        skill = RalPlanSkill()
        plan = skill.create_plan("Plan", "Description")
        
        skill.submit_architect_review(plan, "Approved", "Good", "Alice")
        skill.submit_critic_review(plan, "Rejected", "Not safe", "Bob")
        
        assert not plan.is_critic_approved()
        assert plan.status == PlanStatus.REJECTED


class TestImplementationSteps:
    """Test adding implementation steps."""
    
    def test_add_implementation_steps(self):
        """RED: Can add implementation steps."""
        skill = RalPlanSkill()
        plan = skill.create_plan("Plan", "Description")
        
        skill.add_implementation_step(plan, "Set up OAuth2 provider")
        skill.add_implementation_step(plan, "Implement JWT validation")
        
        assert len(plan.implementation_steps) == 2


class TestRisksAndTradeoffs:
    """Test risks and tradeoffs."""
    
    def test_add_risks(self):
        """RED: Can add risks."""
        skill = RalPlanSkill()
        plan = skill.create_plan("Plan", "Description")
        
        skill.add_risk(plan, "OAuth2 provider downtime")
        
        assert len(plan.risks) == 1
    
    def test_add_tradeoffs(self):
        """RED: Can add tradeoffs."""
        skill = RalPlanSkill()
        plan = skill.create_plan("Plan", "Description")
        
        skill.add_tradeoff(plan, "More secure but slower auth flow")
        
        assert len(plan.tradeoffs) == 1


class TestReporting:
    """Test plan reporting."""
    
    def test_generate_report(self):
        """RED: Can generate plan report."""
        skill = RalPlanSkill()
        plan = skill.create_plan("Plan", "Description")
        
        skill.submit_architect_review(plan, "Approved", "Good", "Alice")
        skill.submit_critic_review(plan, "Approved", "Good", "Bob")
        
        report = skill.generate_report(plan)
        
        assert report.ready_for_execution
        assert report.status == PlanStatus.APPROVED
