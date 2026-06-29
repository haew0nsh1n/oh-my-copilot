"""Domain model for token-efficient model routing."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime


class ModelTier(str, Enum):
    LOW = "low"       # Fast, cheap, simple tasks
    MEDIUM = "medium" # Balanced for most tasks
    HIGH = "high"     # Slow, expensive, complex reasoning


class TaskComplexity(str, Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"


@dataclass
class RoutingRule:
    task_pattern: str
    recommended_tier: ModelTier
    rationale: str


@dataclass
class TokenUsage:
    task_description: str
    model_tier: ModelTier
    estimated_tokens: int
    actual_tokens: int = 0
    cost_saving_vs_high: float = 0.0  # % saved vs always using HIGH
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class EcomodeSession:
    goal: str
    routing_rules: List[RoutingRule] = field(default_factory=list)
    token_usages: List[TokenUsage] = field(default_factory=list)
    default_tier: ModelTier = ModelTier.MEDIUM
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.goal or not self.goal.strip():
            raise ValueError("Goal cannot be empty")

    def add_rule(self, rule: RoutingRule) -> None:
        self.routing_rules.append(rule)

    def route_task(self, task: str, complexity: TaskComplexity) -> ModelTier:
        tier_map = {
            TaskComplexity.SIMPLE: ModelTier.LOW,
            TaskComplexity.MODERATE: ModelTier.MEDIUM,
            TaskComplexity.COMPLEX: ModelTier.HIGH,
        }
        return tier_map.get(complexity, self.default_tier)

    def record_usage(self, usage: TokenUsage) -> None:
        self.token_usages.append(usage)

    def total_estimated_tokens(self) -> int:
        return sum(u.estimated_tokens for u in self.token_usages)

    def average_savings(self) -> float:
        if not self.token_usages:
            return 0.0
        return sum(u.cost_saving_vs_high for u in self.token_usages) / len(self.token_usages)


@dataclass
class EcomodeReport:
    goal: str
    total_tasks: int = 0
    total_estimated_tokens: int = 0
    average_savings_pct: float = 0.0
    tier_breakdown: Dict[str, int] = field(default_factory=dict)
    summary: str = ""
