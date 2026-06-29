"""Domain model for OMP state summaries."""

from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class StateSummary:
    """Summary of persisted OMP state files."""

    total_files: int
    wait_state: str = "missing"
    notification_channel: str = "missing"
    team_controls: List[str] = field(default_factory=list)
