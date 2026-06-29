"""Domain model for visual QA verdict loop."""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class VerdictStatus(str, Enum):
    PENDING = "pending"
    PASS = "pass"
    FAIL = "fail"
    NEEDS_REVIEW = "needs_review"


@dataclass
class VisualAsset:
    name: str
    asset_type: str  # "reference" or "screenshot"
    path: str
    description: str = ""


@dataclass
class VisualComparison:
    reference: VisualAsset
    screenshot: VisualAsset
    score: float = 0.0  # 0-100
    threshold: float = 90.0
    diff_notes: str = ""
    verdict: VerdictStatus = VerdictStatus.PENDING
    compared_at: datetime = field(default_factory=datetime.now)

    def evaluate(self) -> None:
        if self.score >= self.threshold:
            self.verdict = VerdictStatus.PASS
        elif self.score >= self.threshold * 0.8:
            self.verdict = VerdictStatus.NEEDS_REVIEW
        else:
            self.verdict = VerdictStatus.FAIL

    def passed(self) -> bool:
        return self.verdict == VerdictStatus.PASS


@dataclass
class VisualVerdictSession:
    task_description: str
    threshold: float = 90.0
    comparisons: List[VisualComparison] = field(default_factory=list)
    iteration: int = 1
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.task_description or not self.task_description.strip():
            raise ValueError("Task description cannot be empty")

    def add_comparison(self, comparison: VisualComparison) -> None:
        self.comparisons.append(comparison)

    def all_pass(self) -> bool:
        return bool(self.comparisons) and all(c.passed() for c in self.comparisons)

    def average_score(self) -> float:
        if not self.comparisons:
            return 0.0
        return sum(c.score for c in self.comparisons) / len(self.comparisons)


@dataclass
class VisualVerdictReport:
    task_description: str
    iterations: int
    average_score: float
    passed: bool
    threshold: float = 90.0
    summary: str = ""
