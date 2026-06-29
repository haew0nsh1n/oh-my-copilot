"""Domain model for rate-limit wait guidance."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path


class WaitAction(str, Enum):
    """Rate-limit wait action requested by the user."""

    CHECK = "check"
    START = "start"
    STOP = "stop"


class WaitStatus(str, Enum):
    """Status of a rate-limit wait action."""

    READY = "ready"
    PREPARED = "prepared"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class RateLimitWaitResult:
    """Result of a rate-limit wait action."""

    action: WaitAction
    status: WaitStatus
    guidance: str
    tmux_required: bool = True
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not self.guidance or not self.guidance.strip():
            raise ValueError("Guidance cannot be empty")


@dataclass(frozen=True)
class RateLimitWaitStateArtifact:
    """Persisted rate-limit wait state artifact."""

    path: Path
