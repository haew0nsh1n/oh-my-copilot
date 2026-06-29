"""Domain model for local session friction reports."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List


class FrictionSignalType(str, Enum):
    """Kinds of local session friction signals."""

    CONTEXT_BLOAT = "context-bloat"
    OPERATOR_FRICTION = "operator-friction"
    TOOL_RETRY = "tool-retry"
    VALIDATION_FAILURE = "validation-failure"


@dataclass(frozen=True)
class FrictionSignal:
    """A sanitized friction signal without raw prompts or tool output."""

    signal_type: FrictionSignalType
    summary: str
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not self.summary or not self.summary.strip():
            raise ValueError("Signal summary cannot be empty")


@dataclass
class SessionFrictionSession:
    """A local friction reporting session."""

    since: str
    signals: List[FrictionSignal] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.since or not self.since.strip():
            raise ValueError("Since value cannot be empty")

    def add_signal(self, signal: FrictionSignal) -> None:
        self.signals.append(signal)


@dataclass(frozen=True)
class SessionFrictionReport:
    """Summary report for local session friction."""

    since: str
    total_signals: int
    signal_breakdown: Dict[str, int] = field(default_factory=dict)
    summary: str = ""
