"""Tests for ralph skill."""

import pytest
from skills import RalphSkill
from domain import RalphLoopStatus


class TestRalphBasics:
    """Test basic ralph skill functionality."""
    
    def test_skill_can_be_created(self):
        """RED: Skill can be instantiated."""
        skill = RalphSkill()
        assert skill is not None
    
    def test_skill_has_name(self):
        """RED: Skill has a name."""
        skill = RalphSkill()
        assert skill.name == "ralph"


class TestCompletionCreation:
    """Test completion loop creation."""
    
    def test_create_completion(self):
        """RED: Can create a completion loop."""
        skill = RalphSkill()
        
        completion = skill.create_completion(
            "Complete auth implementation",
            "Alice",
            "Finish OAuth2 implementation"
        )
        
        assert completion.task_title == "Complete auth implementation"
        assert completion.owner == "Alice"
        assert completion.status == RalphLoopStatus.STARTING


class TestIterations:
    """Test iterations in completion loop."""
    
    def test_start_iteration(self):
        """RED: Can start an iteration."""
        skill = RalphSkill()
        completion = skill.create_completion("Task", "Alice")
        
        iteration = skill.start_iteration(completion, "Implement OAuth2 flow")
        
        assert iteration.iteration_number == 1
        assert completion.status == RalphLoopStatus.IN_PROGRESS
    
    def test_complete_successful_iteration(self):
        """RED: Can complete successful iteration."""
        skill = RalphSkill()
        completion = skill.create_completion("Task", "Alice")
        iteration = skill.start_iteration(completion, "Step 1")
        
        skill.complete_iteration(iteration, success=True, output="Done")
        
        assert iteration.success
        assert iteration.output == "Done"
    
    def test_complete_failed_iteration(self):
        """RED: Can fail an iteration."""
        skill = RalphSkill()
        completion = skill.create_completion("Task", "Alice")
        iteration = skill.start_iteration(completion, "Step 1")
        
        skill.fail_iteration(iteration, "Test failed")
        
        assert not iteration.success
        assert "Test failed" in iteration.error


class TestMultipleIterations:
    """Test multiple iterations."""
    
    def test_multiple_iterations(self):
        """RED: Can run multiple iterations."""
        skill = RalphSkill()
        completion = skill.create_completion("Task", "Alice")
        
        iter1 = skill.start_iteration(completion, "Step 1")
        skill.complete_iteration(iter1, success=True)
        
        iter2 = skill.start_iteration(completion, "Step 2")
        skill.complete_iteration(iter2, success=True)
        
        assert len(completion.iterations) == 2
        assert len(completion.get_successful_iterations()) == 2
    
    def test_iteration_limit(self):
        """RED: Respects iteration limit."""
        skill = RalphSkill()
        completion = skill.create_completion("Task", "Alice")
        completion.max_iterations = 2
        
        iter1 = skill.start_iteration(completion, "Step 1")
        skill.complete_iteration(iter1, success=True)
        
        iter2 = skill.start_iteration(completion, "Step 2")
        skill.complete_iteration(iter2, success=True)
        
        with pytest.raises(RuntimeError):
            skill.start_iteration(completion, "Step 3")


class TestCompletion:
    """Test completion."""
    
    def test_mark_loop_complete(self):
        """RED: Can mark loop as complete."""
        skill = RalphSkill()
        completion = skill.create_completion("Task", "Alice")
        
        iter1 = skill.start_iteration(completion, "Step 1")
        skill.complete_iteration(iter1, success=True)
        
        skill.mark_complete(completion)
        
        assert completion.status == RalphLoopStatus.COMPLETED
    
    def test_mark_loop_failed(self):
        """RED: Can mark loop as failed."""
        skill = RalphSkill()
        completion = skill.create_completion("Task", "Alice")
        
        skill.mark_failed(completion)
        
        assert completion.status == RalphLoopStatus.FAILED


class TestReporting:
    """Test reporting."""
    
    def test_generate_report(self):
        """RED: Can generate report."""
        skill = RalphSkill()
        completion = skill.create_completion("Task", "Alice")
        
        iter1 = skill.start_iteration(completion, "Step 1")
        skill.complete_iteration(iter1, success=True)
        
        skill.mark_complete(completion)
        
        report = skill.generate_report(completion)
        
        assert report.task_title == "Task"
        assert report.total_iterations == 1
        assert report.successful_iterations == 1
