"""Domain model for OMP project setup."""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List


class ProjectSetupStatus(str, Enum):
    """Status of project setup."""

    INITIALIZED = "initialized"


@dataclass(frozen=True)
class ProjectSetupResult:
    """Result of initializing local OMP project state."""

    status: ProjectSetupStatus
    state_root: Path
    created_paths: List[Path] = field(default_factory=list)
