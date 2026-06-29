"""RalPlan skill for architecture planning with approval."""

from typing import List, Callable
from datetime import datetime
from domain import (
    ArchitecturePlan,
    PlanStatus,
    ReviewRole,
    ReviewEvidence,
    RalPlanReport,
)


class RalPlanSkill:
    """
    A skill for planning and approval with architecture-level decisions.
    
    Combines clarified requirements with Architect and Critic consensus
    to produce an approved architecture and implementation plan.
    """
    
    def __init__(self):
        """Initialize the skill."""
        self.name = "ralplan"
        self.description = "Architecture planning with Architect→Critic approval"
        self.plans: dict = {}
    
    def create_plan(
        self,
        title: str,
        description: str,
        requirements: List[str] = None
    ) -> ArchitecturePlan:
        """
        Create an architecture plan.
        
        Args:
            title: Plan title
            description: Plan description
            requirements: List of requirements
            
        Returns:
            An ArchitecturePlan
        """
        plan = ArchitecturePlan(
            title=title,
            description=description,
            requirements=requirements or []
        )
        self.plans[title] = plan
        return plan
    
    def add_design_decision(
        self,
        plan: ArchitecturePlan,
        decision: str
    ) -> None:
        """
        Add a design decision.
        
        Args:
            plan: The plan
            decision: The design decision
        """
        plan.design_decisions.append(decision)
    
    def add_implementation_step(
        self,
        plan: ArchitecturePlan,
        step: str
    ) -> None:
        """
        Add an implementation step.
        
        Args:
            plan: The plan
            step: The implementation step
        """
        plan.implementation_steps.append(step)
    
    def add_risk(
        self,
        plan: ArchitecturePlan,
        risk: str
    ) -> None:
        """
        Add a risk.
        
        Args:
            plan: The plan
            risk: The risk
        """
        plan.risks.append(risk)
    
    def add_tradeoff(
        self,
        plan: ArchitecturePlan,
        tradeoff: str
    ) -> None:
        """
        Add a tradeoff.
        
        Args:
            plan: The plan
            tradeoff: The tradeoff
        """
        plan.tradeoffs.append(tradeoff)
    
    def submit_architect_review(
        self,
        plan: ArchitecturePlan,
        verdict: str,
        reasoning: str,
        architect_name: str = "Architect"
    ) -> ReviewEvidence:
        """
        Submit architect review.
        
        Args:
            plan: The plan
            verdict: Approved/Rejected
            reasoning: Reasoning
            architect_name: Name of architect
            
        Returns:
            ReviewEvidence
        """
        evidence = ReviewEvidence(
            role=ReviewRole.ARCHITECT,
            reviewer=architect_name,
            verdict=verdict,
            reasoning=reasoning
        )
        plan.add_evidence(evidence)
        
        if plan.is_architect_approved():
            plan.status = PlanStatus.CRITIC_REVIEW
        else:
            plan.status = PlanStatus.REJECTED
        
        return evidence
    
    def submit_critic_review(
        self,
        plan: ArchitecturePlan,
        verdict: str,
        reasoning: str,
        critic_name: str = "Critic"
    ) -> ReviewEvidence:
        """
        Submit critic review.
        
        Args:
            plan: The plan
            verdict: Approved/Rejected
            reasoning: Reasoning
            critic_name: Name of critic
            
        Returns:
            ReviewEvidence
        """
        evidence = ReviewEvidence(
            role=ReviewRole.CRITIC,
            reviewer=critic_name,
            verdict=verdict,
            reasoning=reasoning
        )
        plan.add_evidence(evidence)
        
        if plan.is_architect_approved() and plan.is_critic_approved():
            plan.status = PlanStatus.APPROVED
            plan.approved_at = datetime.now()
        elif not plan.is_critic_approved():
            plan.status = PlanStatus.REJECTED
        
        return evidence
    
    def generate_report(self, plan: ArchitecturePlan) -> RalPlanReport:
        """
        Generate a plan report.
        
        Args:
            plan: The plan
            
        Returns:
            A RalPlanReport
        """
        architect_evidence = plan.get_architect_evidence()
        critic_evidence = plan.get_critic_evidence()
        
        report = RalPlanReport(
            plan=plan,
            status=plan.status,
            architect_verdict=architect_evidence.verdict if architect_evidence else None,
            critic_verdict=critic_evidence.verdict if critic_evidence else None,
            ready_for_execution=plan.is_ready_for_execution(),
            next_steps=[
                "Proceed to ultragoal execution" if plan.is_ready_for_execution()
                else "Address architect and critic feedback"
            ]
        )
        
        return report
    
    def get_plan(self, title: str) -> ArchitecturePlan:
        """Get a plan by title."""
        return self.plans.get(title)
    
    def get_all_plans(self) -> List[ArchitecturePlan]:
        """Get all plans."""
        return list(self.plans.values())
