"""Tests for strategic plan skill."""

import pytest
from skills import StrategicPlanSkill
from domain import PlanPhase, StrategyPlanStatus


class TestStrategicPlanBasics:
    """Test basic strategic plan skill functionality."""
    
    def test_skill_can_be_created(self):
        """RED: Skill can be instantiated."""
        skill = StrategicPlanSkill()
        assert skill is not None
    
    def test_skill_has_name(self):
        """RED: Skill has a name."""
        skill = StrategicPlanSkill()
        assert skill.name == "plan"


class TestPlanCreation:
    """Test plan creation."""
    
    def test_create_plan(self):
        """RED: Can create a plan."""
        skill = StrategicPlanSkill()
        
        plan = skill.create_plan("Q3 Roadmap", "Build scalable auth system")
        
        assert plan.title == "Q3 Roadmap"
        assert plan.vision == "Build scalable auth system"
        assert plan.status == StrategyPlanStatus.DRAFT
    
    def test_plan_validation(self):
        """RED: Validates empty title."""
        skill = StrategicPlanSkill()
        
        with pytest.raises(ValueError):
            skill.create_plan("", "Vision")
    
    def test_plan_vision_validation(self):
        """RED: Validates empty vision."""
        skill = StrategicPlanSkill()
        
        with pytest.raises(ValueError):
            skill.create_plan("Title", "")


class TestGoalsAndObjectives:
    """Test goals and objectives."""
    
    def test_add_goal(self):
        """RED: Can add goals."""
        skill = StrategicPlanSkill()
        plan = skill.create_plan("Title", "Vision")
        
        skill.add_goal(plan, "Implement OAuth2")
        skill.add_goal(plan, "Support MFA")
        
        assert len(plan.goals) == 2
    
    def test_add_objective(self):
        """RED: Can add objectives."""
        skill = StrategicPlanSkill()
        plan = skill.create_plan("Title", "Vision")
        
        obj = skill.add_objective(
            plan,
            "Design auth flow",
            "Create OAuth2 flow diagram",
            phase=PlanPhase.DISCOVERY,
            estimated_hours=8.0
        )
        
        assert len(plan.objectives) == 1
        assert obj.phase == PlanPhase.DISCOVERY


class TestConstraintsAndAssumptions:
    """Test constraints and assumptions."""
    
    def test_add_constraint(self):
        """RED: Can add constraints."""
        skill = StrategicPlanSkill()
        plan = skill.create_plan("Title", "Vision")
        
        skill.add_constraint(plan, "Must use existing database")
        
        assert len(plan.constraints) == 1
    
    def test_add_assumption(self):
        """RED: Can add assumptions."""
        skill = StrategicPlanSkill()
        plan = skill.create_plan("Title", "Vision")
        
        skill.add_assumption(plan, "Team has OAuth2 experience")
        
        assert len(plan.assumptions) == 1


class TestPhaseObjectives:
    """Test getting objectives by phase."""
    
    def test_get_discovery_objectives(self):
        """RED: Can get discovery objectives."""
        skill = StrategicPlanSkill()
        plan = skill.create_plan("Title", "Vision")
        
        skill.add_objective(plan, "Obj1", "Desc1", PlanPhase.DISCOVERY)
        skill.add_objective(plan, "Obj2", "Desc2", PlanPhase.STRATEGY)
        
        discovery = skill.get_discovery_objectives(plan)
        assert len(discovery) == 1
        assert discovery[0].title == "Obj1"
    
    def test_get_execution_objectives(self):
        """RED: Can get execution objectives."""
        skill = StrategicPlanSkill()
        plan = skill.create_plan("Title", "Vision")
        
        skill.add_objective(plan, "Obj1", "Desc1", PlanPhase.EXECUTION)
        skill.add_objective(plan, "Obj2", "Desc2", PlanPhase.STRATEGY)
        
        execution = skill.get_execution_objectives(plan)
        assert len(execution) == 1


class TestEstimates:
    """Test estimation."""
    
    def test_total_estimated_hours(self):
        """RED: Can calculate total hours."""
        skill = StrategicPlanSkill()
        plan = skill.create_plan("Title", "Vision")
        
        skill.add_objective(plan, "O1", "D1", estimated_hours=8.0)
        skill.add_objective(plan, "O2", "D2", estimated_hours=16.0)
        
        total = plan.get_total_estimated_hours()
        assert total == 24.0


class TestApproval:
    """Test plan approval."""
    
    def test_approve_plan(self):
        """RED: Can approve plan."""
        skill = StrategicPlanSkill()
        plan = skill.create_plan("Title", "Vision")
        
        skill.approve_plan(plan, "Looks good")
        
        assert plan.status == StrategyPlanStatus.APPROVED
        assert plan.approval_notes == "Looks good"


class TestReporting:
    """Test reporting."""
    
    def test_generate_report(self):
        """RED: Can generate report."""
        skill = StrategicPlanSkill()
        plan = skill.create_plan("Q3 Plan", "Vision")
        
        skill.add_goal(plan, "Goal 1")
        skill.add_objective(plan, "Obj1", "Desc1", estimated_hours=8.0)
        
        report = skill.generate_report(plan)
        
        assert report.goal_count == 1
        assert report.objective_count == 1
        assert report.total_estimated_hours == 8.0
