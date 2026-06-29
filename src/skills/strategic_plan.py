"""Strategic planning skill for high-level planning."""

from typing import List, Optional
from domain import (
    StrategicPlan,
    PlanObjective,
    PlanPhase,
    PlanStatus,
    StrategicPlanReport,
)


class StrategicPlanSkill:
    """
    A skill for strategic planning.
    
    Unlike RalPlan (detailed architecture), this is for simpler,
    high-level strategic planning with vision, goals, and objectives.
    """
    
    def __init__(self):
        """Initialize the skill."""
        self.name = "plan"
        self.description = "Strategic planning for high-level vision"
        self.plans: dict = {}
    
    def create_plan(
        self,
        title: str,
        vision: str
    ) -> StrategicPlan:
        """
        Create a strategic plan.
        
        Args:
            title: Plan title
            vision: Vision statement
            
        Returns:
            A StrategicPlan
        """
        plan = StrategicPlan(title=title, vision=vision)
        self.plans[title] = plan
        return plan
    
    def add_goal(
        self,
        plan: StrategicPlan,
        goal: str
    ) -> None:
        """
        Add a goal to the plan.
        
        Args:
            plan: The plan
            goal: Goal description
        """
        plan.add_goal(goal)
    
    def add_objective(
        self,
        plan: StrategicPlan,
        title: str,
        description: str,
        phase: PlanPhase = PlanPhase.STRATEGY,
        estimated_hours: float = 0.0
    ) -> PlanObjective:
        """
        Add an objective to the plan.
        
        Args:
            plan: The plan
            title: Objective title
            description: Objective description
            phase: Which phase
            estimated_hours: Estimated hours
            
        Returns:
            A PlanObjective
        """
        objective = PlanObjective(
            title=title,
            description=description,
            phase=phase,
            estimated_hours=estimated_hours
        )
        plan.add_objective(objective)
        return objective
    
    def add_constraint(
        self,
        plan: StrategicPlan,
        constraint: str
    ) -> None:
        """
        Add a constraint.
        
        Args:
            plan: The plan
            constraint: Constraint description
        """
        plan.add_constraint(constraint)
    
    def add_assumption(
        self,
        plan: StrategicPlan,
        assumption: str
    ) -> None:
        """
        Add an assumption.
        
        Args:
            plan: The plan
            assumption: Assumption description
        """
        plan.add_assumption(assumption)
    
    def approve_plan(
        self,
        plan: StrategicPlan,
        notes: str = ""
    ) -> None:
        """
        Approve a plan.
        
        Args:
            plan: The plan
            notes: Approval notes
        """
        plan.mark_approved(notes)
    
    def get_discovery_objectives(self, plan: StrategicPlan) -> List[PlanObjective]:
        """Get discovery phase objectives."""
        return plan.get_objectives_by_phase(PlanPhase.DISCOVERY)
    
    def get_strategy_objectives(self, plan: StrategicPlan) -> List[PlanObjective]:
        """Get strategy phase objectives."""
        return plan.get_objectives_by_phase(PlanPhase.STRATEGY)
    
    def get_execution_objectives(self, plan: StrategicPlan) -> List[PlanObjective]:
        """Get execution phase objectives."""
        return plan.get_objectives_by_phase(PlanPhase.EXECUTION)
    
    def get_validation_objectives(self, plan: StrategicPlan) -> List[PlanObjective]:
        """Get validation phase objectives."""
        return plan.get_objectives_by_phase(PlanPhase.VALIDATION)
    
    def generate_report(self, plan: StrategicPlan) -> StrategicPlanReport:
        """
        Generate a plan report.
        
        Args:
            plan: The plan
            
        Returns:
            A StrategicPlanReport
        """
        summary = (
            f"Strategic plan '{plan.title}': "
            f"{len(plan.goals)} goals, "
            f"{len(plan.objectives)} objectives, "
            f"{plan.get_total_estimated_hours():.1f} estimated hours"
        )
        
        report = StrategicPlanReport(
            title=plan.title,
            vision=plan.vision,
            status=plan.status,
            goal_count=len(plan.goals),
            objective_count=len(plan.objectives),
            total_estimated_hours=plan.get_total_estimated_hours(),
            summary=summary
        )
        
        return report
    
    def get_plan(self, title: str) -> Optional[StrategicPlan]:
        """Get a plan by title."""
        return self.plans.get(title)
    
    def get_all_plans(self) -> List[StrategicPlan]:
        """Get all plans."""
        return list(self.plans.values())
