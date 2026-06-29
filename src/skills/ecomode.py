"""Ecomode skill — token-efficient model routing."""

from typing import Optional
from domain import (
    EcomodeSession, RoutingRule, TokenUsage,
    ModelTier, TaskComplexity, EcomodeReport,
)


class EcomodeSkill:
    name = "ecomode"
    description = "Token-efficient model routing — match task complexity to model tier"

    def __init__(self):
        self.sessions: dict = {}

    def create_session(self, goal: str, default_tier: ModelTier = ModelTier.MEDIUM) -> EcomodeSession:
        session = EcomodeSession(goal=goal, default_tier=default_tier)
        self.sessions[goal] = session
        return session

    def add_rule(self, session: EcomodeSession, task_pattern: str, tier: ModelTier, rationale: str) -> RoutingRule:
        rule = RoutingRule(task_pattern=task_pattern, recommended_tier=tier, rationale=rationale)
        session.add_rule(rule)
        return rule

    def route(self, session: EcomodeSession, task: str, complexity: TaskComplexity) -> ModelTier:
        return session.route_task(task, complexity)

    def record_usage(self, session: EcomodeSession, task: str, tier: ModelTier, estimated_tokens: int, actual_tokens: int = 0) -> TokenUsage:
        # Estimate savings vs always using HIGH
        tier_multipliers = {ModelTier.LOW: 0.1, ModelTier.MEDIUM: 0.4, ModelTier.HIGH: 1.0}
        savings = (1.0 - tier_multipliers.get(tier, 1.0)) * 100.0
        usage = TokenUsage(
            task_description=task,
            model_tier=tier,
            estimated_tokens=estimated_tokens,
            actual_tokens=actual_tokens,
            cost_saving_vs_high=savings
        )
        session.record_usage(usage)
        return usage

    def generate_report(self, session: EcomodeSession) -> EcomodeReport:
        breakdown: dict = {}
        for u in session.token_usages:
            breakdown[u.model_tier.value] = breakdown.get(u.model_tier.value, 0) + 1
        return EcomodeReport(
            goal=session.goal,
            total_tasks=len(session.token_usages),
            total_estimated_tokens=session.total_estimated_tokens(),
            average_savings_pct=session.average_savings(),
            tier_breakdown=breakdown,
            summary=f"Avg {session.average_savings():.1f}% savings vs always-high over {len(session.token_usages)} tasks"
        )

    def get_session(self, goal: str) -> Optional[EcomodeSession]:
        return self.sessions.get(goal)
