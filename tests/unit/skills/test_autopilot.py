"""Tests for autopilot skill."""

import pytest
from skills import AutopilotSkill
from domain import AutopilotPhase, AutopilotStatus


class TestAutopilotBasics:
    """Test basic autopilot skill functionality."""
    
    def test_skill_can_be_created(self):
        """RED: Skill can be instantiated."""
        skill = AutopilotSkill()
        assert skill is not None
    
    def test_skill_has_name(self):
        """RED: Skill has a name."""
        skill = AutopilotSkill()
        assert skill.name == "autopilot"


class TestWorkflowCreation:
    """Test workflow creation."""
    
    def test_create_workflow(self):
        """RED: Can create a workflow."""
        skill = AutopilotSkill()
        
        workflow = skill.create_workflow("Implement auth feature")
        
        assert workflow.task_description == "Implement auth feature"
        assert workflow.status == AutopilotStatus.IN_PROGRESS
        assert workflow.current_phase == AutopilotPhase.INTERVIEW
    
    def test_workflow_validation(self):
        """RED: Validates empty task."""
        skill = AutopilotSkill()
        
        with pytest.raises(ValueError):
            skill.create_workflow("")


class TestPhaseExecution:
    """Test phase execution."""
    
    def test_start_phase(self):
        """RED: Can start a phase."""
        skill = AutopilotSkill()
        workflow = skill.create_workflow("Task")
        
        skill.start_phase(workflow, AutopilotPhase.PLANNING)
        
        assert workflow.current_phase == AutopilotPhase.PLANNING
    
    def test_complete_phase_success(self):
        """RED: Can complete phase successfully."""
        skill = AutopilotSkill()
        workflow = skill.create_workflow("Task")
        
        result = skill.complete_phase(
            workflow,
            AutopilotPhase.INTERVIEW,
            success=True,
            output="Interview complete"
        )
        
        assert result.success
        assert len(workflow.phase_results) == 1
    
    def test_complete_phase_failure(self):
        """RED: Can complete phase with failure."""
        skill = AutopilotSkill()
        workflow = skill.create_workflow("Task")
        
        result = skill.complete_phase(
            workflow,
            AutopilotPhase.PLANNING,
            success=False,
            error="Planning failed"
        )
        
        assert not result.success
        assert "Planning failed" in result.error


class TestReplan:
    """Test replanning."""
    
    def test_should_not_replan_when_all_pass(self):
        """RED: No replan when all phases pass."""
        skill = AutopilotSkill()
        workflow = skill.create_workflow("Task")
        
        # Simulate successful review and QA
        skill.complete_phase(workflow, AutopilotPhase.REVIEW, success=True)
        skill.complete_phase(workflow, AutopilotPhase.QA, success=True)
        
        assert not skill.should_replan(workflow)
    
    def test_should_replan_when_review_fails(self):
        """RED: Replan when review fails."""
        skill = AutopilotSkill()
        workflow = skill.create_workflow("Task")
        
        skill.complete_phase(workflow, AutopilotPhase.REVIEW, success=False)
        
        assert skill.should_replan(workflow)
    
    def test_trigger_replan(self):
        """RED: Can trigger replan."""
        skill = AutopilotSkill()
        workflow = skill.create_workflow("Task")
        
        success = skill.trigger_replan(workflow)
        
        assert success
        assert workflow.replan_count == 1
        assert workflow.status == AutopilotStatus.REPLANNING
        assert workflow.current_phase == AutopilotPhase.PLANNING
    
    def test_replan_limit(self):
        """RED: Respects replan limit."""
        skill = AutopilotSkill()
        workflow = skill.create_workflow("Task")
        workflow.max_replans = 2
        
        # First replan
        assert skill.trigger_replan(workflow)
        # Second replan
        assert skill.trigger_replan(workflow)
        # Third should fail
        assert not skill.trigger_replan(workflow)
        assert workflow.status == AutopilotStatus.BLOCKED


class TestCompletion:
    """Test workflow completion."""
    
    def test_complete_workflow(self):
        """RED: Can complete workflow."""
        skill = AutopilotSkill()
        workflow = skill.create_workflow("Task")
        
        skill.complete_workflow(workflow)
        
        assert workflow.status == AutopilotStatus.COMPLETED
        assert workflow.current_phase == AutopilotPhase.COMPLETE
    
    def test_fail_workflow(self):
        """RED: Can fail workflow."""
        skill = AutopilotSkill()
        workflow = skill.create_workflow("Task")
        
        skill.fail_workflow(workflow)
        
        assert workflow.status == AutopilotStatus.FAILED


class TestReporting:
    """Test reporting."""
    
    def test_generate_report(self):
        """RED: Can generate report."""
        skill = AutopilotSkill()
        workflow = skill.create_workflow("Task")
        
        skill.complete_phase(workflow, AutopilotPhase.INTERVIEW, success=True)
        skill.complete_phase(workflow, AutopilotPhase.PLANNING, success=True)
        skill.complete_workflow(workflow)
        
        report = skill.generate_report(workflow)
        
        assert report.total_phases == 2
        assert report.successful_phases == 2
        assert report.status == AutopilotStatus.COMPLETED
