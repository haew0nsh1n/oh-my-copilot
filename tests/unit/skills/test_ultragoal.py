"""Tests for ultragoal skill."""

import pytest
from skills import UltragoalSkill
from domain import GoalPriority, GoalStatus


class TestUltragoalSkillBasics:
    """Test basic ultragoal skill functionality."""
    
    def test_skill_can_be_created(self):
        """RED: Skill can be instantiated."""
        skill = UltragoalSkill()
        assert skill is not None
    
    def test_skill_has_name(self):
        """RED: Skill has a name."""
        skill = UltragoalSkill()
        assert skill.name == "ultragoal"


class TestUltragoalCreation:
    """Test ultragoal creation."""
    
    def test_create_ultragoal(self):
        """RED: Can create an ultragoal."""
        skill = UltragoalSkill()
        ultragoal = skill.create_ultragoal(
            "Authentication Feature",
            "Implement secure user authentication"
        )
        assert ultragoal.name == "Authentication Feature"
        assert len(ultragoal.goals) == 0


class TestGoalManagement:
    """Test goal management."""
    
    def test_create_and_add_goal(self):
        """RED: Can create and add goals."""
        skill = UltragoalSkill()
        ultragoal = skill.create_ultragoal("Project", "Build something")
        goal = skill.create_goal(
            "Setup database",
            "Configure PostgreSQL",
            priority=GoalPriority.HIGH,
            criteria=["Schema created", "Migrations applied"]
        )
        skill.add_goal(ultragoal, goal)
        assert len(ultragoal.goals) == 1
        assert len(goal.acceptance_criteria) == 2
    
    def test_goal_lifecycle(self):
        """RED: Can track goal lifecycle."""
        skill = UltragoalSkill()
        ultragoal = skill.create_ultragoal("Project", "Build something")
        goal = skill.create_goal("Task 1", "Do something")
        skill.add_goal(ultragoal, goal)
        
        skill.start_goal(goal)
        assert goal.status == GoalStatus.IN_PROGRESS
        
        skill.complete_goal(goal)
        assert goal.status == GoalStatus.COMPLETED


class TestCheckpoints:
    """Test checkpoint management."""
    
    def test_add_checkpoint(self):
        """RED: Can add checkpoints to goals."""
        skill = UltragoalSkill()
        goal = skill.create_goal("Task", "Description")
        checkpoint = skill.create_checkpoint(
            "Code Review",
            "Code must be reviewed"
        )
        skill.add_checkpoint(goal, checkpoint)
        assert len(goal.checkpoints) == 1
    
    def test_complete_checkpoint(self):
        """RED: Can complete checkpoints."""
        skill = UltragoalSkill()
        checkpoint = skill.create_checkpoint("Review", "Code review")
        skill.complete_checkpoint(checkpoint, "Approved by lead")
        assert checkpoint.completed is True
        assert checkpoint.verification_notes == "Approved by lead"


class TestReporting:
    """Test report generation."""
    
    def test_generate_report(self):
        """RED: Can generate ultragoal report."""
        skill = UltragoalSkill()
        ultragoal = skill.create_ultragoal("Project", "Build something")
        
        goal1 = skill.create_goal("Task 1", "Do step 1")
        goal2 = skill.create_goal("Task 2", "Do step 2")
        skill.add_goal(ultragoal, goal1)
        skill.add_goal(ultragoal, goal2)
        
        skill.complete_goal(goal1)
        
        report = skill.generate_report(ultragoal)
        assert report.total_goals == 2
        assert report.completed_goals == 1
        assert report.completion_percentage == 50.0
