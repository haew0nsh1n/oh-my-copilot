"""Ralph skill for single-owner persistent completion."""

from typing import Optional, List
from datetime import datetime
from domain import (
    RalphCompletion,
    RalphLoopStatus,
    LoopIteration,
    RalphReport,
)


class RalphSkill:
    """
    A skill for single-owner persistent completion loops.
    
    Unlike Ultragoal (multi-goal ledger), Ralph keeps one owner pushing
    through repeated iterations until completion without formal
    goal tracking.
    """
    
    def __init__(self):
        """Initialize the skill."""
        self.name = "ralph"
        self.description = "Single-owner persistent completion loop"
        self.completions: dict = {}
    
    def create_completion(
        self,
        task_title: str,
        owner: str,
        description: str = ""
    ) -> RalphCompletion:
        """
        Create a completion loop.
        
        Args:
            task_title: Task title
            owner: Task owner
            description: Task description
            
        Returns:
            A RalphCompletion
        """
        completion = RalphCompletion(
            task_title=task_title,
            owner=owner,
            description=description
        )
        self.completions[task_title] = completion
        return completion
    
    def start_iteration(
        self,
        completion: RalphCompletion,
        description: str
    ) -> LoopIteration:
        """
        Start a new iteration.
        
        Args:
            completion: The completion loop
            description: Iteration description
            
        Returns:
            A LoopIteration
        """
        if not completion.can_continue():
            raise RuntimeError(f"Max iterations ({completion.max_iterations}) reached")
        
        return completion.add_iteration(description)
    
    def complete_iteration(
        self,
        iteration: LoopIteration,
        success: bool = True,
        output: str = ""
    ) -> None:
        """
        Complete an iteration.
        
        Args:
            iteration: The iteration
            success: Whether successful
            output: Iteration output
        """
        iteration.complete(success, output)
    
    def fail_iteration(
        self,
        iteration: LoopIteration,
        error: str = ""
    ) -> None:
        """
        Mark iteration as failed.
        
        Args:
            iteration: The iteration
            error: Error message
        """
        iteration.complete(success=False, output="")
        iteration.error = error
    
    def is_loop_complete(self, completion: RalphCompletion) -> bool:
        """
        Check if loop can be marked complete.
        
        Args:
            completion: The completion loop
            
        Returns:
            True if loop should end
        """
        # Loop is complete when we have successful iterations
        # and owner decides it's done
        return (
            len(completion.get_successful_iterations()) > 0 and
            completion.status in [RalphLoopStatus.IN_PROGRESS, RalphLoopStatus.COMPLETED]
        )
    
    def mark_complete(self, completion: RalphCompletion) -> None:
        """
        Mark loop as complete.
        
        Args:
            completion: The completion loop
        """
        completion.mark_completed()
    
    def mark_failed(self, completion: RalphCompletion) -> None:
        """
        Mark loop as failed.
        
        Args:
            completion: The completion loop
        """
        completion.status = RalphLoopStatus.FAILED
        completion.completed_at = datetime.now()
    
    def generate_report(self, completion: RalphCompletion) -> RalphReport:
        """
        Generate a completion report.
        
        Args:
            completion: The completion loop
            
        Returns:
            A RalphReport
        """
        successful = completion.get_successful_iterations()
        
        summary = (
            f"Loop completed with {len(successful)} successful iterations "
            f"out of {len(completion.iterations)} total."
        )
        
        report = RalphReport(
            task_title=completion.task_title,
            owner=completion.owner,
            status=completion.status,
            total_iterations=len(completion.iterations),
            successful_iterations=len(successful),
            completed_at=completion.completed_at,
            summary=summary
        )
        
        return report
    
    def get_completion(self, task_title: str) -> Optional[RalphCompletion]:
        """Get a completion by task title."""
        return self.completions.get(task_title)
    
    def get_all_completions(self) -> List[RalphCompletion]:
        """Get all completions."""
        return list(self.completions.values())
