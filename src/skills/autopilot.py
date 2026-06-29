"""Autopilot skill for autonomous execution loops."""

from typing import List, Optional, Callable
from domain import (
    AutopilotWorkflow,
    AutopilotPhase,
    AutopilotStatus,
    AutopilotPhaseResult,
    AutopilotReport,
)


class AutopilotSkill:
    """
    Autopilot skill for fully autonomous execution.
    
    Implements the canonical $autopilot workflow:
    deep-interview → ralplan → ultragoal → code-review → ultraqa
    
    Automatically replans when review or QA gates fail.
    """
    
    def __init__(self):
        """Initialize the skill."""
        self.name = "autopilot"
        self.description = "Autonomous execution workflow with auto-replanning"
        self.workflows: dict = {}
    
    def create_workflow(self, task_description: str) -> AutopilotWorkflow:
        """
        Create an autopilot workflow.
        
        Args:
            task_description: Description of the task to execute
            
        Returns:
            An AutopilotWorkflow
        """
        workflow = AutopilotWorkflow(task_description=task_description)
        self.workflows[task_description] = workflow
        workflow.status = AutopilotStatus.IN_PROGRESS
        return workflow
    
    def start_phase(
        self,
        workflow: AutopilotWorkflow,
        phase: AutopilotPhase
    ) -> None:
        """
        Start a workflow phase.
        
        Args:
            workflow: The workflow
            phase: The phase to start
        """
        workflow.current_phase = phase
    
    def complete_phase(
        self,
        workflow: AutopilotWorkflow,
        phase: AutopilotPhase,
        success: bool,
        output: str = "",
        error: str = "",
        duration_seconds: float = 0.0
    ) -> AutopilotPhaseResult:
        """
        Complete a workflow phase.
        
        Args:
            workflow: The workflow
            phase: The phase completed
            success: Whether phase succeeded
            output: Phase output
            error: Any error message
            duration_seconds: Time spent
            
        Returns:
            The AutopilotPhaseResult
        """
        result = AutopilotPhaseResult(
            phase=phase,
            success=success,
            output=output,
            error=error,
            duration_seconds=duration_seconds
        )
        workflow.add_phase_result(result)
        
        return result
    
    def should_replan(self, workflow: AutopilotWorkflow) -> bool:
        """
        Check if replanning is needed.
        
        Based on review and QA phase results.
        
        Args:
            workflow: The workflow
            
        Returns:
            True if replanning needed
        """
        if not workflow.can_replan():
            return False
        
        return workflow.should_replan()
    
    def trigger_replan(self, workflow: AutopilotWorkflow) -> bool:
        """
        Trigger a replan cycle.
        
        Args:
            workflow: The workflow
            
        Returns:
            True if replan triggered successfully
        """
        if not workflow.can_replan():
            workflow.status = AutopilotStatus.BLOCKED
            return False
        
        workflow.replan_count += 1
        workflow.current_phase = AutopilotPhase.PLANNING
        workflow.status = AutopilotStatus.REPLANNING
        return True
    
    def complete_workflow(self, workflow: AutopilotWorkflow) -> None:
        """
        Mark workflow as completed.
        
        Args:
            workflow: The workflow
        """
        workflow.mark_completed()
    
    def fail_workflow(self, workflow: AutopilotWorkflow) -> None:
        """
        Mark workflow as failed.
        
        Args:
            workflow: The workflow
        """
        workflow.status = AutopilotStatus.FAILED
        workflow.completed_at = workflow.created_at  # Mark completion time
    
    def generate_report(self, workflow: AutopilotWorkflow) -> AutopilotReport:
        """
        Generate an autopilot report.
        
        Args:
            workflow: The workflow
            
        Returns:
            An AutopilotReport
        """
        total_phases = len(workflow.phase_results)
        successful = sum(1 for r in workflow.phase_results if r.success)
        
        phase_breakdown = {}
        for phase in AutopilotPhase:
            results = workflow.get_phase_results(phase)
            if results:
                phase_breakdown[phase.value] = all(r.success for r in results)
        
        summary = (
            f"Autopilot completed: {workflow.status.value}. "
            f"Ran {total_phases} phases with {successful} successful. "
            f"Replanned {workflow.replan_count} times."
        )
        
        report = AutopilotReport(
            task_description=workflow.task_description,
            status=workflow.status,
            total_phases=total_phases,
            successful_phases=successful,
            replan_count=workflow.replan_count,
            completed_at=workflow.completed_at,
            summary=summary,
            phase_breakdown=phase_breakdown
        )
        
        return report
    
    def get_workflow(self, task_description: str) -> Optional[AutopilotWorkflow]:
        """Get a workflow by task description."""
        return self.workflows.get(task_description)
    
    def get_all_workflows(self) -> List[AutopilotWorkflow]:
        """Get all workflows."""
        return list(self.workflows.values())
