"""Domain model for provider advisor requests."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path


class ProviderName(str, Enum):
    """Supported provider advisor targets."""

    CLAUDE = "claude"
    CODEX = "codex"
    GEMINI = "gemini"
    ANTIGRAVITY = "antigravity"
    GROK = "grok"
    CURSOR = "cursor"


class ProviderAdvisorStatus(str, Enum):
    """Status of a provider advisor request."""

    PREPARED = "prepared"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True)
class ProviderAvailability:
    """Provider CLI availability check result."""

    provider: ProviderName
    status: ProviderAdvisorStatus
    executable_path: str = ""


@dataclass
class ProviderAdviceRequest:
    """A prepared request for an external provider advisor."""

    provider: ProviderName
    prompt: str
    status: ProviderAdvisorStatus = ProviderAdvisorStatus.PREPARED
    command_preview: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not self.prompt or not self.prompt.strip():
            raise ValueError("Prompt cannot be empty")
        if not self.command_preview:
            self.command_preview = f"{self.provider.value} {self.prompt}"


@dataclass(frozen=True)
class ProviderExecutionResult:
    """Result from executing a provider CLI adapter."""

    provider: ProviderName
    status: ProviderAdvisorStatus
    exit_code: int | None = None
    output_summary: str = ""
    error_summary: str = ""


@dataclass(frozen=True)
class ProviderAdviceArtifact:
    """Recorded provider advice artifact."""

    provider: ProviderName
    path: Path
