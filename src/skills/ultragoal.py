"""Ultragoal skill for durable multi-goal execution."""

from typing import List
from domain import (
    Ultragoal,
    Goal,
    GoalCheckpoint,
    UltragoalReport,
    GoalStatus,
    GoalPriority,
)


class UltragoalSkill:
    """
    A skill for durable multi-goal execution.
    
    This skill turns an approved plan into sequential goals with checkpoints
    and progress tracking.
    """
    
    def __init__(self):
        """Initialize the ultragoal skill."""
        self.name = "ultragoal"
        self.description = "Turn approved plans into durable multi-goal execution with checkpoints"
    
    def create_ultragoal(
        self,
        name: str,
        description: str,
        metadata: dict = None
    ) -> Ultragoal:
        """
        Create a new ultragoal.
        
        Args:
            name: Name of the ultragoal
            description: Description of what it achieves
            metadata: Optional metadata (plan info, context, etc.)
            
        Returns:
            A new Ultragoal
        """
        return Ultragoal(
            name=name,
            description=description,
            metadata=metadata or {}
        )
    
    def create_goal(
        self,
        title: str,
        description: str,
        priority: GoalPriority = GoalPriority.MEDIUM,
        criteria: List[str] = None,
        owner: str = ""
    ) -> Goal:
        """
        Create a goal for an ultragoal.
        
        Args:
            title: Goal title
            description: Goal description
            priority: Goal priority
            criteria: Acceptance criteria
            owner: Goal owner
            
        Returns:
            A new Goal
        """
        goal = Goal(
            title=title,
            description=description,
            priority=priority,
            owner=owner
        )
        
        if criteria:
            for criterion in criteria:
                goal.add_criterion(criterion)
        
        return goal
    
    def add_goal(
        self,
        ultragoal: Ultragoal,
        goal: Goal
    ) -> None:
        """
        Add a goal to an ultragoal.
        
        Args:
            ultragoal: The ultragoal
            goal: The goal to add
        """
        ultragoal.add_goal(goal)
    
    def create_checkpoint(
        self,
        name: str,
        description: str
    ) -> GoalCheckpoint:
        """
        Create a checkpoint for a goal.
        
        Args:
            name: Checkpoint name
            description: Checkpoint description
            
        Returns:
            A new GoalCheckpoint
        """
        return GoalCheckpoint(
            name=name,
            description=description
        )
    
    def add_checkpoint(
        self,
        goal: Goal,
        checkpoint: GoalCheckpoint
    ) -> None:
        """
        Add a checkpoint to a goal.
        
        Args:
            goal: The goal
            checkpoint: The checkpoint to add
        """
        goal.add_checkpoint(checkpoint)
    
    def start_goal(self, goal: Goal) -> None:
        """
        Start working on a goal.
        
        Args:
            goal: The goal to start
        """
        goal.start()
    
    def complete_checkpoint(
        self,
        checkpoint: GoalCheckpoint,
        notes: str = ""
    ) -> None:
        """
        Mark a checkpoint as complete.
        
        Args:
            checkpoint: The checkpoint
            notes: Verification notes
        """
        checkpoint.mark_complete(notes)
    
    def complete_goal(self, goal: Goal) -> None:
        """
        Mark a goal as complete.
        
        Args:
            goal: The goal to complete
        """
        goal.complete()
    
    def block_goal(self, goal: Goal) -> None:
        """
        Mark a goal as blocked.
        
        Args:
            goal: The goal to block
        """
        goal.block()
    
    def fail_goal(self, goal: Goal) -> None:
        """
        Mark a goal as failed.
        
        Args:
            goal: The goal that failed
        """
        goal.fail()
    
    def complete_ultragoal(self, ultragoal: Ultragoal) -> None:
        """
        Mark an ultragoal as complete.
        
        Args:
            ultragoal: The ultragoal to complete
        """
        ultragoal.status = GoalStatus.COMPLETED
        ultragoal.completed_at = __import__('datetime').datetime.now()
    
    def generate_report(self, ultragoal: Ultragoal) -> UltragoalReport:
        """
        Generate a progress report for an ultragoal.
        
        Args:
            ultragoal: The ultragoal
            
        Returns:
            An UltragoalReport
        """
        completed = len(ultragoal.get_completed_goals())
        in_progress = len(ultragoal.get_in_progress_goals())
        pending = len(ultragoal.get_pending_goals())
        blocked = len(ultragoal.get_blocked_goals())
        total = len(ultragoal.goals)
        
        completion_pct = ultragoal.completion_percentage()
        
        summary = f"Ultragoal '{ultragoal.name}': "
        summary += f"{completion_pct:.0f}% complete "
        summary += f"({completed}/{total} goals done)"
        
        if blocked > 0:
            summary += f", {blocked} blocked"
        
        return UltragoalReport(
            ultragoal=ultragoal,
            total_goals=total,
            completed_goals=completed,
            in_progress_goals=in_progress,
            pending_goals=pending,
            blocked_goals=blocked,
            completion_percentage=completion_pct,
            summary=summary
        )
