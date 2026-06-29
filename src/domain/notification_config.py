"""Domain model for notification callback configuration."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List


class NotificationChannel(str, Enum):
    """Supported notification callback channels."""

    TELEGRAM = "telegram"
    DISCORD = "discord"
    SLACK = "slack"
    FILE = "file"
    OPENCLAW = "openclaw"


class NotificationConfigStatus(str, Enum):
    """Status of a notification configuration request."""

    PREPARED = "prepared"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class NotificationCallbackConfig:
    """Prepared callback configuration without storing secrets."""

    channel: NotificationChannel
    tag_list: List[str] = field(default_factory=list)
    status: NotificationConfigStatus = NotificationConfigStatus.PREPARED
    command_preview: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not self.command_preview:
            object.__setattr__(
                self,
                "command_preview",
                f"omp config-stop-callback {self.channel.value}",
            )


@dataclass(frozen=True)
class NotificationConfigArtifact:
    """Persisted notification configuration artifact."""

    channel: NotificationChannel
    path: Path
