"""Domain model for max-parallel execution."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime


class UltraworkStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class LaneStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    DONE = "done"
    FAILED = "failed"


@dataclass
class WorkLane:
    lane_id: str
    description: str
    worker_hint: str = ""
    status: LaneStatus = LaneStatus.PENDING
    output: str = ""
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def start(self) -> None:
        self.status = LaneStatus.ACTIVE
        self.started_at = datetime.now()

    def complete(self, output: str = "") -> None:
        self.status = LaneStatus.DONE
        self.output = output
        self.completed_at = datetime.now()

    def fail(self, reason: str = "") -> None:
        self.status = LaneStatus.FAILED
        self.output = reason
        self.completed_at = datetime.now()


@dataclass
class UltraworkSession:
    goal: str
    lanes: List[WorkLane] = field(default_factory=list)
    status: UltraworkStatus = UltraworkStatus.IDLE
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.goal or not self.goal.strip():
            raise ValueError("Goal cannot be empty")

    def add_lane(self, lane: WorkLane) -> None:
        self.lanes.append(lane)

    def get_active_lanes(self) -> List[WorkLane]:
        return [l for l in self.lanes if l.status == LaneStatus.ACTIVE]

    def get_completed_lanes(self) -> List[WorkLane]:
        return [l for l in self.lanes if l.status == LaneStatus.DONE]

    def completion_rate(self) -> float:
        if not self.lanes:
            return 0.0
        return len(self.get_completed_lanes()) / len(self.lanes)

    def all_done(self) -> bool:
        return all(l.status in (LaneStatus.DONE, LaneStatus.FAILED) for l in self.lanes)


@dataclass
class UltraworkReport:
    goal: str
    status: UltraworkStatus
    total_lanes: int = 0
    completed_lanes: int = 0
    failed_lanes: int = 0
    summary: str = ""
